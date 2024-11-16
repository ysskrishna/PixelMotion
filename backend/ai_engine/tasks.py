from src.core.task_factory import TaskFactory
from src.models.enums import TaskType


def process_image(task_id: str, file_path: str):
    processor = TaskFactory.get_processor(TaskType.IMAGE_TO_VIDEO, task_id)
    processor.process(file_path)
