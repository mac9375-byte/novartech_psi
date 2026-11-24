"""표준 업로드 양식 공통 읽기·쓰기 (Ⅳ-5-1).

- 지정 시트만 읽는다. 없으면 Error.
- 1행 = Header. 앞뒤 공백 제거 후 정확히 일치해야 한다. 순서는 무관.
- 필수 Column 누락 / 병합 셀 = Error. 정의되지 않은 Column은 무시하고 Info로 안내.
- 수식 Cell은 저장된 결과값을 읽는다 (data_only).
- 완전히 빈 행은 무시. 빈 Cell과 "-" 는 NULL.
"""
import io
import re
from datetime import date, datetime, time
from decimal import Decimal, InvalidOperation
from fractions import Fraction

from django.http import HttpResponse
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill

ERROR, WARNING, INFO = "Error", "Warning", "Info"
_EXP_RE = re.compile(r"^[+-]?\d+(\.\d+)?[eE][+-]?\d+$")
_INT_RE = re.compile(r"^[+-]?\d+(\.0+)?$")


def issue(level, sheet, row, field, reason, code=""):
    return {"level": level, "sheet": sheet, "row": row, "code": code, "field": field, "reason": reason}


def is_blank(v):
    return v is None or (isinstance(v, str) and v.strip() in ("", "-"))


def read_sheet(fileobj, sheet, required, optional=()):
    """시트를 읽어 (rows, issues)를 돌려준다. rows = [{'_row': Excel 행 번호, Header: 원래 값, ...}]."""
    try:
        wb = load_workbook(fileobj, data_only=True)
    except Exception:
        return [], [issue(ERROR, sheet, "", "File", "Not a valid Excel (.xlsx) file.")]
    if sheet not in wb.sheetnames:
        return [], [issue(ERROR, sheet, "", "Sheet", f"Sheet '{sheet}' not found.")]
    ws = wb[sheet]
    issues = []
    if ws.merged_cells.ranges:
        cells = ", ".join(str(r) for r in list(ws.merged_cells.ranges)[:5])
        issues.append(issue(ERROR, sheet, "", "Merged cells", f"Merged cells are not allowed ({cells})."))

    cols = {}
    for idx, cell in enumerate(next(ws.iter_rows(min_row=1, max_row=1, values_only=True), ())):
        name = str(cell).strip() if cell is not None else ""
        if not name:
            continue
        if name in cols:
            issues.append(issue(ERROR, sheet, 1, name, "Duplicate column header."))
        cols[name] = idx
    known = list(required) + list(optional)
    for name in required:
        if name not in cols:
            issues.append(issue(ERROR, sheet, 1, name, "Required column is missing."))
    for name in cols:
        if name not in known:
            issues.append(issue(INFO, sheet, 1, name, "Undefined column ignored."))
    if any(i["level"] == ERROR for i in issues):
        return [], issues

    rows = []
    for row_no, values in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        if all(is_blank(v) for v in values):
            continue
        row = {"_row": row_no}
        for name in known:
            if name in cols:
                i = cols[name]
                row[name] = values[i] if i < len(values) else None
        rows.append(row)
    return rows, issues


def to_text(v):
    """일반 문자열 Column. 빈칸·'-' = None."""
    if is_blank(v):
        return None
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return str(v).strip()


def to_code(v):
    """Code Column: 문자열로 읽고 앞뒤 공백 제거 + 영문 대문자 (Ⅵ-1-4-0). 손상된 값은 ValueError."""
    if is_blank(v):
        return None
    if isinstance(v, (datetime, date, time)):
        raise ValueError("Code was converted to a date by Excel.")
    if isinstance(v, bool):
        raise ValueError("Invalid Code.")
    if isinstance(v, float):
        if abs(v) >= 1e15:
            raise ValueError("Number is too long; the Code may be damaged. Use text format.")
        v = int(v) if v.is_integer() else v
    s = str(v).strip()
    if _EXP_RE.match(s):
        raise ValueError("Exponent notation (e.g. 3.04E+11); the Code is damaged. Use text format.")
    return s.upper()


def to_int(v):
    """정수 Column. 빈칸 = None. 정수가 아니면 ValueError."""
    if is_blank(v):
        return None
    if isinstance(v, (datetime, date, time)):
        raise ValueError("Value was converted to a date by Excel.")
    if isinstance(v, bool):
        raise ValueError("Must be a whole number.")
    if isinstance(v, int):
        return v
    if isinstance(v, float):
        if v.is_integer():
            return int(v)
        raise ValueError("Must be a whole number.")
    s = str(v).strip()
    if _INT_RE.match(s):
        return int(float(s))
    raise ValueError("Must be a whole number.")


def to_decimal(v, max_places=6):
    """수량 Column: 숫자(쉼표 허용). 빈칸 = None. 소수 자릿수 초과·날짜·문자는 ValueError (자동 반올림 안 함)."""
    if is_blank(v):
        return None
    if isinstance(v, (datetime, date, time)):
        raise ValueError("Value was converted to a date by Excel. Use text format or a decimal number.")
    if isinstance(v, bool):
        raise ValueError("Must be a number.")
    try:
        d = Decimal(str(v).strip().replace(",", ""))
    except InvalidOperation:
        raise ValueError("Must be a number.")
    if not d.is_finite():
        raise ValueError("Must be a number.")
    if d != d.to_integral_value() and -d.normalize().as_tuple().exponent > max_places:
        raise ValueError(f"Up to {max_places} decimal places are allowed.")
    return d


def to_fraction(v):
    """BOM 소요원수: 숫자(0.02) 또는 분수 문자열('1/50') (Ⅵ-3-9). 날짜로 바뀐 값은 ValueError."""
    if is_blank(v):
        return None
    if isinstance(v, (datetime, date, time)):
        raise ValueError("Q'ty was converted to a date by Excel. Enter it as text or as a decimal (e.g. 0.02).")
    s = str(v).strip().replace(",", "")
    try:
        if "/" in s:
            a, b = s.split("/", 1)
            f = Fraction(Decimal(a.strip())) / Fraction(Decimal(b.strip()))
        else:
            f = Fraction(to_decimal(s, 10))
    except (ValueError, ZeroDivisionError, InvalidOperation):
        raise ValueError("Q'ty must be a number or a fraction (e.g. 0.02 or 1/50).")
    return f


_HEADER_FONT = Font(bold=True)
_BLUE = PatternFill("solid", fgColor="64A9D6")
_GRAY = PatternFill("solid", fgColor="D9D9D9")


def xlsx_response(filename, sheet, headers, rows, upload_headers=()):
    """Excel Download. upload_headers에 있는 Column은 파란 헤더, 나머지는 회색 헤더 (Ⅳ-3-5)."""
    wb = Workbook()
    ws = wb.active
    ws.title = sheet
    ws.append(headers)
    for cell in ws[1]:
        cell.font = _HEADER_FONT
        cell.fill = _BLUE if cell.value in upload_headers else _GRAY
    for row in rows:
        ws.append(list(row))
    for col in ws.columns:
        ws.column_dimensions[col[0].column_letter].width = max(10, min(40, len(str(col[0].value)) + 4))
    ws.freeze_panes = "A2"
    buf = io.BytesIO()
    wb.save(buf)
    resp = HttpResponse(buf.getvalue(),
                        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    resp["Content-Disposition"] = f'attachment; filename="{filename}"'
    return resp
