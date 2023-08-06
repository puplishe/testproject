from typing import Any

from sqlalchemy.orm import Session

from ...cache.cache import cache, cached_with_redis
from ...cache.repository.cache_submenu import invalidate_submenu_cache
from ...models import models
from ...models.schemas.schema_submenu import SubmenuCreate, SubmenuUpdate
from ..crud.submenu_crud import create_submenu as db_create_submenu
from ..crud.submenu_crud import delete_submenu as db_delete_submenu
from ..crud.submenu_crud import get_submenu as db_get_submenu
from ..crud.submenu_crud import patch_submenu as db_patch_submenu
from ..crud.submenu_crud import read_submenu as db_read_submenu


class SubmenuService:
    def __init__(self, db: Session):
        self.db = db

    def read_submenu(self, menu_id: str) -> list[models.Submenu]:
        @cached_with_redis(cache, key_func=lambda: f'{menu_id}:submenu')
        def _read_submenu():
            submenus = db_read_submenu(db=self.db, menu_id=menu_id)
            return submenus
        return _read_submenu()

    def create_submenu(self, menu_id: str, submenu: SubmenuCreate) -> models.Submenu:
        new_submenu = db_create_submenu(
            db=self.db, menu_id=menu_id, submenu=submenu)
        invalidate_submenu_cache(menu_id=menu_id, submenu_id=str(
            new_submenu.id), db=self.db)
        return new_submenu

    def delete_submenu(self, menu_id: str, submenu_id: str) -> dict[str, str]:
        invalidate_submenu_cache(
            menu_id=menu_id, submenu_id=submenu_id, db=self.db)
        return db_delete_submenu(self.db, menu_id, submenu_id)

    def get_submenu(self, menu_id: str, submenu_id: str) -> dict[str, Any]:
        @cached_with_redis(cache, key_func=lambda: f'{menu_id}:submenu:{submenu_id}')
        def _get_submenu():
            submenu_data = db_get_submenu(
                menu_id=menu_id, submenu_id=submenu_id, db=self.db)
            return submenu_data
        return _get_submenu()

    def patch_submenu(self, menu_id: str, submenu_id: str, submenu_data: SubmenuUpdate) -> models.Submenu:
        updated_submenu = db_patch_submenu(db=self.db, menu_id=menu_id,
                                           submenu_id=submenu_id, submenu_data=submenu_data)
        invalidate_submenu_cache(
            menu_id=menu_id, submenu_id=submenu_id, db=self.db)
        return updated_submenu
