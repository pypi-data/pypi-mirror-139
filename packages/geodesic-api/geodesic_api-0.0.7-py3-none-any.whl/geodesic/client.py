import os
import warnings

import requests
from wrapt import ObjectProxy

from geodesic.oauth import AuthManager

os.environ["AWS_NO_SIGN_REQUEST"] = "YES"

HOST = os.getenv("HOST", "https://geodesic.seerai.space/")
SPACETIME_HOST = os.getenv("SPACETIME_HOST", "https://geodesic.seerai.space/spacetime")
ENTANGLEMENT_HOST = os.getenv(
    "ENTANGLEMENT_HOST", "https://geodesic.seerai.space/entanglement"
)
TESSERACT_HOST = os.getenv("TESSERACT_HOST", "https://geodesic.seerai.space/tesseract")
BOSON_HOST = os.getenv("BOSON_HOST", "https://geodesic.seerai.space/boson")
KRAMPUS_HOST = os.getenv("KRAMPUS_HOST", "https://geodesic.seerai.space/krampus")
DEBUG = os.getenv("DEBUG", "false")

if DEBUG.lower() in ("1", "true", "yes", "external"):
    DEBUG = True
else:
    DEBUG = False

EXT = os.getenv("GEODESIC_EXTERNAL", "1")
if EXT.lower() in ("1", "true", "yes", "external"):
    EXTERNAL = True
else:
    EXTERNAL = False

    # For the REST API, as used by this client. :)
    if not SPACETIME_HOST.endswith(":8080"):
        SPACETIME_HOST += ":8080"
    if not ENTANGLEMENT_HOST.endswith(":8080"):
        ENTANGLEMENT_HOST += ":8080"
    if not TESSERACT_HOST.endswith(":8080"):
        TESSERACT_HOST += ":8080"
    if not BOSON_HOST.endswith(":8080"):
        BOSON_HOST += ":8080"

    EXTERNAL_HOSTS = {
        "https://geodesic.seerai.space/spacetime": SPACETIME_HOST,
        "https://geodesic.seerai.space/entanglement": ENTANGLEMENT_HOST,
        "https://geodesic.seerai.space/tesseract": TESSERACT_HOST,
        "https://geodesic.seerai.space/boson": BOSON_HOST,
    }

API_VERSION = 1

client = None


def get_client():
    global client
    if client is not None:
        return client

    client = Client()
    return client


def raise_on_error(res: requests.Response) -> requests.Response:
    """
    Checks a Response for errors. Returns the original Response if none are found.
    """
    try:
        res_json = res.json()
        if 'error' in res_json:
            raise requests.exceptions.HTTPError(res_json)
        return res
    except Exception as e:
        raise requests.exceptions.HTTPError(e, res.text[:200])


class ResponseWrapper(ObjectProxy):
    """
    This is a proxy class that allows for depreciated usage of client.request and its derivatives.
    """

    # Create a fake type that fools isinstance into returning True for both Response and dict.
    #   This likely has all kinds of subtle undesirable effects, but this class is intended to be
    #   removed anyway, so it works. There isn't really a way to warn only on isinstance(x, dict)
    #   with this method, so this defers that warning until the object is actually used.
    class __NotActuallyADict(requests.Response, dict):
        pass

    __class__ = __NotActuallyADict

    def _warn(self):
        warnings.warn(
            'Client.request and its derivative methods now return requests.Response objects '
            'instead of pre-parsed dicts. This proxy class mirrors most of the behavior of '
            'the depreciated return type for temporary backwards compatibility. This behavior '
            'will be phased out in geodesic-python-api vX.X.X (TBD).', DeprecationWarning)

    # NOTE: with some clever coding, the definitions of the magic methods below could definitely be
    #   DRY'ed. If we end up reusing this approach for depreciation, we can do that. But *hopefully*
    #   that won't be necessary.
    def __init__(self, wrapped):
        super(ResponseWrapper, self).__init__(wrapped)
        # Saving what would have been the return value so it can be mutated if needed.
        # Depreciated client.request method raised an exception if .json() returned
        #   anything other than a dict, so we only need to cover that case.
        self.__self_deprec = None

    @property
    def _self_deprec(self):
        # Deferring evaluation means that JSONDecodeError will raise only if this is called
        self._warn()
        if self.__self_deprec is None:
            self.__self_deprec = self.__wrapped__.json()
        return self.__self_deprec

    def __getattr__(self, item):
        """
        If an attribute is not found on the wrapped Response, use self._self_deprec instead

        This covers all dict functionality other than the magic methods defined individually below.
        Implicit in this is that name collisions go to the Response every time. If it's desirable
        to also warn on name collisions, this should be moved to __getattribute__() instead.
        """
        if hasattr(dict, item):
            return self._self_deprec.__getattribute__(item)
        else:
            return self.__wrapped__.__getattribute__(item)

    def __reversed__(self, *args, **kwargs):
        return self._self_deprec.__reversed__(*args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        return self._self_deprec.__setitem__(*args, **kwargs)

    def __getitem__(self, *args, **kwargs):
        return self._self_deprec.__getitem__(*args, **kwargs)

    def __contains__(self, *args, **kwargs):
        return self._self_deprec.__contains__(*args, **kwargs)

    def __delitem__(self, *args, **kwargs):
        return self._self_deprec.__delitem__(*args, **kwargs)

    def __len__(self, *args, **kwargs):
        return self._self_deprec.__len__(*args, **kwargs)


class Client:
    def __init__(self):
        self._auth = AuthManager()
        self._session = None
        self._host = HOST
        self._api_version = API_VERSION

    def request(self, uri, method="GET", **params):

        url = HOST
        if url.endswith("/"):
            url = url[:-1]

        # Route request to correct endpoint
        if uri.startswith("/spacetime"):
            uri = uri.replace("/spacetime", "", 1)
            url = SPACETIME_HOST + uri
        elif uri.startswith("/entanglement"):
            uri = uri.replace("/entanglement", "", 1)
            url = ENTANGLEMENT_HOST + uri
        elif uri.startswith("/tesseract"):
            uri = uri.replace("/tesseract", "", 1)
            url = TESSERACT_HOST + uri
        elif uri.startswith("/krampus"):
            uri = uri.replace("/krampus", "", 1)
            url = KRAMPUS_HOST + uri
        elif uri.startswith("/"):
            url = url + uri

        if uri.startswith("http"):
            url = uri

        if not EXTERNAL:
            for find, replace in EXTERNAL_HOSTS.items():
                url = url.replace(find, replace)

        if method == "GET":
            req = requests.Request("GET", url, params=params)
        elif method == "POST":
            req = requests.Request("POST", url, json=params)
        elif method == "PUT":
            req = requests.Request("PUT", url, json=params)
        elif method == "DELETE":
            body = params.get("__delete_body", None)
            if body is not None:
                req = requests.Request("DELETE", url, json=body)
            else:
                req = requests.Request("DELETE", url, params=params)
        else:
            raise Exception(f"unknown method: {method}")
        if EXTERNAL:
            req.headers["Authorization"] = "Bearer {0}".format(self._auth.id_token)
            req.headers["X-Auth-Request-Access-Token"] = "Bearer {0}".format(self._auth.access_token)

        if self._session is None:
            self._session = requests.Session()

        prepped = req.prepare()
        res = self._session.send(prepped)

        return ResponseWrapper(res)

    def get(self, uri, **query):
        return self.request(uri, method="GET", **query)

    def post(self, uri, **body):
        return self.request(uri, method="POST", **body)

    def put(self, uri, **body):
        return self.request(uri, method="PUT", **body)

    def delete(self, uri, **query):
        return self.request(uri, method="DELETE", **query)

    def delete_with_body(self, uri, **body):
        return self.request(uri, method="DELETE", __delete_body=body)
