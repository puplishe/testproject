import pytest
from fastapi.testclient import TestClient

from fastapi1.main import app

client = TestClient(app)


def assert_menu_properties(response_json):
    # проверяем пришли id и тд в ответе
    if not response_json:
        return
    assert 'id' in response_json
    assert 'title' in response_json
    assert 'description' in response_json


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


def test_get_menus():
    # Получение всех меню
    response = client.get('/api/v1/menus/')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_menus(menu_id):
    # Тестируем правильно ли создается меню
    response = client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert_menu_properties(response.json())
    created_menu = response.json()
    assert created_menu['title'] == 'Menu 2'
    assert created_menu['description'] == 'Description for menu 1'


def test_update_menu(menu_id):
    # Тест на update
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


def test_read_menus(menu_id):
    # Тестируем read определенного меню
    response = client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert_menu_properties(response.json())


def test_delete_menu(menu_id):
    # Удаляем меню
    response = client.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert_menu_properties(response.json())


def test_menu_empty():
    # Проверяем, что меню пустые
    response = client.get('/api/v1/menus/')
    assert response.status_code == 200
    assert response.json() == []


def test_empty_menu_id(menu_id):
    # Проверяем, что респонс пуст
    client.delete(f'/api/v1/menus/{menu_id}')
    response = client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}
