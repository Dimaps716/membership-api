import logging

import requests
from fastapi import HTTPException, status

from settings import Settings


def add_card_token(gateway: str = None, token_info: dict = None):
    """
    Agrega un token de una tarjeta de crédito y lo asigna a un cliente.

    :param gateway: El id de la pasarela de pago a la cual quieres agregar el token.
    :type gateway: str
    :param token_info: Información del token de la tarjeta de crédito.
                       Esta información puede variar según la pasarela de pago utilizada.
                       El ejemplo a continuación es para la pasarela de pago Wompi.
    :type token_info: dict
    :return: El resultado de la respuesta en formato JSON.
    """
    method = add_card_token.__name__

    try:
        url = f"{Settings.TRELI_URL_BASE}cards/add-token"
        headers = {
            "accept": Settings.APPLICATION_JSON,
            "content-type": Settings.APPLICATION_JSON,
            "Authorization": f"Basic {Settings.USER_TRELI_AUTHENTICATION}",
        }

        data = {"gateway": gateway, "token_info": token_info}

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:
        logging.error(f"{method} error {error}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"{method} error: {error}",
        )


def get_tokens(email: str = None, gateway: str = None):
    """
    Obtiene una lista de los tokens asociados a un cliente y pasarela de pago.

    :param email: Email del cliente.
    :type email: str
    :param gateway: Id de la pasarela de pago.
    :type gateway: str
    :return: El resultado de la respuesta en formato JSON.
    """
    method = get_tokens.__name__

    try:
        url = f"{Settings.TRELI_URL_BASE}cards/get-tokens"
        headers = {
            "accept": Settings.APPLICATION_JSON,
            "Authorization": f"Basic {Settings.USER_TRELI_AUTHENTICATION}",
        }

        params = {"email": email, "gateway": gateway}

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:
        logging.error(f"{method} error {error}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"{method} error: {error}",
        )
