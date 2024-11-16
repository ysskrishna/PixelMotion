from PIL import Image, ImageFilter, ImageDraw, ImageEnhance, ImageChops
import numpy as np
import random
from src.models.enums import AnimationType

ANIMATIONS = {}


def apply_animation(frame: Image.Image, params: dict, img_width: int, img_height: int) -> Image.Image:
    """Apply animation parameters to a frame"""
    # Apply image modifications if present
    if 'image' in params:
        frame = params['image']
   
    # Apply scale
    new_size = (int(img_width * params['scale']), int(img_height * params['scale']))
    frame = frame.resize(new_size, Image.LANCZOS)
   
    # Apply rotation
    if params['rotation'] != 0:
        frame = frame.rotate(params['rotation'], expand=True)
   
    # Apply offsets and crop to original size
    new_width, new_height = frame.size
    offset_x = (new_width - img_width) // 2 + params['offset_x']
    offset_y = (new_height - img_height) // 2 + params['offset_y']
    frame = frame.crop((
        offset_x,
        offset_y,
        offset_x + img_width,
        offset_y + img_height
    ))
   
    return frame

def register_animation(name: str, recommended_fps: int):
    def decorator(func):
        ANIMATIONS[name] = {
            'function': func,
            'fps': recommended_fps
        }
        return func
    return decorator


# Basic Zoom Animations
@register_animation(AnimationType.ZOOM_IN.value, 30)
def zoom_in(t: float, duration: float, img: Image.Image) -> tuple:
    scale = 1 + 0.5 * (t / duration)
    return {'scale': scale, 'rotation': 0, 'offset_x': 0, 'offset_y': 0}


@register_animation(AnimationType.ZOOM_OUT.value, 30)
def zoom_out(t: float, duration: float, img: Image.Image) -> tuple:
    scale = 1.5 - 0.5 * (t / duration)
    return {'scale': scale, 'rotation': 0, 'offset_x': 0, 'offset_y': 0}


@register_animation(AnimationType.ZOOM_PULSE.value, 60)
def zoom_pulse(t: float, duration: float, img: Image.Image) -> tuple:
    scale = 1 + 0.1 * np.sin(2 * np.pi * t * 3)
    return {'scale': scale, 'rotation': 0, 'offset_x': 0, 'offset_y': 0}


@register_animation(AnimationType.ZOOM_BOUNCE.value, 60)
def zoom_bounce(t: float, duration: float, img: Image.Image) -> tuple:
    scale = 1 + 0.1 * abs(np.sin(2 * np.pi * t * 2))
    return {'scale': scale, 'rotation': 0, 'offset_x': 0, 'offset_y': 0}


@register_animation(AnimationType.ZOOM_SHAKE.value, 60)
def zoom_shake(t: float, duration: float, img: Image.Image) -> tuple:
    scale = 1 + 0.05 * random.uniform(-1, 1)
    return {'scale': scale, 'rotation': 0, 'offset_x': 0, 'offset_y': 0}


# Pan Animations
@register_animation(AnimationType.PAN_LEFT.value, 30)
def pan_left(t: float, duration: float, img: Image.Image) -> tuple:
    offset_x = int(img.width * 0.3 * (t / duration))
    return {'scale': 1.3, 'rotation': 0, 'offset_x': offset_x, 'offset_y': 0}


@register_animation(AnimationType.PAN_RIGHT.value, 30)
def pan_right(t: float, duration: float, img: Image.Image) -> tuple:
    offset_x = -int(img.width * 0.3 * (t / duration))
    return {'scale': 1.3, 'rotation': 0, 'offset_x': offset_x, 'offset_y': 0}


@register_animation(AnimationType.PAN_CIRCULAR.value, 60)
def pan_circular(t: float, duration: float, img: Image.Image) -> tuple:
    radius = 50
    offset_x = int(radius * np.cos(2 * np.pi * t / duration))
    offset_y = int(radius * np.sin(2 * np.pi * t / duration))
    return {'scale': 1.2, 'rotation': 0, 'offset_x': offset_x, 'offset_y': offset_y}


# Rotate Animations
@register_animation(AnimationType.ROTATE_CLOCKWISE.value, 60)
def rotate_clockwise(t: float, duration: float, img: Image.Image) -> tuple:
    rotation = 360 * (t / duration)
    return {'scale': 1.2, 'rotation': rotation, 'offset_x': 0, 'offset_y': 0}


@register_animation(AnimationType.ROTATE_SWING.value, 60)
def rotate_swing(t: float, duration: float, img: Image.Image) -> tuple:
    rotation = 20 * np.sin(2 * np.pi * t * 2)
    return {'scale': 1.1, 'rotation': rotation, 'offset_x': 0, 'offset_y': 0}


# Complex Movements
@register_animation(AnimationType.SPIRAL_IN.value, 60)
def spiral_in(t: float, duration: float, img: Image.Image) -> tuple:
    scale = 1 + (1 - t/duration)
    rotation = 360 * (t / duration)
    return {'scale': scale, 'rotation': rotation, 'offset_x': 0, 'offset_y': 0}


@register_animation(AnimationType.WAVE.value, 60)
def wave(t: float, duration: float, img: Image.Image) -> tuple:
    offset_y = int(30 * np.sin(2 * np.pi * t * 3))
    return {'scale': 1.1, 'rotation': 0, 'offset_x': 0, 'offset_y': offset_y}


@register_animation(AnimationType.ELASTIC.value, 60)
def elastic(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    scale = 1 + 0.2 * (np.exp(-progress * 5) * np.cos(progress * 20))
    return {'scale': scale, 'rotation': 0, 'offset_x': 0, 'offset_y': 0}


# Combination Animations
@register_animation(AnimationType.ZOOM_ROTATE.value, 60)
def zoom_rotate(t: float, duration: float, img: Image.Image) -> tuple:
    scale = 1 + 0.3 * (t / duration)
    rotation = 180 * (t / duration)
    return {'scale': scale, 'rotation': rotation, 'offset_x': 0, 'offset_y': 0}


@register_animation(AnimationType.PAN_ZOOM.value, 60)
def pan_zoom(t: float, duration: float, img: Image.Image) -> tuple:
    scale = 1 + 0.2 * np.sin(2 * np.pi * t * 2)
    offset_x = int(30 * np.cos(2 * np.pi * t * 3))
    return {'scale': scale, 'rotation': 0, 'offset_x': offset_x, 'offset_y': 0}


# Advanced Combination Animations
@register_animation(AnimationType.SPIRAL_ZOOM.value, 60)
def spiral_zoom(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    scale = 1 + 0.3 * np.sin(2 * np.pi * progress * 2)
    rotation = 360 * progress
    offset_x = int(50 * np.cos(2 * np.pi * progress * 3))
    offset_y = int(50 * np.sin(2 * np.pi * progress * 3))
    return {'scale': scale, 'rotation': rotation, 'offset_x': offset_x, 'offset_y': offset_y}


@register_animation(AnimationType.WAVE_ROTATE.value, 60)
def wave_rotate(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    rotation = 30 * np.sin(2 * np.pi * progress * 2)
    offset_y = int(40 * np.sin(2 * np.pi * progress * 3))
    scale = 1.2 + 0.1 * np.sin(2 * np.pi * progress * 4)
    return {'scale': scale, 'rotation': rotation, 'offset_x': 0, 'offset_y': offset_y}


@register_animation(AnimationType.PULSE_PAN.value, 60)
def pulse_pan(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    scale = 1.1 + 0.1 * np.sin(2 * np.pi * progress * 3)
    offset_x = int(img.width * 0.2 * np.sin(2 * np.pi * progress))
    return {'scale': scale, 'rotation': 0, 'offset_x': offset_x, 'offset_y': 0}


@register_animation(AnimationType.BOUNCE_PAN.value, 60)
def bounce_pan(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    scale = 1.2 + 0.1 * abs(np.sin(2 * np.pi * progress * 2))
    offset_x = int(img.width * 0.25 * np.sin(2 * np.pi * progress))
    offset_y = int(30 * abs(np.sin(2 * np.pi * progress * 3)))
    return {'scale': scale, 'rotation': 0, 'offset_x': offset_x, 'offset_y': offset_y}


@register_animation(AnimationType.SHAKE_ROTATE.value, 60)
def shake_rotate(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    rotation = 10 * random.uniform(-1, 1)
    offset_x = int(10 * random.uniform(-1, 1))
    offset_y = int(10 * random.uniform(-1, 1))
    scale = 1.2 + 0.05 * random.uniform(-1, 1)
    return {'scale': scale, 'rotation': rotation, 'offset_x': offset_x, 'offset_y': offset_y}


# Cinematic Effects
@register_animation(AnimationType.KEN_BURNS.value, 30)
def ken_burns(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    scale = 1.1 + 0.15 * progress
    offset_x = int(img.width * 0.1 * progress)
    offset_y = int(img.height * 0.1 * progress)
    return {'scale': scale, 'rotation': 0, 'offset_x': offset_x, 'offset_y': offset_y}


@register_animation(AnimationType.DRAMATIC_ZOOM.value, 30)
def dramatic_zoom(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    scale = 1 + (0.5 * progress ** 2)  # Accelerating zoom
    rotation = 5 * np.sin(2 * np.pi * progress)  # Subtle rotation
    return {'scale': scale, 'rotation': rotation, 'offset_x': 0, 'offset_y': 0}


@register_animation(AnimationType.SMOOTH_DRIFT.value, 60)
def smooth_drift(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    scale = 1.15
    offset_x = int(30 * np.sin(2 * np.pi * progress * 0.5))
    offset_y = int(20 * np.cos(2 * np.pi * progress * 0.7))
    rotation = 5 * np.sin(2 * np.pi * progress * 0.3)
    return {'scale': scale, 'rotation': rotation, 'offset_x': offset_x, 'offset_y': offset_y}


# Advanced Effects
@register_animation(AnimationType.GLITCH.value, 60)
def glitch(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    # Random glitch effects every 0.1 seconds
    if int(progress * 10) % 2 == 0:
        scale = 1 + 0.1 * random.uniform(-1, 1)
        offset_x = int(20 * random.uniform(-1, 1))
        offset_y = int(20 * random.uniform(-1, 1))
        rotation = 5 * random.uniform(-1, 1)
    else:
        scale, offset_x, offset_y, rotation = 1.0, 0, 0, 0
    return {'scale': scale, 'rotation': rotation, 'offset_x': offset_x, 'offset_y': offset_y}


@register_animation(AnimationType.MATRIX_ZOOM.value, 60)
def matrix_zoom(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    # Combines digital-looking zoom with occasional "jumps"
    scale = 1 + (0.5 * progress) + (0.1 if int(progress * 10) % 2 == 0 else 0)
    offset_x = int(10 * np.sin(2 * np.pi * progress * 5))
    return {'scale': scale, 'rotation': 0, 'offset_x': offset_x, 'offset_y': 0}


@register_animation(AnimationType.DOLLY_ZOOM.value, 60)
def dolly_zoom(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    # Simulates the vertigo effect with opposing zoom and scale
    scale = 1 + 0.5 * progress
    offset_x = int(img.width * 0.2 * progress)
    offset_y = int(img.height * 0.2 * progress)
    return {'scale': scale, 'rotation': 0, 'offset_x': offset_x, 'offset_y': offset_y}


@register_animation(AnimationType.WHIRLPOOL.value, 60)
def whirlpool(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    # Creates a spiraling whirlpool effect
    scale = 1 + 0.3 * progress
    rotation = 720 * progress
    radius = 50 * progress
    offset_x = int(radius * np.cos(4 * np.pi * progress))
    offset_y = int(radius * np.sin(4 * np.pi * progress))
    return {'scale': scale, 'rotation': rotation, 'offset_x': offset_x, 'offset_y': offset_y}


@register_animation(AnimationType.EARTHQUAKE.value, 60)
def earthquake(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    # Violent shaking with increasing intensity
    intensity = progress * 30
    offset_x = int(intensity * np.sin(2 * np.pi * progress * 20))
    offset_y = int(intensity * np.cos(2 * np.pi * progress * 15))
    rotation = 5 * np.sin(2 * np.pi * progress * 10)
    return {'scale': 1.2, 'rotation': rotation, 'offset_x': offset_x, 'offset_y': offset_y}


@register_animation(AnimationType.KALEIDOSCOPE.value, 60)
def kaleidoscope(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    # Rotating kaleidoscope effect
    rotation = 360 * progress
    scale = 1.2 + 0.2 * np.sin(2 * np.pi * progress * 3)
    offset_x = int(30 * np.cos(2 * np.pi * progress * 2))
    offset_y = int(30 * np.sin(2 * np.pi * progress * 2))
    return {'scale': scale, 'rotation': rotation, 'offset_x': offset_x, 'offset_y': offset_y}


# Cinematic Pro Effects
@register_animation(AnimationType.VERTIGO.value, 60)
def vertigo(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    # Classic Hitchcock vertigo effect
    scale = 1 + (0.3 * np.sin(np.pi * progress))
    rotation = 5 * np.sin(2 * np.pi * progress)
    return {'scale': scale, 'rotation': rotation, 'offset_x': 0, 'offset_y': 0}


@register_animation(AnimationType.PARALLAX.value, 60)
def parallax(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    # Simulates parallax scrolling effect
    scale = 1.3
    offset_x = int(img.width * 0.2 * np.sin(np.pi * progress))
    offset_y = int(img.height * 0.1 * np.cos(np.pi * progress))
    return {'scale': scale, 'rotation': 0, 'offset_x': offset_x, 'offset_y': offset_y}


@register_animation(AnimationType.DRONE_FLYBY.value, 60)
def drone_flyby(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    # Simulates a drone flying past the subject
    scale = 1.2 + 0.2 * np.sin(np.pi * progress)
    rotation = 10 * np.sin(np.pi * progress)
    offset_x = int(img.width * 0.3 * np.sin(np.pi * progress))
    offset_y = int(img.height * 0.2 * (1 - np.cos(np.pi * progress)))
    return {'scale': scale, 'rotation': rotation, 'offset_x': offset_x, 'offset_y': offset_y}


# Visual Effects
@register_animation(AnimationType.BLUR_ZOOM.value, 60)
def blur_zoom(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    # Increasing blur radius with zoom
    blur_radius = int(5 * progress)
    scale = 1 + 0.3 * progress
    img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    return {'scale': scale, 'rotation': 0, 'offset_x': 0, 'offset_y': 0, 'image': img}


@register_animation(AnimationType.FADE_PULSE.value, 60)
def fade_pulse(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    # Pulsing transparency effect
    opacity = 0.6 + 0.4 * np.sin(2 * np.pi * progress * 2)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(opacity)
    return {'scale': 1.1, 'rotation': 0, 'offset_x': 0, 'offset_y': 0, 'image': img}


@register_animation(AnimationType.TILT_SHIFT.value, 60)
def tilt_shift(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    # Simulated tilt-shift effect with selective blur
    height = img.height
    blur_img = img.filter(ImageFilter.GaussianBlur(radius=5))
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    center_line = int(height * (0.3 + 0.4 * np.sin(np.pi * progress)))
    gradient_size = 100
    for i in range(gradient_size):
        opacity = int(255 * (i / gradient_size))
        draw.line((0, center_line - i, img.width, center_line - i), fill=opacity)
        draw.line((0, center_line + i, img.width, center_line + i), fill=opacity)
    img = Image.composite(img, blur_img, mask)
    return {'scale': 1.1, 'rotation': 0, 'offset_x': 0, 'offset_y': 0, 'image': img}


@register_animation(AnimationType.DREAM_SEQUENCE.value, 60)
def dream_sequence(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    # Dreamy effect with blur and color enhancement
    blur_radius = 3 + 2 * np.sin(2 * np.pi * progress * 2)
    img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.2)
    scale = 1.1 + 0.1 * np.sin(2 * np.pi * progress)
    rotation = 5 * np.sin(np.pi * progress)
    return {'scale': scale, 'rotation': rotation, 'offset_x': 0, 'offset_y': 0, 'image': img}


@register_animation(AnimationType.COLOR_PULSE.value, 60)
def color_pulse(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    # Pulsing color saturation
    saturation = 1 + 0.5 * np.sin(2 * np.pi * progress * 3)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(saturation)
    return {'scale': 1.0, 'rotation': 0, 'offset_x': 0, 'offset_y': 0, 'image': img}


@register_animation(AnimationType.VIGNETTE_ZOOM.value, 60)
def vignette_zoom(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    # Dynamic vignette effect with zoom
    scale = 1 + 0.2 * progress
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    center = (img.width//2, img.height//2)
    max_radius = int(((img.width/2)**2 + (img.height/2)**2)**0.5)
    for r in range(max_radius):
        opacity = int(255 * (1 - r/max_radius)**2)
        draw.ellipse([center[0]-r, center[1]-r, center[0]+r, center[1]+r], fill=opacity)
    img = Image.composite(img, Image.new('RGB', img.size, 'black'), mask)
    return {'scale': scale, 'rotation': 0, 'offset_x': 0, 'offset_y': 0, 'image': img}


# Artistic Effects
@register_animation(AnimationType.WATERCOLOR.value, 60)
def watercolor(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    # Watercolor painting effect
    img = img.filter(ImageFilter.BLUR)
    img = img.filter(ImageFilter.EDGE_ENHANCE)
    img = img.filter(ImageFilter.SMOOTH)
    scale = 1.1 + 0.1 * np.sin(2 * np.pi * progress * 2)
    return {'scale': scale, 'rotation': 0, 'offset_x': 0, 'offset_y': 0, 'image': img}


@register_animation(AnimationType.PIXELATE.value, 60)
def pixelate(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    # Dynamic pixelation effect
    pixel_size = int(20 * (1 - progress))
    if pixel_size > 0:
        small = img.resize((img.width//pixel_size, img.height//pixel_size), Image.NEAREST)
        img = small.resize(img.size, Image.NEAREST)
    return {'scale': 1.0, 'rotation': 0, 'offset_x': 0, 'offset_y': 0, 'image': img}


@register_animation(AnimationType.DOUBLE_EXPOSURE.value, 60)
def double_exposure(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    # Double exposure effect with offset ghost image
    ghost_img = img.copy()
    offset = int(20 * np.sin(2 * np.pi * progress))
    ghost_img = ImageChops.offset(ghost_img, offset, offset)
    ghost_img = ImageEnhance.Brightness(ghost_img).enhance(0.5)
    img = Image.blend(img, ghost_img, 0.5)
    return {'scale': 1.1, 'rotation': 0, 'offset_x': 0, 'offset_y': 0, 'image': img}


@register_animation(AnimationType.RETRO_WAVE.value, 60)
def retro_wave(t: float, duration: float, img: Image.Image) -> tuple:
    progress = t / duration
    # Retro wave aesthetic with color manipulation and scan lines
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.5)
    # Add scan lines
    draw = ImageDraw.Draw(img)
    for y in range(0, img.height, 4):
        draw.line([(0, y), (img.width, y)], fill=(0, 0, 0, 50))
    scale = 1 + 0.1 * np.sin(2 * np.pi * progress * 2)
    return {'scale': scale, 'rotation': 0, 'offset_x': 0, 'offset_y': 0, 'image': img}