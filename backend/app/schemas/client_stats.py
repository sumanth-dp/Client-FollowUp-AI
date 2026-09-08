from pydantic import BaseModel


class ClientFollowUpStatsResponse(BaseModel):
    client_id: int
    client_name: str
    total: int
    pending: int
    processing: int
    completed: int
    failed: int
    retrying: int