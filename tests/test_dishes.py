import pytest
from fastapi.testclient import TestClient

from fastapi1.main import app

client = TestClient(app)


# Функция для проверки правильности даты, которая приходит в ответе
def assert_properties(response, status_code=200):
    assert response.status_code == status_code
    response_json = response.json()
    if not response_json:
        return
    assert 'id' in response_json
    assert 'title' in response_json
    assert 'description' in response_json


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
    response = client.post(
        f'/api/v1/menus/{menu_id}/submenus', json=submenu_data)
    assert_properties(response, status_code=201)
    created_submenu = response.json()
    yield created_submenu['id']
    client.delete(f'/api/v1/menus/{menu_id}/submenus/{created_submenu["id"]}')


def assert_dish_properties(response_json):
    if not response_json:
        return
    assert 'id' in response_json
    assert 'title' in response_json
    assert 'description' in response_json
    assert 'price' in response_json
    assert 'submenu_id' in response_json


def test_create_dish(menu_id, submenu_id):
    # Создаем блюдо
    data = {
        'title': 'Test Dish',
        'description': 'Test Dish Description',
        'price': '9.99',
    }
    response = client.post(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=data)
    assert response.status_code == 201
    assert_dish_properties(response.json())
    created_dish = response.json()
    assert created_dish['title'] == 'Test Dish'
    assert created_dish['description'] == 'Test Dish Description'
    assert created_dish['price'] == '9.99'
    assert created_dish['submenu_id'] == submenu_id


def test_read_dish(menu_id, submenu_id):
    response = client.get(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
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
    response = client.post(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=data)
    assert response.status_code == 201
    created_dish = response.json()
    dish_id = created_dish['id']

    response = client.get(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code == 200
    assert_dish_properties(response.json())


def test_update_dish(menu_id, submenu_id):
    # Тестируем update блюда
    data = {
        'title': 'Test Dish',
        'description': 'Test Dish Description',
        'price': '9.99',
    }
    response = client.post(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=data)
    assert response.status_code == 201
    created_dish = response.json()
    dish_id = created_dish['id']

    update_data = {
        'title': 'Updated Dish',
        'description': 'Updated dish description',
        'price': '19.99',
    }
    response = client.patch(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', json=update_data)
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
    response = client.post(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=data)
    assert response.status_code == 201
    created_dish = response.json()
    dish_id = created_dish['id']

    response = client.delete(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code == 200
    assert_dish_properties(response.json())
