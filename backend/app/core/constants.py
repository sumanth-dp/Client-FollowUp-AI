from typing import Literal


FollowUpType = Literal[
    "email",
    "whatsapp",
    "call",
    "reminder",
]

FollowUpStatus = Literal[
    "pending",
    "processing",
    "completed",
    "failed",
]

FollowUpPriority = Literal[
    "low",
    "medium",
    "high",
]

FollowUpExecutionStatus = Literal[
    "processing",
    "completed",
    "failed",
]



FOLLOW_UP_EXECUTION_STATUSES = (
    "processing",
    "completed",
    "failed",
)

EXECUTION_PROCESSING = "processing"
EXECUTION_COMPLETED = "completed"
EXECUTION_FAILED = "failed"