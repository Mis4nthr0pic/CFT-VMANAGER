import multiprocessing
from web3 import Web3
import src.settings as settings
import src.log as log
from src.listeners.create_vm import CreateVirtualMachine
from src.listeners.start_vm import StartVirtualMachine
from src.listeners.stop_vm import StopVirtualMachine
from src.validators.spent_balance_check import SpentBalanceCheck
from src.validators.validator import Validator
from src.providers.connection_provider import ConnectionProvider

logger = log.get_logger(__name__)

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
    # Define the listener processes
    listeners = [
        (CreateVirtualMachine, settings.RPC_L1_ENDPOINT, settings.VMANAGER_ADDRESS, True),
        (StartVirtualMachine, settings.RPC_L1_ENDPOINT, settings.VMANAGER_ADDRESS, True),
        (StopVirtualMachine, settings.RPC_L1_ENDPOINT, settings.VMANAGER_ADDRESS, True),
        (SpentBalanceCheck, settings.RPC_L1_ENDPOINT, settings.VMANAGER_ADDRESS, True)  # Adjust as needed
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
        logger.info("Exit")
