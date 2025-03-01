from fastapi import APIRouter,Request
from fastapi.templating import Jinja2Templates

router=APIRouter(prefix="/register",tags=['register'])
templates=Jinja2Templates(directory="app/templates")

@router.get("/")
async def get_login_page(request:Request):
    return templates.TemplateResponse("register.html",{"request":request})