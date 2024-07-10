from typing import Any

from fastapi.encoders import jsonable_encoder

from models.payment.payment import Payment
from repositories import database

db = database.create_session()


def create_payment(payment: Payment):
    """
    Crea un nuevo registro de pago en la base de datos.
    db (Session): Sesión de la base de datos (obtenida mediante dependencia).

    Args:
        payment (Payment): Objeto Payment que representa los datos del pago a crear.


    Returns:
        Payment: El objeto Payment creado y almacenado en la base de datos.
    """
    try:
        payment_data: Any = jsonable_encoder(payment)
        payment = Payment(**payment_data)
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment
    finally:
        db.close()


def read_payment(treli_payment_id: int = None, user_id: str = None):
    """
    Busca un registro de pago en la base de datos según el payment_id o el user_id proporcionado.
    db (Session): Sesión de la base de datos (obtenida mediante dependencia).

    Args:
        treli_payment_id (int): El ID del pago a buscar. (Opcional)
        user_id (str): El ID del usuario asociado al pago a buscar. (Opcional)


    Returns:
        Optional[Payment]: El objeto Payment que coincide con los criterios de búsqueda, o None si no se encuentra.
    """
    try:
        if user_id:
            return db.query(Payment).filter(Payment.user_id == user_id).first()

        return (
            db.query(Payment)
            .filter(Payment.treli_payment_id == treli_payment_id)
            .first()
        )
    finally:
        db.close()
