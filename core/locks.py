from contextlib import contextmanager

from django.db import connection, transaction

MSG_BUSY = ("Another user is uploading. Try again after it finishes. "
            "(다른 사용자가 Upload 중입니다. 완료 후 다시 시도하세요.)")


class UploadBusy(Exception):
    pass


@contextmanager
def upload_lock(key):
    """같은 Module(·주차) Upload가 처리 중이면 즉시 UploadBusy (H-5: 대기하지 않고 거절).

    PostgreSQL advisory lock: Transaction이 끝나면 자동으로 풀린다.
    """
    with transaction.atomic():
        with connection.cursor() as cur:
            cur.execute("SELECT pg_try_advisory_xact_lock(hashtext(%s))", [f"upload:{key}"])
            if not cur.fetchone()[0]:
                raise UploadBusy(MSG_BUSY)
        yield
