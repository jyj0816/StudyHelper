# StudyHelper

강의 내용과 학습자료를 과목별로 관리하고, 검색과 향후 AI 기능을 통해 시험 공부에 다시 활용할 수 있도록 만드는 웹서비스입니다.

## 프로젝트 소개

대학교에서 여러 전공과목을 수강하다 보면 강의 내용, 시험 정리, 과제 메모가 여러 파일과 프로그램에 흩어지게 됩니다.

StudyHelper는 학습자료를 한곳에 모아 저장하고, 과목별 분류와 검색 기능을 통해 필요한 내용을 쉽게 다시 찾아볼 수 있도록 하는 프로젝트입니다.

향후에는 학습자료를 기반으로 AI 과목 추천, 퀴즈 생성, 오답 노트 기능까지 확장하는 것을 목표로 합니다.

## 주요 기능

- 회원가입 및 로그인
- 로그아웃
- 세션 쿠키 기반 로그인 상태 유지
- 비밀번호 해시 저장
- 사용자별 과목 관리
- 사용자별 학습자료 관리
- 과목 생성, 조회, 검색, 수정, 삭제 API
- 학습자료 생성, 조회, 검색, 수정, 삭제 API
- 과목별 학습자료 필터링
- 제목, 내용, 태그 기반 학습자료 검색
- 브라우저 기반 대시보드
- 브라우저 기반 과목 관리 화면
- 브라우저 기반 학습자료 관리 화면
- 과목 삭제 시 연결된 학습자료 자동 삭제
- 로그인하지 않은 사용자의 주요 화면 접근 제한
- 학습자료 태그 정규화
- 태그별 학습자료 필터링
- 학습자료 검색 기능 개선
- 학습자료 기반 간단한 빈칸 퀴즈 생성
- 퀴즈 답안 제출 및 자동 채점
- 퀴즈 풀이 결과 저장
- 오답노트

## 향후 구현 예정 기능

- AI 과목 추천
- 학습자료 기반 퀴즈 생성
- 퀴즈 풀이 및 채점
- 오답 노트
- 학습 통계
- 과목 수정 웹 화면
- 테스트 코드 작성
- Docker 기반 실행 환경 구성
- GitHub Actions 기반 자동 검사
- PostgreSQL 연동

## 기술 스택

### Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn

### Frontend

- HTML
- CSS
- Jinja2

### Development

- Git
- GitHub
- Python 가상환경

### 향후 사용 예정

- PostgreSQL
- pytest
- Docker
- GitHub Actions
- pandas
- scikit-learn
- TF-IDF
- Logistic Regression

## 주요 사용자 흐름

1. 회원가입 및 로그인
2. 과목 생성
3. 학습자료 작성
4. 과목별 학습자료 조회
5. 제목, 내용, 태그 기반 학습자료 검색
6. 학습자료 수정 및 삭제
7. 과목 삭제 시 연결된 학습자료 함께 삭제
8. 로그아웃

## 개발 일정

- 1주차: 프로젝트 기획 및 FastAPI 기초 완료
- 2주차: 데이터베이스 및 과목/학습자료 CRUD 완료
- 3주차: 웹 화면, 기본 인증, 사용자별 데이터 분리 완료
- 다음 목표: 학습자료 검색 기능 개선 및 기본 테스트 코드 작성

## 실행 방법

### 1. 저장소 클론

```bash
git clone https://github.com/jyj0816/StudyHelper.git
cd StudyHelper
```

### 2. 가상환경 생성 및 실행

```bash
python -m venv venv
source venv/Scripts/activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. 서버 실행

```bash
python -m uvicorn app.main:app --reload
```

### 5. 브라우저 접속

```text
http://127.0.0.1:8000/dashboard
```

API 문서:

```text
http://127.0.0.1:8000/docs
```

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
- 사용자별 과목 데이터 분리 구현 완료
- 사용자별 학습자료 데이터 분리 구현 완료
- 로그인하지 않은 사용자의 과목/학습자료 화면 접근 제한 구현 완료
- 과목 삭제 시 연결된 학습자료 함께 삭제 처리 완료
- 사용자별 동일 과목명 생성 가능하도록 수정 완료
- pytest 기반 기본 테스트 코드 작성 완료
- 인증 기능 테스트 작성 완료
- 사용자별 과목 데이터 분리 테스트 작성 완료
- 학습자료 태그 정규화 기능 구현 완료
- 태그별 학습자료 필터링 구현 완료
- 학습자료 검색 기능 개선 완료
- 학습자료 검색/태그 테스트 작성 완료
- 학습자료 기반 빈칸 퀴즈 생성 기능 구현 완료
- 퀴즈 생성 API 구현 완료
- 퀴즈 생성 웹 화면 구현 완료
- 퀴즈 생성 기능 테스트 작성 완료
- 퀴즈 답안 제출 기능 구현 완료
- 퀴즈 자동 채점 기능 구현 완료
- 퀴즈 풀이 결과 저장 기능 구현 완료
- 오답노트 웹 화면 구현 완료
- 퀴즈 풀이 기록 테스트 작성 완료

## 프로젝트 구조

```text
app/
├─ main.py
├─ database.py
├─ security.py
├─ dependencies/
│  ├─ __init__.py
│  └─ auth.py
├─ models/
│  ├─ __init__.py
│  ├─ user.py
│  ├─ course.py
│  ├─ document.py
│  └─ quiz_attempt.py
├─ routers/
│  ├─ auth.py
│  ├─ courses.py
│  ├─ documents.py
│  └─ web.py
├─ schemas/
│  ├─ user.py
│  ├─ course.py
│  ├─ document.py
│  └─ quiz.py
├─ services/
│  ├─ user_service.py
│  ├─ course_service.py
│  ├─ document_service.py
│  └─ quiz_service.py
├─ templates/
│  ├─ base.html
│  ├─ dashboard.html
│  ├─ wrong_notes.html
│  ├─ auth/
│  │  ├─ login.html
│  │  └─ register.html
│  ├─ courses/
│  │  ├─ list.html
|  |  └─ edit.html
│  └─ documents/
│     ├─ list.html
│     ├─ new.html
│     ├─ detail.html
│     ├─ edit.html
│     ├─ quiz.html
│     └─ quiz_result.html
└─ static/
   └─ css/
      └─ style.css

      
tests/
├─ __init__.py
├─ conftest.py
├─ test_security.py
├─ test_auth.py
├─ test_course_isolation.py
├─ test_course_edit_web.py
├─ test_document_search_tags.py      
├─ test_document_quiz.py
└─ test_quiz_attempts.py
```

## 브랜치 전략

- `main`: 완료된 기능만 반영하는 기본 브랜치
- 기능 개발 브랜치: `feat/...`
- 기능 단위로 Pull Request를 생성하고 merge

## 최근 작업 내용

### 기본 인증 기능

- User 모델 추가
- 회원가입 기능 추가
- 로그인 기능 추가
- 로그아웃 기능 추가
- 세션 기반 로그인 상태 관리
- 비밀번호 PBKDF2 해시 저장
- 비로그인 사용자의 대시보드 접근 제한

### 사용자별 데이터 분리

- Course 모델에 `user_id` 추가
- Document 모델에 `user_id` 추가
- 사용자별 과목 조회/생성/수정/삭제 처리
- 사용자별 학습자료 조회/생성/수정/삭제 처리
- 사용자별 동일 과목명 생성 가능
- 과목 삭제 시 연결된 학습자료 함께 삭제

## 테스트

pytest를 사용해 주요 기능을 검증

현재 테스트 범위

- 비밀번호 해시 및 검증 테스트
- 회원가입 성공 테스트
- 중복 이메일 회원가입 실패 테스트
- 로그인 성공 테스트
- 잘못된 비밀번호 로그인 실패 테스트
- 비로그인 API 접근 차단 테스트
- 과목 생성 테스트
- 사용자별 과목 데이터 분리 테스트
- 사용자별 동일 과목명 생성 가능 테스트
- 같은 사용자의 중복 과목명 생성 실패 테스트
- 과목 수정 웹 페이지 접근 테스트
- 과목 수정 성공 테스트
- 중복 과목명 수정 실패 테스트
- 다른 사용자의 과목 수정 화면 접근 차단 테스트
- 학습자료 태그 정규화 테스트
- 학습자료 키워드 검색 테스트
- 학습자료 태그 필터 테스트
- 학습자료 웹 화면 태그 링크 표시 테스트
- 학습자료 웹 화면 태그 필터 테스트
- 학습자료 퀴즈 생성 API 테스트
- 학습자료 퀴즈 생성 웹 화면 테스트
- 다른 사용자의 학습자료 퀴즈 생성 차단 테스트
- 퀴즈 답안 제출 API 테스트
- 퀴즈 정답 판정 테스트
- 퀴즈 오답 판정 테스트
- 오답노트 API 테스트
- 오답노트 웹 화면 테스트

테스트 실행:

```bash
pytest
