from unittest import mock

from celery.exceptions import Retry
from django.test import Client, TestCase, override_settings
from rest_framework import status

from ..tasks import delete_qrcode_task
from ..utils import generate_qr_code

delete_qrcode_task.retry = mock.MagicMock(side_effect=Retry)


class TasksTestCase(TestCase):
    def setUp(self) -> None:
        self.qr = generate_qr_code("test")
        self.client = Client()
        return super().setUp()

    @override_settings(
        CELERY_BROKER_URL="memory://localhost/", CELERY_IGNORE_RESULT=True
    )
    def test_delete_qrcode_task(self):
        img_url = self.qr.image.url
        result = delete_qrcode_task.apply(args=[self.qr.id])
        result.get()
        response = self.client.get(img_url)
        self.assertTrue(result.successful())
        self.assertTrue(response.status_code == status.HTTP_404_NOT_FOUND)

    def tearDown(self) -> None:
        delete_qrcode_task.apply(args=[self.qr.id])
        return super().tearDown()
