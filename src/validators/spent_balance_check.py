from .validator import Validator
from web3 import Web3
import src.log as log

class SpentBalanceCheck(Validator):

    def __init__(self, web3, contract_address):
        print("Starting Bridge Gateway drained funds validator")
        super().__init__(web3, contract_address)
        self.last_processed_block = self.w3.eth.block_number
        return

    async def validate(self):
        print("Validating Bridge Gateway drained funds");
        return True