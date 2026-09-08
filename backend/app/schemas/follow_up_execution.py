from datetime import datetime

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from backend.app.core.constants import FollowUpExecutionStatus


class FollowUpExecutionResponse(BaseModel):
    id: int
    follow_up_id: int
    attempt_number: int
    status: FollowUpExecutionStatus
    provider_reference: str | None
    error: str | None = Field(
        validation_alias=AliasChoices("error", "error_message")
    )
    started_at: datetime
    completed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)

    subject: str | None
    body: str | None