from typing import Type, Dict

from src.core.task_processor import BaseTaskProcessor
from src.models.enums import TaskType
from src.processors.image_to_video import ImageToVideoProcessor


class TaskFactory:
    _processors: Dict[TaskType, Type[BaseTaskProcessor]] = {
        TaskType.IMAGE_TO_VIDEO: ImageToVideoProcessor
    }

    @classmethod
    def get_processor(cls, task_type: TaskType, task_id: str) -> BaseTaskProcessor:
        """Get the appropriate processor for the task type"""
        processor_class = cls._processors.get(task_type)
        if not processor_class:
            raise ValueError(f"No processor found for task type: {task_type}")
        
        return processor_class(task_id) 