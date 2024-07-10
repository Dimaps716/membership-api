from models.users.huntys_profile import UserHunties
from repositories import database

db = database.create_session()


def get_user_profile_user_id(user_id: str = None):
    """
    Busca en la base de datos el registro correspondiente al user_id del usuario.

    Args:
        user_id (str): El user_id del usuario a buscar en la base de datos.

    Returns:
        UsersMaster: El objeto UserHunties correspondiente al correo electrónico del usuario,
                     o None si no se encuentra ningún registro con el correo electrónico dado.
    """
    try:
        return db.query(UserHunties).filter(UserHunties.user_id == user_id).first()

    finally:
        db.close()
