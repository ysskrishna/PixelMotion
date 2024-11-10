from dotenv import load_dotenv
from pm_common.core.config import BaseConfig
import os


load_dotenv()

class Config(BaseConfig):
    IMAGES_FOLDER = os.getenv('IMAGES_FOLDER')
    VIDEOS_FOLDER = os.getenv('VIDEOS_FOLDER')

config = Config()
  

