from filecoin_lotus.rpc_abi import RPC
import json
import base64


class Wallet:

    def __init__(self, filecoin):
        self._filecoin = filecoin
        self._provider = filecoin.provider

    def wallet_new(self, wallet_type: str = 'secp256k1') -> str:
        """
        Create a wallet
        :param wallet_type: secp256k1 or bls
        :return: address
        """
        return self._provider.make_request(RPC.wallet_new, [wallet_type])

    def wallet_balance(self, wallet_address: str) -> float:
        """
        Get wallet balance
        :param wallet_address:
        :return:
        """
        balance = self._provider.make_request(RPC.wallet_balance, [wallet_address])
        return float(self._filecoin.fromAtto(balance))

    def wallet_export(self, address: str) -> str:
        """
        Import wallet to lotus
        :param address:
        :return:
        """
        res = self._provider.make_request(RPC.wallet_export, [address])
        j_res = json.dumps(res).replace(" ", "")
        return base64.b16encode(j_res.strip().encode()).decode().lower()

    def wallet_import(self, private_key: str) -> str:
        info = base64.b16decode(private_key.upper()).decode()
        res = self._provider.make_request(RPC.wallet_import, [json.loads(info)])
        return res

    def wallet_validate(self, address: str) -> bool:
        """
        Check address
        :param address:
        :return:
        """
        try:
            res = self._provider.make_request(RPC.wallet_validate, [address])
            return res is not None
        except:
            return False
