import pytest
from apiCore.crudMethods import crudMethods
from apiCore.endpoints import Endpoints

client = crudMethods()

@pytest
def test_get_author():
    response = client.get_operation(Endpoints.SEARCH_BOOKS, query_params={"q": "J.K. Rowling"})
    assert response.status_code == 200
