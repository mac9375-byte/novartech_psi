# 04. Module 2 · Assy Master 확인 항목 및 설계

- 작성일: 2026-11-24
- 근거: `Prompt 1135.md` Ⅵ-2, Ⅳ-3, Ⅳ-5 / UI 도안 Slide 5 / 표준 업로드 양식 `MD_Assy` 시트
- 상태: **사용자 승인 대기**
- Assy Master는 Material Master(Module 1)와 구조가 거의 같다. 이 문서는 **같은 점은 짧게, 다른 점은 자세히** 적는다.

---

## 1. Ⅰ-6 확인 항목

| 항목 | 내용 |
|---|---|
| 업무 목적 | Assy(노바텍이 생산·납품하는 제품) 기준정보 관리. **Key = Customer Code**(고객사 품번). BOM 상위, Safety Stock, Assy 재고, RTF·Production Plan이 이 Code로 연결된다. Single Source of Truth |
| 입력 Data | Excel 시트 `MD_Assy`: Customer Code, Assy Code, Type, Model, Item, Customer, Country / Admin 화면 수정 |
| 출력 Data | 화면 표, Excel Download, History Download, 다른 Module의 Type·Model·Item·Assy Code·Customer 표시값과 Status |
| 계산 Rule | 자체 계산 없음 |
| CRUD | Create = Upload Add/Change(신규) / Update = Upload Change, 화면 Save / Inactive = Upload Inactive, 화면 Status 변경 / **Delete 없음** |
| Upload Rule | Type 3종(Add / Change / Inactive), 미리보기 → [반영], Transaction, Error 1건이면 전체 중단 (Module 1과 동일) |
| Download Rule | 현재 조회조건 전체 행. 그대로 수정 후 재Upload 가능 |
| 검색 / Filter | Status(All / Active / Inactive, 기본 Active) + 검색조건(**Cust. Code**(기본) / Assy Code / Type / Model / Item / Customer / Country) + 검색어 → Search. 부분일치·대소문자 무시. Cust. Code 오름차순 |
| 권한 | Admin: Upload·Save 포함 전체 / Master·User·Guest: 조회·검색·Download·History |
| Dependency | 없음(독립). 이후 BOM·Safety Stock·Inventory·RTF/Prod.가 Customer Code로 참조. Assy Master에 없는 Code는 그 Module에서 'No DB' |
| 예외 처리 | Optimistic Lock 충돌 안내, 저장 전 이동 경고, 동시 Upload 거절, 미리보기 후 다른 사용자 변경 시 반영 거절 (Module 1과 동일) |
| 완료 조건 | Ⅵ-2 [17. Acceptance Criteria] 전체 |

### 1-1. Field 정의
| Field | 필수 | 규칙 | 화면수정(Admin) |
|---|---|---|---|
| Customer Code | 필수 | Unique. 앞뒤 공백 제거 + 영문 대문자. 숫자 Code는 문자열. 지수표기 Error | 불가 (신규는 Upload만) |
| Assy Code | 선택 | **Key 아님, 중복 허용**. 같은 규칙으로 정규화(대문자). 같은 값의 Material Code가 있어도 OK | 가능 |
| Type | 선택 | 제품군 (Shield Magnet, Magnet, Halbah …) 직접입력 | 가능 |
| Model | 선택 | 적용 고객 제품 | 가능 |
| Item | 선택 | 품명 | 가능 |
| Customer | 선택 | 고객사 | 가능 |
| Country | 선택 | 생산법인 소재국가 | 가능 |
| Update | 시스템 | 값이 실제로 바뀐 경우에만 갱신 | 불가 |
| Status | 시스템 | Active / Inactive | 가능 (Dropdown) |

### 1-2. Module 1과 다른 점
| 구분 | Material Master | **Assy Master** |
|---|---|---|
| Key | Material Code | **Customer Code** |
| 필수 Column | Material Code, Unit, L/T | **Customer Code만** |
| Unit / Purchaser / L/T | 있음 | **없음** (Assy Unit은 EA 고정, 표기·검증 없음 F-10) |
| 'ASSY' 금지 | Material Code에 적용 | 해당 없음 |
| 공존 허용 | – | Assy Code = 어떤 Material Code와 같아도 Error 아님 |

## 2. 구현 방식 `[권장안]`
- Module 1의 Upload·화면 수정·Download·History 처리에서 **Master Data 공통 부분(Code 정규화·중복 검사, 미리보기 분류, 반영 Transaction, Optimistic Lock 저장, History 기록)을 공통 코드로 묶고**, Module 1과 2는 "어떤 Column이 있고 어떻게 검사하는지"만 각자 정의한다.
- 이유: 두 Module의 규칙이 같으므로, 한 곳만 고치면 둘 다 맞게 된다. Module 1의 기존 테스트 21개를 그대로 다시 통과하는지로 안전성을 확인한다.
- DB: `assy`(현재값), `assy_history`(변경 이력) 2개 표 추가. 구조는 Material과 같은 방식(UTC 시각, version, inactive_at/by).
- 화면 URL: `/assy-master/`. Main과 상단 탭에서 "2. Assy Master" 활성화.

## 3. 테스트 계획
- Ⅵ-2 Acceptance Criteria 각 항목 (Customer Code 중복 차단, Assy Code 중복 허용, Material Code와 같은 Assy Code 허용, 숫자 Code, Inactive 범위, Status 필터, 부분검색, Download 재Upload, Rollback, 권한)
- Module 1 기존 테스트 전체 재통과 (공통화 회귀 확인)
- 브라우저: 조회·수정·Save·Upload 미리보기·반영

## 4. [확인 필요] (3개)
| # | 내용 | [권장안] |
|---|---|---|
| ① | Upload Header 명칭이 MD Ⅵ-2 본문은 **`TYPE`**, 실제 양식 시트·Download 목록·안내 시트(v1124)는 **`Type`**입니다. Header는 정확히 일치해야 하므로 하나로 정해야 합니다. | **`Type`** (실제 시트 기준, MD 본문도 `Type`으로 정정) |
| ② | Download Column 목록(Ⅵ-2-13)에는 **No 열이 없고**, 화면 구성(Ⅵ-2-3-1)에는 있습니다. | Module 1과 같이 **No 포함** (Upload 시 무시) |
| ③ | Module 1에서 승인한 방식을 Assy Master에도 같게 적용: History Excel의 **변경 구분·변경자 열**, **빈 양식(Template) Download**, **미리보기 후 다른 사용자 변경 시 반영 거절**, **조회 화면 페이지 나누기 없음** | 동일 적용 |
