"""PostgreSQL에 이 프로젝트 전용 계정·DB를 만든다 (최초 1회).

사용법 (프로젝트 폴더에서):
    .venv\\Scripts\\python tools\\setup_db.py

- PostgreSQL 설치 때 정한 postgres 관리자 비밀번호를 물어본다. (화면에 표시되지 않고 저장하지도 않음)
- 전용 계정 이름·비밀번호는 .env의 DB_USER / DB_PASSWORD를 사용한다.
- 전용 계정에는 테스트용 임시 DB를 만들 수 있도록 CREATEDB 권한만 준다.
"""
import getpass
import sys
from pathlib import Path

import psycopg
from psycopg import sql

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))
from config.settings import ENV  # noqa: E402

name, user, pw = ENV["DB_NAME"], ENV["DB_USER"], ENV["DB_PASSWORD"]
host, port = ENV.get("DB_HOST", "localhost"), ENV.get("DB_PORT", "5432")

admin_pw = getpass.getpass("postgres 관리자 비밀번호: ")
with psycopg.connect(host=host, port=port, user="postgres", password=admin_pw, dbname="postgres", autocommit=True) as conn:
    if conn.execute("SELECT 1 FROM pg_roles WHERE rolname=%s", (user,)).fetchone():
        print(f"계정 {user} 이미 있음 → 비밀번호만 .env 값으로 맞춤")
        conn.execute(sql.SQL("ALTER ROLE {} WITH LOGIN CREATEDB PASSWORD {}").format(sql.Identifier(user), sql.Literal(pw)))
    else:
        conn.execute(sql.SQL("CREATE ROLE {} WITH LOGIN CREATEDB PASSWORD {}").format(sql.Identifier(user), sql.Literal(pw)))
        print(f"계정 {user} 생성")
    if conn.execute("SELECT 1 FROM pg_database WHERE datname=%s", (name,)).fetchone():
        print(f"DB {name} 이미 있음")
    else:
        conn.execute(sql.SQL("CREATE DATABASE {} OWNER {} ENCODING 'UTF8'").format(sql.Identifier(name), sql.Identifier(user)))
        print(f"DB {name} 생성")
print("완료")
