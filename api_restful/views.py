from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from PIL import Image
import io, os
import torch
import json


def nombre_modelo(request):
    if request.method == 'GET':
        return JsonResponse({
            "modelo": "YOLOv5x6",
            "tamaño_entrada": "1024",
            "velocidad_cpu": "3136",
            "box_loss": "0.03494",
            "obj_loss": "0.05193",
            "cls_loss": "0.002209",
            "mAP50": "0.705",
            "mAP50-95": "0.482",
        })
    else:
        return JsonResponse({"respuesta": "Método no soportado"})


@csrf_exempt
def procesarFoto(request):
    if request.method == 'POST':
        #Leer la foto del cuerpo de la solicitud
        fotoBytes = request.body
        
        #Convertir de byte a imagen
        imagen = Image.open(io.BytesIO(fotoBytes))
        
        #Comprobar que el modelo existe
        ruta_yolov5 = os.path.join(settings.MEDIA_ROOT, "yolov5")
        ruta_yolov5_pesos = os.path.join(settings.MEDIA_ROOT, "yolov5/runs/train/exp/weight/best.pt")

        if not os.path.exists(ruta_yolov5_pesos):
            return JsonResponse({"respuesta": "Modelo no disponible"})
        
        #Procesar la foto
        respuesta = inferencia_yolo(imagen, ruta_yolov5, ruta_yolov5_pesos, 1024)
        
        #Enviar la respuesta al cliente
        return JsonResponse(respuesta, safe=False)
    else:
        return JsonResponse({"respuesta": "Método no soportado"})


def inferencia_yolo(foto, ruta_proyecto, ruta_pesos, tamaño):
    modelo = torch.hub.load(
        repo_or_dir = ruta_proyecto,
        model = 'custom',
        path = ruta_pesos,
        source = 'local',
        device = 'cpu',
    )
    
    modelo.conf = 0.25          # umbral de confianza
    modelo.iou = 0.45           # umbral de IoU
    modelo.agnostic = False     # NMS independiente de la clase
    modelo.multi_label = False  # Múltiples etiquetas por caja
    modelo.max_det = 15         # Número máximo de detecciones por imágen
    modelo.amp = False          # Inferencia automática de precisión mixta (Automatic Mixed Precision, AMP)
    
    resultados = modelo(foto, size=tamaño)
    json_result = json.loads(
        resultados.pandas().xyxy[0].to_json(orient="records")
    )
    return json_result