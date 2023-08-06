from filecoin_lotus.rpc_abi import RPC
import os


class State:

    def __init__(self, filecoin):
        self._filecoin = filecoin
        self._provider = filecoin.provider

    def state_search_message(self, message: str) -> bool:
        """
        Check message receipt
        :param message:
        :return:
        """
        res = self._provider.make_request(RPC.state_searchMessage, [{"/": message}])
        receipt_info = res.get("Receipt", None)
        status = receipt_info.get("ExitCode", None)
        return status == 0
