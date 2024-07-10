from sqlalchemy import Column, Integer, Numeric, String, TIMESTAMP

from repositories.database import Base


class UsersSubscriptions(Base):
    """
    Clase para representar las suscripciones de usuarios.

    Esta clase define la estructura de la tabla "users_subscriptions" en el esquema
    "huntys_management". Contiene campos que almacenan información sobre las
    suscripciones de los usuarios, como IDs de suscripción, ID de usuario, ID de pago,
    estado de la suscripción, fechas de actualización y creación.

    Atributos:
        user_subscription_id (int): ID único de la suscripción de usuario (clave primaria).
        user_id (str): ID único del usuario asociado a la suscripción.
        payment_id (float): ID único del pago asociado a la suscripción.
        users_subscription_status (str): Estado de la suscripción de usuario.
        update_date (datetime): Fecha y hora de la última actualización.
        created_date (datetime): Fecha y hora de creación.

    """

    __tablename__ = "users_subscriptions"

    __table_args__ = {"schema": "huntys_management"}

    user_subscription_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        String(),
        unique=True,
    )
    payment_id = Column(
        Numeric,
        unique=True,
    )
    users_subscription_status = Column(String)
    update_date = Column(TIMESTAMP(timezone=False))
    created_date = Column(TIMESTAMP(timezone=False))
