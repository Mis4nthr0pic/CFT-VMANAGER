import asyncio
import src.settings as settings
import src.log as log
from src.providers.connection_provider import connectionProvider
from src.listeners.create_vm import CreateVirtualMachine
from src.validators.spent_balance_check import SpentBalanceCheck
#from src.listeners.bridge_messenger_owner_changed import BridgeMessengerOwnerChanged
#from src.listeners.bridge_address_manager_value_updated import BridgeAddressManagerValueUpdated
#from src.listeners.bridge_messenger_is_paused import BridgeMessengerIsPaused
#from src.validators.bridge_gateway_funds_drained import BridgeGatewayFundsDrained

logger = log.get_logger(__name__)


#create a hello world python
async def main():
    # Connect to websocket
    web3L1 = connectionProvider(settings.RPC_L1_NAME, settings.RPC_L1_ENDPOINT, is_http=True).connect()

    # Start listener
    #virtual_machine_create = CreateVirtualMachine(web3L1, settings.VMANAGER_ADDRESS);
    SpentBalanceChecker = SpentBalanceCheck(web3L1, settings.VMANAGER_ADDRESS)

    #bridgeMessengerOwnerChangedListener = BridgeMessengerOwnerChanged(web3L1, settings.CONTRACT_ADDRESS)
    #bridgeAddressManagerValueUpdated = BridgeAddressManagerValueUpdated(web3L1, settings.CONTRACT_ADDRESS)
    #bridgeMessengerIsPaused = BridgeMessengerIsPaused(web3L1, settings.CONTRACT_ADDRESS)
    #bridgeWithdrawExceedsThreshold = BridgeWithdrawExceedsThreshold(web3L1, settings.CONTRACT_ADDRESS)
    #bridgeMultisigChangedThreshold = BridgeMultisigChangedThreshold(web3L1, settings.CONTRACT_ADDRESS)

    while True:
        await asyncio.create_task(SpentBalanceChecker.validate())
        #first run validators
        #await asyncio.create_task(bridgeMessengerOwnerChangedListener.listen())
        #await asyncio.create_task(bridgeAddressManagerValueUpdated.listen())
        #await asyncio.create_task(bridgeMessengerIsPaused.listen())
        #await asyncio.create_task(bridgeWithdrawExceedsThreshold.listen())
        #await asyncio.create_task(bridgeMultisigChangedThreshold.listen())
        
        #print("scanning blocknumber: ", web3L1.eth.get_block('latest').number)
        await asyncio.sleep(5)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Exit")



