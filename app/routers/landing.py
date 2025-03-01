from fastapi import APIRouter,Request
from fastapi.templating import Jinja2Templates

router=APIRouter(
    tags=['landing_page']
)

templates=Jinja2Templates(directory="app/templates")

@router.get("/landing-page")
async def landing_page(request:Request):
    return templates.TemplateResponse("main.html",{"request":request})