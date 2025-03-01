from fastapi import APIRouter,Depends,Request,HTTPException,status
from fastapi.templating import Jinja2Templates
from ..schemas import EventCreateModel,DeleteEvent
from ..database import db_dependency
from ..models import Event,User
from ..OAuth2 import get_current_user

router=APIRouter(prefix="/event",tags=['event'])
templates=Jinja2Templates(directory="app/templates")


@router.get("/")
async def get_eventPage(request:Request):
    return templates.TemplateResponse("event.html",{"request":request})


@router.get("/getallevents")
async def get_all_events(db:db_dependency,user=Depends(get_current_user)):
    events=db.query(Event).filter(Event.created_by==user.username).all()
    return events

@router.post("/createevent")
async def updatedata(eventData:EventCreateModel,db:db_dependency,user=Depends(get_current_user)):
    try:
        event_model=Event(**eventData.model_dump(),created_by=user.username)
        db.add(event_model)
        db.commit()
        db.refresh(event_model)
        return {"success":"Event addition Successfull"}
    except Exception as e:
        error=f"Event creation failed: {str(e)}"
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=error)
    
@router.delete("/deleteEvent")
async def dele(deleteEventdata:DeleteEvent,db:db_dependency,user=Depends(get_current_user)):
    try:
        data=db.query(Event).filter(Event.title==deleteEventdata.title).filter(Event.description==deleteEventdata.description).filter(User.id==user.id).first()
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Event not found")
        db.delete(data)
        db.commit()
        return {"success":"Event Deleted Successfully"}
    except Exception as e:
        error=f"Deleting Event failed: {str(e)}"
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=error)


