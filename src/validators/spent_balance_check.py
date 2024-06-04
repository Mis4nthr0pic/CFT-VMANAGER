import json
from .validator import Validator
from web3 import Web3
import src.log as log

class SpentBalanceCheck(Validator):

    def __init__(self, web3, contract_address, user_vm_file="src/users.json"):
        print("Starting Spent Check Validator")
        super().__init__(web3, contract_address)
        self.last_processed_block = self.w3.eth.block_number
        self.user_vm_data = self.load_user_vm_data(user_vm_file)  # Load data on init
        print(self.user_vm_data)

    def load_user_vm_data(self, filename):
        """Loads user-VM data from a JSON file."""
        try:
            with open(filename) as json_file:
                user_vm_data = json.load(json_file)
            return user_vm_data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            log.error(f"Error loading user-VM data: {e}")
            return {}  # Return empty dict on error

    async def validate(self):
        print("Validating Bridge Gateway drained funds")
        for user_address, vm_ids in self.user_vm_data.get("users", {}).items():
            #load user credits from the contract
            user_credits_wei = self.contract.functions.userMinuteCredits(user_address).call()
            user_credits = Web3.from_wei(user_credits_wei, 'ether')  # Convert from wei to ether equivalent
            print(f"User {user_address}: {user_credits} minutes remaining")
            for vm_id in vm_ids:

                # Call getTotalMinutesConsumed for each VM
                total_minutes = self.contract.functions.getTotalMinutesConsumed(vm_id).call()
                # Process the retrieved total minutes (log, store, etc.)
                print(f"User {user_address}, VM {vm_id}: {total_minutes} minutes consumed")
                # You can add further logic to handle the retrieved data here

        return True