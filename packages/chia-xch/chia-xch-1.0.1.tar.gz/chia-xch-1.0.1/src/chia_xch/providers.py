from typing import Any, Union
import os
import requests
import itertools
from chia_xch.encoding import FriendlyCode
from chia_xch.types_xch import RPCEndpoint
import requests.packages.urllib3

class JSONBaseProvider:
    def __init__(self) -> None:
        self.request_counter = itertools.count()

    def decode_rpc_response(self, raw_response):
        resp = FriendlyCode().json_decode(raw_response.text)
        status = resp.get("success")
        if not status:
            error = resp.get("error")
            raise Exception(error)
        return resp


    def encode_rpc_request(self, params: Any):
        rpc_dict = {
            "jsonrpc": "2.0",
            "params": params or [],
            "id": next(self.request_counter),
        }
        return rpc_dict


class HttpProvider(JSONBaseProvider):
    """
        An HTTP Provider for API request
        :param endpoint_uri: HTTP API URL base. Default value is ``"http://127.0.0.1:8555"``.
        :param auth: Authorization string, default in ~/.lotus/token
        :return:
    """

    def __init__(self, endpoint_uri: Union[str, dict] = None, cert: str = None, key: str = None, timeout: float = 10):
        super(HttpProvider, self).__init__()
        if endpoint_uri is None:
            self.endpoint_uri = os.environ.get("CHIA_HTTP_PROVIDER_URI", "http://127.0.0.1:8555")
        elif isinstance(endpoint_uri, (str,)):
            self.endpoint_uri = endpoint_uri
        else:
            raise TypeError("unknown endpoint uri {}".format(endpoint_uri))

        requests.packages.urllib3.disable_warnings()
        self.sess = requests.session()
        self.sess.headers = {
            "Content-Type": "application/json"
        }

        self.cert = (cert, key)
        self.timeout = timeout
        """Request timeout in second."""

    def make_request(self, method: RPCEndpoint, params: Any = None) -> Any:
        # json_dict = self.encode_rpc_request(params)
        resp = self.sess.post(self.endpoint_uri + method, json=params, timeout=self.timeout, cert=self.cert,
                              verify=False)
        res = self.decode_rpc_response(resp)
        return res


class FullNodeProvider(HttpProvider):
    def __init__(self, endpoint_uri: Union[str, dict] = None, cert: str = None, key: str = None, timeout: float = 10):
        if endpoint_uri is None:
            endpoint_uri = "https://localhost:8555/"
        if cert is None:
            cert = "/root/.chia/mainnet/config/ssl/full_node/private_full_node.crt"
        if key is None:
            key = "/root/.chia/mainnet/config/ssl/full_node/private_full_node.key"
        super(FullNodeProvider, self).__init__(endpoint_uri, cert, key, timeout)


class WalletProvider(HttpProvider):
    def __init__(self, endpoint_uri: Union[str, dict] = None, cert: str = None, key: str = None, timeout: float = 10):
        if endpoint_uri is None:
            endpoint_uri = "https://localhost:9256/"
        if cert is None:
            cert = "/root/.chia/mainnet/config/ssl/wallet/private_wallet.crt"
        if key is None:
            key = "/root/.chia/mainnet/config/ssl/wallet/private_wallet.key"
        super(WalletProvider, self).__init__(endpoint_uri, cert, key, timeout)
