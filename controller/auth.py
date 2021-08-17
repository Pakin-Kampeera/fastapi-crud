from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from schemas import schemas
from models import models
from util.hashing import Hash
from util.token import create_access_token


def user_login(request: schemas.Login, db: Session):
    user = db.query(models.User).filter(
        models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid Credentials')
    if not Hash.verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Invalid password')
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
