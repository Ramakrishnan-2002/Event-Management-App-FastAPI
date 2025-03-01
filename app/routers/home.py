from fastapi import APIRouter,status,HTTPException,Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from ..database import db_dependency
from ..OAuth2 import verify_access_token
from ..models import User


router=APIRouter(
    prefix="/home",
    tags=['Home_Page']
)

templates=Jinja2Templates(directory="app/templates")


def redirect_to_login():
    redirect_response=RedirectResponse(url="/",status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response


@router.get("/dashboard")
async def dashboard(request:Request,db:db_dependency):
    try:
        token=request.cookies.get("access_token")
        if not token:
            return redirect_to_login()
        user=verify_access_token(token=token,credential_exception=HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found"))
        user_obj=db.query(User).filter(user.id==User.id).first()
        return templates.TemplateResponse("home.html",{"request":request,"username":user_obj.username})
    except Exception as e:
        print(f"Error verifying token: {e}")
        return redirect_to_login()
     
@router.get("/logout")
async def logout():
    return redirect_to_login()
    
    