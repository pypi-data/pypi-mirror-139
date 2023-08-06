from filecoin_lotus.rpc_abi import RPC


class Chain:
    def __init__(self, filecoin):
        self._filecoin = filecoin
        self._provider = filecoin.provider

    def chain_head(self) -> dict:
        """
        Get the latest blocks
        :return:
        """
        return self._provider.make_request(RPC.chain_head, [])

    def chain_latest_height(self) -> int:
        """
        Get the latest block height
        :return:
        """
        resp = self.chain_head()
        return resp.get("Height")

    def chain_get_blocks_by_height(self, height: int) -> list:
        """
        Get all block hash at the same height
        :param height:
        :return:
        """
        res = self._provider.make_request(RPC.chain_getTipSetByHeight, [height, []])
        block_dict = res.get("Cids")
        blocks = [i["/"] for i in block_dict]
        return blocks

    def chain_get_messages_by_block(self, block_hash: str) -> dict:
        """
        Get message in specified block
        :param block_hash:
        :return: dict of messages : {"message_hash1":{"from":xxx,"to":xxx,"value":xxx}, "message_hash2":{"from":xxx,"to":xxx,"value":xxx}}
        """
        res = self._provider.make_request(RPC.chain_getBlockMessages, [{"/": block_hash}])
        messages = {}
        bls_messages = res.get("BlsMessages")
        if bls_messages:
            for m in bls_messages:
                m_hash = m.get("CID").get("/")
                messages.setdefault(
                    m_hash,
                    {
                        "from": m.get("From"),
                        "to": m.get("To"),
                        "value": self._filecoin.fromAtto(m.get("Value", "0"))
                    }
                )
        sec_message = res.get("SecpkMessages")
        if sec_message:
            for m in sec_message:
                m_info = m.get("Message")
                m_hash = m.get("CID").get("/")
                messages.setdefault(
                    m_hash,
                    {
                        "from": m_info.get("From"),
                        "to": m_info.get("To"),
                        "value": self._filecoin.fromAtto(m_info.get("Value", "0"))
                    }
                )
        return messages

    def chain_get_message_by_height(self, height: int) -> dict:
        """
        Get all message info at the same height
        :param height:
        :return:
        """
        messages = {}
        blocks = self.chain_get_blocks_by_height(height)
        for i in blocks:
            messages.update(self.chain_get_messages_by_block(i))
        return messages
