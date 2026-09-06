import time

from backend.app.core.database import SessionLocal
from backend.app.services.follow_up_service import get_due_follow_ups
from backend.app.services.queue_service import enqueue_follow_up

from backend.app.services.follow_up_service import (
    get_due_follow_ups,
    claim_follow_up,
)

def run_scheduler():
    print("Follow-up scheduler started")

    while True:
        db = SessionLocal()

        try:
            follow_ups = get_due_follow_ups(db)

            # for follow_up in follow_ups:
            #     print(
            #         f"Found due follow-up: {follow_up.id}"
            #     )

            #     enqueue_follow_up(follow_up.id)

            #     follow_up.status = "processing"
            # for follow_up in follow_ups:
            #     print(
            #         f"Found due follow-up: {follow_up.id}"
            #     )

            #     enqueue_follow_up(follow_up.id)

            #     follow_up.status = "processing"

            #     db.commit()
            for follow_up in follow_ups:

                claimed = claim_follow_up(
                    db,
                    follow_up.id,
                )

                if not claimed:
                    print(
                        f"Follow-up {follow_up.id} "
                        f"was already claimed"
                    )

                    continue

                print(
                    f"Claimed follow-up: {follow_up.id}"
                )

                enqueue_follow_up(
                    follow_up.id
                )

        except Exception as e:
            db.rollback()
            print(f"Scheduler error: {e}")

        finally:
            db.close()

        time.sleep(10)


if __name__ == "__main__":
    run_scheduler()