import uvicorn
from fastapi import FastAPI
from models import models
from routes import user, blog, auth
from config.database import engine


models.Base.metadata.create_all(engine)

app = FastAPI(redoc_url=None)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(blog.router)

if __name__ == '__main__':
    uvicorn.run('server:app', host='127.0.0.1', reload=True)
