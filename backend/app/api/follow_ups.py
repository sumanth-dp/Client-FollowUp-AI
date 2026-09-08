from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.security import get_current_user

from backend.app.models.client import Client
from backend.app.models.follow_up import FollowUp
from backend.app.models.follow_up_execution import FollowUpExecution
from backend.app.models.user import User

from backend.app.schemas.follow_up import (
    FollowUpCreate,
    FollowUpResponse,
    FollowUpUpdate,
    FollowUpFilterParams,
)
from sqlalchemy import Integer, func, select
from backend.app.schemas.follow_up_execution import (
    FollowUpExecutionResponse,
)

from backend.app.schemas.dashboard import FollowUpStatsResponse
from backend.app.schemas.client_stats import ClientFollowUpStatsResponse

from backend.app.services.follow_up_service import (
    list_follow_ups,
    get_due_follow_ups,
    process_follow_up,
    get_follow_up_stats,
    get_client_follow_up_stats,
)

from backend.app.services.queue_service import enqueue_follow_up


router = APIRouter(
    prefix="/follow-ups",
    tags=["Follow-ups"],
)


# ---------------------------------------------------------
# CREATE FOLLOW-UP
# ---------------------------------------------------------

@router.post(
    "",
    response_model=FollowUpResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_follow_up(
    follow_up_data: FollowUpCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Make sure the client belongs to the logged-in user
    client = db.execute(
        select(Client).where(
            Client.id == follow_up_data.client_id,
            Client.user_id == current_user.id,
        )
    ).scalar_one_or_none()

    if client is None:
        raise HTTPException(
            status_code=404,
            detail="Client not found",
        )

    follow_up = FollowUp(
        **follow_up_data.model_dump()
    )

    db.add(follow_up)
    db.commit()
    db.refresh(follow_up)

    return follow_up


# ---------------------------------------------------------
# GET ALL FOLLOW-UPS
# ---------------------------------------------------------

@router.get(
    "",
    response_model=list[FollowUpResponse],
)
def get_follow_ups(
    filters: Annotated[FollowUpFilterParams, Query()],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = (
        select(FollowUp)
        .join(Client, FollowUp.client_id == Client.id)
        .where(Client.user_id == current_user.id)
    )

    if filters.status is not None:
        query = query.where(FollowUp.status == filters.status)

    if filters.priority is not None:
        query = query.where(FollowUp.priority == filters.priority)

    if filters.client_id is not None:
        query = query.where(FollowUp.client_id == filters.client_id)

    result = db.execute(query)

    return result.scalars().all()

# ---------------------------------------------------------
# GET DUE FOLLOW-UPS
# ---------------------------------------------------------

@router.get("/due")
def get_due_follow_ups_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    follow_ups = (
        db.execute(
            select(FollowUp)
            .join(Client, FollowUp.client_id == Client.id)
            .where(
                Client.user_id == current_user.id,
                FollowUp.status == "pending",
            )
        )
        .scalars()
        .all()
    )

    return {
        "count": len(follow_ups),
        "follow_ups": [
            {
                "id": follow_up.id,
                "client_id": follow_up.client_id,
                "type": follow_up.type,
                "scheduled_at": follow_up.scheduled_at,
                "status": follow_up.status,
            }
            for follow_up in follow_ups
        ],
    }


# ---------------------------------------------------------
# TRIGGER DUE FOLLOW-UPS
# ---------------------------------------------------------

@router.post("/trigger-due")
def trigger_due_follow_ups(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    follow_ups = (
        db.execute(
            select(FollowUp)
            .join(Client, FollowUp.client_id == Client.id)
            .where(
                Client.user_id == current_user.id,
                FollowUp.status == "pending",
            )
        )
        .scalars()
        .all()
    )

    processed = []

    for follow_up in follow_ups:
        follow_up = process_follow_up(
            db,
            follow_up,
        )

        processed.append(
            {
                "id": follow_up.id,
                "client_id": follow_up.client_id,
                "type": follow_up.type,
                "status": follow_up.status,
                "attempt_count": follow_up.attempt_count,
            }
        )

    return {
        "count": len(processed),
        "processed": processed,
    }


# ---------------------------------------------------------
# QUEUE FOLLOW-UP
# ---------------------------------------------------------

@router.post("/{follow_up_id}/queue")
def queue_follow_up(
    follow_up_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    follow_up = db.execute(
        select(FollowUp)
        .join(Client, FollowUp.client_id == Client.id)
        .where(
            FollowUp.id == follow_up_id,
            Client.user_id == current_user.id,
        )
    ).scalar_one_or_none()

    if follow_up is None:
        raise HTTPException(
            status_code=404,
            detail="Follow-up not found",
        )

    enqueue_follow_up(
        follow_up.id
    )

    return {
        "message": "Follow-up added to queue",
        "follow_up_id": follow_up.id,
    }


# ---------------------------------------------------------
# GET FOLLOW-UP EXECUTIONS
# ---------------------------------------------------------

@router.get(
    "/{follow_up_id}/executions",
    response_model=list[FollowUpExecutionResponse],
)
def get_follow_up_executions(
    follow_up_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    follow_up = db.execute(
        select(FollowUp)
        .join(Client, FollowUp.client_id == Client.id)
        .where(
            FollowUp.id == follow_up_id,
            Client.user_id == current_user.id,
        )
    ).scalar_one_or_none()

    if follow_up is None:
        raise HTTPException(
            status_code=404,
            detail="Follow-up not found",
        )

    result = db.execute(
        select(FollowUpExecution)
        .where(
            FollowUpExecution.follow_up_id == follow_up_id
        )
        .order_by(
            FollowUpExecution.id.desc()
        )
    )

    return result.scalars().all()


# ---------------------------------------------------------
# FOLLOW-UP STATS
# ---------------------------------------------------------

@router.get(
    "/stats",
    response_model=FollowUpStatsResponse,
)
def get_follow_up_stats_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    total = db.scalar(
        select(func.count())
        .select_from(FollowUp)
        .join(Client, FollowUp.client_id == Client.id)
        .where(Client.user_id == current_user.id)
    )

    pending = db.scalar(
        select(func.count())
        .select_from(FollowUp)
        .join(Client, FollowUp.client_id == Client.id)
        .where(
            Client.user_id == current_user.id,
            FollowUp.status == "pending",
            FollowUp.next_retry_at.is_(None),
        )
    )

    retrying = db.scalar(
        select(func.count())
        .select_from(FollowUp)
        .join(Client, FollowUp.client_id == Client.id)
        .where(
            Client.user_id == current_user.id,
            FollowUp.status == "pending",
            FollowUp.next_retry_at.is_not(None),
        )
    )

    processing = db.scalar(
        select(func.count())
        .select_from(FollowUp)
        .join(Client, FollowUp.client_id == Client.id)
        .where(
            Client.user_id == current_user.id,
            FollowUp.status == "processing",
        )
    )

    completed = db.scalar(
        select(func.count())
        .select_from(FollowUp)
        .join(Client, FollowUp.client_id == Client.id)
        .where(
            Client.user_id == current_user.id,
            FollowUp.status == "completed",
        )
    )

    failed = db.scalar(
        select(func.count())
        .select_from(FollowUp)
        .join(Client, FollowUp.client_id == Client.id)
        .where(
            Client.user_id == current_user.id,
            FollowUp.status == "failed",
        )
    )

    return {
        "total": total or 0,
        "pending": pending or 0,
        "processing": processing or 0,
        "completed": completed or 0,
        "failed": failed or 0,
        "retrying": retrying or 0,
    }


# ---------------------------------------------------------
# CLIENT FOLLOW-UP STATS
# ---------------------------------------------------------
@router.get(
    "/client-stats",
    response_model=list[ClientFollowUpStatsResponse],
)
def get_client_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = db.execute(
        select(
            Client.id.label("client_id"),
            Client.name.label("client_name"),
            func.count(FollowUp.id).label("total_follow_ups"),
            func.sum(
                (FollowUp.status == "pending").cast(Integer)
            ).label("pending"),
            func.sum(
                (FollowUp.status == "processing").cast(Integer)
            ).label("processing"),
            func.sum(
                (FollowUp.status == "completed").cast(Integer)
            ).label("completed"),
            func.sum(
                (FollowUp.status == "failed").cast(Integer)
            ).label("failed"),
            func.sum(
                (
                    (FollowUp.status == "pending")
                    & FollowUp.next_retry_at.is_not(None)
                ).cast(Integer)
            ).label("retrying"),
        )
        .outerjoin(
            FollowUp,
            FollowUp.client_id == Client.id,
        )
        .where(
            Client.user_id == current_user.id
        )
        .group_by(
            Client.id,
            Client.name,
        )
    )

    rows = result.all()

    return [
        {
            "client_id": row.client_id,
            "client_name": row.client_name,
            "total": row.total_follow_ups,
            "pending": row.pending or 0,
            "processing": row.processing or 0,
            "completed": row.completed or 0,
            "failed": row.failed or 0,
            "retrying": row.retrying or 0,
        }
        for row in rows
    ]


# ---------------------------------------------------------
# GET SINGLE FOLLOW-UP
# ---------------------------------------------------------

@router.get(
    "/{follow_up_id}",
    response_model=FollowUpResponse,
)
def get_follow_up(
    follow_up_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    follow_up = db.execute(
        select(FollowUp)
        .join(Client, FollowUp.client_id == Client.id)
        .where(
            FollowUp.id == follow_up_id,
            Client.user_id == current_user.id,
        )
    ).scalar_one_or_none()

    if follow_up is None:
        raise HTTPException(
            status_code=404,
            detail="Follow-up not found",
        )

    return follow_up


# ---------------------------------------------------------
# UPDATE FOLLOW-UP
# ---------------------------------------------------------

@router.patch(
    "/{follow_up_id}",
    response_model=FollowUpResponse,
)
def update_follow_up(
    follow_up_id: int,
    follow_up_data: FollowUpUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    follow_up = db.execute(
        select(FollowUp)
        .join(Client, FollowUp.client_id == Client.id)
        .where(
            FollowUp.id == follow_up_id,
            Client.user_id == current_user.id,
        )
    ).scalar_one_or_none()

    if follow_up is None:
        raise HTTPException(
            status_code=404,
            detail="Follow-up not found",
        )

    update_data = follow_up_data.model_dump(
        exclude_unset=True
    )

    # If changing client_id, make sure the new client
    # also belongs to the current user.
    if "client_id" in update_data:
        new_client = db.execute(
            select(Client).where(
                Client.id == update_data["client_id"],
                Client.user_id == current_user.id,
            )
        ).scalar_one_or_none()

        if new_client is None:
            raise HTTPException(
                status_code=404,
                detail="Client not found",
            )

    for field, value in update_data.items():
        setattr(
            follow_up,
            field,
            value,
        )

    db.commit()
    db.refresh(follow_up)

    return follow_up


# ---------------------------------------------------------
# DELETE FOLLOW-UP
# ---------------------------------------------------------

@router.delete(
    "/{follow_up_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_follow_up(
    follow_up_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    follow_up = db.execute(
        select(FollowUp)
        .join(Client, FollowUp.client_id == Client.id)
        .where(
            FollowUp.id == follow_up_id,
            Client.user_id == current_user.id,
        )
    ).scalar_one_or_none()

    if follow_up is None:
        raise HTTPException(
            status_code=404,
            detail="Follow-up not found",
        )

    db.delete(follow_up)
    db.commit()