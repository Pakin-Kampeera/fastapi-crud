from fastapi import APIRouter, HTTPException, status, Depends, Response
from typing import List
from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()


@router.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['Blogs'])
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the id {id} is not available')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with the id {id} is not available'}
    return blog


@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Blogs'])
def destroy(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id ==
                                 id).delete(synchronize_session=False)
    db.commit()
    return 'Done'


@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Blogs'])
def update(id, blog: schemas.BlogBase, db: Session = Depends(get_db)):
    blog_update = db.query(models.Blog).filter(
        models.Blog.id == id).update({'title': blog.title, 'body': blog.body})
    db.commit()
    if not blog_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with {id} not found')
    return 'Update'


@router.post('/blog', status_code=status.HTTP_201_CREATED,  tags=['Blogs'])
def create(blog: schemas.BlogBase, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get('/blog', response_model=List[schemas.Blog], tags=['Blogs'])
def show_all_blog(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs
