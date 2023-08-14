import pytest
from httpx import AsyncClient

from fastapi1.main import app

menu_id = ''
submenu_id = ''
dish_id = ''


def assert_menu_properties(response_json):
    if not response_json:
        return
    assert 'id' in response_json
    assert 'title' in response_json
    assert 'description' in response_json


def assert_properties(response, status_code=200):
    assert response.status_code == status_code
    response_json = response.json()
    if not response_json:
        return
    assert 'id' in response_json
    assert 'title' in response_json
    assert 'description' in response_json


def assert_dish_properties(response_json):
    if not response_json:
        return
    assert 'id' in response_json
    assert 'title' in response_json
    assert 'description' in response_json
    assert 'price' in response_json
    assert 'submenu_id' in response_json


@pytest.mark.anyio
async def test_create_menus():
    # Тестируем правильно ли создается меню
    global menu_id
    data = {
        'title': 'Menu 3',
        'description': 'Description for menu 3'
    }
    async with AsyncClient(app=app, base_url='http://test_dish') as client:
        response = await client.post('/api/v1/menus', json=data)
    assert response.status_code == 201
    assert_menu_properties(response.json())
    created_menu = response.json()
    assert created_menu['title'] == 'Menu 3'
    assert created_menu['description'] == 'Description for menu 3'
    menu_id = created_menu['id']


@pytest.mark.anyio
async def test_create_submenu():
    global submenu_id
    submenu_data = {
        'title': 'Test Submenu',
        'description': 'Test Submenu Description'
    }
    async with AsyncClient(app=app, base_url='http://test_dish') as client:
        response = await client.post(
            f'/api/v1/menus/{menu_id}/submenus', json=submenu_data)
    assert_properties(response, status_code=201)
    created_submenu = response.json()
    assert 'id' in created_submenu
    assert created_submenu['title'] == submenu_data['title']
    assert created_submenu['description'] == submenu_data['description']
    submenu_id = created_submenu['id']


@pytest.mark.anyio
async def test_create_dish():
    global dish_id
    data = {
        'title': 'Test Dish',
        'description': 'Test Dish Description',
        'price': '9.99',
    }
    async with AsyncClient(app=app, base_url='http://test_dish') as client:
        response = await client.post(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=data)
    assert response.status_code == 201
    assert_dish_properties(response.json())
    created_dish = response.json()
    assert created_dish['title'] == 'Test Dish'
    assert created_dish['description'] == 'Test Dish Description'
    assert created_dish['price'] == '9.99'
    assert created_dish['submenu_id'] == submenu_id
    dish_id = created_dish['id']


@pytest.mark.anyio
async def test_read_dish():
    async with AsyncClient(app=app, base_url='http://test_dish') as client:
        response = await client.get(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert response.status_code == 200
    dishes = response.json()
    assert isinstance(dishes, list)
    if dishes:
        assert_dish_properties(dishes[0])


@pytest.mark.anyio
async def test_get_dish():

    async with AsyncClient(app=app, base_url='http://test_dish') as client:
        response = await client.get(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')

    assert response.status_code == 200
    assert_dish_properties(response.json())


@pytest.mark.anyio
async def test_update_dish():

    update_data = {
        'title': 'Updated Dish',
        'description': 'Updated dish description',
        'price': '19.99',
    }
    async with AsyncClient(app=app, base_url='http://test_dish') as client:
        response = await client.patch(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', json=update_data)
    assert response.status_code == 200
    assert_dish_properties(response.json())
    updated_dish = response.json()
    assert updated_dish['title'] == 'Updated Dish'
    assert updated_dish['description'] == 'Updated dish description'
    assert updated_dish['price'] == '19.99'
    assert updated_dish['submenu_id'] == submenu_id


@pytest.mark.anyio
async def test_delete_dish():

    async with AsyncClient(app=app, base_url='http://test_dish') as client:
        response = await client.delete(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code == 200


@pytest.mark.anyio
async def test_delete_submenu():
    async with AsyncClient(app=app, base_url='http://test_dish') as client:
        response = await client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert_properties(response)


@pytest.mark.anyio
async def test_delete_menu():
    # Удаляем меню
    async with AsyncClient(app=app, base_url='http://test_dish') as client:
        response = await client.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert_menu_properties(response.json())
