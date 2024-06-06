import os
import json
import logging
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

# Environment variables
RPC_L1_ENDPOINT = os.getenv("RPC_L1_ENDPOINT")
RPC_L1_NAME = os.getenv("RPC_L1_NAME")
VMANAGER_ADDRESS = os.getenv("VMANAGER_ADDRESS")
HYPERSTACK_KEY = os.getenv("HYPERSTACK_KEY")
DB_FILE = os.getenv("DB_FILE")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_json(filename):
    """Loads user-VM data from a JSON file."""
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error loading user-VM data: {e}")
        return {}  # Return empty dict on error

def save_json(data, filename):
    """Saves data to a JSON file."""
    try:
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        logger.info(f"Data successfully saved to {filename}")
    except Exception as e:
        logger.error(f"Error saving data to {filename}: {e}")

def update_json(filename, primary_key, nested_key, value):
    """Updates a specific nested key in the JSON file with a new value."""
    try:
        # Load existing data
        json_data = load_json(filename)
        
        # Ensure the primary key exists
        if primary_key not in json_data:
            json_data[primary_key] = {}
        
        # Update the nested key with the new value
        json_data[primary_key][nested_key] = value
        
        # Save the updated data back to the file
        save_json(json_data, filename)
        
        logger.info(f"Data successfully updated for '{primary_key}/{nested_key}' in {filename}")
    except Exception as e:
        logger.error(f"Error updating '{primary_key}/{nested_key}' in {filename}: {e}")

def load_helper_abi():
    """Loads the ABI for the helper contract."""
    try:
        with open("src/abi.json", 'r') as abi_file:
            abi = json.load(abi_file)
        if abi is None:
            logger.error("Helper ABI not found for contract")
        return abi
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error loading helper ABI: {e}")
        return None
