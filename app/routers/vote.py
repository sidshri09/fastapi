from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db
from app import oauth2


router = APIRouter(
    prefix= '/votes',
    tags= ["Votes"]
)

@router.get("/{post_id}", response_model=List[schemas.Vote])
def getUsers(post_id: str,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    users=db.query(models.Vote).filter(models.Vote.post_id == post_id, models.Vote.user_id == current_user.id).first()
    if users:
     return users
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="vote not found")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.ResponseVote)
def addVote(body: schemas.Vote, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # cur.execute("""INSERT INTO posts (content, \"like\", dislike, love) VALUES(%s,%s,%s,%s) RETURNING *""", (body.content, body.like, body.dislike, body.love))
    # conn.commit()
    # records = cur.fetchall()
    if (db.query(models.Post).filter(models.Post.id == body.post_id)).first():
        records=db.query(models.Vote).filter(models.Vote.post_id == body.post_id, models.Vote.user_id == current_user.id)
        if body.vote_dir == True:
            if records.first():
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} already liked the post {body.post_id}")
            votes=models.Vote(user_id=current_user.id, post_id=body.post_id)
            db.add(votes)
            db.commit()
            db.refresh(votes)
            if votes:
                return votes
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="vote not submitted")
        
        if body.vote_dir == False:
            records=db.query(models.Vote).filter(models.Vote.post_id == body.post_id, models.Vote.user_id == current_user.id)
        
            if records.first() == None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="vote does not exist")
            
            records.delete(synchronize_session=False)
            db.commit()
            return ("vote deleted successfully")

    else:   
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {body.post_id} does not exist")
       