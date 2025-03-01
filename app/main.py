from fastapi import FastAPI,status,Response
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import landing,login,register,users,auth,home,profile,event,chat,forgot

app=FastAPI()


origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]

)


models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def main_page(response:Response):
    response.delete_cookie(key="access_token")
    return RedirectResponse(url="/landing-page",status_code=status.HTTP_302_FOUND)


app.include_router(landing.router)
app.include_router(login.router)
app.include_router(register.router)
app.include_router(users.router) 
app.include_router(auth.router)
app.include_router(home.router)
app.include_router(profile.router)
app.include_router(event.router)
app.include_router(chat.router)
app.include_router(forgot.router)