# 03. Module 1 · Material Master 상세 설계 (DB · 화면 · Upload · History)

- 작성일: 2026-11-24
- 근거: `Prompt 1135.md` Ⅳ-3, Ⅳ-5, Ⅵ-1 (2026-11-24 확정 반영) / `설계/01` B절(Ⅰ-6 확인 항목) / UI 도안 Slide 4
- 상태: **사용자 승인 대기**. 업무 규칙은 설계/01 B절 그대로이며, 이 문서는 "어떻게 만들지"를 정한다.

---

## 1. 이번 Module에서 함께 만드는 공통 부품
Material Master가 처음으로 Excel Upload·Download·History를 쓰는 Module이므로, 다음 공통 부품을 같이 만든다. Module 2~8은 이 부품을 재사용한다.

| 부품 | 역할 | 근거 |
|---|---|---|
| **Excel 읽기 엔진** | 지정 시트만 읽기, 1행 Header 정확 일치(앞뒤 공백 제거), 병합 셀 Error, 수식은 결과값, Code 문자열화·지수표기 Error, 완전 빈 행 무시, `"-"`·빈칸 = NULL, Excel Row 번호 기록 | Ⅳ-5-1 |
| **Upload 기록(감사)** | Upload마다 사용자·시각·Module·파일명·결과·Error/Warning 건수 저장 | Ⅰ-9 |
| **동시 Upload 차단** | 같은 Module Upload가 진행 중이면 두 번째는 거절 + 안내 | H-5 |
| **재계산 필요 표시** | 화면 상단 `Final Calculation: … ● Need Recalculation`. 데이터 변경 시각 > 마지막 재계산 시각이면 빨간 표시 (재계산 기능은 Module 10에서) | Ⅳ-7-2 |
| **Module 화면 틀** | 상단 Module 탭 메뉴, 검색 영역, 버튼(Upload·Download·History), 표 (No·Status 열, 헤더 색: 파랑=Upload 열 / 회색=시스템 열) | Ⅳ-3, PPT |

## 2. DB 설계

### 2-1. `material` (Material Master 현재값)
| Column | 형식 | 규칙 |
|---|---|---|
| id | 숫자 | 내부 번호 |
| material_code | 문자 100, **Unique** | 대문자·앞뒤 공백 제거 저장. 'ASSY' 금지 |
| desc / spec | 문자 (NULL 가능) | |
| unit | 문자, **필수** | `unit_code` 표의 값만 |
| purchaser | 사용자 계정 참조 (NULL 가능) | 계정이 있으면 Status 무관 지정 가능 |
| vendor / country | 문자 (NULL 가능) | |
| lead_time_weeks | 정수 ≥ 1, 필수 | |
| status | ACTIVE / INACTIVE | Physical Delete 없음 |
| updated_at, updated_by | 일시(UTC), 계정 | **값이 실제로 바뀐 경우에만** 갱신 (화면 'Update' 열) |
| created_at, created_by, inactive_at, inactive_by | 일시, 계정 | 감사용 |
| version | 정수 | Optimistic Lock |

### 2-2. `material_history` (변경 이력, History Download용)
- 행이 **새로 생기거나 바뀔 때마다** 바뀐 뒤의 전체 값을 1행씩 복사해 쌓는다. (값 그대로 = "이력 시점 값" F-8)
- Column: material_code, desc, spec, unit, purchaser_id(문자), purchaser_name(당시 이름), vendor, country, lead_time_weeks, status, **change_type**(Add / Change / Inactive / Reactivate / Screen), changed_at, changed_by, upload_batch(있으면)

### 2-3. `unit_code` (Unit 허용값)
- EA, SHEET, SET, G, KG, MM, M을 처음에 넣어 둔다. 허용값 추가는 코드 수정 없이 이 표에 행만 추가. (추가 화면은 이번 범위 아님, Ⅵ-1-4 ④)

### 2-4. `upload_batch` (공통 · Upload 기록)
| Column | 내용 |
|---|---|
| module | 예: M1 |
| upload_type | ADD / CHANGE / INACTIVE (Module 1~3) |
| source_filename, uploaded_by, created_at | |
| state | PREVIEW(검증 완료, 반영 대기) / APPLIED / CANCELLED / FAILED |
| total / new / changed / inactive / skipped / reactivated / error / warning 건수 | |
| preview_rows | 검증 통과한 행 데이터(JSON). [반영] 때 이 내용 그대로 저장 |
| errors | Error·Warning 목록(JSON): 시트명, Excel Row, Code, 항목, 사유 |
| applied_at | |

### 2-5. `system_status` (공통 · 1행)
- data_changed_at, last_calculated_at, last_calculated_by. Module 1~8 저장 시 data_changed_at 갱신.

## 3. 화면 설계 (UI 도안 Slide 4 기준)

```
[ Material Master | Assy Master | BOM | … ]  ← Module 탭 (개발 전 Module은 비활성)
Final Calculation: -  ● Need Recalculation            [Upload] [Download] [History] [Save]
Status [Active ▼]  검색조건 [Mat. Code ▼]  검색어 [______]  [Search]
┌─┬──┬─────────┬─────┬─────┬────┬──────────┬──────┬───────┬──────────┬──────────┬────────┐
│☐│No│Mat. Code│Desc.│Spec.│Unit│Purchaser │Vendor│Country│L/T(Weeks)│Update    │Status  │
└─┴──┴─────────┴─────┴─────┴────┴──────────┴──────┴───────┴──────────┴──────────┴────────┘
  파란 헤더 = Upload 열 / 회색 헤더 = 시스템 열 (No, Update, Status)
```

| 기능 | 동작 |
|---|---|
| 조회 | Status(기본 Active) + 검색조건(Mat. Code / Desc. / Purchaser / Vendor / Country) + 검색어 → Search. 부분일치, 대소문자 무시. Mat. Code 오름차순 |
| 표시 | Purchaser는 이름. 계정 Status가 Approved가 아니면 이름 옆 붉은 글씨 `Requested`/`Disabled`. Inactive는 파란 글씨 |
| 수정 (Admin) | 체크 또는 값 수정 → 해당 행 자동 체크 + 수정 가능 셀 반전 표시. Unit·Status·Purchaser는 Dropdown. **Save = 체크된 행만 저장** |
| 충돌 | 다른 사용자가 먼저 저장했으면 저장 거부 + "다른 사용자가 먼저 수정했습니다. 최신 Data를 다시 조회합니다." + 재조회 |
| 이탈 경고 | 저장 안 한 수정이 있으면 화면 이동·Log-out 전 경고 |
| Upload (Admin) | Upload → 팝업에서 Type(Add/Change/Inactive) 선택 → Confirm → 파일 선택 → Upload → **검증 결과 화면** → [반영] 또는 [취소] |
| 검증 결과 화면 | 총·정상·Error·Warning 건수 / 신규·수정(변경 Field 표시)·Inactive·무시·재활성화 예정 건수 / Error 목록(시트, Row, Code, 항목, 사유). Error가 1건이라도 있으면 [반영] 비활성 |
| Download | 현재 조회조건 전체 행 → `MaterialMaster_YYYYMMDD_HHMM.xlsx`. 열: No, Material Code, Desc., Spec., Unit, Purchaser ID, Purchaser, Vendor, Country, L/T(Weeks), Update, Status. 시트명 `MD_Material` (그대로 수정 후 재Upload 가능) |
| History | 현재 조회 결과 Code들의 전체 변경 이력 → Excel. Download 열 + Update(yyyy-mm-dd hh:mm, 내 Timezone) |
| 비 Admin | Save·Upload 버튼 비활성, 수정 불가. Backend도 거부 |

## 4. Upload 처리 순서 (Transaction)
1. 동시 Upload 확인: 같은 Module에서 처리 중인 Upload가 있으면 거절 (H-5)
2. Excel 읽기 엔진으로 `MD_Material` 시트 읽기 → 형식 Error 수집
3. 업무 검증 (설계/01 B-5): Code 중복·빈값·'ASSY', Unit 필수·허용값, Purchaser ID 존재, L/T 정수 ≥ 1. **Inactive Type은 Code만 검사**
4. DB 현재값과 비교해 신규/수정/Inactive/무시/재활성화 분류, 변경 Field 계산 → `upload_batch`(PREVIEW)에 저장 → 검증 결과 화면
5. [반영] 클릭 시 한 Transaction으로 저장. 중간 오류 시 전체 Rollback. 변경된 행만 Update 시각·version 갱신, History 기록, `system_status.data_changed_at` 갱신
6. 미리보기 후 [반영] 전에 **다른 Admin이 먼저 M1 Upload를 반영했다면 거절** → 다시 Upload 안내 `[권장안]`

## 5. 권한
- Admin: 조회·검색·Download·History·Upload·Save (Status 포함)
- Master·User·Guest: 조회·검색·Download·History. Save·Upload 버튼 비활성 + 서버 거부 (permissions.py의 `upload`, `edit`)

## 6. 테스트 계획
- 설계/01 B-15의 10개 시나리오 + 엔진 검사(시트 없음, Header 누락, 병합 셀, 지수표기, 숫자 Code, 완전 빈 행, '-' = NULL, 정의되지 않은 열 안내)
- 반영 Transaction Rollback, 변경 없는 행의 Update 미갱신, History 기록, 동시 Upload 거절, 권한 거부(Upload·Save API 직접 호출)
- 브라우저: 조회·검색·행 수정·Save·Upload 미리보기·반영·Download·History

## 7. 승인 필요 `[권장안]`
1. **조회 화면은 페이지를 나누지 않고** 전체 행을 한 표에 표시(머리글 고정, 상하·좌우 Scroll). 약 1,000종 규모라 충분히 빠름
2. History Excel에 **'변경 구분'(Add/Change/Inactive/Reactivate/Screen)과 '변경자' 열 추가**
3. 미리보기 후 [반영] 전에 다른 Admin이 먼저 반영하면 **거절 후 재Upload** (4절 6번)
4. **빈 Upload 양식(Template) Download 버튼** 제공 (MD Ⅳ-5-1 권장안)
5. **검증 결과 Excel Download** 제공 (MD Ⅵ-1-7 권장안)
