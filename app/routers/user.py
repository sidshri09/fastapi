from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import util
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db
from app import oauth2


router = APIRouter(
    prefix= '/users',
    tags= ["Users"]
)
#
#
#  USERS
#
#
#
@router.get("/", response_model=List[schemas.ResponseUser])
def getUsers(db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user), limit:int =15, skip:int =0, search:Optional[str]=''):
    users=db.query(models.User).filter(models.User.email.contains(search)).limit(limit).offset(skip).all()
    if users:
     return users
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="users not found")

@router.get("/{id}", response_model=schemas.ResponseUser)
def fetchUserWithId(id: str, resp: Response, db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cur.execute("""SELECT * FROM posts WHERE id=%s""",[id])
    # records = cur.fetchone()
    users=db.query(models.User).filter(models.User.email == id)
    if users.first():
        return users.first()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id: {id} not found")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.ResponseUser)
def createUser(body: schemas.User, db: Session = Depends(get_db)):
    # cur.execute("""INSERT INTO posts (content, \"like\", dislike, love) VALUES(%s,%s,%s,%s) RETURNING *""", (body.content, body.like, body.dislike, body.love))
    # conn.commit()
    # records = cur.fetchall()
    users=db.query(models.User).filter(models.User.email == body.email)
    if users.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="email id already present")
    hashed_pwd = utils.hash(body.password)
    body.password = hashed_pwd
    users=models.User(**body.dict())
    db.add(users)
    db.commit()
    db.refresh(users)
    if users:
        return users
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not added")

@router.put("/changepassword/{id}", status_code=status.HTTP_200_OK)
def changePassword(id:int,body: schemas.EditPassword, db: Session = Depends(get_db)):
    # body.email = current_user.email
    updated_user={}
    users=db.query(models.User).filter(models.User.id == id)
    updated_user['email'] = users.first().email

    if utils.verify(body.old_password,users.first().password):
        updated_user['password'] = utils.hash(body.password) 
        users.update(updated_user,synchronize_session=False)
        db.commit()
        return {"message":"user details updated"}
    else: return{"message":"incorrect old password"}

@router.put("/", status_code=status.HTTP_200_OK)
def updateUser(body: schemas.EditUser, db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # print("inside PUT, printing body.dict",body.dict())
    # cur.execute("""UPDATE posts SET content=%s, \"like\"=%s, dislike=%s, love=%s WHERE id=%s RETURNING *""", (body.content, body.like, body.dislike, body.love, id))
    # conn.commit()
    # records = cur.fetchall()
    # print("inside PUT printing records from DB",records)

    users=db.query(models.User).filter(models.User.id == current_user.id)
    if users.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id: {id} not found")
    body.email = current_user.email
    users.update(body.dict(),synchronize_session=False)
    db.commit()
    return {"message":"user details updated"}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteUser(id: int, db: Session = Depends(get_db)):
    # cur.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",([id]))
    # conn.commit()
    # records = cur.fetchall()
    users=db.query(models.User).filter(models.User.id == id)
    if users.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id: {id} not found")
    users.delete(synchronize_session=False)
    db.commit()
    return ("user deleted successfully")