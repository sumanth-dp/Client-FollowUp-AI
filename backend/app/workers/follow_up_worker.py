import json

from backend.app.core.database import SessionLocal
from backend.app.core.redis import redis_client
from backend.app.models.follow_up import FollowUp
from backend.app.models.client import Client
from backend.app.triggers.engine import execute_trigger
from backend.app.models.follow_up_execution import FollowUpExecution
from backend.app.agents.follow_up_agent import follow_up_agent

QUEUE_NAME = "follow_up_queue"

from datetime import datetime, timedelta, timezone

from backend.app.triggers.engine import execute_trigger


def process_job(job: dict):
    follow_up_id = job["follow_up_id"]

    db = SessionLocal()

    try:
        follow_up = db.get(FollowUp, follow_up_id)

        if follow_up is None:
            print(f"Follow-up {follow_up_id} not found")
            return

        # Prevent processing an already completed follow-up
        if follow_up.status == "completed":
            print(
                f"Follow-up {follow_up.id} is already completed. "
                f"Skipping."
            )
            return

        # Count this execution attempt
        follow_up.attempt_count += 1

        now = datetime.now(timezone.utc)

        execution = FollowUpExecution(
            follow_up_id=follow_up.id,
            attempt_number=follow_up.attempt_count,
            channel=follow_up.type,
            status="processing",
            started_at=now,
            created_at=now,
        )

        db.add(execution)
        db.commit()
        db.refresh(execution)

        print(
            f"Processing follow-up {follow_up.id} "
            f"(attempt {follow_up.attempt_count}/"
            f"{follow_up.max_attempts})"
        )

        # execution_started_at = datetime.now(timezone.utc)

        # execution = FollowUpExecution(
        #     follow_up_id=follow_up.id,
        #     attempt_number=follow_up.attempt_count,
        #     channel=follow_up.type,
        #     status="processing",
        #     started_at=execution_started_at,
        #     created_at=execution_started_at,
        # )

        # db.add(execution)
        # db.flush()

        try:
            result = follow_up_agent.invoke(
                {
                    "follow_up_id": follow_up.id,
                    "client_name": follow_up.client.name,
                    "client_email": follow_up.client.email,
                    "purpose": "Follow up with the client based on the provided notes.",
                    "notes": follow_up.notes,
                    "action": "",
                    "email_subject": "",
                    "email_body": "",
                    "provider_reference": None,
                    "success": False,
                    "error": None,
                    "messages": [],
                }
            )

            print(
                f"[WORKER] Agent result: {result}"
            )

            provider_reference = result.get("provider_reference")
            success = result.get("success", False)
            error = result.get("error")
            # if provider_reference:
            #     execution.provider_reference = provider_reference

            if success and provider_reference:
                execution.provider_reference = provider_reference
                follow_up.status = "completed"
                follow_up.completed_at = datetime.now(timezone.utc)
                follow_up.last_error = None
                follow_up.processing_started_at = None

                execution.status = "completed"
                execution.completed_at = datetime.now(timezone.utc)
                execution.error_message = None

                db.commit()
                print(
                    f"Follow-up {follow_up.id} "
                    f"completed successfully"
                )

                return
            # else:
            #     follow_up.status = "failed"
            #     follow_up.next_retry_at = None
            #     follow_up.processing_started_at = None

            #     db.commit()

            raise Exception("Trigger returned failure")

        except Exception as e:
            follow_up.last_error = str(e)
            print(
                f"[WORKER ERROR] {type(e).__name__}: {e}"
            )
            execution.status = "failed"
            execution.completed_at = datetime.now(timezone.utc)
            execution.error_message = str(e)

            if follow_up.attempt_count < follow_up.max_attempts:
                follow_up.status = "pending"

                retry_delay = 30 * (
                    2 ** (follow_up.attempt_count - 1)
                )

                follow_up.next_retry_at = (
                    datetime.now(timezone.utc)
                    + timedelta(seconds=retry_delay)
                )

                db.commit()

                print(
                    f"Follow-up {follow_up.id} failed. "
                    f"Retry scheduled in {retry_delay} seconds."
                )

            else:
                follow_up.status = "failed"
                follow_up.next_retry_at = None
                follow_up.processing_started_at = None

                db.commit()

                print(
                    f"Follow-up {follow_up.id} permanently failed "
                    f"after {follow_up.attempt_count} attempts."
                )

    except Exception as e:
        db.rollback()
        print(f"Worker database error: {e}")

    finally:
        db.close()
    

def run_worker():
    print("Follow-up worker started")

    
    while True:
        #_, data = redis_client.brpop(QUEUE_NAME)
        result = redis_client.brpop(QUEUE_NAME, timeout=0)

        if result is None:
            continue

        _, data = result

        job = json.loads(data)

        process_job(job)


from datetime import datetime, timezone

from sqlalchemy import or_

from backend.app.models.follow_up import FollowUp


def get_due_follow_ups(db):
    now = datetime.now(timezone.utc)

    return (
        db.query(FollowUp)
        .filter(
            FollowUp.status == "pending",
            or_(
                (
                    FollowUp.scheduled_at.isnot(None)
                    & (FollowUp.scheduled_at <= now)
                    & FollowUp.next_retry_at.is_(None)
                ),
                (
                    FollowUp.next_retry_at.isnot(None)
                    & (FollowUp.next_retry_at <= now)
                ),
            ),
        )
        .order_by(
            FollowUp.priority.desc(),
            FollowUp.scheduled_at.asc(),
        )
        .all()
    )




if __name__ == "__main__":
    run_worker()
