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




client = TestClient(app)



# Функция, чтобы постоянно проверять, 200 ответ, что возвращается id, title, description, либо  [], если пустое сабменю
def assert_properties(response, status_code=200):
    assert response.status_code == status_code
    response_json = response.json()
    if not response_json:
        return
    assert "id" in response_json
    assert "title" in response_json
    assert "description" in response_json

# Фикстура для создания меню
@pytest.fixture
def menu_id():
    data = {
        'title': 'Menu 2',
        'description': 'Description for menu 1'
    }
    response = client.post('/api/v1/menus', json=data)
    assert_properties(response, status_code=201)
    created_menu = response.json()
    yield created_menu['id']
    client.delete(f'/api/v1/menus/{created_menu["id"]}')

# Фикстура для создания сабменю
@pytest.fixture
def submenu_id(menu_id):
    submenu_data = {
        'title': 'Test Submenu',
        'description': 'Test Submenu Description'
    }
    response = client.post(f'/api/v1/menus/{menu_id}/submenus', json=submenu_data)
    assert_properties(response, status_code=201)
    created_submenu = response.json()
    yield created_submenu['id']
    client.delete(f'/api/v1/menus/{menu_id}/submenus/{created_submenu["id"]}')

# Тест для создания сабменю
def test_create_submenu(menu_id):
    submenu_data = {
        'title': 'Test Submenu',
        'description': 'Test Submenu Description'
    }
    response = client.post(f'/api/v1/menus/{menu_id}/submenus', json=submenu_data)
    assert_properties(response, status_code=201)
    created_submenu = response.json()
    assert 'id' in created_submenu
    assert created_submenu['title'] == submenu_data['title']
    assert created_submenu['description'] == submenu_data['description']

#Тест для чтения сабменю
def test_read_submenu(menu_id, submenu_id):
    response = client.get(f'/api/v1/menus/{menu_id}/submenus')
    submenus = response.json()
    assert isinstance(submenus, list)
    # Проверяем, что созданное сабменю есть в списке всех сабменю
    submenu = next((submenu for submenu in submenus if submenu['id'] == submenu_id), None)
    assert submenu is not None
    
 # Тест на апдейт сабменю
def test_update_submenu(menu_id, submenu_id):
    updated_data = {
        'title': 'Updated Submenu',
        'description': 'Updated Submenu Description'
    }
    response = client.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}', json=updated_data)
    assert_properties(response)
    updated_submenu = response.json()
    assert updated_submenu['title'] == updated_data['title']
    assert updated_submenu['description'] == updated_data['description']
    #проверяем, get запрос после patch запроса
    response_updated = client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    submenu_updated = response_updated.json()
    assert submenu_updated['title'] == updated_data['title']
    assert submenu_updated['description'] == updated_data['description']



def test_delete_submenu(menu_id, submenu_id):
    response = client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert_properties(response)

# проверяем, что после удаления сабменю пустое
def test_submenu_empty(menu_id):
    response = client.get(f'/api/v1/menus/{menu_id}/submenus')
    assert_properties(response)
    assert response.json() == []


#Задание с 2 звездочками
def test_check_menu_submenus_and_dishes_count(menu_id):
    num_submenus = 2
    num_dishes_per_submenu = 1
    #Создаем 2 сабменю
    submenu_data_1 = {
        'title': 'Test Submenu 1',
        'description': 'Test Submenu Description 1'
    }
    response = client.post(f'/api/v1/menus/{menu_id}/submenus', json=submenu_data_1)
    assert_properties(response, status_code=201)

    submenu_1 = response.json()
    submenu_id_1 = submenu_1['id']
    submenu_data_2 = {
        'title': 'Test Submenu 2',
        'description': 'Test Submenu Description 2'
    }
    response = client.post(f'/api/v1/menus/{menu_id}/submenus', json=submenu_data_2)
    assert_properties(response, status_code=201)
    #Создаем 2 блюда в разных сабменю
    submenu_2 = response.json()
    submenu_id_2 = submenu_2['id']
    dish_data_1 = {
        'title': 'Test Dish 1',
        'description': 'Test Dish Description 1',
        'price': '9.99',
    }
    dish_data_2 = {
        'title': 'Test Dish 2',
        'description': 'Test Dish Description 2',
        'price': '9.99',
    }
    response = client.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id_1}/dishes', json=dish_data_1)
    client.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id_2}/dishes', json=dish_data_2)
    assert_properties(response, status_code=201)

    # Проверяем кол-во сабменю и блюд в меню
    response = client.get(f'/api/v1/menus/{menu_id}')
    assert_properties(response, status_code=200)
    menu = response.json()

    assert menu['submenus_count'] == num_submenus
    assert menu['dishes_count'] == num_submenus * num_dishes_per_submenu
    #Проверяем кол-во блюд в 1 сабменю
    response = client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id_1}')
    assert_properties(response, status_code=200)
    submenu = response.json()
    assert submenu['dishes_count'] == num_dishes_per_submenu
    # Проверяем кол-во блюд во 2 сабменю
    response = client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id_2}')
    assert_properties(response, status_code=200)
    submenu = response.json()
    assert submenu['dishes_count'] == num_dishes_per_submenu

