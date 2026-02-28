import requests
import logging

logger = logging.getLogger(__name__)
DEFAULT_TIMEOUT = 30

class CrudMethods:
    def __init__(self):
        self.session = requests.Session()

    def get_operation(
            self, 
            endpoint_url,
            query_params: dict = None,
            timeout:int = DEFAULT_TIMEOUT
            ) -> requests.Response:
        logger.info("GET %s params=%s", endpoint_url, query_params)
        response = self.session.get(
            endpoint_url, 
            params=query_params, 
            timeout=timeout
            )
        logger.debug("Response %s from %s", response.status_code, endpoint_url)
        logger.debug("Response body (first 500 chars): %s", response.text[:500])
        return response
    
    def close(self):
        self.session.close()