from chia_xch.providers import FullNodeProvider
from chia_xch.rpc_abi import *


class FullNode:
    def __init__(self, provider: FullNodeProvider):
        self._provider = provider

    def get_blockchain_state(self):
        return self._provider.make_request(RPC.node_getBlockChainState, {})

    def get_additions_and_removals(self, header_hash: str):
        return self._provider.make_request(RPC.node_getAdditionAndRemovals, {"header_hash": header_hash})

    def get_block(self, header_hash: str):
        return self._provider.make_request(RPC.node_getBlock, {"header_hash": header_hash})

    def get_blocks(self, start: int, end: int, exclude_header_hash: bool = False):
        return self._provider.make_request(RPC.node_getBlocks,
                                           {"start": start, "end": end, "exclude_header_hash": exclude_header_hash})

    def get_block_record_by_height(self, height: int):
        return self._provider.make_request(RPC.node_getBlockRecordByHeight, {"height": height})

    def get_block_record(self, header_hash: str):
        return self._provider.make_request(RPC.node_getBlockRecord, {"header_hash": header_hash})

    def get_block_records(self, start: int, end: int):
        return self._provider.make_request(RPC.node_getBlockRecords, {"start": start, "end": end})

    def get_header_hash_by_height(self, height: int):
        record = self.get_block_record_by_height(height)
        return record.get("block_record").get("header_hash")
