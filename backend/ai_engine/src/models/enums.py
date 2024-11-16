from enum import Enum


class TaskType(Enum):
    IMAGE_TO_VIDEO = "IMAGE_TO_VIDEO"


class AnimationType(Enum):
    # Basic Zoom Animations
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"
    ZOOM_PULSE = "zoom_pulse"
    ZOOM_BOUNCE = "zoom_bounce"
    ZOOM_SHAKE = "zoom_shake"
   
    # Pan Animations
    PAN_LEFT = "pan_left"
    PAN_RIGHT = "pan_right"
    PAN_UP = "pan_up"
    PAN_DOWN = "pan_down"
    PAN_CIRCULAR = "pan_circular"
   
    # Rotate Animations
    ROTATE_CLOCKWISE = "rotate_clockwise"
    ROTATE_COUNTERCLOCKWISE = "rotate_counterclockwise"
    ROTATE_SWING = "rotate_swing"
    ROTATE_PULSE = "rotate_pulse"
   
    # Complex Movements
    SPIRAL_IN = "spiral_in"
    SPIRAL_OUT = "spiral_out"
    WAVE = "wave"
    BOUNCE = "bounce"
    ELASTIC = "elastic"
   
    # Combinations
    ZOOM_ROTATE = "zoom_rotate"
    PAN_ZOOM = "pan_zoom"
    BOUNCE_ROTATE = "bounce_rotate"
   
    # Advanced Combinations
    SPIRAL_ZOOM = "spiral_zoom"
    WAVE_ROTATE = "wave_rotate"
    PULSE_PAN = "pulse_pan"
    BOUNCE_PAN = "bounce_pan"
    SHAKE_ROTATE = "shake_rotate"
   
    # Cinematic Effects
    KEN_BURNS = "ken_burns"
    DRAMATIC_ZOOM = "dramatic_zoom"
    SMOOTH_DRIFT = "smooth_drift"
   
    # Advanced Effects
    GLITCH = "glitch"
    MATRIX_ZOOM = "matrix_zoom"
    DOLLY_ZOOM = "dolly_zoom"
    WHIRLPOOL = "whirlpool"
    EARTHQUAKE = "earthquake"
    KALEIDOSCOPE = "kaleidoscope"
   
    # Cinematic Pro
    VERTIGO = "vertigo"
    PARALLAX = "parallax"
    DRONE_FLYBY = "drone_flyby"
   
    # Visual Effects
    BLUR_ZOOM = "blur_zoom"
    FADE_PULSE = "fade_pulse"
    TILT_SHIFT = "tilt_shift"
    DREAM_SEQUENCE = "dream_sequence"
    COLOR_PULSE = "color_pulse"
    VIGNETTE_ZOOM = "vignette_zoom"
   
    # Artistic Effects
    WATERCOLOR = "watercolor"
    PIXELATE = "pixelate"
    DOUBLE_EXPOSURE = "double_exposure"
    RETRO_WAVE = "retro_wave"