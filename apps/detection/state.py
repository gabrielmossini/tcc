import threading, time
from collections import defaultdict

class DetectionState:
    def __init__(self):
        self._lock = threading.Lock()
        self.latest: list = []
        self.counts: dict = defaultdict(int)
        self.muted: bool = False

    def update(self, detections: list, counts: dict):
        with self._lock:
            self.latest = detections
            self.counts = dict(counts)

    def toggle_mute(self) -> bool:
        with self._lock:
            self.muted = not self.muted
            return self.muted

    def snapshot(self) -> dict:
        with self._lock:
            return {
                'detections': list(self.latest),
                'counts': dict(self.counts),
                'muted': self.muted
            }

detection_state = DetectionState()