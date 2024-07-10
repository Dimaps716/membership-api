import base64
import logging
from datetime import datetime

from dateutil.relativedelta import relativedelta
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from clients import api_user_master, historic_status, hubspot, thinkific
from enums import status_user
from schema.pyments.payment import Payment, Subscriptions
from services import (
    create_user,
    hunty_profile,
    pyments,
    user_master,
    user_subscriptions,
)
from settings import Settings
from utils.list_product import plazos


def next_payment_date(product_name, date_latest):
    """
    Agrega un plazo específico a la fecha actual dependiendo del nombre del producto.

    Args:
        product_name (str): El nombre del producto.
        date_latest (str): La fecha actual en formato 'YYYY-MM-DD' o un timestamp Unix.

    Returns:
        str: La nueva fecha resultante después de agregar el plazo, en formato 'YYYY-MM-DD'.

    Nota:
        Los nombres de producto compatibles y sus plazos asociados se definen en el diccionario 'plazos'.
        Si el 'nombre_producto' no coincide con ninguno de los productos definidos, no se realizará ningún cambio.

    """
    # Si la fecha_actual es un timestamp Unix, conviértela a formato de fecha legible.
    if isinstance(date_latest, int):
        date_latest = datetime.utcfromtimestamp(date_latest)

    plazo = plazos.get(product_name, 0)
    if plazo > 0:
        nueva_fecha = date_latest + relativedelta(months=plazo)
        return nueva_fecha

    return date_latest


def create_or_update_user(payment):
    """
    Crea o actualiza un usuario basado en la información del pago.

    Args:
        payment (dict): Un diccionario que contiene la información del pago.

    Returns:
        str: El ID del usuario creado o actualizado.

    Raises:
        UserNotFound: Si el usuario no se encuentra en la base de datos.

    Nota:
        Esta función asume la existencia de los siguientes módulos o funciones:
        - `user_master`: Módulo que maneja la base de datos de usuarios.
        - `create_user`: Función para crear un nuevo usuario en la base de datos.
        - `api_user_master`: Módulo que maneja las actualizaciones de estado de usuarios.
        - `status_user`: Enumeración que define los posibles estados y subestados del usuario.
    """

    billing = payment["content"]["billing"]
    items = payment["content"]["items"][0]

    contact_properties_payment_approved = {
        "user_type": "hunty pro",
        "active_huntypro": True,
        "subscription_name": items["name"],
        "ambiente": Settings.SCOPE,
    }
    contact_properties_payment_failed = {
        "user_type": "Hunty",
        "active_huntypro": False,
        "subscription_name": "subscription canceled",
        "ambiente": Settings.SCOPE,
    }

    def get_user_status(event_type, profile_exists):
        if event_type == "payment_approved":
            if profile_exists:
                return {
                    "status_id": status_user.Status.active.value,
                    "substatus_id": status_user.SubStatus.hunty_pro.value,
                    "stage_id": status_user.StageId.active_subscription,
                }
            else:
                return {
                    "status_id": status_user.Status.registered.value,
                    "substatus_id": status_user.SubStatus.application_form.value,
                    "stage_id": status_user.StageId.alternate_form_hunty_pro,
                }
        else:
            if profile_exists:
                return {
                    "status_id": status_user.Status.active.value,
                    "substatus_id": status_user.SubStatus.free.value,
                    "stage_id": status_user.StageId.failed_payment,
                }
            else:
                return {
                    "status_id": status_user.Status.registered.value,
                    "substatus_id": status_user.SubStatus.application_form.value,
                    "stage_id": status_user.StageId.failed_payment,
                }

    get_user = user_master.read_user_db(email=billing["email"], query=True)

    if not get_user:
        create_user_db = create_user.create_user(billing)
        user_id = create_user_db["user_id"]
        user_status = get_user_status(payment["event_type"], False)

        if payment["event_type"] == "payment_approved":
            create_or_update_user_hubspot(
                billing=billing, user_id=user_id, items=items["name"]
            )

    else:
        user_id = get_user.user_id
        profile = hunty_profile.read_user_profile_db(user_id=user_id, query=True)
        user_status = get_user_status(payment["event_type"], bool(profile))

        if payment["event_type"] == "payment_approved":
            contact_properties = contact_properties_payment_approved
        else:
            contact_properties = contact_properties_payment_failed
        create_or_update_user_hubspot(
            billing=billing, user_id=user_id, data=contact_properties
        )
    old_status = user_master.read_user_db(user_id=user_id, query=True)

    api_user_master.update_user_master(user_id=user_id, data=user_status)
    old_status = jsonable_encoder(old_status)
    if old_status["substatus_id"] != user_status["substatus_id"]:
        historic_status.create_modify_data(old_status, now_status=user_status)
    api_user_master.patch_real_time_db_status(
        user_id=user_id, show_modal=True, show_hubspot_banner=True, show_banner=True
    )

    return user_id


def create_or_update_payment(payment, user_id):
    """
    Crea o actualiza un registro de pago en la base de datos.

    Args:
        payment (dict): Un diccionario que contiene la información del pago.
        user_id (str): El ID del usuario asociado con el pago.

    Raises:
        None
    """
    content = payment["content"]
    totals = content["totals"]
    items = content["items"][0]
    user_payment = {
        "treli_payment_id": content["payment_id"],
        "item_name": items["name"],
        "user_id": user_id,
        "payment_type": content["payment_type"],
        "payment_status": content["payment_status"],
        "payment_method": content["payment_method"],
        "payment_currency": content["currency"],
        "subtotal_payment_amount": totals["sub_total"],
        "discounts_amount": totals["discounts"],
        "total_payment_amount": totals["total"],
        "next_payment_date": next_payment_date(
            product_name=items["name"], date_latest=payment["occurred_at"]
        ),
        "payment_date": datetime.utcfromtimestamp(payment["occurred_at"]),
        "created_date": datetime.utcfromtimestamp(payment["occurred_at"]),
        "update_date": datetime.utcfromtimestamp(payment["occurred_at"]),
    }

    user_subscription_id = pyments.create_payment_db(Payment(**user_payment))

    get_user_subscription_id = user_subscriptions.read_users_subscriptions_db(
        user_id=user_subscription_id.user_id,
        query=True,
    )

    user_subscription_data = {
        "payment_id": user_subscription_id.payment_id,
        "user_id": user_subscription_id.user_id,
        "users_subscription_status": content["payment_status"],
        "payment_date": datetime.utcfromtimestamp(payment["occurred_at"]),
        "created_date": datetime.utcfromtimestamp(payment["occurred_at"]),
    }

    if not get_user_subscription_id:
        user_subscriptions.create_users_subscriptions_db(
            payment=Subscriptions(**user_subscription_data)
        )
    else:
        user_subscriptions.update_users_subscriptions(
            user_id=user_subscription_id.user_id,
            updated_payment=Subscriptions(**user_subscription_data),
        )
    return user_payment, user_subscription_data


def process_payment(payment: dict):
    """
    Procesa un pago, creando o actualizando registros de pago y usuario en la base de datos.

    Args:
        payment (dict): Un diccionario que contiene la información del pago.

    Returns:
        dict: Un diccionario con la información del pago procesado.

    Raises:
        UserNotFound: Si el usuario no se encuentra en la base de datos.
        HTTPException: Si ocurre un error al crear el registro histórico de pago.

    Nota:
        Esta función asume la existencia de los siguientes módulos o funciones:
        - `user_master`: Módulo que maneja la base de datos de usuarios.
        - `create_user`: Función para crear un nuevo usuario en la base de datos.
        - `api_user_master`: Módulo que maneja las actualizaciones de estado de usuarios.
        - `pyments`: Módulo que maneja la base de datos de pagos.
        - `Payment`: Clase que representa un registro de pago.
        - `historical_payments`: Módulo que maneja la base de datos de registros históricos de pago.
        - `HistoricalPayment`: Clase que representa un registro histórico de pago.
        - `status_user`: Enumeración que define los posibles estados y subestados del usuario.
        - `jsonable_encoder`: Una función para convertir datos a formato JSON.

    Nota:
        El diccionario 'pago' debe incluir un campo adicional 'approved' que indique si el pago fue aprobado
        (True para pagos aprobados, False para pagos fallidos).
    """
    try:
        user_id = create_or_update_user(payment)
        user_payment = create_or_update_payment(payment, user_id)

    except HTTPException:
        # Reraise HTTPException with more specific detail
        raise

    except Exception as ex:
        logging.error(f"Error occurred during payment creation: {ex}")
        """
        Si ocurre un error durante la creación del pago
        actualiza el estado del usuario si existe.
        """
        billing = payment["content"]["billing"]
        get_user = user_master.read_user_db(email=billing["email"], query=True)
        if get_user:
            substatus_id = get_user.status_id
            if substatus_id == "f5eaac978aab4071819528431afa79f0":
                user_status = {
                    "status_id": status_user.Status.active.value,
                    "substatus_id": status_user.SubStatus.free.value,
                    "stage_id": status_user.StageId.failed_payment,
                }
                api_user_master.update_user_master(
                    user_id=get_user.user_id, data=user_status
                )

        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Error occurred during payment creation.",
        )

    try:
        if payment["event_type"] == "payment_approved" and Settings.MACHINE != "DEV":
            get_user = user_master.read_user_db(user_id=user_id, query=True)
            thinkific.create_user_with_enrollments_user(
                first_name=get_user.first_name,
                last_name=get_user.last_name,
                email=get_user.email,
            )

        return user_payment, user_id

    except HTTPException:
        # Reraise HTTPException with more specific detail
        raise

    except Exception as ex:
        logging.error(f"Error occurred during payment creation: {ex}")


def create_or_update_user_hubspot(billing, user_id, data=None, items=None):
    """
    Crea un nuevo usuario en HubSpot o actualiza un usuario existente con la información proporcionada.

    Args:
        billing (dict): Un diccionario que contiene la información de facturación del usuario.
        user_id (str): El ID del usuario que se desea asociar en HubSpot.
        data (dict): Un diccionario que contiene la información
        items(str):  contiene la información del tipo de subscription

    Raises:
        HTTPException: Si ocurre algún error durante la creación o actualización del usuario en HubSpot.

    Returns:
        None
    """
    try:
        if not data:
            formatted_phone = f"{billing['phone_country_code']} {billing['phone']}"
            email = billing["email"].encode("ascii")
            email_encode = base64.b64encode(email).decode("ascii")
            contact_properties = {
                "user_id": user_id,
                "city": billing["city"],
                "country": billing["country"],
                "user_type": "hunty pro",
                "firstname": billing["first_name"],
                "lastname": billing["last_name"],
                "phone": str(formatted_phone),
                "email": billing["email"],
                "account_key": email_encode,
                "subscription_name": items,
                "active_huntypro": True,
                "ambiente": Settings.SCOPE,
            }
        else:
            contact_properties = data

        get_user_hubspot = hubspot.get_single_hunty_by_email(email=billing["email"])

        if type(get_user_hubspot) is tuple:
            hubspot.update_user_hubspot(
                data=contact_properties, hubspot_id=get_user_hubspot[0].get("vid")
            )
        else:
            hubspot.create_user_hubspot(contact_properties)

    except Exception as ex:
        logging.error(
            f"Error en la creación o actualización del usuario en HubSpot: {ex}"
        )
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Error en la creación o actualización del usuario en HubSpot.",
        )
