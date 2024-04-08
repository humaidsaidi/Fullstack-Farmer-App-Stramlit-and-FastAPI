from .. import schemas, models, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users'] # Giving title and grouping in the documentation
)

# every endpoint have same name (/users) so to reduce the complexity when the endpoint get increase we do
# prefix each function like above

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)): # see schemas.py to see the key
    # get the email from db to ensure the email does not exist
    user_query = db.query(models.User).filter(models.User.email == user.email).first()
    
    if not user_query:
        if user.password != "":
            # hash the password
            hashed_password = utils.hash(user.password)
            user.password = hashed_password

            new_user = models.User(**user.dict()) # this will unpack the post dict to be formatted like above
            db.add(new_user)
            db.commit()
            db.refresh(new_user) 
            return new_user
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No password entered!")
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered!")
    

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id}, does not exist!")
    
    return user
