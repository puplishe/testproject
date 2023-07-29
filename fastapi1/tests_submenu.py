import json
from fastapi.testclient import TestClient
from fastapi import FastAPI
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
import uuid
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app, get_db
from schemas import SubmenuCreate, SubmenuUpdate
import models


client = TestClient(app)


# Fixture to create menu and return its id
@pytest.fixture
def menu_id():
    data = {
        'title': 'Menu 2',
        'description': 'Description for menu 1'
    }
    response = client.post('/api/v1/menus', json=data)
    assert response.status_code == 201
    created_menu = response.json()
    yield created_menu['id']
    client.delete(f'/api/v1/menus/{created_menu["id"]}')

# Fixture to create a submenu for the given menu_id and return its id
@pytest.fixture
def submenu_id(menu_id):
    submenu_data = {
        'title': 'Test Submenu',
        'description': 'Test Submenu Description'
    }
    response = client.post(f'/api/v1/menus/{menu_id}/submenus', json=submenu_data)
    assert response.status_code == 201
    created_submenu = response.json()
    yield created_submenu['id']
    client.delete(f'/api/v1/menus/{menu_id}/submenus/{created_submenu["id"]}')

# Test cases for submenus
def test_create_submenu(menu_id):
    submenu_data = {
        'title': 'Test Submenu',
        'description': 'Test Submenu Description'
    }
    response = client.post(f'/api/v1/menus/{menu_id}/submenus', json=submenu_data)
    assert response.status_code == 201
    created_submenu = response.json()
    assert 'id' in created_submenu
    assert created_submenu['title'] == submenu_data['title']
    assert created_submenu['description'] == submenu_data['description']

def test_read_submenu(menu_id, submenu_id):
    response = client.get(f'/api/v1/menus/{menu_id}/submenus')
    assert response.status_code == 200
    submenus = response.json()
    assert len(submenus) > 0
    assert submenu_id == submenus[0]['id']

def test_update_submenu(menu_id, submenu_id):
    updated_data = {
        'title': 'Updated Submenu',
        'description': 'Updated Submenu Description'
    }
    response = client.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}', json=updated_data)
    assert response.status_code == 200
    updated_submenu = response.json()
    assert updated_submenu['title'] == updated_data['title']
    assert updated_submenu['description'] == updated_data['description']

def test_delete_submenu(menu_id, submenu_id):
    response = client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200

def test_submenu_empty(menu_id):
    response = client.get(f'/api/v1/menus/{menu_id}/submenus')
    assert response.status_code == 200
    assert response.json() == []