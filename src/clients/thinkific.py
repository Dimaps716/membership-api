import threading
from datetime import datetime
import logging

import requests
from fastapi import HTTPException, status

from settings import Settings

from utils.list_courses import lista_name_courses

create_user_url = Settings.CREATE_USER_THINKIFIC
get_courses_url = Settings.GET_COURSES_THINKIFIC
enrollment_url = Settings.ENROLLMENT_USER_THINKIFIC

headers = {
    "X-Auth-API-Key": Settings.API_KEY_THINKIFIC,
    "X-Auth-Subdomain": Settings.SUBDOMAIN,
    "Content-Type": "application/json",
}


def create_user_and_send_email(first_name, last_name, email):
    """
    Crea un usuario y envía un correo electrónico.

    Esta función crea un usuario utilizando los datos proporcionados y luego envía un correo
    electrónico de bienvenida. Si ocurre algún error durante el proceso, se registrará en
    los registros y se levantará una excepción HTTP.

    Args:
        first_name (str): Nombre del usuario.
        last_name (str): Apellido del usuario.
        email (str): Dirección de correo electrónico del usuario.

    Returns:
        str: ID del usuario creado.

    Raises:
        HTTPException: Si ocurre un error durante la creación del usuario o el envío del correo.

    """
    method = create_user_and_send_email.__name__
    try:
        # Crea el usuario
        user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "send_welcome_email": True,
            "provider": "SSO",
        }

        response = requests.post(create_user_url, headers=headers, json=user_data)

        if response.status_code == 422:
            return response.status_code

        response.raise_for_status()

        return response.json()["id"]
    except Exception as error:
        logging.info(f"Error when execute method {method}, with exception: {error}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error when execute method {method}, with exception: {error}",
        )


def get_courses():
    """
    Obtiene una lista de IDs de cursos según una lista de nombres de cursos.

    Esta función obtiene una lista de IDs de cursos que coinciden con los nombres
    de cursos proporcionados en la lista `lista_name_courses`. Los cursos se obtienen
    de la URL `get_courses_url` utilizando paginación. Si ocurre algún error durante
    el proceso, se registrará en los registros y se levantará una excepción HTTP.

    Returns:
        list: Lista de IDs de cursos.

    Raises:
        HTTPException: Si ocurre un error al obtener los cursos.

    """
    method = get_courses.__name__
    try:
        lista_courses = [item["id"] for item in lista_name_courses]
        params = {"limit": 30}
        page = 1
        courses_ids = []
        while True:
            params["page"] = page
            response = requests.get(get_courses_url, headers=headers, params=params)
            response.raise_for_status()
            courses = response.json()["items"]
            courses_ids.extend((course["id"], course["name"]) for course in courses)

            # Verifica si hay más páginas
            if not response.json()["meta"]["pagination"]["next_page"]:
                break
            page += 1

        response.raise_for_status()

        ids_courses = [item[0] for item in courses_ids if item[0] in lista_courses]

        return ids_courses

    except Exception as error:
        logging.info(f"Error when execute method {method}, with exception: {error}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error when execute method {method}, with exception: {error}",
        )


def enroll_user(
    course_id,
    user_id,
):
    """
    Inscribe a un usuario en un curso.

    Esta función inscribe a un usuario en un curso específico utilizando los IDs
    proporcionados para el curso y el usuario. La inscripción se registra con la
    fecha y hora actual en formato UTC. Si ocurre algún error durante el proceso,
    se registrará en los registros y se levantará una excepción HTTP.

    Args:
        course_id (str): ID del curso al que se inscribirá el usuario.
        user_id (str): ID del usuario que será inscrito en el curso.

    Returns:
        int: Código de estado de la respuesta de la solicitud.

    Raises:
        HTTPException: Si ocurre un error al inscribir al usuario en el curso.

    """
    method = get_courses.__name__
    try:
        now = datetime.utcnow()
        formatted_date_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")

        enrollment_data = {
            "user_id": user_id,
            "course_id": course_id,
            "activated_at": formatted_date_time,
        }

        response = requests.post(enrollment_url, headers=headers, json=enrollment_data)
        response.raise_for_status()

        return response.status_code

    except Exception as error:
        logging.info(f"Error when execute method {method}, with exception: {error}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error when execute method {method}, with exception: {error}",
        )


def create_user_with_enrollments_user(first_name, last_name, email):
    """
    Crea un usuario y lo inscribe en cursos.

    Esta función crea un usuario utilizando los datos proporcionados y luego lo inscribe
    en varios cursos utilizando la función `enroll_user`. Si el usuario ya existe, devuelve
    un detalle de "usuario existente" con un código de estado 202. Si ocurre algún error
    durante el proceso, se registrará en los registros y se levantará una excepción HTTP.

    Args:
        first_name (str): Nombre del usuario.
        last_name (str): Apellido del usuario.
        email (str): Dirección de correo electrónico del usuario.

    Returns:
        HTTPException: Una excepción HTTP con el código de estado adecuado.

    Raises:
        HTTPException: Si ocurre un error al crear el usuario o inscribirlo en cursos.

    """
    method = create_user_with_enrollments_user.__name__
    try:
        user_id = create_user_and_send_email(first_name, last_name, email)

        if user_id == 422:
            return HTTPException(
                status_code=status.HTTP_202_ACCEPTED, detail="the user exists"
            )

        found_id = get_courses()
        threads = []
        for course_id in found_id:
            thread = threading.Thread(target=enroll_user, args=(course_id, user_id))
            thread.start()
            threads.append(thread)

        # Esperar a que todos los hilos terminen
        for thread in threads:
            thread.join()

        return HTTPException(status_code=status.HTTP_201_CREATED)

    except Exception as error:
        logging.info(f"Error when execute method {method}, with exception: {error}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error when execute method {method}, with exception: {error}",
        )
