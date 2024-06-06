from .event_listener import EventListener
import src.log as log
from src.adapters.Hyperstack import HyperStack

logger = log.get_logger(__name__)

class StopVirtualMachine(EventListener):
    FILTER = "VirtualMachineStopped"
    ON_EVENT_MESSAGE = "Stopping VM: %s"

    def __init__(self, web3, contract_address, api_key):
        print('VirtualMachineStopped watcher started')
        super().__init__(web3, contract_address, self.FILTER)
        self.hyperstack = HyperStack(api_key)

    def match_condition(self, event):
        return True

    def on_event(self, event):
        print('EVENT CAUGHT')
        print(event)
        # Extract relevant information from the event
        vm_id = event['args']['vmId']
        operator = event['args']['operator']
        #self.stop_vm(vm_id)

    def stop_vm(self, vm_id):
        try:
            response = self.hyperstack.get(f"virtual-machines/{vm_id}/hibernate")
            logger.info(f"VM {vm_id} hibernated successfully.")
            print(f"VM {vm_id} hibernated successfully.")
        except Exception as e:
            logger.error(f"Failed to hibernate VM {vm_id}: {str(e)}")
            print(f"Failed to hibernate VM {vm_id}: {str(e)}")
