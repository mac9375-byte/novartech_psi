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

### 2026-11-26 DB 백업 명령 (브랜치 `feat/db-backup`)
- `core/management/commands/backup_db.py`: `pg_dump -Fc` → `backups/novatech_psi_YYYYMMDD_HHMMSS.dump`, `--keep`(기본 14) 초과분 오래된 것부터 삭제, 실패 시 반쯤 쓴 파일 삭제
- 테스트 `core.tests.BackupDbTests` 추가(먼저 실패 확인 → 구현 후 통과). 전체 94개 통과
- 실DB 백업 → 임시 DB `psi_restore_check`에 `pg_restore` → 자재 5·사용자 2건 일치 확인 후 임시 DB 삭제
- README에 백업·복원 방법 추가, `.gitignore`에 `backups/`

### 2026-11-26 v1.1 발주필요수량 + Recalculate 안내 (브랜치 `feat/order-requirement`)
사용자 결정: 범위 = 발주필요수량(자재 안전재고·MOQ) + Recalculate 안내, 기준 = PO 과부족, MOQ = 미만이면 MOQ.

계산식 (Material × Plan, Recalculate 때 계산):
1. 주차 t마다 `net_t = PO Balance_t + 앞 주차까지 추가한 발주량 − 자재 안전재고`
2. `net_t < 0`이면 필요량 `q = ceil(−net_t)`(정수 올림) → `q < MOQ`이면 `q = MOQ` → Rounding Value > 0이면 그 배수로 올림. 이 q를 t주차 입고분으로 누적
3. 발주 주차 = t − L/T. 0보다 앞이면(이미 늦음) W0에 합산하고 Overdue 표시
4. Material Master에 없는 자재(No DB)는 L/T를 몰라 계산하지 않음
- 저장: `PsiRow.order_req`(발주 주차 기준 14칸) / 화면: PSI 5번째 행 "Order Requirement"
- Material Master: `Mat. Safety Stock`, `MOQ`, `Rounding Value` 열(선택, 빈칸=0, 0 이상 정수). Change Upload에서 열이 없으면 0으로 바뀜 → 미리보기 변경내역에 표시됨

Recalculate 안내: 모든 Module 화면 상단 "● Need Recalculation" 옆에 권한자에게 [Recalculate] 버튼.

결과:
- 테스트 먼저 작성(공식 단위 5, 재계산 통합 1, Recalculate 버튼 1, Material Master 3) → 실패 확인 → 구현 → 전체 104개 통과
- 기존 테스트 1건 수정: History Download에 열 2개가 늘어 Change Type 열 위치 h[12] → h[14]
- 실DB: `backup_db`로 백업 후 migrate (materials 0003, psi 0002). 데모 자재 Magnet(안전재고 15,000 / MOQ 10,000), Cap(2,000 / 5,000)를 화면 Save로 입력 → 새 Recalculate 버튼으로 재계산 → PSI에 Order Requirement 10,000·5,000 표시 확인
- `load_demo`에도 같은 값 반영, README·운영매뉴얼(용어, 판독, 1번·10번 Tab) 갱신
- 권한 표시는 `core.context.permissions` context processor (서버 검사는 기존 `@require` 그대로)
- 사용자 요청으로 Rounding Value(발주·포장 단위) 추가: MOQ 적용 후 배수 올림. 테스트 105개 통과, 실DB 백업 후 migrate(materials 0004), 데모 Magnet Rounding 4,000 → 발주필요수량 10,000 → 12,000 화면 확인

## 다음 단계 (개선 제언, 우선순위순 — 착수 전 사용자 확인)
1. [ ] DB 자동 백업
   - [x] `backup_db` 명령 + 복원 검증
   - [ ] Windows 작업 스케줄러 일일 등록 (2026-11-26 사용자 보류 — 당분간 수동 `backup_db`)
   - [ ] Weekly Reset 직전 자동 백업 검토
2. [ ] README 보완: 한글 컴퓨터 이름 설치 실패 우회, psycopg DLL 차단 이슈
3. [ ] CI: GitHub Actions + PostgreSQL 서비스로 테스트 자동 실행
4. [ ] 설치 일괄 스크립트(.env 생성→DB 생성→migrate→Master 생성)
5. [ ] 운영 전환: 서버 배포, DEBUG=0, HTTPS, PoC 자동 로그인 미들웨어 제거, SMTP로 임시 P/W 발송
6. [ ] 매뉴얼: 베트남 시간 기준 주차 전환(한국 월 00~02시는 지난주) 명시
7. [x] v1.1: 발주필요수량·MOQ·Rounding Value·자재 안전재고, Recalculate 안내 버튼 (2026-11-26)
8. [ ] 발주 제안 결과 저장 Module (요구사항 Ⅰ-5 (c)) — 발주필요수량을 확정·이력으로 남길지 사용자와 결정 필요

## 현재 상태 / 재개 지점 (2026-11-26)
- Git: `feat/order-requirement` = `feat/db-backup`(backup_db) + v1.1 발주필요수량. 커밋·푸시 후 main 대상 PR 생성, **머지 대기**
- 실DB: migrate 완료(materials 0004, psi 0002). 데모 Magnet(SS 15,000 / MOQ 10,000 / RV 4,000), Cap(SS 2,000 / MOQ 5,000) 입력·재계산 완료. 백업 `backups/` 3개
- 테스트 105개 통과
- 디자인: 사이드바(아이콘 레일/숨김 서랍) 시안 검토 후 **현행 상단 탭 유지**로 결정 (2026-11-26)
- 다음에 할 일: ① PR 머지 → ② 다음 단계 2번(README 설치 이슈) 이후 또는 8번(발주 제안 Module) 업무 규칙 결정
