from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas import schemas
from models import models
from util.hashing import Hash


def show_by_id(id, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The user with id {id} is not available')
    return user


def create_user(user: schemas.User, db: Session):
    new_user = models.User(username=user.username,
                           email=user.email, password=Hash.hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def show_all_users(db: Session):
    users = db.query(models.User).all()
    return users
