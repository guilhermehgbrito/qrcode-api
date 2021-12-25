from django.conf import settings
from django.test import Client, TestCase, override_settings
from qrcode_api.apps.api.models import QrCode
from qrcode_api.apps.api.tasks import delete_qrcode_task
from rest_framework import status

from ..schemas import swagger_schema


class ViewsTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def tearDown(self) -> None:
        for qr in QrCode.objects.all():
            delete_qrcode_task(qr.id)
        return super().tearDown()

    @override_settings(
        CELERY_BROKER_URL="memory://localhost/",
        CELERY_IGNORE_RESULT=True,
    )
    def test_qrcode_api_qr_code_generation_success(self):
        response = self.client.post("/api/qr", {"data": "test"})

        img_path = settings.PROJECT_DIR / response.json()["img_url"][1:]

        self.assertTrue(img_path.exists())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["status"], "success")

    def test_qrcode_api_error(self):
        response = self.client.post("/api/qr", {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["status"], "error")

    def test_swagger_schema(self):
        response = self.client.get("/api/swagger")

        self.assertEqual(response.json(), dict(swagger_schema))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_docs(self):
        response = self.client.get("/api/docs")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
