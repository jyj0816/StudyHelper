from fastapi import FastAPI

from app.routers.courses import router as courses_router

app = FastAPI(
    title="StudyHelper API",
    description="학습 자료 관리 및 과목 분류 서비스",
    version="0.1.0",
)

app.include_router(courses_router)

@app.get("/")
def root():
    return {
        "message": "StudyHelper API",
        "docs": "/docs",
    }

@app.get("/health")
def health():
    return{
        "status": "ok",
        "service" : "StudyHelper",
    }