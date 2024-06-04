import asyncio
import src.settings as settings
import src.log as log
from src.providers.connection_provider import connectionProvider
from src.listeners.create_vm import CreateVirtualMachine
from src.listeners.start_vm import StartVirtualMachine
from src.validators.spent_balance_check import SpentBalanceCheck

logger = log.get_logger(__name__)

async def main():
    # Initialize Web3 connection
    web3L1 = connectionProvider(settings.RPC_L1_NAME, settings.RPC_L1_ENDPOINT, is_http=False).connect()

    # Initialize event listeners and validators
    virtual_machine_create = CreateVirtualMachine(web3L1, settings.VMANAGER_ADDRESS)
    virtual_machine_started = StartVirtualMachine(web3L1, settings.VMANAGER_ADDRESS)
    spent_balance_checker = SpentBalanceCheck(web3L1, settings.VMANAGER_ADDRESS)

    # Run listeners and validators concurrently
    while(True):
        await asyncio.create_task(virtual_machine_create.listen())    
        await asyncio.create_task(virtual_machine_started.listen())
        await asyncio.create_task(spent_balance_checker.validate())

        print("scanning blocknumber: ", web3L1.eth.get_block('latest').number)
        await asyncio.sleep(2)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Exit")
