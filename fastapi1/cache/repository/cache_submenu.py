from sqlalchemy.orm import Session

from ...api.crud.dishes_crud import read_dishes
from .common import invalidate_cache


def invalidate_submenu_cache(db: Session, menu_id: str, submenu_id: str):
    invalidate_cache(f'{menu_id}:submenu:{submenu_id}')
    invalidate_cache(f'{menu_id}:submenu')
    invalidate_cache('menu')
    invalidate_cache(f'menu:{menu_id}')

    dishes = read_dishes(db, menu_id, submenu_id)
    for dish in dishes:
        invalidate_cache(f'{menu_id}:{submenu_id}:dishes:{dish.id}')
        invalidate_cache(f'{menu_id}:{submenu_id}:dishes')
