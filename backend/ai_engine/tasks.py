import time
from pm_common.models.enums import JobStatus
from pm_common.core.task_utils import update_task_status


def process_image(task_id: str, file_path: str):
    try:
        print(f"processing started for task: {task_id}, file_path: {file_path}")
        # Simulate image processing - video generation
        for i in range(10):
            time.sleep(3)  # Simulate processing every 3 seconds
            current_progress = (i + 1) * 10  # Progress in percentage (10% increments)
            update_task_status(task_id, JobStatus.pending.value, current_progress)

        # generated video link
        video_url = "https://www.youtube.com/watch?v=a7Nw_3zDC7A"
        print(f"Image processed successfully for task: {task_id}, file_path: {file_path}")
        update_task_status(task_id, JobStatus.success.value, 100, video_url=video_url)

    except Exception as e:
        print(f"Error processing image for task: {task_id}, file_path: {file_path}, error: {e}")
        update_task_status(task_id, JobStatus.failed.value, 0)



