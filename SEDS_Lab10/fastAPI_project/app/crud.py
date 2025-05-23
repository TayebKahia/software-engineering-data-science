from sqlalchemy.orm import Session
from . import models, schemas

# Get *******************


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()


def get_user_posts(db, user_id, skip, limit):
    return db.query(models.Post).filter(models.Post.author == user_id).offset(skip).limit(limit).all()


# Create *******************
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


# Delete *******************
def delete_user_post(db: Session, post: schemas.Post):
    db.delete(post)
    db.commit()

# Update *************


def update_user(db: Session, user: schemas.UserUpdate, user_id: int):
    # old_user = db.query(models.User).get(user_id)
    # print(old_user)
    # old_user.name = user.name
    # old_user.email = user.email
    old_user = user
    db.merge(old_user)
    db.commit()
    db.refresh(old_user)
    return old_user
