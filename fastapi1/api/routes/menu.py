from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...db.database import get_db
from ...models.schemas.schema_menu import MenusCreate
from ..services.service_menu import MenuService

router = APIRouter()


@router.post('/menus', status_code=201)
def create_menu(menu: MenusCreate, db: Session = Depends(get_db)):
    menu_service = MenuService(db)
    return menu_service.create_menu(menu)


@router.get('/menus')
def read_menu(db: Session = Depends(get_db)):
    menu_service = MenuService(db)
    return menu_service.read_menu()


@router.get('/menus/{menu_id}')
def get_menu(menu_id: str, db: Session = Depends(get_db)):
    menu_service = MenuService(db)
    return menu_service.get_menu(menu_id)


@router.patch('/menus/{menu_id}')
def patch_menu(menu_id: str, menu: MenusCreate, db: Session = Depends(get_db)):
    menu_service = MenuService(db)
    return menu_service.patch_menu(menu_id, menu)


@router.delete('/menus/{menu_id}')
def delete_menu(menu_id: str, db: Session = Depends(get_db)):
    menu_service = MenuService(db)
    return menu_service.delete_menu(menu_id)
