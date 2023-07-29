import json
from fastapi.testclient import TestClient
from main import app
from fastapi import FastAPI
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app
from database import SessionLocal, engine, Base
import models
import uuid

client = TestClient(app)
def assert_menu_properties(response_json):
    # проверяем пришли id и тд в ответе
    if not response_json:
        return
    assert "id" in response_json
    assert "title" in response_json
    assert "description" in response_json

# Создаем фикстуру для создания меню и удаления
@pytest.fixture
def menu_id():
    # Информация для создания
    data = {
        'title': 'Menu 2',
        'description': 'Description for menu 1'
    }
    response = client.post('/api/v1/menus', json=data)
    assert response.status_code == 201
    created_menu = response.json()
    # Удаление меню после теста
    yield created_menu['id']
    client.delete(f'/api/v1/menus/{created_menu["id"]}')

# Получение всех меню
def test_get_menus():
    response = client.get('/api/v1/menus/')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Тестируем правильно ли создается меню
def test_create_menus(menu_id):
    response = client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert_menu_properties(response.json())
    created_menu = response.json()
    assert created_menu['title'] == 'Menu 2'
    assert created_menu['description'] == 'Description for menu 1'

# Тест на update
def test_update_menu(menu_id):
    data = {
        'title': 'Updated Menu 2',
        'description': 'Updated Description 1'
    }
    response = client.patch(f'/api/v1/menus/{menu_id}', json=data)
    assert response.status_code == 200
    assert_menu_properties(response.json())
    updated_menu = response.json()
    assert updated_menu['title'] == data['title']
    assert updated_menu['description'] == data['description']

# Тестируем read определенного меню
def test_read_menus(menu_id):
    response = client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert_menu_properties(response.json())

# Удаляем меню
def test_delete_menu(menu_id):
    response = client.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert_menu_properties(response.json())
# Проверяем, что меню пустые
def test_menu_empty():
    response = client.get('/api/v1/menus/')
    assert response.status_code == 200
    assert response.json() == []
   # Проверяем, что при вызове меню по айди, ничего не найдет
def test_empty_menu_id(menu_id):
    client.delete(f'/api/v1/menus/{menu_id}')
    response = client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}