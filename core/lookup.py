"""Master Data 조회 (계층 2: 화면 조회 시점의 최신 Master 값, Ⅳ-7-0). 없으면 'No DB'."""
NO_DB = "No DB"


def materials(codes=None):
    from materials.models import Material
    qs = Material.objects.all()
    if codes is not None:
        qs = qs.filter(material_code__in=list(codes))
    return {m.material_code: m for m in qs}


def assies(codes=None):
    from assies.models import Assy
    qs = Assy.objects.all()
    if codes is not None:
        qs = qs.filter(customer_code__in=list(codes))
    return {a.customer_code: a for a in qs}


def status(obj):
    return obj.get_status_display() if obj else NO_DB


def status_cls(text):
    """Status 글자색 (Ⅳ-3-6): Inactive 파랑, No DB 빨강."""
    return {"Inactive": "st-inactive", NO_DB: "st-nodb"}.get(text, "")
