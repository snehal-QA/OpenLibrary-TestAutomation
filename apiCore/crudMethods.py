import requests

class CrudMethods:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://openlibrary.org"

    def get_operation(self, endpoint,query_params: dict = None) -> requests.Response:
        url = self.base_url + endpoint
        response = self.session.get(url, query_params)
        return response