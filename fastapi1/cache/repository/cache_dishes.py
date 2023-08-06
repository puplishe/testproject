from .common import invalidate_cache


def invalidate_dish_cache(menu_id: str, submenu_id: str, dish_id: str):
    invalidate_cache(f'{menu_id}:{submenu_id}:dishes:{dish_id}')
    invalidate_cache(f'{menu_id}:{submenu_id}:dishes')
    invalidate_cache('menu')
    invalidate_cache(f'menu:{menu_id}')
    invalidate_cache(f'menu:{menu_id}:submenu')
    invalidate_cache(f'menu:{menu_id}:submenu:{submenu_id}')
