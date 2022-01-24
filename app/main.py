from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote, follower

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# To activate the same virtual env tomorrow, use bin/activate command.
# Use the bin inside the relevant virtual env directory.
# If you use pipenv shell command, it will create a new child virtual env.

@app.get('/')
def hello():
    return {"message":"hello world"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(follower.router)
