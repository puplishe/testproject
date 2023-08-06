from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...db.database import get_db
from ...models.schemas.schema_submenu import SubmenuCreate, SubmenuUpdate
from ..services.service_submenu import SubmenuService

router = APIRouter()


@router.get('/menus/{menu_id}/submenus')
def read_submenu(menu_id: str, db: Session = Depends(get_db)):
    submenu_service = SubmenuService(db)
    return submenu_service.read_submenu(menu_id)


@router.post('/menus/{menu_id}/submenus', status_code=201)
def create_submenu(menu_id: str, submenu: SubmenuCreate, db: Session = Depends(get_db)):
    submenu_service = SubmenuService(db)
    return submenu_service.create_submenu(menu_id, submenu)


@router.delete('/menus/{menu_id}/submenus/{submenu_id}')
def delete_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    submenu_service = SubmenuService(db)
    return submenu_service.delete_submenu(menu_id, submenu_id)


@router.get('/menus/{menu_id}/submenus/{submenu_id}')
def get_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    submenu_service = SubmenuService(db)
    return submenu_service.get_submenu(menu_id, submenu_id)


@router.patch('/menus/{menu_id}/submenus/{submenu_id}')
def patch_submenu(menu_id: str, submenu_id: str, submenu_data: SubmenuUpdate, db: Session = Depends(get_db)):
    submenu_service = SubmenuService(db)
    return submenu_service.patch_submenu(menu_id, submenu_id, submenu_data)
