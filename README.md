# StudyHelper

강의 내용을 과목별로 관리하고, 간단한 AI를 통해 분류하며학습자료를 기반으로 퀴즈를 만들 수 있는 웹서비스입니다.

## 프로젝트 소개

대학교에서 여러 전공과목을 수강하다 보면 강의내용, 시험 정리, 과제 메모가 여러 파일과 프로그램에 흩어지게 됩니다.

StudyHelper는 학습자료를 한곳에 모아 저장하고 검색과 퀴즈 기능을 통해 시험 공부에 다시 활용할 수 있도록 하는 프로젝트입니다.

## 주요 기능
- 회원가입 및 로그인
- 로그아웃
- 세션 쿠키 기반 로그인 상태 유지
- 과목 생성, 조회, 검색, 수정, 삭제
- 학습자료 생성, 조회, 검색, 수정, 삭제
- 과목별 학습자료 필터링
- 브라우저 기반 대시보드
- 브라우저 기반 과목 관리 화면
- 브라우저 기반 학습자료 관리 화면
- 비밀번호 해시 저장

## 기술 스택

### Backend

- Python
- FASTAPI
- SQLAlchemy
- SQLite
- PostgreSQL

### Frontend

- HTML
- CSS
- JavaScript
- Jinja2

### Machine Learning

- pandas
- scikit-learn
- TF-IDF
- Logistic Regression

### Development

- Git
- GitHub
- pytest
- Docker
- GitHub Actions

## 주요 사용자 흐름

1. 회원가입 및 로그인
2. 과목 생성
3. 학습자료 작성
4. AI 과목 추천
5. 학습자료 저장 및 검색
6. 퀴즈 생성
7. 퀴즈 풀이 및 채점
8. 오답 노트 확인

## 개발 일정

- 1주차: 프로젝트 기획 및 FastAPI 기초 완료
- 2주차: 데이터베이스 및 과목/학습자료 CRUD 완료
- 3주차: 웹 화면 및 기본 인증 기능 진행 중
- 다음 목표: 사용자별 과목/학습자료 데이터 분리

## 실행 방법

개발이 진행되면서 작성할 예정

## 프로젝트 상태

- 프로젝트 기획 완료
- Python 가상환경 구성 완료
- FastAPI 및 Uvicorn 설치 완료
- 프로젝트 기본 폴더 구조 생성 완료
- 기본 API 및 상태 확인 API 구현 완료
- SQLite를 이용한 기본 SQL CRUD 실습 완료
- SQLAlchemy 기반 데이터베이스 연결 완료
- Course ORM 모델 및 과목 CRUD API 구현 완료
- Document ORM 모델 및 학습자료 CRUD API 구현 완료
- Jinja2 기반 웹 화면 구현 완료
- 대시보드 화면 구현 완료
- 과목 생성 및 목록 화면 구현 완료
- 학습자료 생성, 조회, 검색, 수정, 삭제 화면 구현 완료
- 정적 CSS 파일 연결 완료
- User ORM 모델 구현 완료
- 회원가입, 로그인, 로그아웃 기능 구현 완료
- 세션 쿠키 기반 로그인 상태 관리 구현 완료
- 비로그인 사용자의 대시보드 접근 제한 구현 완료
- PBKDF2 기반 비밀번호 해시 처리 구현 완료

## 프로젝트 구조

```text
app/
├─ main.py
├─ routers/
│  └─ courses.py
├─ schemas/
│  └─ course.py
└─ services/
   └─ course_service.py