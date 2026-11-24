from django.db import migrations

UNITS = ["EA", "SHEET", "SET", "G", "KG", "MM", "M"]  # Ⅵ-1-4 ④ 확정 허용값


def seed(apps, schema_editor):
    UnitCode = apps.get_model("materials", "UnitCode")
    for i, code in enumerate(UNITS, start=1):
        UnitCode.objects.get_or_create(code=code, defaults={"sort_order": i})


class Migration(migrations.Migration):
    dependencies = [("materials", "0001_initial")]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
