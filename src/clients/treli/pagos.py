import logging

import requests
from fastapi import HTTPException, status

from settings import Settings


def create_payment(
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
    Crea un pago único o una solicitud de pago asociada a una factura.

    :param email: Correo electrónico de tu cliente.
    :type email: str
    :param billing_address: Dirección de facturación de tu cliente.
    :type billing_address: dict
    :param requires_shipping: Decide si el pago tiene asociada una dirección de envío.
    :type requires_shipping: bool
    :param manual_payment: Decide si el pago debe ser completado por parte del cliente.
                           Si el pago es manual (True), este request te retorna un link de pago para que redirecciones a tu cliente.
                           Si el pago no es manual (False), debes enviar la información del método de pago.
    :type manual_payment: bool
    :param payment_collection: Decide cómo quieres que Treli realice la cobranza del pago.
                               "now" para crear un pago que debe ser pagado al instante y que Treli envíe una notificación solicitando el pago.
                               "template" para utilizar una plantilla de pago creada previamente.
                               No aplica si "manual_payment" es True o False.
    :type payment_collection: str
    :param payment_template: Si "payment_collection" es "template", debes enviar el id de la plantilla que quieres utilizar.
                             Puedes consultar tus plantillas con el endpoint "listar plantillas".
                             No aplica si "manual_payment" es True o False.
    :type payment_template: str
    :param connect_invoice_number: Ingresa el número de una factura que ya tengas creada en tu proveedor de facturación contable.
                                   Treli descargará la factura, la enviará a tu cliente en las notificaciones de solicitud de pago.
                                   Debes tener integrado un proveedor contable en tu cuenta de Treli.
    :type connect_invoice_number: str
    :param upload_invoice_number: Ingresa el número de una factura que ya tengas creada en tu proveedor de facturación contable.
                                  Úsalo cuando NO tengas integrado un proveedor contable en tu cuenta de Treli y quieras recaudar una factura.
    :type upload_invoice_number: str
    :param upload_invoice_pdf_url: Ingresa la URL del PDF de la factura que estás recaudando.
                                   Úsalo cuando NO tengas integrado un proveedor contable en tu cuenta de Treli y quieras recaudar una factura.
                                   No es necesario si ya estás enviando la cadena en base64 del PDF de la factura.
    :type upload_invoice_pdf_url: str
    :param upload_invoice_pdf_base64: Ingresa la cadena en base64 de la factura que estás recaudando.
                                      Úsalo cuando NO tengas integrado un proveedor contable en tu cuenta de Treli y quieras recaudar una factura.
                                      No es necesario si ya estás enviando la URL del PDF de la factura.
    :type upload_invoice_pdf_base64: str
    :param shipping_address: Dirección de envío de tu cliente.
    :type shipping_address: dict
    :param products: Lista de productos asociados al pago. Requerido si estás creando un pago con productos existentes en tu cuenta de Treli.
    :type products: list
    :param amount: Ingresa el valor total a pagar. Solo es necesario y válido cuando estás creando un pago sin productos.
    :type amount: int
    :param payment_info: Información del método de pago.
    :type payment_info: dict
    :param currency: Código de la moneda en tres letras (ISO 4217). Debes tener la moneda habilitada en tu cuenta de Treli.
                     Este campo es opcional, si envías este campo vacío, se utiliza la moneda base configurada en tu cuenta de Treli.
    :type currency: str
    :return: El resultado de la respuesta en formato JSON.
    """
    method = create_payment.__name__
    try:
        url = f"{Settings.TRELI_URL_BASE}payments/create"
        headers = {
            "accept": Settings.APPLICATION_JSON,
            "content-type": Settings.APPLICATION_JSON,
            "Authorization": f"Basic {Settings.USER_TRELI_AUTHENTICATION}",
        }

        data = {
            "email": email,
            "billing_address": billing_address,
            "requires_shipping": requires_shipping,
            "manual_payment": manual_payment,
            "payment_collection": payment_collection,
            "payment_template": payment_template,
            "connect_invoice_number": connect_invoice_number,
            "upload_invoice_number": upload_invoice_number,
            "upload_invoice_pdf_url": upload_invoice_pdf_url,
            "upload_invoice_pdf_base64": upload_invoice_pdf_base64,
            "shipping_address": shipping_address,
            "products": products,
            "amount": amount,
            "payment": payment_info,
            "currency": currency,
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:
        logging.error(f"{method} error {error}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"{method} error: {error}",
        )


def update_payment_status(
    payment_id: int = None, invoice_number: int = None, status_paymet: str = None
):
    """
    Cambia el estado de un pago a anulado o aprobado.

    :param payment_id: Id del pago sobre el cual quieres cambiar el estado.
    :type payment_id: int
    :param invoice_number: Número de la factura asociada al pago sobre el cual quieres cambiar el estado.
                           No aplica si ya estás utilizando "payment_id".
    :type invoice_number: int
    :param status_paymet: Para aprobar un pago - "approved". Para anular un pago - "voided"
    :type status_paymet: str
    :return: El resultado de la respuesta en formato JSON.
    """
    method = update_payment_status.__name__
    try:
        url = f"{Settings.TRELI_URL_BASE}payments/update-status"
        headers = {
            "accept": Settings.APPLICATION_JSON,
            "content-type": Settings.APPLICATION_JSON,
        }

        data = {
            "payment_id": payment_id,
            "invoice_number": invoice_number,
            "status": status_paymet,
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:
        logging.error(f"{method} error {error}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"{method} error: {error}",
        )


def get_payments(
    email=None,
    date_created=None,
    date_range=None,
    subscription_id=None,
    payment_id=None,
):
    """
    Obtiene una lista de pagos con posibles filtros.

    :param email: Obtiene una lista de los pagos asociados a un correo. Ejemplo. demo@treli.co
    :type email: str
    :param date_created: Obtiene una lista de los pagos creados en una fecha especifica. Ejemplo. 2022-11-26
    :type date_created: str
    :param date_range: Obtiene una lista de los pagos creados en un rango de fecha. Ejemplo. 2022-11-26...2022-12-26
    :type date_range: str
    :param subscription_id: Obtiene una lista de los pagos asociados a una suscripción. Este filtro sobrescribe cualquier filtro enviado anteriormente. Ejemplo. 12345
    :type subscription_id: int
    :param payment_id: Obtiene el detalle de un pago específico. Este filtro sobrescribe cualquier filtro enviado anteriormente. Ejemplo. 12345
    :type payment_id: str
    :return: El resultado de la respuesta en formato JSON.
    """
    method = get_payments.__name__

    try:
        url = f"{Settings.TRELI_URL_BASE}payments"
        headers = {
            "accept": Settings.APPLICATION_JSON,
            "Authorization": f"Basic {Settings.USER_TRELI_AUTHENTICATION}",
        }

        params = {
            "email": email,
            "date_created": date_created,
            "date_range": date_range,
            "subscription_id": subscription_id,
            "payment_id": payment_id,
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:
        logging.error(f"{method} error {error}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"{method} error: {error}",
        )


def get_payment_templates():
    """
    Obtiene una lista de tus plantillas de pago.

    :return: El resultado de la respuesta en formato JSON.
    """
    method = get_payment_templates.__name__
    try:
        url = f"{Settings.TRELI_URL_BASE}payments/templates"
        headers = {
            "accept": Settings.APPLICATION_JSON,
            "Authorization": f"Basic {Settings.USER_TRELI_AUTHENTICATION}",
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:
        logging.error(f"{method} error {error}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"{method} error: {error}",
        )
