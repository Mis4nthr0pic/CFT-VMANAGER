from .event_listener import EventListener
import src.log as log
from src.adapters.Hyperstack import HyperStack
from src.providers.database_provider import get_db

logger = log.get_logger(__name__)

class StopVirtualMachine(EventListener):
    FILTER = "VirtualMachineStopped"
    ON_EVENT_MESSAGE = "Stopping VM: %s"

    def __init__(self, web3, contract_address):
        print('VirtualMachineStopped watcher started')
        super().__init__(web3, contract_address, self.FILTER)
        self.hyperstack = HyperStack()

    def match_condition(self, event):
        return True

    def on_event(self, event):
        print('EVENT CAUGHT')
        print(event)
        # Extract relevant information from the event
        vm_id = event['args']['vmId']
        operator = event['args']['operator']
        self.stop_vm(vm_id)
        self.update_vm_status(vm_id, '0')

    def stop_vm(self, vm_id):

        #load id_host based on vm_id from sql database
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id_host FROM virtual_machines WHERE id_contract = %s;", (vm_id,))
        id_host = cursor.fetchone()[0]

        try:
            response = self.hyperstack.get(f"virtual-machines/{id_host}/hibernate")
            logger.info(f"VM {vm_id} hibernated successfully.")
            print(f"VM {vm_id} hibernated successfully.")
        except Exception as e:
            logger.error(f"Failed to hibernate VM {vm_id}: {str(e)}")
            print(f"Failed to hibernate VM {vm_id}: {str(e)}")


    #create function to update SQL database with the new status of the virtual machine
    def update_vm_status(self, vm_id, status):
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE virtual_machines SET status = %s WHERE id_contract = %s;", (status, vm_id))
            conn.commit()
        except Exception as e:
            logger.error(f"Error updating VM status: {e}")
            print(f"Error updating VM status: {e}")
        finally:
            cursor.close()
            conn.close()