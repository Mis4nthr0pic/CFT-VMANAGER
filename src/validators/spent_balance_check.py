# src/validators/spent_balance_check.py

import time
from .validator import Validator
from web3 import Web3
import src.log as log
from src.settings import load_json, DB_FILE

logger = log.get_logger(__name__)

class SpentBalanceCheck(Validator):
    def __init__(self, web3, contract_address):
        print("Starting Spent Check Validator")
        super().__init__(web3, contract_address)
        self.user_vm_data = load_json(DB_FILE)  # Load data on init
        self.last_processed_block = self.w3.eth.block_number

    def validate(self):
        while True:
            try:
                for user_address, vm_ids in self.user_vm_data.get("users", {}).items():
                    print(user_address)
                    user_credits_wei = self.contract.functions.userMinuteCredits(user_address).call()
                    user_credits = Web3.from_wei(user_credits_wei, 'ether')  # Convert from wei to ether equivalent
                    for vm_id in vm_ids:
                        # Call getTotalMinutesConsumed for each VM
                        total_minutes = self.contract.functions.getTotalMinutesConsumed(vm_id).call()
                        # Process the retrieved total minutes (log, store, etc.)
                        print(f"VM {vm_id} has consumed {total_minutes} minutes")
                time.sleep(2)  # Sleep for 2 seconds before the next validation
            except Exception as e:
                logger.error(f"Error in validating: {e}")
                time.sleep(2)  # Sleep for 2 seconds before retrying
