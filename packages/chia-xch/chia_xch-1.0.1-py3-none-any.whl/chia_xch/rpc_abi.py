from chia_xch.types_xch import RPCEndpoint


class RPC:
    node_getBlockChainState = RPCEndpoint("get_blockchain_state")
    node_getBlock = RPCEndpoint("get_block")
    node_getBlocks = RPCEndpoint("get_blocks")
    node_getBlockRecordByHeight = RPCEndpoint("get_block_record_by_height")
    node_getBlockRecord = RPCEndpoint("get_block_record")
    node_getBlockRecords = RPCEndpoint("get_block_records")
    node_getUnfinishedBlockHeader = RPCEndpoint("get_unfinished_block_headers")
    node_getNetworkSpace = RPCEndpoint("get_network_space")
    node_getAdditionAndRemovals = RPCEndpoint("get_additions_and_removals")

    wallet_login = RPCEndpoint("log_in")
    wallet_getWallets = RPCEndpoint("get_wallets")
    wallet_createNewWallet = RPCEndpoint("create_new_wallet")
    wallet_getHeightInfo = RPCEndpoint("get_height_info")
    wallet_getSyncStatus = RPCEndpoint("get_sync_status")
    wallet_getPrivateKey = RPCEndpoint("get_private_key")
    wallet_generateMnemonic = RPCEndpoint("generate_mnemonic")
    wallet_addKey = RPCEndpoint("add_key")
    wallet_deleteKey = RPCEndpoint("delete_key")
    wallet_getWalletBalance = RPCEndpoint("get_wallet_balance")
    wallet_getNextAddress = RPCEndpoint("get_next_address")
    wallet_getPublicKeys = RPCEndpoint("get_public_keys")
    wallet_getTransactions = RPCEndpoint("get_transactions")
    wallet_sendTransaction = RPCEndpoint("send_transaction")

