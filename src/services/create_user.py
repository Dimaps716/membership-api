import base64
import logging

from fastapi import HTTPException, status

from clients import auth_role, historic_status
from enums import status_user
from settings import Settings

setting_var = Settings


def create_user(data: dict):
    """
    Crea un nuevo usuario mediante el registro en el sistema.

    Args:
        data (dict): Datos del usuario que se utilizarán para crear el registro. Debe ser un diccionario
                     con detalles del usuario, como nombre, correo electrónico, etc.

    Returns:
        dict: Respuesta JSON que contiene información sobre el nuevo registro de usuario, incluido el ID del usuario.

    Raises:
        HTTPException: Excepción personalizada en caso de error en el registro o en la solicitud.

    Note:
        Antes de llamar a esta función, se debe asegurar que `auth_role.create_user_register` y `historic_status.create_historic`
        están implementadas para manejar la creación del usuario y el registro de su estado histórico respectivamente.
    """
    method = create_user.__name__
    try:
        email = data.get("email").encode("ascii")

        email_encode = base64.b64encode(email).decode("ascii")

        data_user = {
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "email": data.get("email"),
            "password": email_encode,
            "user_type_id": status_user.TypeUser.hunty,
            "user_subtype_id": status_user.TypeUser.hunty,
            "status_id": status_user.Status.registered.value,
            "sub_status_id": status_user.SubStatus.registration.value,
        }

        create_user_auth = auth_role.create_user_register(data=data_user)

        user_status = {
            "user_id": create_user_auth.get("user_id"),
            "current_status_id": status_user.Status.registered.value,
            "current_sub_status_id": status_user.SubStatus.registration.value,
            "created_by_id": create_user_auth.get("user_id"),
        }

        historic_status.create_historic(data=user_status)

        return create_user_auth

    except HTTPException:
        # Reraise HTTPException with more specific detail
        raise

    except Exception as error:
        logging.error(f"{method} error {error}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"{method} error: {error}",
        )
