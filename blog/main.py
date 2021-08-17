from fastapi import FastAPI
from database import engine
import models
import uvicorn
from routes import user, blog


models.Base.metadata.create_all(engine)

app = FastAPI(redoc_url=None)
app.include_router(user.router)
app.include_router(blog.router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', reload=True)
