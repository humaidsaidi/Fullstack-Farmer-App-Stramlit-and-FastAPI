from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

# retrieve user credential
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
# def login(user_credential: schemas.UserLogin, db: Session = Depends(database.get_db)):
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    # user = db.query(models.User).filter(models.User.email == user_credential.email).first()
    
    # when retreaving user credential from OAuth2PasswordRequestForm the email is stored in field called username
    # and it only return 2 thing {"username": "abcd", "password": "abcd"}
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credential")
    
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credential")
    
    
    # Create a token
    # return token
    access_token = oauth2.create_access_token(data= {"user_id": user.id}) # the data is the payload, you can add what you want
    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id}