from typing import Any

import pytest
from httpx import AsyncClient

from fastapi1.main import app

from .test_dishes import assert_dish_properties, assert_menu_properties

menu_id = ''
submenu_id = ''
dish_id: list[Any] = []


def assert_properties(response):
    response_json = response.json()
    if not response_json:
        return
    assert 'id' in response_json
    assert 'title' in response_json
    assert 'description' in response_json


def assert_properties_submenu(response_json):
    response_json
    if not response_json:
        return
    assert 'id' in response_json
    assert 'title' in response_json
    assert 'description' in response_json


@pytest.mark.anyio
async def test_create_menus():
    # Тестируем правильно ли создается меню
    global menu_id
    data = {
        'title': 'Test Menu 1',
        'description': 'Test description for menu 1'
    }
    async with AsyncClient(app=app, base_url='http://test_new') as client:
        response = await client.post('/api/v1/menus', json=data)
    assert response.status_code == 201
    assert_menu_properties(response.json())
    created_menu = response.json()
    assert created_menu['title'] == data['title']
    assert created_menu['description'] == data['description']
    menu_id = created_menu['id']


@pytest.mark.anyio
async def test_create_submenu():
    global submenu_id
    submenu_data = {
        'title': 'Test Submenu',
        'description': 'Test Submenu Description'
    }
    async with AsyncClient(app=app, base_url='http://test_new') as client:
        response = await client.post(
            f'/api/v1/menus/{menu_id}/submenus', json=submenu_data)
    assert_properties(response)
    created_submenu = response.json()
    assert 'id' in created_submenu
    assert created_submenu['title'] == submenu_data['title']
    assert created_submenu['description'] == submenu_data['description']
    submenu_id = created_submenu['id']


@pytest.mark.anyio
async def test_create_dish():
    global dish_id
    data = {
        'title': 'Test Dish 1',
        'description': 'Test Dish Description 1',
        'price': '9.99',
    }
    async with AsyncClient(app=app, base_url='http://test_new') as client:
        response = await client.post(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=data)
    assert response.status_code == 201
    assert_dish_properties(response.json())
    created_dish = response.json()
    assert created_dish['title'] == data['title']
    assert created_dish['description'] == data['description']
    assert created_dish['price'] == data['price']
    assert created_dish['submenu_id'] == submenu_id
    dish_id = created_dish['id']


@pytest.mark.anyio
async def test_create_dish_2():
    global dish_id
    data = {
        'title': 'Test Dish 2',
        'description': 'Test Dish Description 2',
        'price': '9.99',
    }
    async with AsyncClient(app=app, base_url='http://test_new') as client:
        response = await client.post(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=data)
    assert response.status_code == 201
    assert_dish_properties(response.json())
    created_dish = response.json()
    assert created_dish['title'] == data['title']
    assert created_dish['description'] == data['description']
    assert created_dish['price'] == data['price']
    assert created_dish['submenu_id'] == submenu_id
    dish_id = created_dish['id']


@pytest.mark.anyio
async def test_for_new_endpoint():
    """Проверка нового энпоинта"""
    async with AsyncClient(app=app, base_url='http://test_new') as client:
        response = await client.get('/api/v1/menus_info/')
    assert response.status_code == 200
    response = response.json()
    for menu in response:
        assert_menu_properties(menu)
        for submenu in menu['submenus']:
            assert_properties_submenu(submenu)
            for dish in submenu['dishes']:
                assert_dish_properties(dish)


@pytest.mark.anyio
async def test_delete_submenu():
    async with AsyncClient(app=app, base_url='http://test_new') as client:
        response = await client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert_properties(response)


@pytest.mark.anyio
async def test_submenu_empty():
    async with AsyncClient(app=app, base_url='http://test_new') as client:
        response = await client.get(f'/api/v1/menus/{menu_id}/submenus')
    assert_properties(response)
    assert response.json() == []


@pytest.mark.anyio
async def test_delete_menu():
    # Удаляем меню
    async with AsyncClient(app=app, base_url='http://test_new') as client:
        response = await client.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200


@pytest.mark.anyio
async def test_menu_empty():
    # Проверяем, что меню пустые
    async with AsyncClient(app=app, base_url='http://test_new') as client:
        response = await client.get('/api/v1/menus')
    assert response.status_code == 200
    assert response.json() == []
