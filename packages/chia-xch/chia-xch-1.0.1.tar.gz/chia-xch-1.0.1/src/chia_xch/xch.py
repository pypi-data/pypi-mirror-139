from chia_xch.providers import *
from chia_xch.wallet import Wallet
from chia_xch.full_node import FullNode


class Xch:

    @staticmethod
    def wallet(provider: WalletProvider):
        return Wallet(provider)

    @staticmethod
    def full_node(provider: FullNodeProvider):
        return FullNode(provider)
