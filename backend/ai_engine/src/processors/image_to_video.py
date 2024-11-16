from src.core.task_processor import BaseTaskProcessor
from pm_common.models.enums import JobStatus
from pm_common.core.task_status import update_task_status
from src.utilities.animations import apply_animation, ANIMATIONS
from PIL import Image
import numpy as np
import random
from moviepy.editor import VideoClip, AudioFileClip


class ImageToVideoProcessor(BaseTaskProcessor):
    def __init__(self, task_id: str):
        super().__init__(task_id)

    
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
        
        animation_data = ANIMATIONS[animation_type]
        animation_func = animation_data['function']
        fps = animation_data['fps']
    
        def make_frame(t):
            frame = img.copy()
            params = animation_func(t, duration, img)
            frame = apply_animation(frame, params, img_width, img_height)
            return np.array(frame)
    
        # Create and save video
        video_clip = VideoClip(make_frame, duration=duration)
        video_clip = video_clip.with_fps(fps)
        video_clip.write_videofile(output_path, codec="libx264")
        if audio_path:
            audio_clip = AudioFileClip(audio_path)
            audio_clip = audio_clip.subclipped(0, duration)  # Trim audio to match video duration
            video_clip = video_clip.with_audio(audio_clip)
            video_clip.write_videofile(output_path, codec="libx264")


    def process(self, file_path: str, **kwargs):
        try:
            print(f"Processing started for task: {self.task_id}, file_path: {file_path}")
            

            image_path = "image.png"  # Path to your image
            output_path = "output.mp4"  # Path to save the video
            animation_type = random.choice(list(ANIMATIONS.keys()))
            duration = 5  # Duration of the video in seconds
            audio_path = "https://music.wixstatic.com/preview/e102c1_916abfabecba4855a7b15e634d74ff18-128.mp3"

            # Generate video
            self.create_animated_video(image_path, output_path, duration, animation_type, audio_path)

            # generated video link
            video_url = ""
            print(f"Image processed successfully for task: {self.task_id}, file_path: {file_path}")
            update_task_status(self.task_id, JobStatus.success.value, 100, video_url=video_url)

        except Exception as e:
            print(f"Error processing image for task: {self.task_id}, file_path: {file_path}, error: {e}")
            update_task_status(self.task_id, JobStatus.failed.value, 0)


