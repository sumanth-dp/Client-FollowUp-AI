from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.client import Client
from backend.app.schemas.client import ClientCreate, ClientResponse, ClientUpdate
# from app.schemas.client import (
#     ClientCreate,
#     ClientResponse,
#     ClientUpdate,
# )

router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
)


@router.post(
    "",
    response_model=ClientResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_client(
    client_data: ClientCreate,
    db: Session = Depends(get_db),
):
    client = Client(**client_data.model_dump())

    db.add(client)
    db.commit()
    db.refresh(client)

    return client


@router.get(
    "",
    response_model=list[ClientResponse],
)
def get_clients(
    db: Session = Depends(get_db),
):
    result = db.execute(
        select(Client)
    )

    return result.scalars().all()


@router.get(
    "/{client_id}",
    response_model=ClientResponse,
)
def get_client(
    client_id: int,
    db: Session = Depends(get_db),
):
    client = db.get(Client, client_id)

    if client is None:
        raise HTTPException(
            status_code=404,
            detail="Client not found",
        )

    return client



@router.patch(
    "/{client_id}",
    response_model=ClientResponse,
)
def update_client(
    client_id: int,
    client_data: ClientUpdate,
    db: Session = Depends(get_db),
):
    client = db.get(Client, client_id)

    if client is None:
        raise HTTPException(
            status_code=404,
            detail="Client not found",
        )

    update_data = client_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(client, field, value)

    db.commit()
    db.refresh(client)

    return client



@router.delete(
    "/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
):
    client = db.get(Client, client_id)

    if client is None:
        raise HTTPException(
            status_code=404,
            detail="Client not found",
        )

    db.delete(client)
    db.commit()