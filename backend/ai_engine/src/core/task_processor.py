from abc import ABC, abstractmethod


class BaseTaskProcessor(ABC):
    def __init__(self, task_id: str):
        self.task_id = task_id

    @abstractmethod
    def process(self, **kwargs):
        pass