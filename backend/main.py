from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, utils
from .database import engine, get_db
from . routers import user, post, auth ,diagnose


models.Base.metadata.create_all(bind=engine) # it will make the table in database

app = FastAPI()

app.include_router(post.router) # all functionalities about post are in routers directory
app.include_router(user.router) # all functionalities about user are in routers directory
app.include_router(auth.router)
app.include_router(diagnose.router)

@app.get('/') # this derocator in order the function below do not act like ordinary function, btw this is get http method
def root():
    return {'massage':'from the root page'}



