# YOUTUBE_BOOKMARK_V1_0

YouTube URL을 카테고리별로 등록하고 회원이 조회할 수 있는 초경량 Django MVP입니다.

## 주요 기능

- 이메일 + 비밀번호 + 사용자명(username) 회원가입
- 이메일 또는 사용자명으로 로그인
- 카테고리 관리
- YouTube URL 등록/수정/삭제
- YouTube Embed 재생
- 카테고리별 영상 조회
- 영상 상세 페이지
- 영상 조회수
- 회원별 영상 좋아요(별표)
- 회원별 영상당 댓글 1개
- 댓글 삭제
- Django Admin을 이용한 관리
- PostgreSQL + Docker Compose
- Bootstrap 기반 반응형 UI

## 기술 스택

- Python 3.12
- Django 5.2
- PostgreSQL 16
- Gunicorn
- Bootstrap 5 CDN
- Docker / Docker Compose

## 프로젝트 구조

```text
YOUTUBE_BOOKMARK_V1_0/
├─ config/
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
│  └─ asgi.py
├─ videos/
│  ├─ admin.py
│  ├─ forms.py
│  ├─ models.py
│  ├─ urls.py
│  ├─ views.py
│  └─ migrations/
├─ templates/
│  ├─ base.html
│  ├─ registration/
│  └─ videos/
├─ static/
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
└─ manage.py
```

## 실행

### 1. 환경파일

`.env.example`을 복사하여 `.env`를 만듭니다.

PowerShell:

```powershell
Copy-Item .env.example .env
```

### 2. Docker 실행

```powershell
docker compose up -d --build
```

### 3. 마이그레이션

```powershell
docker compose exec web python manage.py migrate
```

### 4. 관리자 생성

```powershell
docker compose exec web python manage.py createsuperuser
```

### 5. 접속

- 사이트: http://localhost:8000/
- 관리자: http://localhost:8000/admin/

## 관리자에서 운영

1. `/admin/` 로그인
2. Categories에서 카테고리 생성
3. Videos에서 YouTube 영상 등록
4. 공개 여부를 확인
5. 사이트에서 카테고리별 영상 확인

YouTube URL 예:

```text
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://youtu.be/dQw4w9WgXcQ
https://www.youtube.com/shorts/dQw4w9WgXcQ
```

## 데이터 모델

```text
User
  ├── VideoLike
  └── Comment

Category
  └── Video
        ├── VideoLike
        └── Comment
```

### 핵심 제약

`VideoLike`는 `(video, user)`가 유일합니다.

`Comment`는 `(video, user)`가 유일합니다.

따라서 회원 한 명은 하나의 영상에 좋아요 1개, 댓글 1개만 등록할 수 있습니다.

## 다음 개발 단계

- 검색
- 인기영상/최신영상
- 관리자 대시보드
- 댓글 신고/관리
- 회원 정지
- YouTube Data API 연동
- AI 제목/요약/카테고리 추천
- 무료 호스팅(Render 등) 배포


## V1.0 FIX1 - YouTube Embed Error 153

YouTube에서 2025년부터 Embed 요청의 `HTTP Referer` 또는 동등한 클라이언트 식별 정보를 검사합니다.
FIX1에서는 다음을 적용했습니다.

- iframe `referrerpolicy="origin"`
- Django `SECURE_REFERRER_POLICY = "origin"`
- iframe URL에 현재 사이트 `origin` 전달
- Embed 실패 시 `YouTube에서 직접 보기` 링크 제공

기존 PostgreSQL DB 이름/사용자/비밀번호 및 Docker 설정은 변경하지 않았습니다.

기존 `.env` 파일이 있다면 그대로 유지하고 `.env`를 덮어쓰지 마십시오.
