r"""DB 백업 (pg_dump custom 형식). 작업 스케줄러로 매일 실행한다.

    .venv\Scripts\python manage.py backup_db                # backups\ 에 저장, 최근 14개 보관
    .venv\Scripts\python manage.py backup_db --keep 30
복원: pg_restore -h localhost -U novatech_app -d <빈 DB> --no-owner <파일>
"""
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection

# ponytail: PATH에 없으면 기본 설치 경로만 찾는다. 다른 위치면 .env에 PG_BIN 추가
DEFAULT_PG_BIN = r"C:\Program Files\PostgreSQL\17\bin"


def _pg_dump():
    found = shutil.which("pg_dump") or shutil.which("pg_dump", path=settings.ENV.get("PG_BIN", DEFAULT_PG_BIN))
    if not found:
        raise CommandError("pg_dump not found. Set PG_BIN in .env (PostgreSQL bin folder).")
    return found


class Command(BaseCommand):
    help = "Back up the database with pg_dump and keep only the latest N files."

    def add_arguments(self, parser):
        parser.add_argument("--dir", default=str(settings.BASE_DIR / "backups"))
        parser.add_argument("--keep", type=int, default=14)

    def handle(self, *args, **opts):
        if opts["keep"] < 1:
            raise CommandError("--keep must be 1 or more.")
        db = connection.settings_dict
        prefix = settings.ENV.get("DB_NAME", "novatech_psi")
        out_dir = Path(opts["dir"])
        out_dir.mkdir(parents=True, exist_ok=True)
        target = out_dir / f"{prefix}_{datetime.now():%Y%m%d_%H%M%S}.dump"
        result = subprocess.run(
            [_pg_dump(), "-Fc", "-h", db["HOST"] or "localhost", "-p", str(db["PORT"] or 5432),
             "-U", db["USER"], "-d", db["NAME"], "-f", str(target)],
            env={**os.environ, "PGPASSWORD": db["PASSWORD"]}, capture_output=True, text=True,
        )
        if result.returncode != 0:
            target.unlink(missing_ok=True)  # 반쯤 쓴 파일을 백업으로 오인하지 않도록
            raise CommandError(f"pg_dump failed: {result.stderr.strip()}")

        files = sorted(out_dir.glob(f"{prefix}_*.dump"))  # 파일명이 시각순이라 이름 정렬 = 시간 정렬
        for old in files[:-opts["keep"]]:
            old.unlink()
        self.stdout.write(f"Backup: {target} ({target.stat().st_size:,} bytes), kept {min(len(files), opts['keep'])}")
