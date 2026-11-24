# Material PSI 분석 도우미 (구매SCM 관리 시스템) — PoC

휴대폰·태블릿용 자석부품 협력사 **㈜노바텍** 구매팀이 매주 Excel로 하던 **향후 14주 자재 과부족 점검**을 웹 시스템으로 옮긴 PoC(시범 버전)입니다.

생산계획(RTF / Production Plan)과 BOM으로 **자재 소요량을 자동 계산**하고, 재고·입고예정·Open PO와 대조해 **어느 자재가 몇 주차부터 부족한지**를 보여줍니다.

> 상태: v1.0 기능 구현 완료 (PoC, 로컬 PC 실행). 운영 배포 전 단계입니다.

---

## 주요 기능

| 구분 | Module | 내용 |
|---|---|---|
| 공통 | 계정·권한 | Log-in / Sign up / Master 승인 / User Management, Class별 권한(Master·Admin·User·Guest), 5회 실패 10분 잠금, 2시간 미사용 자동 Log-out |
| Master DB | 1. Material Master | 자재 기준정보, Excel Upload(Add / Change / Inactive), 화면 수정·Save, History |
| | 2. Assy Master | 제품(Assy) 기준정보 (Key = Customer Code) |
| | 3. BOM | Assy별 자재 구성·소요원수(분수 지원 `1/50`), 버전 History |
| | 4. Safety Stock | Assy별 안전재고 (RTF 14주차에 합산) |
| Weekly Data | 5. Inventory | 작업 주차 월요일 아침 재고 |
| | 6. RTF / Production | 출하계획·생산계획 14주 (W0 ~ W+13) |
| PO | 7. Open PO | 미입고 발주 (Final PO, Remain Q'ty 자동 계산) |
| | 8. Scheduled Receipt | 입고예정 (Manual) + Open PO 차이분을 L/T 주차에 자동 배치 (Calculated) |
| Report | 9. Material Requirement | Σ(Assy 주별 계획 × BOM 소요원수), RTF·Prod. 기준 각각 |
| | 10. Material PSI | 재고 과부족 · PO 과부족, **Recalculate**, **Weekly Reset** |

### 핵심 계산
- **RTF 기준 기초재고** = Material 재고 + Σ(Assy 재고 × 소요원수)
- **Prod. 기준 기초재고** = Material 재고
- **재고 과부족(주차 t)** = 기초재고 + 누적 입고예정 − 누적 소요량
- **PO 과부족(주차 t)** = 기초재고 + Open PO(In Transit + Remain) − 누적 소요량

### 공통 규칙
- 주차는 **ISO Week**, Current Week는 **베트남 시간(Asia/Ho_Chi_Minh)** 월요일 00:00에 전환. 화면 표기 `W48(W0)`
- 모든 Upload는 **검증 결과 미리보기 → [반영]**. Error가 1건이라도 있으면 전체 중단(Rollback)
- Master에 없는 Code는 Upload 허용 + 화면 `No DB` 표시 + Warning 보고
- 계산 결과(Module 9·10)는 **Recalculate 실행 시에만** 갱신, 그 전에는 `● Need Recalculation` 표시
- 권한은 화면 버튼뿐 아니라 **서버에서도** 검사

---

## 기술 스택
- Python 3.12+ (개발: 3.14), **Django 6**
- **PostgreSQL 17**
- 화면: Django Template(서버 렌더링) + CSS, 별도 Frontend 빌드 없음
- Excel: openpyxl

---

## 설치 및 실행 (Windows)

### 1. 준비물
- Python 3.12 이상
- PostgreSQL 17 (설치 시 postgres 관리자 비밀번호 설정, 포트 5432)
  ```
  winget install --id PostgreSQL.PostgreSQL.17 -i
  ```
  > Windows 사용자 이름이 한글이면 설치가 실패할 수 있습니다. 관리자 PowerShell에서 `$env:TEMP="C:\pgtemp"; $env:TMP="C:\pgtemp"`로 임시 폴더를 영문 경로로 바꾼 뒤 설치하세요.

### 2. 소스 받기 및 패키지 설치
```
git clone https://github.com/mac9375-byte/novartech_psi.git
cd novartech_psi
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

### 3. 환경 설정 (`.env`)
프로젝트 폴더에 `.env` 파일을 만들고 아래 내용을 넣은 뒤, `DJANGO_SECRET_KEY`와 `DB_PASSWORD`를 임의의 긴 문자열로 바꿉니다.
```
DJANGO_SECRET_KEY=change-me-to-a-long-random-string
DJANGO_DEBUG=1
DB_NAME=novatech_psi
DB_USER=novatech_app
DB_PASSWORD=change-me
DB_HOST=localhost
DB_PORT=5432
POC_SKIP_LOGIN=1
```
> `.env`에는 비밀번호가 들어가므로 Git에 올리지 않습니다 (`.gitignore`에 포함).

### 4. DB 준비
```
.venv\Scripts\python tools\setup_db.py      # postgres 관리자 비밀번호 입력 → 전용 계정·DB 생성
.venv\Scripts\python manage.py migrate
.venv\Scripts\python manage.py create_master --email 관리자메일@회사.com
```
`create_master`가 Master 계정 `novamaster`의 **임시 비밀번호를 한 번만** 화면에 보여줍니다. 최초 로그인 시 새 비밀번호로 바꿔야 합니다.

### 5. 서버 실행
```
.venv\Scripts\python manage.py runserver
```
브라우저에서 **http://localhost:8000** 접속. 끄려면 `Ctrl + C`.

---

## PoC 점검용 기능

### 로그인 생략
개발 모드(`DJANGO_DEBUG=1`)에서는 로그인 없이 **`poc_admin`(Admin)**으로 자동 로그인됩니다.
- 다른 계정으로 확인하려면 `/login/` 화면에서 직접 로그인
- 끄려면 `.env`에 `POC_SKIP_LOGIN=0`
- 운영 배포(`DJANGO_DEBUG=0`)에서는 자동으로 꺼집니다

### 예시 데이터
```
.venv\Scripts\python manage.py load_demo          # DEMO- 코드 예시 데이터 적재 + Recalculate
.venv\Scripts\python manage.py load_demo --clear  # 예시 데이터만 삭제
```

---

## 주간 사용 순서 (Admin)
1. (필요 시) **10. Material PSI → Weekly Reset**: 이번 주 Module 5~8 데이터 초기화
2. **Module 5~8 Upload**: Inventory → RTF/Production → **Open PO → Scheduled Receipt** (Open PO 먼저)
   - 각 화면 **Template** 버튼으로 이번 주 주차 Header가 들어간 빈 양식을 받을 수 있습니다
3. **10. Material PSI → Recalculate**
4. Module 9·10에서 과부족 확인 → 발주 의사결정

표준 업로드 양식은 `표준 업로드 양식_1123.xlsx`를 참고하세요. 시트명과 1행 Header는 정확히 일치해야 합니다.

---

## 테스트
```
.venv\Scripts\python manage.py test
```
자동 테스트 93개 (PostgreSQL 필요, 테스트용 DB는 자동 생성·삭제).

---

## 폴더 구조
```
config/      Django 설정·URL
accounts/    계정·로그인·권한(permissions.py)·User Management
core/        공통: Excel 읽기/쓰기, 주차 계산, Upload 미리보기·반영 흐름, 공통 화면
materials/   Module 1 Material Master
assies/      Module 2 Assy Master
bom/         Module 3 BOM
safety/      Module 4 Safety Stock
weekly/      Module 5~8 Inventory, RTF/Production, Open PO, Scheduled Receipt
psi/         Module 9~10 계산 엔진(engine.py), Recalculate, Weekly Reset
templates/   화면 HTML
static/      CSS
tools/       DB 준비 스크립트
설계/         설계 문서 (01~05)
Prompt 1135.md   요구사항 정의서 (업무 규칙 원본)
```

## 문서
- **운영 매뉴얼**: [`docs/운영매뉴얼.html`](docs/운영매뉴얼.html) — 주간 PSI 운영 프로세스, 10개 Tab 사용법, Error 조치 (내려받아 브라우저로 열기)
- 요구사항 정의서: [`Prompt 1135.md`](Prompt%201135.md)
- 설계 문서: [`설계/`](설계) — 01 공통기능·Material Master 확인항목, 02 공통기반 설계, 03 Material Master, 04 Assy Master, 05 Module 3~10 구현기록

## 운영 전환 전 할 일
- 운영 환경(클라우드 / 사내 서버) 결정 및 배포
- PoC 자동 로그인 제거, `DJANGO_DEBUG=0`, HTTPS
- 임시 비밀번호 e-mail 발송 연결 (현재는 서버 실행 화면에 출력)
- DB 자동 백업
- v1.0 범위 외(다음 버전): 발주필요수량 계산, MOQ, 자재 안전재고, 발주 제안
