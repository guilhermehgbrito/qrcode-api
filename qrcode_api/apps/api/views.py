import logging

from django.conf import settings
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from qrcode_api.apps.api.utils import generate_qr_code
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import HttpRequest

from .schemas import swagger_schema
from .tasks import delete_qrcode_task, expiration_time

logger = logging.getLogger(__name__)


@api_view(["POST"])
def qrcode_api(request: HttpRequest) -> JsonResponse:

    data = request.data.get("data", None)

    if data is not None:
        qr = generate_qr_code(data)

        delete_qrcode_task.delay(qr.id)
        logger.info(f"Task called: {qr.id}")

        return JsonResponse(
            {
                "status": "success",
                "img_url": f"{settings.MEDIA_URL}{qr.path}",
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
