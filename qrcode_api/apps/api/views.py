import logging
from datetime import datetime

import qrcode
from decouple import config
from django.conf import settings
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from qrcode_api.apps.api.models import QrCode
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import HttpRequest

from .schemas import swagger_schema
from .tasks import delete_qrcode_task

logger = logging.getLogger(__name__)

expiration_time = config("EXPIRATION_TIME", default=1800, cast=int)


@api_view(["POST"])
def qrcode_api(request: HttpRequest) -> JsonResponse:

    data = request.data.get("data", None)

    if data is not None:
        img = qrcode.make(data)
        img_name = f"qrcode{datetime.now().isoformat().replace(':', '')}.png"
        img_path = settings.MEDIA_ROOT / img_name
        with open(img_path, "wb") as f:
            img.save(f)

        logger.info(f"QR code saved to {img_path}")
        qr = QrCode.objects.create(
            data=data,
            path=img_path,
        )
        logger.info(f"QR Code created: {img_path}")

        delete_qrcode_task.apply_async(args=[qr.id], countdown=expiration_time)
        logger.info(f"Task called: {qr.id}")

        return JsonResponse(
            {
                "status": "success",
                "img_url": f"{settings.MEDIA_URL}{img_name}",
                "message": "This QR code will be expired "
                + f"in {expiration_time/60:.0f} minute(s).",
            }
        )
    else:
        return JsonResponse(
            {"status": "error", "message": "data is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
def swagger(request: HttpRequest) -> JsonResponse:
    return JsonResponse(swagger_schema)


def docs(request: HttpRequest) -> HttpResponse:
    swagger_url = f"{request.scheme}://{request.get_host()}/api/swagger"
    return render(request, "swagger.html", {"swagger_url": swagger_url})
