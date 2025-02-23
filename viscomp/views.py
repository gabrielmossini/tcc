import os, cv2, cvzone, math, json, gc, time, threading

from django.shortcuts import render
from ultralytics import YOLO
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'best.pt')
model = YOLO(model_path)

latest_detections = []
classNames = ['Protecao de Ouvido', 'Capacete', 'Mascara', 'Sem Luva', 'Sem Capacete', 'Sem Botina', 'Sem Colete Refletivo', 'Botina',
            'Oculos de Protecao', 'Luvas de Protecao', 'Colete Refletivo']

detection_count = {class_name: 0 for class_name in classNames}

mute = False

#@csrf_exempt
def detect(request):
    return render(request, 'vision/detect.html')

def video_feed(request):
    return StreamingHttpResponse(video_feed_generator(), content_type='multipart/x-mixed-replace; boundary=frame')

def video_feed_generator():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Não foi possível abrir a câmera.")
        return

    global latest_detections
    latest_detections = []
    frame_index = 0  # Inicializa o index de Frame

    batch_size = 1  # Processa o frame um de cada vez
    frame_buffer = []

    while True:
        start_time = time.time()

        success, img = cap.read()
        if not success:
            print("Error: Falha ao capturar imagem.")
            break

        frame_buffer.append(img)

        if len(frame_buffer) >= batch_size:
            # Processa apenas um frame
            img = frame_buffer.pop(0)  # Usa e Remove os frames mais velhos do buffer
            results = model([img], stream=True)
            detection_count = {}  # Incializa a detecção em cada frame

            boxes = []
            confidences = []
            class_ids = []

            for r in results:
                for box in r.boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    conf = math.ceil((box.conf[0] * 100)) / 100
                    cls = int(box.cls[0])

                    if conf > 0.5:
                        # Converte as coordenadas em float
                        boxes.append([float(x1), float(y1), float(x2), float(y2)])
                        confidences.append(float(conf))
                        class_ids.append(cls)

                        currentClass = classNames[cls]
                        latest_detections.append(currentClass)

                        if currentClass in detection_count:
                            detection_count[currentClass] += 1
                        else:
                            detection_count[currentClass] = 1

            # Aplica Non-Maximum Suppression
            indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.4)

            if len(indices) > 0:
                indices = indices.flatten()  # Achata os indices de Array
                for i in indices:
                    x1, y1, x2, y2 = boxes[i]
                    conf = confidences[i]
                    cls = class_ids[i]
                    currentClass = classNames[cls]

                    if currentClass in ['Sem Capacete', 'Sem Luva', 'Sem Colete Refletivo', 'Sem Botina']:
                        myColor = (0, 0, 255)  # Vermelho para alertas
                        cv2.putText(img, 'ALERTA', (11, 100), 0, 1, [0, 0, 255], thickness=3, lineType=cv2.LINE_AA)
                        play_sound()  # Ativa o som
                    elif currentClass in ['Protecao de Ouvido', 'Capacete', 'Mascara', 'Botina', 'Oculos de Protecao', 'Colete Refletivo', 'Luvas de Protecao']:
                        myColor = (0, 255, 0)  # Verdes para seguro
                    else:
                        myColor = (0, 0, 255)  # Azul para outros

                    cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), myColor, 2)
                    cvzone.putTextRect(img, f'{currentClass} {conf}',
                                       (max(0, int(x1)), max(35, int(y1))), scale=1, thickness=1, colorB=myColor,
                                       colorT=(0, 0, 0), colorR=myColor, offset=6)

            # Termina o timer e calcula o tempo de inferencia
            inference_time = (time.time() - start_time) * 1000  # Tempo em ms

            # Resolução do Frame
            height, width = img.shape[:2]
            resolution = f'{width}x{height}'

            # Gera um String para as legendas
            caption = f"{frame_index}: {resolution} " + ", ".join([f'{v} {k}' for k, v in detection_count.items()]) + f", {inference_time:.1f} ms"
            cv2.putText(img, caption, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            frame_index += 1  # Incrementa o frame de index

            # Codifica os quadros para streaming
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()

            # Produza o quadro e os dados de detecção como JSON
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n' +
                   b'--detection-data\r\n'
                   b'Content-Type: application/json\r\n\r\n' +
                   json.dumps(detection_count).encode() + b'\r\n\r\n')

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        gc.collect()

def get_detections(request):
    global latest_detections

    # Utiliza as últimas detecções do video feed
    new_detections = latest_detections
    update_detection_counts(new_detections)

    response_data = {
        "detections": new_detections,  # List of new detections Lista novas detecções
        "detectionCount": detection_count  # Atualiza contagem
    }
    return JsonResponse(response_data)

def update_detection_counts(detected_objects):
    global detection_count
    detection_count = {}  # Redefinir a contagem de detecção para cada atualização
    for obj in detected_objects:
        if obj in detection_count:
            detection_count[obj] += 1
        else:
            detection_count[obj] = 1

def play_sound():
    global mute
    if not mute:
        threading.Thread(target=lambda: os.system('aplay /Aegis/static/effect/beep.wav')).start()

@csrf_exempt
def toggle_mute(request):
    global mute
    if request.method == 'POST':
        mute = not mute
        return JsonResponse({'muted': mute})
    return JsonResponse({'error': 'Invalid request'}, status=400)

