from .event_listener import EventListener
import src.log as log
from src.adapters.Hyperstack import HyperStack
from src.providers.database_provider import get_db
import random

logger = log.get_logger(__name__)

class CreateVirtualMachine(EventListener):
    FILTER = "VirtualMachineCreated"

    def __init__(self, web3, contract_address):
        print('VirtualMachineCreated watcher started')
        super().__init__(web3, contract_address, self.FILTER)
        self.hyperstack = HyperStack()
        self.colors = [
            "Crimson", "FireBrick", "Maroon", "Burgundy", "Carmine", "Cerise",
            "Coral", "Salmon", "Magenta", "Fuchsia", "Rose", "Ruby", "Mahogany",
            "Tomato", "DeepPink", "HotPink", "LightCoral", "DarkSalmon", "LightSalmon"
        ]
        self.animals = [
            "Lion", "Lamb", "Eagle", "Serpent", "Dove", "Raven", "Ox", "Leopard", 
            "Bear", "Wolf", "Horse", "Unicorn", "Leviathan", "Vulture"
        ]

    def on_event(self, event):
        print('EVENT CAUGHT')
        vm_id = event['args']['vmId']  # Extract user address from event
        user_address = event['args']['operator']  # Extract user address from event
        vm_data = self.get_vm_data_template()
        print(event)

        # Create VM using Hyperstack
        response = self.create_vm(vm_data)
        if response and response.get('status'):
            instance = response['instances'][0]
            self.insert_vm_data(vm_data['name'], instance['id'], vm_id, user_address)

    def match_condition(self, event):
        return True

    def create_vm(self, vm_data):
        try:
            response = self.hyperstack.post("virtual-machines", vm_data)
            logger.info(f"VM creation response: {response}")
            return response
        except Exception as e:
            logger.error(f"VM creation failed: {str(e)}")
            return None

    def get_vm_data_template(self):
        color = random.choice(self.colors)
        animal = random.choice(self.animals)
        number = random.randint(100000, 999999)
        random_name = f"{color}-{animal}{number}"
        if len(random_name) > 50:
            random_name = f"{color[:25]}-{animal[:20]}{number}"
        return {
            "name": random_name,
            "environment_name": "CFT-BASIC",
            "image_name": "Ubuntu Server 22.04 LTS R535 CUDA 12.2",
            "volume_name": "",
            "create_bootable_volume": False,
            "user_data": "#cloud-config\nusers:\n  - name: demo\n    ssh-authorized-keys:\n      - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCnLaIyV2h7JYEjqN+jOq09cTK5VP6XclvkmWhbxmSyw+T4LRecJxT8kTf1GFXXNPeaLsRzvv/13cDW+2IGYB6D2WjShkkSg2zV9jZH6zIDNClOlaBHo/rj2YEI4R4aQl+6WCa/JVo3gz6zdOcwSkqO3DimrgpHdYSSCn5MdNSgeZY8LW3sdHyW77DDW2LPN35BNSdKDcHGJZCCTrw96yy10aJnzmPJIcQ5sxI0B8IloHgo+17uM8SLQ5Yqaon/81YI4ZTgAOg6KbxHxuXP/4USVa8mNxoyfB2OtpLo+Tm28E744YtX3DmFVeO6QKDOQED/2blNjps+t1OW+aiTDedr3/HCByGxbci8ZswhDp2VzHJEpe2rmPkOd8SKoCyN1v2Kxt0x7wVp35ZlUZ9K4zDFMqKxRZpwV2p3eRsYIzfpl+OSbb/8V5mJ3J4/0s7uweY3Ys06CJ2lz6vg5bcJVi9tjnsppjdBRU9XIYChskwqrwHwQON/X2OCA+yIa+Y2jBtX9SB/UwtcUzLjnFQSzIxiuJJeUm2O7wfQvONbVnzJCj49sTe4v0sGPQJZUA6mDT7dYkDXVtB+Sc7q0n3zART+oHMObWwS1XvAOXZC7HGDqX/2r403dQpJvFB7XngRHZI/hxls8zrWwM1SFeKekd1R4b6q6Cx9WH91zEC1MVrx7Q== mis4nthr0pic@proton.me\n    sudo: ['ALL=(ALL) NOPASSWD:ALL']\n    groups: sudo\n    shell: /bin/bash\nwrite_files:\n  - path: /etc/ssh/sshd_config\n    content: |\n         Port 4444",
            "flavor_name": "n1-cpu-small",
            "key_name": "MIS KEY",
            "assign_floating_ip": True,
            "count": 1
        }

    def insert_vm_data(self, name, id_host, vm_id, user_address):
        """Insert VM data into the database."""
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO virtual_machines (id_contract, id_host, machine_name, owner_address, status)
                VALUES (%s, %s, %s, %s, %s);
                """,
                (
                    vm_id,
                    id_host,
                    name,
                    user_address,
                    1
                )
            )

            conn.commit()
            logger.info(f"Inserted VM data into database for VM {vm_id}")
        except Exception as e:
            logger.error(f"Error inserting VM data into database: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def get_status(self, status):
        """Convert status string to integer for database."""
        status_map = {
            'active': 1,
            'inactive': 0,
            'terminated': 2
        }
        return status_map.get(status.lower(), 0)
