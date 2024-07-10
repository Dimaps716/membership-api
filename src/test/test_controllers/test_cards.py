from unittest import mock

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)
ruta = "/get_tokens/"


def test_get_tokens_endpoint_success():
    # Mock de la función get_tokens
    tokens_mock = ["token1", "token2"]
    with mock.patch("controllers.cards.get_tokens_endpoint", return_value=tokens_mock):
        # Hacemos una solicitud GET simulando una solicitud válida
        response = client.get(
            ruta,
            params={"email": None, "gateway": None},
        )

        # Verificamos que la respuesta sea 200 OK
        assert response.status_code == 200

        # Verificamos que la respuesta contenga los tokens esperados
        assert response.json() == {
            "success": True,
            "tokens": tokens_mock,
            "message": "Tokens obtenidos exitosamente.",
        }


def test_get_tokens_endpoint_missing_parameters():
    response = client.get(ruta)
    assert response.status_code == 424
    assert response.json() == {
        "detail": "get_tokens error: 400 Client Error: Bad Request for url: https://treli.co/wp-json/api/cards/get-tokens"
    }


def test_get_tokens_endpoint_invalid_email():
    response = client.get(
        ruta, params={"email": "invalid_email", "gateway": "pasarela1"}
    )
    assert response.status_code == 424
    assert response.json() == {
        "detail": "get_tokens error: 400 Client Error: Bad Request for url: https://treli.co/wp-json/api/cards/get-tokens?email=invalid_email&gateway=pasarela1"
    }
