import logging

import requests
from fastapi import HTTPException, status

from settings import Settings
from utils.sa_token import generate_sa_token

setting_var = Settings

auth_role = setting_var.AUTH_ROLE


def update_role(
    user_id: str = None,
    new_role: str = None,
):
    """
    Actualiza el rol de un usuario mediante una solicitud PUT a un servicio de autenticación.

    Args:
        user_id (str): ID del usuario al que se le actualizará el rol.
        new_role (str): Nuevo rol que se asignará al usuario.

    Returns:
        int: Código de estado de la respuesta HTTP de la solicitud PUT.

    Raises:
        HTTPException: Excepción personalizada en caso de error en la solicitud.

    Note:
        Antes de llamar a esta función, se debe asegurar que `generate_sa_token` ha sido
        implementada para obtener un token de acceso de servicio (Service Account Token).
    """
    method = update_role.__name__
    try:
        sa_token = generate_sa_token(service_audience=setting_var.USERS_RAW_URL)

        url = f"{auth_role}/auth/user/{user_id}/change/role/{new_role.lower()}"

        response = requests.put(
            url=url,
            headers={"Authorization": f"Bearer {sa_token}"},
        )
        response.raise_for_status()

        return response.status_code

    except requests.exceptions.RequestException as error:
        logging.error(f"{method} error {error}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"{method} error: {error}",
        )


def create_user_register(data, utm: dict = None):
    """
    Crea un nuevo registro de usuario mediante una solicitud POST a un servicio de autenticación.

    Args:
        data (dict): Datos del usuario que se utilizarán para crear el registro. Debe ser un diccionario
                     con los detalles del usuario, como nombre, correo electrónico, etc.
        utm (dict, optional): Datos de seguimiento de la fuente de tráfico (UTM parameters) para
                              la campaña de marketing. Si se proporciona, debe ser un diccionario con
                              claves como "utm_web_campaing", "utm_web_medium", "utm_web_source" y "utm_content".
                              Por defecto es None.

    Returns:
        dict: Respuesta JSON de la solicitud POST que contiene información sobre el nuevo registro de usuario.

    Raises:
        HTTPException: Excepción personalizada en caso de error en la solicitud.

    Note:
        Antes de llamar a esta función, se debe asegurar que `generate_sa_token` ha sido
        implementada para obtener un token de acceso de servicio (Service Account Token).


    """
    method = create_user_register.__name__
    try:
        sa_token = generate_sa_token(service_audience=setting_var.USERS_RAW_URL)

        url = f"{auth_role}/auth/registry/user/internal"

        response = requests.post(
            url=url,
            json=data,
            headers={
                "Authorization": f"Bearer {sa_token}",
                "utm-web-campaing": utm.get("utm_web_campaing") if utm else None,
                "utm-web-medium": utm.get("utm_web_medium") if utm else None,
                "utm-web-source": utm.get("utm_web_source") if utm else None,
                "utm-content": utm.get("utm_content") if utm else None,
            },
        )
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:
        logging.error(f"{method} error {error}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"{method} error: {error}",
        )


def change_password_crm(token):
    """
    Cambia la contraseña de un usuario en el Customer Relationship Management (CRM) mediante una solicitud POST
    a un servicio de autenticación.

    Args:
        token (str): Token de autenticación del usuario en el CRM que se utilizará para cambiar la contraseña.

    Returns:
        dict: Respuesta JSON de la solicitud POST que contiene información sobre el cambio exitoso de contraseña.

    Raises:
        HTTPException: Excepción personalizada en caso de error en la solicitud.

    Note:
        Antes de llamar a esta función, se debe asegurar que `generate_sa_token` ha sido
        implementada para obtener un token de acceso de servicio (Service Account Token).
    """
    method = change_password_crm.__name__
    try:
        sa_token = generate_sa_token(service_audience=setting_var.USERS_RAW_URL)

        url = f"{auth_role}/auth/crm/change/password"

        response = requests.post(
            url=url,
            headers={
                "Authorization": f"Bearer {sa_token}",
                "x-auth-crm-token": token,
            },
        )
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:
        logging.error(f"{method} error {error}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"{method} error: {error}",
        )
