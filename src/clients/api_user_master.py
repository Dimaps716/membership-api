import json
import logging

import requests
from fastapi import HTTPException, status

from settings import Settings
from utils.sa_token import generate_sa_token

setting_var = Settings

user_api_update = setting_var.USER_MASTER_UPDATE


def update_user_master(user_id: str = None, data: dict = None):
    """
    Actualiza los datos de un usuario a través de una API utilizando un token de cuenta de servicio.

    Esta función realiza una solicitud PUT a la API de usuarios para actualizar la información
    del usuario identificado por el `user_id` proporcionado. La función requiere un token de cuenta
    de servicio para autenticar la solicitud.

    Parámetros:
        user_id (str): El identificador del usuario cuyos datos se deben actualizar.
        data (dict): Un diccionario que contiene los datos actualizados del usuario.

    Retorna:
        dict: Un diccionario que contiene la respuesta JSON de la API si la actualización es exitosa.

    Lanza:
        HTTPException: Si ocurre un error durante la llamada a la API, se generará una HTTPException
                       con un código de estado 424 Failed Dependency y un mensaje de error en el detalle.
                       El error también se registrará mediante el módulo de registro de Python.

    Ejemplo:
        user_id = "12345"
        data = {"nombre": "Juan Pérez", "correo": "juan.perez@example.com"}
        datos_actualizados = actualizar_usuario_maestro(user_id, data)
    """
    method = update_user_master.__name__
    try:
        sa_token = generate_sa_token(service_audience=setting_var.USERS_RAW_URL)

        url = f"{user_api_update}/{user_id}"

        response = requests.put(
            url=url,
            data=json.dumps(data),
            headers={"Authorization": f"Bearer {sa_token}"},
        )
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:
        logging.error(f"{method} error {error}")

        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"{method} error: {error}",
        )


def patch_real_time_db_status(
    user_id: str,
    show_modal: bool = None,
    show_hubspot_banner: bool = None,
    show_banner: bool = None,
):
    """
    Obtiene la información principal del usuario por ID utilizando la API de Usuarios Hunty.

    Args:
        show_banner (bool, opcional): Bandera para mostrar el banner.
        show_hubspot_banner (bool, opcional): Bandera para mostrar el banner de HubSpot.
        user_id (str): ID de usuario.
        show_modal (bool, opcional): Bandera para mostrar el modal.

    Returns:
        dict: Información principal del usuario.

    """

    method = patch_real_time_db_status.__name__
    try:
        sa_token = generate_sa_token(service_audience=setting_var.USERS_RAW_URL)

        request_url = f"{setting_var.USER_MASTER}/real-time-db-notification/{user_id}"

        params = {
            "show_modal": show_modal,
            "show_hubspot_banner": show_hubspot_banner,
            "show_banner": show_banner,
        }
        response = requests.put(
            request_url, params=params, headers={"Authorization": f"Bearer {sa_token}"}
        )
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:
        logging.error(f"{method} error {error}")

        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"{method} error: {error}",
        )
