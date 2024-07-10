import functools
import logging

import requests.exceptions
from fastapi import HTTPException, status


def handle_request_exceptions(func):
    """
    Decorador para manejar excepciones de solicitud y registrar errores.

    Este decorador envuelve una función de endpoint, capturando cualquier excepción
    que ocurra durante la solicitud y registrando el error. Si ocurre una excepción
    de solicitud, se levanta una HTTPException con el código de estado 424.

    Args:
        func (callable): La función de endpoint que está siendo envuelta.

    Returns:
        callable: La función de endpoint decorada.
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except requests.exceptions.RequestException as error:
            method = func.__name__
            logging.error(f"{method} error {error}")
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=f"{method} error: {error}",
            )

    return wrapper
