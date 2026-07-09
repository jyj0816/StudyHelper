from fastapi import FastAPI

from app.database import Base, engine
from app.models import Course, Document
from app.routers.courses import router as courses_router
from app.routers.documents import router as documents_router


# ORM 모델을 Python이 불러오도록 명시적으로 참조
_ = Course
_ = Document

# 아직 Alembic을 배우기 전이므로 자동으로 테이블 생성
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="StudyHelper API",
    description="학습 자료 관리 및 과목 분류 서비스",
    version="0.1.0",
)


app.include_router(courses_router)
app.include_router(documents_router)


@app.get("/")
def root():
    return {
        "message": "StudyHelper API",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "StudyHelper",
    }