# Material PSI 분석 도우미 (novartech_psi)

㈜노바텍 구매팀의 14주 자재 과부족(PSI) 점검을 웹으로 옮긴 PoC. 업무 규칙·기능 상세는 `README.md`, 요구사항 원본은 `Prompt 1135.md`, 설계는 `설계/`.

## 기술 스택
- Python 3.14 venv(`.venv`), Django 6.1, PostgreSQL 17, openpyxl, psycopg 3
- 서버 렌더링 Template + `static/css/app.css` (빌드 도구 없음)
- 디자인은 전역 스킬 `novatech-design`으로도 추출되어 있음

## 명령
- 서버: `.venv/Scripts/python manage.py runserver` (또는 preview `psi-dev`) → http://localhost:8000 (poc_admin 자동 로그인)
- 테스트: `.venv/Scripts/python manage.py test --noinput` (93개, 약 2.5분, PostgreSQL 필요)
- 데모 데이터: `manage.py load_demo` / `load_demo --clear`

## 코딩 규칙
- 최소 변경, 기존 스타일 유지. 업로드는 미리보기→반영, Error 1건이면 전체 Rollback 규칙 유지.
- 권한은 서버에서도 검사(`accounts/permissions.py`).

## Constraints
- PostgreSQL 전용 코드 있음(advisory lock, `core/locks.py`, `psi/engine.py`) → SQLite로 바꾸지 말 것.
- 이 PC(컴퓨터 이름 한글)에서는 EDB 설치 프로그램의 initdb·서비스 등록 단계가 실패한다. 재설치 시 `initdb -E UTF8 --locale=C` 수동 실행 + `pg_ctl register`로 처리.
- `.env`에 비밀값(DJANGO_SECRET_KEY, DB_PASSWORD, PG_SUPERUSER_PASSWORD, NOVAMASTER_TEMP_PASSWORD)이 있다. 출력·커밋 금지.
- 커밋·푸시는 사용자 요청 시에만.
