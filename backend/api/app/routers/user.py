from fastapi import APIRouter,  HTTPException, File, Form, UploadFile

import uuid
import json
from datetime import datetime
from app.models.schemas import TaskStatus
from pm_common.core.s3 import S3Client
from pm_common.core.redis_utils import RedisConnection
from app.core.config import config

router = APIRouter()

s3_client = S3Client()
redis_conn = RedisConnection.get_redis_connection()


@router.get("/tasks", response_model=list[TaskStatus])
async def get_all_tasks():
    task_keys = redis_conn.keys()
    tasks = []
    for task_key in task_keys:
        task_id = task_key.decode("utf-8")
        task_status_str = redis_conn.get(task_id)
        if task_status_str:
            task_status = json.loads(task_status_str)
            tasks.append(TaskStatus(**task_status))
    return tasks



@router.post("/upload")
def upload_image(file: UploadFile = File(...), title: str = Form(...)):
    # Generate unique filename
    current_datetime = datetime.now()
    formatted_timestamp = current_datetime.strftime('%y%m%d%H%M%S')
    filename = f"{formatted_timestamp}_{file.filename}"
    task_id = str(uuid.uuid4())

    
    if file.content_type not in ['image/jpeg', 'image/png', 'image/jpg']:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Upload file to S3
    file_url = s3_client.upload_file(file.file, f"{config.IMAGES_FOLDER}/{filename}", file.content_type)
    print(f"file_url: {file_url}, title: {title}, content_type: {file.content_type}")

    # create_task_status(task_id, JobStatus.pending.value, title, image_url=file_path)
    
    # # Add background task to jobs_queue
    # jobs_queue.enqueue(process_image, task_id, file_path)

    return {"task_id": task_id, "filename": filename, "file_url": file_url}