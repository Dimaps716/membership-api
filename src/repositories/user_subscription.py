from typing import Any

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from enums.payment_status import PaymentStatus, PaymentType
from models.payment.subscriptions import UsersSubscriptions
from repositories import database

db = database.create_session()


def create_users_subscriptions(payment: UsersSubscriptions):
    """
    Crea un nuevo registro de pago histórico en la base de datos.
    db (Session): Sesión de la base de datos (obtenida mediante dependencia).

    Args:
        payment (HistoricalPayment): Objeto HistoricalPayment que representa los datos del pago histórico a crear.


    Returns:
        HistoricalPayment: El objeto HistoricalPayment creado y almacenado en la base de datos.
    """
    try:
        payment_data: Any = jsonable_encoder(payment)
        payment = UsersSubscriptions(**payment_data)
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment
    finally:
        db.close()


def read_users_subscriptions(user_id: str = None):
    """
    Busca registros de pagos históricos en la base de datos según el payment_id o el user_id proporcionado.
    db (Session): Sesión de la base de datos (obtenida mediante dependencia).
    Args:
        user_id (int): El ID del pago histórico a buscar. (Opcional)


    Returns:
        List[HistoricalPayment]: Una lista de objetos HistoricalPayment que coinciden con los criterios de búsqueda.
    """
    try:
        return (
            db.query(UsersSubscriptions)
            .filter(UsersSubscriptions.user_id == user_id)
            .first()
        )

    finally:
        db.close()


def read_hunty_status_subscription(user_id: str):
    """
    Search the user's subscription history to see if they have an active hunty pro subscription or if they have had one and it has been cancelled.
    Args:
        user_id (str): User ID
    Returns:
        Dict: Data Status Subscription Hunty
    """
    try:
        return db.execute(
            f"""
            WITH payments as (
                SELECT user_id,
                    payment_id,
                    payment_type,
                    CASE WHEN lower(item_name) LIKE '%mensual%' THEN 'Hunty Pro Mensual'
                    WHEN lower(item_name) LIKE '%trimestral%' THEN 'Hunty Pro Trimestral'
                    WHEN lower(item_name) LIKE '%semestral%' THEN 'Hunty Pro Semestral'
                END as type_subscription,
                item_name,
                payment_status,
                next_payment_date,
                row_number() over (partition by user_id order by payment_date desc) as row
                FROM users_payments.payments
                WHERE payment_status = '{PaymentStatus.aprobado.value}' and payment_type != '{PaymentType.pago_unico.value}'
            ), last_payment_per_user as (
                select *
                from payments
                where row = 1
            )
            SELECT
                us.user_id,
                us.users_subscription_status,
                p.next_payment_date,
                p.type_subscription
            FROM huntys_management.users_subscriptions us
                INNER JOIN last_payment_per_user p ON us.user_id = p.user_id
            WHERE us.users_subscription_status != '{PaymentStatus.rechazado.value}' and us.user_id='{user_id}'
            """
        ).first()

    finally:
        db.close()


def update_users_subscriptions(user_id: str, updated_payment: UsersSubscriptions):
    """
    Actualiza un registro de pago en la base de datos según el payment_id proporcionado.
    db (Session): Sesión de la base de datos (obtenida mediante dependencia).

    Args:
        user_id (int): El ID del pago a actualizar.
        updated_payment (Payment): Objeto Payment que contiene los datos actualizados para el pago.


    Raises:
        HTTPException: Si el pago con el payment_id especificado no existe en la base de datos.
        HTTPException: Si ocurre un error al confirmar la transacción en la base de datos.
        HTTPException: Si ocurre un error al refrescar el objeto Payment desde la base de datos.

    Returns:
        Payment: El objeto Payment actualizado.
    """
    try:
        users_subscriptions = read_users_subscriptions(user_id)
        if not users_subscriptions:
            raise HTTPException(
                status_code=404,
                detail="Payment with the specified ID does not exist in the database",
            )
        for key, value in updated_payment.dict(exclude_unset=True).items():
            setattr(users_subscriptions, key, value)

        db.add(users_subscriptions)
        db.commit()
        db.refresh(users_subscriptions)
        return users_subscriptions
    finally:
        db.close()
