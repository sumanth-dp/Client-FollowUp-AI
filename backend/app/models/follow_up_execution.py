# from datetime import datetime

# from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
# from sqlalchemy.orm import Mapped, mapped_column

# from backend.app.core.database import Base
# from sqlalchemy.orm import Mapped, mapped_column, relationship

# class FollowUpExecution(Base):
#     __tablename__ = "follow_up_executions"

#     id: Mapped[int] = mapped_column(
#         Integer,
#         primary_key=True,
#         index=True,
#     )

#     follow_up_id: Mapped[int] = mapped_column(
#         ForeignKey("follow_ups.id"),
#         nullable=False,
#         index=True,
#     )

#     attempt_number: Mapped[int] = mapped_column(
#         Integer,
#         nullable=False,
#     )

#     channel: Mapped[str] = mapped_column(
#         String(50),
#         nullable=False,
#     )

#     status: Mapped[str] = mapped_column(
#         String(50),
#         nullable=False,
#     )

#     started_at: Mapped[datetime] = mapped_column(
#         DateTime,
#         nullable=False,
#     )

#     completed_at: Mapped[datetime | None] = mapped_column(
#         DateTime,
#         nullable=True,
#     )

#     error_message: Mapped[str | None] = mapped_column(
#         Text,
#         nullable=True,
#     )

#     provider_reference: Mapped[str | None] = mapped_column(
#         String(255),
#         nullable=True,
#     )

#     created_at: Mapped[datetime] = mapped_column(
#         DateTime,
#         nullable=False,
#     )

#     follow_up = relationship(
#     "FollowUp",
#     back_populates="executions",
#     )

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base
from sqlalchemy.orm import relationship

class FollowUpExecution(Base):
    __tablename__ = "follow_up_executions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    follow_up_id: Mapped[int] = mapped_column(
        ForeignKey("follow_ups.id"),
        nullable=False,
        index=True,
    )

    attempt_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    channel: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    provider_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    follow_up = relationship(
        "FollowUp",
        back_populates="executions",
    )

    subject: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    body: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

