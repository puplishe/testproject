
from database import Base, engine, SessionLocal, get_db
from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session
from schemas import MenusCreate, SubmenuCreate, SubmenuUpdate, DishCreate, DishUpdate
import models
from fastapi.responses import JSONResponse
import uvicorn

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.post('/api/v1/menus',status_code=201)
def create_menu(menu:MenusCreate, db:Session=Depends(get_db)):
    new_menu = models.Menu(**menu.model_dump())
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu

@app.get('/api/v1/menus')
def read_menu(db:Session=Depends(get_db)):
    get_menus = db.query(models.Menu).all()
    return get_menus

@app.get('/api/v1/menus/{menu_id}')
def get_menu(menu_id:str, db:Session=Depends(get_db)):
    menu = db.query(models.Menu).get(menu_id)
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
    submenus = db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).all()
    if menu:
        submenus_count = len(submenus)
        dishes_count = sum(len(submenu.dishes) for submenu in submenus)
        response_data = {
            'id': menu.id,
            'title': menu.title,
            'description': menu.description,
            'submenus_count': submenus_count,
            'dishes_count': dishes_count,
            'submenus': submenus  
        }

        return response_data
    return menu


@app.patch('/api/v1/menus/{menu_id}')
def patch_menu(menu_id:str,menu:MenusCreate, db: Session=Depends(get_db)):
    get_menu = db.query(models.Menu).filter(models.Menu.id==menu_id)
    get_menu.first()
    get_menu.update(menu.model_dump(), synchronize_session=False)
    db.commit()
    return get_menu.first()


@app.delete('/api/v1/menus/{menu_id}')
def delete_menu(menu_id:str, db:Session=Depends(get_db)):
    get_menu = db.query(models.Menu).filter(models.Menu.id==menu_id)
    get_menu.delete()
    db.commit()
    return get_menu



@app.get('/api/v1/menus/{menu_id}/submenus')
def read_submenu(menu_id: str, db: Session=Depends(get_db)):
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")
    submenus = db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).all()
    return submenus

@app.post('/api/v1/menus/{menu_id}/submenus', status_code=201)
def create_submenu(menu_id: str, submenu: SubmenuCreate, db: Session=Depends(get_db)):
    new_submenu = models.Submenu(**submenu.model_dump(), menu_id=menu_id)
    db.add(new_submenu)
    db.commit()
    db.refresh(new_submenu)
    return new_submenu


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def delete_submenu(submenu_id: str, db:Session=Depends(get_db)):
    get_submenu = db.query(models.Submenu).filter(models.Submenu.id==submenu_id)
    get_submenu.delete()
    db.commit()
    return get_submenu

@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def get_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")
    submenu = db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).first()
    submenu = db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()
    dishes = db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).all()
    dishes_count = len(dishes)
    if not submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    response_data = {
        'id': submenu.id,
        'title': submenu.title,
        'description': submenu.description,
        'menu_id': submenu.menu_id,
        'dishes_count': dishes_count,  
        'dishes': dishes  
    }

    return response_data

@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def patch_submenu(menu_id: str, submenu_id: str, submenu_data: SubmenuUpdate, db: Session=Depends(get_db)):
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")
    update_submenu = db.query(models.Submenu).filter(
        models.Submenu.id == submenu_id,
        models.Submenu.menu_id == menu_id
    ).update(submenu_data.model_dump(exclude_unset=True))
    if update_submenu == 0:
        raise HTTPException(status_code=404, detail="submenu not found")
    db.commit()
    updated_submenu = db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()
    return updated_submenu


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
def read_dishes(menu_id: str, submenu_id: str, db: Session=Depends(get_db)):
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")
    dish = db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).all()
    return dish

@app.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',status_code=201)
def post_dish(menu_id: str, submenu_id: str,dish_data: DishCreate, db: Session=Depends(get_db)):
    new_dish = models.Dish(**dish_data.model_dump(), submenu_id=submenu_id)
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    return new_dish

@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def get_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session=Depends(get_db)):
    dish = db.query(models.Dish).filter(
        models.Dish.id == dish_id,
        models.Dish.submenu_id == submenu_id
    ).first()
    if not dish:
        raise HTTPException(status_code=404, detail="dish not found")
    return dish

@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def patch_dish(menu_id: str, submenu_id: str, dish_id: str, dish_data: DishUpdate, db: Session=Depends(get_db)):
    update_dish = db.query(models.Dish).filter(
        models.Dish.id == dish_id,
        models.Dish.submenu_id == submenu_id
    ).update(dish_data.model_dump(exclude_unset=True))
    if update_dish == 0:
        raise HTTPException(status_code=404, detail="submenu not found")
    db.commit()
    updated_dish = db.query(models.Dish).filter(models.Dish.id == dish_id).first()
    return updated_dish

@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def delete_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session=Depends(get_db)):
    dish = db.query(models.Dish).filter(models.Dish.id==dish_id,
                                        models.Dish.submenu_id==submenu_id
    )
    dish.delete()
    db.commit()
    return dish


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)