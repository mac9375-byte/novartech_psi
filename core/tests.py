"""Excel 읽기 엔진 테스트 (Ⅳ-5-1)."""
import io
from datetime import datetime

from django.test import SimpleTestCase, TestCase
from openpyxl import Workbook

from .excel import ERROR, INFO, read_sheet, to_code, to_int, to_text


def xlsx(rows, sheet="S", merge=None, extra_sheets=()):
    wb = Workbook()
    ws = wb.active
    ws.title = sheet
    for r in rows:
        ws.append(r)
    if merge:
        ws.merge_cells(merge)
    for name in extra_sheets:
        wb.create_sheet(name).append(["x"])
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf


class ReadSheetTests(SimpleTestCase):
    def test_reads_only_named_sheet_and_maps_headers_in_any_order(self):
        f = xlsx([[" B ", "A", "Extra"], [2, 1, "x"], [None, None, None], [4, 3, None]], extra_sheets=["Other"])
        rows, issues = read_sheet(f, "S", required=["A"], optional=["B"])
        self.assertEqual([(r["_row"], r["A"], r["B"]) for r in rows], [(2, 1, 2), (4, 3, 4)])  # 빈 행 무시
        self.assertEqual([(i["level"], i["field"]) for i in issues], [(INFO, "Extra")])     # 정의 안 된 열 안내

    def test_missing_sheet_is_error(self):
        rows, issues = read_sheet(xlsx([["A"]], sheet="Wrong"), "S", ["A"])
        self.assertEqual((rows, issues[0]["level"], issues[0]["field"]), ([], ERROR, "Sheet"))

    def test_missing_required_column_is_error(self):
        rows, issues = read_sheet(xlsx([["B"], [1]]), "S", ["A"], ["B"])
        self.assertEqual(rows, [])
        self.assertIn("Required column is missing.", [i["reason"] for i in issues])

    def test_header_must_match_exactly_after_trim(self):
        rows, issues = read_sheet(xlsx([["material code"], ["x"]]), "S", ["Material Code"])
        self.assertTrue(any(i["level"] == ERROR for i in issues))

    def test_merged_cells_is_error(self):
        rows, issues = read_sheet(xlsx([["A", "B"], [1, 2]], merge="A2:B2"), "S", ["A"], ["B"])
        self.assertEqual(issues[0]["field"], "Merged cells")

    def test_not_an_excel_file(self):
        rows, issues = read_sheet(io.BytesIO(b"hello"), "S", ["A"])
        self.assertEqual(issues[0]["field"], "File")


class ValueTests(SimpleTestCase):
    def test_to_code(self):
        self.assertEqual(to_code(" smaz13001 "), "SMAZ13001")
        self.assertEqual(to_code(4605000219), "4605000219")
        self.assertEqual(to_code(4605000219.0), "4605000219")
        self.assertEqual(to_code("304060006 (AVBS)-1"), "304060006 (AVBS)-1")
        self.assertIsNone(to_code("-"))
        for bad in ["3.04E+11", 3.04e20, datetime(2026, 1, 1)]:
            with self.assertRaises(ValueError):
                to_code(bad)

    def test_to_int(self):
        self.assertEqual([to_int(5), to_int(5.0), to_int("5"), to_int(" 7 ")], [5, 5, 5, 7])
        self.assertIsNone(to_int(None))
        for bad in [1.5, "1.5", "abc", datetime(2026, 1, 1)]:
            with self.assertRaises(ValueError):
                to_int(bad)

    def test_to_text(self):
        self.assertEqual([to_text(" a "), to_text("-"), to_text(""), to_text(12.0)], ["a", None, None, "12"])


class BackupDbTests(TestCase):
    def test_writes_pg_dump_file_and_keeps_only_latest(self):
        import tempfile
        from pathlib import Path

        from django.core.management import call_command

        with tempfile.TemporaryDirectory() as d:
            for old in ("novatech_psi_20000101_000000.dump", "novatech_psi_20000102_000000.dump"):
                Path(d, old).write_bytes(b"old")
            call_command("backup_db", dir=d, keep=2, stdout=io.StringIO())
            files = sorted(p.name for p in Path(d).glob("*.dump"))
            self.assertEqual(len(files), 2)
            self.assertEqual(files[0], "novatech_psi_20000102_000000.dump")  # 가장 오래된 것부터 삭제
            self.assertEqual(Path(d, files[1]).read_bytes()[:5], b"PGDMP")  # pg_dump custom 형식
