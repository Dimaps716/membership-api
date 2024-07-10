import logging

from fastapi import HTTPException, status

from repositories.huntys_profile import get_user_profile_user_id


def read_user_profile_db(user_id: str = None, query: bool = None):
    """
    Lee la información de un usuario en la base de datos.

    Args:
        user_id (str, optional): ID del usuario a buscar en la base de datos. Por defecto es None.
        query (bool, optional): Si es True, devuelve la información del usuario encontrada en la base de datos.
                                Si es False, lanza una excepción HTTP 404 si el usuario no es encontrado.
                                Por defecto es None.

    Returns:
        dict or None: Si `query` es True y se encuentra el usuario, devuelve un diccionario con la información del usuario.
                      Si `query` es False y el usuario no es encontrado, devuelve None.

    Raises:
        HTTPException: Excepción personalizada en caso de error al acceder a la base de datos o si el usuario no es encontrado.

    Note:
        Antes de llamar a esta función, se debe asegurar que `get_user_email_or_user_id` ha sido implementada para obtener la
        información del usuario según su correo electrónico o ID.
    """
    try:
        profile = get_user_profile_user_id(user_id=user_id)

        if query:
            return profile

        if not profile:
            raise HTTPException(status_code=404, detail="Historical Payment not found")

    except HTTPException:
        # Reraise HTTPException with more specific detail
        raise

    except Exception as ex:
        logging.error(f"Error accessing database: {ex}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Error accessing database",
        )
