from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...db.database import get_db
from ...models.schemas.schema_menu import MenusCreate
from ..crud import menu_crud

router = APIRouter()

@router.post('/menus', status_code=201)
def create_menu(menu: MenusCreate, db: Session = Depends(get_db)):
    return menu_crud.create_menu(menu, db)

@router.get('/menus')
def read_menu(db: Session = Depends(get_db)):
    return menu_crud.read_menu(db)

@router.get('/menus/{menu_id}')
def get_menu(menu_id: str, db: Session = Depends(get_db)):
    return menu_crud.get_menu(menu_id, db)

@router.patch('/menus/{menu_id}')
def patch_menu(menu_id: str, menu: MenusCreate, db: Session = Depends(get_db)):
    return menu_crud.patch_menu(menu_id, menu, db)

@router.delete('/menus/{menu_id}')
def delete_menu(menu_id: str, db: Session = Depends(get_db)):
    return menu_crud.delete_menu(menu_id, db)
