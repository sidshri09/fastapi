
from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

from app import oauth2
from .. import models, schemas 
from ..database import get_db
router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
);

@router.get("/",response_model=List[schemas.PostOut])
def getPosts(db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user), limit:int =15, skip:int =0, search:Optional[str]=''):
    # posts=db.query(models.Post).filter(models.Post.content.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.content.contains(search)).limit(limit).offset(skip).all()

    if posts:
     return posts
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="posts not found")

@router.get("/{id}", response_model=schemas.PostOut)
def fetchPostWithId(id: int, resp: Response, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # cur.execute("""SELECT * FROM posts WHERE id=%s""",[id])
    # records = cur.fetchone()
    # records=db.query(models.Post).filter(models.Post.id == id)
    records = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id)
    if records.first():
        return records.first()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found")

@router.get("/replies/{id}",response_model=List[schemas.PostOut])
def fetchPostWithId(id: int, resp: Response, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # cur.execute("""SELECT * FROM posts WHERE id=%s""",[id])
    # records = cur.fetchone()
    # records=db.query(models.Post).filter(models.Post.id == id)
    records = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.parent_post == id).all()
    print("records***")
    print(records)
    if records:
        return records
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found")



@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.ResponsePost)
def createPost(body: schemas.Body, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # cur.execute("""INSERT INTO posts (content, \"like\", dislike, love) VALUES(%s,%s,%s,%s) RETURNING *""", (body.content, body.like, body.dislike, body.love))
    # conn.commit()
    # records = cur.fetchall()
    records=models.Post(user_id=current_user.id, **body.dict())
    db.add(records)
    db.commit()
    db.refresh(records)
    if records:
        return records
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not submitted")

@router.put("/{id}", status_code=status.HTTP_200_OK)
def updatePost(id: int, body: schemas.EditPost, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # print("inside PUT, printing body.dict",body.dict())
    # cur.execute("""UPDATE posts SET content=%s, \"like\"=%s, dislike=%s, love=%s WHERE id=%s RETURNING *""", (body.content, body.like, body.dislike, body.love, id))
    # conn.commit()
    # records = cur.fetchall()
    # print("inside PUT printing records from DB",records)
    records=db.query(models.Post).filter(models.Post.id == id)

    if records.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found")
    
    if current_user.id != records.first().user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not authorized to perform the requested action")

    
    records.update(body.dict(),synchronize_session=False)
    db.commit()
    return {"message":"record updated"}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # cur.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",([id]))
    # conn.commit()
    # records = cur.fetchall()
    records=db.query(models.Post).filter(models.Post.id == id)
    replies=db.query(models.Post).filter(models.Post.parent_post == id)
    
    if replies.all() != None:
        for pst in replies.all():
            print(pst.parent_post)
            pst.parent_post = None

    if records.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found")
    
    if current_user.id != records.first().user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not authorized to perform the requested action")

    records.delete(synchronize_session=False)
    db.commit()
    return ("post deleted successfully")
