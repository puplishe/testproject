import pytest
from httpx import AsyncClient

from fastapi1.main import app

menu_id = ''
submenu_id = ''
# Функция, чтобы постоянно проверять, 200 ответ, что возвращается id, title, description, либо  [], если пустое сабменю


def assert_properties(response, status_code=200):
    assert response.status_code == status_code
    response_json = response.json()
    if not response_json:
        return
    assert 'id' in response_json
    assert 'title' in response_json
    assert 'description' in response_json


def assert_menu_properties(response_json):
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
        'title': 'Menu 2',
        'description': 'Description for menu 2'
    }
    async with AsyncClient(app=app, base_url='http://test_submenu') as client:
        response = await client.post('/api/v1/menus', json=data)
    assert response.status_code == 201
    assert_menu_properties(response.json())
    created_menu = response.json()
    assert created_menu['title'] == 'Menu 2'
    assert created_menu['description'] == 'Description for menu 2'
    menu_id = created_menu['id']


@pytest.mark.anyio
async def test_create_submenu():
    global submenu_id
    submenu_data = {
        'title': 'Test Submenu',
        'description': 'Test Submenu Description'
    }
    async with AsyncClient(app=app, base_url='http://test_submenu') as client:
        response = await client.post(
            f'/api/v1/menus/{menu_id}/submenus', json=submenu_data)
    assert_properties(response, status_code=201)
    created_submenu = response.json()
    assert 'id' in created_submenu
    assert created_submenu['title'] == submenu_data['title']
    assert created_submenu['description'] == submenu_data['description']
    submenu_id = created_submenu['id']


@pytest.mark.anyio
async def test_read_submenu():
    async with AsyncClient(app=app, base_url='http://test_submenu') as client:
        response = await client.get(f'/api/v1/menus/{menu_id}/submenus')
    submenus = response.json()
    assert isinstance(submenus, list)
    # Проверяем, что созданное сабменю есть в списке всех сабменю
    submenu = next(
        (submenu for submenu in submenus if submenu['id'] == submenu_id), None)
    assert submenu is not None


@pytest.mark.anyio
async def test_update_submenu():
    updated_data = {
        'title': 'Updated Submenu',
        'description': 'Updated Submenu Description'
    }
    async with AsyncClient(app=app, base_url='http://test_submenu') as client:
        response = await client.patch(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}', json=updated_data)
    assert_properties(response)
    updated_submenu = response.json()
    assert updated_submenu['title'] == updated_data['title']
    assert updated_submenu['description'] == updated_data['description']


@pytest.mark.anyio
async def test_delete_submenu():
    async with AsyncClient(app=app, base_url='http://test_submenu') as client:
        response = await client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert_properties(response)


@pytest.mark.anyio
async def test_submenu_empty():
    async with AsyncClient(app=app, base_url='http://test_submenu') as client:
        response = await client.get(f'/api/v1/menus/{menu_id}/submenus')
    assert_properties(response)
    assert response.json() == []


@pytest.mark.anyio
async def test_delete_menu():
    # Удаляем меню
    async with AsyncClient(app=app, base_url='http://test_submenu') as client:
        response = await client.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert_menu_properties(response.json())
