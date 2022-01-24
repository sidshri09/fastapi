from typing import List
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from app import oauth2
from sqlalchemy import func



router = APIRouter(
    prefix= '/followers',
    tags= ["Followers"]
)

@router.get("/{following_id}", response_model=List[schemas.FollowingOut])
def getFollowers(following_id: str,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    followers=db.query(models.Follower).filter(models.Follower.following_id == following_id)
    print(followers)
    if followers.all():
        return followers.all()

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="followers not found")

@router.get("/all/{following_id}")
def getFollowers(following_id: str,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    users=db.query(models.User).join(models.Follower,models.Follower.follower_id == models.User.id, isouter=True).order_by(models.Follower.following_id).filter(models.Follower.following_id == following_id)
    print(users.all())
    if users.all():
        return users.all()

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="followers not found")

@router.get("/gurus/{follower_id}", response_model=List[schemas.FollowingOut])
def getFollowers(follower_id: str,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    followings=db.query(models.Follower).filter(models.Follower.follower_id == follower_id)
    print(followings)
    if followings.all():
        return followings.all()

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="followings not found")


@router.get("/one/{following_id}", response_model=schemas.FollowingOut)
def getFollowers(following_id: str,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    followings=db.query(models.Follower).filter(models.Follower.follower_id == current_user.id, models.Follower.following_id == following_id)
    print(followings)
    if followings.first():
        return followings.first()

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="followings not found")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.FollowingOut)
def addVote(body: schemas.FollowingIn, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # cur.execute("""INSERT INTO posts (content, \"like\", dislike, love) VALUES(%s,%s,%s,%s) RETURNING *""", (body.content, body.like, body.dislike, body.love))
    # conn.commit()
    # records = cur.fetchall()
    if (db.query(models.User).filter(models.User.id == body.following_id)).first():
        records=db.query(models.Follower).filter(models.Follower.following_id == body.following_id, models.Follower.follower_id == current_user.id)
        if body.follow_dir == True:
            if records.first():
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} already followed the user {body.following_id}")
            followers=models.Follower(follower_id=current_user.id, following_id=body.following_id)
            db.add(followers)
            db.commit()
            db.refresh(followers)
            if followers:
                return followers
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="could not follow")
        
        if body.follow_dir == False:
        
            if records.first() == None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="following does not exist")
            
            records.delete(synchronize_session=False)
            db.commit()
            return ("vote deleted successfully")

    else:   
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {body.post_id} does not exist")
       