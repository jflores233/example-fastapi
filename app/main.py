from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings


#tell sqlalchemy to auto create the tables for us
#not really needed with alembic installed, setup/configured
#models.Base.metadata.create_all(bind=engine)

#########################
# https://www.youtube.com/watch?v=0sOvCWFmrtA
##########################

app = FastAPI()
#origins = ["https://www.google.com", "https://www.youtube.com"] #how you can access the app from a google.com webpage
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, #use the list above of which domains can access this app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/") #first path operation that matches, runs the code
def root():
    return {"message": "Hello World"}