"""10개 업무 Module 메뉴 (Main 화면 그룹 + Module 화면 상단 탭). url_name이 None이면 개발 전(비활성)."""
from django.urls import reverse

MODULES = [
    ("M1", "Master DB", "1. Material Master", "Material Master", "materials:list"),
    ("M2", "Master DB", "2. Assy Master", "Assy Master", "assies:list"),
    ("M3", "Master DB", "3. BOM", "BOM", None),
    ("M4", "Master DB", "4. Safety Stock", "Safety Stock", None),
    ("M5", "Weekly Data", "5. Inventory", "Inventory", None),
    ("M6", "Weekly Data", "6. RTF/Production", "RTF/Production", None),
    ("M7", "PO", "7. Open PO", "Open PO", None),
    ("M8", "PO", "8. Scheduled Receipt", "Scheduled Receipt", None),
    ("M9", "Report", "9. Material Requirement", "Material Requirement", None),
    ("M10", "Report", "10. Material PSI", "Material PSI", None),
]


def _url(name):
    return reverse(name) if name else None


def main_groups():
    groups = {}
    for _, group, label, _, url_name in MODULES:
        groups.setdefault(group, []).append((label, _url(url_name)))
    return list(groups.items())


def tabs(active):
    return [{"key": key, "label": short, "url": _url(url_name), "active": key == active}
            for key, _, _, short, url_name in MODULES]
