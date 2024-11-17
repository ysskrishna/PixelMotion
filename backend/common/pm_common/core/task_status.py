from pm_common.models.enums import OperationType
from pm_common.core.redis_utils import RedisConnection
import json
from datetime import datetime

redis_conn = RedisConnection.get_redis_connection()

def update_task_status(task_id: str, status: str, message: str, progress: int, video_url: str = ""):
    task_status = {
        "task_id": task_id,
        "status": status,
        "message": message,
        "progress": progress,
        "video_url": video_url,
        "updated_at": datetime.now().isoformat(),
        "operation_type": OperationType.update.value
    }
    print(f"Updated task : {task_id}, progress: {progress}")
    redis_conn.publish('task_updates', json.dumps(task_status))


def create_task_status(task_id: str, status: str, title: str, message: str, image_url: str):
    task_status = {
        "task_id": task_id,
        "status": status,
        "message": message,
        "title": title,
        "image_url": image_url,
        "progress": 0,
        "video_url": "",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "operation_type": OperationType.create.value
    }
    print(f"Created task : {task_id}")
    redis_conn.publish('task_updates', json.dumps(task_status))