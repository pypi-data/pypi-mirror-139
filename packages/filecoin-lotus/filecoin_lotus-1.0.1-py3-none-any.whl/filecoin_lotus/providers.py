from typing import Any, Union
import os
import requests
import itertools
from filecoin_lotus.encoding import FriendlyCode
from filecoin_lotus.types_fil import RPCEndpoint


class JSONBaseProvider:
    def __init__(self) -> None:
        self.request_counter = itertools.count()

    def decode_rpc_response(self, raw_response):
        resp = FriendlyCode().json_decode(raw_response.text)
        res = resp.get("result")
        if res:
            return res
        else:
            error = resp.get("error")
            raise Exception(error)

    def encode_rpc_request(self, method: RPCEndpoint, params: Any):
        rpc_dict = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or [],
            "id": next(self.request_counter),
        }
        return rpc_dict


class HttpProvider(JSONBaseProvider):
    """
        An HTTP Provider for API request
        :param endpoint_uri: HTTP API URL base. Default value is ``"http://127.0.0.1:1234/rpc/v0"``. Can also be configured via the ``FILECOIN_LOTUS_HTTP_PROVIDER_URI`` environment variable.
        :param auth: Authorization string, default in ~/.lotus/token
        :return:
    """

    def __init__(self, endpoint_uri: Union[str, dict] = None, auth: str = None, timeout: float = 10):
        super(HttpProvider, self).__init__()
        if endpoint_uri is None:
            self.endpoint_uri = os.environ.get("FILECOIN_LOTUS_HTTP_PROVIDER_URI", "http://127.0.0.1:1234/rpc/v0")
        elif isinstance(endpoint_uri, (str,)):
            self.endpoint_uri = endpoint_uri
        else:
            raise TypeError("unknown endpoint uri {}".format(endpoint_uri))

        if auth is None:
            auth = os.popen("cat ~/.lotus/token").read().strip()

        self.sess = requests.session()
        self.sess.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + auth
        }

        self.timeout = timeout
        """Request timeout in second."""

    def make_request(self, method: RPCEndpoint, params: Any = None) -> Any:
        json_dict = self.encode_rpc_request(method, params)
        resp = self.sess.post(self.endpoint_uri, json=json_dict, timeout=self.timeout)
        res = self.decode_rpc_response(resp)
        return res
