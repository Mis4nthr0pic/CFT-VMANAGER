from .event_listener import EventListener
import src.log as log

logger = log.get_logger(__name__)

class StartVirtualMachine(EventListener):
    FILTER = "VirtualMachineStarted"
    ON_EVENT_MESSAGE = "Starting VM: %s"

    def __init__(self, web3, contract_address):
        print('VirtualMachineStarted watcher started')
        super().__init__(web3, contract_address, self.FILTER)

    def match_condition(self, event):
        return True

    def on_event(self, event):
        print('EVENT CAUGHT')
        print(event)
        # Extract relevant information from the event
        vm_id = event['args']['vmId']
        operator = event['args']['operator']
