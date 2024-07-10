import logging
from datetime import datetime

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from clients import api_user_master, historic_status
from enums import status_user
from schema.pyments.payment import Subscriptions
from services import user_master, user_subscriptions
from services.process_payment import create_or_update_user_hubspot
from settings import Settings


def subscription(payment: dict):
    """
    Process a subscription payment and update user status accordingly.

    Args:
        payment (dict): Payment information containing customer and other details.

    Returns:
        Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]: A tuple containing updated
        user master data, real-time database data, and payment details.

    Raises:
        HTTPException: If an error occurs during processing the subscription payment.
    """

    try:
        billing = payment["content"]["customer"]

        get_user = user_master.read_user_db(email=billing["email"], query=True)

        if not get_user:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail="Error user not exist",
            )
        else:
            user_id = get_user.user_id

            old_status = user_master.read_user_db(user_id=user_id, query=True)
            old_status = jsonable_encoder(old_status)

            user_status = {
                "status_id": status_user.Status.active.value,
                "substatus_id": status_user.SubStatus.free.value,
                "stage_id": status_user.StageId.subscription_cancelled,
            }

            user_master_data = api_user_master.update_user_master(
                user_id=user_id, data=user_status
            )
            if old_status["substatus_id"] != user_status["substatus_id"]:
                historic_status.create_modify_data(old_status, now_status=user_status)

            api_user_master.patch_real_time_db_status(
                user_id=user_id,
                show_modal=True,
                show_hubspot_banner=True,
                show_banner=True,
            )

            user_subscription_data = {
                "users_subscription_status": "subscription canceled",
                "update_date": datetime.utcfromtimestamp(payment["occurred_at"]),
            }

            update_data = user_subscriptions.update_users_subscriptions(
                user_id=user_id,
                updated_payment=Subscriptions(**user_subscription_data),
            )

            contact_properties = {
                "user_type": "Hunty",
                "active_huntypro": False,
                "subscription_name": "subscription canceled",
                "ambiente": Settings.SCOPE,
            }

            create_or_update_user_hubspot(
                billing=billing, user_id=user_id, data=contact_properties
            )

            return user_master_data, update_data

    except Exception as ex:
        logging.error(f"Error: Failed to process subscription {ex}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Error: Failed to process subscription payment",
        )
