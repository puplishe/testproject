import json
from fastapi.testclient import TestClient
from fastapi import FastAPI
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import uuid
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main_app.main import app, get_db
from main_app.tests.test_submenu import menu_id, submenu_id


client = TestClient(app)

#Функция для проверки правильности даты, которая приходит в ответе
def assert_dish_properties(response_json):
    if not response_json:
        return
    assert "id" in response_json
    assert "title" in response_json
    assert "description" in response_json
    assert "price" in response_json
    assert "submenu_id" in response_json


def test_create_dish(menu_id, submenu_id):
    # Создаем блюдо
    data = {
        'title': 'Test Dish',
        'description': 'Test Dish Description',
        'price': '9.99',
    }
    response = client.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=data)
    assert response.status_code == 201
    assert_dish_properties(response.json())
    created_dish = response.json()
    assert created_dish['title'] == 'Test Dish'
    assert created_dish['description'] == 'Test Dish Description'
    assert created_dish['price'] == '9.99'
    assert created_dish['submenu_id'] == submenu_id


def test_read_dish(menu_id, submenu_id):
    response = client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert response.status_code == 200
    dishes = response.json()
    assert isinstance(dishes, list)
    if dishes:
        assert_dish_properties(dishes[0])


def test_get_dish(menu_id, submenu_id):
    # Тестируем get запрос после создания блюда
    data = {
        'title': 'Test Dish',
        'description': 'Test Dish Description',
        'price': '9.99',
    }
    response = client.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=data)
    assert response.status_code == 201
    created_dish = response.json()
    dish_id = created_dish['id']

    response = client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code == 200
    assert_dish_properties(response.json())


def test_update_dish(menu_id, submenu_id):
    # Тестируем update блюда
    data = {
        'title': 'Test Dish',
        'description': 'Test Dish Description',
        'price': '9.99',
    }
    response = client.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=data)
    assert response.status_code == 201
    created_dish = response.json()
    dish_id = created_dish['id']

    update_data = {
        'title': 'Updated Dish',
        'description': 'Updated dish description',
        'price': '19.99',
    }
    response = client.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', json=update_data)
    assert response.status_code == 200
    assert_dish_properties(response.json())
    updated_dish = response.json()
    assert updated_dish['title'] == 'Updated Dish'
    assert updated_dish['description'] == 'Updated dish description'
    assert updated_dish['price'] == '19.99'
    assert updated_dish['submenu_id'] == submenu_id


def test_delete_dish(menu_id, submenu_id):
    # Тест удаления блюда
    data = {
        'title': 'Test Dish',
        'description': 'Test Dish Description',
        'price': '9.99',
    }
    response = client.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=data)
    assert response.status_code == 201
    created_dish = response.json()
    dish_id = created_dish['id']

    response = client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code == 200
    assert_dish_properties(response.json())
