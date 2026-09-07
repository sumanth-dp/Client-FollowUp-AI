# from datetime import datetime

# from sqlalchemy import select
# from sqlalchemy.orm import Session

# from backend.app.models.follow_up import FollowUp

# def get_due_follow_ups(db: Session) -> list[FollowUp]:
#     """
#     Return all pending follow-ups whose scheduled time
#     has arrived.
#     """

    
#     #now = datetime.utcnow()
#     now = datetime.now()

#     statement = select(FollowUp).where(
#         FollowUp.status == "pending",
#         FollowUp.scheduled_at <= now,
#     )

#     result = db.scalars(statement)

#     return list(result)


from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.follow_up import FollowUp

# def get_due_follow_ups(db: Session) -> list[FollowUp]:
#     now = datetime.now()

    
#     statement = select(FollowUp).where(
#         FollowUp.status == "pending",
#         FollowUp.scheduled_at <= now,
#     )

#     result = db.scalars(statement)

#     return list(result)

# def get_due_follow_ups(db: Session) -> list[FollowUp]:

#     now = datetime.now(timezone.utc)

#     statement = select(FollowUp).where(
#         FollowUp.status == "pending",
#         FollowUp.scheduled_at <= now,
#         (
#             FollowUp.next_retry_at.is_(None)
#             | (FollowUp.next_retry_at <= now)
#         ),
#     )

#     result = db.scalars(statement)

#     return list(result)
    
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.follow_up import FollowUp


# def get_due_follow_ups(db: Session) -> list[FollowUp]:

#     now = datetime.now(timezone.utc)

#     statement = select(FollowUp).where(
#         FollowUp.status == "pending",
#         FollowUp.scheduled_at <= now,
#         (
#             FollowUp.next_retry_at.is_(None)
#             | (FollowUp.next_retry_at <= now)
#         ),
#     )

#     result = db.scalars(statement)

#     return list(result)

from datetime import datetime

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from backend.app.models.follow_up import FollowUp


# def get_due_follow_ups(db: Session) -> list[FollowUp]:
#     now = datetime.now()

#     statement = select(FollowUp).where(
#         FollowUp.status == "pending",
#         FollowUp.scheduled_at <= now,
#         (
#             FollowUp.next_retry_at.is_(None)
#             | (FollowUp.next_retry_at <= now)
#         ),
#     )

#     result = db.scalars(statement)

#     return list(result)

def get_due_follow_ups(db: Session) -> list[FollowUp]:
    now = datetime.now()

    statement = select(FollowUp).where(
        FollowUp.status == "pending",
        FollowUp.scheduled_at <= now,
        or_(
            FollowUp.next_retry_at.is_(None),
            FollowUp.next_retry_at <= now,
        ),
    )

    result = db.scalars(statement)

    return list(result)

def process_follow_up(
    db: Session,
    follow_up: FollowUp,
    ) -> FollowUp:
    follow_up.status = "processing"
    follow_up.attempt_count += 1

    
    db.commit()
    db.refresh(follow_up)

    return follow_up


from sqlalchemy import update

from backend.app.models.follow_up import FollowUp


# def claim_follow_up(db, follow_up_id: int) -> bool:
#     result = db.execute(
#         update(FollowUp)
#         .where(
#             FollowUp.id == follow_up_id,
#             FollowUp.status == "pending",
#         )
#         # .values(
#         #     status="processing",
#         # )
#         .values(
#             status="processing",
#             processing_started_at=datetime.now(timezone.utc),
#         )
#     )

#     db.commit()

#     return result.rowcount == 1

from datetime import datetime, timedelta, timezone

from sqlalchemy import update

from backend.app.models.follow_up import FollowUp

"""
def recover_stuck_follow_ups(db):

    now = datetime.now()

    timeout = now - timedelta(minutes=10)

    stuck_follow_ups = (
        db.query(FollowUp)
        .filter(
            FollowUp.status == "processing",
            FollowUp.processing_started_at.isnot(None),
            FollowUp.processing_started_at < timeout,
        )
        .all()
    )

    recovered = 0

    for follow_up in stuck_follow_ups:

        print(
            f"Recovering stuck follow-up {follow_up.id}"
        )

        if follow_up.attempt_count < follow_up.max_attempts:

            follow_up.status = "pending"
            follow_up.next_retry_at = now
            follow_up.processing_started_at = None

            recovered += 1

        else:

            follow_up.status = "failed"
            follow_up.processing_started_at = None
            follow_up.next_retry_at = None

    db.commit()

    return recovered
    """
"""
def recover_stuck_follow_ups(db):

    now = datetime.now()

    timeout = now - timedelta(minutes=10)

    print(f"[RECOVERY] now = {now}")
    print(f"[RECOVERY] timeout = {timeout}")

    stuck_follow_ups = (
        db.query(FollowUp)
        .filter(
            FollowUp.status == "processing",
            FollowUp.processing_started_at.isnot(None),
            FollowUp.processing_started_at < timeout,
        )
        .all()
    )

    print(
        f"[RECOVERY] Found {len(stuck_follow_ups)} stuck follow-ups"
    )

    recovered = 0

    for follow_up in stuck_follow_ups:

        print(
            f"[RECOVERY] Recovering follow-up {follow_up.id}"
        )

        if follow_up.attempt_count < follow_up.max_attempts:

            follow_up.status = "pending"
            follow_up.next_retry_at = now
            follow_up.processing_started_at = None

            recovered += 1

        else:

            follow_up.status = "failed"
            follow_up.processing_started_at = None
            follow_up.next_retry_at = None

    db.commit()

    return recovered
"""
'''
def recover_stuck_follow_ups(db):

    now = datetime.now()
    timeout = now - timedelta(minutes=10)

    print(f"[RECOVERY] Python now     = {now}")
    print(f"[RECOVERY] Python timeout = {timeout}")

    processing_follow_ups = (
        db.query(FollowUp)
        .filter(
            FollowUp.status == "processing",
        )
        .all()
    )

    print(
        f"[RECOVERY] Processing rows = {len(processing_follow_ups)}"
    )

    for follow_up in processing_follow_ups:

        print(
            f"[RECOVERY] ID={follow_up.id}"
        )

        print(
            f"[RECOVERY] status="
            f"{follow_up.status}"
        )

        print(
            f"[RECOVERY] processing_started_at="
            f"{follow_up.processing_started_at}"
        )

        if follow_up.processing_started_at:

            print(
                f"[RECOVERY] processing_started_at type="
                f"{type(follow_up.processing_started_at)}"
            )

            print(
                f"[RECOVERY] is_stuck="
                f"{follow_up.processing_started_at < timeout}"
            )

    return 0
'''

"""
def recover_stuck_follow_ups(db):
    now = datetime.now()
    timeout = now - timedelta(minutes=10)  # TEST ONLY

    print(f"[RECOVERY] Python now     = {now}")
    print(f"[RECOVERY] Python timeout = {timeout}")

    processing_follow_ups = (
        db.query(FollowUp)
        .filter(
            FollowUp.status == "processing",
            FollowUp.processing_started_at.isnot(None),
        )
        .all()
    )

    print(f"[RECOVERY] Processing rows = {len(processing_follow_ups)}")

    recovered = 0

    for follow_up in processing_follow_ups:

        print(f"[RECOVERY] ID={follow_up.id}")
        print(f"[RECOVERY] status={follow_up.status}")
        print(
            f"[RECOVERY] processing_started_at="
            f"{follow_up.processing_started_at}"
        )

        if follow_up.processing_started_at < timeout:

            print(
                f"[RECOVERY] Recovering stuck follow-up "
                f"{follow_up.id}"
            )

            if follow_up.attempt_count < follow_up.max_attempts:

                follow_up.status = "pending"
                follow_up.next_retry_at = now
                follow_up.processing_started_at = None

                recovered += 1

                print(
                    f"[RECOVERY] Follow-up {follow_up.id} "
                    f"reset to pending"
                )

            else:

                follow_up.status = "failed"
                follow_up.next_retry_at = None
                follow_up.processing_started_at = None

                print(
                    f"[RECOVERY] Follow-up {follow_up.id} "
                    f"marked as permanently failed"
                )

    db.commit()

    print(
        f"[RECOVERY] Total recovered = {recovered}"
    )

    return recovered
"""

def recover_stuck_follow_ups(db: Session) -> int:
    now = datetime.now()
    timeout = now - timedelta(minutes=10)

    processing_follow_ups = (
        db.query(FollowUp)
        .filter(
            FollowUp.status == "processing",
            FollowUp.processing_started_at.is_not(None),
            FollowUp.processing_started_at < timeout,
        )
        .all()
    )

    recovered = 0

    for follow_up in processing_follow_ups:

        if follow_up.attempt_count < follow_up.max_attempts:

            follow_up.status = "pending"

            follow_up.next_retry_at = now + timedelta(
                seconds=30 * (2 ** (follow_up.attempt_count - 1))
            )

            follow_up.processing_started_at = None

        else:

            follow_up.status = "failed"

            follow_up.processing_started_at = None

        recovered += 1

    if recovered:
        db.commit()

    return recovered

# from datetime import datetime, timezone

# from sqlalchemy import update

# from backend.app.models.follow_up import FollowUp


# def claim_follow_up_for_queue(
#     db,
#     follow_up_id: int,
# ) -> bool:

#     result = db.execute(
#         update(FollowUp)
#         .where(
#             FollowUp.id == follow_up_id,
#             FollowUp.status == "pending",
#         )
#         .values(
#             status="processing",
#             processing_started_at=datetime.now(timezone.utc),

#         )
#     )

#     db.commit()

#     return result.rowcount == 1


from datetime import datetime

from sqlalchemy import update
from sqlalchemy.orm import Session

from backend.app.models.follow_up import FollowUp


def claim_follow_up_for_queue(
    db: Session,
    follow_up_id: int,
) -> bool:

    result = db.execute(
        update(FollowUp)
        .where(
            FollowUp.id == follow_up_id,
            FollowUp.status == "pending",
        )
        .values(
            status="processing",
            processing_started_at=datetime.now(),
        )
    )

    db.commit()

    return result.rowcount == 1