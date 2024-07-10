from fastapi import APIRouter

from schema.pyments.payment import Payment
from services.pyments import create_payment_db, read_payment_db

router = APIRouter(tags=["Payments"])


@router.post("/payments/")
def create_payment(
    payment: Payment,
):
    """
    Crea un nuevo registro de pago en la base de datos.

    Esta función permite crear un nuevo registro de pago en la base de datos utilizando
    los datos proporcionados en el objeto `payment`.

    Parámetros:
    - payment (Payment): Un objeto que contiene los detalles del pago a crear.
                        Debe ser una instancia de la clase `Payment`.

    Returns:
    - dict: Un diccionario con el resultado de la creación del pago.
            En caso de éxito, el diccionario puede contener un mensaje de éxito y el ID del nuevo pago creado.
    """
    return create_payment_db(payment)


@router.get("/payments/payment_id/user_id")
def read_payment(payment_id: int = None, user_id: str = None):
    """
    Obtiene información de pagos según el ID del pago y/o el ID del usuario.

    Esta función permite obtener información de pagos de la base de datos utilizando
    el ID del pago y/o el ID del usuario como criterios de búsqueda.

    Parámetros:
    - payment_id (int, opcional): El ID del pago que se desea buscar. Debe ser un valor entero positivo.
    - user_id (str, opcional): El ID del usuario asociado a los pagos que se desean buscar.

    Returns:
    - list: Una lista que contiene los registros de pagos que coinciden con los criterios de búsqueda.
            Cada registro de pago es representado por un diccionario con sus detalles.
            Ejemplo de respuesta:
            [
            ```
                {
                    "id_payments": 123,
                    "payment_id": 456,
                    "subscription": "Suscripción Premium",
                    "user_id": "user123",
                    "payment_type": "Tarjeta de crédito",
                    "payment_status": "Completado",
                    "payment_method": "Visa",
                    "payment_currency": "USD",
                    "subtotal_payment_amount": "100.00",
                    "discounts_amount": "10.00",
                    "total_payment_amount": "90.00",
                    "next_payment_date": "2023-08-15 12:00:00",
                    "payment_date": "2023-07-26 15:30:00",
                    "created_date": "2023-07-25 09:45:00",
                    "update_date": "2023-07-26 10:30:00"
                },
                {
                    "id_payments": 124,
                    "payment_id": 457,
                    "subscription": "Suscripción Básica",
                    "user_id": "user123",
                    "payment_type": "Tarjeta de crédito",
                    "payment_status": "Pendiente",
                    "payment_method": "Mastercard",
                    "payment_currency": "EUR",
                    "subtotal_payment_amount": "50.00",
                    "discounts_amount": "0.00",
                    "total_payment_amount": "50.00",
                    "next_payment_date": "2023-08-05 09:00:00",
                    "payment_date": "2023-07-26 14:20:00",
                    "created_date": "2023-07-25 10:15:00",
                    "update_date": "2023-07-26 11:10:00"
                }
                ```

            ]
    """
    return read_payment_db(payment_id, user_id)
