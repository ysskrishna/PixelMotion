from pydantic import BaseModel

class TaskStatus(BaseModel):
    task_id: str
    status: str
    message: str
    image_url: str
    created_at: str
    updated_at: str
    title: str = ""
    progress: int = 0
    video_url: str = ""