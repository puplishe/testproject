from fastapi import APIRouter, Depends, HTTPException

from ...celery.tasks import ExcelParser
from ..crud.dishes_crud import DishesCrud
from ..crud.menu_crud import MenuCrud
from ..crud.submenu_crud import SubmenuCrud

parser_router = APIRouter(prefix='/parser', tags=['Parser'])


@parser_router.post('/parse-excel')
async def parse_excel(
    menu_service: MenuCrud = Depends(),
    submenu_service: SubmenuCrud = Depends(),
    dish_service: DishesCrud = Depends()
):
    try:
        excel_parser = ExcelParser(menu_service, submenu_service, dish_service)
        await excel_parser.parser()
        return {'message': 'Excel data parsed and loaded successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
