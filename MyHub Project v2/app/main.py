from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import auth, users, ratings,posts
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(users.router, prefix="/users", tags = ["Users"])
app.include_router(auth.router, tags=["Users"])
app.include_router(ratings.router, prefix ="/rate", tags=["Ratings"])

@app.get("/", tags=["General"])
def home_page() -> dict:
    return {"message": "Available queries -> /posts /users /rate"}