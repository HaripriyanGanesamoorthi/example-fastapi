from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from random import randrange
from ..import models, schemas, oauth2
from sqlalchemy import func
from ..database import get_db

router = APIRouter(
    prefix ="/post",
    tags = ["Posts"]
)

# #GET /post
# @router.get("/", response_model = List[schemas.Post])
# def get_post(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
#     #posts = cursor.execute("""SELECT * FROM posts """)
#     #posts = cursor.fetchall()
#     #print(posts)
#     print(current_user.id)
#     posts = db.query(models.Post).filter(
#         models.Post.owner_id == current_user.id).all()
#     print(posts)
#     return posts


@router.get("/", response_model=List[schemas.PostOut])
#@router.get("/")
def get_post(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user),Limit : int = 10, skip : int = 0, search : Optional[str] = ""):
    
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()

    
    return posts







@router.post("/",status_code=status.HTTP_201_CREATED, response_model = schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    #cursor.execute(
        #"""INSERT INTO posts (title,content,published)
        #VALUES (%s, %s, %s)
        #RETURNING * """,
        #(post.title,post.content,post.published)
    #)
    #new_post=cursor.fetchone()
    #conn.commit()
    # print(user_id.id)
    # print(user_id.email)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    # print(post.dict())
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()

    db.refresh(new_post)
    return new_post
    




#GET /posts/{id}
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return post


# #GET /posts/{id}
# @router.get("/posts/{id}")
# def get_post(id:int, response: Response):

#     post=find_post(id)
#     if not post:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"message":f"post with id: {id} not found"}
#     return {"post_detail":post}


#DELETE /posts/{id}
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    #deleting post
    #find the index in the array that has required ID
    #my_post.pop(index)
    #index=find_index_post(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post=post_query.first()
    
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    #my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT )



#PUT /posts/{id}
@router.put("/{id}", response_model = schemas.Post)
def update_post(id:int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    #index=find_index_post(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    updated_post = post_query.first()
    return updated_post

