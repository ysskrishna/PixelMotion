from src.core.task_processor import BaseTaskProcessor
from pm_common.models.enums import JobStatus
from pm_common.core.task_status import update_task_status
from pm_common.core.s3 import S3Client
from src.utilities.animations import apply_animation, ANIMATIONS
from PIL import Image
import numpy as np
import random
from moviepy.editor import VideoClip, AudioFileClip
import tempfile
import os


class ImageToVideoProcessor(BaseTaskProcessor):
    SUPPORTED_FORMATS = {'jpg', 'jpeg', 'png'}

    def __init__(self, task_id: str):
        super().__init__(task_id)
        self.s3_client = S3Client()

    
    def create_animated_video(
        self,
        image_path: str,
        output_path: str,
        duration: int,
        animation_type: str,
        audio_path: str = None,
    ):
        # Load image
        img = Image.open(image_path)
        img_width, img_height = img.size
        print(f"Image size: {img_width}x{img_height}")
        
        animation_data = ANIMATIONS[animation_type]
        animation_func = animation_data['function']
        fps = animation_data['fps']
        print(f"Animation type: {animation_type}, fps: {fps}")

        def make_frame(t):
            frame = img.copy()
            params = animation_func(t, duration, img)
            frame = apply_animation(frame, params, img_width, img_height)
            return np.array(frame)
    
        # Create and save video
        video_clip = VideoClip(make_frame, duration=duration)
        video_clip = video_clip.set_fps(fps)
        print(f"Set video clip fps to {fps}")
        
        if audio_path:
            audio_clip = AudioFileClip(audio_path)
            audio_clip = audio_clip.subclip(0, duration)  # Trim audio to match video duration
            video_clip = video_clip.set_audio(audio_clip)
            print(f"Set audio clip to {audio_path}")

        video_clip.write_videofile(output_path, codec="libx264")
        print(f"Video clip written to {output_path}")

    def process(self, file_path: str, **kwargs):
        try:
            print(f"Processing started for task: {self.task_id}, file_path: {file_path}")

            file_ext = file_path.split('.')[-1].lower()
            if file_ext not in self.SUPPORTED_FORMATS:
                raise ValueError(f"Unsupported file format: {file_ext}")
            
            with tempfile.TemporaryDirectory() as temp_dir:
                image_path = os.path.join(temp_dir, f"image.{file_ext}")
                self.s3_client.download_file(file_path, image_path)
                print(f"Image path: {image_path}")
                
                output_path = os.path.join(temp_dir, f"{self.task_id}_output.mp4")
                animation_type = random.choice(list(ANIMATIONS.keys()))
                duration = 5  # Duration of the video in seconds
                # audio_path = "https://music.wixstatic.com/preview/e102c1_916abfabecba4855a7b15e634d74ff18-128.mp3"
                audio_path = os.path.join(os.path.dirname(__file__), "e102c1_916abfabecba4855a7b15e634d74ff18-128.mp3")
                print(f"Audio path: {audio_path}")

                self.create_animated_video(image_path, output_path, duration, animation_type, audio_path)

                video_url = self.s3_client.upload_file(output_path, f"videos/{self.task_id}_output.mp4", extra_args={'ContentType': 'video/mp4'})
                print(f"Image processed successfully for task: {self.task_id}, file_path: {file_path}, video_url: {video_url}")
                update_task_status(self.task_id, JobStatus.success.value, 100, video_url=video_url)

        except Exception as e:
            print(f"Error processing image for task: {self.task_id}, file_path: {file_path}, error: {e}")
            update_task_status(self.task_id, JobStatus.failed.value, 0)


