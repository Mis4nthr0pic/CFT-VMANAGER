import src.log as log
from src.adapters.Hyperstack import HyperStack
import random

logger = log.get_logger(__name__)

class CreateVirtualMachine:
    FILTER = "VirtualMachineCreated"
    ON_EVENT_MESSAGE = "Creating VM: %s"

    def __init__(self, web3, contract_address, api_key):
        self.web3 = web3
        self.contract_address = contract_address
        self.hyperstack = HyperStack(api_key)
        self.animals = [
            "Lion", "Lamb", "Eagle", "Serpent", "Dove", "Raven", "Ox", "Leopard", 
            "Bear", "Wolf", "Horse", "Unicorn", "Leviathan", "Vulture"
        ]

    def listen(self):
        # Listening logic here
        pass

    def on_event(self, event):
        print('EVENT CAUGHT')
        print(event)
        # Generate VM data
        vm_data = self.get_vm_data_template()
        # Create the VM
        #self.create_vm(vm_data)

    def create_vm(self, vm_data):
        try:
            response = self.hyperstack.post("virtual-machines", vm_data)
            logger.info(f"VM creation successful: {response}")
            return response
        except Exception as e:
            logger.error(f"VM creation failed: {str(e)}")
            return None

    def get_vm_data_template(self):
        random_name = f"{random.choice(self.animals)}{random.randint(100000, 999999)}"
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