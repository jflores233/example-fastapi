from fastapi import Depends, Response, status, HTTPException, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, oauth2
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostOut] ) #use LIST as there are multiple posts to return
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #cursor.execute("""select * from posts""") #postgres way of doing things
    #posts = cursor.fetchall()

    #limit will limit the number of results, default is 10
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #get all posts for everyone
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() #get all posts for the current user

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #line 6 uses pydantic to validate data from POST
    #cursor.execute("""INSERT INTO  posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()

    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(owner_id=current_user.id,**post.dict()) #simply way of doing vs line above
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post



@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #everything is a str, need to make it an int and validate it as an int
    #cursor.execute("""select * from posts where id = %s""", (str(id)) )
    #posts = cursor.fetchone()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    #limit who can get a post
    #if post.owner_id != current_user.id:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform the current action")

    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id), ))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    #if deleted_post == None:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id doesn't exist")
    #return Response(status_code=status.HTTP_204_NO_CONTENT) #204 doesn't return any data so we can only pass code 204

    post_query = db.query(models.Post).filter(models.Post.id == id) #sqlalchemy way of doing things
    post = post_query.first()

    #check if there are any posts
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id doesn't exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform the current action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT) #204 doesn't return any data so we can only pass code 204



@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published=%s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    
    #if updated_post == None:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id doesn't exist")

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id doesn't exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform the current action")

    post_query.update(updated_post.dict(), synchronize_session=False) #{"title":'title of my post'}
    db.commit()

    return post_query.first()