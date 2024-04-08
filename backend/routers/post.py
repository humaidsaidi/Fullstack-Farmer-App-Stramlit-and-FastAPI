from .. import schemas, models, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts'] # Giving title and grouping in the documentation
)

# every endpoint have same name (/posts) so to reduce the complexity when the endpoint get increase we do
# prefix each function like above

@router.get('/', response_model=List[schemas.Post]) # the return is list of Post, so we need to convert it to list
def get_posts(db: Session = Depends(get_db), 
              limit: int = 10, skip: int = 0):
    # print(current_user, " -> ", current_user.email)
    posts = db.query(models.Post).limit(limit).offset(skip).all()

    # Here is if you want your get_posts function only get the posts that you made
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate, 
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)
): # as mentioned earlier Post is used for validation
    # print(current_user.id)
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(owner_id=current_user.id, **post.dict()) # this will unpack the post dict to be formatted like above
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # this is like RETURNING * in sql, will return the created post in sql to new_post vrbl
    return new_post


@router.get('/my_article', response_model=List[schemas.Post])
def get_post(db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # (id: int, response: Response)
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() # it will fetch the first id that found
   
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with owner_id: {current_user.id} was not found!!")
    # Check the current user id wether it value is the same with owner_id of the post
    # Check if any of the posts don't belong to the current user
    for post in posts:
        if post.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")
    return posts

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist!!")
    # Check the current user id wether it value is the same with owner_id of the post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action" )
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, 
                db: Session=Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first() # grab the values in query
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist!!")
    
    # Check the current user id wether it value is the same with owner_id of the post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action" )
    
    # post_query.update({"title": "Updated Title", "content": "This is my updated content"}, synchronize_session=False)
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()