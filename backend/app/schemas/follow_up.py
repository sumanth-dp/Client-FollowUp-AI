from datetime import datetime

from pydantic import BaseModel, ConfigDict

from typing import Literal

from backend.app.core.constants import (
    FollowUpType,
    FollowUpStatus,
    FollowUpPriority,
)

# class FollowUpCreate(BaseModel):
#     client_id: int
#     type: Literal[
#     "email",
#     "whatsapp",
#     "call",
#     "reminder",
#     ]
#     scheduled_at: datetime
#     status: Literal[
#         "pending",
#         "processing",
#         "completed",
#         "failed",
#     ] = "pending"

#     priority: Literal[
#         "low",
#         "medium",
#         "high",
#     ] = "medium"
#     notes: str | None = None

class FollowUpCreate(BaseModel):
    client_id: int
    type: FollowUpType
    scheduled_at: datetime
    status: FollowUpStatus = "pending"
    priority: FollowUpPriority = "medium"
    notes: str | None = None


# class FollowUpUpdate(BaseModel):
#     type: Literal[
#         "email",
#         "whatsapp",
#         "call",
#         "reminder",
#     ] | None = None

#     scheduled_at: datetime | None = None

#     status: Literal[
#         "pending",
#         "processing",
#         "completed",
#         "failed",
#     ] | None = None

#     priority: Literal[
#         "low",
#         "medium",
#         "high",
#     ] | None = None

#     notes: str | None = None

class FollowUpUpdate(BaseModel):
    type: FollowUpType | None = None
    scheduled_at: datetime | None = None
    status: FollowUpStatus | None = None
    priority: FollowUpPriority | None = None
    notes: str | None = None


class FollowUpResponse(BaseModel):
    id: int
    client_id: int
    # type: str
    scheduled_at: datetime
    # status: str
    type: FollowUpType
    status: FollowUpStatus
    priority: FollowUpPriority
    # priority: str
    notes: str | None

    attempt_count: int
    max_attempts: int

    next_retry_at: datetime | None
    last_error: str | None
    processing_started_at: datetime | None

    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)



class FollowUpExecutionResponse(BaseModel):
    id: int
    attempt_number: int
    channel: str
    status: str
    provider_reference: str | None
    started_at: datetime | None
    completed_at: datetime | None
    error_message: str | None


from pydantic import Field


class FollowUpFilterParams(BaseModel):
    status: FollowUpStatus | None = None
    client_id: int | None = Field(default=None, gt=0)
    priority: FollowUpPriority | None = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)