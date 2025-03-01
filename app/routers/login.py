from fastapi import APIRouter,Request
from fastapi.templating import Jinja2Templates

router=APIRouter(prefix="/login",tags=['login'])
templates=Jinja2Templates(directory="app/templates")

@router.get("/")
async def get_login_page(request:Request):
    return templates.TemplateResponse("login.html",{"request":request})