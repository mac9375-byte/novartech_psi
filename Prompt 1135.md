[표기 규칙: 약어] (수정 파일 확정)

긴 단어는 화면·설명 표기에 약어를 사용한다. 
단, Excel Upload Header 및 Column명은 Ⅶ에 정의된 명칭과 정확히 일치해야 하므로 약어로 바꾸지 않는다.

Customer Code → Cust. Code
Material Code → Mat. Code
Description → Desc.
Specification → Spec.
Lead Time → L/T
Quantity → Q'ty
Currency → Curr.
Production Plan → Prod.
Return to forecast → RTF
Good Receipt → G/R

너는 제조업 구매SCM 및 자재관리 시스템 구축 전문가이자
Full-stack 소프트웨어 아키텍트이다.
나는 휴대폰/태블릿PC용 자석부품을 공급하는 협력사
'㈜노바텍'에서 20년 이상 구매업무를 수행한 구매전문가이며,
현재 Excel로 수행하고 있는 재고 과부족 점검, 발주량 결정 등
구매SCM(조달구매) 업무를 Web 기반 시스템으로 구현하고자 한다.
나는 프로그래밍 경험이 거의 없는 초보자이다.
따라서 AI는 복잡한 기술적인 내용을 한꺼번에 설명하거나
바로 Coding을 시작하지 말고 아래 순서에 따라 단계적으로 진행한다.
업무정의
→ 데이터구조
→ 업무규칙 및 Validation
→ 시스템설계
→ 화면설계
→ DB설계
→ API/Backend 설계
→ UI 개발
→ 테스트
→ 배포
각 단계에서는 전문용어가 필요한 경우
초보자도 이해할 수 있도록 간단한 설명을 함께 제공한다.

본 요구사항 문서는 다음과 같이 큰 단락을 구분한다.
예:
Ⅰ
Ⅱ
Ⅲ
Ⅳ
Ⅴ-1
Ⅴ-2
Ⅴ-3
Ⅴ-4
Ⅴ-5
Ⅵ-1
Ⅵ-2
...
Ⅶ
Ⅷ
────────────────────
Ⅰ. AI 개발 진행 원칙
────────────────────
이 프로젝트에서는 AI가 사용자의 업무를 임의로 추정하여
기능이나 업무규칙을 만들어서는 안 된다.
AI는 반드시 사용자가 정의한 업무 요구사항을 기준으로 시스템을 설계한다.
[1. 전체 개발 순서]
먼저 시스템 공통 기반 기능을 구축하고,
그 이후 10개의 업무 기능 Module을 순차적으로 개발한다.
공통 시스템 기반 기능:
사용자 계정 DB
Log-in / Log-out
사용자 권한(Master / Admin / User / Guest)
Sign up
Main Navigation
User Management
업무 기능 개발 순서:
Material Master
Assy Master
BOM
Safety Stock
Inventory
RTF/Production Plan
Open PO
Scheduled Receipt
Material Requirement
Material PSI
한꺼번에 여러 업무 Module을 개발하지 않는다.
현재 개발 중인 Module을
요구사항 확인
→ 미결정 사항 확인
→ 설계
→ 사용자 검토/승인
→ 개발
→ 테스트
→ 완료 확인
순서로 완료한 후 다음 Module로 이동한다.
[2. 단계 진행 원칙]
내가 명시적으로
"개발 시작"
"다음 단계 진행"
"다음 모듈 진행"
등의 지시를 하기 전에는
AI가 임의로 다음 개발 단계나 다음 Module로 넘어가지 않는다.
[3. 미결정 사항 처리]
내가 정의하지 않은 업무규칙을 AI가 임의로 결정하지 않는다.
추가 결정이 필요한 사항이 발견되면 반드시
[확인 필요]
항목으로 정리하여 사용자에게 질문한다.
일반적인 Software Engineering 관점에서
더 안전하거나 유지보수에 유리한 방법이 있다면
[권장안]
으로 제안할 수 있다.
사용자의 승인 전에는 권장안을
확정된 업무규칙으로 간주하지 않는다.

[4. 화면 이미지 사용 원칙]
첨부한 화면 이미지는 UI/UX 및 화면배치 참고자료이다.
첨부 이미지에는 빨간색(#FF0000) 화살표와 설명글을 사용하여
화면 기능을 설명한 부분이 있다.
이 빨간색 화살표와 설명글은 실제 시스템 UI에 구현하지 않는다.
화면 이미지와 Text 요구사항이 충돌하는 경우
AI가 임의로 둘 중 하나를 선택하지 않는다.
충돌 내용을 사용자에게 설명하고 확인받은 후 구현한다.
[5. 확장성]
현재 개발 중인 Module 외의 기능을 동시에 구현하지 않는다.
단, 향후 다른 Module이나 추가 기능을 연결할 수 있도록
DB, Backend, UI 구조는 확장 가능한 구조로 설계한다.
v1.0 범위 외 항목(2026-11 확정): 자재 단위 안전재고, MOQ(최소발주수량), 발주필요수량 계산, 발주 제안 기능은 이번 버전에 포함하지 않는다.
다만 다음 버전에서 추가할 수 있도록 다음을 미리 확보한다.
  (a) Material Master에 안전재고, MOQ 등 속성 필드를 추가할 수 있는 구조
  (b) PSI 계산 엔진(Module 9~10)에 발주 계산 단계를 추가할 수 있도록 계산 단계를 분리한 구조
  (c) 발주 제안 결과를 저장할 별도 Module을 추가할 수 있는 구조 (DB 테이블과 API 분리)
[6. 각 Module 개발 전 확인 항목]
각 Module 개발 전에 최소 다음 내용을 먼저 정리하여
사용자에게 보여준다.
업무 목적
입력 Data
출력 Data
Field 정의
Validation Rule
계산 Rule
CRUD Rule
Excel Upload Rule
Excel Download Rule
검색 / Filter Rule
사용자 권한
다른 Module과의 Dependency
예외 처리
미결정 사항
테스트 Scenario
완료 조건(Acceptance Criteria)
[7. 계산 Logic]
모든 계산식과 데이터 처리 Rule은
Code 내부에 암묵적으로 구현하지 않는다.
먼저 사람이 읽고 이해할 수 있는 업무규칙과 계산식으로 설명한 후
사용자의 확인을 받고 Coding한다.
[8. 데이터 정합성]
시스템의 데이터 정합성을 최우선으로 한다.
특히 다음 Module은 서로 Code를 기준으로 연결된다.
Material Master
Assy Master
BOM
Safety Stock
Inventory
RTF/Production
Open PO
Scheduled Receipt

다른 Module에서 사용하는 Assy의 Customer Code 또는 Material Code가
Master Data에 존재하지 않는 경우
AI나 시스템이 임의로 새로운 Code를 생성해서는 안 된다.
[예외 (2026-11 확정)] Master Data에 없는 Code가 포함된 Upload는 허용한다. 해당 Code는 화면에 Status 'No DB'로 표시하고 계산에 포함하되, Warning 목록으로 사후 보고한다. 이 경우에도 시스템이 Master Data를 자동 생성하지는 않는다. (Ⅳ-7-10)

모든 모듈의 우측에 'Status' Column을 두고 
Assy의 Customer Code 또는 Material Code가 Master에 없는 경우 'No DB'
존재할 경우 'Active' 또는 'Inactive'를 표기하도록 한다. 

모든 모듈의 upload에서 
Assy의 Customer Code 또는 Material Code가 Master에 없는 경우나 'Inactive'라고해도 
정상적으로 upload가 진행되고 Error가 나지 않도록 한다. 



[9. 권한 보안]
사용자 권한은 단순히 화면에서 Button을 숨기는 방식으로만
구현해서는 안 된다.
Frontend와 별개로 Backend/API에서도
반드시 사용자 권한을 확인한다.
권한이 없는 사용자가 URL이나 API를 직접 호출하더라도
Upload
수정
저장
삭제
User Management
Weekly Reset(추가)
Recalculate(추가)
등의 기능을 수행할 수 없어야 한다.

감사 기록 원칙: 업로드, 재계산, Weekly Reset 실행 시 사용자 ID, 실행 시각, 대상 Module, 결과(성공·실패, Error·Warning 건수)를 기록한다.

[10. Timezone]
시스템의 Weekly 업무 기준 Timezone은
Asia/Ho_Chi_Minh (UTC+7)를 Default Business Timezone으로 사용한다.
Date/Time은 DB에 UTC로 저장하고,
화면 표시 시 사용자 Local Timezone으로 변환한다.
단, ISO Current Week의 판단은 사용자 Local Timezone이 아니라
베트남 Business Timezone을 기준으로 한다.
[11. 동시 편집(Concurrency) 처리]
화면 수정은 Optimistic Lock 방식을 사용한다. (확정)
Optimistic Lock
여러 사용자가 동시에 같은 Row를 편집할 수 있다.
각 Row에 version 필드를 둔다.
Save 시점에 조회 당시의 version과 DB의 현재 version을 비교한다.
다르면 저장하지 않고
"다른 사용자가 먼저 수정했습니다. 최신 Data를 다시 조회합니다."
메시지를 표시한 후 해당 Row를 다시 조회한다.
Pessimistic Lock(Row 선택 시 잠금)은 사용하지 않는다.
Excel Upload의 동시성
같은 주차 데이터 동시 Upload 차단
같은 Module·같은 작업 주차의 Upload가 진행 중이면 두 번째 시도는 거절하고 "다른 사용자가 Upload 중입니다. 완료 후 다시 시도하세요." 메시지를 표시한다. (2026-11-24 확정, I-1)

────────────────────
Ⅱ. 회사 및 업무 배경
────────────────────
'㈜노바텍'은 약 100여 종의 자석 관련 부품을
가공/조립하여 휴대폰 제조사에 납품하고 있다.
노바텍에서는 다음 용어를 사용한다.

Assy:
노바텍이 생산하여 고객사에 납품하는 제품 또는 조립품.

Material:
Assy를 생산하기 위해
노바텍이 외부 협력사로부터 구매하는 자재.

Customer Code:
고객사가 부여한 Assy의 품번.
본 시스템에서 Assy를 식별하는 기준 Key이다.
고객사의 FCST, RTF, Production Plan, BOM, Safety Stock, Assy 재고는
모두 Customer Code로 Assy를 식별한다.

Assy Code:
노바텍 내부에서 BOM을 기준으로 Assy를 관리하는 코드체계.  
같은(동일한 BOM) Assy Code를 서로 다른 고객사에 납품할 경우 Customer Code가 달라질 수 있음 
본 시스템에서는 Key가 아니라 참고 속성으로 관리한다.

Material Code:
Material을 식별하는 기준 Key.

Material 재고 / Assy 재고:
Material 재고 = 아직 Assy로 가공·조립되지 않은 자재의 재고 (Material 단위)
Assy 재고 = 완성된 Assy의 재고 (Assy 단위, Customer Code 기준)

노바텍 구매팀은 약 20명이며
한국 본사와 베트남 공장에서 근무하고 있다.
구매팀이 관리하는 Material은 약 1,000여 종이다.
현재 구매SCM 업무는 별도의 통합 시스템 없이
여러 개의 Excel File을 이용하여 관리하고 있다.
이번 시스템 구축의 목적은 기존 Excel 중심 업무를 시스템화하여
다음 효과를 얻는 것이다.
생산계획 기반 자재소요량 자동 산출
재고 / 입고예정 / Open PO 통합관리
향후 14주간 재고 과부족 분석
자재 부족 조기경보
구매담당자별 업무관리
구매 의사결정 지원
Excel 수작업 최소화
본 시스템의 이름은 우선
"Material PSI 분석 도우미"
또는
"구매SCM 관리 시스템"
으로 사용하며,
최종 명칭은 추후 변경할 수 있다.
────────────────────

Ⅲ. 생산계획 및 구매업무 프로세스
────────────────────
휴대폰 제조사는 매주 수요일
노바텍에 각 Assy별 향후 14주 FCST를 Excel로 제공한다.
[1. RTF]
노바텍 생산관리팀은 목요일
고객사의 주별 FCST를 기준으로
공급 가능 여부를 검토하여 RTF를 작성한다.
RTF:
Return to Forecast의 약자.
주별 FCST에 대해 협력사가 검토한 공급계획을 의미한다.
노바텍 관점에서는 출하계획이고,
휴대폰 제조사 관점에서는 납품계획이다.
[2. Production Plan]
노바텍 생산관리팀은 금요일
최종 RTF를 기준으로 설비 Capa 등 생산 제약조건을 반영하여
주별 Production Plan을 수립한다.
생산관리팀은
RTF
Production Plan
을 하나의 Excel File로 작성하여
회사 게시판에 등록한다.

[3. 구매팀의 주간 업무]
다음 주 월요일 구매팀은 생산관리팀의
RTF
Production Plan
을 기준으로 Material Requirement를 산출한다.
이후
Inventory
Scheduled Receipt
Material Requirement
를 기본으로 검토하고,
Open PO 정보와 Lead Time 등을 추가로 확인하여
향후 14주 Material 과부족과 신규 발주 필요수량을 판단한다.

필요한 경우:
기존 Open PO의 입고예정일 조정
신규 PO 발주
긴급 발주
등을 수행한다.
구매팀은 원칙적으로 매주 월요일 정기발주를 수행하며,
그 이후에는 특별한 사유가 있는 경우에만 긴급발주를 진행한다.
Open PO:
이미 구매발주한 PO 중
아직 입고되지 않은 잔량을 의미한다.

[상대 주차 표기 (W±ww)] 
작업 주차(당주)는 'W0' 주차로 표기하고, 1주 전은 W-1, 차주는 W+1로 표기한다.
예) 작업 주차 44주인 경우:
2026년 W42(W-2), W43(W-1), W44(W0), W45(W+1), W46(W+2), W47(W+3), W48(W+4), W49(W+5), W50(W+6), W51(W+7), W52(W+8), W53(W+9), 2027년 W01(W+10), W02(W+11), W03(W+12), W04(W+13)
생산계획/PSI를 14주 관리한다는 의미는 W0~W+13까지 데이터를 입력하고 계산한다는 의미이다.
화면 표기는 'W44(W0)'처럼 주차와 상대 주차를 병기한다. 업로드 Header와 DB 주차는 YYYY-Www 형식을 유지한다. (2026-11 확정, 권장안 채택)


[4. Material Requirement]
Material Requirement는
Assy의 RTF 또는 Production Plan과 BOM을 이용하여 산출한다.
기본 계산:
Material Requirement
= Σ(Assy 주별 계획수량×해당 Assy BOM의 Material 소요원수)
소요원수:
Assy 1개를 생산하는 데 필요한
특정 Material의 사용수량을 의미한다.
[4-1. 두 가지 계산 기준]
Material Requirement와 Material PSI는
다음 두 기준으로 각각 계산하여 모두 제공한다.
두 결과를 하나로 합치거나
둘 중 하나만 자동 선택하지 않는다.

① RTF 기준 (출하계획 기준)
소요량:
RTF 기준 Material Requirement(주별)
Σ( Assy RTF 주별수량 × BOM 소요원수 )
RTF 기준은 작업 주차(1주차)부터 14주이다. (확정)

1~13주차는 업로드된 RTF 수량을 그대로 사용한다.
14주차는 업로드된 RTF 수량(공백은 0)과 Safety Stock 소요량을 합산한다. (확정)

Safety 열 소요량
Σ( Assy Safety Stock 수량 × BOM 소요원수 )
Safety 소요량은 14번째(마지막) 주차 소요량에 합산되어 표시되며,
RTF 기준 과부족 계산에서 마지막 주의 소요량처럼 차감한다.
Production Plan 기준에는 Safety Stock을 반영하지 않는다.
(Production Plan 기준도 작업 주차부터 14주)

과부족 판단의 기초재고:
Material 재고 + Assy 재고
를 합계한 수량을 기준으로 과부족을 계산한다.

Assy 재고는 Assy 단위이므로
Material 수량으로 환산하여 Material 재고와 합산한다.
Assy 재고의 Material 환산수량
Σ( Assy 재고 × 해당 Assy BOM의 Material 소요원수 )
예:
Material M 재고 = 5,000
Assy A 재고 = 1,000 (Assy A의 Material M 소요원수 = 2)
RTF 기준 기초재고(Material M)
= 5,000 + 1,000 × 2
= 7,000
위 환산 방식은 사용자가 확인한 확정 규칙이다.
하나의 Assy BOM에 같은 Material이 여러 행이면
모든 행의 소요원수를 합산하여 환산한다.

② Production Plan 기준 (VN PLAN, 생산계획 기준)
소요량:
Production Plan 기준 Material Requirement(주별)
Σ( Assy Production Plan 주별수량 × BOM 소요원수 )
과부족 판단의 기초재고:
Material 재고만 반영한다.
Assy 재고는 반영하지 않는다.
(생산계획에는 Assy 재고가 이미 고려되어 있기 때문이다.)


[4-2. 주별 과부족의 기본 구조]
두 기준 모두 다음 구조를 기본으로 한다.
기초재고
Scheduled Receipt(주별)
Material Requirement(주별)
= 해당 주 기말재고 (다음 주 기초재고)
이 기말재고를 "재고 과부족(Inventory Balance)"이라 한다.
(입고예정 주차를 반영한 시점별 과부족)


[4-2-1. PO 과부족] (확정)
두 기준 모두 재고 과부족과 함께 "PO 과부족"을 주별로 계산한다.
PO 과부족(주별)

기초재고
해당 Material의 Open PO 전체 (Open PO = In Transit + Remain Q'ty, 입고 주차와 무관하게 전량)
작업 주차부터 해당 주까지의 누적 Material Requirement
Open PO(= In Transit + Remain Q'ty)는 Ⅶ-9의 Open 판단을 따른다. In Transit + Remain Q'ty > 0 인 행을 Open PO로 사용한다. (Remain Q'ty = 0이어도 In Transit > 0이면 포함, Remain Q'ty < 0은 Error) (2026-11-24 확정)

해당 Material의 1주차(W0주차) 재고에 Open PO를 합산하고 주차별로 Material Requirement를 차감하는 형태로 PO Balance를 표기한다. 

PO 과부족이 마이너스(PO Balance < 0) 인 주차부터 이미 발주한 수량으로도 부족하다는 뜻이며,
신규 발주가 필요하다는 신호로 표시한다.
재고 과부족은 마이너스이지만 PO 과부족은 플러스이면
수량은 발주되어 있으나 입고 시점이 늦다는 뜻이다. (납기 당김 검토 대상)


[4-3. BOM이 없는 Assy]

RTF 또는 Production Plan 수량이 0보다 큰데
BOM이 등록되지 않은 Assy가 있으면:
해당 Assy의 소요량은 0으로 간주하여 나머지 Assy와 함께 계산하되, 반드시 Warning 목록으로 표시한다. (2026-11 확정, 권장안 채택)

모듈 6(RTF/Production Plan)의 'No BOM' Column에 'NO'로 표시하고, Admin이 BOM을 추가 등록하도록 Warning을 표시한다. Recalculate 결과에 'BOM 미등록 n건'을 함께 표시한다. 
(Customer Code, 주차별 계획수량)
Material Requirement, Material PSI 화면 상단에
"BOM 미등록 Assy n건 – 소요량 0 간주 (Warning)" 경고를 표시한다.
이 경우는 Ⅳ-7-1의 "Validation Error 시 갱신 중단" 규칙의 예외이다.

[v1.0 범위 외, 확장 구조만 확보 (Ⅰ-5, C-3)]
발주필요수량의 계산식 (L/T, 안전재고, MOQ 등 반영 여부)
이번 구매SCM 시스템의 핵심 목적은
매주 월요일 구매팀이 수행하는
RTF / Production Plan
→ Material Requirement
→ Inventory
→ Scheduled Receipt
→ Material PSI
→ 구매 의사결정
과정을 시스템화하는 것이다.


────────────────────
Ⅳ. 시스템 구성
────────────────────
시스템은 크게
4개의 시스템 관리 화면
10개의 업무 기능 Module
로 구성한다.
[1. 시스템 관리 화면]
Log-in
시스템 URL 접속 시 최초 화면
첨부 '스크린샷 Login01.png' 참조
Sign up
신규 사용자 등록 화면
첨부 '스크린샷 Sign up01.png' 참조
Main
Log-in 성공 후 이동하는 Main Navigation 화면
첨부 '스크린샷 Main 01.png' 참조
User Management
Master 권한 사용자 전용 사용자 관리 화면
첨부 '스크린샷 User Management 01.png' 참조
[2. 업무 기능 Module]
Material Master
첨부 '스크린샷 01.png' 참조
Assy Master
첨부 '스크린샷 02.png' 참조
BOM
첨부 '스크린샷 03.png' 참조
Safety Stock
첨부 '스크린샷 04.png' 참조
Inventory
첨부 '스크린샷 05.png' 참조
RTF/Production Plan
첨부 '스크린샷 06.png' 참조
Open PO
첨부 '스크린샷 07.png' 참조
Scheduled Receipt
첨부 '스크린샷 08.png' 참조
Material Requirement
첨부 '스크린샷 09.png' 참조
Material PSI
첨부 '스크린샷 10.png' 참조

[3. 공통 화면 기능]
모든 업무 Module은 기본적으로 Table 형태의 Data를 보여준다.
필요에 따라 다음 기능을 제공한다.
상하 Scroll / 좌우 Scroll / 검색 / Filter / Excel Download / History Download / 작업 주차 선택(5~10번 Module)

[3-0. 화면 수정 범위] (수정 파일 확정)
모듈 1~2 (Material Master, Assy Master): Row 선택 Column(체크박스)과 Save 버튼을 유지한다. Admin만 수정·저장할 수 있다.

모듈 3~10: Save 버튼과 Row 선택 Column을 두지 않는다. 화면 수정 기능이 없다.

모든 모듈: Delete 버튼 및 관련 기능을 두지 않는다. Inactive 처리는 모듈 1~2의 Status 변경(Save) 또는 Excel Upload Type ③으로만 한다.

모든 모듈: '새로고침' 버튼 및 관련 기능을 두지 않는다. 재계산은 모듈 10 화면의 Recalculate 버튼으로만 실행한다. (Ⅳ-7)

버튼 활성화: Admin은 Upload 및 (모듈 1~2) Save가 활성화된다. Master, User, Guest는 Save·Upload 버튼이 비활성화되며 조회 및 Download만 가능하다.

[3-1. 화면 공통 반영 사항]
Status 열: 모든 모듈 화면 우측에 Status 열을 둔다.
           모듈 1~2(Master Data)에는 (Active / Inactive), 모듈 3~10 모듈에는 (Active / Inactive / No DB)를 표기한다. 
           'No DB'는 Master Data에 등록되지 않은 경우를 뜻한다. 

Status 필터: Material Master, Assy Master는 상단에 Status 드롭다운(All / Active / Inactive, 기본값 Active)을 두고, BOM과 Safety Stock은 Status 드롭다운(All / Active / Inactive / No DB, 기본값 Active)을 둔다. 검색조건·검색어와 함께 Search 클릭 시 실행한다. (2026-11 추가, M4-3)
 검색조건·검색어와 함께 Search 클릭 시 실행한다.

RTF/Production Plan은 Plan 드롭다운(All / RTF / Prod., 기본값 All. / Prod. = Production Plan의 약칭)과 검색조건·검색어를 함께 두고 Search 클릭 시 실행한다.

History Download: Material Master, Assy Master, Safety Stock, BOM 화면에 History 버튼을 둔다. 

화면 검색 결과(Status·검색조건·검색어)에 해당하는 Code(또는 Assy)의 과거 변경 이력을 Excel로 다운로드하며, 기존 Download 양식을 따르고 Update(yyyy-mm-dd hh:mm, 사용자 Local Timezone)로 구분한다.

세부 규칙은 Ⅵ-1, Ⅵ-2, Ⅵ-3, Ⅶ에서 정의한다.

[3-2. No Column] (수정 파일 확정)
모든 모듈 화면 맨 좌측에 Row 번호를 표기하는 'No' Column을 두고 1부터 1씩 증가하는 수를 표기한다.
모듈 1~2는 Row 선택 Column 바로 다음에 'No' Column을 둔다.

[3-4. 화면 언어] (2026-11 확정)
화면 기본 언어는 영문으로 하며, 필요 시 한글을 병기할 수 있다. 팝업(Weekly Reset 등)도 동일하게 적용한다.

[3-3. 검색 조건 요약] (수정 파일 확정, 세부는 각 Module 참조)
화면의 작업 주차 표기는 Module 5~10 모두 'W44(W0)' 형식으로 통일한다. (IN-1 확정, 2026-11)
모듈 1 (Material Master): ① Status(All / Active / Inactive) + ② 검색조건(Mat. Code / Desc. / Purchaser / Vendor / Country) → 검색어 → Search

모듈 2 (Assy Master): ① Status(All / Active / Inactive) + ② 검색조건(Cust. Code / Assy Code / Type / Model / Item /  Customer / Country) → 검색어 → Search 

모듈 3 (BOM): ① Assy Status(All / Active / Inactive / No DB) + ② 검색조건(Cust. Code / Mat. Code) → 검색어 → Search

모듈 4 (Safety Stock): ① Status(All / Active / Inactive / No DB) + ② 검색조건(Cust. Code / Assy Code / Type) → 검색어 → Search

모듈 5 (Inventory): ① 적용주차(작업 주차 Default ~ 지난 16주 전) + ② 검색조건 Code → 검색어 → Search

모듈 6 (RTF/Production): ① 적용주차 + ② 계획선택(All / RTF / Prod.) + ③ 검색조건(Cust. Code / Assy Code / Type) → 검색어 → Search 

모듈 7 (Open PO): ① 적용주차 + ② 검색조건(PO Date / PO No / Mat. Code / Vendor) → 검색어 → Search

모듈 8 (Scheduled Receipt): ① 적용주차 + ② 검색조건(Mat. Code / Vendor / L/T) → 검색어 → Search

모듈 9 (Material Requirement): ① 적용주차 + ② 계획선택(All / RTF / Prod.) + ③ 검색조건(Mat. Code / Cust. Code) → 검색어 → Search

모듈 10 (Material PSI): ① 적용주차 + ② 계획선택(All / RTF / Prod.) + ③ 검색조건(Mat. Code / Desc.) → 검색어 → Search (R-2 확정)

[3-5. 헤더 색상 규칙 (데이터 소스 구분)] (2026-11 확정)
파란색 헤더 Column: 엑셀 업로드로 입력되는 Column이다.
회색 헤더 Column: 시스템이 Master Data를 참조하여 표시하거나 자동 계산하는 Column이다. 엑셀 업로드 양식에 포함하지 않는다.
각 Module의 Upload 양식은 파란색 Column만 포함한다. (Ⅶ 참조)

[3-6. 화면 강조 규칙] (2026-11-24 확정, 전체 Module 공통)
Status 글자색: Inactive = 파란색(#0000FF), No DB = 빨간색(#C00000). Active는 기본 글자색.
Assy 행 또는 집계 행(BOM의 Assy 행, Module 9의 Total 행, Module 10의 Requirement 행): 굵은 글씨와 옅은 회색 셀 배경으로 강조한다.
음수(부족) 셀: 셀 배경 주황색(#F8CBAD), 숫자 글자색 빨간색(#C00000). (Module 10 Inventory Balance, PO Balance)
Calculated 입고예정(L/T 기준 계산값): 파란색(#0000FF). Manual 입고예정은 검정색. (Module 8, Module 10)
Purchaser ID 또는 Purchaser의 상태가 'Request' 또는 'Disabled'인 경우 이름 옆에 붉은 글씨로 표기한다. (Module 1)
행 선택 체크 시 해당 행의 수정 가능한 셀을 반전(강조)하여 수정 가능한 셀임을 표시한다. (Module 1, Module 2)

[4. Module 유형]
1~4번 Module:
기준정보 성격의 Module이다.
Material Master
Assy Master
BOM
Safety Stock (Assy 기준, Customer Code별)
등록된 정보를 지속적으로 사용하며
필요 시 수정하거나 Inactive 처리한다.

5~8번 Module:
매주 변동하는 Weekly Data Module이다.
Inventory
RTF/Production Plan
Open PO
Scheduled Receipt
매주 새로운 Data를 Upload한다.
새로운 Week Data를 Upload하더라도
과거 Week Data를 삭제해서는 안 된다.
예:
2026-W41 Data를 Upload할 경우
2026-W41 대상 Data
→ 신규 등록 또는 갱신
2026-W40 이하의 기존 과거 Data
→ 그대로 보존
Weekly Data 관리 시 DB 내부에서는
필요에 따라 다음과 같은 이력정보를 관리할 수 있도록 설계한다.
예:
year_week
snapshot_date
upload_batch_id
uploaded_at
uploaded_by
source_filename
구체적인 DB Field는 DB 설계 단계에서 결정한다.

9~10번 Module:
계산 및 Report Module이다.
Material Requirement
Material PSI
사용자가 별도의 Excel Data를 Upload하지 않는다.
1~8번 Module에 등록된 Data를 이용하여
시스템이 계산한 결과를 조회한다.

[5. Excel Upload 공통 방식]
Upload 방식은 모듈별로 다음과 같이 적용한다. (수정 파일 확정)
모듈 1(Material Master), 모듈 2(Assy Master): Upload Type 3종(Add / Change / Inactive)을 팝업에서 선택한 후 파일을 선택한다. (Ⅵ-1-6, Ⅵ-2-6)

모듈 3(BOM): Upload Type 2종(Add / Change)을 팝업에서 선택한 후 파일을 선택한다. (Ⅵ-3)

모듈 4(Safety Stock): Upload Type 없이 파일을 선택하여 전체교체한다. 기존 Data는 Update 기준으로 History에 보관한다.

모듈 5~8(Inventory, RTF/Production Plan, Open PO, Scheduled Receipt): Upload Type 없이 파일을 선택하여 작업 주차의 기존 Data 전체를 대체한다. 기존 Data는 삭제하며 History 조회 기능은 없다. 과거 주차 Upload는 불가하다.

모듈 9~10: Excel Upload 없음.

작동 순서: 'Upload' 클릭 → (모듈 1~3만) 팝업에서 Upload Type 선택 → 'Confirm' → 파일 탐색기 → 파일 선택 → 'Upload' 클릭 → Validation 결과 확인 → [반영]

모듈 3~10에서 Upload 시 Material Master·Assy Master의 기준속성(Desc., Spec., Type, Model, Item 등)은 시스템이 자동으로 반영하여 조회 시 Master 값을 표시한다.

5~8번 Weekly Data Module의 "전체교체"는 DB 전체 Data 삭제를 의미하지 않는다.
반드시 현재 선택된 작업 주차의 Data만 교체하며, 과거 주차 Data는 삭제하지 않는다.
각 Mode의 정확한 처리 Rule은 해당 Module 요구사항에서 별도로 정의한다.

[5-1. 표준 업로드 양식 규칙]
모든 Excel Upload는
첨부 '표준 업로드 양식_1123.xlsx'의 시트 구조를 따른다.
Module별 시트명, Column 구성은 Ⅶ에서 정의한다.

시트명 고정
각 Module은 지정된 시트명의 시트만 읽는다.
다른 시트는 무시한다.
따라서 하나의 Excel File에 여러 Module 시트가 함께 있어도 된다.
지정 시트가 없으면 Upload Error로 처리한다.

Header 위치
1행 = Header
2행부터 = Data
Header 위의 제목행, 합계행, 빈 행을 허용하지 않는다.

Header 이름
Ⅶ에 정의된 Column명과 정확히 일치해야 한다.
앞뒤 공백은 제거한 후 비교한다.
Column 순서가 달라도 Header 이름으로 인식한다.
필수 Column이 없으면 Upload Error.
정의되지 않은 Column은 무시하고 Validation 결과에 안내한다.
병합 셀 금지
병합 셀이 있으면 Upload Error.
수식
수식 Cell은 수식이 아니라
Excel에 저장된 계산 결과값을 읽는다.
양식에는 수식을 사용하지 않고 값만 입력하도록 안내한다.

Code Column
Code 값은 항상 문자열로 읽는다.
숫자로 저장된 Code(예: 4605000219)도
문자열 '4605000219'로 변환한다.
지수표기(예: 3.04E+11)로 손상된 값은 Upload Error.
앞뒤 공백을 제거한다.

수량 Column
숫자만 허용한다.
빈 Cell은 Module별 규칙에 따라 0 또는 NULL로 처리한다.
음수 허용 여부는 Module별로 정의한다.
완전히 빈 행
Code를 포함한 모든 Cell이 빈 행은 무시한다.
Template Download
[권장안] Upload 기능이 있는 각 Module 화면에서
해당 Module의 빈 표준 양식을 Download할 수 있도록 한다.

────────────────────
[6. 주차 및 시간 기준]
────────────────────
시스템의 모든 Weekly Data 및 계산결과는
ISO Week 기준으로 관리한다.
본 시스템의 업무 기준 Timezone(Business Timezone) 및
Server Timezone의 Default 값은 베트남 시간으로 한다.
Default Timezone:
Asia/Ho_Chi_Minh
UTC+7
노바텍의 주요 생산공장과 주요 고객사의 휴대폰 생산공장이
베트남 하노이에 위치하고 있으므로,
주차 판단 및 주간 업무 기준은 베트남 시간을 기준으로 통일한다.
[6-1. Current Week 결정 방식]
Current Week는 시스템이 자동으로 계산한다.
기준:
ISO Week Number
ISO Week는
월요일
~
일요일
을 하나의 Week로 관리한다.
Current Week 판단 기준 Timezone은
Asia/Ho_Chi_Minh (UTC+7)
으로 한다.
시스템은 베트남 시간 기준 매일 자정(00:00)에
날짜와 Current Week 정보를 다시 판단한다.
Week가 변경되는 시점은
베트남 시간:
월요일 00:00
이다.
예:
Vietnam Time:
2026-10-12 Monday 00:00
→ 새로운 ISO Week로 전환
동일 시점의 Korea Time은:
2026-10-12 Monday 02:00
이지만
시스템의 Current Week 전환기준은
사용자의 Local Time이 아니라
베트남 Business Timezone을 따른다.
예:
Current Week
2026-W42
연말/연초의 Week 계산은
일반 Calendar Year 기준이 아니라
ISO Week-Year 기준으로 처리한다.
ISO 기준으로 1년은 52주 또는 53주이다.
예:
2026년은 53주까지 있다.
2026-W53 = 2026-12-28(월) ~ 2027-01-03(일)
2027-W01 = 2027-01-04(월) ~ 2027-01-10(일)
주차를 계산할 때
"52주 다음은 1주"로 고정하지 않는다.
반드시 ISO Week 계산 함수로 판단한다.
[6-1-1. 주차 표기 규칙]
시스템 화면, DB, Excel Upload/Download의 주차는
연도를 포함한 다음 형식으로 표기한다.
YYYY-Www
예:
2026-W43
2026-W53
2027-W01
연도가 없는 주차 숫자(예: 43, 1)만으로는
주차를 판단하지 않는다.
Upload Header의 주차가 이 형식이 아니면 Upload Error.

[6-1-2. 상대 주차 표기 (W±ww)] 
작업 주차(당주)는 'W0' 주차로 표기하고, 1주 전은 W-1, 차주는 W+1로 표기한다.
예) 작업 주차 44주인 경우:
2026년 W42(W-2), W43(W-1), W44(W0), W45(W+1), W46(W+2), W47(W+3), W48(W+4), W49(W+5), W50(W+6), W51(W+7), W52(W+8), W53(W+9), 2027년 W01(W+10), W02(W+11), W03(W+12), W04(W+13)
생산계획/PSI를 14주 관리한다는 의미는 W0~W+13까지 데이터를 입력하고 계산한다는 의미이다.
화면 표기는 'W44(W0)'처럼 주차와 상대 주차를 병기한다. 업로드 Header와 DB 주차는 YYYY-Www 형식을 유지한다. (2026-11 확정, 권장안 채택)

(Ⅳ-6-1-1)
[6-2. 작업 주차]
사용자가 화면에서 조회하거나 작업할 기준 Week를
"작업 주차"
라고 정의한다.
작업주차는 상대주차 W0로 표기한다. 

5~10번 업무 Module(Weekly Data 및 계산 Module) 화면에는
작업 주차를 선택할 수 있는 Dropdown을 제공한다.

1~4번 기준정보 Module(Material Master, Assy Master, BOM, Safety Stock)은
주차별 이력이 없으므로 작업 주차 Dropdown을 표시하지 않는다. (확정)
항상 현재 Data를 표시한다.
Default:
베트남 Business Timezone 기준
오늘 날짜의 Current Week
예:
Vietnam 기준 Current Week = 2026-W42
화면 최초 진입:
작업 주차 = 2026-W42
사용자는 작업 주차 Dropdown에서 다른 Week를 선택하여 과거 Data와 과거 Snapshot을 조회하고 Download할 수 있다.
적용주차 선택 범위는 작업 주차(Default)부터 지난 16주 전까지이다. (Ⅳ-3-3)
과거 주차는 조회 및 Download만 가능하며 Upload·수정·Recalculate는 불가하다.
작업 주차 변경은
시스템의 Current Week 자체를 변경하는 기능이 아니다.
Current Week:
베트남 Business Timezone 기준으로
시스템이 자동 결정하는 실제 현재 Week
작업 주차:
사용자가 화면에서 선택한
조회 및 업무 기준 Week
[6-3. Current Week와 작업 주차 구분]
예:
Vietnam 기준 Current Week
2026-W42
사용자가 작업 주차를
2026-W40
으로 변경한 경우:
Current Week
2026-W42
작업 주차
2026-W40
따라서 시스템은
Current Week
와
작업 주차
를 서로 다른 값으로 관리한다.

[6-4. UTC 저장 및 Local Time 표시]
DB의 Date/Time 정보는
UTC 기준으로 저장한다.
예:
created_at
updated_at
uploaded_at
inactive_at
recalculated_at
login_at
password_reset_at
등
화면에 Date/Time을 표시할 때에는
사용자의 Local Timezone을 기준으로 변환하여 표시한다.
예:
DB:
UTC 기준 저장
Vietnam 사용자:
Asia/Ho_Chi_Minh
UTC+7 기준 표시
Korea 사용자:
Asia/Seoul
UTC+9 기준 표시
단,
Current Week
작업 주차의 Default Week
Recalculate의 Current Week 판단
등 Weekly 업무 Logic의 기준 Timezone은
사용자의 Local Timezone이 아니라
Asia/Ho_Chi_Minh (UTC+7)
을 사용한다.
즉,
"시간 표시 기준"
과
"주차 업무 판단 기준"
을 구분한다.
시간 표시:
각 사용자 Local Timezone
Current Week 판단:
베트남 Business Timezone

[6-5. 과거 Week 보존]
과거 작업 주차 Data는
당시의 업무 Snapshot으로 보관한다.
Master Data 또는 BOM 등이 현재 수정되더라도
과거 Week 계산결과를 자동으로 다시 계산하지 않는다.
과거 Snapshot은
당시 계산결과와 당시 업무상태를 유지하는 것을 원칙으로 한다.

[6-6. 주차 전환 시 처리]
베트남 시간 월요일 00:00에 Current Week가 바뀌면:
지난 주차
지난 주차의 Data와 계산결과는
마지막으로 재계산된 상태 그대로 Snapshot으로 확정한다.
새 작업 주차 (Data Upload 전)
새 작업 주차는 빈 상태로 시작한다. 지난 주차 Data를 자동 복사하지 않는다. (수정 파일 반영, 작동 예 2)
필요 시 모듈 10의 Weekly Reset으로 작업 주차 Data(모듈 5~8)를 초기화한 후 Upload한다. (Ⅳ-7-4)
주차 Column이 있는 Data(RTF, Production Plan, Scheduled Receipt)는 새 작업 주차부터 14주 범위로 맞춘다.
지난 주차 Column은 제외하고, 새로 추가되는 마지막 주차는 0으로 둔다.
────────────────────
[7. Weekly Reset / Recalculate (재계산)]
본 절의 "Current Week"는 Asia/Ho_Chi_Minh (UTC+7) 기준 ISO Current Week를 의미한다.
기존 '새로고침' 버튼과 관련 기능은 모든 시스템에서 삭제한다.

[7-0. 변경 반영 3계층 규칙] (2026-11 확정, 권장안 채택)
계층 1. 원본 데이터: Upload 또는 Save 시 해당 모듈에 즉시 저장한다. 다른 모듈의 저장값은 직접 수정하지 않는다.
        대상: Material·Assy Master, BOM, Safety, Inventory, RTF·Production Plan, Open PO, Manual Scheduled Receipt.
계층 2. 파생 표시값: 화면 조회 시점에 최신 원본과 Master를 조합하여 실시간으로 산출한다. 저장하지 않는다.
        대상: Desc., Spec., Type, Model, Item, L/T, Status(Master 참조), Module 8 Calculated Scheduled Receipt(파란색), Open PO 잔량 차이분.
        차이분이 음수이면 화면에 빨간색 경고를 표시한다.
계층 3. 계산 결과: Module 9(Material Requirement), Module 10(Material PSI)의 값은 Recalculate 실행 시에만 갱신한다.
        원본 변경 후 Recalculate 전까지는 "● Need Recalculation"을 표시하고 이전 계산 결과를 유지한다.
        Recalculate 시 차이분이 음수이면 Error로 차단한다. (Ⅳ-7-10)
별도의 반영 스위치 기능은 두지 않는다. 'Need Recalculation' 표시와 Recalculate 버튼이 그 역할을 한다.
예1) Master 변경 → 계층 2 표시값(Desc., Type 등) 즉시 반영, BOM 기반 소요량은 계층 3(Recalculate)에서 반영
예2) Material L/T 변경 → 계층 2 Calculated Scheduled Receipt 배치 주차 즉시 재산출, 계층 3 결과는 Recalculate에서 반영
예3) Open PO 변경 → 계층 2 잔량과 차이분 즉시 재산출, 음수면 경고 표시, Recalculate 시 Error 차단

[7-1. Recalculate 기본 동작] (확정)
위치: 모듈 10 화면 우측 상단, 'Download' 버튼 좌측.
실행 권한: Admin만 활성. Master·User·Guest는 버튼 비활성화(클릭 불가)이며 Backend에서도 거부한다.

동작: 모듈 1~8의 현재 정보를 기준으로 모듈 9(Material Requirement)와 모듈 10(Material PSI)의 주별 소요량, 기초재고, 입고예정량, 재고 과부족, PO 과부족 등을 재계산하여 업데이트한다.
재계산 대상 Week: Current Week에 한한다. 과거 주차 Snapshot은 재계산하지 않고 조회만 한다. (Ⅳ-6-5)

재계산은 DB에 Save·Upload된 Data만 사용한다. 화면에서 수정 중이지만 저장하지 않은 값은 제외한다.

저장되지 않은 수정내용이 있는 상태에서 Recalculate를 클릭하면 경고를 표시한다.
예: "저장되지 않은 수정내용은 재계산에 반영되지 않습니다. 계속하시겠습니까?"
실행이 끝나면 화면 우측 상단의 "Final Calculation"을 재계산 실행 시각(사용자 Local Timezone 기준)으로 갱신한다.

Validation Error가 발생하면 값을 임의로 보정하지 않고 Error 내용을 표시하며 해당 계산결과의 갱신을 중단한다. (예외: Master Data에 Code 미등록, Inactive 등은 에러 표시하지 않음)

[7-2. 재계산 필요 표시] (확정)
Final Calculation 시각 이후 모듈 1~8에서 Upload 또는 수정이 발생하면 "● Need Recalculation"을 붉은색으로 표시한다.
표시 대상은 계층 3(모듈 9~10 계산 결과)이다. 계층 2 파생 표시값은 실시간 반영되므로 재계산 전 화면 값과 모듈 9~10 값이 다를 수 있으며, 모듈 10 화면에 "재계산 전 원본 기준 차이 있음"을 함께 표시한다.
Recalculate를 실행한 직후에는 "● Need Recalculation"을 표시하지 않는다.

[7-3. 작동 예]
예 1) 월요일 아침 Admin이 모듈 5~8에 Excel을 모두 업로드하더라도 Recalculate를 누르지 않으면 모듈 9~10에는 빈칸만 보인다.
예 2) Admin이 Weekly Reset으로 모듈 5~8 Data를 Reset(빈칸으로 만듦)하더라도 Recalculate를 누르지 않으면 모듈 9~10은 기존 정보를 그대로 보여준다.

[7-4. Weekly Reset] (확정)
위치: 모듈 10 화면 우측 상단, 'Recalculate' 버튼 좌측.
권한: Admin만 활성. Master·User·Guest는 비활성화(클릭 불가)이며 Backend에서도 거부한다.
버튼 클릭 시 팝업: "Do you want to restart Weekly PSI analysis? Reset Inventory, Plan, PO, Scheduled receipt" 

[Cancel] [Confirm]
Confirm 시 모듈 5~8의 작업 주차(W0, 예: 2026-W44) Data를 삭제하여 빈칸으로 만든다. 과거 주차 Data는 대상이 아니다. (Ⅳ-4 과거 Data 보존 규칙과 충돌하지 않도록 작업 주차 Data만 대상으로 한다.)

목적: PSI 분석을 여러 차례 진행할 때 전회차 Data와의 혼입을 예방한다.
예 1) 월요일 PSI 분석으로 구매발주 등을 진행하고, 수요일에 생산잔량·변경된 발주/입고예정·현 재고로 다시 분석하려면 Weekly Reset으로 월요일 등록 정보를 Reset한 후 Upload를 다시 시작한다.
예 2) 월요일 새 작업 주차가 시작되고 당주 Data가 전혀 없으면 모듈 5~8에 Excel을 차례로 Upload한다.

Reset 후에도 Recalculate를 실행하기 전까지 모듈 9~10은 기존 결과를 유지한다.

[7-5. Weekly PSI 분석 운영 방식] (수정 파일 확정)
모듈 1~4는 Master Data 성격으로, 주별 프로세스와 상관없이 항상 최신 Data를 유지한다.
당주차(=작업주차, W0)는 베트남 시간 월요일 00:00부터 시작한다. 예: 2026년 W44
지난 주차(W-1, 예: W43)의 모듈 5~10 Data는 수정·Upload 불가, 조회 및 Download만 가능하다.

당주차(W0)의 모듈 5~8은 Upload가 가능하다.
운영 순서: (필요 시) 모듈 10의 Weekly Reset → 모듈 5~8 Upload → 모듈 10의 Recalculate → 모듈 9~10 업데이트

[7-6. 사용자 입력 원천 Data 보호]
Recalculate는 계산결과 또는 자동산출 Data를 갱신하는 기능이다.
사용자가 입력하거나 Upload하여 저장한 원천 Data를 재계산만으로 임의 수정해서는 안 된다.
예: Material Master, Assy Master, BOM, Safety Stock 원본값, Inventory Upload Data, RTF / Production Plan Upload Data, Open PO 원본 Data, 사용자가 직접 입력한 Scheduled Receipt

[7-7. Scheduled Receipt와 L/T]
Scheduled Receipt는 다음 두 종류를 구분하여 관리한다.
① Manual Scheduled Receipt: 사용자가 Vendor와 협의하여 직접 입력(Upload)한 입고예정 Data. 재계산이나 L/T 변경으로 자동 수정하지 않는다.
② Calculated Scheduled Receipt: Open PO 차이분을 Master Data의 L/T(Weeks)로 계산하여 시스템이 자동 산출한 입고예정. 화면 조회 시 실시간 산출하며 저장하지 않는다(계층 2). 모듈 9~10 반영은 Recalculate 시 Current Week에 한한다.
계산 규칙은 Ⅶ-11에서 정의한다. (확정)

[7-8. 재계산 결과 표시]
재계산 완료 후 최소 다음 정보를 보여준다: 재계산 성공/실패, Current Week, 재계산 대상 Module, 완료시간, Error 여부.
예: "2026-W44 재계산이 완료되었습니다. 영향 Module: Material Requirement, Material PSI"

[7-9. 재계산 동시 실행]
재계산은 한 번에 하나만 실행한다.
재계산이 진행 중일 때 다른 사용자가 Recalculate를 클릭하면 추가 실행하지 않고 "다른 사용자가 재계산 중입니다. 완료 후 결과가 표시됩니다." 메시지를 표시한다.
재계산이 끝나면 모든 사용자 화면에 같은 결과를 보여준다.

[7-10. 검증 결과 등급: Error / Warning] (2026-11 확정)
Error (치명 오류): 해당 Upload 전체 또는 계산을 중단한다. 사용자가 수정 후 재실행해야 한다.
  예) 지정 시트 없음, Unit 불일치(Upload Unit ≠ Material Master, Material Master 변경 후 기존 BOM Unit 불일치), Code 중복(Excel 내), 지수표기 손상, Q'ty 변환 불가, Open PO Remain Q'ty 음수, 같은 Material+Vendor 중복 입고예정 행, Assy 열 2회 이상
Warning (경고): 처리는 정상 수행한다. 대상 목록을 결과에 포함하여 사후에 작업자에게 보고하고, [반영]을 막지 않는다.
  예) Master에 없는 Code('No DB'), Inactive Assy·Material 수량의 계산 포함, BOM 미등록 Assy(소요량 0 간주), Assy 열만 있는 Assy 무시(기존 BOM 유지)
Validation 결과 화면에는 Error 건수와 Warning 건수를 구분하여 표시한다.

────────────────────
Ⅴ-1. 사용자 권한 및 계정 관리
────────────────────
시스템 사용자는
한국 본사 및 베트남 공장에서 근무하는
약 20명의 구매 관련 인력이다.
사용자 권한은 다음 네 종류로 구분한다.
Master
Admin
User
Guest

[1. Master]
Master는 시스템 사용자 계정을 관리하는 운영자 권한이다.
Master ID는 novamaster 한 개만 운영한다. (1014 문서의 nova-master 표기는 novamaster로 통일한다.)
Master 계정의 초기 Password는 Source Code에 고정된 평문 Password로 구현하지 않는다.
초기 Master 계정 생성 시 임시 Password를 발급하고, 최초 Log-in 시 반드시 새로운 Password로 변경하도록 한다.
Master 주요 권한: 신규 ID 승인 / 사용자 Class 변경 / ID Status 변경 / Password Reset / User Management 접근

Master로 Log-in한 경우에만 Main 화면에 "※ User Management" Button이 표시된다. Admin, User, Guest에게는 표시하지 않는다.
Frontend뿐 아니라 Backend에서도 Master 권한 여부를 검증한다.
Master는 10개 업무 Module에서 조회, 검색, Filter, Excel Download 권한만 가진다.
Excel Upload, 화면 수정, Save, Recalculate 권한은 가지지 않으며 해당 버튼은 비활성화된다.

[2. Admin]
Admin은 약 1~2명의 전체 구매SCM Process 관리자이다.
Module 1~2 (Material Master, Assy Master): 조회, 검색, Filter, Excel Download, Excel Upload, 화면 수정 및 Save (Status 변경 포함)
Module 3 (BOM): 조회, 검색, Filter, Excel Download, History Download, Excel Upload. 화면 수정은 불가하다.
Module 4~8 (Safety Stock, Inventory, RTF/Production Plan, Open PO, Scheduled Receipt): 조회, 검색, Filter, Excel Download, Excel Upload. 화면 수정은 없다.
Module 9 (Material Requirement): 조회, 검색, Filter, Excel Download.
Module 10 (Material PSI): 조회, 검색, Filter, Excel Download, Recalculate, Weekly Reset.

[3. User]
User는 실제 자재 발주와 Vendor 입고예정 관리를 수행하는 일반 구매담당자이다.
Module 1~10: 조회, 검색, Filter, Excel Download.
화면 수정, Save, Excel Upload는 불가하다. Module 7(Open PO), Module 8(Scheduled Receipt)도 조회만 한다. (수정 파일 확정)
Recalculate, Weekly Reset은 불가하다.
향후 일부 Module의 화면 수정·Upload 권한을 User에게 부여할 수 있도록 권한 구조를 확장 가능하게 설계한다. (현재는 Admin 전용)

[3-1. Guest]
Guest는 구매팀 외 관련 부서 인원 등 업무 Data를 열람만 하는 사용자이다.
Module 1~10: 조회, 검색, Filter, Excel Download.
Guest가 할 수 없는 기능: User Management 접근, Excel Upload, 화면 수정, Save, Recalculate, Weekly Reset.
Guest 화면에서는 Save·Upload 버튼을 비활성화하며, Frontend와 별개로 Backend/API에서도 반드시 차단한다. (Ⅰ-9)
Guest도 Main 화면의 ID Info Pop-up에서 본인의 Password, Name, e-mail, Tel은 수정할 수 있다.
Guest 계정 생성:
Guest도 User와 동일하게 Sign up으로 신규 등록하고, Master 승인 후에만 Log-in할 수 있다.
Sign up 시에는 Class = User로 저장되며, Master가 User Management에서 Class를 Guest로 변경한 후 승인한다.

[4. 권한 Matrix] (수정 파일 확정)
기능                      Master          Admin                    User            Guest
User Management           관리            접근불가                 접근불가        접근불가
Material Master (M1)      조회/다운로드   관리(Upload·화면수정·Save) 조회/다운로드  조회/다운로드
Assy Master (M2)          조회/다운로드   관리(Upload·화면수정·Save) 조회/다운로드  조회/다운로드
BOM (M3)                  조회/다운로드   Upload만(화면수정 불가)    조회/다운로드   조회/다운로드
Safety Stock (M4)         조회/다운로드   Upload                   조회/다운로드   조회/다운로드
Inventory (M5)            조회/다운로드   Upload                   조회/다운로드   조회/다운로드
RTF/Production (M6)       조회/다운로드   Upload                   조회/다운로드   조회/다운로드
Open PO (M7)              조회/다운로드   Upload                   조회/다운로드   조회/다운로드
Scheduled Receipt (M8)    조회/다운로드   Upload                   조회/다운로드   조회/다운로드
Material Requirement (M9) 조회/다운로드   조회/다운로드            조회/다운로드   조회/다운로드
Material PSI (M10)        조회/다운로드   조회/다운로드            조회/다운로드   조회/다운로드
Recalculate·Weekly Reset  불가            가능(모듈 10 화면)       불가            불가

※ 업무 Module에서 "관리"란 조회, 검색/Filter, Excel Download, Excel Upload, (모듈 1~2) 화면 수정 및 Save를 의미한다.
※ Save·Upload 버튼은 Admin 외 사용자에게 비활성화한다. Backend에서도 동일하게 검증한다.
※ 나중에 User에게 일부 Module의 화면 수정·Upload 권한을 부여할 수 있도록 권한 구조를 확장 가능하게 설계한다.

[5. 사용자 계정 Status]
사용자 ID의 Status는 다음 세 값을 사용한다.
Requested
Approved
Disabled

Requested:
신규 Sign up 후 Master 승인을 기다리는 상태.
Log-in 불가.

Approved:
Master가 사용을 승인한 상태.
정상 Log-in 가능.

Disabled:
퇴직자 또는 시스템 사용 중지 사용자.
Log-in 불가.

[6. Password 공통 Rule]
Password는 DB에 평문으로 저장하지 않는다.
Backend에서 안전한 Password Hash 방식으로 저장한다.
시스템 관리자도
사용자의 기존 Password를 조회할 수 없어야 한다.
Password Reset은
기존 Password를 알아내는 기능이 아니다.
새로운 임시 Password를 발급하는 방식으로 구현한다.
임시 Password로 Log-in한 사용자는
새 Password를 설정하기 전에는
정상적인 시스템 업무 기능을 사용할 수 없도록 한다.

[7. 보안 규칙] (확정)
Password:
8자 이상
영문과 숫자를 각각 1자 이상 포함
특수문자 사용 가능 (필수 아님)
공백 불가
Log-in 실패:
같은 ID로 연속 5회 실패 시 10분간 Log-in 잠금
잠금 중에는 "Log-in 시도 횟수를 초과했습니다. 10분 후 다시 시도하세요." 표시
Log-in 성공 시 실패 횟수 초기화
Session:
2시간 동안 사용하지 않으면 자동 Log-out
저장하지 않은 수정내용이 있으면 Log-out 전에 경고 표시
위 규칙에 없는 Security Rule이 추가로 필요하면
개발 전에 [확인 필요]로 사용자에게 질문한다.
────────────────────
Ⅴ-2. 첫번째 관리 화면 _ Log-in
────────────────────
시스템 URL을 입력하면
Log-in 화면으로 이동한다.
첨부:
'스크린샷 Login01.png'
기존 사용자는
ID
Password
입력 후
"Log in"을 클릭한다.
Log-in 가능 조건:
ID Status = Approved
그리고
Password 정상 일치
Requested 또는 Disabled 상태 ID는
Password가 맞더라도 Log-in할 수 없다.
Log-in 성공 시 Main 화면으로 이동한다.
신규 사용자는
"Sign up"
Button을 클릭하여
Sign up 화면으로 이동한다.
Master가 Password Reset을 수행하여
임시 Password가 발급된 사용자가 Log-in한 경우
Main 화면으로 이동한 후
자동으로 ID Info Pop-up을 표시한다.
새 Password로 변경하기 전까지
업무 Module 접근을 제한한다.
────────────────────
Ⅴ-3. 두번째 관리 화면 _ Sign up
────────────────────
신규 사용자가 자신의 정보를 등록하고
시스템 사용 승인을 요청하는 화면이다.
첨부:
'스크린샷 Sign up01.png'
Sign up 완료 시:
Class = User
ID Status = Requested
로 자동 저장한다.
사용자는 Sign up에서
Admin 권한을 직접 신청하거나 선택하지 않는다.
Admin 또는 Guest가 필요한 경우
Master가 User Management에서 Class를 변경한다.
[1. ID]
문자열
영문자, 숫자, '.', '_', '-' 사용 (2026-11-24 확정)
그 외 특수문자 불가
대소문자 구분 없음 (소문자로 저장·비교) (2026-11-24 확정)
앞뒤 공백 제거
중간 공백 불가
빈 값 불가
동일 ID 중복 불가
Unique Key
입력 후
"ID check"
Button으로 중복 여부를 확인한다.
[2. P/W]
문자열
영문자 / 숫자 / 특수문자 사용 가능
공백 불가
DB 평문 저장 금지
Ⅴ-1-7 보안 규칙(8자 이상, 영문+숫자 포함)을 따른다.
[3. P/W Again]
첫 P/W와 동일해야 한다.
불일치 시 Save 불가.
[4. Name]
사용자 이름.
[5. e-mail]
사용자 e-mail 주소.
Password Reset,
시스템 알림,
향후 Report 송신 등에 사용한다.
[6. Tel]
문자열로 관리한다.
국가번호 포함 가능.
예:
+821056781345
+82-10-5678-1234
[7. Save]
Validation 통과 시
Class = User
ID Status = Requested
상태로 저장한다.
Master 승인 전에는 Log-in할 수 없다.
────────────────────
Ⅴ-4. 세번째 관리 화면 _ Main
────────────────────
Log-in 성공 후 이동하는
Main Navigation 화면이다.
첨부:
'스크린샷 Main 01.png'
10개 업무 Module을 표시하고
클릭하면 해당 Module로 이동한다.
[1. Log out]
Session을 종료하고
Log-in 화면으로 이동한다.
[2. ID Info]
현재 로그인 사용자의 개인정보 수정 Pop-up.
수정 가능:
Password
Name
e-mail
Tel
일반 Password 변경 시
Old P/W 확인 후 변경한다.
[3. Password Reset 후 강제 변경]
임시 Password 사용자 Log-in 시
ID Info Pop-up을 자동 표시한다.
새 Password 저장 전까지
업무 Module 사용을 제한한다.
[4. User Management]
Master에게만
"※ User Management"
Button을 표시한다.
클릭하면
User Management 화면으로 이동한다.
────────────────────
Ⅴ-5. 네번째 관리 화면 _ User Management
────────────────────
Master 권한 전용
사용자 계정 관리 화면이다.
첨부:
'스크린샷 User Management 01.png'
표시 Field:
Check
ID
Name
Class
ID Status
e-mail
Tel
Password 자체는 표시하지 않는다.
ID:
수정불가
Name:
Master 수정불가
Class:
User / Admin / Guest
Master 변경 가능
Guest로 사용할 신규 사용자는
Sign up 후 Requested 상태에서 Master가 Class를 Guest로 변경하고
ID Status를 Approved로 변경하여 승인한다.
ID Status:
Requested
Approved
Disabled
Master 변경 가능
Password Reset:
대상 Row 선택
→ P/W Reset
→ 임시 Password 발급
→ e-mail 통보
→ 다음 Login 시 Password 변경 강제
※ 임시 Password 통보 수단은 e-mail 발송으로 확정한다. (Ⅷ A-2)
e-mail / Tel:
Master 수정불가
Class 또는 ID Status를 수정한 경우
반드시 Row 선택 후 Save해야 반영한다.
Field              Master 수정
ID                 불가
Name               불가
Class              가능
ID Status          가능
Password Reset     가능
e-mail             불가
Tel                불가
────────────────────
Ⅵ-1. 첫번째 기능 Module _ Material Master
────────────────────
[1. 기능 / 업무 목적]
Material Master 는 시스템에서 사용하는 Material의 기준정보를 관리한다.
화면 UI: '스크린샷 01.png'
(단, 화면 Column 구성은 본 절의 [3. 데이터 구성]이 우선한다.)
기준 Key: Material Code
다음 Module의 공통 기준정보로 사용한다.
BOM
Inventory
Open PO
Scheduled Receipt
Material Requirement
Material PSI
Material Master는 Code 및 기준속성의 Single Source of Truth이다.

다른 Module에서 신규 사용하는 Material Code 가 Material Master에 존재하지 않거나
Status = Inactive 이더라도 Error 처리하지 않는다. (Status에 상태표기로 대체)

다른 Module의 Code 확인 기준:
Material을 사용하는 Data
(BOM 하위, Material 재고, Open PO, Scheduled Receipt)
→ Material Master의 Material Code와 비교

Code 비교는 Ⅵ-1-4의 Code 정규화(앞뒤 공백 제거, 영문 대문자 변환)를
적용한 값으로 한다.

다른 Module Data가 Material Master와 충돌할 경우
시스템이 임의로 다른 Data를 수정하지 않는다.
Validation Error를 발생시킨다.

────────────────────
[2. Key 규칙]
────────────────────
Material Code는 Material Master 안에서 중복 불가.
Assy의 Key(Customer Code)와 Material의 Key(Material Code)가 서로 다르므로
두 Data는 충돌하지 않는다.

────────────────────
[3. 데이터 구성]
────────────────────
Excel Upload (시트명 고정, Ⅳ-5-1 및 Ⅶ 참조): 화면 UI '스크린샷 01.png'에서 데이터 헤더 셀의 음영이 파란색(#64A9D6)으로 표기된 Column은 업로드 데이터 

시트 'MD_Material':
Material Code
Desc.
Spec.
Unit
Purchaser ID
Vendor
Country
L/T(Weeks)
update와 Status는 Upload Column으로 받지 않는다.
시스템이 관리한다.

[3-1. 화면 구성] (확정)
Material Master Column:
Material Code
Desc.
Spec.
Unit
Purchaser Name('User Management' 모듈에서 로그인 ID에 해당하는 Name을 찾아서 적용)
Vendor
Country
L/T(Weeks)
update
Status (맨 우측)

Row 선택은 체크박스 방식이다. (Ⅵ-1-9-1)
Purchaser 표기: Purchaser 이름 옆에 해당 사용자의 Status가 Approved가 아니면 붉은 글씨로 'Requested' 또는 'Disabled'를 표기한다. (Ⅳ-3-6, 2026-11 확정) 'No' Column은 Row 선택 Column 바로 다음에 둔다. (Ⅳ-3-2)

Excel Download:
현재 선택된 Table의 모든 Column (화면 구성과 동일)
No, 
Material Code
Desc.
Spec.
Unit
Purchaser Name('User Management' 모듈에서 로그인 ID에 해당하는 Name을 찾아서 적용)
Vendor
Country
L/T(Weeks)
update
Status

────────────────────
[4. Field 정의]
────────────────────
[4-0. Code 정규화] (확정)
Material Code 는 다음과 같이 정규화하여 저장하고 비교한다.
앞뒤 공백 제거
영문은 대문자로 변환하여 저장
(예: 'smaz13001' → 'SMAZ13001', 두 값은 같은 Code)
그 외 문자는 제한하지 않는다.
(숫자, '-', '_', 공백, 괄호, '' 등 허용.
예: 'MAGNET D33T', '304060006 (AVBS)-1')
숫자로 저장된 Excel 값도 문자열로 변환한다.
① Material Code
Material의 Unique Key
문자열, Ⅵ-1-4-0 정규화 적용
빈 값 불가
Material Master 내 중복 불가
화면 신규입력 불가
화면 수정 불가
신규등록은 Admin Excel Upload만 가능
② Desc.
품명
문자열
화면 수정 가능
Excel Upload 가능
③ Spec.
사양
문자열
일반 규격 특수문자 허용
화면 수정 가능
Excel Upload 가능
④ Unit (확정)
필수. 빈 값은 Validation Error (2026-11-24 확정: 다른 Module의 Unit 비교 기준이므로)
허용값:
EA
SHEET
SET
G
KG
MM
M
소문자·대소문자 혼용으로 입력해도 대문자로 변환하여 판단
(예: 'sheet' → 'SHEET')
허용값 외의 값은 Validation Error
화면에서는 Dropdown으로 선택
Excel Upload 가능
허용값 추가는 Source Code 수정 없이 관리할 수 있는 구조로 설계한다.
(허용값 추가 화면은 이번 범위가 아니다.)

⑤ Purchaser (확정)
구매담당자를 사용자 계정 ID로 연결한다.
Upload에는 사용자 ID를 입력한다. (예: nova007)
화면에는 해당 ID의 사용자 Name을 표시한다. (예: Emily)
User Management에 등록되지 않은 ID는 Validation Error
화면에서 수정 시 등록된 사용자 목록에서 선택(화면에 ▼로 표기)  한다.
빈 값 허용 (담당자 미지정)
향후 "내 담당 자재" Filter 등
구매담당자별 업무관리에 사용한다.

Purchaser ID의 계정 Status 처리 (확정):
User Management에 등록된 ID이면
Status(Requested / Approved / Disabled)와 관계없이 Purchaser로 지정할 수 있다.
Requested 또는 Disabled 상태의 사용자는
Ⅴ-1-5에 따라 Master 승인(Approved) 전까지 Log-in할 수 없다.
화면에서는 Approved가 아닌 사용자가 Purchaser인 경우
이름 옆에 해당 Status를 함께 표시하여 식별할 수 있게 한다.

⑥ Vendor (확정)
자유기재 문자열
여러 Vendor를 한 Cell에 기재할 수 있다.
(예: 'VINA/KS/Magtech/LS')
참고정보이며 다른 Module과 Code로 연결하지 않는다.
⑦ Country
Main Vendor 소재국가
직접입력
⑧ L/T(Weeks) (확정)
Material Master에만 있는 Field
필수
정수
1 이상
빈 값, 0, 음수, 소수는 Validation Error
⑨ update
시스템 자동 생성
사용자 수정 불가
화면에서는 사용자 Local Timezone 기준으로 표시한다.
DB 저장은 UTC 기준으로 관리한다.
[권장안] 실제로 값이 변경된 행만 update를 갱신한다.
⑩ Status
Active
Inactive
시스템 관리
Admin이 화면에서 Active / Inactive를 선택하여 변경 가능 (Row 선택 후 Save). Upload Column이 아님
Inactive 처리 (Delete 기능 없음)
Physical Delete 금지
────────────────────
[5. Validation]
────────────────────
시트 'MD_Material'
Material Code    필수
Desc.            가능
Spec.            가능
Unit             필수 (허용값 목록) (2026-11-24 확정)
Purchaser ID     가능 (등록된 사용자 ID)
Vendor           가능
Country          가능
L/T(Weeks)       필수 (1 이상의 정수)
Rule 위반 시
자동수정하지 않고 Validation Error.

────────────────────
[6. Excel Upload]
────────────────────
Upload 대상 시트 'MD_Material' → Material Master에만 영향.
Upload Type 3종 (팝업에서 선택 후 Confirm, 수정 파일 확정):

① Add(등록): Upload Material Code가 DB에 없는 신규 Code이면 추가 등록(Status = Active). DB에 이미 존재하면 엑셀 데이터를 무시(건너뛰기).

② Change(수정): Upload Material Code가 DB에 존재하면 Upload 정보로 덮어쓰고 Status를 Active로 설정. DB에 없으면 신규 등록(Status = Active).

③ Inactive(삭제): Upload Material Code가 DB에 존재하면 Status를 Inactive로 변경(엑셀 내 나머지 Column 값은 무시). DB에 없으면 무시.
Excel 빈 Cell은 Change에서 NULL로 처리한다. (L/T(Weeks)는 필수이므로 빈 값이면 Validation Error)
DB 반영 전 다음 건수를 표시하고 사용자 확인을 받는다.
신규등록 예정 / 수정 예정(변경 Field 표시) / Inactive 예정 / 무시 예정 / 재활성화 예정

Inactive 대상 Code가 다른 Module에서 사용 중이더라도 Inactive 처리를 차단하지 않는다.


────────────────────
[7. Excel Upload Validation]
────────────────────
Upload 후 즉시 DB 저장하지 않는다.
Upload → Validation 결과 표시 → 사용자 [반영] 클릭 → DB 저장
순서로 처리한다.
Validation:
지정 시트 존재 여부
필수 Column
Column Name
Code 빈 값
Excel 내부 Code 중복 (정규화 후 기준, 2회 이상이면 Error. 엑셀 수정 후 재업로드하도록 경고 표시)
허용 Field
Unit 필수 및 허용값 (2026-11-24 확정)
Purchaser ID 등록 여부
L/T 필수, 1 이상의 정수
병합 셀 여부
지수표기 등 손상된 Code
Material Code 'ASSY' 사용 금지 (Ⅶ-5, 2026-11-24 추가)
Upload Type ③ Inactive 시 사용 중인 Code 여부 (Ⅵ-1)
앞뒤 공백 제거.
빈 Cell = NULL
"-" = NULL
Validation 결과:
총 건수
정상 건수
Error 건수
시트명
Excel Row
Code
Error Field
Error 사유
[권장안] Validation 결과를 Excel로 Download할 수 있도록 한다.
Error가 하나라도 있으면
전체 DB 반영 중단.
DB 반영은 Transaction 처리.
중간 Error 발생 시
전체 Rollback.
────────────────────
[8. 화면 조회 / 정렬]
────────────────────
기본 정렬:
Material Code 오름차순
상하/좌우 Scroll 제공.
작업 주차 Dropdown은 표시하지 않는다. (Ⅳ-6-2)
────────────────────
[9 화면 수정]
────────────────────
수정 불가:
Material Code
update
수정 가능: Admin만 수정 가능
Desc.
Spec.
Unit (Dropdown)
Purchaser (사용자 목록에서 선택)
Vendor
Country
L/T(Weeks)
Status (Active / Inactive 드롭다운, Row 선택 후 Save로 반영)

[9-1. Row 선택 및 수정] (확정, 수정 파일 반영)
Admin은 화면 맨 좌측의 Row 선택 Column(체크박스)으로 Row를 선택한다. 여러 Row를 동시에 선택할 수 있다.
작동 순서: Row 선택 → 수정 가능 Data 활성화 → Data 수정 → 'Save' 클릭
수정 가능 Data(8가지): Desc., Spec., Unit, Purchaser, Vendor, Country, L/T(Weeks), Status

값을 수정하면 해당 Row가 자동으로 선택된다.
행을 선택(체크)하면 해당 행의 수정 가능 셀을 반전 표시하여 수정 가능한 셀임을 구분할 수 있게 한다. (Ⅳ-3-6, 2026-11 확정)

Save는 선택된 Row만 저장한다.
Save하지 않은 수정내용이 있는 상태에서 화면 이동 시 경고를 표시한다.
동시 편집 충돌은 Ⅰ-11(Optimistic Lock)을 따른다.
────────────────────

[10. Inactive 처리]
Physical Delete 금지. 화면에 Delete 버튼을 두지 않는다.
Inactive 전환 경로는 두 가지다.
① Admin 화면: Row 선택 → Status를 Inactive로 변경 → Save
② Excel Upload: Upload Type ③ Inactive
사용 중인 Code도 Inactive 전환을 허용한다. (B-7 확정) Confirmation 후 Status = Inactive로 변경하며, 사용 중인 Code는 계산 시 Warning으로 표시한다.

Inactive 시 update 갱신.
기본화면에는 Inactive 미표시 (Status 필터 기본값 Active).
과거 Data 참조관계 유지.
재활성화: Upload Type ② Change, 또는 Admin 화면에서 Status를 Active로 변경 후 Save.
────────────────────
[11. Filter]
Status 필터: 드롭다운 All / Active / Inactive (기본값 Active)
Active: Active Row만 조회
All: Active + Inactive 조회
Inactive: Inactive Row만 조회
Status 필터는 검색조건·검색어와 함께 적용하며, Search 클릭 시 실행한다.
Inactive Row는 Status 열로 식별 가능하게 표시한다.
────────────────────
[12. 검색]
────────────────────
검색조건은 현재 Column 중에서 선택한다.
Default: Material Code
검색대상: Material Code, Desc., Purchaser(이름 또는 ID), Vendor, Country
부분일치 검색. 영문 대소문자 구분 없음.
Status 필터 + 검색조건 + 검색어를 함께 적용하며, Search 클릭 시 실행한다.
────────────────────
[13. Excel Download]
────────────────────
Status(All / Active / Inactive) + 검색조건 + 검색어를 반영한 전체 조회결과 Download.
화면에 일부만 보여도 해당 조건의 전체 Row Download.
Column:
No, Material Code, Desc., Spec., Unit, Purchaser ID, Purchaser,
Vendor, Country, L/T(Weeks), update, Status
Download File의 Column 구성을 Upload 양식과 맞추어 Download → 수정 → 다시 Upload가 가능하도록 한다.
(No, update, Status, Purchaser 이름 Column은 Upload 시 무시)
────────────────────
[13-1. History Download]
────────────────────
조회 조건: 화면 검색 결과 기준 (Status 필터 + 검색조건 + 검색어로 조회된 Material Code 목록)
결과: 검색 결과에 해당하는 Material의 과거 변경 이력 전체를 Excel로 다운로드한다.
기존 Download Column 양식을 그대로 따르며, 각 행의 update를 yyyy-mm-dd hh:mm(사용자 Local Timezone)으로 표기하여 변경 시점별로 구분한다.
이력 행의 Desc., Spec. 등 표시 항목은 해당 변경 시점의 값을 그대로 표시한다.
팝업(Material Code·기간 조건)은 두지 않는다.
────────────────────
[14. Recalculate와 Material Master 변경]
Material Master 수정 후 Save해도 다른 Module의 계산결과는 즉시 자동 변경되지 않는다.
화면에 "● Need Recalculation" 알림을 표시한다. (Ⅳ-7-2)
Admin이 모듈 10의 Recalculate를 실행하면 Current Week 기준 모듈 1~8의 현재 정보로 모듈 9·10을 재계산한다. (Ⅳ-7-1)
예: Material L/T 수정 → Save → Recalculate → Scheduled Receipt 자동계산 및 모듈 9·10 재계산
과거 Week Snapshot은 재계산하지 않는다.
────────────────────
[15. 권한]
────────────────────
Ⅴ-1 권한 Matrix를 따른다.
Admin: 조회, 검색, Filter, Download, Excel Upload, 화면 수정·Save (Status 포함)
Master: 조회, 검색, Filter, Download
User: 조회, 검색, Filter, Download
Guest: 조회, 검색, Filter, Download
Save, Upload 버튼은 Admin 외 사용자에게 비활성화한다.
Backend에서도 권한을 검증한다.
────────────────────
[16. Audit Data]
────────────────────
DB 내부 관리 예:
created_at
created_by
updated_at
updated_by
inactive_at
inactive_by
version (Optimistic Lock용)
DateTime은 UTC 저장.
화면 표시는 사용자 Local Timezone 기준.
────────────────────
[17. Acceptance Criteria]
────────────────────
화면 신규 Code 등록 불가
신규 Code는 Admin Excel Upload만 가능
Material Code는 Material Master 내 중복 차단
Code는 앞뒤 공백 제거 + 영문 대문자로 저장·비교

Unit은 필수이며 허용 값만 저장 (소문자 입력도 대문자로 변환)
Purchaser ID는 등록된 사용자 ID만 허용, 화면에는 이름 표시
L/T는 1 이상의 정수, 필수
허용 Field만 화면 수정
체크박스 다중 선택, 수정 시 자동 선택
동시 수정 시 나중 저장자에게 충돌 안내 (Optimistic Lock)
숫자로 저장된 Code도 문자열로 처리
지정 시트명만 읽고, 1행 Header 규칙 적용

Upload Type ③(Inactive)은 파일 내 Code만 처리한다
Excel 내 Code 2회 이상은 Error, 엑셀 수정 후 재업로드 안내
Inactive 처리 (Delete 기능 없음)
Status 필터 기본값 Active, All / Active / Inactive 선택 후 Search로 조회
부분검색 동작 (대소문자 무시)
현재 조회조건 전체 Excel Download, Status 포함
빈 Excel Cell = NULL
Validation Error 시 Upload 전체 중단
Upload Transaction Rollback
Admin만 관리 가능
Master/User/Guest는 조회·Download만 가능 (Save·Upload 버튼 비활성화)
Backend 권한검증
작업 주차 Dropdown 미표시
※ Current Week, 작업 주차, Recalculate 관련 항목은
Master Data 전용이 아니라 공통 기능(Ⅳ-6, Ⅳ-7)의 Acceptance Criteria로 관리한다.
────────────────────
Ⅵ-2. 두번째 기능 Module _ Assy Master
────────────────────
[1. 기능 / 업무 목적]
Assy Master 는 시스템에서 사용하는 Assy의 기준정보를 관리한다.
화면 UI:
'스크린샷 02.png'
(단, 화면 Column 구성은 본 절의 [3. 데이터 구성]이 우선한다.)
다음 Module의 공통 기준정보로 사용한다.
BOM
Safety Stock
Inventory
RTF/Production
Material Requirement
Material PSI
Assy Master 는Code 및 기준속성의
Single Source of Truth이다.
다른 Module의 Code 확인 기준:
Assy를 사용하는 Data
(BOM 상위, RTF, Production Plan, Safety Stock, Assy 재고)
→ Assy Master의 Customer Code와 비교
Code 비교는 Ⅵ-2-4의 Code 정규화(앞뒤 공백 제거, 영문 대문자 변환)를
적용한 값으로 한다.
다른 Module Data가 Assy Master 와 충돌할 경우
시스템이 임의로 다른 Data를 수정하지 않는다.
Validation Error를 발생시킨다.
────────────────────
[2. Key 규칙]
────────────────────
Customer Code는 Assy Master 안에서 중복 불가.
Material과 Assy Code를 겸하는 Code는 공존을 허용한다.
예:
Assy Master:
Customer Code = 4605000219
Assy Code     = MGMZ21022
Material Master:
Material Code = MGMZ21022
Assy의 Key(Customer Code)와 Material의 Key(Material Code)가 서로 다르므로
두 Data는 충돌하지 않는다.
Assy Code와 같은 값의 Material Code가 존재해도 Error로 처리하지 않는다.
Assy Code는 Key가 아니므로 중복을 허용한다. (확정)
하나의 Assy Code에 여러 Customer Code가 연결될 수 있다.
────────────────────
[3. 데이터 구성]
────────────────────
Excel Upload (시트명 고정, Ⅳ-5-1 및 Ⅶ 참조):
시트 'MD_Assy':
Customer Code
Assy Code
TYPE
Model
Item
Customer
Country
update와 Status는 Upload Column으로 받지 않는다.
시스템이 관리한다.
[3-1. 화면 구성] (확정)
Table Column:
No
Customer Code
Assy Code
TYPE

Model
Item
Customer
Country
update
Status (맨 우측)
Assy Table에는 Purchaser, Vendor, L/T Column을 표시하지 않는다.
Row 선택은 체크박스 방식이다. (Ⅵ-2-9-1) 'No' Column은 Row 선택 Column 바로 다음에 둔다.(Ⅳ-3-2)

Excel Download:
현재 선택된 Table의 모든 Column (화면 구성과 동일)
No, 
Customer Code
Assy Code
Type
Model
Item
Customer
Country)
update
Status
────────────────────
[4. Field 정의]
────────────────────
[4-0. Code 정규화] (확정)
Customer Code, Assy Code는
다음과 같이 정규화하여 저장하고 비교한다.
앞뒤 공백 제거
영문은 대문자로 변환하여 저장
(예: 'smaz13001' → 'SMAZ13001', 두 값은 같은 Code)
그 외 문자는 제한하지 않는다.
(숫자, '-', '_', 공백, 괄호, '' 등 허용.
예: 'MAGNET D33T', '304060006 (AVBS)-1')
숫자로 저장된 Excel 값도 문자열로 변환한다.
Assy의 Unit은 'EA'로 고정되며, 시스템에서 Unit을 별도로 표기하지 않는다. Assy에는 Unit 관련 Validation을 두지 않는다.
① Customer Code (Assy Master)
Assy의 Unique Key
문자열, Ⅵ-2-4-0 정규화 적용
빈 값 불가
Assy Master 내 중복 불가
화면 신규입력 불가
화면 수정 불가
신규등록은 Admin Excel Upload만 가능

② Assy Code (Assy Master)
노바텍 내부 Assy 관리번호
참고 속성 (Key 아님, 중복 허용)
문자열, Ⅵ-2-4-0 정규화 적용
화면 수정 가능
Excel Upload 가능

③ Type
Assy 제품군 구분
(예: Shield Magnet, Epoxy Plate, Magnet, Magnet Bar, MPP, Halbah, MPS)
직접입력

④ Model
사양 (적용되는 Customer제품)
문자열
일반 규격 특수문자 허용
화면 수정 가능
Excel Upload 가능

⑤ Item
품명
문자열
화면 수정 가능
Excel Upload 가능


⑥ Customer
직접입력
⑦ Country
Assy:
생산법인 소재국가
직접입력
⑧ update 
시스템 자동 생성
사용자 수정 불가
화면에서는 사용자 Local Timezone 기준으로 표시한다.
DB 저장은 UTC 기준으로 관리한다.
[권장안] 실제로 값이 변경된 행만 update를 갱신한다.

⑨ Status
Active
Inactive
시스템 관리
Admin이 화면에서 Row 선택 후 Active / Inactive를 선택하여 변경 가능(변경후 Save). Upload Column이 아님
Inactive 처리 (Delete 기능 없음)
Physical Delete 금지

────────────────────
[5. Validation]
────────────────────
Customer Code    필수
Assy Code        가능
Type             가능
Model            가능
Item             가능
Customer         가능
Country          가능
Rule 위반 시
자동수정하지 않고 Validation Error.
────────────────────
[6. Excel Upload]
────────────────────
Upload 대상 시트 'MD_Assy' → Assy Master에만 영향.
Upload Type 3종 (팝업에서 선택 후 Confirm, Ⅵ-1-6과 동일 규칙, Code는 Customer Code 기준):
① Add(등록): Upload Customer Code가 DB에 없는 신규 Code이면 추가 등록(Status = Active). DB에 이미 존재하면 엑셀 데이터를 무시(건너뛰기).
② Change(수정): Upload Customer Code가 DB에 존재하면 Upload 정보로 덮어쓰고 Status를 Active로 설정. DB에 없으면 신규 등록.
③ Inactive(삭제): Upload Customer Code가 DB에 존재하면 Status를 Inactive로 변경(엑셀 내 나머지 값 무시). DB에 없으면 무시.
Excel 빈 Cell은 Change에서 NULL로 처리한다.

DB 반영 전 신규등록 예정 / 수정 예정(변경 Field 표시) / Inactive 예정 / 무시 예정 / 재활성화 예정 건수를 표시하고 사용자 확인을 받는다.

Excel Upload Type ③의 경우: Assy Master에 없는 경우 무시, Assy Master에 있고 Active인 경우 Inactive로 변경

────────────────────
[7. Excel Upload Validation]
────────────────────
Upload 후 즉시 DB 저장하지 않는다.
Upload → Validation 결과 표시 → 사용자 [반영] 클릭 → DB 저장
순서로 처리한다.

Validation:
지정 시트 존재 여부
필수 Column
Column Name
Code 빈 값
Excel 내부 Code 중복 (정규화 후 기준)
허용 Field
병합 셀 여부
지수표기 등 손상된 Code

Upload Type ③ Inactive 시 사용 중인 Code도 전환을 허용한다. (Ⅵ-2-6, B-7 확정)
앞뒤 공백 제거.
빈 Cell = NULL
"-" = NULL

Validation 결과:
총 건수
정상 건수
Error 건수
시트명
Excel Row
Code
Error Field
Error 사유

Validation 결과를 Excel로 Download할 수 있도록 한다.
Error가 하나라도 있으면
전체 DB 반영 중단.
DB 반영은 Transaction 처리.
중간 Error 발생 시
전체 Rollback.

────────────────────
[8. 화면 조회 / 정렬]
────────────────────
기본 정렬:
Assy Table: Customer Code 오름차순
상하/좌우 Scroll 제공.
작업 주차 Dropdown은 표시하지 않는다. (Ⅳ-6-2)
────────────────────
[9. 화면 수정]
────────────────────
수정 불가:
Customer Code
update

수정 가능:
Assy Code
Type
Model
Item
Customer
Country
Admin만 수정 가능: Row 선택 후 Status (Active / Inactive 드롭다운) 변경 후 Save로 반영

[9-1. Row 선택 및 수정] (확정, 수정 파일 반영)
Admin은 화면 맨 좌측의 Row 선택 Column(체크박스)으로 Row를 선택한다. 여러 Row를 동시에 선택할 수 있다.

작동 순서: Row 선택 → 수정 가능 Data 활성화 → Data 수정 → 'Save' 클릭
수정 가능 Data(7가지): Assy Code, Type, Model, Item, Customer, Country, Status
값을 수정하면 해당 Row가 자동으로 선택된다.
행을 선택(체크)하면 해당 행의 수정 가능 셀을 반전 표시하여 수정 가능한 셀임을 구분할 수 있게 한다. (Ⅳ-3-6, 2026-11 확정)
Save는 선택된 Row만 저장한다.
Save하지 않은 수정내용이 있는 상태에서 화면 이동 시 경고를 표시한다.
동시 편집 충돌은 Ⅰ-11(Optimistic Lock)을 따른다.


────────────────────
[10. Inactive 처리]
Physical Delete 금지. 화면에 Delete 버튼을 두지 않는다.
Inactive 전환 경로는 두 가지다.
① Admin 화면: Row 선택 → Status를 Inactive로 변경 → Save
② Excel Upload: Upload Type ③ Inactive
Inactive 시 update 갱신.
기본화면에는 Inactive 미표시 (Status 필터 기본값 Active).
과거 Data 참조관계 유지.
재활성화: Upload Type ② Change, 또는 Admin 화면에서 Status를 Active로 변경 후 Save.
────────────────────
[11. Filter]
Status 필터: 드롭다운 All / Active / Inactive (기본값 Active)
Active: Active Row만 조회
All: Active + Inactive 조회
Inactive: Inactive Row만 조회
Status 필터는 검색조건·검색어와 함께 적용하며, Search 클릭 시 실행한다.
Inactive Row는 Status 열로 식별 가능하게 표시한다.
────────────────────
[12. 검색]
────────────────────
검색조건은 현재 Column 중에서 선택한다.
Default: Customer Code
검색대상: Customer Code, Assy Code, Type, Model, Item, Customer, Country
부분일치 검색. 영문 대소문자 구분 없음.
Status 필터 + 검색조건 + 검색어를 함께 적용하며, Search 클릭 시 실행한다.
────────────────────
[13. Excel Download]
────────────────────
Status(All / Active / Inactive) + 검색조건 + 검색어를 반영한 전체 조회결과 Download.
화면에 일부만 보여도 해당 조건의 전체 Row Download.
Column:
Customer Code, Assy Code, Type, Model, Item, 
Customer, Country, update, Status
Download File의 Column 구성을 화면 Column을 그대로 Download → 수정 → 다시 Upload가 가능하도록 한다.
업로드 양식에 없는 Column(update, Status Column)등은 Upload 시 무시
────────────────────
[13-1. History Download]
────────────────────
조회 조건: 화면 검색 결과 기준 (Status 필터 + 검색조건 + 검색어로 조회된 Customer Code 목록)
결과: 검색 결과에 해당하는 Assy의 과거 변경 이력 전체를 Excel로 다운로드한다.
기존 Download Column 양식을 그대로 따르며, 각 행의 update를 yyyy-mm-dd hh:mm(사용자 Local Timezone)으로 표기하여 변경 시점별로 구분한다.
이력 행의 Desc., Spec. 등 표시 항목은 해당 변경 시점의 값을 그대로 표시한다.
팝업(Customer Code·기간 조건)은 두지 않는다.
────────────────────
[14. Recalculate와 Assy Master 변경]
Assy Master 수정 후 Save해도 다른 Module의 계산결과는 즉시 자동 변경되지 않는다.
화면에 "● Need Recalculation" 알림을 표시한다. (Ⅳ-7-2)
Admin이 모듈 10의 Recalculate를 실행하면 Current Week 기준 모듈 1~8의 현재 정보로 모듈 9·10을 재계산한다. (Ⅳ-7-1)
예: Assy Master의 Customer Code 신규 등록 또는 Status 변경 → Save → Recalculate → 모듈 9·10 재계산 (BOM은 Assy Status와 독립이므로 제외)
과거 Week Snapshot은 재계산하지 않는다.
────────────────────
[15. 권한]
────────────────────
Ⅴ-1 권한 Matrix를 따른다.
Admin: 조회, 검색, Filter, Download, Excel Upload, 화면 수정·Save (Status 포함)
Master: 조회, 검색, Filter, Download
User: 조회, 검색, Filter, Download
Guest: 조회, 검색, Filter, Download
Save, Upload 버튼은 Admin 외 사용자에게 비활성화한다.
Backend에서도 권한을 검증한다.
────────────────────
[16. Audit Data]
────────────────────
DB 내부 관리 예:
created_at
created_by
updated_at
updated_by
inactive_at
inactive_by
version (Optimistic Lock용)
DateTime은 UTC 저장.
화면 표시는 사용자 Local Timezone 기준.
────────────────────
[17. Acceptance Criteria]
────────────────────
화면 신규 Code 등록 불가
신규 Code는 Admin Excel Upload만 가능
Customer Code는 Assy Master 내 중복 차단
Assy Code 중복 허용
Assy Code와 같은 값의 Material Code 공존 허용
Code는 앞뒤 공백 제거 + 영문 대문자로 저장·비교
허용 Field만 화면 수정
체크박스 다중 선택, 수정 시 자동 선택
동시 수정 시 나중 저장자에게 충돌 안내 (Optimistic Lock)
숫자로 저장된 Code도 문자열로 처리
지정 시트명만 읽고, 1행 Header 규칙 적용
전체교체는 Upload Type ③ Inactive 처리 범위를 파일 내 Code로 한정
Inactive 처리 (Delete 기능 없음)
Status 필터 기본값 Active, All / Active / Inactive 선택 후 Search로 조회
부분검색 동작 (대소문자 무시)
Inactive + 검색 동시사용
현재 조회조건 전체 Excel Download, Status 포함
빈 Excel Cell = NULL
Validation Error 시 Upload 전체 중단
Upload Transaction Rollback
Admin만 관리 가능
Master/User/Guest는 조회·Download만 가능 (Save·Upload 버튼 비활성화)
Backend 권한검증
작업 주차 Dropdown 미표시
※ Current Week, 작업 주차, Recalculate 관련 항목은
Master Data 전용이 아니라 공통 기능(Ⅳ-6, Ⅳ-7)의 Acceptance Criteria로 관리한다.

────────────────────
Ⅵ-3. 세번째 기능 Module _ BOM
────────────────────
(2026-11-24 정리본. 기존 [작성 중] 내용을 Module 4~10과 같은 형식으로 재구성했다. 확정 대기 항목 없음.)

[1. 기능 / 업무 목적]
BOM은 Assy 1개를 생산하기 위해 필요한 Material 구성과 소요원수(Q'ty)를 관리한다.
BOM은 Module 9(Material Requirement) 계산의 기준 데이터이다.
화면 UI: '스크린샷 03.png' (화면 Column 구성은 본 절의 [3. 데이터 구성]이 우선한다.)

[2. BOM 구조]
Level 0 = Assy (Customer Code), Level 1 = Material (Material Code)만 사용한다. Multi-Level BOM은 사용하지 않으므로 Level 표기는 두지 않는다. (확정)
BOM Row는 시스템 내부 고유 식별자(BOM Line ID)를 가진다. 사용자가 입력하지 않는다.

[3. 데이터 구성]
[3-1. 화면 Column] (스크린샷 03 기준)
순서: No / Cust. Code / Mat. Code / Desc. / Spec. / Unit / Q'ty / Type / Model / Item / Update / Status
헤더 색상 (Ⅳ-3-5):
  파란색 = 엑셀 업로드 Column: Cust. Code, Mat. Code, Unit, Q'ty
  회색 = Master 참조 또는 시스템 표시 Column: Desc., Spec., Type, Model, Item, Update, Status
Assy 행 (Assy 열): Cust. Code 행 전체를 굵은 글씨와 옅은 회색 배경으로 강조한다. (Ⅳ-3-6)
  Type, Model, Item은 Assy Master 값을 표시하고, Desc., Spec., Unit, Q'ty는 빈 칸이다.
자재 행 (Material 열): Desc., Spec.은 Material Master, Type, Model, Item은 Assy Master 값을 표시한다.
Status: Assy 행은 Assy Master의 Status, 자재 행은 Material Master의 Status를 표시한다. (Ⅳ-3-1)
화면에서 BOM을 등록·수정·삭제할 수 없다. (Ⅳ-3-0)

[4. Field 정의]
Cust. Code  Upload 필수, 문자열, 공백 불가. Assy Master 존재 여부 및 Assy Status와 무관하게 BOM 등록 가능
Mat. Code   Upload 필수, 문자열, 공백 불가. 'ASSY'는 자재 코드로 사용 불가 (Ⅶ-5). Material Master 존재 여부 및 Material Status와 무관하게 BOM 등록 가능
Unit        자재 행 필수, Material Master의 Unit과 같아야 함 (불일치 Error, 2026-11 확정). Assy 행은 무시
Q'ty        자재 행 필수, 0보다 큰 수, 정수 또는 분수 문자열 허용. Assy 행은 무시
Update      같은 Assy의 모든 행은 같은 Update 값(BOM 최종 Upload 시각)을 가진다. 저장: yyyy-mm-dd hh:mm (UTC 저장, Local 변환). 화면 표시: yyyy-mm-dd

[5. Key 규칙]
하나의 Assy BOM은 Assy 열 1개와 그 아래 연속된 자재 열들로 구성한다. 같은 Customer Code의 행은 반드시 연속되어야 한다.
Customer Code + Mat. Code는 Unique Key가 아니다. 같은 Assy 안에서 같은 Material이 여러 행에 있는 것을 허용한다.
  예) Assy A의 Material M이 Q'ty 0.5와 0.3으로 두 행 있으면, 두 행 모두 정상 Data이며 총 소요원수는 0.8이다. (반제품 조립과 단품 직접 투입 등 용도가 다를 수 있음)
  자동 병합하지 않는다. 원본 BOM Row는 그대로 저장하고, Module 9 계산 시 모든 Row를 포함한다.
Assy 열 식별: Mat. Code가 'Assy'(정규화 후)인 행만 Assy 열로 인정한다. Assy 열의 Unit·Q'ty 값은 무시한다.

[예시 1: 정상 Upload]
Cust. Code     | Mat. Code      | Unit | Q'ty
GH00-00000B    | Assy           |      |          ← Assy 열 (새 BOM 시작)
GH00-00000B    | 자재코드 1     | EA   | 1
GH00-00000B    | 자재코드 2     | G    | 1/200
GH00-00000B    | 자재코드 3     | MM   | 0.5
GH00-00000B    | 자재코드 4     | EA   | 4
GH00-00000B    | 자재코드 3     | MM   | 0.3      ← 같은 Assy의 같은 자재 (허용)

[예시 2: 에러 - Assy 불연속]
GH00-00000B 행 뒤에 GH11-11111B 블록이 나온 뒤 다시 GH00-00000B 행이 나오면 Error. (같은 Customer Code는 연속되어야 함)

[예시 3: 에러 - Assy 열 없이 자재 열 시작]
GH11-11111B의 Assy 열 없이 자재 열이 나오면 Error.

[6. Customer Code와 Material Code가 Master에 없는 경우]
Upload는 허용한다. (Ⅰ-8 예외, 확정)
Customer Code가 Assy Master에 없으면 Assy 행의 Status를 'No DB'로 표시하고, 그 Assy의 Type, Model, Item은 빈 칸으로 둔다. (스크린샷 03_No DB)
Material Code가 Material Master에 없으면 자재 행의 Desc., Spec.을 빈 칸으로 둔다. 자재 행의 Status는 'No DB'로 표시한다. (스크린샷 03_No DB)
자재 행의 Unit은 Material Master 기준으로 비교할 수 없으므로, Material Master가 없으면 Unit 불일치 검사를 생략하고 Upload 값을 저장한다. (Warning으로 목록 표시)

[7. Validation]
시트 'BOM' 존재 여부 (없으면 Error, Ⅳ-5-1)
필수 Column 4개(Cust. Code, Mat. Code, Unit, Q'ty) Header 존재 여부 (없으면 Error)
Cust. Code 빈 값 (Error), Mat. Code 빈 값 (Error)
Mat. Code 정규화 후 'ASSY'를 자재 코드로 사용 (Error, Ⅶ-5)
같은 Cust. Code 행이 불연속 (Error)
Assy 열 없이 자재 열이 나타남 (Error)
같은 Cust. Code의 Assy 열이 파일 내 2회 이상 (Error)
자재 열 Unit이 Material Master Unit과 다름 (Error)
자재 열 Q'ty가 0 이하이거나, 숫자·분수로 변환할 수 없음 (Error)
Q'ty가 Excel 날짜로 인식됨 (Error, [9. Q'ty 표기와 Excel 날짜 변환] 참조)
지수표기 등 손상된 Code (Error, Ⅳ-5-1)
병합 셀 존재 (Error, Ⅳ-5-1)
자재 열이 없는 Assy (Assy 열만 존재) (Error가 아니라 무시, 기존 BOM 유지, 결과에 '무시된 Assy 수' 표시)
완전히 빈 행 (무시, Ⅳ-5-1)
동일 Cust. Code + Mat. Code 행의 중복 (Error가 아님, [5. Key 규칙])
Assy Master 또는 Material Master에 없는 Code (Warning, 'No DB' 표시)

[8. Excel Upload와 Upload Type]
Upload Type 2종을 팝업에서 선택한 후 파일을 선택한다. (스크린샷 03 Pop up, 확정)
① Add(등록): Cust. Code가 기존 BOM에 없으면 신규 BOM으로 추가한다. 기존 Cust. Code는 엑셀 내용을 무시하고 건너뛴다.
② Change(변경): Cust. Code가 기존 BOM에 있으면 기존 BOM 전체를 History로 보관한 뒤, 엑셀의 BOM으로 교체한다.
③ 삭제는 없다. BOM은 삭제하거나 Inactive 처리하지 않는다.
④ Change는 파일에 포함된 Assy만 교체한다. 파일에 없는 Assy의 BOM은 유지한다.
⑤ 자재 열이 없는 Assy는 BOM으로 등록하지 않고 무시하며 기존 BOM을 유지한다.
Assy Status 전환은 BOM 등록·변경·History에 영향을 주지 않는다.
Upload 방식: Admin만 가능하다. (Ⅴ-1 권한 Matrix)
Validation Error가 1건이라도 있으면 전체 반영을 중단하고 Transaction을 Rollback한다.
동일 내용을 재Upload한 Assy는 이력을 새로 만들지 않는다.
Validation 결과 항목: 총 Assy 수, 정상 Assy 수, Error 건수, Warning 건수, 무시된 Assy 수(자재 열 없음), 시트명, Excel Row, Cust. Code, Mat. Code, Error Field, Error 사유. Validation 결과는 Excel로 Download할 수 있다.

[9. Q'ty 표기와 Excel 날짜 변환] (확정)
화면 표기: 분수로 표시한다. 예: 1/50, 1/1,000. 1 이상의 정수는 그대로 표시한다. 예: 1, 2.
  분모가 정수가 되지 않는 값(예: 0.014)은 기약분수(7/500)로 표시하고, 분수로 표현하기 어려우면 소수로 표시한다.
Excel Upload: 숫자(0.02)와 분수 문자열('1/50') 모두 허용하며 숫자로 변환하여 저장한다.
저장: 분수(분자/분모)를 우선한다. 분수로 저장할 수 없으면 소수점 10째 자리까지 저장한다. (Q-1 확정)
Excel 날짜 자동 변환: Q'ty 셀이 날짜로 인식되면(예: 1/50이 날짜로 바뀜) Upload Error. 안내 문구: '텍스트 서식으로 입력하거나 소수(예: 0.02)로 입력'.

[10. 화면 조회 / 검색 / 정렬]
Assy Status 드롭다운: All / Active / Inactive / No DB (기본값 Active, 스크린샷 03 확정). Inactive·No DB Assy는 기본 화면에서 숨긴다.
검색 조건: ① Cust. Code / Mat. Code 중 선택 → ② 검색어 → ③ Search 클릭 (부분검색, 대소문자 무시)
  Cust. Code 검색은 해당 Assy 전체 BOM을, Mat. Code 검색은 그 자재를 포함하는 Assy의 BOM을 표시한다. (스크린샷 03_Search)
Material Status(Inactive)는 Filter 대상이 아니며 자재 행의 Status 열로만 표시한다.
기본 정렬: Cust. Code 오름차순. 같은 Assy 안에서는 Assy 행을 먼저, 자재 행은 BOM Line ID 순서(업로드 순서)로 표시한다.
화면에는 Assy별 현재(최신) BOM만 표시한다. 과거 이력은 History Download에서만 조회한다.
작업 주차 Dropdown은 표시하지 않는다. (Ⅳ-6-2)
상하·좌우 Scroll을 제공한다.

[11. Excel Download와 History]
Excel Download: 검색 조건(Assy Status + 검색조건 + 검색어)에 해당하는 전체 Row를 내려받는다. 화면에 일부만 보여도 전체 Row를 포함한다.
  Column: Cust. Code, Mat. Code, Desc., Spec., Unit, Q'ty, Type, Model, Item, Update, Status
History Download: 화면 검색 결과에 해당하는 Assy의 과거 BOM 이력을 Excel로 내려받는다. (팝업 없음)
  Assy 단위로 BOM(Assy 열 + 자재 열)을 Update 기준으로 나열하며, Update는 yyyy-mm-dd hh:mm(Local Timezone)으로 표기한다.
  이력 행의 Desc., Spec., Type, Model, Item은 해당 Update 시점의 값을 그대로 표시한다. (현재 Master 값으로 바꾸지 않는다)
Download 값은 원본 값(Q'ty 분수 표기 규칙 동일)이다.

[12. 반영 시점과 재계산] (Ⅳ-7-0 3계층 규칙)
BOM 원본은 Upload 시 즉시 저장한다. (계층 1)
Type, Model, Item, Desc., Spec., Status는 조회 시 Master 값으로 실시간 표시한다. (계층 2)
Module 9·10 계산 결과는 Recalculate 실행 시 갱신한다. 실행 전까지 "● Need Recalculation"을 표시한다. (계층 3, Ⅳ-7-2)
Recalculate 실행: Admin만 가능 (Module 10 화면). 과거 주차 Snapshot은 재계산하지 않는다. (Ⅳ-6-5)
Inactive Assy 수량과 Inactive Material 행은 Module 9 계산에 포함하며, Warning 목록으로 표시한다. (F-9, Ⅵ-9 [5])

[13. 권한]
BOM Upload(Add / Change): Admin만 가능. Backend에서 검증한다.
화면 수정·저장·삭제: 모든 사용자 불가 (Admin 포함). BOM은 Excel Upload로만 변경한다.
조회, 검색, Excel Download, History Download: Admin, Master, User, Guest 모두 가능.

[14. Audit Data] (DB 내부 관리 예)
bom_line_id (BOM Row 고유 Key), cust_code, mat_code, unit, qty (분수 또는 소수 10째 자리)
snapshot: desc, spec, type, model, item (Upload 시점 값, History 표시 기준)
upload_batch_id, uploaded_at (UTC), uploaded_by, source_filename, update
created_at, created_by
DateTime은 UTC 저장, 화면과 Download 표시는 사용자 Local Timezone 기준.

[15. Acceptance Criteria]
① Mat. Code가 'Assy'인 행은 Assy 열로 인식되며, 그 행의 Unit·Q'ty 값은 무시된다.
② Cust. Code는 Assy Master의 존재 여부와 Assy Status와 무관하게 BOM 등록이 가능하다.
③ Mat. Code는 Material Master의 존재 여부와 Material Status와 무관하게 BOM 등록이 가능하다.
④ 'ASSY'는 자재 코드로 사용할 수 없다.
⑤ 같은 Cust. Code + Mat. Code 행은 허용되며, 자동 병합되지 않는다.
⑥ 자재 행의 Unit이 Material Master와 다르면 Error로 Upload가 중단된다.
⑦ Q'ty가 0 이하이거나 변환할 수 없거나 Excel 날짜로 인식되면 Error이다.
⑧ 불연속 Cust. Code 또는 Assy 열 없는 자재 열은 Error이다.
⑨ 자재 열이 없는 Assy는 무시되며, 기존 BOM은 유지된다.
⑩ Change는 파일에 포함된 Assy만 교체하고, 교체 전 BOM은 History로 보관된다.
⑪ 파일에 없는 Assy의 BOM은 유지된다.
⑫ Error가 1건이라도 있으면 전체 반영이 중단되고 Rollback된다.
⑬ 같은 Assy의 모든 행은 같은 Update 값을 가진다. 화면은 yyyy-mm-dd, Download와 History는 yyyy-mm-dd hh:mm으로 표시한다.
⑭ History 행의 Desc., Spec., Type, Model, Item은 이력 시점 값으로 표시된다.
⑮ Assy Master 또는 Material Master에 없는 Code는 'No DB'로 표시되고 업로드가 완료된다. 해당 Desc., Spec., Type, Model, Item은 빈 칸이다.
⑯ 화면에서 BOM을 등록, 수정, 삭제할 수 없다.
⑰ Upload는 Admin만 가능하다. Master, User, Guest는 Backend에서도 거부된다.
⑱ Excel Download는 화면 검색 결과의 전체 Row를 포함한다.
⑲ 작업 주차 Dropdown은 표시되지 않는다.

────────────────────
Ⅵ-4. 네번째 기능 Module _ Safety Stock
────────────────────

[1. 기능 / 업무 목적]
Safety Stock(안전재고)은 Assy 단위로 고객사별 안전재고 수량을 관리한다. (Ⅶ-6, 확정)
Material은 Safety Stock을 운영하지 않는다. (Assy 기준 관리)
등록된 Safety Q'ty는 RTF 기준 14주차(W+13)에 자동 반영되어 소요량으로 계산된다. (Ⅲ-4-1)
Production Plan 기준에는 반영하지 않는다.
화면 UI: '스크린샷 04.png' (화면 Column 구성은 본 절의 [3. 데이터 구성]이 우선한다.)

[2. Key 규칙]
Key: Customer Code (Excel 내 중복 불가, Ⅶ-6)
Customer Code 비교는 Ⅵ-2-4의 Code 정규화(앞뒤 공백 제거, 영문 대문자 변환)를 적용한다.
Assy 기준정보(Assy Code, Type, Model, Item, Customer)는 Assy Master에서 조회하여 표시하며, Safety Stock 자체에는 저장하지 않는다. (Ⅵ-2 Single Source of Truth)
Assy Master에 없는 Customer Code는 'No DB'로 표시한다. 업로드는 허용한다. (Ⅰ-8 예외, 확정)

[3. 데이터 구성]
[3-1. 화면 Column] (스크린샷 04 기준, 확정 예정)
순서: No / Cust. Code / Assy Code / Type / Model / Item / Customer / Safety Q'ty / Update / Status
헤더 색상 (Ⅳ-3-5):
  파란색 = 엑셀 업로드 Column: Cust. Code, Safety Q'ty
  회색 = Assy Master 참조 Column: Assy Code, Type, Model, Item, Customer
  회색 = 시스템 표시 Column: No, Update, Status
Status 열은 맨 우측에 표기하며 'Active / Inactive / No DB' 중 하나를 표시한다. (Ⅳ-3-1)
Status는 Assy Master의 Status를 따르며, Safety Stock 화면에서 직접 변경하지 않는다.
'Weeks' Column은 사용하지 않는다. (Ⅶ-6)
화면 수정 기능은 없다. Save 버튼과 Row 선택 Column을 두지 않는다. (Ⅳ-3-0)

[4. Field 정의]
Cust. Code     Upload 필수, 문자열, 공백 불가, Excel 내 중복 불가
Safety Q'ty    Upload 필수, 0 이상의 정수, 빈 Cell = 0, 음수·소수·텍스트 불가 (M4-1 확정: 소수 불필요)
Update         시스템 자동 기록, 해당 Row가 실제로 변경된 Upload 시각 (yyyy-mm-dd hh:mm, 사용자 Local Timezone, Ⅳ-6-4)
Status         시스템 표시 (Active / Inactive / No DB)

[5. Validation]
Upload 시 다음 항목을 검증한다. 자동 수정하지 않는다.
시트 'SAFETY' 존재 여부 (없으면 Error)
필수 Column 'Customer Code', 'Safety Q'ty' Header 존재 여부 (없으면 Error)
병합 셀 존재 (Error, Ⅳ-5-1)
Customer Code 공백 (Error)
Excel 내 Customer Code 중복 (Error, 합산하지 않음, Ⅶ-6)
Safety Q'ty가 0 또는 자연수가 아님, 음수, 소수, 텍스트 (Error)
지수표기 손상 Code(예: 3.04E+11) (Error, Ⅳ-5-1)
Excel 날짜 자동 변환으로 인식된 Safety Q'ty (Error, Ⅵ-3 규칙 동일)
Customer Code가 Assy Master에 없음 (Warning, 'No DB' 표시, 계산 포함)
Customer Code가 Assy Master에 있으나 Inactive (Warning, 목록 보고 후 계산 포함)
Customer Code의 BOM이 없음 (Warning, Ⅲ-4-3: 소요량 0 간주 후 계산 진행)

[6. Excel Upload]
Upload 방식: 파일 선택 후 전체교체. 일부 Code만 수정할 수 없다. (Ⅶ-6, Ⅳ-5)
Upload Type 선택 없음 (M4는 Add/Change 구분 없이 항상 전체교체).
시트명: SAFETY
Column: Customer Code / Safety Q'ty (파란색 Column만 포함, Ⅳ-3-5)
Upload Mode: Admin만 가능하다. (Ⅴ-1 권한 Matrix)
Upload 전 기존 Data 전체 행을 History에 보관한다. (Update 기준, Ⅶ-6)
동일 내용 재Upload 시 이력을 생성하지 않는다. 실제 변경된 Row만 Update 값을 갱신한다. (Ⅵ-3 규칙과 동일)
Excel 빈 Cell은 Safety Q'ty = 0으로 처리한다.
Validation Error가 1건이라도 있으면 전체 반영을 중단하고 Transaction을 Rollback한다.

[7. Excel Upload Validation 결과 표시]
표시 항목: 시트명, Excel Row, Customer Code, 항목명, 오류 사유, Error 건수, Warning 건수 (Ⅶ-10, Ⅳ-7-10)
Validation 결과는 Excel로 Download할 수 있다.

[8. 화면 조회 / 정렬]
기본 정렬: Cust. Code 오름차순 (M4-2 확정). 같은 Cust. Code가 없으므로 Key 중복은 발생하지 않는다.
화면 No Column은 정렬된 순서대로 1부터 부여한다.

[9. 검색 / Filter]
Status 필터 (M4-3 확정): ① Status 드롭다운(All / Active / Inactive / No DB, 기본값 Active)
검색 조건: ② 검색조건 Dropdown (Cust. Code / Assy Code / Type) → ③ 검색어 → ④ Search 클릭 시 실행
부분검색, 대소문자 무시 (Ⅵ-1-12 규칙과 동일)
Assy Code, Type 검색은 Assy Master의 값을 기준으로 한다.
Status 필터는 두며, Status 조건은 Search 실행 시 검색조건과 함께 적용한다.

[10. Excel Download]
화면 검색 결과(검색조건·검색어) 전체 Row를 Download한다. 화면에 일부만 보여도 전체 Row를 포함한다.
Download 양식은 Upload 양식(Customer Code, Safety Q'ty)과 맞추어, Download → 수정 → 재Upload가 가능하도록 한다.
(No, Assy Code, Type, Model, Item, Customer, Update, Status Column은 Upload 시 무시한다.)

[11. History]
History 버튼은 화면 우측 상단에 둔다. (Ⅳ-3-1)
Customer Code 기준 과거 Safety Q'ty 변경 이력을 조회하고 Excel로 Download한다.
History 조회는 화면 검색 결과 기준이며 팝업을 두지 않는다. (Ⅵ-3 History 규칙과 동일)
이력 Column: Customer Code, Safety Q'ty, Update (yyyy-mm-dd hh:mm), 변경 구분(추가 / 변경 / 삭제)

[12. 재계산(Recalculate) 및 계산 영향]
Safety Q'ty 변경은 Module 10 재계산 대상 Data 변경으로 본다. 저장 즉시 재계산하지 않으며, 화면에 'Need Recalculation'을 표시한다. (Ⅳ-7-2)
Safety Q'ty는 RTF 기준 14주차(W+13) 열에 합산된다. 자동 합산 값은 화면에서 수정할 수 없다. (Ⅲ-4-1, Ⅶ-8)
계산식: Safety 소요량 = Σ(Assy Safety Q'ty × BOM 소요원수)
Safety 소요량은 Material Requirement(Module 9) 계산 단계에서 Material 단위로 환산된다.
Assy Master에 없는 Customer Code(No DB)의 Safety Q'ty도 계산에 포함하며 Warning 목록에 표시한다. (Ⅰ-8 예외)
BOM이 없는 Assy는 소요량 0 간주 후 계산하고 Warning 목록에 표시한다. (Ⅲ-4-3)

[13. 권한]
Admin: 조회, 검색, Filter, Excel Download, History Download, Excel Upload (Ⅴ-1 권한 Matrix)
Master / User / Guest: 조회, 검색, Excel Download, History Download (Upload 버튼 비활성화)
Backend에서 권한을 검증한다. (Ⅴ-1-7)

[14. Audit Data]
Upload 시 다음을 기록한다: 사용자 ID, Upload 시각(UTC 저장, Local 표시), 파일명, 전체 Row 수, 신규·변경·동일·삭제 건수, Error/Warning 건수 (Ⅰ-9, Ⅵ-3 Audit 규칙 동일)

[15. Acceptance Criteria]
① Admin이 SAFETY 시트를 Upload하면 기존 Data 전체가 교체되고, 이전 값은 History에서 조회된다.
② Customer Code가 Excel 내 중복이면 Upload 전체가 중단되고 중복 행이 표시된다.
③ Safety Q'ty에 소수·음수·텍스트가 있으면 해당 행을 Error로 표시하고 Upload가 중단된다.
④ Assy Master에 없는 Customer Code는 'No DB'로 표시되고 Upload가 완료된다. Warning 목록에 포함된다.
⑤ 동일 내용을 다시 Upload하면 이력이 생성되지 않는다.
⑥ 화면에 Save 버튼과 수정 입력란이 없다.
⑥-1 Status 필터(All / Active / Inactive / No DB)와 Cust. Code 오름차순 정렬이 동작한다.
⑦ 14주차(W+13) 열에 Safety 값이 합산되어 RTF 계산에 반영된다. (Production Plan 기준에는 반영되지 않는다.)
⑧ Master·User·Guest 계정에서 Upload 버튼이 표시되지 않으며, 서버에서도 거부된다.

[16. 확정 사항 (2026-11)]
M4-1 (확정): Safety Q'ty는 0 이상의 정수만 허용한다.
M4-2 (확정): 기본 정렬은 Cust. Code 오름차순이다.
M4-3 (확정): Status 필터(All / Active / Inactive / No DB)를 추가한다. 모듈 3(BOM)도 동일하게 No DB 조건을 추가한다. (Ⅳ-3-1, Ⅳ-3-3)

────────────────────
Ⅵ-5. 다섯번째 기능 Module _ Inventory (재고)
────────────────────

[1. 기능 / 업무 목적]
Inventory는 작업 주차 월요일 아침 기준의 재고 수량을 Material·Assy 단위로 관리한다. (Ⅶ-7, 확정)
재고는 Stock Q'ty(TOTAL, 합계) 하나만 관리한다. ROH / WIP 구분은 두지 않는다.
재고는 작업 주차의 기초재고(Opening Inventory)로 사용한다. (Ⅲ-4-1)
화면 UI: '스크린샷 05.png' (화면 Column 구성은 본 절의 [3. 데이터 구성]이 우선한다.)

[2. Key 규칙]
Key: Category + Code (Excel 내 중복 불가, Category 구분 필수) (확정)
Code 비교는 Ⅵ-2-4의 Code 정규화(앞뒤 공백 제거, 영문 대문자 변환)를 적용한다.
Assy 재고의 Code는 Customer Code이다. Assy Master의 Customer Code와 비교한다.
Material 재고의 Code는 Material Code이다. Material Master의 Material Code와 비교한다.
Master에 없는 Code는 'No DB'로 표시하며 업로드는 허용한다. (Ⅰ-8 예외, 확정)

[3. 데이터 구성]
[3-1. 화면 Column] (스크린샷 05 기준)
순서: No / Category / Code / Unit / Stock Q'ty / Status / Type / Desc.
헤더 색상 (Ⅳ-3-5):
  파란색 = 엑셀 업로드 Column: Category, Code, Unit, Stock Q'ty
  회색 = 시스템 표시 Column: No, Status, Type / Desc.
Type / Desc.: Assy 행은 Assy Master의 Type 값을, Material 행은 Material Master의 Desc. 값을 자동 표시한다. (Ⅳ-3-5, 참조 전용)
Status 열은 맨 우측에 표기하며 Active / Inactive / No DB 중 하나를 표시한다. (Ⅳ-3-1)
Status는 Master Data의 Status를 따르며 Inventory 화면에서 직접 변경하지 않는다.
Unit, Stock Q'ty는 화면에서 수정할 수 없다. 화면 수정 기능과 Save 버튼은 없다. (Ⅳ-3-0)

[4. Field 정의]
Category     Upload 필수, 'Assy' 또는 'Material'만 허용 (대소문자 무시, 정규화 후 판단)
Code         Upload 필수, 문자열, 공백 불가
Unit         Material 행 Upload 필수, Material Master의 Unit과 같아야 함 (허용값: EA, SHEET, SET, G, KG, MM, M)
             Assy 행은 빈 칸 또는 'EA'만 허용. Assy는 EA로 고정한다. (Excel 양식 안내 기준)
Stock Q'ty   Upload 필수, 0 이상의 숫자, 소수점 6자리까지 허용, 빈 Cell = 0, 음수·텍스트·소수점 7자리 이상 불가 (IN-2 수정 확정)
Update       시스템 자동 기록 (yyyy-mm-dd hh:mm, 사용자 Local Timezone, Ⅳ-6-4). 화면 표시만 하며, 본 Module은 History를 두지 않는다.

[5. Validation]
시트 'INVENTORY' 존재 여부 (없으면 Error)
필수 Column 'Category', 'Code', 'Unit', 'Stock Q'ty' Header 존재 여부 (없으면 Error)
병합 셀 존재 (Error, Ⅳ-5-1)
Category가 'Assy' 또는 'Material'이 아님 (Error)
Category + Code 중복 (Excel 내, Error, 합산하지 않음)
Material 행의 Unit이 Material Master와 다름 (Error, 2026-11 확정: Unit 불일치는 Error)
Assy 행의 Unit이 빈 칸 또는 'EA'가 아님 (Error)
Stock Q'ty가 0 이상의 숫자가 아니거나 소수점 7자리 이상임 (Error, 자동 반올림하지 않음)
지수표기 손상 Code(예: 3.04E+11) (Error, Ⅳ-5-1)
Excel 날짜 자동 변환으로 인식된 Stock Q'ty (Error)
Code가 Master에 없음 (Warning, 'No DB' 표시, 업로드 허용)
Master에 있으나 Inactive (Warning, 목록 보고 후 계산에 포함)

[6. Excel Upload]
Upload 방식: 작업 주차의 기존 Data 전체를 파일로 대체한다. (Ⅶ-7, Ⅳ-5)
기존 Data는 삭제하며 History는 두지 않는다.
Upload Type 선택 없음.
시트명: INVENTORY
Column: Category / Code / Unit / Stock Q'ty (파란색 Column만 포함, Ⅳ-3-5)
Upload Mode: Admin만 가능하다. (Ⅴ-1 권한 Matrix)
과거 주차에는 Upload할 수 없다. 작업 주차 Upload만 허용한다. (Ⅵ-5 화면 표시 규칙, 스크린샷 05)
Excel 빈 Cell은 Stock Q'ty = 0으로 처리한다.
Validation Error가 1건이라도 있으면 전체 반영을 중단하고 Transaction을 Rollback한다.

[7. 재고 Upload 규칙]
재고 기준시점 = 작업 주차 월요일 아침 재고 (Ⅶ-7)
Material 재고는 RTF 기준, Production Plan 기준 모두 사용한다.
Assy 재고는 RTF 기준에만 사용한다. Assy 재고는 BOM 소요원수로 Material 환산하여 사용한다. (Ⅲ-4-1)
Assy 재고 Upload 후 Assy 단위 재고는 Assy Master 기준으로 저장한다.

[8. 화면 조회 / 정렬]
기본 정렬: Category(Assy → Material) 순, 같은 Category 안에서는 Code 오름차순.
조회 결과는 No 순으로 1부터 부여한다.

[9. 검색 / 작업 주차]
작업 주차 Dropdown: 기본값 'Current Week'의 작업 주차. 표기는 'W44(W0)' 형식이며 Module 5~10 공통 (IN-1 확정). 지난 16주까지 선택 가능 (Ⅳ-6-5)
검색조건: Code만 가능 (스크린샷 05 기준). Code 부분검색, 대소문자 무시.
검색 실행: 작업 주차 선택 → Code 입력 → Search 클릭
과거 주차를 선택하면 조회(Search)와 Download만 가능하며, Upload는 불가하다. (스크린샷 05 주석)
Status 필터는 두지 않는다. (IN-3 확정: 추가하지 않음)

[10. Excel Download]
선택한 작업 주차와 검색 조건(Code)에 해당하는 전체 Row를 Download한다.
Download 양식은 Upload 양식(Category, Code, Unit, Stock Q'ty)과 맞추어, Download → 수정 → 재Upload가 가능하도록 한다.
(No, Status, Type / Desc., Update Column은 Upload 시 무시한다.)

[11. 재계산(Recalculate) 및 계산 영향]
Inventory Upload 후 Module 10 재계산 대상 Data 변경으로 본다. 저장 즉시 재계산하지 않으며 'Need Recalculation'을 표시한다. (Ⅳ-7-2)
재고 값은 작업 주차의 기초재고로 Material Requirement(Module 9)·Material PSI(Module 10) 계산에 사용된다.
Assy 재고 중 Assy Master에 없는 Code(No DB)는 계산에 반영하고, Warning 목록으로 표시한다. (IN-4 확정)
사유: 개발 단계에서 샘플로 입고된 자재가 재고로 있으나 Master에는 아직 등록되지 않은 경우가 있으므로 계산을 막지 않는다.
Material 재고 중 Material Master에 없는 Code(No DB)도 동일하게 계산에 반영하고 Warning으로 표시한다.

[12. 권한]
Admin: 조회, 검색, Download, Upload (Ⅴ-1 권한 Matrix)
Master / User / Guest: 조회, 검색, Download (Upload 버튼 비활성화)
Backend에서 권한을 검증한다. (Ⅴ-1-7)

[13. Audit Data]
Upload 시 다음을 기록한다: 사용자 ID, Upload 시각(UTC 저장, Local 표시), 파일명, 작업 주차, 전체 Row 수, 신규·변경·동일·삭제 건수, Error/Warning 건수 (Ⅰ-9 감사 기록 원칙)

[14. Acceptance Criteria]
① Admin이 작업 주차 INVENTORY 시트를 Upload하면 해당 주차 기존 재고 Data가 전체 교체된다. 이전 Data는 조회할 수 없다.
② Category + Code가 Excel 내 중복이면 Upload 전체가 중단되고 중복 행이 표시된다.
③ Material 행의 Unit이 Material Master와 다르면 Error로 Upload가 중단된다.
④ Stock Q'ty에 음수·텍스트·소수점 7자리 이상이 있으면 Error로 Upload가 중단된다. 소수점 6자리 이하(예: 0.5)는 정상 저장된다.
⑤ Master에 없는 Code는 'No DB'로 표시되고 Upload가 완료된다.
⑥ 과거 주차를 선택하면 Upload 버튼이 비활성화되고, 조회와 Download만 된다.
⑦ 화면에 Save 버튼과 수정 입력란이 없다.
⑧ Master·User·Guest 계정에서 Upload 버튼이 표시되지 않으며, 서버에서도 거부된다.

[15. 화면 주석 정정 필요 (스크린샷 05)]
스크린샷 05 상단 주석 "선택한 행(Row) 삭제, 저장"은 Ⅳ-3-0(모듈 3~10은 Save·Delete 없음)과 충돌한다. 본 초안은 Inventory 화면 수정 기능이 없는 것으로 작성했다. 캡쳐 주석 정정이 필요하다.

[16. 확정 사항 (2026-11)]
IN-1 (확정): 작업 주차 표기는 'W44(W0)' 형식으로 Module 5~10 전체 통일한다. 화면 캡쳐도 재작성하여 다시 첨부한다.
IN-2 (수정 확정): Stock Q'ty는 0 이상의 숫자이며 소수점 6자리까지 허용한다 (예: 0.5 Kg). 초기 정수 결정은 소수 필요성 확인 후 변경되었다. 단위가 Kg인 Material은 소수 입력이 필요하다.
IN-3 (확정): Status 필터를 추가하지 않는다.
IN-4 (확정): No DB Code의 재고는 계산에 반영하고 Warning으로 표시한다.

────────────────────
Ⅵ-6. 여섯번째 기능 Module _ RTF / Production Plan
────────────────────

[1. 기능 / 업무 목적]
RTF(Return to Forecast, 고객 예측 기반 출하계획)와 Production Plan(생산계획, 약칭 Prod.)을 Assy 단위·14주 기준으로 관리한다. (Ⅲ-1, Ⅲ-2)
두 계획은 별도 시트로 Upload하고, 별도로 저장한다. (Ⅶ-8)
RTF 14주차에는 Safety Stock 수량이 자동 합산된다. Production Plan에는 합산하지 않는다. (Ⅲ-4-1)
화면 UI: '스크린샷 06.png' (화면 Column 구성은 본 절의 [3. 데이터 구성]이 우선한다.)

[2. Key 규칙]
Key: Customer Code (Plan 단위로 Excel 내 중복 불가, 중복 시 Error, 합산하지 않음) (Ⅶ-8)
Code 비교는 Ⅵ-2-4의 Code 정규화(앞뒤 공백 제거, 영문 대문자 변환)를 적용한다.
Assy Code, Type, Model, Item, Customer는 Assy Master에서 조회하여 표시하며, 본 Module에 저장하지 않는다. (Ⅵ-2 Single Source of Truth)
Assy Master에 없는 Customer Code는 'No DB'로 표시하며 업로드는 허용한다. (Ⅰ-8 예외, 확정)

[3. 데이터 구성]
[3-1. 화면 Column] (스크린샷 06 기준)
순서: No / Cust. Code / Assy Code / Type / Model / Item / Plan / W44(W0) / W45(W+1) / … / W04(W+13) / Status / No BOM
주차 Column: 14개. 14번째 열 Header는 'Safety(W+13)'로 표기한다. (F-4 확정)
헤더 색상 (Ⅳ-3-5):
  파란색 = 엑셀 업로드 Column: Cust. Code, Plan, 14개 주차 Column
  회색 = Assy Master 참조 Column: Assy Code, Type, Model, Item
  회색 = 시스템 표시 Column: No, Status, No BOM
Status 열은 우측에 표기하며 Active / Inactive / No DB 중 하나를 표시한다. (Ⅳ-3-1)
No BOM 열은 Status 우측에 둔다. BOM 미등록 Assy에만 'NO'를 표시하고, BOM이 있으면 빈 칸으로 둔다. (Ⅲ-4-3, 스크린샷 06 기준)
화면 수정 기능과 Save 버튼은 없다. (Ⅳ-3-0)

[4. Field 정의]
Cust. Code     Upload 필수, 문자열, 공백 불가, Plan 시트 내 중복 불가
Plan           Upload 필수. RTF 시트는 'RTF'만, PROD_PLAN 시트는 'Prod.' 또는 'Production'만 허용 (Ⅶ-8)
주차 Column    14개, Upload 필수. 빈 Cell = 0. 정수만 허용, 음수 불가 (IN-2 기준 통일)
14번째 주차    RTF 기준 행: 화면 값 = 업로드 수량 + Safety Stock (자동 합산, 화면 수정 불가)
               Production 기준 행: 화면 값 = 업로드 수량 (Safety 미반영)
Status         시스템 표시 (Active / Inactive / No DB), Master 기준
No BOM         시스템 표시 ('NO' 또는 빈 칸), 모듈 3(BOM) 기준으로 판정 (아래 [5] 참조)

[5. BOM 유무 판정] (스크린샷 06 주석 확정)
BOM 등록 기준: 모듈 3(BOM)에 해당 Customer Code의 Assy 열이 1개 있고, 이어서 Material 열이 1개 이상 있으면 등록(BOM 있음)으로 본다.
조건 미충족 시 No BOM = 'NO'로 표시한다. (Ⅲ-4-3)
BOM이 없는 Assy도 Upload는 막지 않는다. 계산 단계에서 소요량 0 간주 후 Warning 목록으로 표시한다.
Recalculate 결과에는 'BOM 미등록 n건'을 함께 표시한다. (Ⅲ-4-3)

[6. Validation]
시트 'RTF'와 'PROD_PLAN' 중 하나 이상 존재 여부 (둘 다 없으면 Error). 한쪽만 있으면 나머지는 [7-1]에 따라 자동 생성 (M6-1 확정)
필수 Column 'Customer Code', 'Plan', 14개 주차 Header 존재 여부 (없으면 Error)
병합 셀 존재 (Error, Ⅳ-5-1)
Customer Code 공백 또는 중복 (Error, 합산하지 않음, Ⅶ-8)
Plan 값이 시트 허용값과 다름 (Error, 예: RTF 시트에 'Prod.' 입력)
주차 Header가 작업 주차부터 연속된 14주가 아님 (Error, Ⅶ-2)
주차 값이 음수, 소수, 텍스트, 지수표기 손상 (Error)
Excel 날짜 자동 변환으로 인식된 수량 (Error, Ⅵ-3 규칙 동일)
Customer Code가 Assy Master에 없음 (Warning, 'No DB' 표시, 계산 포함)
Customer Code가 Assy Master에 있으나 Inactive (Warning, 목록 보고 후 계산 포함, Ⅲ-4-3 및 F-9와 동일 방식)
BOM 미등록 Assy (Warning, 소요량 0 간주, 'No BOM' = NO 표시)

[7. Excel Upload]
Upload 방식: 작업 주차의 기존 Data 전체를 파일로 대체한다. 기존 Data는 삭제하며 History는 두지 않는다. (Ⅶ-8, Ⅳ-5)
RTF와 PROD_PLAN은 각각 별도 파일 또는 별도 시트로 Upload하고, 각각 별도로 저장한다. (Ⅶ-8)
Upload Type 선택 없음.
시트명: RTF 또는 PROD_PLAN
Column: Customer Code / Plan / 14개 주차 (파란색 Column만 포함, Ⅳ-3-5)
Upload Mode: Admin만 가능하다. (Ⅴ-1 권한 Matrix)
과거 주차에는 Upload할 수 없다. 작업 주차 Upload만 허용한다. (스크린샷 06 주석)
Validation Error가 1건이라도 있으면 전체 반영을 중단하고 Transaction을 Rollback한다.

[7-1. 자동 생성 규칙] (M6-1 확정, 2026-11)
규칙 A. 한쪽 계획만 존재하는 경우
  Customer Code가 RTF 또는 Prod. 중 한쪽에만 있으면, 나머지 한쪽을 자동 생성하고 14주 모든 값을 0으로 채운다.
  예) 이미 생산해 둔 Assy 재고가 많아 RTF만 있는 경우, Prod. 계획을 W0~W13 전 주차 0으로 자동 생성한다.
규칙 B. Safety Stock만 있는 경우
  Module 4(Safety Stock)에 Customer Code가 있으나 RTF와 Prod. 모두 없으면, 두 계획을 모두 생성한다.
  RTF 14주차(W+13)에는 Safety Stock 수량을 넣고, Prod. 계획은 모든 주차를 0으로 한다.
규칙 C. 자동 생성 시점
  Module 6 Upload 완료 시 규칙 A를 적용한다.
  Recalculate(Module 10) 실행 시 규칙 B를 적용하여 Safety 기준 누락분을 보완한다.
  자동 생성 건수는 Recalculate 결과에 'RTF/Prod. 자동 생성 n건'으로 표시하고 Audit에 기록한다.
  자동 생성 행은 Upload 원본이 아니므로 재Upload 시 파일 기준으로 다시 맞춘다.

[8. 화면 조회 / 검색 / Filter]
작업 주차 Dropdown: 'W44(W0)' 형식, 기본값 Current Week의 작업 주차. 지난 16주까지 선택 가능 (Ⅳ-6-5, IN-1 확정)
Plan Dropdown: All / RTF / Prod. (기본값 All)
검색 조건: ① Cust. Code / Assy Code / Type 중 선택 → ② 검색어 → ③ Search 클릭 시 실행 (부분검색, 대소문자 무시)
Status 필터는 두지 않는다. (M6-2 확정: 추가하지 않음)
과거 주차 선택 시 조회와 Download만 가능하며, Upload 버튼은 비활성화한다.
기본 정렬: Cust. Code 오름차순, 같은 Cust. Code 안에서는 Plan 순서 RTF → Prod. 로 표시한다.

[9. Excel Download]
선택한 작업 주차, Plan, 검색 조건에 해당하는 전체 Row를 Download한다. 화면에 일부만 보여도 전체 Row를 포함한다.
Download 양식은 Upload 양식(Customer Code, Plan, 14개 주차)과 맞추어 Download → 수정 → 재Upload가 가능하도록 한다.
(No, Assy Code, Type, Model, Item, Status, No BOM 열은 Upload 시 무시한다.)
Safety 자동 합산 값은 Download에 포함하지 않는다. 업로드 원본값으로 내보낸다. (M6-3 확정)
자동 생성된 행(0 값)도 Download에 0으로 포함한다.

[10. 계산 및 재계산 영향]
RTF 기준 행 14주차 = 업로드 수량 + Safety Stock (Ⅲ-4-1, 확정)
Production 기준 행 14주차 = 업로드 수량 (Safety 미반영)
RTF / Production 기준 소요량은 각각 계산하며 Material Requirement(Module 9)에서 BOM 소요원수로 Material 단위 환산한다.
Upload 후 Module 10 재계산 대상 Data 변경으로 본다. 저장 즉시 재계산하지 않으며 'Need Recalculation'을 표시한다. (Ⅳ-7-2)
Inactive Assy의 RTF·Production 수량은 Material Requirement에 포함하여 계산하고 Warning으로 표시한다. (Ⅲ-4-3, F-9)

[11. 권한]
Admin: 조회, 검색, Filter, Download, Upload (Ⅴ-1 권한 Matrix)
Master / User / Guest: 조회, 검색, Filter, Download (Upload 버튼 비활성화)
Backend에서 권한을 검증한다. (Ⅴ-1-7)

[12. Audit Data]
Upload 시 다음을 기록한다: 사용자 ID, Upload 시각(UTC 저장, Local 표시), 파일명, 시트명(RTF / PROD_PLAN), 작업 주차, 전체 Row 수, 신규·변경·동일·삭제 건수, Error/Warning 건수 (Ⅰ-9 감사 기록 원칙)

[13. Acceptance Criteria]
① Admin이 작업 주차 RTF 시트를 Upload하면 해당 주차 기존 RTF Data가 전체 교체된다. 이전 Data는 조회할 수 없다.
② Customer Code가 Excel 내 중복이면 Upload 전체가 중단되고 중복 행이 표시된다.
③ RTF 시트에 Plan 'Prod.'가 있거나 Prod. 시트에 'RTF'가 있으면 Error로 Upload가 중단된다.
④ 14번째 열 Header는 'Safety(W+13)'로 표시되고, RTF 행 14주차 값에 Safety Stock이 합산되어 있다.
⑤ Production 행 14주차에는 Safety Stock이 합산되지 않는다.
⑥ BOM이 없는 Assy는 No BOM 열에 'NO'가 표시되고 Upload가 완료된다.
⑦ Assy Master에 없는 Customer Code는 'No DB'로 표시되고 Warning 목록에 포함된다.
⑧ 과거 주차를 선택하면 Upload 버튼이 비활성화되고 조회와 Download만 된다.
⑨ 화면에 Save 버튼과 수정 입력란이 없다.
⑩ Master·User·Guest 계정에서 Upload 버튼이 표시되지 않으며, 서버에서도 거부된다.
⑪ RTF만 Upload된 Customer Code는 Prod.가 0으로 자동 생성되어 화면에 표시된다.
⑫ Safety Stock에만 있는 Customer Code는 Recalculate 후 RTF(14주차 = Safety)와 Prod.(전 주차 0) 행이 생성된다.
⑬ Download 값에는 Safety 합산 값이 포함되지 않는다.

[14. 화면 주석 정리 필요 (스크린샷 06)]
주석 "BOM 미등록 Assy Upload 허용, 'Status'의 우측에 'NO' 체크"는 본 초안과 일치한다. 다만 Excel 안내 문구 'BOM 유무 Column'은 'No BOM'으로 명칭을 통일한다. (Ⅶ-8 수정 필요)
Plan 드롭다운의 'Prod.'는 Production Plan 약칭(G-13)으로 통일하며, 'P Plan' 표기는 사용하지 않는다.

[15. 확정 사항 참고]
F-4 (14번째 열 Header 'Safety(W+13)'), IN-1 (W44(W0) 표기), IN-2 (정수), IN-3 (Status 필터 없음) 결과를 반영했다.

[16. 확정 사항 (2026-11)]
M6-1 (확정): 한쪽 계획만 있으면 나머지를 0으로 자동 생성한다. Safety Stock만 있는 Customer Code는 RTF(14주차에 Safety 수량)와 Prod.(전 주차 0)를 모두 생성한다. ([7-1])
M6-2 (확정): Module 6에는 Status 필터를 추가하지 않는다.
M6-3 (확정): Download는 업로드 원본값으로 내보낸다. Safety 합산 값은 포함하지 않는다.

────────────────────
Ⅵ-7. 일곱번째 기능 Module _ Open PO (미입고 발주)
────────────────────

[1. 기능 / 업무 목적]
Open PO는 공급업체에 발주했으나 아직 입고되지 않은 수량을 Material·Vendor 단위로 관리한다. (Ⅲ-4-2-1, Ⅶ-9)
작업 주차의 PO Balance(PO 과부족) 계산에 사용한다.
화면 UI: '스크린샷 07.png' (화면 Column 구성은 본 절의 [3. 데이터 구성]이 우선한다.)

[2. 용어 및 계산식] (Ⅶ-9, 스크린샷 07 주석 기준)
PO Q'ty    = 최초 발주 수량 (Upload)
Cancel     = 취소 수량 (Upload)
Final PO   = PO Q'ty − Cancel (시스템 계산)
G/R        = 입고 수량, Good Receipt (Upload)
In Transit = 업체에서 출하되어 운송 중인 수량 (Upload)
Remain Q'ty = Final PO − G/R − In Transit (시스템 계산)
Open PO    = In Transit + Remain Q'ty (Ⅲ-4-2-1, F-1)
Amount        = PO Q'ty × Unit Price (시스템 계산, 스크린샷 07 기준). Unit Price가 빈 칸이면 Amount도 빈 칸으로 둔다.
Remain Amount = Remain Q'ty × Unit Price (시스템 계산)
(Unit Price가 없으면 Amount와 Remain Amount는 빈 칸으로 표시한다. 2026-11 확정)

[3. 데이터 구성]
[3-1. 화면 Column] (스크린샷 07 기준)
순서: No / PO Date / PO No / Mat. Code / Unit / PO Q'ty / Curr. / Unit Price / Amount / Cancel / Final PO(+/-) / G/R / In Transit / Remain Q'ty(+/-) / Remain Amount / Vendor / Status
헤더 색상 (Ⅳ-3-5):
  파란색 = 엑셀 업로드 Column: PO Date, PO No, Mat. Code, Unit, PO Q'ty, Curr., Unit Price, Cancel, G/R, In Transit, Vendor
  회색 = 시스템 계산 또는 Master 참조 Column: No, Amount, Final PO, Remain Q'ty, Remain Amount, Status
Status 열은 우측에 표기하며 Active / Inactive / No DB 중 하나를 표시한다. Material Master의 Status를 따른다. (Ⅳ-3-1)
화면 수정 기능은 없다. (Ⅳ-3-0) 스크린샷 07 상단 주석 "선택한 행(Row) 저장"은 적용하지 않는다.

[4. Field 정의]
PO Date     Upload 필수, 날짜 yyyy-mm-dd. 같은 날짜 중복 가능 (Excel 안내 기준)
PO No       Upload 필수 (OP-2 확정), 문자열, 빈 칸 불가. 같은 PO No 안에 같은 Material이 여러 행이면 각각 별도 행으로 저장 (병합하거나 Error 처리하지 않음)
Mat. Code   Upload 필수, Material Master 내 존재 여부와 Status와 무관하게 업로드 가능. 없으면 'No DB' 표시
Unit        Upload 필수, Material Master의 Unit과 비교하여 다르면 Error (Unit 불일치 Error, 2026-11 확정)
PO Q'ty     Upload 필수, 0보다 큰 숫자, 소수점 6자리까지 허용 (OP-2 확정)
Curr.       Unit Price를 입력한 경우 Upload 필수. 허용값: USD, KRW, VND, CNY, JPY
Unit Price  Upload 선택, 0 이상의 숫자, 소수점 6자리까지 허용. 빈 Cell = 미입력 (Amount도 빈칸)
Cancel      Upload 선택, 0 이상의 숫자, 소수점 6자리까지 허용, 빈 Cell = 0
G/R         Upload 선택, 0 이상의 숫자, 소수점 6자리까지 허용, 빈 Cell = 0
In Transit  Upload 선택, 0 이상의 숫자, 소수점 6자리까지 허용, 빈 Cell = 0
Vendor      Upload 필수 (OP-1 확정), 문자열. 문자 사이 공백 가능, 빈 칸 불가. Material Master의 Vendor와 무관

[5. Validation]
시트 'OPEN_PO' 존재 여부 (없으면 Error)
필수 Column Header 존재 여부 (PO Date, PO No, Material Code, Unit, PO Q'ty, Vendor 등) (없으면 Error)
병합 셀 존재 (Error, Ⅳ-5-1)
PO Date가 yyyy-mm-dd가 아님 (Error)
PO Q'ty가 0 이하이거나 숫자가 아님 (Error)
Unit이 Material Master의 Unit과 다름 (Error)
Currency가 허용값 외이거나, Unit Price 입력 시 Currency 누락 (Error)
Unit Price 또는 수량의 소수점 7자리 이상 (Error, 자동 반올림하지 않음)
Cancel, G/R, In Transit이 음수이거나 숫자가 아님 (Error)
Remain Q'ty < 0 (= Cancel + G/R + In Transit > Final PO 계열 초과) (Error, 수정 후 재등록 안내)
지수표기 손상 Code (Error, Ⅳ-5-1)
Excel 날짜 자동 변환 Error: PO Q'ty 등 수량 셀이 날짜로 인식된 경우 (Error)
Material Code가 Material Master에 없음 (Warning, 'No DB' 표시, 계산 포함)
Material Code가 Material Master에 있으나 Inactive (Warning, 계산 포함, F-9와 동일)
Material + Vendor 기준 Scheduled Receipt 14주 합계가 Open PO보다 큼 (Error, Ⅶ-10 — 업로드 시 Module 8과 함께 점검)

[6. Excel Upload]
Upload 방식: 작업 주차의 기존 Data 전체를 파일로 대체한다. 기존 Data는 삭제하며 History는 두지 않는다. (Ⅶ-9, Ⅳ-5)
Upload Type 선택 없음. 과거 주차 Upload 불가.
Upload Mode: Admin만 가능하다. (Ⅴ-1 권한 Matrix)
시트명: OPEN_PO
Column (Upload 순서): PO Date, PO No, Material Code, Unit, PO Q'ty, Currency, Unit Price, Cancel, G/R, In Transit, Vendor (Ⅶ-9, Header 명칭 2026-11-24 확정)
Excel 빈 Cell 처리: Cancel, G/R, In Transit = 0, Unit Price = 미입력
Validation Error가 1건이라도 있으면 전체 반영을 중단하고 Transaction을 Rollback한다.
PO Line과 ETA Column은 사용하지 않는다. (Ⅶ-9, 확정)

[7. 계산 규칙]
시스템은 Upload 원본값으로 Final PO, Remain Q'ty, Amount, Remain Amount를 계산한다. Upload 값으로 받지 않는다.
Open PO 목록은 In Transit + Remain Q'ty > 0 인 행만 계산에 사용한다. Remain Q'ty = 0이어도 In Transit > 0이면 운송 중 수량이 있으므로 포함한다. In Transit + Remain Q'ty = 0 인 행은 Open PO 목록에서 제외한다. (2026-11-24 확정)
Material + Vendor 기준 Open PO 합계 = Σ(In Transit + Remain Q'ty) (Ⅶ-10)
Material + Vendor 기준 차이분 = Open PO 합계 − SCHED_RECEIPT 14주 합계 (Ⅶ-10, Ⅶ-11)
차이분 < 0 → Error (Module 8 수정 후 재Upload)
차이분 ≥ 0 → Calculated Scheduled Receipt로 '작업 주차 + L/T' 주차에 반영 (Ⅶ-11)
Material Requirement(Module 9)의 PO Balance는 Material 단위 Open PO 합계를 사용한다. (Ⅲ-4-2-1)
Upload 후 Module 10 재계산 대상 Data 변경으로 본다. 저장 즉시 재계산하지 않으며 'Need Recalculation'을 표시한다. (Ⅳ-7-2)

[8. 화면 조회 / 검색 / Filter]
작업 주차 Dropdown: 'W44(W0)' 형식, 기본값 Current Week의 작업 주차. 지난 16주까지 선택 가능 (Ⅳ-6-5, IN-1 확정)
검색 조건: ① PO Date / PO No / Mat. Code / Vendor 중 선택 → ② 검색어 → ③ Search 클릭 (부분검색, 대소문자 무시)
Status 필터는 두지 않는다. (Module 6과 동일, 스크린샷 07 기준)
Mat. Code 검색 시 안내 문구는 'Mat. Code로 검색'으로 표기한다. (스크린샷 07의 'Cust. Code로 검색' 문구는 정정 필요)
기본 정렬: PO Date 오름차순, 같은 날짜는 PO No 순.
과거 주차 선택 시 조회와 Download만 가능하며, Upload 버튼은 비활성화한다.

[9. Excel Download]
선택한 작업 주차와 검색 조건에 해당하는 전체 Row를 Download한다.
Download 양식은 Upload 양식(Ⅶ-9 Upload Column 순서)과 맞추어, Download → 수정 → 재Upload가 가능하도록 한다.
(No, Final PO, Amount, Remain Q'ty, Remain Amount, Status Column은 Upload 시 무시한다.)
Download 값은 업로드 원본값으로 내보낸다. (Module 6 M6-3과 동일 원칙)

[10. 권한]
Admin: 조회, 검색, Filter, Download, Upload (Ⅴ-1 권한 Matrix)
Master / User / Guest: 조회, 검색, Download (Upload 버튼 비활성화)
Backend에서 권한을 검증한다. (Ⅴ-1-7)

[11. Audit Data]
Upload 시 다음을 기록한다: 사용자 ID, Upload 시각(UTC 저장, Local 표시), 파일명, 작업 주차, 전체 Row 수, 신규·변경·동일·삭제 건수, Error/Warning 건수, Remain Q'ty 합계 (Ⅰ-9 감사 기록 원칙)

[12. Acceptance Criteria]
① Admin이 작업 주차 OPEN_PO 시트를 Upload하면 해당 주차 기존 Data가 전체 교체된다.
② Final PO = PO Q'ty − Cancel, Remain Q'ty = Final PO − G/R − In Transit으로 계산되어 화면에 표시된다.
③ Remain Q'ty < 0 행이 있으면 해당 행이 Error로 표시되고 Upload가 중단된다.
④ Unit이 Material Master와 다르면 Error로 Upload가 중단된다.
⑤ Currency 허용값 외 값이나 Unit Price 입력 시 Currency 누락이면 Error로 중단된다.
⑥ 같은 PO No 안의 같은 Material 행은 병합되지 않고 각각 표시된다.
⑦ Material Master에 없는 Material Code는 'No DB'로 표시되고 Upload가 완료된다. Warning 목록에 포함된다.
⑧ Material + Vendor 기준 Open PO 합계가 SCHED_RECEIPT 14주 합계보다 작으면 Error로 표시된다.
⑨ 화면에 Save 버튼과 수정 입력란이 없다.
⑩ Master·User·Guest 계정에서 Upload 버튼이 표시되지 않으며, 서버에서도 거부된다.

[13. 엑셀 양식 안내 문구 정정 필요 (표준 업로드 양식_1123, OPEN_PO 시트)]
G/R, In Transit 안내는 소수점 6자리 허용으로 수정되었다. (사용자 확인 완료)
Vendor 안내는 "문자 사이 공백 가능"으로 정정한다. (OP-1 확정: 필수)
PO No 안내 "공백가능, 중복 가능"은 OP-2 확정(필수)과 충돌하므로 "공백 불가, 중복 가능"으로 정정한다.
Material Code 안내 "허용값 내에서 선택"은 Material Master 기준 Code 검증 문구로 정정이 필요하다.

[14. 화면 주석 정정 필요 (스크린샷 07)]
상단 "선택한 행(Row) 저장" 주석은 Ⅳ-3-0(모듈 3~10은 저장 없음)과 충돌하므로 삭제한다.
검색 Dropdown 상단 라벨 "Purchaser"는 "검색조건"으로 정정한다.
Mat. Code 검색 안내 "Cust. Code'로 검색"은 "Mat. Code'로 검색"으로 정정한다.

[15. 확정 사항 참고]
IN-1 (W44(W0) 표기), IN-2 (Stock 소수 정책은 Module 5 한정), M6-2 (Status 필터 없음)를 반영했다.
Unit Price와 수량은 소수점 6자리까지 허용한다. (OP-2 확정)

[16. 확정 사항 (2026-11)]
OP-1 (확정): Vendor는 필수이며, 문자 사이 공백은 허용한다. 빈 칸은 불가하다.
OP-2 (확정): PO No는 필수다. PO Q'ty, Unit Price, Cancel, G/R, In Transit은 소수점 6자리까지 허용한다.
OP-3 (확정): 스크린샷 07 주석 정정은 완료되었다. 상단 "선택한 행(Row) 저장" 삭제, "Mat. Code로 검색", 검색조건 라벨 정정.

────────────────────
Ⅵ-8. 여덟번째 기능 Module _ Scheduled Receipt (입고예정)
────────────────────

[1. 기능 / 업무 목적]
Scheduled Receipt(입고예정)는 Material + Vendor 단위로 주차별 입고 예정 수량을 관리한다. (Ⅶ-10, 확정)
입고예정은 두 종류이다.
  ① Manual Scheduled Receipt: 구매 담당자가 Vendor와 협의하여 Upload한 입고예정 (검정색 표시)
  ② Calculated Scheduled Receipt: Open PO 중 아직 14주 입고예정에 반영되지 않은 차이분을 L/T 기준으로 자동 배치한 값 (파란색 표시) (Ⅶ-11)
화면 UI: '스크린샷 08.png' (화면 Column 구성은 본 절의 [3. 데이터 구성]이 우선한다.)

[2. Key 규칙]
Key: Material Code + Vendor (Excel 내 중복 불가, 중복 시 합산하지 않고 Error) (D-7, 확정)
Code 비교는 Ⅵ-2-4의 Code 정규화(앞뒤 공백 제거, 영문 대문자 변환)를 적용한다.
Material 정보(Desc., Spec., Unit, L/T)는 Material Master에서 조회하여 표시한다. (Ⅵ-1 Single Source of Truth)
Material Master에 없는 Code는 'No DB'로 표시하며 업로드는 허용한다. 단, 자동 계산을 위한 L/T는 없으므로 계산을 생략하고 Warning으로 표시한다 (SR-1 확정).

[3. 데이터 구성]
[3-1. 화면 Column] (스크린샷 08 기준)
순서: No / Mat. Code / Vendor / Unit / W44(W0) / W45(W+1) / … / W04(W+13) / Open PO(In Transit, Remain Q'ty) / L/T(W) / Status
헤더 색상 (Ⅳ-3-5):
  파란색 = 엑셀 업로드 Column: Mat. Code, Vendor, Unit, 14개 주차 Column
  회색 = Master 참조 또는 계산 Column: No, Open PO(In Transit, Remain Q'ty), L/T(W), Status
표시 구분 (스크린샷 08 주석 확정):
  검정 = 사용자 입력 (Manual Scheduled Receipt)
  파랑 = 계산 입고예정 (Calculated Scheduled Receipt, 시스템 자동 계산)
Status 열은 우측에 표기하며 Active / Inactive / No DB 중 하나를 표시한다. (Ⅳ-3-1)
Status와 L/T는 Material Master 기준이며, 이 화면에서 직접 변경하지 않는다.
화면 수정 기능과 Save 버튼은 없다. (Ⅳ-3-0)

[4. Field 정의]
Mat. Code   Upload 필수, 문자열, 공백 불가. Material Master 존재 여부와 무관하게 업로드 허용 (No DB 표시)
Vendor      Upload 필수, 문자열. 문자 사이 공백 가능, 빈 칸 불가. Material Master의 Vendor와 무관 (Module 7 OP-1과 동일)
Unit        Upload 필수, Material Master의 Unit과 비교하여 다르면 Error (Unit 불일치 Error, 2026-11 확정)
14개 주차   Upload 필수 (빈 Cell 허용, 빈 Cell = 0). 0 이상의 숫자, 소수점 6자리까지 허용, 음수·소수점 7자리 이상 불가 (Ⅶ-10)
Open PO     시스템 표시. Material + Vendor 기준 In Transit 합계와 Remain Q'ty 합계 (Module 7 Upload 기준)
L/T(W)      시스템 표시. Material Master의 L/T(Weeks), 1 이상 자연수
Status      시스템 표시 (Active / Inactive / No DB)

[5. Validation]
시트 'SCHED_RECEIPT' 존재 여부 (없으면 Error)
필수 Column Header 존재 여부 (Material Code, Vendor, Unit, 14개 주차) (없으면 Error)
병합 셀 존재 (Error, Ⅳ-5-1)
주차 Header가 작업 주차부터 연속된 14주가 아님 (Error, Ⅶ-2)
Mat. Code + Vendor 중복 (Excel 내, Error, 합산하지 않음, D-7)
Unit이 Material Master와 다름 (Error, Unit 불일치 Error)
주차 값이 음수, 텍스트, 소수점 7자리 이상, 지수표기 손상 (Error)
Excel 날짜 자동 변환으로 인식된 수량 (Error)
Material + Vendor 기준 SCHED 14주 합계 > Open PO (In Transit + Remain Q'ty 합계) (Error, Ⅶ-10)
Material Master에 없는 Code (Warning, 'No DB' 표시, 업로드 허용)
Material Master에 있으나 Inactive (Warning, 계산 포함)

[6. Excel Upload]
Upload 방식: 작업 주차의 기존 Data 전체를 파일로 대체한다. 기존 Data는 삭제하며 History는 두지 않는다. (Ⅶ-10, Ⅳ-5)
Upload Type 선택 없음. 과거 주차 Upload 불가.
Upload Mode: Admin만 가능하다. (Ⅴ-1 권한 Matrix)
시트명: SCHED_RECEIPT
Column (Upload 순서): Material Code, Vendor, Unit, 14개 주차 (파란색 Column만 포함)
Excel 빈 Cell은 0으로 처리한다.
Validation Error가 1건이라도 있으면 전체 반영을 중단하고 Transaction을 Rollback한다.
Upload 시 Open PO 기준으로 차이분을 계산하므로, Module 7(OPEN_PO)이 같은 작업 주차에 Upload되어 있어야 정확하다. Open PO 미Upload 상태에서 입고예정을 Upload하면 Open PO = 0으로 보고 Error 처리한다. (SR-2 확정)

[7. 계산 규칙] (Ⅶ-10, Ⅶ-11, F-3, G-11, 확정)
① 기준 합계: Material + Vendor별 Open PO = Σ(In Transit + Remain Q'ty), Module 7 Upload 기준
② 차이분 = Open PO − Manual SCHED 14주 합계
③ 차이분 < 0 → Upload Error (입고예정이 Open PO를 초과). 수정 후 재Upload.
④ 차이분 = 0 → 계산 입고예정 없음
⑤ 차이분 > 0 → 입고 주차 = 작업 주차 + L/T(Weeks)
    예) 작업 주차 W44, L/T 8 → W52 (W+8) 열에 차이분을 파란색으로 합산한다.
⑥ 입고 주차가 W+13을 넘으면 14주차(W+13) 열에 합산한다. (Q4 확정)
⑦ 해당 주차에 Manual 값이 이미 있으면 Manual 값에 차이분을 더하여 표시한다. 계산값은 Upload 값이 아니다.
⑧ 계산 입고예정은 화면 조회 시 실시간 산출하며 저장하지 않는다. (Ⅳ-7-0 계층 2)
⑧-1 차이분이 음수이면 화면에 빨간색 경고를 표시한다. Upload 시점에 음수이면 Upload Error로 차단한다. (Ⅶ-10 유지)
⑧-2 모듈 9~10 반영은 Recalculate 실행 시 Current Week에 한하여 이루어진다. Recalculate 시 음수는 Error로 차단한다. (Ⅳ-7-0 계층 3)
⑨ 계산 결과는 Manual 값과 분리하여 저장한다. Manual 원본은 Download 시 원본값으로 내보낸다. (M6-3과 동일 원칙)

[8. 화면 조회 / 검색 / Filter]
작업 주차 Dropdown: 'W44(W0)' 형식, 기본값 Current Week의 작업 주차. 지난 16주까지 선택 가능 (IN-1 확정)
검색 조건: ① Mat. Code / Vendor / L/T 중 선택 → ② 검색어 → ③ Search 클릭 (부분검색, 대소문자 무시)
Status 필터는 두지 않는다. (M6-2와 동일)
기본 정렬: Mat. Code 오름차순, 같은 Mat. Code 안에서는 Vendor 오름차순. (SR-3 확정)
과거 주차 선택 시 조회와 Download만 가능하며, Upload 버튼은 비활성화한다.

[9. Excel Download]
선택한 작업 주차와 검색 조건에 해당하는 전체 Row를 Download한다.
Download 양식은 Upload 양식(Material Code, Vendor, Unit, 14개 주차)과 맞추어, Download → 수정 → 재Upload가 가능하도록 한다.
Download 값은 Manual 원본값이다. 계산 입고예정(파란색)은 포함하지 않는다.
(No, Open PO, L/T, Status Column은 Upload 시 무시한다.)

[10. 권한]
Admin: 조회, 검색, Filter, Download, Upload (Ⅴ-1 권한 Matrix)
Master / User / Guest: 조회, 검색, Download (Upload 버튼 비활성화)
Backend에서 권한을 검증한다. (Ⅴ-1-7)

[11. Audit Data]
Upload 시 다음을 기록한다: 사용자 ID, Upload 시각(UTC 저장, Local 표시), 파일명, 작업 주차, 전체 Row 수, 신규·변경·동일·삭제 건수, Error/Warning 건수, 계산 입고예정 건수와 합계 (Ⅰ-9 감사 기록 원칙)

[12. Acceptance Criteria]
① Admin이 작업 주차 SCHED_RECEIPT 시트를 Upload하면 해당 주차 기존 Data가 전체 교체된다.
② Material Code + Vendor가 Excel 내 중복이면 Upload 전체가 중단되고 중복 행이 표시된다.
③ Material + Vendor 기준 SCHED 14주 합계가 Open PO보다 크면 Error로 Upload가 중단된다.
④ 차이분 > 0인 경우 '작업 주차 + L/T' 열에 파란색으로 차이분이 표시된다. L/T가 W+13을 넘으면 W+13 열에 표시된다.
⑤ Manual 값과 계산 값은 색상으로 구분되며, Download에는 Manual 원본값만 포함된다.
⑥ Unit이 Material Master와 다르면 Error로 Upload가 중단된다.
⑦ Material Master에 없는 Code는 'No DB'로 표시되고 Upload가 완료된다.
⑧ 과거 주차를 선택하면 Upload 버튼이 비활성화되고 조회와 Download만 된다.
⑨ 화면에 Save 버튼과 수정 입력란이 없다.
⑩ Master·User·Guest 계정에서 Upload 버튼이 표시되지 않으며, 서버에서도 거부된다.

[13. 화면 주석 정정 필요 (스크린샷 08)]
계산 입고예정의 배치 위치가 주석과 다르다. (2026-11 캡쳐 수정으로 정정 완료)
Material 'SMMZ25010'(No DB)에 L/T 2가 표시되어 있으나, Master에 없는 Code는 L/T를 알 수 없다. (SR-1 확정)
검색 조건 Dropdown의 'L/T로 검색'은 Material Master L/T 기준임을 명확히 한다.

[14. 엑셀 양식 확인 (표준 업로드 양식_1123, SCHED_RECEIPT 시트)]
Vendor 안내 "공백문자 가능"은 "문자 사이 공백 가능, 빈 칸 불가"로 정정이 필요하다. (Module 7 OP-1과 동일 기준)
주차 값 안내는 "소수 가능(6자리), 빈칸 0"으로 되어 있어 본 초안과 일치한다.
Material Code와 Unit 안내는 Ⅵ-1 기준과 일치한다.

[15. 확정 사항 참고]
D-7 (중복 Error), Q4 (W+13 초과 시 14주차 합산), G-11 (차이분 L/T 반영), F-3, IN-1 (W44(W0) 표기), M6-2 (Status 필터 없음), OP-1 (Vendor 필수)을 반영했다.

[16. 확정 사항 (2026-11)]
SR-1 (확정): No DB 자재는 자동 계산을 생략하고 Warning으로 표시한다.
SR-2 (확정): Open PO가 없는 Material + Vendor의 입고예정은 Error로 처리한다.
SR-3 (확정): 기본 정렬은 Mat. Code → Vendor 순이다.
변경 반영 방식 (확정): Ⅳ-7-0 3계층 규칙을 따른다. 계산 입고예정은 조회 시 실시간 산출, 모듈 9~10은 Recalculate 시 반영한다.

────────────────────
Ⅵ-9. 아홉번째 기능 Module _ Material Requirement (자재 소요량)
────────────────────

[1. 기능 / 업무 목적]
Material Requirement(자재 소요량)는 Assy의 RTF 계획 또는 Production Plan과 BOM을 이용하여 Material별 주차 소요량을 산출한다. (Ⅲ-4, 확정)
계산식: Σ(Assy 주별 계획수량 × 해당 Assy BOM의 Material 소요원수) (Ⅲ-4-1)
RTF 기준과 Production Plan 기준을 각각 계산하여 함께 제공하며, 두 결과를 합치지 않는다. (Ⅲ-4-1)
이 Module은 조회와 Download만 제공한다. 입력 기능은 없다. (Ⅴ-1 권한 Matrix)
화면 UI: '스크린샷 09.png' (화면 Column 구성은 본 절의 [3. 데이터 구성]이 우선한다.)

[2. 행 구조] (사용자 답변 확정, 2026-11)
하나의 Material은 다음과 같이 행 묶음으로 표시한다.
  ① Total 행 (첫 행): Cust. Code 열에 'Total'을 표기한다. 같은 Material·Plan의 모든 Assy 행의 주차별 합계를 표시한다. Status는 Material Master의 Status를 따른다.
  ② Assy 행 (Total 행 아래): 해당 Material을 사용하는 각 Assy(Customer Code)의 계산 소요량(계획수량 × 소요원수)을 표시한다. Status는 Assy Master의 Status를 따른다.
Plan별로 Total 행을 따로 둔다. (Plan = All이면 RTF 묶음과 Prod. 묶음이 각각 Total 행을 가진다.)
동일 Assy·동일 Material의 BOM Row가 여러 개이면 하나의 Assy 행으로 합산 표시한다. 원본 BOM Row는 변경하지 않는다. (M-1 확정)
Total 행은 Assy 행들의 합계이므로 Material 기준 Module 10 계산의 입력값이 된다. (M-1 확정)

[3. 데이터 구성]
[3-1. 화면 Column] (스크린샷 09 기준, Unit Column 추가 확정)
순서: No / Mat. Code / Cust. Code / Desc. / Type / Spec. / Model / Plan / Unit / Q'ty / W44(W0) / W45(W+1) / … / W04(W+13) / Status
헤더 표기: "Desc. / Type"과 "Spec. / Model"은 각각 하나의 Column이며, 행 종류에 따라 값이 다르다. (사용자 확정)
헤더 색상: 본 Module은 Upload가 없으므로 모든 Column을 시스템 계산 또는 Master 참조 색(회색)으로 표시한다.
Mat. Code: 모든 행(Total 행과 Assy 행)에 표시한다. (M9-3 권장안)
Cust. Code: Total 행은 'Total', Assy 행은 Customer Code.
Desc. / Spec. (Total 행): Material Master의 Desc., Spec.을 표시한다. Material Master에 없는 'No DB' Material은 빈 칸으로 표시한다. (사용자 확정)
Type / Model (Assy 행): Assy Master의 Type, Model을 표시한다. Assy Master에 없는 Customer Code(No DB)는 빈 칸으로 표시한다. (사용자 확정)
Desc. / Type 열과 Spec. / Model 열은 행 종류에 따라 Material 값 또는 Assy 값을 표시한다.
Unit: Material Master의 Unit을 표시한다. Material Master에 없으면 빈 칸으로 둔다. (추가 확정)
Plan: RTF 또는 Prod.
Q'ty: Assy 행에만 BOM 소요원수를 표시한다. Total 행은 빈 칸 또는 '-'로 표시한다.
주차 값: Total 행은 하위 Assy 행의 합계, Assy 행은 Σ(계획수량 × 소요원수)이다.
14번째 열(W+13): RTF 행에만 Safety Stock 소요량을 포함한다. (Ⅲ-4-1, Ⅶ-8)
Status: 행 종류에 따라 [4] 규칙으로 표시한다.

[4. Status 규칙] (사용자 답변 확정, 2026-11)
Total 행: Material Master의 Status (Active / Inactive / No DB)
Assy 행: Assy Master의 Status (Active / Inactive / No DB)
Status는 계산 반영 여부를 바꾸지 않는다. Assy와 Material의 Status와 무관하게 BOM이 존재하면 소요량을 계산하여 반영한다.

[5. Validation 및 계산 전 점검]
Module 9 계산은 Ⅳ-7-1 규칙에 따라 Error가 있으면 중단한다.
Error 대상 (계산 중단):
  BOM Unit과 Material Master Unit 불일치 (2026-11 확정, Error)
  Q'ty 음수, 또는 계산 정밀도(소수점 10자리)를 벗어나는 값
Warning 대상 (계산 계속, 목록 표시):
  Material Master에 없는 Material (No DB, Desc./Spec./Unit 빈 칸, 계산 포함)
  Assy Master에 없는 Customer Code (No DB, 계산 포함)
  Inactive Assy 또는 Inactive Material의 소요량 (계산 포함, F-9 확정)
  BOM 미등록 Assy의 계획 수량 (소요량 0 간주, 'No BOM', Ⅲ-4-3 확정)
Warning 목록은 Recalculate 결과 화면에 표시하며 'BOM 미등록 n건'을 함께 표시한다.

[6. 계산 기준]
RTF 기준 Assy 행: 1~13주차는 업로드된 RTF 수량 × 소요원수, 14주차(W+13)는 (RTF 수량 + Safety Stock) × 소요원수 (Ⅲ-4-1)
Production Plan 기준 Assy 행: 14주 모두 Production Plan 수량 × 소요원수. Safety Stock은 반영하지 않는다. (Ⅲ-4-1)
Safety Stock은 RTF 기준에만 포함한다. (C-2 확정)
Module 9는 재고, Open PO, 입고예정을 계산에 사용하지 않는다. (Ⅲ-4-2)

[7. 계산 정밀도와 표시] (사용자 답변 확정, 2026-11)
내부 계산값: 소수점 10자리까지 유지한다. 분수로 표현 가능한 경우에는 분수를 우선한다. (Q-1 확정)
화면 표시: 소수점 둘째 자리까지 표시한다. 반올림은 표시에만 적용하고 계산에는 원본 정밀도를 사용한다.
Download: DB에 저장된 값 그대로, 소수점 10자리까지 내보낸다.

[8. 화면 조회 / 검색 / Filter]
작업 주차 Dropdown: 'W44(W0)' 형식, 기본값 Current Week. 지난 16주까지 선택 가능 (IN-1 확정)
Plan Dropdown: All / RTF / Prod. (기본값 All)
검색 조건: ① Mat. Code / Cust. Code 중 선택 → ② 검색어 → ③ Search 클릭 (부분검색, 대소문자 무시)
  Cust. Code로 검색하면 해당 Assy 행이 속한 Material 묶음 전체(Total 행 포함)를 표시한다.
Status 필터는 두지 않는다. (M6-2 기준과 동일)
기본 정렬: Mat. Code 오름차순 → Total 행 먼저 → Assy 행은 Cust. Code 오름차순 → Plan 순서 RTF 먼저, Prod. 나중
과거 주차 선택 시 조회와 Download만 가능하다. (Ⅳ-6-5)

[9. 행 강조 표시] (사용자 답변 확정, 2026-11)
Total 행은 굵은 글씨와 회색 배경으로 구분한다. (사용자 확정)
빨간색은 음수(부족) 표시와 'Need Recalculation'에 사용하므로 Total 행 표시에는 사용하지 않는다. (권장안, 사용자 답변 "붉은 글씨 또는 행 색깔 구분" 중 색 구분 방식 채택)

[10. Excel Download]
선택한 작업 주차, Plan, 검색 조건에 해당하는 전체 Row(Total 행과 Assy 행 모두)를 Download한다.
Download 값은 계산 원본값(소수점 10자리)이다. 화면 표시 반올림값과 다를 수 있다.
Download 양식에는 Unit, Status 열을 포함한다. 분석용 데이터이므로 Upload 양식과 맞추지 않는다.

[11. 반영 시점과 권한] (Ⅳ-7-0 계층 3, 확정)
원본 변경 후 Recalculate 실행 시에만 값이 갱신된다. 전에는 이전 계산 결과를 유지하고 'Need Recalculation'을 표시한다.
Recalculate 실행: Admin만 가능 (Module 10 화면에서 실행, Ⅳ-7-1)
조회·Download: Admin, Master, User, Guest 모두 가능 (Ⅴ-1 Matrix)

[12. Audit Data]
Recalculate 시 기록: 사용자 ID, 실행 시각(UTC 저장, Local 표시), 작업 주차, Plan별 Material 수, Warning 건수(유형별), Error 건수, BOM 미등록 Assy 건수 (Ⅰ-9 감사 기록 원칙)

[13. Acceptance Criteria]
① 각 Material은 Plan별 Total 행 1개와 Assy 행들로 구성되며, Total 행의 주차 값은 Assy 행 합계와 일치한다.
② 같은 Assy·Material의 BOM Row는 하나의 Assy 행으로 합산 표시된다.
③ RTF 행의 14주차(W+13)에 Safety Stock × 소요원수가 포함되고, Production Plan 행에는 포함되지 않는다.
④ Total 행의 Status는 Material Master, Assy 행의 Status는 Assy Master를 따른다.
⑤ Status가 Inactive 또는 No DB여도 BOM이 있으면 소요량이 계산되어 반영된다.
⑥ Material Master에 없는 Material은 Total 행의 Desc., Spec., Unit이 빈 칸으로 표시되고 Warning 목록에 포함된다.
⑥-1 Total 행의 Desc., Spec.은 Material Master 값, Assy 행의 Type, Model은 Assy Master 값으로 표시된다.
⑦ BOM 미등록 Assy의 소요량은 0으로 표시되고 Warning 목록에 포함된다.
⑧ BOM Unit과 Material Master Unit이 다르면 Recalculate가 Error로 중단된다.
⑨ 화면에서 소수점 둘째 자리까지 표시되고, Download는 소수점 10자리까지 내보낸다.
⑩ Total 행은 굵은 글씨와 회색 배경으로 구분된다.
⑪ Recalculate 전에는 이전 계산 결과가 유지되고 'Need Recalculation'이 표시된다.
⑫ Admin 이외의 계정에서 Recalculate 버튼이 비활성화되며, 서버에서도 거부된다.
⑬ 화면에 Save, Upload, 수정 입력란이 없다.

[14. 스크린샷 09 정정 필요]
Total 행의 Cust. Code 'Total' 표기는 수정본(스크린샷 09.png)에 반영되어 있다.
Total 행의 빨간색 표시는 Total 행 구분 방식(굵은 글씨, 회색 배경)으로 바꾸어 재캡쳐가 필요하다.
Unit Column은 스크린샷 09에 추가되어 있다.

[15. 확정 사항 참고]
Ⅲ-4-1 계산식, C-2(Safety는 RTF에만), Q-1(분수 우선, 소수 10자리), M-1(Total 합산·Module 10 Material 기준), F-9·Ⅲ-4-3(Warning), Ⅳ-7-0(3계층), 사용자 답변(Total 행, Status 규칙, Unit 추가, 소수 표시 방식, 행 강조)을 반영했다.

[16. 확정 사항 (2026-11)]
M9-1 (확정): 계산은 소수점 10자리 유지, 화면은 소수점 둘째 자리 표시, Download는 10자리 원본값.
M9-2 (확정): 빨간색 Total 행 표시를 폐지하고 회색 배경과 굵은 글씨로 구분한다.
M9-3 (확정): Total 행에는 Material Master의 Desc., Spec.을, Assy 행에는 Assy Master의 Type, Model을 표시한다. 헤더는 "Desc. / Type", "Spec. / Model"로 한다.

────────────────────
Ⅵ-10. 열번째 기능 Module _ Material PSI (자재 수급 분석)
────────────────────

[1. 기능 / 업무 목적]
Material PSI는 Material별로 주차 소요량(Module 9)과 재고, 입고예정, Open PO를 대조하여 재고 과부족과 PO 과부족을 주차별로 산출한다. (Ⅲ-4-2, 확정)
RTF 기준과 Production Plan 기준을 각각 계산하여 함께 제공한다. (Ⅲ-4-1)
이 Module은 조회, 검색, Download와 Admin의 Recalculate·Weekly Reset만 제공한다. 입력 기능은 없다.
화면 UI: '스크린샷 10.png' (수정본) (화면 Column 구성은 본 절의 [3. 데이터 구성]이 우선한다.)

[2. 계산 기준] (스크린샷 10 주석 확정)
기초재고 (Opening Inventory):
  RTF 기준 = Material 재고 + Σ(Assy 재고 × 해당 Assy BOM의 Material 소요원수) (Ⅲ-4-1)
  Production Plan 기준 = Material 재고만
입고예정 (Scheduled Receipt): 주차별 Manual 입고예정(검정) + Calculated 입고예정(파랑), Material 단위 합계 (Module 8, Ⅶ-11)
소요량 (Requirement): Module 9의 Total 행 주차 값 (Plan별)
재고 과부족 (Inventory Balance), 주차 t:
  = 기초재고 + Σ(k=W0~t) 입고예정 − Σ(k=W0~t) 소요량
PO 과부족 (PO Balance), 주차 t:
  = 기초재고 + Open PO 잔량(전체) − Σ(k=W0~t) 소요량
  Open PO 잔량 = Module 7의 In Transit + Remain Q'ty 합계 (Material 단위)
  PO 과부족에는 Scheduled Receipt를 더하지 않는다. (스크린샷 10 주석)
음수(부족) 셀은 붉은 계열 배경으로 강조한다. (스크린샷 10 주석)

[3. 데이터 구성]
[3-1. 화면 Column] (스크린샷 10 기준)
순서: No / Mat. Code / Desc. / Spec. / Unit / Opening Inventory / Open PO / Plan / PSI / W44(W0) / W45(W+1) / … / W04(W+13) / Status
Desc., Spec., Unit: Material Master에서 조회한다. Material Master에 없는 'No DB' Material은 빈 칸으로 표시한다. (Module 9 [4] 규칙과 동일, 2026-11 확정)
Opening Inventory, Open PO: Material 단위 값이며, 같은 Material의 4개 항목 행에 반복 표시한다. 기준(Plan)에 따라 다른 값이 표시된다. (RTF 기준 기초재고와 Prod. 기준 기초재고는 다름)
Plan: RTF 또는 Prod.
PSI (4행 고정): Requirement / Scheduled Receipt / Inventory Balance / PO Balance
Status: Material Master 기준 (Active / Inactive / No DB). Module 9 Total 행과 동일 규칙 (Ⅳ-3-1)
헤더 색상: 본 Module은 Upload가 없으므로 모든 Column을 시스템 계산 또는 Master 참조 색(회색)으로 표시한다.

[4. 행 구조]
Material 1개 × Plan 1개 = 4행 블록 (Requirement → Scheduled Receipt → Inventory Balance → PO Balance)
Plan = All이면 Material별로 RTF 블록과 Prod. 블록을 각각 둔다.
Material 블록 사이에 구분선을 둔다.

[5. 입고예정 표시] (스크린샷 10 주석 확정)
검정 = 사용자 Manual 입고예정 (Module 8 원본)
파랑 = Calculated 입고예정 (Open PO 차이분을 L/T 기준으로 배치한 값, Module 8 [7] 규칙)
Module 10 화면은 조회 시점에 계산된 Calculated 값을 표시한다. (Ⅳ-7-0 계층 2)

[6. Validation 및 계산 전 점검]
Module 10 계산은 Ⅳ-7-1 규칙에 따라 Error가 있으면 중단한다.
Error 대상:
  Module 9의 Error (BOM Unit 불일치 등)
  Material + Vendor 기준 SCHED 14주 합계 > Open PO 잔량 (Module 8 SR-2, Error)
Warning 대상 (계산 계속, 목록 표시):
  Material Master에 없는 Material (No DB, 빈 칸 표시)
  Inactive Material (계산 포함, F-9)
  BOM 미등록 Assy로 인한 소요량 0 간주 (Ⅲ-4-3)
  Inactive Assy 수량 포함 (F-9)
Warning 목록은 Recalculate 결과 화면에 표시한다.

[7. 화면 조회 / 검색 / Filter]
작업 주차 Dropdown: 'W44(W0)' 형식, 기본값 Current Week, 지난 16주까지 선택 가능 (IN-1 확정)
Plan Dropdown: All / RTF / Production (기본값 All). 스크린샷 10의 "Prod."는 Module 6~9와 같이 "Prod."로 표기하며, 드롭다운 항목은 "All / RTF / Prod."로 통일한다.
검색 조건: ① Mat. Code / Desc. 중 선택 → ② 검색어 → ③ Search 클릭 (R-2 확정, 부분검색, 대소문자 무시)
Status 필터는 두지 않는다. (M6-2와 동일 기준)
기본 정렬: Mat. Code 오름차순 → Plan 순서 RTF 먼저, Prod. 나중 → 항목 순서 고정
과거 주차 선택 시 조회와 Download만 가능하다. (Ⅳ-6-5)

[8. 반영 시점과 재계산] (Ⅳ-7-0 계층 3, 확정)
Module 10은 계층 3(계산 결과)이다. 원본 변경 후 Recalculate 실행 시에만 값이 갱신된다.
화면 상단 "Final Calculation" 시각과 "● Need Recalculation" 표시를 유지한다. (Ⅳ-7-2)
Recalculate 버튼: 우측 상단, Download 좌측. Admin만 활성. (Ⅳ-7-1)
Recalculate 순서: Module 9 → Module 10 계산 결과 갱신. 결과 화면에 Warning 목록과 'BOM 미등록 n건', 'RTF/Prod. 자동 생성 n건'을 표시한다. (M6-1 규칙 C, Ⅲ-4-3)
Recalculate 중 다른 사용자의 실행 요청은 대기 메시지로 처리한다. (Ⅳ-7-9)

[9. Weekly Reset] (Ⅳ-7-4 확정, 스크린샷 10 팝업 반영)
위치: 우측 상단, Recalculate 좌측. Admin만 활성.
팝업 1: "Do you want to restart Weekly PSI analysis?" — Reset 대상: Inventory, Plan, PO, Scheduled Receipt. [Cancel] [Confirm]
팝업 2: "Upload new weekly data in this week." — 대상: Inventory, Plan, PO, Scheduled Receipt. [OK]
Reset 후 해당 작업 주차의 Inventory, Plan(RTF·Prod.), Open PO, Scheduled Receipt Data를 비우고 새 Upload를 받는다. (Ⅳ-6-6, G-9)
Material Master, Assy Master, BOM, Safety Stock은 Reset 대상이 아니다. (Ⅳ-7-5, 모듈 1~4는 항상 최신 유지)
Weekly Reset 팝업과 화면 언어는 Ⅳ-3-4 정책(영문 기본, 한글 병기 가능)을 따른다.

[10. Download]
선택한 작업 주차, Plan, 검색 조건에 해당하는 전체 행(4행 블록 전체)을 Download한다.
Download 값은 계산 원본값(소수점 10자리)이며, 화면 표시는 소수점 둘째 자리이다. (Module 9 [7] 규칙과 동일)
Download 양식 Column: Mat. Code / Desc. / Spec. / Unit / Opening Inventory / Open PO / Plan / PSI / 14개 주차 / Status

[11. 권한]
Admin: 조회, 검색, Download, Recalculate, Weekly Reset (Ⅴ-1 권한 Matrix)
Master / User / Guest: 조회, 검색, Download (Recalculate, Weekly Reset 버튼 비활성화, Backend 거부)

[12. Audit Data]
Recalculate와 Weekly Reset 시 기록: 사용자 ID, 실행 시각(UTC 저장, Local 표시), 작업 주차, 대상 Module, Warning 건수(유형별), Error 건수, 결과(성공/실패) (Ⅰ-9 감사 기록 원칙)

[13. Acceptance Criteria]
① Requirement 행의 주차 값은 Module 9 Total 행과 같다.
② RTF 기준 Opening Inventory = Material 재고 + Σ(Assy 재고 × 소요원수), Prod. 기준 = Material 재고 (스크린샷 10 예: RTF 6,800, Prod. 5,000과 같은 구조).
③ Inventory Balance = 전 주차 값 + 입고예정 − 소요량이 주차별로 누적 계산된다.
④ PO Balance = Opening Inventory + Open PO 잔량 − 누적 소요량이며, Scheduled Receipt는 포함하지 않는다.
⑤ 음수 셀은 붉은 계열 배경으로 표시된다.
⑥ Calculated 입고예정은 파란색, Manual 입고예정은 검정색으로 표시된다.
⑦ Recalculate 전에는 이전 계산 결과를 유지하고 'Need Recalculation'을 표시한다.
⑧ Weekly Reset은 Inventory, Plan, PO, Scheduled Receipt만 비우고, 모듈 1~4 Data는 유지한다.
⑨ Desc., Spec., Unit은 Material Master 값이며, No DB Material은 빈 칸으로 표시된다.
⑩ Admin 이외 계정에서 Recalculate와 Weekly Reset 버튼이 비활성화되며, 서버에서도 거부된다.
⑪ 화면에 Save, Upload, 수정 입력란이 없다.

[14. 스크린샷 10 확인 결과]
수정본 스크린샷 10의 계산 예시 값(RTF W44 Opening 6,800, Open PO 11,000, Inventory Balance W44 8,600, PO Balance W44 16,600, Prod. W44 Inventory Balance 7,000)은 위 [2] 계산식과 모두 일치한다.
Unit Column은 수정본에 반영되어 있다. Module 9와 같은 기준(Material Master, 없으면 빈 칸)을 적용한다.
Desc.와 Spec.은 수정본대로 각각 별도 열로 표시한다. (Module 9의 "Desc. / Type" 통합 열과 다른 Module이므로 헤더를 맞출지 검토 필요, 권장: 본 Module은 별도 열 유지)

[15. 확정 사항 참고]
Ⅲ-4-1 (기초재고 기준), Ⅲ-4-2 (PO 과부족), Ⅲ-4-3 (BOM 미등록 Warning), Ⅳ-6-5·6-6 (과거 주차·새 주차), Ⅳ-7-0 (3계층), Ⅳ-7-1·7-2·7-4·7-9 (재계산, 표시, Weekly Reset, 동시 실행), F-9, R-2 (Material/Desc. 검색), M-1, Q-1, Module 8 SR-1·SR-2를 반영했다.

────────────────────
Ⅶ. 표준 업로드 양식 (Upload Data 구조)
────────────────────
본 절은 각 Module의 Excel Upload 양식(시트명, Column)을 정의한다.
첨부 '표준 업로드 양식_1123.xlsx'가 본 절의 Excel 구현본이다. 시트별 캡쳐 파일명은 'Upload모듈번호_Sheet명.png' 형식을 따른다 (예: Upload03_BOM.png). 본 절은 제공된 시트 캡쳐와 대조하여 확인한다.
공통 규칙은 Ⅳ-5-1(표준 업로드 양식 규칙)과
Ⅳ-6-1-1(주차 표기 규칙)을 따른다.
각 Module의 화면 규칙과 Upload Mode의 세부 처리는
해당 Module(Ⅵ-n) 정의 단계에서 사용자와 확인 후 확정한다.
본 절은 Data 구조와 이미 확정된 업무기준만 정리한다.

[1. Module별 Upload 시트]
Module                 시트명            Data 구분 기준
Material Master     MD_Material       Material Code
Assy Master         MD_Assy           Customer Code
BOM                 BOM               Customer Code + Material Code (Key 아님, Ⅵ-3 참조)
Safety Stock        SAFETY            Customer Code
Inventory           INVENTORY         Code
RTF/Production      RTF               Customer Code
PROD_PLAN           PROD_PLAN         Customer Code
Open PO             OPEN_PO           Upload 행 단위 (시스템 내부 ID)
Scheduled Receipt   SCHED_RECEIPT     Material Code + Vendor

[2. 주차 Column 공통] (확정)
PROD_PLAN, SCHED_RECEIPT 시트는
Code Column 뒤에 14개의 주차 Column을 둔다.
RTF 시트의 14번째 주차는 업로드된 수량(공백 허용)에 Safety Stock(SAFETY 시트) 수량을 시스템이 합산한다. (Ⅲ-4-1)
주차 Column Header는 YYYY-Www 형식이다.

규칙:
첫 번째 주차 Column = 작업 주차
작업 주차부터 연속된 ISO Week (RTF 14개, PROD_PLAN·SCHED_RECEIPT 14개)
주차 Column 수가 위 개수와 다르거나,
첫 주차가 작업 주차와 다르거나,
중간에 빠지거나 중복된 주차가 있으면 Upload Error
예 (작업 주차 = 2026-W44):
2026-W44, 2026-W45, ... , 2026-W53, 2027-W01, ... , 2027-W04
빈 Cell = 0
음수 불가

[3. MD_Material]
Ⅵ-1 Material Master참조.

[4. MD_Assy]
Ⅵ-2 Assy Master 참조.

[5. BOM]
Column:
Customer Code    필수, Assy Master내 존재여부, Status와 무관
Material Code    필수, Material Master내 존재여부나 Status와 무관, Assy 열은 'Assy' 입력
Assy 열 식별: Material Code가 'Assy'(정규화 후)인 행만 Assy 열로 인정하며, 해당 행의 Unit·Q'ty 값은 무시한다. 자재 코드 'ASSY'는 사용 금지 코드로 등록하여 Material Master에 등록하거나 Upload할 수 없게 한다.

Unit             자재 열 필수, Material Master의 'Unit'가 다를 경우 Error 발생 (Assy 열 값은 무시)
Q'ty             자재 열 필수, 소요원수, 0보다 큰 숫자 (소수·분수 문자열 허용, Assy 열 값은 무시)
Level, Desc., Spec., Type, Model, Item, Update는 Upload하지 않는다.
화면에서는 Material Master, Assy Master 기준으로 시스템이 표시한다. (Ⅵ-3 [시스템의 화면 표시 항목])
Ⅵ-3 BOM에서 세부 규칙을 확정한다.


[6. SAFETY]
Safety Stock은 Assy 기준으로 관리한다. (확정)
Upload 방식: 파일 선택 후 Upload하여 전체교체한다 (일부 코드만 수정 불가). 기존 Data는 Update 기준으로 History에 보관한다. (Ⅳ-5)
Column:
Customer Code    필수, Assy Master내 존재여부나 Status와 무관
Safety Q'ty      필수, 0 이상의 숫자 (Assy 단위)
Excel 내부 Customer Code 중복 불가.
화면 공통: Status 열(Assy Status) 맨 우측 표기, History Download 제공 (Ⅳ-3-1).
과부족 반영 (확정):
Safety Q'ty는 RTF 기준 14주차 소요량에 합산된다. (Ⅲ-4-1)
RTF 기준 소요량에만 포함한다. (Ⅲ-4-1) Production Plan 기준에는 반영하지 않는다.
Safety Stock 화면의 'Weeks' Column은 사용하지 않는다.

[7. INVENTORY]
Material 재고와 Assy 재고를 하나의 시트로 Upload한다.
Upload 방식: 작업 주차의 기존 Data 전체를 파일로 대체한다. 기존 Data는 삭제하며 History는 두지 않는다. (Ⅳ-5)
Category(Assy 또는 Material) 라는 구분자를 두어 입력한다. 
Column:
Category         필수, Material 또는 Assy
Code             필수
Unit             Material 행 필수, Material Master와 동일 여부 확인.
Assy 행은 Unit을 표기하지 않으며 Unit Validation 대상이 아니다. (Assy는 EA만 사용)
Stock Q'ty       필수, 0 이상의 숫자, 소수점 6자리까지 허용 (예: 0.5, 0.123456). 소수점 7자리 이상은 Error이며 자동 반올림하지 않음 (IN-2 수정 확정, 2026-11)
재고 기준 (확정):
재고 기준시점 = 작업 주차 월요일 아침 재고
이 재고를 작업 주차의 기초재고로 사용한다.
ROH / WIP 구분 없이 합계(TOTAL) 수량만 관리한다.
재고의 사용:
Material 재고 → RTF 기준, Production Plan 기준 모두 사용
Assy 재고     → RTF 기준에만 사용 (Ⅲ-4-1 참조)

[8. RTF / PROD_PLAN]
RTF와 Production Plan(VN PLAN)은 각각 별도 시트로 Upload하고
각각 별도로 저장한다.
Column:
Customer Code    필수, Assy Master내 존재여부나 Status와 무관
Plan             필수. RTF 시트는 'RTF'만, PROD_PLAN 시트는 'Prod.' 또는 'Production'만 허용. 허용값 외는 Upload Error.

3~16. 주차 Column  RTF 14개 / PROD_PLAN 14개 (Ⅶ-2 참조), Assy 단위 수량
단위는 EA로 고정하며 0 이상의 정수만 허용한다. 소수는 불가하다. (2026-11 확정, Safety·RTF·Production Plan 공통)
화면 필터: Plan(All / RTF / Prod., Prod. = Production Plan의 약칭) + 검색조건(Customer Code / Assy Code / Type) + 검색어 + Search 클릭 시 실행. Status 열(Assy Status) 맨 우측 표기 (Ⅳ-3-1).

Upload 방식: 작업 주차의 기존 Data 전체교체 (Ⅳ-5).
"Safety/W+ww" 으로 표기한다(예: Safety/W+13)

14번째 열(14주차)은 Safety Stock을 더하는 주차를 의미한다.
RTF 행 14주차 = 업로드 수량(공백은 0) + Safety Stock (자동 합산, 화면 수정 불가)
Production 행 14주차 = 업로드 수량(공백은 0)
Excel 내부 Customer Code 중복 불가.
(중복 시 합산하지 않고 Upload Error)

계획수량이 있는데 BOM이 없는 Assy는
Upload는 허용하고, 계산 단계에서 경고 목록으로 표시한다. (Ⅲ-4-3)

[BOM 유무 Column] (수정 파일 확정)
모듈 6(RTF/Production Plan) 화면 맨 우측(Status 우측)에 'BOM 유무' Column을 추가한다.
기준: 모듈 3(BOM)에 해당 Customer Code 기준으로 Assy 열이 1개 있고 이어서 Material 열이 1개 이상 있으면 'YES', 그 외에는 'NO'로 표기한다.
BOM 유무와 무관하게 다른 Module의 Upload는 막히지 않는다.


[9. OPEN_PO]
Upload 방식: 작업 주차의 기존 Data 전체교체. Upload는 Admin만 가능하며 화면 수정은 불가하다. (Ⅳ-5)
Open PO는 공급업체에 발주된 수량 중 미입고된 수량을 말한다.
납품, 검수, 송장 처리, 결제가 완료된 자재는 재고(Inventor)로 전환됨.
용어 정의:
PO Q'ty = 최초 발주된 수량
Cancel = 발주가 취소된 수량
Final PO = (최초 발주에서 취소 수량을 차감한 주문 수량)
= PO Q'ty - Cancel (시스템이 자동 계산)

G/R = 입고 수량(Good Receipt)
In Transit: 업체에서 출하되어 운송중인 수량
Remain Qty: 업체에서 아직 출하되지 않은 수량
Open PO = 발주된 수량 중 미입고된 수량
= In Transit + Remain Q'ty
= Final PO - G/R Q'ty
= PO Q'ty - Cancel - G/R Q'ty

Open PO는 잔량이 0인 PO를 포함한 전체 PO 목록을 Upload하고,
시스템이 Open PO(잔량 > 0)만 걸러서 사용한다. (확정)
시스템 화면 Column:
PO Date          Upload 필수, 날짜(yyyy-mm-dd)
PO No            Upload 필수
Material Code    Upload 필수, Material Master내 존재여부나 Status와 무관
Unit             Upload 필수, Material Master의 Unit과 비교하여 상이하면 Error
PO Q'ty          Upload 필수, 0보다 큰 숫자, 소수점 6자리까지 허용 (2026-11 확정)
Currency         Unit Price를 입력한 경우 Upload 필수
허용값: USD, KRW, VND, CNY, JPY
Unit Price       Upload 선택, 0 이상의 숫자, 소수점 6자리까지 허용, 빈 Cell은 미입력 (Amount도 빈칸)
Amount           시스템 자동 계산(Unit Price를 미입력한 경우 빈칸, 2026-11-24 확정), Upload 값 제외
Cancel           Upload 선택, 0 이상의 숫자, 소수점 6자리까지 허용, 빈 Cell = 0
Final PO         시스템 자동 계산, Upload 값 제외
G/R              Upload 선택, 0 이상의 숫자, 소수점 6자리까지 허용, 빈 Cell = 0
In Transit       Upload 선택, 0 이상의 숫자, 소수점 6자리까지 허용, 빈 Cell = 0
(Upload Header 명칭은 표준 업로드 양식 실제 시트 기준: Currency, Cancel, G/R, In Transit. 2026-11-24 확정)
Remain Q'ty      시스템 자동 계산, Upload 값 제외
Remain Amount    시스템 자동 계산, Upload 값 제외
Vendor           Upload 필수, 문자열. 문자 사이 공백 가능, 빈 칸 불가 (OP-1 확정)
Remain Q'ty 는 반드시 0보다 크거나 같아야 하며 0보다 작을 경우 Error.

PO Line과 ETA Column은 사용하지 않는다. (확정)
같은 PO No 안에 같은 Material Code가 여러 행이면
각각 별도 행으로 저장한다. (병합하거나 Error 처리하지 않음)
최종 PO(Final PO)와 잔량(Remain Q'ty)은 Upload하지 않고 시스템이 계산한다.

Open PO 화면 Column 순서 (확정):
PO Date, PO No, Material Code, Unit, PO Q'ty, Curr., Unit Price, Amount,
Cancel, Final PO(계산), G/R, In Transit, Remain Q'ty(계산), Remain Amount(계산), Vendor
최종 PO는 Cancel 바로 오른쪽에 표시한다.
최종 PO, Remain, Remain Amount는 시스템 계산 값이며 화면에서 수정할 수 없다.

Upload Column 순서 (확정):
PO Date, PO No, Material Code, Unit, PO Q'ty, Currency, Unit Price,
Cancel, G/R, In Transit, Vendor
Amount, Final PO, Remain Q'ty, Remain Amount는 시스템 계산 값이며 화면에서 수정할 수 없다.

Open PO 판단 (확정): 각각의 행 별로 아래의 기준을 적용한다
In Transit + Remain Q'ty > 0  → Open PO (계산에 사용. Remain Q'ty = 0이어도 In Transit > 0이면 포함)
In Transit + Remain Q'ty = 0  → 합계 영향 없음, Open PO 목록에서 제외
Remain Q'ty < 0               → Error 처리, 수정해서 다시 등록하도록 안내
(2026-11-24 확정)

Material + Vendor 기준으로 Open PO(= In Transit + Remain Q'ty) − SCHED_RECEIPT 14주 합계 = 차이분 (수정 파일 확정)

차이분 < 0 → Upload Error (Ⅶ-10). 모듈 7·8을 수정한 후 진행한다.
차이분 ≥ 0 → 차이분을 Material Master의 L/T(Weeks)를 감안하여 '작업 주차 + L/T' 주차에 Calculated Scheduled Receipt로 반영한다. (Ⅶ-11)

[10. SCHED_RECEIPT]
Scheduled Receipt(현재 Excel의 Input Plan)는 'Material + Vendor' 기준으로  
주별 수량으로 입력한다. (확정)
같은 Vendor의 같은 자재 일별 입고계획은 사용자가 주별로 합산하여 입력한다.

Upload 파일 Column:
Material Code    필수, Material Master내 존재여부나 Status와 상관없이 업로드 되어야 한다. (화면상에 Active, Inactive, No DB만 표기하는 것으로 사용자에게 경고하도록 함) 
Vendor           필수
Unit             필수, Material Master의 Unit과 비교하여 상이하면 Error

4~17. 주차 Column   14개 (Ⅶ-2 참조), Material 단위 수량, 소수점 6자리까지 허용 (2026-11 확정, Module 8)
이 시트로 Upload한 Data는
Ⅳ-7-7의 ① Manual Scheduled Receipt로 관리한다.
In Transit 수량의 도착 예정분도 이 시트에 입력한다. (Ⅶ-9)

중복 행 처리 (확정):
같은 Material Code + Vendor가 여러 행이면 담당자가 주차별로 수량을 합산하여 업로드하여야 한다. 중복하여 존재하면 Error처리하고 다시 등록하도록 한다

Open PO 초과 입고예정 처리:
Material + Vendor별 Scheduled Receipt 14주 합계가
해당 Material + Vendor의 Open PO(= In Transit + Remain Q'ty)보다 크면 Error 처리하여 조치하도록 한다.

Open PO 차이분(Open PO − SCHED_RECEIPT 14주 합계)이 0보다 크면, Master Data의 L/T(Weeks)를 기준으로 '작업 주차 + L/T' 주차의 입고예정에 합산하고 파란색으로 표기한다. (상세 계산 규칙은 Ⅶ-11)

────────────────────
Ⅶ-11. Calculated Scheduled Receipt (L/T 기준 입고예정) (수정 파일 확정)
────────────────────
계산 단위: Material Code + Vendor (Ⅶ-9, Ⅶ-10과 동일)
L/T: Material Master의 L/T(Weeks)
계산식 (작업 주차 기준)
① 차이분 = Open PO 합계(= In Transit + Remain Q'ty, Remain = 0 포함) − SCHED_RECEIPT 14주 합계
② 차이분 < 0 → Upload Error (Ⅶ-10). 계산하지 않는다.
③ 차이분 = 0 → Calculated Scheduled Receipt 없음.
④ 차이분 > 0 → 입고 주차 = 작업 주차 + L/T(Weeks). 해당 주차의 입고예정에 차이분 수량을 합산한다. (Upload 숫자에 합산, 파란색)
⑤ 입고 주차가 W+13을 넘는 경우에도 14주차(W+13) 열에 합산하여 반영한다. (2026-11 확정)


예:
작업 주차 = 2026-W44, A자재 Open PO 합계 = 50, SCHED_RECEIPT 14주 합계 = 0, L/T = 8 Weeks
차이분 = 50 − 0 = 50
입고 주차 = W44 + 8주 = 2026-W52 (W+8)에 50을 Calculated Scheduled Receipt로 표시

PSI 표시 (Ⅵ-10 Material PSI 화면 기준)
입고예정은 입력분과 계산분을 나누지 않고 "입고예정" 한 행으로 표시한다.
글씨색으로 구분한다. (셀 배경색은 사용하지 않는다)
검정 = Manual Scheduled Receipt (엑셀 Upload 숫자)
파랑 = Calculated Scheduled Receipt (Open PO 차이분 L/T 반영분)
같은 주에 두 종류가 함께 있으면 합계를 표시하고 파랑으로 표기하며, 셀 클릭 시 구성 내역(입력분/계산분)을 보여준다.

PSI 행 구성 (기준별, Material별):
소요량(Requirement) / 입고예정(Scheduled Receipt) / 재고 과부족(Inventory Balance) / PO 과부족(PO Balance)

고정 Column 순서 (확정):
Material, Desc., Spec., 기초재고(Opening Inventory), Open PO, 기준, 항목, 주차 14개
마지막(14번째) 열 (Ⅲ-4-1, Ⅶ-8):
RTF 기준 행 = 14주차 소요량 (업로드 수량 + Safety Stock)
Production 기준 행 = 14주차 소요량 (업로드 수량)
Open PO = 해당 Material의 Open PO 합계 (In Transit + Remain Q'ty, Open PO > 0인 건만)
PO 과부족 계산에 사용하는 값과 같으며, 기준(RTF/Production) 행마다 같은 값을 표시한다.
재고 과부족과 PO 과부족이 마이너스인 셀은 강조 표시한다.
셀에 마우스를 올리거나 클릭하면 해당 PO No, PO Date, 수량을 확인할 수 있게 한다.
RTF 기준과 Production Plan 기준 PSI 모두 같은 Scheduled Receipt(입력분 + 계산분)를 사용한다.
재계산:
Open PO, SCHED_RECEIPT, L/T가 변경되면 Calculated Scheduled Receipt는 화면 조회 시 실시간으로 다시 산출된다(계층 2). 모듈 9~10 반영은 Recalculate 실행 시 Current Week에 한한다.
차이분이 음수가 되면 화면에 경고(빨간색)를 표시하고, Recalculate 실행 시 Error로 차단한다.
과거 주차 Snapshot은 재계산하지 않는다. (Ⅳ-6-5)





────────────────────
Ⅷ. 미결정 사항 목록
────────────────────
AI는 개발 전에 아래 "미결정" 항목을 [확인 필요]로 사용자에게 질문한다.
사용자가 답하기 전에는 임의로 결정하지 않는다.
[권장안]이 있는 항목도 사용자 승인 전에는 확정된 규칙이 아니다.

[1. 미결정 항목]
A-1. 시스템 운영환경 (서버 위치: 사내 서버 / Cloud, DB 종류, 개발 도구)
→ 사용자는 아직 선호가 없다. AI는 2~3개 대안의 비용·보안·유지보수 난이도를 비교한 [권장안]을 먼저 제시하고 선택을 받는다.
C-3. 발주필요수량 계산식 (L/T, 안전재고, MOQ 반영 여부) → v1.0 범위 외. 다음 버전으로 이관하며 확장 구조만 확보 (Ⅰ-5 확정)
I-1. 동시 Excel Upload 처리 (Ⅰ-11) → 거절 + 안내 메시지로 확정 (2026-11-24, H-5)
Q-1. Q'ty 실제 저장 방식은 분수로 확정(불가능할 경우 소수점 10째 자리로 제안해 줄것) (확정)
M-1. Material Requirement의 BOM Row 합산 표시 수준 — 모듈 9, 10에서는 Material Code 기준으로 합산하여 관리 (Open PO, Scheduled Receipt에서만 Material Code + Vendor로 관리) (확정)
R-1. 모듈 6 검색조건: Customer Code / Assy Code / Type (확정)
R-2. 모듈 10 검색조건: 10번 화면 스케치는 Material / Desc. 검색(확정)
R-3. 모듈 2 검색조건: Ⅵ-2-12 기준(Cust. Code, Assy Code, Type, Model, Item, Customer, Country) 적용 (확정)

R-4. Ⅶ-11 예시: W44 + L/T 8주를 W52(W+8) (확정)
R-5. 납기 지연(PO Date 기준 입고 주차 지연) 개념과 빨강 표시는 수정 파일의 작업 주차 + L/T 방식과 충돌하여 삭제함. (확정))

R-6. Calculated Scheduled Receipt 계산 단위: Material + Vendor (확정)

[2. 확정된 항목 (참고)]
A-2. 임시 Password 통보 수단 = e-mail 발송 (Ⅴ-5) [수정 파일 확정]
A-3. Master ID = novamaster (Ⅴ-1)
A-4. 보안: Password 8자 이상·영문+숫자, 5회 실패 시 10분 잠금, 2시간 미사용 시 자동 Log-out (Ⅴ-1-7)
A-5. 동시 편집 = Optimistic Lock (Ⅰ-11)
A-6. 주차 전환 시 지난 주 확정, 새 주차는 빈 상태로 시작 (Ⅳ-6-6, 수정 파일 반영)
A-7. Recalculate는 한 번에 하나만 실행 (Ⅳ-7-9)
A-8. Final Calculation 시각 + "● Need Recalculation" 알림 표시 (Ⅳ-7-2)
B-1. Code 문자 제한 없음, 앞뒤 공백 제거, 영문 대문자 통일 (Ⅵ-1-4-0)
B-2. Assy Code 중복 허용 (Ⅵ-2-2)
B-3. Unit 허용값 목록 + 대문자 변환 (Ⅵ-1-4 ④)
B-4. Purchaser는 사용자 ID로 연결 (Ⅵ-1-4 ⑤)
B-5. Vendor 자유기재 유지 (Ⅵ-1-4 ⑥)
B-6. L/T 필수, 1 이상의 정수 (Ⅵ-1-4 ⑧)
B-7. 사용 중인 Code의 Inactive 차단 (Ⅵ-1) → Inactive 전환 허용(확정)
B-8. Module 1~4는 작업 주차 Dropdown 미표시 (Ⅳ-6-2)
B-9. 체크박스 다중 선택 + 수정 시 자동 선택 (Ⅵ-1-9-1)
B-10. Purchaser ID는 계정 Status와 무관하게 지정 가능, Approved 전에는 해당 사용자 Log-in 불가 (Ⅵ-1-4 ⑤)
B-11. BOM 표시 속성(Type, Model, Item)은 Assy Master 기준 표시. BOM에 Desc./Comment 표시 항목은 없음 (Ⅵ-3)
C-1. RTF 기준 Assy 재고는 BOM 소요원수로 Material 환산 후 합산 (Ⅲ-4-1)
C-2. Safety Stock은 RTF 14주차 열에 합산, RTF 기준 소요량에만 포함 (Ⅲ-4-1, Ⅶ-6)
C-4. BOM 없는 Assy는 경고 후 나머지 계산 진행 (Ⅲ-4-3)
D-1. 주차 Column = 작업 주차부터 연속 14주 (Ⅶ-2)
D-2. 재고 = 월요일 아침 재고, TOTAL만 관리 (Ⅶ-7)
D-3. Open PO Remain Q'ty 음수 = Error (Ⅶ-9)
D-4. In Transit은 사용자가 Scheduled Receipt로 입력 (Ⅶ-9)
D-5. PO Line, ETA 미사용 (Ⅶ-9)
D-6. Currency Column 추가 (Ⅶ-9)
D-7. Scheduled Receipt 같은 Material+Vendor 중복 행은 Error, 합산하지 않음 (Ⅶ-10, 2026-11 확정)
D-8. Scheduled Receipt 14주 합계가 Open PO보다 크면 Error (Ⅶ-10)
E-1. Guest 권한: 사용자 관리 외 모든 Module 조회/다운로드, 새로고침 불가 → 재계산 불가로 정정, Master 승인 시 Class를 Guest로 지정 (Ⅴ-1-3-1)

[2026-11 추가 확정]
F-1. Open PO = In Transit + Remain Q'ty. "Open PO 잔량"은 "Open PO"로 통일 (Ⅲ-4-2-1, Ⅶ-9)
F-2. Remain Q'ty = 0 포함, 음수는 Error (Ⅶ-9)
F-3. Material + Vendor 기준 차이분(Open PO − SCHED_RECEIPT 14주 합계)을 작업 주차 + L/T 주차에 Calculated Scheduled Receipt로 합산 (Ⅶ-10, Ⅶ-11, 수정 파일 반영)
F-4. RTF 14주차 = 업로드 수량 + Safety Stock, 14번째 열 Header는 "Safety/W+13", Prod. = Production Plan 동의어 (Ⅲ-4-1, Ⅶ-8)
F-5. BOM은 Assy Status·Material Status와 독립. Inactive Assy도 BOM 등록 가능 (Ⅵ-3)
F-6. BOM Upload는 Add / Change 2종. Change는 Assy 단위 전체교체, Add는 기존 Assy 무시. 파일에 없는 Assy의 기존 BOM 유지, 자재 열이 없는 Assy는 무시 (Ⅵ-3)
F-7. BOM Update는 같은 Assy의 모든 행이 같은 값, 내부 hh:mm, 화면 yyyy-mm-dd (Ⅵ-3)
F-8. History 행의 표시 항목은 이력 시점 값 (Ⅵ-1-13-1, Ⅵ-2-13-1, Ⅵ-3)
F-9. Inactive Assy 수량·Inactive Material 행은 Material Requirement에 포함 계산하고 점검 목록을 Warning 등급으로 표시 (Ⅵ-3, 2026-11 수정)
F-10. Assy 단위는 EA 고정, Unit 표기·Validation 없음 (Ⅵ-2, Ⅶ-7)
F-11. History 조건은 화면 검색 결과 기준, 팝업 없음 (Ⅳ-3-1)
F-12. Status 필터 기본값 Active, Search 클릭 시 실행. Status 화면 편집은 Admin만 가능 (Ⅵ-1, Ⅵ-2)
F-13. Excel 날짜 자동 변환 Q'ty는 Error (권장안 반영) (Ⅵ-3)
F-14. Material Master Unit 변경 시 기존 BOM의 Unit 불일치는 Error (Ⅵ-3, 2026-11 변경)
F-15. 같은 Customer Code의 Assy 열 2회 이상은 Error, 동일 내용 재Upload는 이력 미생성 (Ⅵ-3)
F-16. Validation 결과 Excel Download 제공 (Ⅵ-3)
[2026-11 수정 파일 반영]
G-1. Upload 방식: 모듈 1·2는 Type 3종(Add / Change / Inactive), 모듈 3은 Type 2종(Add / Change), 모듈 4는 전체교체, 모듈 5~8은 작업 주차 전체교체 (Ⅳ-5)
G-2. 모듈 1~2만 Row 선택·Save 유지, 모듈 3~10은 Save·Row 선택 없음, Delete 기능 전체 삭제 (Ⅳ-3-0)
G-3. '새로고침' 전체 삭제. Recalculate·Weekly Reset은 모듈 10 화면 Admin 전용 (Ⅳ-7)
G-4. Recalculate = 모듈 1~8 현재 정보 기준으로 모듈 9·10 재계산. 부분(Dependency) 재계산은 삭제 (Ⅳ-7-1)
G-5. 권한: 모듈 1~8 Upload와 모듈 1~2 화면 수정은 Admin만. User는 모듈 7·8 포함 조회·Download만 (Ⅴ-1)
G-6. 모듈 1 Excel 내 Code 2회 이상 Error, 엑셀 수정 후 재업로드 안내 (Ⅵ-1-7)
G-7. 모듈 6에 BOM 유무 Column 추가 (Ⅶ-8)
G-8. 상대 주차 표기 W±ww (Ⅳ-6-1-2)
G-9. 새 작업 주차 Data 자동 복사 없음, 빈 상태 시작 (Ⅳ-6-6)
G-10. Safety Stock 전체교체 + Update 기준 History (Ⅶ-6)
G-11. Calculated Scheduled Receipt = 차이분을 작업 주차 + L/T 주차에 반영 (Ⅶ-11)
G-12. 표준 업로드 양식_1123을 Ⅶ 기준으로 사용 (Ⅶ)
G-13. 약어 표기 규칙 (문서 상단)
G-14. 주차 Header·DB는 YYYY-Www 유지, 화면만 'W44(W0)' 병기 (Ⅳ-6-1-2, 권장안 채택)
G-15. Master 미등록 Code 업로드 허용, 'No DB' 표시·계산 포함, Warning 보고 (Ⅰ-8 예외, 권장안 채택)
G-16. BOM 미등록 Assy 소요량 0 간주 + Warning 목록, Recalculate 결과에 'BOM 미등록 n건' 표시 (Ⅲ-4-3, 권장안 채택)
G-17. 14주 초과 입고예정은 W+13 열에 합산 반영 (Ⅶ-11 ⑤)
G-18. 같은 Material+Vendor 중복 입고예정 행은 Error (Ⅶ-10, D-7)
G-19. Error / Warning 2단계 등급 적용 (Ⅳ-7-10, 2026-11 확정)
G-20. 화면 기본 언어 영문, 필요 시 한글 병기 (Ⅳ-3-4)
[2026-11-24 확정 (권장안 채택)]
H-0. 운영환경(A-1): PoC는 사용자 PC Local Hosting, DB는 PostgreSQL. 실제 운영환경은 PoC 후 재결정
H-1. Material Master Unit 필수 (Ⅵ-1-4 ④, Ⅵ-1-5)
H-2. 사용자 ID: 영문·숫자·'.'·'_'·'-' 허용, 대소문자 구분 없음(소문자 저장) (Ⅴ-3-1)
H-3. Open PO 계산 대상 = In Transit + Remain Q'ty > 0 인 행 (Ⅲ-4-2-1, Ⅵ-7-7, Ⅶ-9)
H-4. OPEN_PO Upload Header = Currency, Cancel, G/R, In Transit (실제 시트 기준). Unit Price 미입력 시 Amount 빈칸 (Ⅶ-9)
H-5. 같은 Module·같은 작업 주차 동시 Upload는 거절 + 안내 메시지 (Ⅰ-11, I-1)
H-6. 표준 업로드 양식 안내 시트를 MD 기준으로 갱신 (v1124). Material Code 'ASSY' 금지를 Ⅵ-1 Validation에 추가
────────────────────
[이번 요청]
────────────────────
이번 단계에서는 Coding을 하지 않는다.
Ⅷ의 A-1(운영환경)에 대해
대안 비교와 [권장안]을 제시하고 나의 선택을 받는다.
전문용어는 초보자도 이해할 수 있게 간단히 설명한다.
Ⅰ~Ⅴ의 공통 시스템 기반 기능과 Ⅵ-1 Master Data에 대해
Ⅰ-6의 확인 항목을 정리하여 보여준다.
Ⅶ의 표준 업로드 양식이 Ⅵ-1 및 Ⅲ-4의 계산 기준과
충돌하는 부분이 있는지 검토한다.
문서 안에서 서로 충돌하거나 모호한 부분을 추가로 발견하면
[확인 필요]로 정리하여 한 번에 최대 5개까지만 질문한다.
Ⅵ-4 이후 Module은 순서대로 정의하며, 사용자가 "다음 모듈 진행"을 지시하기 전까지 설계하지 않는다.
내가 "개발 시작"이라고 지시할 때까지 다음 단계로 넘어가지 않는다

────────────────────
[3. 2026-11 확정 사항 추가 (Module 3~10 및 화면 규칙)]
모듈 4 Safety Stock: Safety Q'ty는 0 이상의 정수. 기본 정렬 Cust. Code 오름차순. Status 필터(All / Active / Inactive / No DB) 추가. (M4-1~3)
모듈 5 Inventory: Stock Q'ty 소수점 6자리 허용, Status 필터 없음, No DB 재고는 계산 반영 후 Warning, 작업 주차 'W44(W0)' 표기, Remark 열 헤더 'Type / Desc.'. (IN-1~4)
모듈 6 RTF/Production: 단위 EA, 0 이상의 정수. 한쪽 계획만 있으면 나머지를 0으로 자동 생성(업로드 시), Safety만 있는 Customer Code는 RTF(W+13=Safety)와 Prod.(전주 0)를 Recalculate 시 생성. Status 필터 없음. Download는 업로드 원본값. (M6-1~3)
모듈 7 Open PO: Vendor 필수(문자 사이 공백 허용), PO No 필수, PO Q'ty·Unit Price·Cancel·G/R·In Transit 소수점 6자리 허용. Remain 0 행은 Open PO 목록에서 제외. (OP-1~3)
모듈 8 Scheduled Receipt: 계산 입고예정은 조회 시 실시간 산출하며 저장하지 않음. No DB 자재는 계산 생략 + Warning. Open PO 없는 Material+Vendor 입고예정은 Error. 기본 정렬 Mat. Code → Vendor. (SR-1~3)
모듈 9 Material Requirement: Total 행(Material 합계, Desc./Spec. 표시) + Assy 행(Type/Model 표시) 구조. Status는 행 종류별 Master 기준. 계산 10자리, 화면 소수 둘째 자리, Download 10자리. Unit 열 추가. (M9-1~3)
모듈 10 Material PSI: 열 헤더 '항목'을 'PSI'로 변경. Opening Inventory는 RTF 기준(Material + Assy 환산), Prod. 기준(Material만). PO Balance는 Scheduled Receipt 제외. Weekly Reset은 Inventory, Plan, PO, Scheduled Receipt만 초기화. Unit 열 추가. Desc./Spec. 별도 열. (스크린샷 10 수정본)
Module 3 BOM: Assy 행 강조, No DB 표시 규칙, Upload Type Add / Change 2종, 자재 열 없는 Assy 무시, History는 이력 시점 값 표시. (Ⅵ-3 정리본)
화면 공통 (Ⅳ-3-6): Status 색상, 집계 행 강조, 음수 셀 색상, Calculated 입고예정 파란색, Purchaser Request·Disabled 붉은 표기, 행 선택 시 수정 가능 셀 반전.
변경 반영 방식 (Ⅳ-7-0): 원본 즉시 저장, 파생 표시 실시간, 계산 결과 Recalculate 시 반영.
v1.0 범위 외 (Ⅰ-5): 안전재고, MOQ, 발주필요수량 계산, 발주 제안 기능은 다음 버전으로 두고, 확장 가능한 구조만 확보한다. (C-3 확정)
