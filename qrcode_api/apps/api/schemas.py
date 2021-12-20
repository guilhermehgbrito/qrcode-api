from decouple import config
from drf_yasg.openapi import Info, Schema, Swagger

post_schema = Schema(
    title="QRCode",
    type="object",
    properties={"data": {"type": "string"}},
    required=["data"],
)

response_schema = Schema(
    title="QRCodeResponse",
    type="object",
    properties={
        "status": {"type": "string"},
        "img_url": {"type": "string"},
        "message": {"type": "string"},
    },
    required=["status", "message"],
)

swagger_schema = Swagger(
    Info(
        "QRCodeAPI",
        "v1.0.0",
        "Generate your QR code through an easy-to-use API REST",
    ),
    paths={
        "/qr": {
            "post": {
                "tags": ["QRCode"],
                "description": "Generate a new QRCode.",
                "responses": {
                    "200": {
                        "description": "Your QR Code image url.",
                        "schema": {"$ref": "#/definitions/QRCodeResponse"},
                    },
                    "400": {
                        "description": "Data sent was invalid.",
                        "schema": {"$ref": "#/definitions/QRCodeResponse"},
                    },
                },
                "parameters": [
                    {
                        "name": "data",
                        "in": "body",
                        "schema": {"$ref": "#/definitions/QRCode"},
                    }
                ],
            }
        }
    },
    _url=config("DOMAIN"),
    _prefix="/api",
    definitions={"QRCode": post_schema, "QRCodeResponse": response_schema},
)
