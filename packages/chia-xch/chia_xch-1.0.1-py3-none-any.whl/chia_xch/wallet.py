from chia_xch.rpc_abi import RPC
from chia_xch.providers import WalletProvider
from chia_xch.encoding import FriendlyCode


class Wallet:
    """
    Some wallet function can't work before wallet loading, please ensure your wallet is loaded,
    you can check whether your wallet is loaded via list_wallets function. If your wallet is encrypted,
    please unlock your wallet via wallet_pass_phrase first
    """

    def __init__(self, provider: WalletProvider):
        self._provider = provider

    def log_in(self, fingerprint: int, log_in_type: str = "skip", recovery_host: str = "127.0.0.1"):
        return self._provider.make_request(RPC.wallet_login,
                                           {"fingerprint": fingerprint, "type": log_in_type, "host": recovery_host})

    def get_wallets(self):
        return self._provider.make_request(RPC.wallet_getWallets, {})

    def create_new_wallet(self, host: str = "127.0.0.1", wallet_type: str = "cc_wallet", mode: str = "new",
                          amount: int = 10000):
        return self._provider.make_request(RPC.wallet_createNewWallet,
                                           {"host": host, "wallet_type": wallet_type, "mode": mode, "amount": amount})

    def get_height_info(self):
        return self._provider.make_request(RPC.wallet_getHeightInfo, {})

    def get_sync_status(self):
        return self._provider.make_request(RPC.wallet_getSyncStatus, {})

    def get_private_key(self, fingerprint: int):
        return self._provider.make_request(RPC.wallet_getPrivateKey, {"fingerprint": fingerprint}).get("private_key")

    def generate_mnemonic(self):
        return self._provider.make_request(RPC.wallet_generateMnemonic, {}).get("mnemonic")

    def add_key(self, mnemonic: list, action_type: str = "new_wallet"):
        res = self._provider.make_request(RPC.wallet_addKey, {"mnemonic": mnemonic, "type": action_type})
        if res.get("status"):
            return res.get("1238658939")

    def del_key(self, fingerprint: int):
        return self._provider.make_request(RPC.wallet_deleteKey, {"fingerprint": fingerprint})

    def get_wallet_balance(self, wallet_id: int):
        """
        {
            'confirmed_wallet_balance': 89999990000,
            'max_send_amount': 89999990000,
            'pending_change': 0,
            'pending_coin_removal_count': 0,
            'spendable_balance': 89999990000,
            'unconfirmed_wallet_balance': 89999990000,
            'unspent_coin_count': 1,
            'wallet_id': 1
        }
        :param wallet_id:
        :return:
        """
        return self._provider.make_request(RPC.wallet_getWalletBalance, {"wallet_id": wallet_id}).get("wallet_balance")

    def get_next_address(self, wallet_id: int, new_address: bool = True):
        return self._provider.make_request(RPC.wallet_getNextAddress,
                                           {"wallet_id": wallet_id, "new_address": new_address}).get("address")

    def get_public_keys(self):
        return self._provider.make_request((RPC.wallet_getPublicKeys, {}))

    def get_transactions(self, wallet_id: int, start: int, end: int):
        return self._provider.make_request(RPC.wallet_getTransactions,
                                           {"wallet_id": wallet_id, "start": start, "end": end}).get("transactions")

    def send_transaction(self, wallet_id: int, amount: float, address: str, fee: int):
        if not self.get_sync_status().get("synced"):
            raise Exception("Wallet not synced")
        fe = FriendlyCode()
        return self._provider.make_request(RPC.wallet_sendTransaction,
                                           {"wallet_id": wallet_id, "amount": int(fe.value_encode(amount, 12)),
                                            "address": address, "fee": int(fe.value_encode(fee, 12))}).get(
            "transaction_id")
