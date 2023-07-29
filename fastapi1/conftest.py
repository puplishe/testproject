import pytest
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

@pytest.fixture
def menu_id():
    # Test for creating a menu
    data = {
        'title': 'Menu 1',
        'description': 'Description for menu 1'
    }
    response = client.get('/api/v1/menus', json=data)
    menu_id = response.json()["id"]

    return menu_id