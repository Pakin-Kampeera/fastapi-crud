from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.orm import Session
from config.database import get_db
from schemas import schemas
from controller import user
from util.oauth2 import get_current_user

router = APIRouter(prefix='/user', tags=['User'])


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def show(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return user.show_by_id(id, db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create_user(request, db)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser])
def show_all_user(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return user.show_all_users(db)
