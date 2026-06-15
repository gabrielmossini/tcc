import os, cv2, cvzone, time, threading

from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .state import detection_state


def _get_detector():
    return apps.get_app_config('detection').detector

@login_required(login_url=reverse_lazy('login'))
def detect(request):
    return render(request, 'detection/detect.html')


@login_required(login_url=reverse_lazy('login'))
def video_feed(request):
    return StreamingHttpResponse(
        video_feed_generator(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )


def video_feed_generator():
    detector = _get_detector()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        error_img = 255 * __import__('numpy').ones((240, 640, 3), dtype='uint8')
        cv2.putText(error_img, 'Camera not found', (30, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 200), 2)
        _, buffer = cv2.imencode('.jpg', error_img)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'
               + buffer.tobytes() + b'\r\n\r\n')
        return

    frame_index = 0

    try:
        while True:
            start_time = time.time()
            success, img = cap.read()

            if not success:
                break

            result = detector.run(img)
            detections = result['detections']
            counts = result['counts']

            detection_state.update(
                [d['class'] for d in detections],
                counts
            )

            for d in detections:
                x1, y1, x2, y2 = (int(v) for v in d['box'])
                color = (0, 0, 255) if d['alert'] else (0, 255, 0)

                if d['alert']:
                    cv2.putText(
                        img, 'ALERTA', (11, 100), 0, 1,
                        (0, 0, 255), thickness=3, lineType=cv2.LINE_AA
                    )
                    play_sound()

                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                cvzone.putTextRect(
                    img,
                    f"{d['class']} {d['confidence']}",
                    (max(0, x1), max(35, y1)),
                    scale=1, thickness=1,
                    colorB=color, colorT=(0, 0, 0),
                    colorR=color, offset=6
                )

            inference_time = (time.time() - start_time) * 1000
            height, width = img.shape[:2]
            caption = (
                f"{frame_index}: {width}x{height} "
                + ", ".join([f'{v} {k}' for k, v in counts.items()])
                + f", {inference_time:.1f} ms"
            )
            cv2.putText(
                img, caption, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2
            )

            frame_index += 1

            ret, buffer = cv2.imencode('.jpg', img)
            if not ret:
                continue

            frame = buffer.tobytes()
            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
            )

    finally:
        cap.release()


@login_required(login_url=reverse_lazy('login'))
def get_detections(request):
    snapshot = detection_state.snapshot()
    return JsonResponse({
        'detections': snapshot['detections'],
        'detectionCount': snapshot['counts']
    })

def process_image_logic(image_path):
    model.predict(source=image_path, save=True, project=output_dir, name="results")


def play_sound():
    if not detection_state.snapshot()['muted']:
        sound_path = os.path.join(
            os.path.dirname(__file__), '..', '..', 'static', 'audio', 'beep.wav'
        )
        threading.Thread(
            target=lambda: os.system(f'aplay "{sound_path}"'),
            daemon=True
        ).start()


@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def toggle_mute(request):
    if request.method == 'POST':
        muted = detection_state.toggle_mute()
        return JsonResponse({'muted': muted})
    return JsonResponse({'error': 'Invalid request'}, status=400)
