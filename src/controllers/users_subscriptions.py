from fastapi import APIRouter

from schema.pyments.payment import Subscriptions
from services.user_subscriptions import (
    create_users_subscriptions_db,
    read_users_subscriptions_db,
    update_users_subscriptions_db,
)

router = APIRouter(tags=["Users subscriptions"])


@router.post("/users_subscriptions/", response_model=Subscriptions)
def create_users_subscriptions(payment: Subscriptions):
    """
    Crea un nuevo registro de pago histórico en la base de datos.

    Parámetros:
    - payment (UsersSubscriptions): Un objeto que contiene los detalles del pago histórico a crear.
                                   Debe ser una instancia de la clase `HistoricalPayment`.

    Respuesta:
    - UsersSubscriptions: Un objeto que contiene el resultado de la creación del pago histórico.
                                 En caso de éxito, el objeto puede contener un mensaje de éxito y el
                                 pago histórico creado.

    Ejemplo de respuesta en caso de éxito:
    ```json
    {
        "message": "Registro de pago histórico creado exitosamente.",
        "created_historical_payment": {

        }
    }
    ```

    Ejemplo de respuesta en caso de error:
    ```json
    {
        "message": "Error al crear el registro de pago histórico.",
        "status_code": 424
    }
    ```
    """
    return create_users_subscriptions_db(payment)


@router.get("/users_subscriptions/payment_id", response_model=Subscriptions)
def read_users_subscriptions(payment_id: int = None):
    """
    Obtiene información histórica de pagos según el ID del pago y/o el ID del usuario.

    Esta función permite obtener información histórica de pagos de la base de datos utilizando
    el ID del pago y/o el ID del usuario como criterios de búsqueda.

    Parámetros:
    - payment_id (int, opcional): El ID del pago que se desea buscar. Debe ser un valor entero positivo.

    Returns:
    - HistoricalPayment: Un objeto que contiene los registros de pagos históricos que coinciden
                         con los criterios de búsqueda. Cada registro de pago histórico es representado
                         por un objeto con sus detalles.
    """
    return read_users_subscriptions_db(payment_id)


@router.put("/users_subscriptions/user_id", response_model=Subscriptions)
def update_users_subscriptions(user_id: str, updated_payment: Subscriptions):
    """
    Actualiza las suscripciones de un usuario en la base de datos.

    Esta función permite actualizar las suscripciones de un usuario en la base de datos.
    Se utiliza el ID del usuario para identificar al usuario cuyas suscripciones se van a actualizar.
    Se proporciona la información actualizada de suscripción mediante el objeto `updated_payment`.

    Parámetros:
    - user_id (str): El identificador único del usuario.
    - updated_payment (Subscriptions): El objeto que contiene los detalles de las suscripciones actualizadas.

    Returns:
    - Subscriptions: El objeto que representa las suscripciones actualizadas después de la actualización.

    Ejemplo de uso:
        Puedes enviar una solicitud PUT a /users_subscriptions/{user_id} para actualizar las suscripciones
        de un usuario específico. Debes proporcionar el ID del usuario en la URL y los detalles actualizados
        de suscripción en el cuerpo de la solicitud.

    Respuestas:
        - 200 OK: Si las suscripciones se han actualizado correctamente. Se devuelve el objeto Subscriptions
                  con los detalles actualizados.
        - 404 Not Found: Si el usuario con el user_id proporcionado no existe en la base de datos.
    """
    return update_users_subscriptions_db(user_id, updated_payment)
