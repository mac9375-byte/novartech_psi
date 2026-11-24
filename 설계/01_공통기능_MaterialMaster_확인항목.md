# 01. 공통 기반 기능 + Ⅵ-1 Material Master 확인 항목 (Ⅰ-6)

- 작성일: 2026-11-24
- 근거 문서: `Prompt 1135.md`, `PSI_기획서_시스템 UI 도안 1123.pptx`, `표준 업로드 양식_1123.xlsx`
- 상태: **[확인 필요] 5건 확정 완료 (2026-11-24, 권장안 채택)**. 나머지 `[권장안]` 항목은 사용자 검토 대기 (코딩 전 단계. "개발 시작" 지시 전까지 구현하지 않음)
- 표기: `[확정]` = 문서에 확정된 규칙, `[권장안]` = AI 제안(승인 전에는 규칙 아님), `[확인 필요]` = 사용자 답변 필요

---

## 0. 결정 기록

| 항목 | 결정 | 일자 |
|---|---|---|
| A-1 운영환경 | **PoC는 사용자 PC Local Hosting** (`http://localhost:8000`). 실제 운영환경은 PoC 후 재결정 | 2026-11-24 |
| DB | **PostgreSQL** (Local 설치, 운영 전환 시 동일 DB 사용) | 2026-11-24 |
| Backend | Python + Django `[권장안]` (A-1 비교 시 제안, 시스템설계 단계에서 확정) | – |
| e-mail | PoC에서는 실제 발송 대신 화면 로그/파일로 임시 P/W 확인 `[권장안]` | – |
| ① Material Unit | **필수** (다른 Module Unit 비교 기준) | 2026-11-24 |
| ② 사용자 ID | **영문·숫자·`.`·`_`·`-` 허용, 대소문자 구분 없음(소문자로 저장)** | 2026-11-24 |
| ③ Open PO 계산 대상 | **In Transit + Remain Q'ty > 0 인 행** (Remain = 0이어도 운송 중 수량은 포함) | 2026-11-24 |
| ④ OPEN_PO Header | **`PO Date`, `PO No`, `Material Code`, `Unit`, `PO Q'ty`, `Currency`, `Unit Price`, `Cancel`, `G/R`, `In Transit`, `Vendor`** (실제 시트 기준). Unit Price가 없으면 Amount·Remain Amount는 **빈칸** | 2026-11-24 |
| ⑤ 동시 Upload (I-1) | 같은 Module·같은 작업 주차 Upload 진행 중이면 두 번째 시도는 **거절** + "다른 사용자가 Upload 중입니다. 완료 후 다시 시도하세요." | 2026-11-24 |
| ⑤ Excel 안내 시트 | MD 기준으로 갱신 (`표준 업로드 양식_1123.xlsx` → v1124) | 2026-11-24 |

PC 현황(2026-11-24 확인): Python 3.14.6, openpyxl 3.1.5, Git, VS Code 있음 / PostgreSQL, Django 미설치.

---

## A. 공통 기반 기능 (Ⅰ~Ⅴ)

대상: 사용자 계정 DB, Log-in / Log-out, 권한(Master / Admin / User / Guest), Sign up, Main, User Management

### A-1. 업무 목적
- 약 20명 구매 관련 인원(한국 본사 + 베트남 공장)이 본인 계정으로 접속하고, Class(권한등급)에 따라 10개 업무 Module을 조회·관리한다.
- 계정 승인·권한 변경·P/W 초기화는 Master(novamaster) 1명이 관리한다.

### A-2. 입력 Data
| 화면 | 입력 |
|---|---|
| Log-in | ID, Password |
| Sign up | ID, P/W, P/W Again, Name, e-mail, Tel |
| ID Info Pop-up (본인) | Old P/W, New P/W, P/W Again, Name, e-mail, Tel |
| User Management (Master) | Class, ID Status 변경, P/W Reset 실행 |

### A-3. 출력 Data
- Main 화면: 10개 Module 메뉴, 로그인 사용자 ID, (Master만) "※ User Management" 버튼
- User Management 표: Check / Purchaser ID / Name / Class / ID Status / e-mail / Tel (Password는 표시하지 않음)
- 임시 Password 통보 (운영: e-mail / PoC: 로그 `[권장안]`)

### A-4. Field 정의 (사용자 계정)
| Field | 규칙 | 근거 |
|---|---|---|
| ID | 필수, Unique, 영문·숫자·`.`·`_`·`-` 허용, 그 외 특수문자 불가, 앞뒤 공백 제거, 중간 공백 불가. **대소문자 구분 없음(소문자로 저장·비교)**. 수정 불가 | Ⅴ-3-1, 확정 ② |
| Password | 8자 이상, 영문·숫자 각 1자 이상, 특수문자 가능, 공백 불가. **Hash 저장**(평문 금지, 관리자도 조회 불가) | Ⅴ-1-6, Ⅴ-1-7 |
| Name | 필수 `[권장안]`. Master 수정 불가(본인만 ID Info에서 수정) | Ⅴ-3-4, Ⅴ-5 |
| e-mail | 필수 `[권장안]`(P/W Reset 통보에 필요). Master 수정 불가 | Ⅴ-3-5 |
| Tel | 문자열, 국가번호 포함 가능. Master 수정 불가 | Ⅴ-3-6 |
| Class | Master / Admin / User / Guest. Sign up 시 User 고정. Master만 변경 | Ⅴ-1, Ⅴ-3 |
| ID Status | Requested / Approved / Disabled. Sign up 시 Requested. Master만 변경 | Ⅴ-1-5 |
| 임시 P/W 여부 | 시스템 관리. True이면 새 P/W 저장 전 업무 Module 사용 제한 | Ⅴ-1-6 |
| 로그인 실패 횟수 / 잠금 해제 시각 | 시스템 관리. 5회 연속 실패 시 10분 잠금 | Ⅴ-1-7 |
| created_at, updated_at, login_at, password_reset_at | UTC 저장, 사용자 Local Timezone 표시 | Ⅳ-6-4 |

### A-5. Validation Rule
- Sign up: ID 형식·중복("ID check" 버튼 + Save 시 재검사), P/W 규칙, P/W Again 일치, e-mail 형식 `[권장안]`
- Log-in: ID Status = Approved이고 Password 일치할 때만 성공. Requested / Disabled는 P/W가 맞아도 실패
- 잠금 중 메시지: "Log-in 시도 횟수를 초과했습니다. 10분 후 다시 시도하세요."
- 일반 P/W 변경: Old P/W 확인 후 변경

### A-6. 계산 Rule
- 없음. (Current Week 계산은 업무 Module 공통 기능: Asia/Ho_Chi_Minh 기준 ISO Week, 월요일 00:00 전환)

### A-7. CRUD Rule
| 동작 | 누가 | 방법 |
|---|---|---|
| 계정 생성 | 본인 | Sign up (Class=User, Status=Requested) |
| Master 계정 생성 | 시스템 설치 시 1회 | 임시 P/W 발급 → 최초 Log-in 시 변경 강제. 소스코드에 고정 P/W 금지 |
| 조회 | Master | User Management 화면 |
| 수정 | Master: Class, ID Status / 본인: P/W, Name, e-mail, Tel | Row 선택 후 Save |
| P/W Reset | Master | Row 선택 → P/W Reset → 임시 P/W 발급·통보 → 다음 Log-in 시 변경 강제 |
| 삭제 | 없음 | 퇴직자는 ID Status = Disabled |

### A-8. Excel Upload / Download Rule
- 공통 기반 기능에는 Excel Upload·Download 없음.

### A-9. 검색 / Filter Rule
- User Management: 문서에 정의 없음. 20명 규모이므로 PoC에서는 검색 없이 전체 표시 `[권장안]`.

### A-10. 사용자 권한 (Ⅴ-1-4 권한 Matrix)
| 기능 | Master | Admin | User | Guest |
|---|---|---|---|---|
| User Management | 관리 | 불가 | 불가 | 불가 |
| M1·M2 Material·Assy Master | 조회/다운로드 | Upload·화면수정·Save | 조회/다운로드 | 조회/다운로드 |
| M3 BOM | 조회/다운로드 | Upload만 | 조회/다운로드 | 조회/다운로드 |
| M4~M8 | 조회/다운로드 | Upload | 조회/다운로드 | 조회/다운로드 |
| M9·M10 | 조회/다운로드 | 조회/다운로드 | 조회/다운로드 | 조회/다운로드 |
| Recalculate·Weekly Reset | 불가 | 가능(M10 화면) | 불가 | 불가 |
| ID Info(본인 정보 수정) | 가능 | 가능 | 가능 | 가능 |

- 버튼 비활성화만으로 끝내지 않고 **Backend/API에서도 동일하게 차단**한다. (Ⅰ-9)
- 향후 User에게 일부 Module 권한을 줄 수 있도록 "Class → 기능별 권한" 구조로 설계한다. (Ⅴ-1-3)

### A-11. 다른 Module과의 Dependency
- Material Master의 **Purchaser ID**는 사용자 계정 ID를 참조한다. (Status와 무관하게 지정 가능)
- 모든 Upload·Recalculate·Weekly Reset 감사 기록에 사용자 ID가 남는다. (Ⅰ-9)

### A-12. 예외 처리
- 2시간 미사용 → 자동 Log-out. 저장하지 않은 수정내용이 있으면 Log-out 전에 경고.
- 임시 P/W 사용자 → Main 진입 후 ID Info Pop-up 자동 표시, 새 P/W 저장 전 업무 Module 접근 차단(URL 직접 입력 포함).
- Master가 자기 자신을 Disabled로 바꾸거나 Class를 바꾸는 경우: 문서 정의 없음 → **차단** `[권장안]` (Master 1명 운영이라 잠기면 복구 불가).

### A-13. 미결정 사항
- 없음. (ID 규칙 ②, 동시 Upload ⑤ 확정 — 0절 참조)

### A-14. 테스트 Scenario
1. Sign up → Requested 상태로 저장 → Log-in 시도 실패
2. Master가 Approved로 변경·Save → 해당 사용자 Log-in 성공
3. 같은 ID로 5회 연속 실패 → 10분 잠금 메시지 → 10분 후 정상 Log-in → 실패 횟수 초기화
4. Master P/W Reset → 임시 P/W로 Log-in → ID Info Pop-up 자동 표시 → 업무 Module URL 직접 접근 차단 확인
5. Guest 계정으로 Upload API를 직접 호출 → 서버에서 거부
6. Admin/User/Guest로 User Management URL 직접 접근 → 거부
7. Disabled 사용자 Log-in 실패
8. 2시간 무동작 후 자동 Log-out

### A-15. 완료 조건 (Acceptance Criteria)
- Approved만 Log-in 가능, 5회 실패 10분 잠금, 2시간 자동 Log-out
- DB에 평문 Password 없음
- Master만 User Management 버튼이 보이고 접근 가능 (Backend 검증 포함)
- 권한 Matrix대로 버튼 활성/비활성 + Backend 차단
- 임시 P/W 사용자는 새 P/W 저장 전 업무 Module 사용 불가
- 모든 Date/Time UTC 저장, 사용자 Local Timezone 표시

---

## B. Ⅵ-1 Material Master

### B-1. 업무 목적
- Material(구매 자재) 기준정보의 **Single Source of Truth**. Key = Material Code.
- BOM, Inventory, Open PO, Scheduled Receipt, Material Requirement, Material PSI가 Desc., Spec., Unit, L/T, Status를 이 Master에서 가져다 쓴다.

### B-2. 입력 Data
- Excel 시트 `MD_Material` (Admin Upload): Material Code, Desc., Spec., Unit, Purchaser ID, Vendor, Country, L/T(Weeks)
- 화면 수정 (Admin, Row 선택 후 Save): Desc., Spec., Unit, Purchaser, Vendor, Country, L/T(Weeks), Status

### B-3. 출력 Data
- 화면: [체크박스] / No / Mat. Code / Desc. / Spec. / Unit / Purchaser(이름) / Vendor / Country / L/T(Weeks) / Update / Status
- Excel Download / History Download
- 다른 Module의 표시값(계층 2)과 계산 입력값(계층 3)

### B-4. Field 정의
| Field | 필수 | 규칙 | 화면수정(Admin) |
|---|---|---|---|
| Material Code | 필수 | Unique. 앞뒤 공백 제거 + 영문 대문자 변환. 숫자 Code도 문자열. 지수표기 손상 Error | 불가 (신규는 Upload만) |
| Desc. | 선택 | 문자열 | 가능 |
| Spec. | 선택 | 문자열, 특수문자 허용 | 가능 |
| Unit | **필수** (확정 ①) | EA / SHEET / SET / G / KG / MM / M. 대문자 변환. 허용값은 코드 수정 없이 추가 가능한 구조 | 가능 (Dropdown) |
| Purchaser ID | 선택 | 계정에 존재하는 ID. 화면은 Name 표시, Status가 Approved가 아니면 이름 옆 붉은 글씨로 Requested/Disabled | 가능 (사용자 목록) |
| Vendor | 선택 | 자유기재, 여러 Vendor 기재 가능. 다른 Module과 연결 안 함 | 가능 |
| Country | 선택 | 직접입력 | 가능 |
| L/T(Weeks) | 필수 | 1 이상의 정수. 빈 값·0·음수·소수 Error | 가능 |
| Update | 시스템 | 실제 값이 변경된 행만 갱신 `[권장안]`. UTC 저장, Local 표시 | 불가 |
| Status | 시스템 | Active / Inactive. Physical Delete 금지 | 가능 (Dropdown) |
| version | 시스템 | Optimistic Lock용 (화면 비표시) | – |

### B-5. Validation Rule (Upload)
- 시트 `MD_Material` 존재, 1행 Header, 필수 Column(Material Code, Unit, L/T(Weeks)) 존재, 병합 셀 금지
- Unit 빈 값 → Error (확정 ①)
- Material Code 빈 값 / 지수표기 손상 / **Excel 내 중복(정규화 후 2회 이상) → Error, 엑셀 수정 후 재업로드 안내**
- Unit 허용값 외 → Error
- Purchaser ID가 계정에 없음 → Error
- L/T 필수, 1 이상의 정수 → 위반 시 Error
- **Material Code = 'ASSY' → Error** `[권장안 추가]` (Ⅶ-5에서 'ASSY'를 Material Master에 등록 금지로 정했으나 Ⅵ-1 Validation 목록에는 누락)
- 빈 Cell = NULL, "-" = NULL. 정의되지 않은 Column은 무시하고 결과에 안내
- Error가 1건이라도 있으면 전체 반영 중단, Transaction Rollback

### B-6. 계산 Rule
- 자체 계산 없음.
- 영향: L/T → Module 8 Calculated Scheduled Receipt 배치 주차(계층 2 즉시 반영) / Unit → 다른 Module Unit 일치 검사 / Status → 다른 Module Status 표시

### B-7. CRUD Rule
| 동작 | 방법 | 비고 |
|---|---|---|
| Create | Upload Type ① Add 또는 ② Change(없는 Code) | Status = Active. 화면 신규 입력 불가 |
| Read | 모든 Class | Status 필터 기본값 Active |
| Update | Upload ② Change(덮어쓰기 + Active), 화면 Save | 빈 Cell은 NULL로 덮어씀 |
| Inactive | Upload ③ Inactive, 화면 Status 변경 Save | 사용 중인 Code도 허용, 사용 중 건수를 Warning으로 안내 |
| Delete | 없음 | Physical Delete 금지 |

### B-8. Excel Upload Rule
- 순서: Upload → 팝업에서 Type 선택(Add / Change / Inactive) → Confirm → 파일 선택 → Validation 결과 → [반영]
- 반영 전 표시: 신규등록 예정 / 수정 예정(변경 Field) / Inactive 예정 / 무시 예정 / 재활성화 예정 건수
- Type별 검사 범위 `[권장안]`: Add·Change는 파일의 모든 행을 검사, Inactive는 Material Code만 검사 (Ⅵ-1-6 "나머지 Column 값은 무시"에 맞춤)
- Validation 결과 Excel Download 제공 `[권장안]`

### B-9. Excel Download Rule
- 현재 조회조건(Status + 검색조건 + 검색어)의 **전체 Row**
- Column: No, Material Code, Desc., Spec., Unit, Purchaser ID, Purchaser, Vendor, Country, L/T(Weeks), Update, Status
- 그대로 수정해서 재Upload 가능 (No, Update, Status, Purchaser 이름 Column은 Upload 시 무시)
- History Download: 검색 결과 Code의 과거 변경 이력 전체, 기존 Download 양식 + Update(yyyy-mm-dd hh:mm, Local), 이력 시점 값 표시, 팝업 없음

### B-10. 검색 / Filter Rule
- Status: All / Active / Inactive (기본 Active)
- 검색조건: Mat. Code(기본) / Desc. / Purchaser(이름 또는 ID) / Vendor / Country
- 부분일치, 대소문자 무시, Search 클릭 시 실행
- 기본 정렬 Material Code 오름차순. 작업 주차 Dropdown 없음

### B-11. 사용자 권한
- Admin: 조회·검색·Filter·Download·History·Upload·화면수정·Save
- Master / User / Guest: 조회·검색·Filter·Download·History (Save·Upload 비활성 + Backend 차단)

### B-12. 다른 Module과의 Dependency
- 참조함: 사용자 계정(Purchaser ID → Name, Status)
- 참조됨: BOM·Inventory·Open PO·Scheduled Receipt(Unit 일치 검사, Desc./Spec./Status 표시), Scheduled Receipt(L/T), Material Requirement·PSI(Desc./Spec./Unit/Status)
- Master 변경 후 Module 9·10은 Recalculate 전까지 "● Need Recalculation"

### B-13. 예외 처리
- 동시 편집: Optimistic Lock. 충돌 시 "다른 사용자가 먼저 수정했습니다. 최신 Data를 다시 조회합니다." 후 해당 Row 재조회
- Save하지 않은 수정내용이 있는 상태로 화면 이동 → 경고
- **Unit 변경 시 기존 BOM / 주간 Data와 Unit 불일치 → Recalculate에서 Error(F-14)**. Save·Upload 단계에서 "영향받는 BOM n건" Warning을 미리 보여줌 `[권장안]`
- Purchaser ID 사용자가 Disabled여도 지정 유지, 이름 옆 붉은 표기

### B-14. 미결정 사항
- 없음. (Unit 필수 확정 ①)

### B-15. 테스트 Scenario
1. Add: 신규 3건 + 기존 2건 파일 → 신규 3 / 무시 2 표시 → 반영 후 신규 3건 Active
2. Change: 기존 Code 값 변경 + Inactive Code 포함 → 수정 예정·재활성화 예정 표시 → 반영
3. Inactive: 존재 Code 2건 + 없는 Code 1건 → Inactive 2 / 무시 1
4. 'smaz13001'과 'SMAZ13001 '이 같은 파일에 있음 → 중복 Error, 전체 반영 안 됨
5. L/T 0, 1.5, 빈 값 → 각각 Error
6. Unit 'sheet' → 'SHEET'로 저장 / Unit 'BOX' → Error
7. 숫자 Code 4605000219 → 문자열 저장 / 3.04E+11 → Error
8. 두 Admin이 같은 Row를 동시에 수정 → 나중 Save한 쪽에 충돌 안내
9. User 계정으로 Save API 직접 호출 → 거부
10. Status=All, 검색조건 Purchaser='emi' → 해당 Row 전체 Download, History Download

### B-16. 완료 조건
- 문서 Ⅵ-1 [17. Acceptance Criteria] 전체 + 위 'ASSY' 금지 규칙

---

## C. Ⅶ 표준 업로드 양식 vs Ⅵ-1·Ⅲ-4 충돌 검토

`표준 업로드 양식_1123.xlsx`를 열어 실제 시트 Header·예시값과 `00_안내` 시트를 MD와 대조했다.

### C-1. 계산(Ⅲ-4)에 영향을 주는 충돌
| # | 내용 | 영향 |
|---|---|---|
| 1 | **Open PO 판단 기준**: Ⅵ-7·Ⅶ-9는 "Remain Q'ty = 0 행은 Open PO 목록에서 제외", Ⅲ-4-2-1은 "Open PO = In Transit + Remain Q'ty". Remain = 0이고 In Transit > 0인 행(전량 출하, 운송 중)을 제외하면 **운송 중 수량이 PO 과부족과 입고예정 차이분에서 빠진다** | **확정 ③**: In Transit + Remain Q'ty > 0 인 행을 Open PO로 사용 |
| 2 | OPEN_PO 실제 Header는 `Currency`, `Cancel`, `G/R`, `In Transit`인데, Ⅶ-9 본문은 `Curr.`(Upload 순서), `Cancel Q'ty`, `G/R Q'ty`, `In Transit Q'ty`, 안내 시트는 `Received Q'ty`. Header는 "정확히 일치"해야 하므로 하나로 확정 필요 | **확정 ④**: 실제 시트 명칭 사용 |
| 3 | Amount: Ⅵ-7은 Unit Price 없으면 **빈칸**, Ⅶ-9는 **0** | **확정 ④**: 빈칸 |

### C-2. Ⅵ-1(Material Master)과의 충돌·누락
| # | 내용 | 처리 |
|---|---|---|
| 4 | Unit이 MD_Material에서 "선택"(빈 값 허용)인데, BOM·Inventory·Open PO·Scheduled Receipt는 Material Master Unit과 다르면 Error. Master Unit이 비어 있으면 비교 기준이 없음 | **확정 ①**: Unit 필수 |
| 5 | 'ASSY' 금지 Code(Ⅶ-5)가 Ⅵ-1 Validation 목록에 없음 | B-5에 `[권장안]`으로 추가 |
| 6 | Ⅵ-1 [1]의 "다른 Module Data가 Master와 충돌하면 Validation Error" 문장은 Ⅰ-8 예외(No DB 허용)와 상충 | 해석: **Code 미등록·Inactive = Warning, Unit 불일치 = Error** (Ⅳ-7-10 기준 적용) |
| 7 | 예시행 L/T 값이 텍스트 '1'로 저장되어 있음 | 숫자로 변환 가능한 텍스트는 정수로 인정 `[권장안]` |

### C-3. `00_안내` 시트가 구버전(v1029)이라 MD(최신)와 다른 부분
| 안내 시트 내용 | MD 최신 규칙 |
|---|---|
| BOM·SAFETY·RTF·PROD_PLAN·OPEN_PO·SCHED_RECEIPT의 Code는 "Master에 Active로 존재" | Master에 없거나 Inactive여도 Upload 허용, 'No DB' 표시 + Warning (Ⅰ-8) |
| SCHED_RECEIPT 16주(2026-W44 ~ 2027-W06) | 14주 (실제 시트도 14주) |
| BOM은 "3열만, Unit은 자동 표시" | 4열(Unit 필수, Master와 불일치 시 Error), 실제 시트도 4열 |
| INVENTORY Assy 행 Unit "값 있으면 무시" | Assy 행 Unit은 빈칸 또는 'EA'만, 그 외 Error (Ⅵ-5) |
| RTF·PROD_PLAN 설명에 Plan Column 없음 | Plan Column 필수 (실제 시트에는 있음) |
| MD_Assy Header `TYPE` | 실제 시트 Header는 `Type` (Ⅵ-2 본문은 `TYPE`) |
| 예시행에 '문자열', 'EA, SHEET, …', '"Assy"'(따옴표 포함) 같은 설명 문구 | 그대로 Upload하면 Error. 특히 BOM의 `"Assy"`는 따옴표 때문에 Assy 열로 인식 안 됨 |

→ **확정 ⑤: 갱신 완료** (2026-11-24, v1124). 원본은 `표준 업로드 양식_1123_v1029백업.xlsx`로 보관.
갱신 범위: `00_안내` 시트 전체, 각 시트 1행 Header 메모, 입력 제한(데이터 유효성 검사) 오류 수정, BOM 예시행 `"Assy"` → `Assy`.
갱신하지 않은 것: 각 시트 2행 이하의 예시 설명 문구('문자열' 등). 실제 Upload 전에 지우도록 안내 시트에 명시함.

---

## D. [확인 필요] (이번 회차 5개) — **2026-11-24 전부 권장안으로 확정** (결과는 0절)

| # | 질문 | [권장안] |
|---|---|---|
| ① | Material Master의 **Unit을 필수**로 할까요? (빈 값이면 BOM·재고·PO·입고예정의 Unit 비교 기준이 없음) | 필수 |
| ② | Sign up ID 규칙은 "특수문자 불가"인데 화면 예시에 `nana.kang`, `jet.son`이 있습니다. **마침표(.) 등을 허용**할까요? 또한 ID 대소문자를 구분할까요? | 영문·숫자·`.`·`_`·`-` 허용, 대소문자 구분 없음(소문자 저장) |
| ③ | Open PO 계산에 쓰는 행 기준을 **"Remain Q'ty > 0"** 대신 **"In Transit + Remain Q'ty > 0"**으로 바꿀까요? (운송 중 수량 누락 방지) | In Transit + Remain > 0 |
| ④ | OPEN_PO Upload Header를 실제 시트대로 **`Currency`, `Cancel`, `G/R`, `In Transit`**으로 확정하고, Unit Price가 없을 때 Amount는 **빈칸**으로 할까요? | 실제 시트 명칭 + 빈칸 |
| ⑤ | (Ⅷ I-1) 같은 주차 Data를 다른 사람이 Upload 중일 때 두 번째 Upload는 **거절**(메시지 표시)할까요, **대기**할까요? 그리고 Excel 안내 시트를 MD 기준으로 갱신할까요? | 거절 + "다른 사용자가 Upload 중입니다" / 안내 시트 갱신 |
