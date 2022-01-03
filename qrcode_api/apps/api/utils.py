import logging
from datetime import datetime
from io import BytesIO

import qrcode
from django.conf import settings
from django.core.files import images

from .models import QrCode

logger = logging.getLogger("utils")


def generate_qr_code(data: str) -> QrCode:
    img = qrcode.make(data)
    img_name = f"qrcode{datetime.now().isoformat().replace(':', '')}.png"
    b = BytesIO()
    img.save(b)
    qr = QrCode(data=data)
    qr.image.save(img_name, images.ImageFile(b))
    qr.save()
    logger.info(f"QR Code created: {qr.id} | {qr.image}")

    return qr
