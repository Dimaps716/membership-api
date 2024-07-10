import json
import logging

import requests
from fastapi import HTTPException, status

from settings import Settings
from utils.sa_token import generate_sa_token

setting_var = Settings

user_api_url = setting_var.BASE_URL


def create_historic(data: dict):
    """
    Crea un registro histórico del estado de un usuario en el sistema.

    Args:
        data (dict): Datos del estado histórico del usuario. Debe ser un diccionario que contenga la información
                     relevante sobre el usuario y su estado en un momento específico.

    Returns:
        dict: Respuesta JSON de la solicitud POST que contiene información sobre el registro histórico.

    Raises:
        HTTPException: Excepción personalizada en caso de error en la solicitud.

    Note:
        Antes de llamar a esta función, se debe asegurar que `generate_sa_token` ha sido
        implementada para obtener un token de acceso de servicio (Service Account Token).

    """
    method = create_historic.__name__
    try:
        sa_token = generate_sa_token(service_audience=setting_var.USERS_RAW_URL)

        url = f"{user_api_url}user/hunty/historic/status"

        response = requests.post(
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


def create_modify_data(old_status: dict, now_status: dict):
    """
    Crea un registro histórico a partir de los estados previo y actual de un usuario.

    Args:
        old_status (dict): Diccionario con el estado previo del usuario, que debe contener las claves 'user_id',
                           'status_id', 'substatus_id' y 'stage_id'.
        now_status (dict): Diccionario con el estado actual del usuario, que debe contener las claves 'user_id',
                           'status_id', 'substatus_id' y 'stage_id'.

    Returns:
        dict: Diccionario con los siguientes datos:
              - 'user_id': ID del usuario.
              - 'current_status_id': ID del estado actual del usuario.
              - 'previous_status_id': ID del estado previo del usuario.
              - 'current_sub_status_id': ID del subestado actual del usuario.
              - 'previous_sub_status_id': ID del subestado previo del usuario.
              - 'created_by_id': ID del usuario que realizó la modificación (puede ser el mismo que 'user_id').
              - 'current_stage_id': ID de la etapa actual del usuario.
              - 'previous_stage_id': ID de la etapa previa del usuario.

    Note:
        Antes de llamar a esta función, se debe asegurar que `create_historic` ha sido implementada para
        crear el registro histórico.

    """
    data = {
        "user_id": old_status.get("user_id"),
        "current_status_id": now_status.get("status_id"),
        "previous_status_id": old_status.get("status_id"),
        "current_sub_status_id": now_status.get("substatus_id"),
        "previous_sub_status_id": old_status.get("substatus_id"),
        "created_by_id": old_status.get("user_id"),
        "current_stage_id": now_status.get("stage_id"),
        "previous_stage_id": old_status.get("stage_id"),
    }
    historic_data = create_historic(data)

    return historic_data
