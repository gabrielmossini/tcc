import os
from pathlib import Path
from django.apps import AppConfig

class DetectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.detection'

    def ready(self):
        from .inference import PPEDetector

        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        model_path = BASE_DIR / 'models' / 'best.pt'

        if not model_path.exists():
            raise FileNotFoundError(
                f"YOLO model not found at {model_path}. "
                "Place best.pt inside the models/ directory."
            )

        self.detector = PPEDetector(str(model_path))