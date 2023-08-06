try:
    import arcgis
except ImportError:
    arcgis = None
try:
    import pandas as pd
except ImportError:
    pd = None

try:
    import geopandas as gpd
except ImportError:
    gpd = None

try:
    from osgeo import gdal
except ImportError:
    gdal = None

import os
import hashlib
from urllib.parse import unquote
import json
import pytz
import uuid

from collections import defaultdict
# from datetime import datetime

from geodesic.client import get_client, raise_on_error
from geodesic.utils.downloader import download
from geodesic.utils.gdal_utils import lookup_dtype, get_spatial_reference
from geodesic.utils.exif import get_image_geometry
from geodesic.raster import Raster
from geodesic.widgets import get_template_env, jinja_available
from shapely.geometry import shape
# from shapely.geometry.base import BaseGeometry
from dateutil.parser import ParserError, parse
from datetime import datetime as pydt
from typing import Tuple, List, Optional, Union


class Feature(dict):
    """Feature representation.

    Args:
        obj: Dictionary representation of a feature

    """

    def __init__(self, obj=None):
        if isinstance(obj, dict):
            self.update(obj)

        self._geometry = None

    @property
    def geometry(self):
        if self._geometry is not None:
            return self._geometry

        try:
            self._geometry = shape(self["geometry"])
        except KeyError:
            return None
        return self._geometry

    @geometry.setter
    def geometry(self, g):
        if isinstance(g, dict):
            # make sure g is a geometry
            try:
                _ = shape(g)
            except Exception as e:
                raise ValueError("this does not appear to be a valid geometry") from e
            self["geometry"] = g
            return
        try:
            self["geometry"] = g.__geo_interface__
            try:
                self["bbox"] = g.bounds
            except AttributeError:
                try:
                    self["bbox"] = g.extent
                except Exception:
                    pass
            return
        except AttributeError:
            raise ValueError("unknown geometry object")

    def set_property(self, k, v):
        self.properties[k] = v

    @property
    def properties(self):
        props = self.get("properties", {})
        self.properties = props
        return props

    @property
    def __geo_interface__(self):
        return dict(self)

    @properties.setter
    def properties(self, v):
        self["properties"] = v

    @property
    def links(self):
        links = self.get("links", [])
        self.links = links
        return links

    @links.setter
    def links(self, v):
        self["links"] = v

    def _repr_svg_(self):
        try:
            return self.geometry._repr_svg_()
        except Exception:
            return None


class FeatureCollection(dict):
    def __init__(self, obj=None, dataset=None, query=None):
        # From GeoJSON
        if isinstance(obj, dict):
            self.update(obj)
        self._gdf = None
        self._sedf = None
        self._ogr = None

        self._is_stac = False
        self.dataset = dataset
        self.query = query
        if self.dataset is not None:
            self._ds_type = self.dataset.dataset_type
            self._ds_subtype = self.dataset.dataset_subtype

        self._provenance = None

    def _repr_html_(self):
        if not jinja_available():
            return self.__repr__()

        template = get_template_env().get_template("feature_collection_template.html.jinja")
        vals = defaultdict(None)
        vals['n_feats'] = len(self['features'])
        return template.render(fc=self, vals=vals)

    @property
    def features(self):
        is_stac = False

        if len(self['features']) > 0:
            f = self['features'][0]
            if 'assets' in f:
                is_stac = True
        if is_stac:
            return [Item(f, dataset=self.dataset) for f in self["features"]]
        else:
            return [Feature(f) for f in self["features"]]

    @property
    def gdf(self):
        if gpd is None:
            raise ValueError("this method requires geopandas (not installed)")
        if self._gdf is not None:
            return self._gdf
        df = pd.DataFrame(self["features"])
        geo = [shape(g) for g in df.geometry]
        self._gdf = gpd.GeoDataFrame(df, geometry=geo, crs="EPSG:4326")
        return self._gdf

    @property
    def sedf(self):
        if pd is None:
            raise ValueError("this method requires pandas (not installed)")
        if self._sedf is not None:
            return self._sedf
        df = pd.DataFrame(self["features"])
        geo = [arcgis.geometry.Geometry.from_shapely(shape(g)) for g in df.geometry]
        df.spatial.set_geometry(geo)
        self._sedf = df
        return self._sedf

    @property
    def ogr(self):
        if gdal is None:
            raise ValueError("this method requires gdal/ogr (not installed")
        if self._ogr is not None:
            return self._ogr

        feats = json.dumps(self)
        ds = gdal.OpenEx(feats, allowed_drivers=['GeoJSON'])
        self._ogr = ds
        return ds

    @property
    def __geo_interface__(self):
        return dict(self)

    @property
    def _next_link(self):
        links = self.get("links", [])
        if links is not None:
            for link in links:
                if link.get("rel", None) == "next":
                    return unquote(link.get("href"))

    def get_all(self):
        features = self.get("features", [])
        self["features"] = features
        client = get_client()
        next_uri = self._next_link
        while next_uri is not None:

            res = raise_on_error(client.get(next_uri)).json()
            if len(res["features"]) == 0:
                return

            features.extend(res["features"])
            next_uri = self._next_link

    @property
    def query_hash(self):
        if self.query is None:
            return ""
        st = json.dumps(self.query)
        return hashlib.sha256(st.encode()).hexdigest()

    @property
    def provenance(self):
        """
        Returns the data provenance, if available, for this object.

        Returns:
            provenance - a dictionary representing a json provenance object

        Example:
            >>> provenance = feature_collection.get_provenance()
            >>> provenance
            {
                "query_hash": "234809s7dfsouj9s8j3f9s3j8o4ij2o3ij4",
                "query": {
                    ...
                },
                "provenance":{
                    "landsat-8-l1": [
                        {
                            "pfs:commit": "79swa87f9s8d7f987234jlsdfkljsld"
                            "pfs:path": "LC80120322021032LGN00.json"
                        }, {
                            ...
                        }
                    ],
                    "srtm-gl1": [
                        {
                            ...
                        }
                    ]
                }
            }


        """
        if self._provenance is not None:
            return self._provenance

        prov = defaultdict(list)
        for feature in self.features:
            try:
                pfs = feature.pfs
            except AttributeError:
                continue

            repo = pfs.pop("pfs:repo")
            if repo is None:
                continue

            prov[repo].append(pfs)

        self._provenance = {
            "id": self.query_hash,
            "query": self.query,
            "provenance": prov,
        }
        return self._provenance

    def rasterize(
                self,
                reference_dataset=None,
                property_name=None,
                dtype=None,
                shape=None,
                geo_transform=None,
                spatial_reference=None,
                return_dataset=True):

        if reference_dataset is not None:
            driver = reference_dataset.GetDriver()
            gt = reference_dataset.GetGeoTransform()
            spatial_reference = reference_dataset.GetSpatialRef()
            xsize = reference_dataset.RasterXSize
            ysize = reference_dataset.RasterYSize
        else:
            driver = gdal.GetDriverByName("GTiff")
            gt = geo_transform
            ysize, xsize = shape
            spatial_reference = get_spatial_reference(spatial_reference)

        datatype = lookup_dtype(dtype)

        fname = f'/vsimem/{str(uuid.uuid4())}.tif'

        target_ds = driver.Create(fname, xsize, ysize, 1, datatype)
        target_ds.SetGeoTransform((gt[0], gt[1], 0, gt[3], 0, gt[5]))
        target_ds.SetSpatialRef(spatial_reference)

        options = gdal.RasterizeOptions(attribute=property_name)
        _ = gdal.Rasterize(target_ds, self.ogr, options=options)
        if return_dataset:
            return target_ds

        return target_ds.ReadAsArray()


def check_tz(d):
    if d.tzinfo is not None and d.tzinfo.utcoffset(d) is not None:
        return d
    return pytz.utc.localize(d)


class Item(Feature):
    """Class representing a STAC item.

    Implements additional STAC properties on top of a :class:`geodesic.stac.feature`

    Args:
        obj: A python object representing a STAC item.
        dataset: The dataset object this Item belongs to.

    """

    def __init__(self, obj=None, dataset=None):
        super().__init__(obj)
        if dataset is not None:
            self.item_type = dataset.dataset_subtype
            self.dataset = dataset

        assets = self.get("assets", {})
        assets = {k: Asset(v) for k, v in assets.items()}
        self._assets = assets
        self['assets'] = assets

    def _repr_html_(self):
        assets = self.get("assets", {})
        if "thumbnail" in assets:
            href = assets["thumbnail"]["href"]
            width = 500
            if href == "https://seerai.space/images/Logo.svg":
                width = 100

            return f'<img src="{href}" style="width: {width}px;"></img>'
        else:
            try:
                return self._repr_svg_()
            except Exception:
                href = "https://seerai.space/images/Logo.svg"
                width = 100
                return f'<img src="{href}" style="width: {width}px;"></img>'

    @property
    def datetime(self):
        dt = self.properties.get("datetime", None)
        if dt is None:
            return
        try:
            pdt = parse(dt)
            return check_tz(pdt)
        # datetime could be a list
        except TypeError:
            return [check_tz(d) for d in map(parse, dt)]

    @datetime.setter
    def datetime(self, v):
        if isinstance(v, (list, tuple)):
            try:
                self.set_property("datetime", [d.isoformat() for d in v])
            except AttributeError:
                self.set_property("datetime", v)
        else:
            try:
                self.set_property("datetime", v.isoformat())
            except AttributeError:
                self.set_property("datetime", v)

    @property
    def pfs(self):
        """Get information about this item from PFS

        If this item was produced by running in a Pachyderm pipeline, all of the relevant Pachyderm
        info will be stored in here. This allows the provenance of an item to be traced.
        """
        return {
            "pfs:repo": self.properties.get("pfs:repo", None),
            "pfs:commit": self.properties.get("pfs:commit", None),
            "pfs:path": self.properties.get("pfs:path", None),
        }

    def set_pfs(self, repo=None, commit=None, path=None):
        self.set_property("pfs:repo", repo)
        self.set_property("pfs:commit", commit)
        self.set_property("pfs:path", path)

    def set_asset(self, k, a):
        assets = self.assets
        assets[k] = dict(a)

    def get_asset(self, k):
        return self.assets[k]

    @property
    def raster(self):
        if self.item_type != "raster":
            raise ValueError(
                "item must be of raster type, is: '{0}'".format(self.item_type)
            )
        return Raster(self, dataset=self.dataset)

    @property
    def assets(self):
        return self._assets

    @assets.setter
    def assets(self, assets):
        self._assets = {k: Asset(v) for k, v in assets.items()}
        self["assets"] = self._assets

    @staticmethod
    def new(dataset=None):
        return Item(
            obj={
                "type": "Feature",
                "id": None,
                "geometry": None,
                "bbox": None,
                "collection": None,
                "stac_extensions": [],
                "properties": {},
                "assets": {},
                "links": [],
            },
            dataset=dataset,
        )

    @staticmethod
    def from_image(path: str):
        g = get_image_geometry(path)

        i = Item.new()
        i.geometry = g
        i.id = path
        img = Asset.new()
        img.href = path
        img.title = path
        img.description = "local image"
        thumb = Asset.new()
        thumb.href = path
        thumb.title = path
        thumb.description = "thumbnail"
        thumb.roles = ["thumbnail"]
        i.assets['image'] = img
        i.assets['thumbnail'] = thumb

        return i

    @property
    def id(self):
        i = self.get("id", None)
        return i

    @id.setter
    def id(self, id):
        if not isinstance(id, str):
            raise ValueError("id must be a string")
        self["id"] = id

    @property
    def collection(self):
        c = self.get("collection", None)
        return c

    @collection.setter
    def collection(self, c):
        if not isinstance(c, str):
            raise ValueError("collection must be a string")
        self["collection"] = c

    @property
    def stac_extensions(self):
        e = self.get("stac_extensions", [])
        return e

    @stac_extensions.setter
    def stac_extensions(self, e):
        self["stac_extensions"] = e


class Asset(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._local = None

    @property
    def href(self) -> str:
        return self["href"]

    @href.setter
    def href(self, v):
        self["href"] = v

    @property
    def title(self) -> str:
        return self["title"]

    @title.setter
    def title(self, v):
        self["title"] = v

    @property
    def description(self):
        return self["description"]

    @description.setter
    def description(self, v):
        self["description"] = v

    @property
    def type(self):
        return self["type"]

    @type.setter
    def type(self, v):
        self["type"] = v

    @property
    def roles(self) -> List[str]:
        roles = self.get("roles", [])
        self["roles"] = roles
        return roles

    @roles.setter
    def roles(self, v):
        self["roles"] = v

    def has_role(self, role: str):
        for r in self.roles:
            if role == r:
                return True
        return False

    @property
    def local(self) -> str:
        if self._local is not None:
            return self._local

        self._local = self.get('local', '')
        return self._local

    @local.setter
    def local(self, local):
        self._local = local
        self['local'] = local

    @local.deleter
    def local(self):
        path = self.pop('local')
        self._local = None
        if os.path.exists(path):
            os.remove(path)

    @staticmethod
    def new():
        return Asset(
            {
                "href": None,
                "title": None,
                "type": None,
                "description": None,
                "roles": [],
            }
        )

    def download(self, out_dir: str = None) -> str:
        """
        Download the asset to a local directory, returns the full path to the asset.
        """

        if self._local is not None:
            return self._local

        path = download(self.href, out_dir)
        self.local = path
        return path


def search(
    bbox: Optional[Union[List, Tuple]] = None,
    datetime: Union[List, Tuple, str, pydt] = None,
    intersects=None,
    collections: List[str] = None,
    ids: List[str] = None,
    limit: int = 10,
    method: str = 'POST'
) -> FeatureCollection:
    """Search through the SeerAI STAC catalogue.

    Use the search function on the STAC catalogue using the STAC API version of search.
    The STAC api is described [here](https://stacspec.org/STAC-api.html#operation/postSearchSTAC).

    Args:
        bbox: list or tuple of coordinates describing a bounding box. Should have length should be either 4 or 6.
        datetime: Either a datetime or interval expressed as a string. Open ended intervals can be expressed using
                  double-dots '..'. If given as a string datetimes must be in RFC3339 format. See examples below
                  for different formats.
        intersects: Only items that intersect this geometry will be included in the results. Can be either geojson or
                    object that has  `__geo_interface__`.
        collections: List of strings with collection IDs to include in search results.
        ids: List of item IDs to return. All other filter parameters that further restrict the search are ignored.
        limit: The maximum number of results to return.
        method: Request method to use. Valid options are 'POST' (default) and 'GET'. Normally you should not have to
                change this from the default.

    Examples:
        An example search.

        >>> from geodesic.stac import search
        >>> search(
        ...    bbox=[(-122.80058577975704, 40.72377233124292, -122.7906160884923, 40.726188159862616)],
        ...    datetime="2021-06-15T00:00:00",
        ...    collections: ['sentinel-2-l2a]
        ... )

        Datetimes can be passed as either python datetime objects or as strings. The following are valid arguments.

        >>> from datetime import datetime
        >>> dt = [datetime(2021, 1, 1), datetime(2021, 1, 2)]
        >>> dt = datetime(2021, 1, 1)
        >>> dt = ["2021-01-01T00:00:00", "2021-01-02T00:00:00"]
        >>> dt = "2021-01-01T00:00:00/2021-01-02T00:00:00"
        >>> dt = "2021-01-01T00:00:00"

        Datetimes may also be passed as open intervals using double-dot notation.

        >>> dt = "../2021-05-10T00:00:00"
        >>> dt = "2021-05-10T00:00:00/.."

    """
    query = {}

    method = method.upper()
    if method not in ['POST', 'GET']:
        raise ValueError("method can only be one of 'POST'(default) or 'GET'")

    if bbox is not None:
        if not (len(bbox) == 4 or len(bbox) == 6):
            raise ValueError("bbox must have either 4 or 6 coordinates")
        if method == "GET":
            bbox = [str(coord) for coord in bbox]
            bbox = ",".join(bbox)

        query['bbox'] = bbox

    if datetime is not None:
        if isinstance(datetime, (list, tuple)):
            dt = [parse_date(d) for d in datetime]
            pdt = "/".join(dt)
        elif isinstance(datetime, str):
            if "/" in datetime:
                start_end = datetime.split('/')
                if len(start_end) != 2:
                    raise ValueError("datetime range can only contain one '/'")
                dt = [parse_date(d) for d in start_end]
                pdt = "/".join(dt)
            else:
                pdt = parse_date(datetime)
        elif isinstance(datetime, pydt):
            pdt = parse_date(datetime)
        else:
            raise TypeError("unknown type for datetime")

        query['datetime'] = pdt

    if intersects is not None:
        if hasattr(intersects, "__geo_interface__"):
            g = intersects
        elif isinstance(intersects, dict):
            try:
                g = shape(intersects)
            except Exception:
                try:
                    g = shape(intersects['geometry'])
                except Exception as e:
                    raise ValueError("could not determine type of intersection geometry") from e

        else:
            raise ValueError("intersection geometry must be either geojson or object with __geo_interface__")

        query["intersects"] = g.__geo_interface__

    if collections is not None:
        if not isinstance(collections, list):
            raise TypeError("collections must be a list of strings")
        query['collections'] = collections

    if ids is not None:
        if not isinstance(ids, list):
            raise TypeError("ids must be a list of strings")
        query['ids'] = ids

    if limit is None:
        query['limit'] = 500
    else:
        query['limit'] = limit

    c = get_client()
    if method == 'POST':
        res = raise_on_error(c.post('/spacetime/api/v1/stac/search', **query)).json()
    elif method == 'GET':
        # raise NotImplementedError("GET not implemented yet")
        res = raise_on_error(c.get('/spacetime/api/v1/stac/search', **query)).json()
    fc = FeatureCollection(obj=res, dataset=None, query=query)
    if limit is None:
        fc.get_all()
    return fc


def parse_date(dt):
    if isinstance(dt, str):
        try:
            return parse(dt).isoformat()
        except ParserError as e:
            if dt == '..' or dt == '':
                return dt
            else:
                raise e
    elif isinstance(dt, pydt):
        return dt.isoformat()
    else:
        raise ValueError("could not parse datetime. unknown type.")
