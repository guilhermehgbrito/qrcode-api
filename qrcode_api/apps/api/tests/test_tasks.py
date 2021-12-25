from unittest import mock

from celery.exceptions import Retry
from django.conf import settings
from django.test import TestCase, override_settings

from ..tasks import delete_qrcode_task
from ..utils import generate_qr_code

delete_qrcode_task.retry = mock.MagicMock(side_effect=Retry)


class TasksTestCase(TestCase):
    def setUp(self) -> None:
        self.qr = generate_qr_code("test")
        return super().setUp()

    @override_settings(
        CELERY_BROKER_URL="memory://localhost/", CELERY_IGNORE_RESULT=True
    )
    def test_delete_qrcode_task(self):
        result = delete_qrcode_task.apply(args=[self.qr.id])
        result.get()
        self.assertTrue(result.successful())
        self.assertFalse((settings.MEDIA_ROOT / self.qr.path).exists())

    def tearDown(self) -> None:
        delete_qrcode_task.apply(args=[self.qr.id])
        return super().tearDown()
