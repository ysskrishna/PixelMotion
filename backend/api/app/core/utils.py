import json
from app.models.schemas import TaskStatus
from pm_common.core.s3 import S3Client



connected_websockets = set()



s3_client = S3Client()

def format_task(task_status_str: str):
    task_status = json.loads(task_status_str)
    task_status = TaskStatus(**task_status).model_dump()

    image_url = task_status.get("image_url")
    if image_url:
        task_status["image_url"] = s3_client.get_file_url(image_url)
    
    video_url = task_status.get("video_url") 
    if video_url:
        task_status["video_url"] = s3_client.get_file_url(video_url)

    return task_status

