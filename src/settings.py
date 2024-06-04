import os
import json
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

RPC_L1_ENDPOINT = os.getenv("RPC_L1_ENDPOINT")
RPC_L1_NAME = os.getenv("RPC_L1_NAME")
VMANAGER_ADDRESS = os.getenv("VMANAGER_ADDRESS")

def load_helper_abi():
    with open("src/abi.json") as abi_file:
        abi = json.load(abi_file)

    if(abi is None):
        self.logger.error("Helper abi not found for contract")  

    return abi