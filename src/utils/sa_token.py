import json
import logging

import google.auth.transport.requests
import google.oauth2.id_token
import requests
from fastapi import HTTPException, status

from settings import Settings

settings = Settings()


def generate_sa_token(service_audience):
    """
    It takes a service audience as an argument, and returns a JWT token

    :param service_audience: The URL of the service you want to access
    :return: A JWT token
    """

    try:
        if settings.MACHINE == "DEV":
            if service_audience is None:
                service_audience = settings.BASE_URL
            body = {"audience": service_audience}

            response = requests.post(
                f"{settings.BASE_URL}/pilot/api/any/token",
                data=json.dumps(body),
            )
            response = json.loads(response.json())

            return response["JWT"]

        else:
            # GC Run URL
            auth_req = google.auth.transport.requests.Request()
            id_token = google.oauth2.id_token.fetch_id_token(
                auth_req, service_audience + "/"
            )

            return id_token

    except Exception as e:
        logging.error(f"generate_sa_token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="service account authentication failed",
        )
