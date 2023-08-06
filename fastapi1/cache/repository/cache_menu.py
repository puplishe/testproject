from sqlalchemy.orm import Session

from ...api.crud.dishes_crud import read_dishes
from ...api.crud.submenu_crud import read_submenu
from .common import invalidate_cache


def invalidate_menu_cache(db: Session, menu_id: str):
    invalidate_cache(f'menu:{menu_id}')
    invalidate_cache('menu')

    submenus = read_submenu(db, menu_id)
    for submenu in submenus:
        invalidate_cache(f'{menu_id}:submenu:{submenu.id}')
        invalidate_cache(f'{menu_id}:submenu')

        dishes = read_dishes(db, menu_id, submenu.id)
        for dish in dishes:
            invalidate_cache(f'{menu_id}:{submenu.id}:dishes:{dish.id}')
            invalidate_cache(f'{menu_id}:{submenu.id}:dishes')
