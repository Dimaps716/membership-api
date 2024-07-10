import base64
import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    MACHINE = os.getenv("MACHINE")

    if MACHINE == "GCP":
        ROOT_PATH = "/membership"
    else:
        ROOT_PATH = ""

    ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS")
    ALLOW_CREDENTIALS = os.getenv("ALLOW_CREDENTIALS")
    ALLOW_METHODS = os.getenv("ALLOW_METHODS")
    ALLOW_HEADERS = os.getenv("ALLOW_HEADERS")

    # Treli
    TRELI_URL_BASE = os.getenv("TRELI_URL_BASE")
    TRELI_API_KEY = os.getenv("TRELI_API_KEY")
    APPLICATION_JSON = "application/json"
    USERNAME = "HuntyPro"
    SCOPE = os.getenv("SCOPE")
    USER_TRELI = f"{USERNAME}:{TRELI_API_KEY}".encode("ascii")
    USER_TRELI_AUTHENTICATION = base64.b64encode(USER_TRELI).decode("ascii")

    BASE_URL = os.getenv("BASE_URL")
    USER_MASTER = f"{BASE_URL}user/master"
    USERS_RAW_URL = os.getenv("USERS_RAW_URL")
    USER_MASTER_UPDATE = f"{USER_MASTER}/update"
    # auth api
    AUTH_ROLE = f"{BASE_URL}auth"
    PASSWORD = os.getenv("PASSWORD")
    ALGORITHM = os.getenv("ALGORITHM")

    # THINKIFIC
    API_KEY_THINKIFIC = os.getenv("API_KEY_THINKIFIC")
    URL_BASE_THINKIFIC = os.getenv("URL_BASE_THINKIFIC")
    CREATE_USER_THINKIFIC = f"{URL_BASE_THINKIFIC}/users"
    GET_COURSES_THINKIFIC = f"{URL_BASE_THINKIFIC}/courses"
    ENROLLMENT_USER_THINKIFIC = f"{URL_BASE_THINKIFIC}/enrollments"
    SUBDOMAIN = "huntyacademy"

    # HUBSPOT
    HUBSPOT_URL = os.getenv("HUBSPOT_URL")
    HUBSPOT_URL_V3 = os.getenv("HUBSPOT_URL_V3")
    HUBSPOT_CONTACT_URL = f"{HUBSPOT_URL}contact"
    HUBSPOT_EMAIL_URL = f"{HUBSPOT_CONTACT_URL}/email"
    HUBSPOT_PROFILE = "profile?"
    HUBSPOT_ACCESS_TOKEN = os.getenv("HUBSPOT_ACCESS_TOKEN")
