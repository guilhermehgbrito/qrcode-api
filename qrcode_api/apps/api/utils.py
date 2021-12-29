import logging
from datetime import datetime

import qrcode
from django.conf import settings

from .models import QrCode

logger = logging.getLogger("utils")


def generate_qr_code(data: str) -> QrCode:
    img = qrcode.make(data)
    img_name = f"qrcode{datetime.now().isoformat().replace(':', '')}.png"
    img_path = settings.MEDIA_ROOT / img_name

    if not settings.MEDIA_ROOT.exists():
        settings.MEDIA_ROOT.mkdir()
    with open(img_path, "wb") as f:
        img.save(f)

    qr = QrCode.objects.create(
        data=data,
        path=img_name,
    )
    logger.info(f"QR Code created: {qr.id} | {qr.path}")

    return qr
