import json
import base64
import re
import datetime as pydatetime

from geodesic.account.projects import Project, get_project
from geodesic.bases import APIObject, reset_attr
from dateutil.parser import isoparse
from geodesic.bases import APIObject

from geodesic.service import ServiceClient
from dateutil.parser import parse

from collections import defaultdict

from geodesic.client import get_client, raise_on_error
from geodesic.account import get_active_project
from geodesic.entanglement import Object
from geodesic.stac import FeatureCollection
from geodesic.widgets import get_template_env, jinja_available
import numpy as np
from geodesic.utils import datetime_to_utc

from shapely.geometry import shape, box
try:
    import pyproj
except ImportError:
    pyproj = None

from typing import Any, Optional, Union, List, Tuple

datasets_client = ServiceClient('entanglement', 1, 'datasets')
stac_client = ServiceClient('spacetime', 1, 'stac')
boson_client = ServiceClient('boson', 1, 'proxy')

stac_root_re = re.compile(r'(.*)\/collections\/')


def list_datasets(ids: Union[List, str] = [], 
                  search: str = None, 
                  project=None, 
                  version_datetime: Union[str, pydatetime.datetime] = None):
    if project is None:
        project = get_active_project()
    else:
        if isinstance(project, str):
            project = get_project(project)
        elif not isinstance(project, Project):
            raise ValueError("project must be a string or Project")

    params = {}
    if ids:
        if isinstance(ids, str):
            ids = ids.split(",")
        params['ids'] = ",".join(ids)

    if search is not None:
        params['search'] = search

    params['project'] = project.name
    # Find object versions that were valid at a specific datetime
    if version_datetime is not None:
        # check for valid format
        if isinstance(version_datetime, str):
            params['datetime'] = datetime_to_utc(isoparse(version_datetime)).isoformat()
        elif isinstance(version_datetime, pydatetime.datetime):
            params['datetime'] = datetime_to_utc(version_datetime).isoformat()
        else:
            raise ValueError("version_datetime must either be RCF3339 formatted string, or datetime.datetime")

    resp = datasets_client.get('', **params)
    raise_on_error(resp)

    js = resp.json()
    if js['datasets'] is None:
        return DatasetList([])

    ds = [Dataset(**r) for r in js["datasets"]]
    datasets = DatasetList(ds, ids=ids)
    return datasets


class Dataset(Object):
    """Allows interaction with SeerAI datasets.

    Dataset provides a way to interact with datasets in the SeerAI.

    Args:
        **spec (dict): Dictionary with all properties in the dataset
    """

    def __init__(self, **obj):
        self._boson = None

        o = {'class': "dataset"}
        # If this came from the dataset API, this needs to be built as an object
        if 'item' not in obj:
            o['item'] = obj
            uid = obj.get('uid')
            if uid is not None:
                o['uid'] = uid
            o['name'] = obj.get('name', None)

            o['class'] = "dataset"
            o['domain'] = obj.get('domain', "*")
            o['category'] = obj.get('category', "*")
            o['type'] = obj.get('type', "*")
            o['description'] = obj.get('description', '')
            o['keywords'] = obj.get('keywords', [])

            # geom from extent
            e = obj.get('extent', {})
            se = e.get('spatial', None)
            if se is not None:
                g = box(*se, ccw=False)
                self.geometry = g

            o.update(obj.get('entanglement', {}))

        # Otherwise, parse as object
        else:
            obj['item']['uid'] = obj['uid']
            o = obj

        project = o.get('item', {}).get('project', None)

        super(Dataset, self).__init__(**o)
        if project is not None:
            self.project = project

    def validate(self):
        body = json.dumps(self.item)

        res = self._client.post(
            "datasets/validate",
            body=base64.b64encode(body.encode()).decode(),
            format="json",
            project=self.project
        )

        try:
            raise_on_error(res)
        except Exception:
            try:
                print(res.json()['error'])
            except Exception:
                print(res.text)
            return False

        return True

    @property
    def object_class(self):
        return "Dataset"

    @object_class.setter
    def object_class(self, v):
        if v.lower() != "dataset":
            raise ValueError("shouldn't happen")
        self._set_item('class', 'dataset')

    @property
    def dataset_type(self):
        return self.item['type']

    @dataset_type.setter
    def dataset_type(self, v: str):
        if not isinstance(v, str):
            raise ValueError("dataset_type must be a string")
        self.item['type'] = v

    @property
    def dataset_subtype(self):
        return self.item["subtype"]

    @dataset_subtype.setter
    def dataset_subtype(self, v: str):
        if not isinstance(v, str):
            raise ValueError("dataset_subtype must be a string")
        self.item['subtype'] = v

    @property
    def boson(self):
        if self._boson is not None:
            return self._boson

        b = self.item.get("boson", None)
        if b is None:
            b = {}
            self.boson = b
            return b

        self._boson = Boson(**self.item["boson"])
        return self._boson

    @boson.setter
    @reset_attr
    def boson(self, v: dict):
        self.item['boson'] = Boson(**v)

    @property
    def stac(self):
        stac = self.item.get("stac", {})
        if not stac:
            self.item['stac'] = stac
        return stac

    @stac.setter
    def stac(self, v: dict):
        if not isinstance(v, dict):
            raise ValueError("stac must be a dict")
        self.item['stac'] = v

    @property
    def clients(self):
        return self.item.get("clients", [])

    @clients.setter
    def clients(self, v: list):
        if not isinstance(v, list):
            raise ValueError("clients must be a list of strings")
        self.item['clients'] = v

    @property
    def alias(self):
        return self.item.get("alias", self.name)

    @alias.setter
    def alias(self, v: str):
        if not isinstance(v, str):
            raise ValueError('alias must be a string')
        self.item["alias"] = v

    @property
    def item_assets(self):
        return ItemAssets(item_assets=self.stac['itemAssets'], ds_name=self.alias)

    @item_assets.setter
    def item_assets(self, v: dict):
        if not isinstance(v, dict):
            raise ValueError("item assets must be a dict")
        self.stac['itemAssets'] = v

    @property
    def bands(self):
        """
        Alias for item_assets
        """
        return self.item_assets

    def _repr_html_(self, add_style=True):
        if not jinja_available():
            return self.__repr__()

        template = get_template_env().get_template("dataset_template.html.jinja")
        # Make this look like dataset list but with a single entry so one template can be used for both
        dataset = {self.name: self}
        return template.render(datasets=dataset)

    def query(
        self,
        bbox: Optional[List] = None,
        datetime: Union[List, Tuple] = None,
        limit: Optional[Union[bool, int]] = 10,
        intersects: Optional[object] = None,
        **kwargs
    ):
        """ Query the dataset for items.

        Query this service's OGC Features or STAC API.

        Args:
            bbox: The spatial extent for the query as a bounding box. Example: [-180, -90, 180, 90]
            datetime: The temporal extent for the query formatted as a list: [start, end].
            limit: The maximum number of items to return in the query.

        Returns:
            A :class:`geodesic.stac.FeatureCollection` with all items in the dataset matching the query.

        Examples:
            A query on the `sentinel-2-l2a` dataset with a given bouding box and time range. Additionally it
            you can apply filters on the parameters in the items.

            >>> bbox = geom.bounds
            >>> date_range = (datetime.datetime(2020, 12,1), datetime.datetime.now())
            >>> ds.query(
            ...          bbox=bbox,
            ...          datetime=date_range,
            ...          query={'properties.eo:cloud_cover': {'lte': 10}}
            ... )
        """
        # STAC client is for Spacetime requests
        client = stac_client

        # No prefix needed for Spacetime queries
        url_prefix = ''
        project = self.project

        # STAC Collection <=> Dataset name
        collection = self.name

        # If this Dataset is a boson, the url needs to be crafted slightly differently.
        # Specifically, it needs the servicer and dataset config fragment prefixed to the
        # STAC/OGC Features url fragment
        if self.boson:
            if 'collection' in self.boson.properties:
                collection = self.boson.properties['collection']
            client = boson_client
            url_prefix = f'stac/{self.name}.{project}/'

        api = kwargs.get("api", None)
        # clients = self.clients

        if api is None:
            api = "stac"

        query_all = False
        if not limit:
            limit = 500
            query_all = True

        # Request query/body
        params = {"limit": limit, 'project': project}

        if api == "features":
            url = url_prefix + f"collections/{collection}/items"
        elif api == "stac":
            params["collections"] = [collection]
            url = url_prefix + "search"
        else:
            raise ValueError(f"specified api must be either 'features' or 'stac', got '{api}'")

        # Parse geospatial aspect of this query (bbox and intersects)
        params = self._query_parse_geometry(params, api, bbox, intersects)

        # Parse STAC search specific query/filtering
        if api == "stac":
            params = self._query_parse_stac_query(params, api, kwargs)

        if datetime is not None:
            params["datetime"] = "/".join([parsedate(d).isoformat() for d in datetime])

        if api == "features":
            res = raise_on_error(client.get(url, **params))
        elif api == "stac":
            res = raise_on_error(client.post(url, **params))

        # Wrap the results in a FeatureCollection
        collection = FeatureCollection(obj=res.json(), dataset=self, query=params)

        # If query_all, this cycles through all pages and reads into the feature collection.
        if query_all:
            collection.get_all()

        # Set a flag on the collection denoting that STAC capabilities are available.
        if api == "stac":
            collection._is_stac = True

        return collection

    def _query_parse_geometry(self, params: dict, api: str, bbox: Optional[list], intersects: object) -> dict:
        """
        For a STAC/OGC Features query, parse the bbox/geometry depending on the API type

        Arguments:
            params: the dictionary of parameters we are updated for the query. Modified inplace, but also returned.
            api: the type of api for the call we are building
            bbox: the four corners of a geospatial bounding box
            intersects: a geometry object or something that satisfies the geointerface spec

        Returns:
            params

        """
        # If the bounding box only provided.
        if bbox is not None and intersects is None:
            if api == "stac":
                params["bbox"] = bbox
            else:
                params["bbox"] = ",".join(map(str, bbox))
        # If a intersection geometry was provided
        if intersects is not None:
            # Geojson
            if isinstance(intersects, dict):
                try:
                    g = shape(intersects)
                except ValueError:
                    try:
                        g = shape(intersects['geometry'])
                    except Exception as e:
                        raise ValueError('could not determine type of intersection geometry') from e

            elif hasattr(intersects, "__geo_interface__"):
                g = intersects

            else:
                raise ValueError("intersection geometry must be either geojson or object with __geo_interface__")

            # If STAC, use the geojson
            if api == "stac":
                params["intersects"] = g.__geo_interface__
            # Bounding box is all that's supported for OAFeat
            else:
                try:
                    # Shapely
                    params["bbox"] = g.bounds
                except AttributeError:
                    # ArcGIS
                    params["bbox"] = g.extent
        return params

    def _query_parse_stac_query(self, params: dict, api: str, kwargs: dict) -> dict:
        """
        For a STAC/OGC Features query, parse the bbox/geometry depending on the API type

        Arguments:
        """
        # Individual item ids to get
        ids = kwargs.get("ids", None)
        if ids is not None:
            params["ids"] = ids

        # Parse the original STAC Query object, this will go away soon now that
        # The core STAC spec adopted CQL.
        query = kwargs.get("query", None)
        if query is not None:
            for k, v in query.items():
                gt = v.get("gt")
                if gt is not None and isinstance(gt, pydatetime.datetime):
                    v["gt"] = gt.isoformat()
                lt = v.get("lt")
                if lt is not None and isinstance(lt, pydatetime.datetime):
                    v["lt"] = lt.isoformat()
                gte = v.get("gte")
                if gte is not None and isinstance(gte, pydatetime.datetime):
                    v["gte"] = gte.isoformat()
                lte = v.get("lte")
                if lte is not None and isinstance(lte, pydatetime.datetime):
                    v["lte"] = lte.isoformat()
                eq = v.get("eq")
                if eq is not None and isinstance(eq, pydatetime.datetime):
                    v["eq"] = eq.isoformat()
                neq = v.get("neq")
                if neq is not None and isinstance(neq, pydatetime.datetime):
                    v["neq"] = neq.isoformat()
                query[k] = v

            params["query"] = query

        # Sortby object, see STAC sort spec
        sortby = kwargs.pop("sortby", None)
        if sortby is not None:
            params["sortby"] = sortby

        # Fields to include/exclude.
        fields = kwargs.pop("fields", None)
        if fields is not None:
            fieldsObj = defaultdict(list)
            # fields with +/-
            if isinstance(fields, list):
                for field in fields:
                    if field.startswith("+"):
                        fieldsObj["include"].append(field[1:])
                    elif field.startswith("-"):
                        fieldsObj["exclude"].append(field[1:])
                    else:
                        fieldsObj["include"].append(field)
            else:
                fieldsObj = fields
            params["fields"] = fieldsObj
        return params

    def warp(self, *,
             bbox: list,
             pixel_size: Optional[list] = None,
             shape: Optional[list] = None,
             pixel_dtype: Union[np.dtype, str] = np.float32,
             bbox_srs: str = "EPSG:4326",
             output_srs: str = "EPSG:3857",
             resampling: str = 'nearest',
             input_nodata: Any = None,
             output_nodata: Any = None,
             content_type: str = 'raw',
             asset_names: list = [],
             band_ids: list = [],
             query: dict = {}
             ):

        if pixel_size is None and shape is None:
            raise ValueError('must specify at least pixel_size or shape')
        elif pixel_size is not None and shape is not None:
            raise ValueError('must specify pixel_size or shape, but not both')

        if content_type not in ('raw', 'jpeg', 'jpg', 'gif', 'tiff', 'png'):
            raise ValueError('content_type must be one of raw, jpeg, jpg, gif, tiff, png')

        if pixel_dtype in ['byte', 'uint8']:
            ptype = pixel_dtype
        else:
            ptype = np.dtype(pixel_dtype).name

        req = {
            'output_extent': bbox,
            'output_extent_spatial_reference': bbox_srs,
            'output_spatial_reference': output_srs,
            'pixel_type': ptype,
            'resampling_method': resampling,
            'content_type': content_type
        }

        if asset_names:
            req['asset_names'] = asset_names

        if band_ids:
            req['band_ids'] = band_ids

        if query:
            req['query'] = query

        if pixel_size is not None:
            if isinstance(pixel_size, (list, tuple)):
                req['output_pixel_size'] = pixel_size
            elif isinstance(pixel_size, (int, float)):
                req['output_pixel_size'] = (pixel_size, pixel_size)

        if shape is not None:
            req['output_shape'] = shape

        if input_nodata is not None:
            req['input_no_data'] = input_nodata
        if output_nodata is not None:
            req['output_no_data'] = output_nodata,

        res = boson_client.post(f'raster/{self.name}.{self.project}/warp', **req)
        raw_bytes = res.content

        if content_type == 'raw':
            h = res.headers
            bands = int(h['X-Image-Bands'])
            rows = int(h['X-Image-Rows'])
            cols = int(h['X-Image-Columns'])

            x = np.frombuffer(raw_bytes, dtype=pixel_dtype)
            return x.reshape((bands, rows, cols))
        elif content_type == 'tiff':
            import tifffile
            from io import BytesIO
            data = BytesIO(raw_bytes)
            x = tifffile.imread(data)
            return x

    @staticmethod
    def from_arcgis_item(
                         name: str,
                         item_id: str,
                         arcgis_instance: str = "https://www.arcgis.com/",
                         credentials=None
                         ) -> 'Dataset':

        if arcgis_instance.endswith('/'):
            arcgis_instance = arcgis_instance[:-1]
        url = f'{arcgis_instance}/sharing/rest/content/items/{item_id}?f=pjson'
        res = get_client().get(url)

        try:
            js = res.json()
        except Exception:
            raise ValueError("unable to get item info. (did you enter the correct arcgis_instance?)")

        # Get the server metadata for additional info that can be used to construct a initial dataset
        server_metadata = get_client().get(js['url'], params={"f": "pjson"})
        try:
            server_metadata = server_metadata.json()
        except Exception:
            server_metadata = {}

        stac_cfg = {}
        if js['type'] == 'Image Service':
            type_ = 'stac'
            subtype = 'raster'

            item_assets = {}
            for band_name in server_metadata.get('bandNames', []):
                item_assets[band_name] = {
                    "title": band_name,
                    "type": "application/octet-stream",
                    "description": band_name,
                    "roles": ["dataset"]
                }
            stac_cfg['itemAssets'] = item_assets

        elif js['type'] == 'Feature Service':
            type_ = 'features'
            subtype = 'other'
        elif js['type'] == 'Map Service':
            type_ = 'features'
            subtype = 'other'
        else:
            raise ValueError(f"unsupported ArcGIS Service Type '{js['type']}'")

        if 'termsofuse' in js['licenseInfo']:
            license = "https://goto.arcgis.com/termsofuse/viewtermsofuse"
        else:
            license = '(unknown)'

        spatial_extent = [-180, -90, 180, 90]
        if 'extent' in js:
            (x0, y0), (x1, y1) = js['extent']

            spatial_extent = [x0, y0, x1, y1]

        extent = {
            'spatial': spatial_extent
        }

        providers = []
        if 'owner' in js:
            providers.append({
                "name": js['owner'],
                "roles": ["processor"],
                "url": arcgis_instance
            })
        stac_cfg['providers'] = providers

        c = server_metadata['capabilities']
        supportsQuery = False
        supportsImage = False
        if 'Catalog' in c or 'Query' in c:
            supportsQuery = True
        if 'Image' in c:
            supportsImage = True

        boson_cfg = Boson(
            providerName="geoservices",
            url=url,
            threadSafe=True,
            passHeaders=['X-Esri-Authorization'],
            properties={
                "supportsQuery": supportsQuery,
                "supportsImage": supportsImage,
            }
        )

        dataset = boson_dataset(
            name=name,
            alias=js['title'],
            description=js['snippet'],
            keywords=js['tags'],
            license=license,
            type=type_,
            subtype=subtype,
            extent=extent,
            boson_cfg=boson_cfg,
            stac_cfg=stac_cfg,
        )

        return dataset

    @staticmethod
    def from_arcgis_service(name: str, url: str, credentials=None) -> 'Dataset':
        if url.endswith('/'):
            url = url[:-1]
        if not url.endswith("Server"):
            raise ValueError("url must end with ImageServer, FeatureServer, or MapServer")
        res = get_client().get(url, params=dict(f="pjson"))

        # Get the server metadata for additional info that can be used to construct a initial dataset
        try:
            server_metadata = res.json()
        except Exception:
            raise ValueError("unable to get service metadata. (did you enter the correct url?)")

        # Get the name, if the name doesn't exist, get the serviceItemId and build using from_arcgis_item
        dataset_alias = server_metadata.get('name')
        if dataset_alias is None:
            item_id = server_metadata.get('serviceItemId')
            # No way to find out the alias/human readable name, so set to the provided dataset name
            if item_id is None:
                dataset_alias = name
            else:
                return Dataset.from_arcgis_item(name=name, item_id=item_id)

        stac_cfg = {}
        if 'ImageServer' in url:
            type_ = 'stac'
            subtype = 'raster'

            item_assets = {}
            for band_name in server_metadata.get('bandNames', []):
                item_assets[band_name] = {
                    "title": band_name,
                    "type": "application/octet-stream",
                    "description": band_name,
                    "roles": ["dataset"]
                }
            stac_cfg['itemAssets'] = item_assets
        elif 'FeatureServer' in url:
            type_ = 'features'
            subtype = 'other'
        elif 'MapServer' in url:
            type_ = 'features'
            subtype = 'other'
        else:
            raise ValueError("unsupported service type")

        license = '(unknown)'

        spatial_extent = [-180, -90, 180, 90]
        if 'extent' in server_metadata:
            e = server_metadata['extent']
            x0 = e['xmin']
            y0 = e['ymin']
            x1 = e['xmax']
            y1 = e['ymax']

            sr = e.get('spatialReference', {})
            wkid = sr.get('latestWkid', sr.get('wkid', 4326))

            if wkid != 4326:
                p0 = pyproj.Proj(f'epsg:{wkid}', preserve_units=True)
                p1 = pyproj.Proj('epsg:4326', preserve_units=True)
                t = pyproj.Transformer.from_proj(p0, p1, always_xy=True)
                lo0, la0 = t.transform(x0, y0)
                lo1, la1 = t.transform(x1, y1)

            else:
                lo0, la0, lo1, la1 = x0, y0, x1, y1

            spatial_extent = [lo0, la0, lo1, la1]

        extent = {
            'spatial': spatial_extent
        }

        c = server_metadata['capabilities']
        supportsQuery = False
        supportsImage = False
        if 'Catalog' in c or 'Query' in c:
            supportsQuery = True
        if 'Image' in c:
            supportsImage = True

        boson_cfg = Boson(
            providerName="geoservices",
            url=url,
            threadSafe=True,
            passHeaders=['X-Esri-Authorization'],
            properties={
                "supportsQuery": supportsQuery,
                "supportsImage": supportsImage,
            }
        )

        dataset = boson_dataset(
            name=name,
            alias=server_metadata['name'],
            description=server_metadata['description'],
            keywords=[],
            license=license,
            type=type_,
            subtype=subtype,
            extent=extent,
            boson_cfg=boson_cfg,
            stac_cfg=stac_cfg
        )

        return dataset

    @staticmethod
    def from_stac_collection(name: str, url: str, credentials=None, subtype: str = 'raster') -> 'Dataset':
        if url.endswith('/'):
            url = url[:-1]

        if 'collections' not in url:
            raise ValueError("url must be of the form {STAC_ROOT}/collections/:collectionId")

        rs = stac_root_re.match(url)

        try:
            root = rs.group(1)
        except Exception:
            raise ValueError("invalid URL")

        res = get_client().get(url)

        try:
            stac_collection = res.json()
        except Exception:
            raise ValueError("unable to get service metadata. (did you enter the correct url?)")
        print('res', res)
        stac_extent = stac_collection.get('extent', {})
        spatial_extent = stac_extent.get('spatial', {})
        bbox = spatial_extent.get('bbox', [[-180.0, -90.0, 180.0, 90.0]])[0]
        temporal_extent = stac_extent.get('temporal', {})
        interval = temporal_extent.get('interval', [
            [
                pydatetime.datetime.fromtimestamp(0).strftime("%Y-%m-%dT%H:%M:%SZ"),
                pydatetime.datetime(2040, 1, 1).strftime("%Y-%m-%dT%H:%M:%SZ")
            ]
        ])

        extent = {
            'spatial': bbox,
            'temporal': interval[0],
        }

        if interval[0][1] is None:
            interval[0][1] = pydatetime.datetime(2040, 1, 1).strftime("%Y-%m-%dT%H:%M:%SZ")

        item_assets = stac_collection.get('item_assets', {})
        if not item_assets:
            item_assets = stac_collection.get('itemAssets', {})

        stac_cfg = {}
        if item_assets:
            stac_cfg['itemAssets'] = {}
        for key, asset in item_assets.items():
            stac_cfg['itemAssets'][key] = asset

        links = stac_collection.get('links', [])
        stac_cfg['links'] = links

        extensions = stac_collection.get('stac_extensions', [])
        stac_cfg['extensions'] = extensions

        providers = stac_collection.get('providers', [])
        stac_cfg['providers'] = providers

        keywords = stac_collection.get('keywords', [])
        keywords += ['boson']

        boson_cfg = Boson(
            providerName="stac",
            url=root,
            threadSafe=True,
            passHeaders=[],
            properties={
                "collection": stac_collection['id']
            }
        )

        type_ = 'stac'

        dataset = boson_dataset(
            name=name,
            alias=stac_collection.get('title', name),
            description=stac_collection.get('description', ''),
            keywords=keywords,
            license=stac_collection.get('license', ''),
            type=type_,
            subtype=subtype,
            extent=extent,
            boson_cfg=boson_cfg,
            stac_cfg=stac_cfg
        )

        return dataset


def boson_dataset(*,
                  name: str,
                  alias: str,
                  description: str,
                  keywords: List[str],
                  license: str,
                  type: str,
                  subtype: str,
                  extent: dict,
                  boson_cfg: 'Boson',
                  stac_cfg: dict) -> Dataset:

    dataset = Dataset(
        name=name,
        alias=alias,
        description=description,
        keywords=keywords,
        license=license,
        type=type,
        subtype=subtype,
        extent=extent,
        boson=boson_cfg,
        stac=stac_cfg,
        category="dataset",
        version="0.0.1",
        created=pydatetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        updated=pydatetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        service="boson",
        clients=["stac", "oafeat"],
        schemes=["http"],
        entanglement={
            "class": "dataset",
            "domain": "*",
            "category": "*",
            "type": "*"
        },
        project=get_active_project().name
    )

    return dataset


def parsedate(dt):
    try:
        return parse(dt)
    except TypeError:
        return dt


class Boson(APIObject):
    @property
    def name(self):
        return self['providerName']

    @name.setter
    def name(self, v: str):
        if not isinstance(v, str):
            raise ValueError("name must be a string")
        self._set_item('providerName', v)

    @property
    def url(self):
        return self['url']

    @url.setter
    def url(self, v: str):
        if not isinstance(v, str):
            raise ValueError("url must be a string")
        self._set_item('url', v)

    @property
    def thread_safe(self):
        return self['threadSafe']

    @thread_safe.setter
    def thread_safe(self, v: bool):
        if not isinstance(v, bool):
            raise ValueError("thread_safe must be a bool")
        self._set_item('threadSafe', v)

    @property
    def pass_headers(self):
        return self['passHeaders']

    @pass_headers.setter
    def pass_headers(self, v: List[str]):
        if not isinstance(v, list):
            raise ValueError("pass_headers must be a list of strings")

        self._set_item('passHeaders', v)

    @property
    def max_page_size(self):
        return self['maxPageSize']

    @max_page_size.setter
    def max_page_size(self, v: int):
        if not isinstance(v, int):
            raise ValueError("max_page_size must be an int")

    @property
    def properties(self):
        props = self.get("properties", {})
        self.properties = props
        return props

    @properties.setter
    def properties(self, v: dict):
        if not isinstance(v, dict):
            raise ValueError("properties must be a dict")
        self._set_item("properties", v)


class DatasetList(APIObject):
    def __init__(self, datasets, ids=[]):

        self.ids = ids
        if len(ids) != len(datasets):
            self.ids = [dataset.name for dataset in datasets]
        for dataset in datasets:
            self._set_item(dataset.name, dataset)

    def __getitem__(self, k) -> Dataset:
        if isinstance(k, str):
            return super().__getitem__(k)
        elif isinstance(k, int):
            did = self.ids[k]
            return super().__getitem__(did)
        else:
            raise KeyError("invalid key")

    def _repr_html_(self):
        if not jinja_available():
            return self.__repr__()
        template = get_template_env().get_template("dataset_template.html.jinja")
        return template.render(datasets=self)


class ItemAssets(dict):
    def __init__(self, item_assets=None, ds_name=None):
        self.update(item_assets)
        self._ds_name = ds_name

    def _repr_html_(self, add_style=True):
        if not jinja_available():
            return self.__repr__()
        template = get_template_env().get_template("item_assets_template.html.jinja")
        return template.render(assets=self)
