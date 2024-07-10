from fastapi import APIRouter, status

from clients.treli import suscripción
from services.user_subscriptions import read_user_status_subscription

router = APIRouter(tags=["Treli Suscripcion"])


@router.post("/create_subscription/")
def create_subscription_endpoint(
    email: str = None,
    billing_address: dict = None,
    shipping_address: dict = None,
    payment: dict = None,
):
    """
    Crea una nueva suscripción para un cliente con la información proporcionada.

    Parameters:
        email (str): Correo electrónico del cliente para el que se crea la suscripción.
        billing_address (dict, optional): Información de la dirección de facturación del cliente en formato de diccionario.
        shipping_address (dict, optional): Información de la dirección de envío del cliente en formato de diccionario.
        payment (dict, optional): Información de pago para la suscripción en formato de diccionario.
                                  El diccionario debe contener la información necesaria para realizar el pago.
                                  Por ejemplo:
                                  {
                                      "gateway": "paypal",
                                      "card_number": "1234-5678-9012-3456",
                                      "expiry_date": "12/25",
                                      "cvv": "123",
                                      "amount": 29.99,
                                      "currency": "USD"
                                  }

    Returns:
        dict: Un diccionario que contiene el resultado de la operación.
              El diccionario puede contener las siguientes claves:
              - 'success' (bool): Un indicador que indica si la operación fue exitosa o no.
              - 'subscription_id' (str): El identificador único de la suscripción creada.
              - 'message' (str): Un mensaje descriptivo que indica el resultado de la operación.
              - Otras claves adicionales en caso de ser necesario.

    Raises:
        HTTPException: Si ocurre algún error durante la operación, se lanzará una excepción con el código de error adecuado.

    Example:
        Un ejemplo de solicitud POST a '/create_subscription/' podría ser:

        {
            "email": "cliente@example.com",
            "billing_address": {
                "street": "123 Main St",
                "city": "Ciudad Ejemplo",
                "country": "País Ejemplo"
            },
            "shipping_address": {
                "street": "456 Shipping St",
                "city": "Ciudad Envío",
                "country": "País Envío"
            },
            "payment": {
                "gateway": "paypal",
                "card_number": "1234-5678-9012-3456",
                "expiry_date": "12/25",
                "cvv": "123",
                "amount": 29.99,
                "currency": "USD"
            }
        }

        Si la operación es exitosa, la respuesta podría ser:

        {
            'success': True,
            'subscription_id': 'ABC123XYZ',
            'message': 'Suscripción creada exitosamente.'
        }
    """
    return suscripción.create_subscription(
        email=email,
        billing_address=billing_address,
        shipping_address=shipping_address,
        payment=payment,
    )


@router.post("/update_subscription/")
def update_subscription_endpoint(
    subscription_id: int = None,
    email: str = None,
    billing_address: dict = None,
    shipping_address: dict = None,
    payment: dict = None,
):
    """
    Actualiza una suscripción existente con la información proporcionada.

    Parameters:
        subscription_id (int): El identificador único de la suscripción que se desea actualizar.
        email (str, optional): Nuevo correo electrónico del cliente asociado a la suscripción.
        billing_address (dict, optional): Nueva información de la dirección de facturación del cliente en formato de diccionario.
        shipping_address (dict, optional): Nueva información de la dirección de envío del cliente en formato de diccionario.
        payment (dict, optional): Nueva información de pago para la suscripción en formato de diccionario.
                                  El diccionario debe contener la información necesaria para realizar el pago.
                                  Por ejemplo:
                                  {
                                      "gateway": "paypal",
                                      "card_number": "1234-5678-9012-3456",
                                      "expiry_date": "12/25",
                                      "cvv": "123",
                                      "amount": 29.99,
                                      "currency": "USD"
                                  }

    Returns:
        dict: Un diccionario que contiene el resultado de la operación.
              El diccionario puede contener las siguientes claves:
              - 'success' (bool): Un indicador que indica si la operación fue exitosa o no.
              - 'message' (str): Un mensaje descriptivo que indica el resultado de la operación.
              - Otras claves adicionales en caso de ser necesario.

    Raises:
        HTTPException: Si ocurre algún error durante la operación, se lanzará una excepción con el código de error adecuado.

    Example:
        Un ejemplo de solicitud POST a '/update_subscription/' podría ser:

        {
            "subscription_id": 12345,
            "email": "nuevo_email@example.com",
            "billing_address": {
                "street": "456 New Billing St",
                "city": "Ciudad Facturación Nueva",
                "country": "País Facturación Nuevo"
            },
            "shipping_address": {
                "street": "789 New Shipping St",
                "city": "Ciudad Envío Nueva",
                "country": "País Envío Nuevo"
            },
            "payment": {
                "gateway": "stripe",
                "card_number": "9876-5432-1234-5678",
                "expiry_date": "01/30",
                "cvv": "456",
                "amount": 39.99,
                "currency": "USD"
            }
        }

        Si la operación es exitosa, la respuesta podría ser:

        {
            'success': True,
            'message': 'Suscripción actualizada exitosamente.'
        }
    """
    return suscripción.update_subscription(
        subscription_id=subscription_id,
        email=email,
        billing_address=billing_address,
        shipping_address=shipping_address,
        payment=payment,
    )


@router.get("/list_subscriptions/")
def list_subscriptions_endpoint(
    email: str = None,
    date_created: str = None,
    date_range: str = None,
    status_subscription: str = None,
    subscription_id: int = None,
):
    """
    Obtiene una lista de suscripciones filtrada por diferentes criterios.

    Parameters:
        email (str, optional): Correo electrónico del cliente asociado a las suscripciones.
        date_created (str, optional): Fecha de creación de las suscripciones en formato 'YYYY-MM-DD'.
        date_range (str, optional): Rango de fechas en el que se crearon las suscripciones en formato 'YYYY-MM-DD,YYYY-MM-DD'.
        status (str, optional): Estado de las suscripciones (por ejemplo, 'active', 'inactive', etc.).
        subscription_id (int, optional): Identificador único de una suscripción específica.

    Returns:
        dict: Un diccionario que contiene el resultado de la operación.
              El diccionario puede contener las siguientes claves:
              - 'success' (bool): Un indicador que indica si la operación fue exitosa o no.
              - 'subscriptions' (list): Una lista de suscripciones que cumplen con los criterios de búsqueda.
              - 'message' (str): Un mensaje descriptivo que indica el resultado de la operación.
              - Otras claves adicionales en caso de ser necesario.

    Raises:
        HTTPException: Si ocurre algún error durante la operación, se lanzará una excepción con el código de error adecuado.

    Example:
        Un ejemplo de solicitud GET a '/list_subscriptions/' podría ser:

        /list_subscriptions/?email=cliente@example.com&status=active

        Si la operación es exitosa y hay suscripciones que cumplen con los criterios de búsqueda, la respuesta podría ser:

        {
            'success': True,
            'subscriptions': [
                {
                    'subscription_id': 12345,
                    'email': 'cliente@example.com',
                    'status': 'active',
                    'date_created': '2023-07-21'
                },
                {
                    'subscription_id': 67890,
                    'email': 'cliente@example.com',
                    'status': 'active',
                    'date_created': '2023-07-19'
                }
            ],
            'message': 'Lista de suscripciones obtenida exitosamente.'
        }

        Si no hay suscripciones que cumplan con los criterios de búsqueda, la respuesta podría ser:

        {
            'success': True,
            'subscriptions': [],
            'message': 'No se encontraron suscripciones con los criterios de búsqueda proporcionados.'
        }
    """
    return suscripción.list_subscriptions(
        email=email,
        date_created=date_created,
        date_range=date_range,
        status_subscription=status_subscription,
        subscription_id=subscription_id,
    )


@router.get(
    "/user/{user_id}/subscription",
    tags=["User_master"],
    status_code=status.HTTP_200_OK,
    summary="get hunty data subscription",
)
def get_data_suscription(user_id: str):
    """
    GET hunty data suscription

    Args:
        user_id (str): User ID

    Returns:
        dict: Users data subscription
    """
    return read_user_status_subscription(user_id)


@router.post("/view_subscription/")
def view_subscription_endpoint(subscription_id: int = None):
    """
    Obtiene información detallada de una suscripción específica.

    Parameters:
        subscription_id (int): El identificador único de la suscripción que se desea obtener información detallada.

    Returns:
        dict: Un diccionario que contiene el resultado de la operación.
              El diccionario puede contener las siguientes claves:
              - 'success' (bool): Un indicador que indica si la operación fue exitosa o no.
              - 'subscription' (dict): Un diccionario que contiene información detallada de la suscripción.
                                       El diccionario puede contener campos como 'subscription_id', 'email',
                                       'status', 'billing_address', 'shipping_address', 'payment', etc.
              - 'message' (str): Un mensaje descriptivo que indica el resultado de la operación.
              - Otras claves adicionales en caso de ser necesario.

    Raises:
        HTTPException: Si ocurre algún error durante la operación, se lanzará una excepción con el código de error adecuado.

    Example:
        Un ejemplo de solicitud POST a '/view_subscription/' podría ser:

        {
            "subscription_id": 12345
        }

        Si la operación es exitosa y se encuentra la suscripción con el subscription_id proporcionado, la respuesta podría ser:

        {
            'success': True,
            'subscription': {
                'subscription_id': 12345,
                'email': 'cliente@example.com',
                'status': 'active',
                'billing_address': {
                    'street': '123 Main St',
                    'city': 'Ciudad Ejemplo',
                    'country': 'País Ejemplo'
                },
                'shipping_address': {
                    'street': '456 Shipping St',
                    'city': 'Ciudad Envío',
                    'country': 'País Envío'
                },
                'payment': {
                    'gateway': 'paypal',
                    'card_number': '1234-5678-9012-3456',
                    'expiry_date': '12/25',
                    'cvv': '123',
                    'amount': 29.99,
                    'currency': 'USD'
                }
            },
            'message': 'Información de suscripción obtenida exitosamente.'
        }

        Si no se encuentra la suscripción con el subscription_id proporcionado, la respuesta podría ser:

        {
            'success': True,
            'subscription': None,
            'message': 'No se encontró ninguna suscripción con el subscription_id proporcionado.'
        }
    """
    return suscripción.view_subscription(subscription_id=subscription_id)


@router.post("/subscription_action/")
def subscription_action_endpoint(subscription_id: int = None, action: str = None):
    """
    Realiza una acción específica en una suscripción.

    Parameters:
        subscription_id (int): El identificador único de la suscripción en la que se realizará la acción.
        action (str): La acción que se desea realizar en la suscripción (por ejemplo, 'cancel', 'pause', 'resume', etc.).

    Returns:
        dict: Un diccionario que contiene el resultado de la operación.
              El diccionario puede contener las siguientes claves:
              - 'success' (bool): Un indicador que indica si la operación fue exitosa o no.
              - 'message' (str): Un mensaje descriptivo que indica el resultado de la operación.
              - Otras claves adicionales en caso de ser necesario.

    Raises:
        HTTPException: Si ocurre algún error durante la operación, se lanzará una excepción con el código de error adecuado.

    Example:
        Un ejemplo de solicitud POST a '/subscription_action/' podría ser:

        {
            "subscription_id": 12345,
            "action": "cancel"
        }

        Si la operación es exitosa y se pudo cancelar la suscripción con el subscription_id proporcionado, la respuesta podría ser:

        {
            'success': True,
            'message': 'La suscripción ha sido cancelada exitosamente.'
        }

        Si se proporciona una acción no válida o la suscripción no puede ser cancelada por alguna razón, la respuesta podría ser:

        {
            'success': False,
            'message': 'No se pudo realizar la acción solicitada en la suscripción.'
        }
    """
    return suscripción.subscription_action(
        subscription_id=subscription_id, action=action
    )


@router.post("/report_subscription_usage/")
def report_subscription_usage_endpoint(
    subscription_id: int = None,
    process_renewal: bool = False,
    usage_report: list = None,
):
    """
    Reporta el uso de una suscripción y opcionalmente procesa la renovación de la suscripción.

    Parameters:
        subscription_id (int): El identificador único de la suscripción para la que se reportará el uso.
        process_renewal (bool, optional): Un indicador que determina si se debe procesar la renovación de la suscripción
                                          después de reportar el uso. Por defecto, es False y no se procesará la renovación.
        usage_report (list, optional): Una lista que contiene el reporte de uso de la suscripción. Cada elemento de la lista
                                       debe ser un diccionario con los siguientes campos:
                                       - 'item_id' (int): El identificador único del artículo o producto utilizado.
                                       - 'quantity' (int): La cantidad utilizada del artículo.

    Returns:
        dict: Un diccionario que contiene el resultado de la operación.
              El diccionario puede contener las siguientes claves:
              - 'success' (bool): Un indicador que indica si la operación fue exitosa o no.
              - 'message' (str): Un mensaje descriptivo que indica el resultado de la operación.
              - Otras claves adicionales en caso de ser necesario.

    Raises:
        HTTPException: Si ocurre algún error durante la operación, se lanzará una excepción con el código de error adecuado.

    Example:
        Un ejemplo de solicitud POST a '/report_subscription_usage/' podría ser:

        {
            "subscription_id": 12345,
            "process_renewal": True,
            "usage_report": [
                {"item_id": 1, "quantity": 3},
                {"item_id": 2, "quantity": 1}
            ]
        }

        Si la operación es exitosa y se pudo reportar el uso de la suscripción, la respuesta podría ser:

        {
            'success': True,
            'message': 'Uso de suscripción reportado exitosamente. La renovación será procesada.'
        }

        Si no se proporciona el usage_report o la suscripción no pudo ser actualizada por alguna razón, la respuesta podría ser:

        {
            'success': False,
            'message': 'No se pudo reportar el uso de la suscripción.'
        }
    """
    return suscripción.report_subscription_usage(
        subscription_id=subscription_id,
        process_renewal=process_renewal,
        usage_report=usage_report,
    )
