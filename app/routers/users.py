from fastapi import APIRouter,status,Depends,HTTPException,status
from ..database import db_dependency
from ..schemas import UserCreateModel
from ..models import User
from ..OAuth2 import get_current_user
from ..utils import hash


router=APIRouter(
    prefix="/users",
    tags=['users']
)


@router.post("/createuser",status_code=status.HTTP_201_CREATED)
async def create_user(userdata:UserCreateModel,db:db_dependency):
    try:
        userdata.password=hash(userdata.password)
        user_model=User(**userdata.model_dump())
        db.add(user_model)
        db.commit()
        db.refresh(user_model)
        return {"success":"Signup Successfull"}
    except Exception as e:
        error=f"Signup failed: {str(e)}"
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=error)

@router.get("/allusers")
async def getallusers(db:db_dependency):
    userdata=db.query(User).all()
    return userdata
    
@router.delete("/deleteuser")
async def deleteuser(db:db_dependency,user=Depends(get_current_user)):
    try:
        user=db.query(User).filter(User.id==user.id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
        user.delete()
        db.commit()
    except Exception as e:
        error=f"Error in deleting user : {str(e)}"
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=error)

