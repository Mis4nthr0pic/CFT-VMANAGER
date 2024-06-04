from .event_listener import EventListener
import src.log as log

logger = log.get_logger(__name__)

class CreateVirtualMachine(EventListener):
    FILTER = "VirtualMachineCreated"
    ON_EVENT_MESSAGE = "Creating new VM: %s"
    API_ENDPOINT = "virtual-machines"

    def __init__(self, web3, contract_address):
        super().__init__(web3, contract_address, self.FILTER, 'latest')

    def match_condition(self, event):
        return True

    def on_event(self, event):
        print(event)
        #make post request to the api with json data
        #rest_provider.post(event)
        #logger.info(self.ON_EVENT_MESSAGE, event)
        
        
