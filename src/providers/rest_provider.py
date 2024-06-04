from requests import get, post
import src.log as log

logger = log.get_logger(__name__)

class rest_provider:
#make post and get requests to the api and handle results
    def __init__(self, url):
        self.url = url

    #create get function with optional parameters
    def get(self):
        pass

    def post(self):
        pass

    def handle_result(self, response):
        pass

    def on_error(self, error):
        logger.error("Error: ", error)