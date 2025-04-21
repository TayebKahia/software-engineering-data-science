from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/", response_model=list[schemas.User])
async def get_users(skip: int = 0, limit: int = 100, db: Session =
                    Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/{user_id}/posts/", response_model=list[schemas.Post])
async def get_user_posts(user_id: int, skip: int = 0, limit: int = 100, db:
                         Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    posts = crud.get_user_posts(db, user_id, skip, limit)
    return posts


@app.post("/users/new", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session =
                      Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.post("/users/{user_id}/posts/new", response_model=schemas.Post)
async def create_post_for_user(user_id: int,
                               post: schemas.PostCreate,
                               db: Session = Depends(get_db)
                               ):
    return crud.create_user_post(db=db, post=post, user_id=user_id)


@app.delete("/users/{user_id}/delete_post/{post_id}")
async def delete_post_for_user(user_id: int,
                               post_id: int,
                               db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.author == user_id,
                                           models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="User or Post not found")
    crud.delete_user_post(db=db, post=db_post)
    return {"msg": "Successfully Deleted"}


@app.delete("/users/{user_id}")
async def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    success = crud.delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"msg": "User successfully deleted"}


@app.patch("/users/{user_id}")
async def update_user_endpoint(user_id: int, user_data: schemas.UserBase, db: Session = Depends(get_db)):
    user = crud.update_user(db=db, user_id=user_id, user_data=user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"msg": "User successfully updated", "user": user}


@app.patch("/posts/{post_id}")
async def update_post_endpoint(post_id: int, post_data: schemas.PostUpdate, db: Session = Depends(get_db)):
    post = crud.update_user_post(db=db, post_id=post_id, post_data=post_data)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"msg": "Post successfully updated", "post": post}
