import pytest
from httpx import AsyncClient

from fastapi1.main import app

menu_id = ''


def assert_menu_properties(response_json):
    if not response_json:
        return
    assert 'id' in response_json
    assert 'title' in response_json
    assert 'description' in response_json


@pytest.mark.anyio
async def test_get_menus():
    # Получение всех меню
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get('/api/v1/menus')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.anyio
async def test_create_menus():
    # Тестируем правильно ли создается меню
    global menu_id
    data = {
        'title': 'Menu 1',
        'description': 'Description for menu 1'
    }
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post('/api/v1/menus', json=data)
    assert response.status_code == 201
    assert_menu_properties(response.json())
    created_menu = response.json()
    assert created_menu['title'] == 'Menu 1'
    assert created_menu['description'] == 'Description for menu 1'
    menu_id = created_menu['id']


@pytest.mark.anyio
async def test_update_menu():
    # Тест на update
    data = {
        'title': 'Updated Menu 1',
        'description': 'Updated Description 1'
    }
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.patch(f'/api/v1/menus/{menu_id}', json=data)
    assert response.status_code == 200
    assert_menu_properties(response.json())
    updated_menu = response.json()
    assert updated_menu['title'] == data['title']
    assert updated_menu['description'] == data['description']


@pytest.mark.anyio
async def test_read_menus():
    # Тестируем read определенного меню
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert_menu_properties(response.json())
    response = response.json()
    assert response != []


@pytest.mark.anyio
async def test_delete_menu():
    # Удаляем меню
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200


@pytest.mark.anyio
async def test_menu_empty():
    # Проверяем, что меню пустые
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get('/api/v1/menus')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.anyio
async def test_empty_menu_id():
    # Проверяем, что респонс пуст
    async with AsyncClient(app=app, base_url='http://test') as client:
        await client.delete(f'/api/v1/menus/{menu_id}')
        response = await client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}
