import multiprocessing
import logging
from web3 import Web3
import src.settings as settings
import src.log as log
from src.listeners.create_vm import CreateVirtualMachine
from src.listeners.start_vm import StartVirtualMachine
from src.validators.spent_balance_check import SpentBalanceCheck
from src.validators.validator import Validator

logger = log.get_logger(__name__)

def run_listener(listener_class, web3_url, contract_address):
    web3 = Web3(Web3.HTTPProvider(web3_url))
    if not web3.is_connected():
        logger.error(f"Failed to connect to Web3 at {web3_url}")
        return
    instance = listener_class(web3, contract_address)
    
    if isinstance(instance, Validator):
        instance.validate()
    else:
        instance.listen()

def main():
    # Define the listener processes
    listeners = [
        (CreateVirtualMachine, settings.RPC_L1_ENDPOINT, settings.VMANAGER_ADDRESS),
        (StartVirtualMachine, settings.RPC_L1_ENDPOINT, settings.VMANAGER_ADDRESS),
        (SpentBalanceCheck, settings.RPC_L1_ENDPOINT, settings.VMANAGER_ADDRESS)  # Adjust as needed
    ]

    processes = []
    for listener_class, web3_url, contract_address in listeners:
        process = multiprocessing.Process(target=run_listener, args=(listener_class, web3_url, contract_address))
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
