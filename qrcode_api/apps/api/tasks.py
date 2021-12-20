from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger("tasks")


@shared_task(
    bind=True,
    default_retry_delay=3,
    countdown=1800,
    retry_kwargs={"max_retries": 5},
)
def delete_qrcode_task(self, qrcode_id):
    import os

    from qrcode_api.apps.api.models import QrCode

    try:
        qrcode = QrCode.objects.get(id=qrcode_id)
        logger.info(f"Deactivating qrcode {qrcode_id}")
        qrcode.active = False
        qrcode.save()
        logger.info(f"Deleting qrcode {qrcode_id}")
        if os.path.exists(qrcode.path):
            os.remove(qrcode.path)
            logger.info(f"Deleted qrcode {qrcode_id}")
        else:
            logger.info("QRCode img doesn't found")
    except Exception as e:
        logger.error(e)
        self.retry(exc=e)
