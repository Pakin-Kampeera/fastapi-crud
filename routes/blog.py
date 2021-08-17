from fastapi import APIRouter, status, Depends
from typing import List
from .. import schemas
from sqlalchemy.orm import Session
from ..database import get_db
from ..controller import blog

router = APIRouter(prefix='blog', tags=['Blogs'])


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show(id, db: Session = Depends(get_db)):
    return blog.show_by_id(id, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    return blog.destroy_by_id(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.BlogBase, db: Session = Depends(get_db)):
    return blog.update_by_id(id, request, db)


@router.post('/', status_code=status.HTTP_201_CREATED,  tags=['Blogs'])
def create(request: schemas.BlogBase, db: Session = Depends(get_db)):
    return blog.create_user(request, db)


@router.get('/', response_model=List[schemas.Blog])
def show_all_blog(db: Session = Depends(get_db)):
    return blog.show_all_blog(db)
