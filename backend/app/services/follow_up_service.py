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

def get_due_follow_ups(db: Session) -> list[FollowUp]:
    now = datetime.now()

    
    statement = select(FollowUp).where(
        FollowUp.status == "pending",
        FollowUp.scheduled_at <= now,
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


def claim_follow_up(db, follow_up_id: int) -> bool:
    result = db.execute(
        update(FollowUp)
        .where(
            FollowUp.id == follow_up_id,
            FollowUp.status == "pending",
        )
        # .values(
        #     status="processing",
        # )
        .values(
            status="processing",
            processing_started_at=datetime.now(timezone.utc),
        )
    )

    db.commit()

    return result.rowcount == 1

from datetime import datetime, timedelta, timezone

from sqlalchemy import update

from backend.app.models.follow_up import FollowUp


def recover_stuck_follow_ups(db):
    now = datetime.now(timezone.utc)

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
            f"Recovering stuck follow-up "
            f"{follow_up.id}"
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

from datetime import datetime, timezone

from sqlalchemy import update

from backend.app.models.follow_up import FollowUp


def claim_follow_up_for_queue(
    db,
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
            processing_started_at=datetime.now(timezone.utc),
        )
    )

    db.commit()

    return result.rowcount == 1