from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..crud import submenu_crud
from ...models.schemas.schema_submenu import SubmenuCreate, SubmenuUpdate
from ...db.database import get_db

router = APIRouter()

@router.get('/menus/{menu_id}/submenus')
def read_submenu(menu_id: str, db: Session = Depends(get_db)):
    return submenu_crud.read_submenu(menu_id, db)

@router.post('/menus/{menu_id}/submenus', status_code=201)
def create_submenu(menu_id: str, submenu: SubmenuCreate, db: Session = Depends(get_db)):
    return submenu_crud.create_submenu(menu_id, submenu, db)

@router.delete('/menus/{menu_id}/submenus/{submenu_id}')
def delete_submenu(submenu_id: str, db: Session = Depends(get_db)):
    return submenu_crud.delete_submenu(submenu_id, db)

@router.get('/menus/{menu_id}/submenus/{submenu_id}')
def get_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    return submenu_crud.get_submenu(menu_id, submenu_id, db)

@router.patch('/menus/{menu_id}/submenus/{submenu_id}')
def patch_submenu(menu_id: str, submenu_id: str, submenu_data: SubmenuUpdate, db: Session = Depends(get_db)):
    return submenu_crud.patch_submenu(menu_id, submenu_id, submenu_data, db)
