from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from .. import schemas, models
from sqlalchemy.orm import Session
from ..database import get_db
from hashing import Hash

router = APIRouter()


@router.get('/user/{id}', response_model=schemas.ShowUser, tags=['User'])
def show(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The user with id {id} is not available')
    return user


@router.post('/user', tags=['User'])
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(username=user.username,
                           email=user.email, password=Hash.hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/user', response_model=List[schemas.ShowUser], tags=['User'])
def show_all_user(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users
