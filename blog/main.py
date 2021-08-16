from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import List
from hashing import Hash
import schemas
import models
from database import engine, SessionLocal
import uvicorn
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['Blogs'])
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the id {id} is not available')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with the id {id} is not available'}
    return blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Blogs'])
def destroy(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id ==
                                 id).delete(synchronize_session=False)
    db.commit()
    return 'Done'


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Blogs'])
def update(id, blog: schemas.Blog, db: Session = Depends(get_db)):
    blog_update = db.query(models.Blog).filter(
        models.Blog.id == id).update(blog)
    db.commit()
    if not blog_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with {id} not found')
    return blog_update


@app.post('/blog', status_code=status.HTTP_201_CREATED,  tags=['Blogs'])
def create(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog', response_model=List[schemas.ShowBlog], tags=['Blogs'])
def show_all_blog(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/user/{id}', response_model=schemas.ShowUser, tags=['User'])
def show(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The user with id {id} is not available')
    return user


@app.post('/user', tags=['User'])
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(username=user.username,
                           email=user.email, password=Hash.hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user', response_model=List[schemas.ShowUser], tags=['User'])
def show_all_user(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', reload=True)
