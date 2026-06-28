import threading
from collections import defaultdict

_CONFIRM_FRAMES = 5
_RELEASE_FRAMES = 10

_IDLE      = 'IDLE'
_CANDIDATE = 'CANDIDATE'
_VIOLATION = 'VIOLATION'
_RELEASING = 'RELEASING'


class ViolationTracker:
    """
    Per-class state machine that debounces detections before triggering alerts.
    IDLE → CANDIDATE (seen N frames) → VIOLATION → RELEASING (absent M frames) → IDLE
    """

    def __init__(self, confirm: int = _CONFIRM_FRAMES, release: int = _RELEASE_FRAMES):
        self._lock = threading.Lock()
        self._confirm = confirm
        self._release = release
        self._entries: dict = {} 

    def update(self, active_classes: set) -> set:
        """
        Call once per frame with currently detected violation class names.
        Returns the set of classes that just transitioned into VIOLATION this frame.
        """
        with self._lock:
            newly_violated: set = set()
            for cls in set(self._entries) | active_classes:
                entry = self._entries.get(cls)
                state = entry['state'] if entry else _IDLE
                count = entry['count'] if entry else 0

                if cls in active_classes:
                    if state == _IDLE:
                        self._entries[cls] = {'state': _CANDIDATE, 'count': 1}
                    elif state == _CANDIDATE:
                        count += 1
                        if count >= self._confirm:
                            self._entries[cls] = {'state': _VIOLATION, 'count': 0}
                            newly_violated.add(cls)
                        else:
                            self._entries[cls] = {'state': _CANDIDATE, 'count': count}
                    elif state == _RELEASING:
                        self._entries[cls] = {'state': _VIOLATION, 'count': 0}
                else:
                    if state in (_IDLE, _CANDIDATE):
                        self._entries.pop(cls, None)
                    elif state == _VIOLATION:
                        self._entries[cls] = {'state': _RELEASING, 'count': 1}
                    elif state == _RELEASING:
                        count += 1
                        if count >= self._release:
                            self._entries.pop(cls)
                        else:
                            self._entries[cls] = {'state': _RELEASING, 'count': count}

            return newly_violated

    def active_violations(self) -> set:
        """Returns class names currently in confirmed VIOLATION state."""
        with self._lock:
            return {cls for cls, e in self._entries.items() if e['state'] == _VIOLATION}


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
violation_tracker = ViolationTracker()