from ecdsa.ecdsa import Private_key
from sqlalchemy import Column, Integer, Text, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, Boolean
from .database import Base

class Post(Base):
    __tablename__="posts"

    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(Text, nullable=False)
    published = Column(Boolean, nullable=False, server_default='True')
    CreatedAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    parent_post = Column(Integer, nullable=True)
    user = relationship("User")

class User(Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    CreatedAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    profile_pic = Column(Text, nullable=True, server_default="https://bagheera-img.s3.amazonaws.com/another%40example.com/download.jpeg")

class Vote(Base):
    __tablename__="votes"

    post_id = Column(Integer, ForeignKey("posts.id",ondelete="CASCADE"), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), primary_key=True, nullable=False)

class Follower(Base):
    __tablename__="followers"

    follower_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), primary_key=True, nullable=False)
    following_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), primary_key=True, nullable=False)