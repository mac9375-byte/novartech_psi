# PLAN — novartech_psi (회사 노트북 환경)

## 목표
GitHub에서 zip으로 받은 PSI 시스템을 이 PC에서 실행하고, 이후 개선 작업을 Git으로 관리한다.

## 성공 기준
- http://localhost:8000 에서 Main·Material PSI 화면 정상, 데모 데이터 유지
- `manage.py test` 93개 통과
- PC 재부팅 후에도 DB 자동 기동

## 진행 기록

### 2026-11-25 환경 구축 (완료)
- `.venv`(Python 3.14) + requirements 설치. 처음엔 psycopg-binary DLL이 Windows 앱 제어 정책에 막혔으나 PostgreSQL 설치 후 정상 로드.
- PostgreSQL 17.12 winget 설치 → 한글 컴퓨터 이름 때문에 initdb·서비스 등록 실패 → 수동 initdb 후 서비스 등록.
  - 서비스 `postgresql-x64-17`(자동 시작, NetworkService), 데이터 `C:\Program Files\PostgreSQL\17\data`, 포트 5432
- `.env` 생성(비밀값 무작위 생성, postgres 관리자 비밀번호 포함), DB `novatech_psi`/계정 `novatech_app` 생성, migrate
- Master `novamaster` 생성(이메일 임시값 admin@novatech.local, 임시 P/W는 `.env`의 NOVAMASTER_TEMP_PASSWORD, 첫 로그인 시 변경)
- `load_demo` 적재(DEMO-, 2026-W48) → 사용자 점검 완료, 데모 데이터 유지 요청
- 테스트 93개 통과
- Git: `git init` 후 origin(mac9375-byte/novartech_psi) main 이력에 연결. 작업 폴더 = origin/main `8879d18` 동일(이 두 파일 제외)
- 디자인을 전역 스킬 `~/.claude/skills/novatech-design`으로 추출

## 다음 단계 (개선 제언, 우선순위순 — 착수 전 사용자 확인)
1. [ ] DB 자동 백업: 작업 스케줄러 + `pg_dump` 일일 백업, 최근 N개 보관. Weekly Reset 직전 자동 백업 검토
   - 검증: 백업 파일 생성 → 테스트 DB에 복원 확인
2. [ ] README 보완: 한글 컴퓨터 이름 설치 실패 우회, psycopg DLL 차단 이슈
3. [ ] CI: GitHub Actions + PostgreSQL 서비스로 테스트 자동 실행
4. [ ] 설치 일괄 스크립트(.env 생성→DB 생성→migrate→Master 생성)
5. [ ] 운영 전환: 서버 배포, DEBUG=0, HTTPS, PoC 자동 로그인 미들웨어 제거, SMTP로 임시 P/W 발송
6. [ ] 매뉴얼: 베트남 시간 기준 주차 전환(한국 월 00~02시는 지난주) 명시
7. [ ] v1.1 기능 후보: 발주필요수량·MOQ·자재 안전재고·발주 제안, 업로드 반영 후 Recalculate 유도

## 미커밋 상태
- `CLAUDE.md`, `PLAN.md`(이 파일)만 신규, 아직 커밋하지 않음
