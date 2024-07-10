import logging

import requests
from fastapi import HTTPException, status

from settings import Settings


def get_payment_gateways():
    """
    Obtiene una lista de las pasarelas y métodos de pago disponibles en tu cuenta de Treli.

    :return: El resultado de la respuesta en formato JSON.
    """
    method = get_payment_gateways.__name__
    try:
        url = f"{Settings.TRELI_URL_BASE}gateways/list"
        headers = {
            "accept": Settings.APPLICATION_JSON,
            "Authorization": f"Basic {Settings.USER_TRELI_AUTHENTICATION}",
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:
        logging.error(f"{method} error {error}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"{method} error: {error}",
        )
