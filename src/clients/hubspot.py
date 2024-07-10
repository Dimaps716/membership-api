import json
import logging

import requests
from fastapi import HTTPException, status

from settings import Settings

setting_var = Settings

hubspot_email_url = setting_var.HUBSPOT_EMAIL_URL
hubspot_profile = setting_var.HUBSPOT_PROFILE
hubspot_token = setting_var.HUBSPOT_ACCESS_TOKEN
hubspot_url_v3 = setting_var.HUBSPOT_URL_V3

headers = {
    "content-type": "application/json",
    "authorization": "Bearer %s" % hubspot_token,
}


def get_single_hunty_by_email(email: str) -> object:
    """
    Obtiene información de un usuario desde HubSpot por su correo electrónico.

    Args:
        email (str): El correo electrónico del usuario cuya información se quiere obtener.
        query (str, opcional): Una cadena que indica el tipo de consulta a realizar. Los valores válidos son:
                               - None: Si no se proporciona un valor, se devolverá toda la información del usuario.
                               - "True": Devuelve el código de estado de la solicitud HTTP.
                               - "status_data": Devuelve un diccionario que contiene la información del usuario
                                               desde HubSpot y el código de estado de la solicitud HTTP.

    Returns:
        object: La información del usuario en formato JSON si no se especifica un valor para 'query'.
                int: El código de estado de la solicitud HTTP si 'query' es "True".
                dict: Un diccionario que contiene la información del usuario desde HubSpot y el código de estado de la solicitud HTTP
                      si 'query' es "status_data".
    """
    try:
        payload = {"propertyMode": "value_only"}
        url = f"{hubspot_email_url}/{email}/{hubspot_profile}"
        user_hubspot = requests.get(url=url, params=payload, headers=headers)

        if user_hubspot.status_code != 200:
            return user_hubspot.status_code

        return user_hubspot.json(), user_hubspot.status_code

    except Exception as error:
        logging.error(
            f"Error al obtener información del usuario desde HubSpot: {error}"
        )
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Error al obtener información del usuario desde HubSpot.",
        )


def create_user_hubspot(data):
    """
    Crea un nuevo usuario en HubSpot con la información proporcionada.

    Args:
        data (dict): Un diccionario que contiene las propiedades del usuario a crear en HubSpot.

    Returns:
        dict: Un diccionario que contiene los datos de respuesta de HubSpot tras crear el usuario.
    """
    try:
        url = f"{hubspot_url_v3}objects/contacts"

        properties = {"properties": data}

        response = requests.post(url=url, data=json.dumps(properties), headers=headers)
        response_data = response.json()

        response.raise_for_status()

        return response_data

    except Exception as error:
        logging.info({error})
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"Se produjo un error al crear el usuario en HubSpot: {error}",
        )


def update_user_hubspot(data, hubspot_id):
    """
    Actualiza un usuario existente en HubSpot con la información proporcionada.

    Args:
        data (dict): Un diccionario que contiene las propiedades del usuario a actualizar en HubSpot.
        hubspot_id (str): El ID del usuario en HubSpot que se desea actualizar.

    Returns:
        dict: Un diccionario que contiene los datos de respuesta de HubSpot tras actualizar el usuario.
    """
    try:
        url = f"{hubspot_url_v3}objects/contacts/{hubspot_id}"
        properties = {"properties": data}
        response = requests.patch(url=url, data=json.dumps(properties), headers=headers)
        response_data = response.json()

        response.raise_for_status()

        return response_data
    except Exception as error:
        logging.info(f"Error al actualizar el usuario en HubSpot: {error}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"Error al actualizar el usuario en HubSpot: {error}",
        )


def delete_user_hubspot(hubspot_id):
    """
    Elimina un usuario existente en HubSpot.

    Args:
        hubspot_id (str): El ID del usuario en HubSpot que se desea eliminar.

    Returns:
        str: Un mensaje que indica el resultado de la operación de eliminación.
    """
    try:
        url = f"{hubspot_url_v3}objects/contacts/{hubspot_id}"

        response = requests.delete(url=url, headers=headers)

        return f"Se eliminó el usuario en HubSpot con el ID: {hubspot_id}, estado: {response.status_code}"

    except Exception as error:
        logging.info(f"Error al eliminar el usuario en HubSpot: {error}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"Error al eliminar el usuario en HubSpot: {error}",
        )
