from fastapi import APIRouter,Request,Depends,status,HTTPException
from ..OAuth2 import get_current_user
from fastapi.templating import Jinja2Templates
from ..database import db_dependency
from ..models import User
from ..schemas import UserOut

router=APIRouter(prefix="/profile",tags=['profile'])
templates=Jinja2Templates(directory="app/templates")



@router.get("/")
async def get_login_page(request:Request):
    return templates.TemplateResponse("profile.html",{"request":request}) 

@router.get("/userdata",response_model=UserOut)
async def get_user_data(db:db_dependency,user=Depends(get_current_user)):
    try:
        user_data=db.query(User).filter(User.id==user.id).first()
        return user_data
    except Exception as e:
        error=f"User retriving process failed: {str(e)}"
        print(error) 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=error)