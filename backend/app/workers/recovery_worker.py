import time

from backend.app.core.database import SessionLocal
from backend.app.services.follow_up_service import recover_stuck_follow_ups
from backend.app.models.client import Client


def run_recovery_worker():

    print("Recovery worker started")

    while True:

        db = SessionLocal()

        try:

            recovered = recover_stuck_follow_ups(db)

            if recovered:
                print(
                    f"Recovered {recovered} "
                    f"stuck follow-up(s)"
                )

        except Exception as e:

            db.rollback()

            print(
                f"Recovery worker error: {e}"
            )

        finally:

            db.close()

        time.sleep(60)


if __name__ == "__main__":
    run_recovery_worker()