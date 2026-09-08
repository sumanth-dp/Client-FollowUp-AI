from pydantic import BaseModel


class FollowUpEmail(BaseModel):
    subject: str
    body: str