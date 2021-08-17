from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas import schemas
from models import models


def show_by_id(id, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the id {id} is not available')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with the id {id} is not available'}
    return blog


def destroy_by_id(id, db: Session):
    db.query(models.Blog).filter(models.Blog.id ==
                                 id).delete(synchronize_session=False)
    db.commit()
    return 'Done'


def update_by_id(id, blog: schemas.BlogBase, db: Session):
    blog_update = db.query(models.Blog).filter(
        models.Blog.id == id).update({'title': blog.title, 'body': blog.body})
    db.commit()
    if not blog_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with {id} not found')
    return 'Update'


def create_user(blog: schemas.BlogBase, db: Session):
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def show_all_blog(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs
