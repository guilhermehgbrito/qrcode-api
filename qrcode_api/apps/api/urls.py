from django.urls import path

from .views import docs, qrcode_api, swagger

urlpatterns = [
    path("qr", qrcode_api, name="qrcode_api"),
    path("swagger", swagger, name="swagger"),
    path("docs", docs, name="docs"),
]
