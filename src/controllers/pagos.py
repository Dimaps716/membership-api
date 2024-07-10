from fastapi import APIRouter

from clients.treli import pagos

router = APIRouter(tags=["Treli Pagos"])


@router.post("/create_payment/")
def create_payment_endpoint(
    email: str,
    billing_address: dict,
    requires_shipping: bool,
    manual_payment: bool = None,
    payment_collection: str = None,
    payment_template: str = None,
    connect_invoice_number: str = None,
    upload_invoice_number: str = None,
    upload_invoice_pdf_url: str = None,
    upload_invoice_pdf_base64: str = None,
    shipping_address: dict = None,
    products: list = None,
    amount: int = None,
    payment_info: dict = None,
    currency: str = None,
):
    """
    Crea un nuevo pago y procesa la información relacionada con él.

    Parameters:
        email (str): Correo electrónico del cliente para el que se crea el pago.
        billing_address (dict): Información de la dirección de facturación del cliente en formato de diccionario.
        requires_shipping (bool): Indica si el pago requiere envío de productos físicos.
        manual_payment (bool): Indica si el pago se realizará de forma manual fuera del sistema.
        payment_collection (str): Método de colección de pagos utilizado (por ejemplo, 'credit_card', 'paypal', etc.).
        payment_template (str): Plantilla personalizada utilizada para la generación del pago.
        connect_invoice_number (str): Número de factura para pagos de tipo "Connect".
        upload_invoice_number (str): Número de factura para pagos de tipo "Upload".
        upload_invoice_pdf_url (str): URL del archivo PDF de la factura para pagos de tipo "Upload".
        upload_invoice_pdf_base64 (str): Cadena Base64 del archivo PDF de la factura para pagos de tipo "Upload".
        shipping_address (dict): Información de la dirección de envío del cliente en formato de diccionario.
        products (list): Lista de productos asociados al pago, cada uno representado como un diccionario.
        amount (int): Monto total del pago.
        payment_info (dict): Información adicional relacionada con el pago en formato de diccionario.
        currency (str): Moneda utilizada para el pago (por ejemplo, 'USD', 'EUR', etc.).

    Returns:
        dict: Un diccionario que contiene el resultado de la operación.
              El diccionario puede contener las siguientes claves:
              - 'success' (bool): Un indicador que indica si la operación fue exitosa o no.
              - 'payment_id' (str): El identificador único del pago generado.
              - 'message' (str): Un mensaje descriptivo que indica el resultado de la operación.
              - Otras claves adicionales en caso de ser necesario.

    Example:
        Un ejemplo de solicitud POST a '/create_payment/' podría ser:

        {
            "email": "cliente@example.com",
            "billing_address": {
                "street": "123 Main St",
                "city": "Ciudad Ejemplo",
                "country": "País Ejemplo"
            },
            "requires_shipping": True,
            "payment_collection": "credit_card",
            "products": [
                {
                    "name": "Producto 1",
                    "price": 10
                },
                {
                    "name": "Producto 2",
                    "price": 20
                }
            ],
            "amount": 30,
            "currency": "USD"
        }

        Si la operación es exitosa, la respuesta podría ser:

        {
            'success': True,
            'payment_id': 'ABC123XYZ',
            'message': 'Pago creado exitosamente.'
        }
    """
    return pagos.create_payment(
        email=email,
        billing_address=billing_address,
        requires_shipping=requires_shipping,
        manual_payment=manual_payment,
        payment_collection=payment_collection,
        payment_template=payment_template,
        connect_invoice_number=connect_invoice_number,
        upload_invoice_number=upload_invoice_number,
        upload_invoice_pdf_url=upload_invoice_pdf_url,
        upload_invoice_pdf_base64=upload_invoice_pdf_base64,
        shipping_address=shipping_address,
        products=products,
        amount=amount,
        payment_info=payment_info,
        currency=currency,
    )


@router.post("/update_payment_status/")
def update_payment_status_endpoint(
    payment_id: int = None, invoice_number: int = None, status_paymet: str = None
):
    """
    Actualiza el estado de un pago identificado por el número de pago o el número de factura.

    Parameters:
        payment_id (int): El identificador único del pago que se desea actualizar.
        invoice_number (int): El número de factura asociado al pago que se desea actualizar.
        status_paymet (str): El nuevo estado que se desea asignar al pago (por ejemplo, 'paid', 'pending', 'failed', etc.).

    Returns:
        dict: Un diccionario que contiene el resultado de la operación.
              El diccionario puede contener las siguientes claves:
              - 'success' (bool): Un indicador que indica si la operación fue exitosa o no.
              - 'message' (str): Un mensaje descriptivo que indica el resultado de la operación.
              - Otras claves adicionales en caso de ser necesario.

    Raises:
        HTTPException: Si ocurre algún error durante la operación, se lanzará una excepción con el código de error adecuado.

    Example:
        Un ejemplo de solicitud POST a '/update_payment_status/' podría ser:

        {
            "payment_id": 12345,
            "status": "paid"
        }

        o

        {
            "invoice_number": 67890,
            "status": "pending"
        }

        Si la operación es exitosa, la respuesta podría ser:

        {
            'success': True,
            'message': 'Estado del pago actualizado exitosamente.'
        }
    """

    return pagos.update_payment_status(
        payment_id=payment_id,
        invoice_number=invoice_number,
        status_paymet=status_paymet,
    )


@router.get("/get_payments/")
def get_payments_endpoint(
    email=None,
    date_created=None,
    date_range=None,
    subscription_id=None,
    payment_id=None,
):
    """
    Obtiene una lista de pagos basados en diferentes criterios de búsqueda.

    Parameters:
        email (str): Correo electrónico asociado a los pagos que se desean obtener.
        date_created (str): Fecha de creación de los pagos en formato 'YYYY-MM-DD'.
        date_range (str): Rango de fechas en el que los pagos fueron creados, en formato 'YYYY-MM-DD to YYYY-MM-DD'.
        subscription_id (int): Identificador único de la suscripción asociada a los pagos.
        payment_id (int): Identificador único de un pago específico.

    Returns:
        dict: Un diccionario que contiene el resultado de la operación.
                El diccionario puede contener las siguientes claves:
                - 'success' (bool): Un indicador que indica si la operación fue exitosa o no.
                - 'payments' (list): Una lista de pagos que coinciden con los criterios de búsqueda.
                - 'message' (str): Un mensaje descriptivo que indica el resultado de la operación.
                - Otras claves adicionales en caso de ser necesario.

    Raises:
        HTTPException: Si ocurre algún error durante la operación, se lanzará una excepción con el código de error adecuado.

    Example:
        Un ejemplo de solicitud GET a '/get_payments/' podría ser:

        /get_payments/?email=cliente@example.com&date_created=2023-07-21

        Si la operación es exitosa y hay pagos que coinciden con los criterios de búsqueda, la respuesta podría ser:

        {
            'success': True,
            'payments': [
                {
                    'payment_id': 12345,
                    'amount': 50.0,
                    'status': 'paid',
                    'date_created': '2023-07-21',
                    'subscription_id': 9876
                },
                {
                    'payment_id': 67890,
                    'amount': 30.0,
                    'status': 'pending',
                    'date_created': '2023-07-21',
                    'subscription_id': 5432
                }
            ],
            'message': 'Pagos obtenidos exitosamente.'
        }

        Si no se encuentran pagos que coincidan con los criterios de búsqueda, la respuesta podría ser:

        {
            'success': True,
            'payments': [],
            'message': 'No se encontraron pagos con los criterios de búsqueda proporcionados.'
        }
    """
    return pagos.get_payments(
        email=email,
        date_created=date_created,
        date_range=date_range,
        subscription_id=subscription_id,
        payment_id=payment_id,
    )


@router.get("/get_payment_templates/")
def get_payment_templates_endpoint():
    """
    Obtiene la lista de plantillas de pagos disponibles.

    Returns:
        dict: Un diccionario que contiene el resultado de la operación.
                El diccionario puede contener las siguientes claves:
                - 'success' (bool): Un indicador que indica si la operación fue exitosa o no.
                - 'payment_templates' (list): Una lista de plantillas de pagos disponibles.
                - 'message' (str): Un mensaje descriptivo que indica el resultado de la operación.
                - Otras claves adicionales en caso de ser necesario.

    Raises:
        HTTPException: Si ocurre algún error durante la operación, se lanzará una excepción con el código de error adecuado.

    Example:
        Un ejemplo de solicitud GET a '/get_payment_templates/' podría ser:

        /get_payment_templates/

        Si la operación es exitosa y hay plantillas de pagos disponibles, la respuesta podría ser:

        {
            'success': True,
            'payment_templates': [
                {
                    'template_id': 1,
                    'name': 'Plantilla 1',
                    'description': 'Esta es la plantilla de pago estándar.'
                },
                {
                    'template_id': 2,
                    'name': 'Plantilla 2',
                    'description': 'Esta es otra plantilla de pago personalizada.'
                }
            ],
            'message': 'Plantillas de pagos obtenidas exitosamente.'
        }

        Si no hay plantillas de pagos disponibles, la respuesta podría ser:

        {
            'success': True,
            'payment_templates': [],
            'message': 'No hay plantillas de pagos disponibles en el momento.'
        }
    """
    return pagos.get_payment_templates()
