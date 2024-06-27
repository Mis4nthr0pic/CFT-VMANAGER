import multiprocessing
import src.settings as settings
import src.log as log
from src.providers.connection_provider import ConnectionProvider
from src.listeners.create_virtual_machine import CreateVirtualMachine
from src.listeners.start_virtual_machine import StartVirtualMachine
from src.listeners.stop_virtual_machine import StopVirtualMachine
from src.validators.spent_balance_check import SpentBalanceCheck
from src.validators.validator import Validator
from src.providers.database_provider import create_user  # Ensure this is correctly imported

logger = log.get_logger(__name__)

"""
def create_mock_user():
    try:
        # Assuming create_user returns the ID of the created user or None
        user_id = create_user("0xEeB40816c52DE2ae2875f2Ddef43DE9030891a10", 10000)
        if user_id:
            logger.info(f"Mock user created successfully with ID: {user_id}")
        else:
            logger.error("Failed to create mock user.")
    except Exception as e:
        logger.error(f"Error creating mock user: {str(e)}")
"""


def run_listener(listener_class, provider, contract_address):
    web3 = provider.connect(is_http=True)
    if not web3:
        logger.error(f"Failed to connect to Web3 at {provider.url}")
        return
    instance = listener_class(web3, contract_address)
    
    if isinstance(instance, Validator):
        instance.validate()
    else:
        instance.listen()

def main():
    #create_mock_user()  # Call to create a mock user before starting listeners

    # Define the listener processes
    listeners = [
        (CreateVirtualMachine, settings.RPC_L1_ENDPOINT, settings.VMANAGER_ADDRESS),
        (StartVirtualMachine, settings.RPC_L1_ENDPOINT, settings.VMANAGER_ADDRESS),
        (StopVirtualMachine, settings.RPC_L1_ENDPOINT, settings.VMANAGER_ADDRESS),
        #(SpentBalanceCheck, settings.RPC_L1_ENDPOINT, settings.VMANAGER_ADDRESS)  
    ]

    processes = []
    for listener_class, web3_url, contract_address in listeners:
        provider = ConnectionProvider(listener_class.__name__, web3_url)
        process = multiprocessing.Process(target=run_listener, args=(listener_class, provider, contract_address))
        process.start()
        processes.append(process)

    # Join the processes to ensure they keep running
    for process in processes:
        process.join()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Shutdown requested...exiting")
    except Exception:
        logger.exception("Error occurred during execution of the main application")
    finally:
        logger.info("Cleanup complete, application closed")
