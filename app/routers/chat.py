from fastapi import APIRouter,Request,status,HTTPException,Depends
from fastapi.responses import RedirectResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from ..OAuth2 import verify_access_token,get_current_user
from ..database import db_dependency
from ..models import User
from ..config import settings
import google.generativeai as genai
import html
import markdown2


router=APIRouter(
    tags=['chat']
)

templates=Jinja2Templates(directory="app/templates")

def redirect_to_login():
    redirect_response=RedirectResponse(url="/",status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie("access_token")
    return redirect_response


chat_sessions={}

genai.configure(api_key=settings.GEMINI_API_KEY)



def get_chat_session(session_id):
    if session_id not in chat_sessions:
        try:
            model=genai.GenerativeModel("gemini-1.5-flash")
            chat_sessions[session_id]=model.start_chat(
                history=[
                    {"role":"model","parts":"HI! How can I assist you today?"}
                ]
            )
        except Exception as e:
            print(f"Failed to initialize chat session: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Failed to initiate chat session.")
    return chat_sessions[session_id]


@router.get("/chat")
async def dashboard(request:Request,db:db_dependency):
    try:
        token=request.cookies.get("access_token")
        if not token:
            return redirect_to_login()
        
        user=verify_access_token(token=token,credential_exception=HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found"))
        user_obj=db.query(User).filter(user.id==User.id).first()
        if not user_obj:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not authorized")
        return templates.TemplateResponse("chat.html",{"request":request})
    except Exception as e:
        print(f"Error verifying token: {e}")
        return redirect_to_login()
    


@router.post("/chat")
async def chat_endpoint(request:Request,user=Depends(get_current_user)):
    try:
        data=await request.json()
        user_message= data.get("chat") 
        if not user_message:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Chat message is required")
        session_id=str(user.id)
        print("Session Id:",session_id)
        chat_session=get_chat_session(session_id)

        response=chat_session.send_message(user_message,stream=True)

        response_text="".join(chunk.text for chunk in response)
        generated_text = response.text  
        generated_text = html.unescape(generated_text)
        generated_text = generated_text.replace("**", "<b>").replace("*", "<i>").replace("</i><i>", "").replace("</b><b>", "").replace("<i></i>", "").replace("<b></b>", "")
        response_text=markdown2.markdown(generated_text)


        chat_session.history.append({"role":"user","parts":user_message})
        chat_session.history.append({"role":"model","parts":response_text})

        return JSONResponse({"bot":response_text})
    except Exception as e: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"An error occured : {str(e)}")