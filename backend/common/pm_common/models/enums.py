from enum import Enum


class JobStatus(Enum):
    pending = "pending"
    processing = "processing"
    success = "success"
    failed = "failed"

class OperationType(Enum):
    create = "create"
    update = "update"