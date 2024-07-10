import logging

import requests
from fastapi import HTTPException, status

from settings import Settings


def get_plans(plan_id: int = None):
    """
    Obtiene una lista de todos tus planes o el detalle de uno específico.

    :param plan_id: Id del plan que quieres obtener. Dejar vacío para obtener todos tus planes.
    :type plan_id: int
    :return: El resultado de la respuesta en formato JSON.
    """
    method = get_plans.__name__
    try:
        url = f"{Settings.TRELI_URL_BASE}api/plans"
        headers = {
            "accept": Settings.APPLICATION_JSON,
            "Authorization": f"Basic {Settings.USER_TRELI_AUTHENTICATION}",
        }

        params = {"id": plan_id}

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:
        logging.error(f"{method} error {error}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"{method} error: {error}",
        )


def create_plan(
    name: str = None,
    description: str = None,
    sku: str = None,
    trackqty: bool = False,
    inventory: int = None,
    stockstatus: str = None,
    image_url: str = None,
    productstatus: str = None,
    product_type: str = None,
    subs_plans: list = None,
):
    """
    Crea un plan.

    :param name: Nombre del plan.
    :type name: str
    :param description: Descripción del plan.
    :type description: str
    :param sku: SKU/ID del plan.
    :type sku: str
    :param trackqty: Decide si quieres activar la gestión y seguimiento de inventario para este plan.
    :type trackqty: bool
    :param inventory: Número de unidades disponibles para este plan. Solo tiene efecto si activaste la gestión y seguimiento de inventario.
    :type inventory: int
    :param stockstatus: Si no hay gestión y seguimiento de inventario, puedes definir si este plan está disponible o agotado.
                        "instock" para disponible, "outofstock" para agotado.
    :type stockstatus: str
    :param image_url: URL de la imagen para este plan. Posibles extensiones jpg, jpeg, gif y png.
    :type image_url: str
    :param productstatus: Define el estado del plan. "active", "draft" o "private".
    :type productstatus: str
    :param product_type: Define el tipo de plan. "subsproduct" para un producto recurrente, "membership" para una membresía o "service" para un servicio recurrente.
    :type product_type: str
    :param subs_plans: Lista de planes de suscripción del plan.
    :type subs_plans: list
    :return: El resultado de la respuesta en formato JSON.
    """
    method = create_plan.__name__
    try:
        url = f"{Settings.TRELI_URL_BASE}plans/create"
        headers = {
            "accept": Settings.APPLICATION_JSON,
            "content-type": Settings.APPLICATION_JSON,
            "Authorization": f"Basic {Settings.USER_TRELI_AUTHENTICATION}",
        }

        data = {
            "name": name,
            "description": description,
            "sku": sku,
            "trackqty": trackqty,
            "inventory": inventory,
            "stockstatus": stockstatus,
            "image_url": image_url,
            "productstatus": productstatus,
            "product_type": product_type,
            "subs_plans": subs_plans,
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


def update_plan(
    plan_id: int = None, subscription_plan_id: int = None, subs_plan: dict = None
):
    """
    Actualiza un plan de suscripción de un plan.

    :param plan_id: Id del plan. Lo puedes obtener consultando el endpoint "Listar planes".
    :type plan_id: int
    :param subscription_plan_id: Id del plan de suscripción. Si tus planes solo tienen un plan de suscripción, puedes enviar este valor como "0".
                                 Si tus planes tienen varios planes de suscripción, puedes consultar el endpoint "Listar planes" para obtener el id del plan de suscripción que quieres actualizar.
    :type subscription_plan_id: int
    :param subs_plan: Lista de planes de suscripción del plan.
    :type subs_plan: dict
    :return: El resultado de la respuesta en formato JSON.
    """
    method = update_plan.__name__
    try:
        url = f"{Settings.TRELI_URL_BASE}plans/update"
        headers = {
            "accept": Settings.APPLICATION_JSON,
            "content-type": Settings.APPLICATION_JSON,
            "Authorization": f"Basic {Settings.USER_TRELI_AUTHENTICATION}",
        }

        data = {
            "id": plan_id,
            "subscription_plan_id": subscription_plan_id,
            "subs_plan": subs_plan,
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
