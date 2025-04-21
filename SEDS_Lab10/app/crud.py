from sqlalchemy.orm import Session
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email,
                          name=user.name)
    # instance object added to database session
    db.add(db_user)
    # changes are saved to the database
    db.commit()
    # instance is refreshed to contain any new data from the database, like the generated ID
    db.refresh(db_user)
    return db_user


def create_user_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(**post.dict(), author=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_user_posts(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Post)
        .filter(models.Post.author == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def delete_user_post(db: Session,
                     post: schemas.Post
                     ):
    db.delete(post)
    db.commit()


def update_user(db: Session, user_id: int, user_data: schemas.UserBase):
    user = get_user(db, user_id)
    if not user:
        return None
    for key, value in user_data.dict().items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def update_user_post(db: Session, post_id: int, post_data: schemas.PostBase):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        return None
    for key, value in post_data.dict().items():
        setattr(post, key, value)
    db.commit()
    db.refresh(post)
    return post


def delete_user(db: Session, user_id: int):
    # Fetch the user by ID
    user = get_user(db, user_id)
    if user:
        # If user has related posts, delete them first (optional, depending on cascade settings)
        posts = get_user_posts(db, user_id)
        for post in posts:
            db.delete(post)

        # Delete the user
        db.delete(user)
        db.commit()
        return True
    return False
