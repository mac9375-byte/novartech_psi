# 05. Module 3~10 구현 기록 및 적용한 권장안

- 작성일: 2026-11-24
- 배경: 사용자 지시 "다음 모듈부터 끝까지 개발 완료" (2026-11-24). Module별 사전 승인 단계를 생략하고 `Prompt 1135.md`의 확정 규칙대로 구현했다.
- MD에 없어서 AI가 정한 부분은 아래 **[권장안 적용]**에 모두 적었다. **사용자 검토가 필요하다.** 바꾸고 싶은 항목은 번호로 알려주면 수정한다.

---

## 1. 구현 범위

| Module | URL | 주요 기능 |
|---|---|---|
| 3 BOM | `/bom/` | Upload Add/Change, Assy 열 블록 검사(연속·Assy 열 시작·중복), 분수 소요원수, Unit 불일치 Error, No DB Warning, 현재 BOM 조회(Assy 행 강조), Download, History(모든 버전) |
| 4 Safety Stock | `/safety-stock/` | 전체교체 Upload, 0 이상 정수, 추가·변경·삭제 History, Status 필터(No DB 포함) |
| 5 Inventory | `/inventory/` | 작업 주차 전체교체, Category+Code, Material Unit 검사, Assy Unit 빈칸/EA, 소수 6자리 |
| 6 RTF/Production | `/rtf-production/` | RTF·PROD_PLAN 시트별 교체, 14주 Header 검사, 정수, 자동 생성(규칙 A·B), 14주차 Safety 합산 표시, No BOM 표시 |
| 7 Open PO | `/open-po/` | Final PO·Remain·Amount 계산, Remain 음수 Error, Currency 규칙, 입고예정과 교차 점검 |
| 8 Scheduled Receipt | `/scheduled-receipt/` | Material+Vendor 중복 Error, Open PO 초과 Error, Calculated 입고예정(파랑, L/T 배치, W+13 초과는 W+13) |
| 9 Material Requirement | `/material-requirement/` | Total 행 + Assy 행, RTF/Prod. 분리, 14주차 Safety, 화면 소수 2자리·Download 10자리 |
| 10 Material PSI | `/material-psi/` | 4행(Requirement / Scheduled Receipt / Inventory Balance / PO Balance), 음수 강조, **Recalculate**, **Weekly Reset**, 작업 기록 Download |

공통: 작업 주차 Dropdown(Current Week ~ 지난 16주, 'W48(W0)' 표기), 과거 주차는 조회·Download만, Upload 미리보기 → [반영], 동시 Upload 거절, 감사 기록(Upload·Recalculate·Weekly Reset), Backend 권한 검사.

### 계산 확인 (브라우저 예시 데이터)
- RTF 기초재고 = Material 재고 5,000 + Assy 재고 500 × 소요원수 2 = **6,000**
- 재고 과부족 W0 = 6,000 + 입고예정 3,000 − 소요량 1,000 = **8,000**
- PO 과부족 W0 = 6,000 + Open PO 20,000 − 1,000 = **25,000**
- Open PO Amount = 50,000 × 0.7501 = **37,505**, Remain Amount = 15,000 × 0.7501 = **11,251.5** (PPT 예시와 일치)

## 2. [권장안 적용] — 사용자 검토 필요

| # | 내용 | 적용한 방식 | 이유 |
|---|---|---|---|
| P-1 | BOM·재고·PO·입고예정에서 **Material Master에 없는(No DB) 자재의 Unit** | 허용 Unit 목록(EA, SHEET …)에 있어야 함. 아니면 Error | Master가 없으면 비교 기준이 없어 오타를 막을 최소 장치 |
| P-2 | **Material + Vendor 비교 방식** (Open PO ↔ 입고예정) | Vendor 앞뒤 공백 제거 + 대소문자 무시 (`yx` = `YX`) | 같은 업체가 표기 차이로 분리되는 것 방지 |
| P-3 | Module 9·10 화면의 Desc./Spec./Type/Model/Status | **조회 시점 최신 Master 값** 표시 (계층 2). 과거 주차 Snapshot도 숫자는 당시 값, 설명 문구는 최신 값 | MD Ⅳ-7-0 계층 2 규칙 |
| P-4 | BOM History | 현재 BOM 포함 **모든 버전**을 Update 순으로, 'Version' 열(Current / History)과 변경자 표시 | 현재와 과거를 한 파일에서 비교 가능 |
| P-5 | BOM·RTF·Open PO·입고예정 Download Header | Upload Header 명칭 그대로 (예: `Customer Code`, `Material Code`) — 그대로 재Upload 가능 | 약어 규칙상 Upload Header는 약어 금지 |
| P-6 | Safety Stock History | 'Customer Code, Safety Q'ty, Update, 변경 구분(Add/Change/Delete), 변경자'. Status=All·검색어 없음이면 삭제된 Code 이력도 포함 | MD Ⅵ-4-11 + Module 1·2와 같은 변경자 열 |
| P-7 | Weekly Module(5~8) **빈 양식(Template) Download** | 이번 작업 주차 Header(YYYY-Www 14개)가 채워진 빈 양식 제공 (Admin) | 매주 주차 Header를 손으로 바꾸는 실수 방지 |
| P-8 | 미리보기 후 반영 전 변경 | 같은 주차에 같은 Module(또는 Open PO↔입고예정)이 먼저 반영되었거나 Weekly Reset이 실행되면 반영 거절, 작업 주차가 바뀐 경우도 거절 | Module 1·2와 같은 원칙 |
| P-9 | Recalculate 결과 표시 | 성공: "2026-W48 재계산이 완료되었습니다. 영향 Module: …" + 완료 시각 + Warning 수 / 실패: Error 내용, 기존 결과 유지. 상세 Error·Warning은 **'Operation log' Excel** | MD Ⅳ-7-8 |
| P-10 | Safety Stock에만 있고 BOM도 없는 Code | 규칙 B로 RTF(14주차 Safety)·Prod.(0) 자동 생성 후, RTF 소요량이 있으므로 **BOM 미등록 건수에 포함** | Ⅲ-4-3 규칙의 문자 그대로 적용 |
| P-11 | PSI 'Open PO' 셀 | 마우스를 올리면 PO No · PO Date · Open 수량 표시. 입고예정 셀은 Manual / Calculated 구성 표시 | MD Ⅶ-11 |
| P-12 | Recalculate 확인 창 | "Unsaved screen changes are not included" 확인 후 실행 | MD Ⅳ-7-1 경고 문구 |

## 3. 구현하지 않은 것 / 한계
- **Material·Assy Inactive Upload 시 '다른 Module에서 사용 중' Warning 목록** (Ⅵ-1-10): Inactive 전환은 허용되며 계산 시 Warning으로는 표시되지만, Upload 미리보기에서 사용 중 건수를 따로 보여주지는 않는다.
- Main·업무 화면의 **임시 P/W Pop-up은 별도 화면**(대화상자 모양)으로 구현 (모달 아님).
- 실제 e-mail 발송 없음 (PoC: 실행 터미널 출력).
- 화면에서 **실제 파일을 골라 Upload**하는 동작은 브라우저 도구 제약으로 자동 확인하지 못했다 (같은 처리를 테스트와 서버 측 실행으로 확인).
- 약 1,000 Material 규모 실데이터로 속도 확인은 하지 않았다.
- v1.0 범위 외: 발주필요수량, MOQ, 자재 안전재고, 발주 제안 (Ⅰ-5). 계산 엔진은 단계별 함수로 나눠 추가할 수 있게 했다 (`psi/engine.py`).
