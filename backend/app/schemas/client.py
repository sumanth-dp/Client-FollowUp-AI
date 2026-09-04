# pydantic is for API input/output validation

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

# What the frontend/client is allowed to send
class ClientCreate(BaseModel):
    name: str
    company: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    whatsapp: str | None = None
    status: str = "new"
    priority: str = "medium"
    assigned_user_id: int | None = None

# What our API returns:
class ClientResponse(BaseModel):
    id: int
    name: str
    company: str | None
    email: EmailStr | None
    phone: str | None
    whatsapp: str | None
    status: str
    priority: str
    assigned_user_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# for client update
class ClientUpdate(BaseModel):
    name: str | None = None
    company: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    whatsapp: str | None = None
    status: str | None = None
    priority: str | None = None
    assigned_user_id: int | None = None