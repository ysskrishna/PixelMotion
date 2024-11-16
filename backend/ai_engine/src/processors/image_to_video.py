import time
from pm_common.models.enums import JobStatus
from pm_common.core.task_status import update_task_status
from src.core.task_processor import BaseTaskProcessor

class ImageToVideoProcessor(BaseTaskProcessor):
    def __init__(self, task_id: str):
        super().__init__(task_id)

    def process(self, file_path: str, **kwargs):
        try:
            print(f"Processing started for task: {self.task_id}, file_path: {file_path}")
            # Simulate image processing - video generation
            for i in range(10):
                time.sleep(3)  # Simulate processing every 3 seconds
                current_progress = (i + 1) * 10  # Progress in percentage (10% increments)
                update_task_status(self.task_id, JobStatus.pending.value, current_progress)

            # generated video link
            video_url = "https://www.youtube.com/watch?v=a7Nw_3zDC7A"
            print(f"Image processed successfully for task: {self.task_id}, file_path: {file_path}")
            update_task_status(self.task_id, JobStatus.success.value, 100, video_url=video_url)

        except Exception as e:
            print(f"Error processing image for task: {self.task_id}, file_path: {file_path}, error: {e}")
            update_task_status(self.task_id, JobStatus.failed.value, 0)


