"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.client import Client
from backend.app.models.follow_up import FollowUp
from backend.app.schemas.follow_up import (
    FollowUpCreate,
    FollowUpResponse,
    FollowUpUpdate,
)

from backend.app.services.follow_up_service import get_due_follow_ups


router = APIRouter(
    prefix="/follow-ups",
    tags=["Follow-ups"],
)


@router.post(
    "",
    response_model=FollowUpResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_follow_up(
    follow_up_data: FollowUpCreate,
    db: Session = Depends(get_db),
):
    client = db.get(Client, follow_up_data.client_id)

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


@router.get(
    "",
    response_model=list[FollowUpResponse],
)
def get_follow_ups(
    db: Session = Depends(get_db),
):
    result = db.execute(
        select(FollowUp)
    )

    return result.scalars().all()



@router.get("/due")
def get_due_follow_ups_endpoint(db: Session = Depends(get_db)):
    follow_ups = get_due_follow_ups(db)

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

from backend.app.services.follow_up_service import (
    get_due_follow_ups,
    process_follow_up,
)

@router.post("/trigger-due")
def trigger_due_follow_ups(
    db: Session = Depends(get_db),
    ):
    follow_ups = get_due_follow_ups(db)

    
    processed = []

    for follow_up in follow_ups:
        follow_up = process_follow_up(db, follow_up)

        processed.append({
            "id": follow_up.id,
            "client_id": follow_up.client_id,
            "type": follow_up.type,
            "status": follow_up.status,
            "attempt_count": follow_up.attempt_count,
        })

    return {
        "count": len(processed),
        "processed": processed,
    }
    
from backend.app.services.queue_service import enqueue_follow_up

@router.post("/{follow_up_id}/queue")
def queue_follow_up(
    follow_up_id: int,
    db: Session = Depends(get_db),
    ):
    follow_up = db.get(FollowUp, follow_up_id)

    
    if follow_up is None:
        raise HTTPException(
            status_code=404,
            detail="Follow-up not found",
        )

    enqueue_follow_up(follow_up.id)

    return {
        "message": "Follow-up added to queue",
        "follow_up_id": follow_up.id,
    }






@router.get(
    "/{follow_up_id}",
    response_model=FollowUpResponse,
)
def get_follow_up(
    follow_up_id: int,
    db: Session = Depends(get_db),
):
    follow_up = db.get(FollowUp, follow_up_id)

    if follow_up is None:
        raise HTTPException(
            status_code=404,
            detail="Follow-up not found",
        )

    return follow_up


@router.patch(
    "/{follow_up_id}",
    response_model=FollowUpResponse,
)
def update_follow_up(
    follow_up_id: int,
    follow_up_data: FollowUpUpdate,
    db: Session = Depends(get_db),
):
    follow_up = db.get(FollowUp, follow_up_id)

    if follow_up is None:
        raise HTTPException(
            status_code=404,
            detail="Follow-up not found",
        )

    update_data = follow_up_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(follow_up, field, value)

    db.commit()
    db.refresh(follow_up)

    return follow_up


@router.delete(
    "/{follow_up_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_follow_up(
    follow_up_id: int,
    db: Session = Depends(get_db),
):
    follow_up = db.get(FollowUp, follow_up_id)

    if follow_up is None:
        raise HTTPException(
            status_code=404,
            detail="Follow-up not found",
        )

    db.delete(follow_up)
    db.commit()

"""



from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.client import Client
from backend.app.models.follow_up import FollowUp

from backend.app.schemas.follow_up import (
    FollowUpCreate,
    FollowUpResponse,
    FollowUpUpdate,
)

from backend.app.services.follow_up_service import (
    get_due_follow_ups,
    process_follow_up,
)

from backend.app.services.queue_service import enqueue_follow_up

from backend.app.models.follow_up_execution import FollowUpExecution
from backend.app.models.follow_up_execution import FollowUpExecution
from backend.app.schemas.follow_up_execution import FollowUpExecutionResponse

from backend.app.schemas.follow_up import FollowUpExecutionResponse

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
):
    client = db.get(Client, follow_up_data.client_id)

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
    db: Session = Depends(get_db),
):
    result = db.execute(
        select(FollowUp)
    )

    return result.scalars().all()


# ---------------------------------------------------------
# GET DUE FOLLOW-UPS
# ---------------------------------------------------------

@router.get("/due")
def get_due_follow_ups_endpoint(
    db: Session = Depends(get_db),
):
    follow_ups = get_due_follow_ups(db)

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
):
    follow_ups = get_due_follow_ups(db)

    processed = []

    for follow_up in follow_ups:
        follow_up = process_follow_up(
            db,
            follow_up,
        )

        processed.append({
            "id": follow_up.id,
            "client_id": follow_up.client_id,
            "type": follow_up.type,
            "status": follow_up.status,
            "attempt_count": follow_up.attempt_count,
        })

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
):
    follow_up = db.get(
        FollowUp,
        follow_up_id,
    )

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


"""
@router.get(
    "/{follow_up_id}/executions",
    response_model=list[FollowUpExecutionResponse],
)
def get_follow_up_executions(
    follow_up_id: int,
    db: Session = Depends(get_db),
):
    follow_up = db.get(FollowUp, follow_up_id)

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
            FollowUpExecution.attempt_number
        )
    )

    executions = result.scalars().all()

    """

@router.get(
    "/{follow_up_id}/executions",
    response_model=list[FollowUpExecutionResponse],
)
def get_follow_up_executions(
    follow_up_id: int,
    db: Session = Depends(get_db),
):
    follow_up = db.get(FollowUp, follow_up_id)

    if follow_up is None:
        raise HTTPException(
            status_code=404,
            detail="Follow-up not found",
        )

    result = db.execute(
        select(FollowUpExecution)
        .where(FollowUpExecution.follow_up_id == follow_up_id)
        .order_by(FollowUpExecution.id.desc())
    )

    return result.scalars().all()

    # return {
    #     "follow_up_id": follow_up_id,
    #     "count": len(executions),
    #     "executions": [
    #         {
    #             "id": execution.id,
    #             "attempt_number": execution.attempt_number,
    #             "channel": execution.channel,
    #             "status": execution.status,
    #             "provider_reference": execution.provider_reference,
    #             "started_at": execution.started_at,
    #             "completed_at": execution.completed_at,
    #             "error_message": execution.error_message,
    #         }
    #         for execution in executions
    #     ],
    # }
    return [
        {
            "id": execution.id,
            "attempt_number": execution.attempt_number,
            "channel": execution.channel,
            "status": execution.status,
            "provider_reference": execution.provider_reference,
            "started_at": execution.started_at,
            "completed_at": execution.completed_at,
            "error_message": execution.error_message,
        }
        for execution in executions
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
):
    follow_up = db.get(
        FollowUp,
        follow_up_id,
    )

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
):
    follow_up = db.get(
        FollowUp,
        follow_up_id,
    )

    if follow_up is None:
        raise HTTPException(
            status_code=404,
            detail="Follow-up not found",
        )

    update_data = follow_up_data.model_dump(
        exclude_unset=True
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
):
    follow_up = db.get(
        FollowUp,
        follow_up_id,
    )

    if follow_up is None:
        raise HTTPException(
            status_code=404,
            detail="Follow-up not found",
        )

    db.delete(follow_up)
    db.commit()


# @router.get("/{follow_up_id}/executions")
# def get_follow_up_executions(
#     follow_up_id: int,
#     db: Session = Depends(get_db),
# ):
#     follow_up = db.get(FollowUp, follow_up_id)

#     if follow_up is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Follow-up not found",
#         )

#     executions = (
#         db.query(FollowUpExecution)
#         .filter(
#             FollowUpExecution.follow_up_id == follow_up_id
#         )
#         .order_by(
#             FollowUpExecution.attempt_number.asc()
#         )
#         .all()
#     )

#     return {
#         "follow_up_id": follow_up_id,
#         "count": len(executions),
#         "executions": [
#             {
#                 "id": execution.id,
#                 "attempt_number": execution.attempt_number,
#                 "channel": execution.channel,
#                 "status": execution.status,
#                 "provider_reference": execution.provider_reference,
#                 "started_at": execution.started_at,
#                 "completed_at": execution.completed_at,
#                 "error_message": execution.error_message,
#             }
#             for execution in executions
#         ],
#     }