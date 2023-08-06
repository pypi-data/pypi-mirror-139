from filecoin_lotus.types_fil import RPCEndpoint

RPC_PREFIX = "Filecoin."


class RPC:
    # chain
    chain_head = RPCEndpoint(RPC_PREFIX + "ChainHead")
    chain_getBlock = RPCEndpoint(RPC_PREFIX + "ChainGetBlock")
    chain_getTipSetByHeight = RPCEndpoint(RPC_PREFIX + "ChainGetTipSetByHeight")
    chain_getBlockMessages = RPCEndpoint(RPC_PREFIX + "ChainGetBlockMessages")
    chain_getMessage = RPCEndpoint(RPC_PREFIX + "ChainGetMessage")

    # state
    state_searchMessage = RPCEndpoint(RPC_PREFIX + "StateSearchMsg")

    # mpool
    mpool_pushMessage = RPCEndpoint(RPC_PREFIX + "MpoolPushMessage")

    # wallet
    wallet_new = RPCEndpoint(RPC_PREFIX + "WalletNew")
    wallet_balance = RPCEndpoint(RPC_PREFIX + "WalletBalance")
    wallet_import = RPCEndpoint(RPC_PREFIX + "WalletImport")
    wallet_validate = RPCEndpoint(RPC_PREFIX + "WalletValidateAddress")
    wallet_export = RPCEndpoint(RPC_PREFIX+"WalletExport")
