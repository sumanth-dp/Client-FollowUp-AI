from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FollowUpCreate(BaseModel):
    client_id: int
    type: str
    scheduled_at: datetime
    status: str = "pending"
    priority: str = "medium"
    notes: str | None = None


class FollowUpUpdate(BaseModel):
    type: str | None = None
    scheduled_at: datetime | None = None
    status: str | None = None
    priority: str | None = None
    notes: str | None = None


class FollowUpResponse(BaseModel):
    id: int
    client_id: int
    type: str
    scheduled_at: datetime
    status: str
    priority: str
    notes: str | None
    attempt_count: int
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