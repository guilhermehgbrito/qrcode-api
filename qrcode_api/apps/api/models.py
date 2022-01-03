from django.db import models


class QrCode(models.Model):
    """
    Model for the QR Code
    """

    # Path to the QR Code
    image = models.ImageField(upload_to="qrcodes", null=True)
    # The description of the QR Code
    data = models.TextField(max_length=2048)
    # The date the QR Code was created
    created_date = models.DateTimeField(auto_now_add=True)
    # The date the QR Code was updated
    updated_date = models.DateTimeField(auto_now=True)
    # If the QR Code still actives in storage
    active = models.BooleanField(default=True)

    def __str__(self):  # pragma: no cover
        return str(self.id)
