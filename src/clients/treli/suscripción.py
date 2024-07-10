import logging

import requests
from fastapi import HTTPException, status

from settings import Settings


def create_subscription(
    email: str = None,
    billing_address: dict = None,
    shipping_address: dict = None,
    payment: dict = None,
):
    """
    Crea una suscripción.

    :param email: Correo electrónico de tu cliente.
    :type email: str
    :param billing_address: Dirección de facturación de tu cliente.
    :type billing_address: dict
    :param shipping_address: Dirección de envío de tu cliente.
    :type shipping_address: dict
    :param payment: Información del pago de la suscripción.
    :type payment: dict
    :return: El código de estado de la respuesta.
    """
    method = create_subscription.__name__
    try:
        url = f"{Settings.TRELI_URL_BASE}subscriptions/create"
        headers = {
            "accept": Settings.APPLICATION_JSON,
            "content-type": Settings.APPLICATION_JSON,
            "Authorization": f"Basic {Settings.USER_TRELI_AUTHENTICATION}",
        }

        data = {
            "email": email,
            "billing_address": billing_address,
            "shipping_address": shipping_address,
            "payment": payment,
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


def update_subscription(
    subscription_id: int = None,
    email: str = None,
    billing_address: dict = None,
    shipping_address: dict = None,
    payment: dict = None,
):
    """
    Actualiza una suscripción.

    :param subscription_id: Id de la suscripción que quieres actualizar.
    :type subscription_id: int
    :param email: Correo electrónico de tu cliente.
    :type email: str
    :param billing_address: Dirección de facturación de tu cliente.
    :type billing_address: dict
    :param shipping_address: Dirección de envío de tu cliente.
    :type shipping_address: dict
    :param payment: Información del pago de la suscripción.
    :type payment: dict
    :return: El código de estado de la respuesta.
    """
    method = update_subscription.__name__
    try:
        url = f"{Settings.TRELI_URL_BASE}subscriptions/update"
        headers = {
            "accept": Settings.APPLICATION_JSON,
            "content-type": Settings.APPLICATION_JSON,
            "Authorization": f"Basic {Settings.USER_TRELI_AUTHENTICATION}",
        }

        data = {
            "subscription_id": subscription_id,
            "email": email,
            "billing_address": billing_address,
            "shipping_address": shipping_address,
            "payment": payment,
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


def list_subscriptions(
    email: str = None,
    date_created: str = None,
    date_range: str = None,
    status_subscription: str = None,
    subscription_id: int = None,
):
    """
    Obtiene una lista de suscripciones con posibles filtros.

    :param email: Obtén una lista de las suscripciones asociadas a un correo.
    :type email: str
    :param date_created: Obtén una lista de las suscripciones creadas en una fecha específica.
    :type date_created: str
    :param date_range: Obtén una lista de las suscripciones creadas en un rango de fechas.
    :type date_range: str
    :param status_subscription: Obtén una lista de las suscripciones con un estado específico.
                   Posibles estados: "active", "paused", "cancelled", "dunning", "in validation", "on hold", "intent".
    :type status_subscription: str
    :param subscription_id: Obtén el detalle de una suscripción específica. Este filtro sobrescribe cualquier filtro enviado anteriormente.
    :type subscription_id: int
    :return: El resultado de la respuesta en formato JSON.
    """
    method = list_subscriptions.__name__
    try:
        url = f"{Settings.TRELI_URL_BASE}subscriptions/list"
        headers = {
            "accept": Settings.APPLICATION_JSON,
            "Authorization": f"Basic {Settings.USER_TRELI_AUTHENTICATION}",
        }

        params = {
            "email": email,
            "date_created": date_created,
            "date_range": date_range,
            "status": status_subscription,
            "subscription_id": subscription_id,
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


def view_subscription(subscription_id: int = None):
    """
    Ver el detalle de la suscripción de un cliente.

    :param subscription_id: Id de la suscripción que quieres ver.
    :type subscription_id: int
    :return: El resultado de la respuesta en formato JSON.
    """
    method = view_subscription.__name__
    try:
        url = f"{Settings.TRELI_URL_BASE}subscriptions/view"
        headers = {
            "accept": Settings.APPLICATION_JSON,
            "content-type": Settings.APPLICATION_JSON,
            "Authorization": f"Basic {Settings.USER_TRELI_AUTHENTICATION}",
        }

        data = {"subscription_id": subscription_id}

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:
        logging.error(f"{method} error {error}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"{method} error: {error}",
        )


def subscription_action(subscription_id: int = None, action: str = None):
    """
    Pausar, cancelar o reactivar la suscripción de un cliente.

    :param subscription_id: Id de la suscripción sobre la que quieres hacer una acción.
    :type subscription_id: int
    :param action: Para pausar una suscripción - "pause".
                   Para activar una suscripción - "activate".
                   Para cancelar una suscripción - "cancel".
    :type action: str
    :return: El resultado de la respuesta en formato JSON.
    """
    method = subscription_action.__name__

    try:
        url = f"{Settings.TRELI_URL_BASE}subscriptions/actions"
        headers = {
            "accept": Settings.APPLICATION_JSON,
            "content-type": Settings.APPLICATION_JSON,
            "Authorization": f"Basic {Settings.USER_TRELI_AUTHENTICATION}",
        }

        data = {"subscription_id": subscription_id, "action": action}

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:
        logging.error(f"{method} error {error}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"{method} error: {error}",
        )


def report_subscription_usage(
    subscription_id: int = None,
    process_renewal: bool = False,
    usage_report: list = None,
):
    """
    Reportar el uso de una suscripción.

    :param subscription_id: Id de la suscripción a la cual le quieres reportar el uso.
    :type subscription_id: int
    :param process_renewal: Decide si quieres reportar uso únicamente o reportar uso y procesar la renovación.
                            False para únicamente reportar uso. True para reportar uso y procesar la renovación.
                            Valor por defecto, False.
    :type process_renewal: bool
    :param usage_report: Lista de items dentro de la suscripción a los cuales le estás reportando el uso.
    :type usage_report: list
    :return: El resultado de la respuesta en formato JSON.
    """
    method = report_subscription_usage.__name__

    try:
        url = f"{Settings.TRELI_URL_BASE}subscriptions/report-usage"
        headers = {
            "accept": Settings.APPLICATION_JSON,
            "content-type": Settings.APPLICATION_JSON,
            "Authorization": f"Basic {Settings.USER_TRELI_AUTHENTICATION}",
        }

        data = {
            "subscription_id": subscription_id,
            "process_renewal": process_renewal,
            "usage_report": usage_report,
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
