from typing import Any

from sqlalchemy.orm import Session

from ...cache.cache import cache, cached_with_redis
from ...cache.repository.cache_menu import invalidate_menu_cache
from ...models import models
from ...models.schemas.schema_menu import MenusCreate
from ..crud.menu_crud import create_menu as db_create_menu
from ..crud.menu_crud import delete_menu as db_delete_menu
from ..crud.menu_crud import get_menu as db_get_menu
from ..crud.menu_crud import patch_menu as db_patch_menu
from ..crud.menu_crud import read_menu as db_read_menu


class MenuService:
    def __init__(self, db: Session):
        self.db = db

    def create_menu(self, menu: MenusCreate) -> models.Menu:
        new_menu = db_create_menu(self.db, menu)
        invalidate_menu_cache(menu_id=str(new_menu.id), db=self.db)
        return new_menu

    def read_menu(self) -> list[models.Menu]:
        @cached_with_redis(cache, key_func=lambda: 'menu')
        def _read_menu():
            return db_read_menu(self.db)

        return _read_menu()

    def get_menu(self, menu_id: str) -> dict[str, Any]:
        @cached_with_redis(cache, key_func=lambda: f'menu:{menu_id}')
        def _get_menu():
            menu = db_get_menu(self.db, menu_id)
            return menu
        return _get_menu()

    def patch_menu(self, menu_id: str, menu: MenusCreate) -> models.Menu:
        updated_menu = db_patch_menu(self.db, menu_id, menu)
        invalidate_menu_cache(menu_id=menu_id, db=self.db)
        return updated_menu

    def delete_menu(self, menu_id: str) -> dict[str, str]:
        invalidate_menu_cache(menu_id=menu_id, db=self.db)
        return db_delete_menu(self.db, menu_id)
