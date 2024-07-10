from models.users.users_master import UsersMaster
from repositories import database

db = database.create_session()


def get_user_email_or_user_id(email: str = None, user_id: str = None):
    """
    Busca en la base de datos el registro correspondiente al correo electrónico o user_id del usuario.

    Args:
        email (str): El correo electrónico del usuario a buscar en la base de datos.
        user_id (str): El user_id del usuario a buscar en la base de datos.

    Returns:
        UsersMaster: El objeto UsersMaster correspondiente al correo electrónico del usuario,
                     o None si no se encuentra ningún registro con el correo electrónico dado.
    """
    try:
        if email:
            return db.query(UsersMaster).filter(UsersMaster.email == email).first()

        return db.query(UsersMaster).filter(UsersMaster.user_id == user_id).first()
    finally:
        db.close()
