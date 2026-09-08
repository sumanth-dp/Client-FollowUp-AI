from pydantic import BaseModel


class FollowUpStatsResponse(BaseModel):
    total: int
    pending: int
    processing: int
    completed: int
    failed: int
    retrying: int