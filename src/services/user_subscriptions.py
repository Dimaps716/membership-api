import logging

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from models.payment.subscriptions import UsersSubscriptions
from repositories.user_subscription import (
    create_users_subscriptions,
    read_hunty_status_subscription,
    read_users_subscriptions,
    update_users_subscriptions,
)


def create_users_subscriptions_db(payment: UsersSubscriptions) -> UsersSubscriptions:
    """
    Crea un registro histórico de pago en la base de datos.

    Esta función toma un objeto HistoricalPayment como entrada y crea un nuevo registro
    histórico de pago en la base de datos. Si ocurre un error durante la creación del registro,
    se levanta una excepción HTTP 424 (Failed Dependency) con detalles del error.

    Args:
        payment (HistoricalPayment): El objeto HistoricalPayment que representa el registro histórico de pago.

    Raises:
        HTTPException: Si ocurre un error durante la creación del registro histórico de pago.
                       El estado de la respuesta será 424 (Failed Dependency) y el detalle proporcionará
                       información sobre el error.
    """
    try:
        return create_users_subscriptions(payment)

    except HTTPException:
        # Reraise HTTPException with more specific detail
        raise

    except Exception as ex:
        logging.error(f"create_historical_payment_db: {ex}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Error occurred during historical payment creation.",
        )


def read_users_subscriptions_db(user_id: str = None, query: bool = None):
    """
    Busca un pago histórico en la base de datos según el payment_id o el user_id proporcionado.

    Args:
        user_id (int): El ID del pago histórico a buscar. (Opcional)
        query (boo): (Opcional)

    Raises:
            HTTPException: Si no se encuentra el pago histórico con los parámetros proporcionados.
            HTTPException: Si ocurre un error desconocido al acceder a la base de datos.

    Returns:
            HistoricalPayment: El objeto HistoricalPayment que coincide con los criterios de búsqueda.
    """
    try:
        payment = read_users_subscriptions(user_id)

        if query:
            return payment

        if not payment:
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


def read_user_status_subscription(user_id: str):
    """
    Search the user's subscription history to see if they have an active hunty pro subscription or if they have had one and it has been cancelled.

    Args:
        user_id (str): Hunty ID

    Returns:
            Dict: Dictionary with hunty subscription status information
    """
    try:
        subscription = read_hunty_status_subscription(user_id)

        return jsonable_encoder(subscription)

    except Exception as ex:
        logging.error(f"Error processing the subscription: {ex}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"Error processing the subscription: {ex.args}",
        )


def update_users_subscriptions_db(
    user_id: str, updated_payment: UsersSubscriptions
) -> UsersSubscriptions:
    """
    Actualizar un pago en la base de datos.

    Esta función toma como entrada el identificador del pago (payment_id) y un objeto Pago actualizado,
    y actualiza el registro de pago correspondiente en la base de datos. Si el pago con el ID especificado
    no se encuentra en la base de datos, se levanta una excepción HTTP 404. Si ocurre algún otro error inesperado
    durante el proceso de actualización,

    Args:
        user_id (str): El ID del pago que se desea actualizar en la base de datos.
        updated_payment (Payment): El objeto Pago actualizado que se almacenará en la base de datos.

    Returns:
        Payment: El objeto Pago actualizado.

    Raises:
        HTTPException: Si el pago con el ID especificado no se encuentra en la base de datos.
                       El código de estado será 404 (No Encontrado), y el detalle especificará
                       "Pago con el mismo ID no existe en la base de datos".
        HTTPException: Si ocurre un error inesperado durante el proceso de actualización.
                       El código de estado será 500 (Error Interno del Servidor), y el detalle
                       proporcionará información sobre el error inesperado.
    """
    try:
        db_payment = update_users_subscriptions(
            user_id=user_id, updated_payment=updated_payment
        )
        return db_payment

    except HTTPException:
        # Reraise HTTPException with more specific detail
        raise

    except Exception as ex:
        logging.error(f"update_users_subscriptions_db: {ex}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Unexpected error occurred during users subscriptions update.",
        )
