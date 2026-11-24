"""조회 전용 표 화면(Module 3~10) 공통: 검색 영역 + 버튼 + 표 (Ⅳ-3)."""
from django.shortcuts import render

from .context import module_context


def cell(text="", cls="", title=""):
    return (text if text is not None else "", cls, title)


def render_table(request, module, title, columns, rows, *, controls=None, buttons=(), upload=None,
                 banners=(), extra=None):
    """columns: [(라벨, 'up'|'sys')], rows: [{'cls': str, 'cells': [cell(...)]}]."""
    return render(request, "core/table_page.html", module_context(
        module, page_title=title, columns=columns, rows=rows, controls=controls or {}, buttons=buttons,
        upload=upload, banners=banners, query_string=request.GET.urlencode(), **(extra or {}),
    ))
