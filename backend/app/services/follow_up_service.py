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


from datetime import datetime

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
    

