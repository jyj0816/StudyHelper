from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.models import Course, Document
from app.routers.courses import router as courses_router
from app.routers.documents import router as documents_router
from app.routers.web import router as web_router


_ = Course
_ = Document

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="StudyHelper API",
    description="학습 자료 관리 및 과목 분류 서비스",
    version="0.1.0",
)


app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)

app.include_router(web_router)
app.include_router(courses_router)
app.include_router(documents_router)


@app.get("/")
def root():
    return {
        "message": "StudyHelper API",
        "docs": "/docs",
        "dashboard": "/dashboard",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "StudyHelper",
    }