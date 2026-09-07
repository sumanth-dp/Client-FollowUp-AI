from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FollowUpExecutionResponse(BaseModel):
    id: int
    follow_up_id: int
    attempt_number: int
    status: str
    provider_reference: str | None
    error: str | None
    started_at: datetime
    completed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)