from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from config.database import get_db
from schemas import schemas
from controller import user

router = APIRouter(prefix='/user', tags=['User'])


@router.get('/{id}', response_model=schemas.ShowUser)
def show(id, db: Session = Depends(get_db)):
    return user.show_by_id(id, db)


@router.post('/')
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create_user(request, db)


@router.get('/', response_model=List[schemas.ShowUser])
def show_all_user(db: Session = Depends(get_db)):
    return user.show_all_users(db)
