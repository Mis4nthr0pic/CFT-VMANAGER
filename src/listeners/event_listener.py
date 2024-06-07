import logging
from web3 import Web3
from src.settings import load_helper_abi, load_json, update_json, DB_FILE

logger = logging.getLogger(__name__)

class EventListener:
    def __init__(self, web3: Web3, contract_address: str, event_name: str):
        self.w3 = web3
        self.contract_address = contract_address
        abi = load_helper_abi()
        self.contract = self.w3.eth.contract(address=contract_address, abi=abi)
        self.event_name = event_name
        self.last_processed_block = load_json(DB_FILE).get("processed_blocks", {}).get(self.event_name, 0)
        logger.info(f"LAST BLOCK PROCESSED: {self.last_processed_block}")
        logger.info(f"{self.event_name} event listener started")

    def listen(self):
        while True:
            try:
                latest_block = self.w3.eth.get_block('latest').number
                logger.info(f"Listening for {self.event_name} from block {self.last_processed_block} to {latest_block}")

                if self.last_processed_block == 'lastest':
                    self.last_processed_block = latest_block

                if latest_block > self.last_processed_block:
                    event_filter = self.contract.events[self.event_name].create_filter(fromBlock=self.last_processed_block + 1, toBlock=latest_block)
                    events = event_filter.get_all_entries()
                    for event in events:
                        logger.info(f"{self.event_name} event received:")
                        logger.info(f" - block: {event['blockNumber']}")
                        logger.info(f" - tx: {event['transactionHash'].hex()}")
                        logger.info(f" - contract: {self.contract_address}")
                        if self.match_condition(event):
                            self.on_event(event)
                    self.last_processed_block = latest_block
                    update_json(DB_FILE, "processed_blocks", self.event_name, latest_block)
            except Exception as e:
                logger.error(f"Error in listening to events: {e}")

    def match_condition(self, event):
        return True

    def on_event(self, event):
        pass
