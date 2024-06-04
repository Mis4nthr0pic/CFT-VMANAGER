from .event_listener import EventListener
import src.log as log
import requests

logger = log.get_logger(__name__)

class StopVirtualMachine(EventListener):
    FILTER = "VirtualMachineStopped"
    ON_EVENT_MESSAGE = "Creating new VM: %s"

    def __init__(self, web3, contract_address):
        print('VirtualMachineStopped watcher started')
        super().__init__(web3, contract_address, self.FILTER)

    def match_condition(self, event):
        return True

    def on_event(self, event):
        print('EVENT CAUGHT')
        print(event)
        # Extract relevant information from the event
        #vm_id = event['args']['vmId']
        #operator = event['args']['operator']
