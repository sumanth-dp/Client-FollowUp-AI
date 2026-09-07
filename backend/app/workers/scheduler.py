# import time

# from backend.app.core.database import SessionLocal
# from backend.app.services.follow_up_service import get_due_follow_ups
# from backend.app.services.queue_service import enqueue_follow_up


# def run_scheduler():

#     print("Follow-up scheduler started")

#     while True:

#         db = SessionLocal()

#         try:

#             follow_ups = get_due_follow_ups(db)

#             for follow_up in follow_ups:

#                 enqueue_follow_up(follow_up.id)

#                 print(
#                     f"Queued follow-up {follow_up.id}"
#                 )

#         except Exception as e:

#             db.rollback()

#             print(
#                 f"Scheduler error: {e}"
#             )

#         finally:

#             db.close()

#         time.sleep(10)


# if __name__ == "__main__":
#     run_scheduler()








# import time

# from backend.app.core.database import SessionLocal
# from backend.app.services.follow_up_service import (
#     get_due_follow_ups,
#     claim_follow_up_for_queue,
# )
# from backend.app.services.queue_service import enqueue_follow_up


# def run_scheduler():

#     print("Follow-up scheduler started")

#     while True:

#         db = SessionLocal()

#         try:

#             follow_ups = get_due_follow_ups(db)

#             print(
#                 f"Found {len(follow_ups)} due follow-ups"
#             )

#             for follow_up in follow_ups:

#                 claimed = claim_follow_up_for_queue(
#                     db,
#                     follow_up.id,
#                 )

#                 if claimed:

#                     enqueue_follow_up(follow_up.id)

#                     print(
#                         f"Queued follow-up {follow_up.id}"
#                     )

#         except Exception as e:

#             db.rollback()

#             print(
#                 f"Scheduler error: {e}"
#             )

#         finally:

#             db.close()

#         time.sleep(10)


# if __name__ == "__main__":
#     run_scheduler()



import time

from backend.app.core.database import SessionLocal

from backend.app.services.follow_up_service import (
    get_due_follow_ups,
    claim_follow_up_for_queue,
    recover_stuck_follow_ups,
)
from backend.app.services.queue_service import enqueue_follow_up


def run_scheduler():
    print(">>> NEW SCHEDULER CODE LOADED <<<")
    print("Follow-up scheduler started")

    while True:

        db = SessionLocal()

        try:

            # Recover jobs stuck for more than 10 minutes
            recovered = recover_stuck_follow_ups(db)

            if recovered:
                print(
                    f"Recovered {recovered} stuck follow-up(s)"
                )

            # Find due follow-ups
            follow_ups = get_due_follow_ups(db)

            for follow_up in follow_ups:

                claimed = claim_follow_up_for_queue(
                    db,
                    follow_up.id,
                )

                if claimed:

                    enqueue_follow_up(follow_up.id)

                    print(
                        f"Queued follow-up {follow_up.id}"
                    )

        except Exception as e:

            db.rollback()

            print(
                f"Scheduler error: {e}"
            )

        finally:

            db.close()

        time.sleep(10)


if __name__ == "__main__":
    run_scheduler()