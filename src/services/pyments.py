import logging

from fastapi import HTTPException, status

from models.payment.payment import Payment
from repositories.payments import create_payment, read_payment


def create_payment_db(payment: Payment) -> Payment:
    """
    Crea un registro de pago en la base de datos.

    Esta función toma un objeto Pago como entrada y crea un nuevo registro de pago en la base de datos.
    Si ya existe un pago con el mismo ID en la base de datos, se levanta una excepción HTTP 404.
    Si ocurre cualquier otro error inesperado durante el proceso de creación, se levanta una excepción HTTP 500.

    Args:
        payment (Pago): El objeto Pago que representa el nuevo pago a ser creado.

    Returns:
        Pago: El objeto Pago recién creado.

    Raises:
        HTTPException: Si ya existe un pago con el mismo ID en la base de datos.
                       El código de estado será 404 (No Encontrado) y el detalle especificará
                       "Ya existe un pago con el mismo ID en la base de datos".
        HTTPException: Si ocurre un error inesperado durante el proceso de creación.
                       El código de estado será 500 (Error Interno del Servidor) y el detalle
                       proporcionará información sobre el error inesperado.
    """
    try:
        db_payment = create_payment(payment)
        return db_payment

    except HTTPException:
        # Reraise HTTPException with more specific detail
        raise

    except Exception as ex:
        logging.error(f"create_payment_db: {ex}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Unexpected error occurred during payment creation.",
        )


def read_payment_db(
    treli_payment_id: int = None, user_id: str = None, query: bool = None
) -> Payment:
    """
    Recuperar un pago de la base de datos.

    Esta función toma como entrada el identificador del pago (payment_id) y recupera el registro de pago
    correspondiente desde la base de datos. Si el pago con el ID especificado no se encuentra en la base de datos,
    se levanta una excepción HTTP 404. Si ocurre algún otro error inesperado durante el proceso de recuperación,

    Args:
        treli_payment_id (int): El ID del pago que se desea recuperar de la base de datos.
        user_id (str): El ID del usuario que se desea recuperar de la base de datos.
        query (bool)

    Returns:
        Payment: El objeto Pago recuperado desde la base de datos.

    Raises:
        HTTPException: Si el pago con el ID especificado no se encuentra en la base de datos.
                       El código de estado será 404 (No Encontrado), y el detalle especificará
                       "Pago no encontrado en la base de datos".
        HTTPException: Si ocurre un error inesperado durante el proceso de recuperación.
                       El código de estado será 500 (Error Interno del Servidor), y el detalle
                       proporcionará información sobre el error inesperado.
    """
    try:
        db_obj = read_payment(treli_payment_id, user_id)

        if query:
            return db_obj

        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found in the database",
            )
        return db_obj

    except HTTPException:
        # Reraise HTTPException with more specific detail
        raise

    except Exception as ex:
        logging.error(f"read_payment_db: {ex}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Unexpected error occurred during payment retrieval.",
        )
