from filecoin_lotus.encoding import FriendlyCode
from filecoin_lotus.providers import HttpProvider
from filecoin_lotus.wallet import Wallet
from filecoin_lotus.chain import Chain
from filecoin_lotus.mpool import MPool
from filecoin_lotus.state import State

class FileCoin:
    COIN_DECIMAL = 18
    HttpProvider = HttpProvider

    def __init__(self, provider: HttpProvider):
        self.provider = provider
        self._wallet = Wallet(self)
        self._chain = Chain(self)
        self._mpool = MPool(self)
        self._state = State(self)

    @property
    def wallet(self):
        return self._wallet

    @property
    def chain(self):
        return self._chain

    @property
    def mpool(self):
        return self._mpool

    @property
    def state(self):
        return self._state

    def toAtto(self, value):
        """
        Fil to attoFil
        :param value:
        :return:
        """
        return FriendlyCode().value_encode(value, FileCoin.COIN_DECIMAL)

    def fromAtto(self, value):
        """
        AttoFil to Fil
        :param value:
        :return:
        """
        return FriendlyCode().value_decode(value, FileCoin.COIN_DECIMAL)
