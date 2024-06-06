from web3 import Web3
import src.log as log

logger = log.get_logger(__name__)

class ConnectionProvider:
    ERROR_CANT_CONNECT = "Could not connect to RPC server"

    def __init__(self, name, url, is_http=False):
        self.name = name
        self.url = url

    def connect(self, is_http=False):
        if  is_http:
            web3 = Web3(Web3.HTTPProvider(self.url))
        else:
            web3 = Web3(Web3.WebsocketProvider(self.url))

        if not web3.is_connected():
            self.on_error(self.ERROR_CANT_CONNECT)
            return None

        logger.info("Connected to RPC server: %s", self.name)
        return web3

    def on_error(self, error):
        logger.error("Error: %s", error)

def main():
    provider = ConnectionProvider("MyProvider", "http://localhost:8545", is_http=True)
    web3 = provider.connect()
    if web3:
        print("Connection successful!")
    else:
        print("Connection failed.")

if __name__ == "__main__":
    main()
