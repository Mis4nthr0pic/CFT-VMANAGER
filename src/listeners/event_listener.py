import logging
from web3 import Web3
from src.settings import load_helper_abi
from src.providers.database_provider import get_db
from decimal import Decimal

logger = logging.getLogger(__name__)

class EventListener:
    def __init__(self, web3: Web3, contract_address: str, event_name: str):
        self.w3 = web3
        self.contract_address = contract_address
        abi = load_helper_abi()
        self.contract = self.w3.eth.contract(address=contract_address, abi=abi)
        self.event_name = event_name
        self.last_processed_block = int(self.get_last_processed_block())  # Fetch from database
        logger.info(f"LAST BLOCK PROCESSED: {self.last_processed_block}")
        logger.info(f"{self.event_name} event listener started")

    def listen(self):
        while True:
            try:
                latest_block = self.w3.eth.get_block('latest').number
                logger.info(f"Listening for {self.event_name} from block {self.last_processed_block} to {latest_block}")

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
                    self.update_last_processed_block(latest_block)
            except Exception as e:
                logger.error(f"Error in listening to events: {e}")

    def match_condition(self, event):
        return True

    def on_event(self, event):
        pass

    def get_last_processed_block(self):
        """Fetch the last processed block from the database."""
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT block FROM processed_blocks WHERE event_name = %s ORDER BY id DESC LIMIT 1;", (self.event_name,))
            row = cursor.fetchone()
            return row[0] if row else 0
        except Exception as e:
            logger.error(f"Error fetching last processed block: {e}")
            return 0
        finally:
            cursor.close()
            conn.close()

    def update_last_processed_block(self, block):
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT block FROM processed_blocks WHERE event_name = %s ORDER BY id DESC LIMIT 1;", (self.event_name,))
            row = cursor.fetchone()
            if row:
                cursor.execute("UPDATE processed_blocks SET block = %s WHERE event_name = %s;", (block, self.event_name))
            else:
                cursor.execute("INSERT INTO processed_blocks (event_name, block) VALUES (%s, %s);", (self.event_name, block))
            conn.commit()
        except Exception as e:
            logger.error(f"Error updating last processed block: {e}")
        finally:
            cursor.close()
            conn.close()

