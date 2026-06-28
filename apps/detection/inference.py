import threading

from ultralytics import YOLO

CLASS_NAMES = [
    'Protecao de Ouvido', 'Capacete', 'Mascara',
    'Sem Luva', 'Sem Capacete', 'Sem Botina',
    'Sem Colete Refletivo', 'Botina',
    'Oculos de Protecao', 'Luvas de Protecao', 'Colete Refletivo'
]

NO_PPE_CLASSES = {'Sem Capacete', 'Sem Luva', 'Sem Colete Refletivo', 'Sem Botina'}
PPE_CLASSES    = set(CLASS_NAMES) - NO_PPE_CLASSES


class PPEDetector:
    def __init__(self, model_path: str, confidence_threshold: float = 0.5):
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold
        self._lock = threading.Lock()

    def run(self, frame) -> dict:
        """
        Runs inference on a single frame.
        Returns a dict with 'detections' (list of dicts) and 'counts'.
        """
        results = self.model([frame], stream=True)
        detections = []
        counts = {}

        for r in results:
            for box in r.boxes:
                conf = float(box.conf[0])
                if conf < self.confidence_threshold:
                    continue
                cls = int(box.cls[0])
                cls_name = CLASS_NAMES[cls]
                x1, y1, x2, y2 = (float(v) for v in box.xyxy[0])
                detections.append({
                    'class': cls_name,
                    'confidence': round(conf, 2),
                    'box': [x1, y1, x2, y2],
                    'alert': cls_name in NO_PPE_CLASSES
                })
                counts[cls_name] = counts.get(cls_name, 0) + 1

        return {'detections': detections, 'counts': counts}