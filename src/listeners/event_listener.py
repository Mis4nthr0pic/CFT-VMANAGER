import asyncio
import src.log as log
from web3 import Web3
from src.settings import load_helper_abi

logger = log.get_logger(__name__)

class EventListener:
    status = True

    def __init__(self, web3, contract_address, event_name):
        self.w3 = web3
        self.contract_address = contract_address
        abi = load_helper_abi()
        self.contract = self.w3.eth.contract(address=contract_address, abi=abi)
        self.event_name = event_name
        logger.info("%s event listener started", self.event_name)

    async def listen(self):
        event_filter = self.contract.events[self.event_name].create_filter(fromBlock='latest')
        while True:
            for event in event_filter.get_new_entries():
                if self.match_condition(event):
                    logger.info("%s event received:", self.event_name)
                    logger.info(" - block: %d", event['blockNumber'])
                    logger.info(" - tx: %s", event['transactionHash'].hex())
                    logger.info(" - contract: %s", self.contract_address)
                    self.on_event(event)

    def match_condition(self, event):
        return True

    def on_event(self, event):
        pass
