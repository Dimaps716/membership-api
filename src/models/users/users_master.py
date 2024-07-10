from sqlalchemy import (
    ARRAY,
    JSON,
    TIMESTAMP,
    Boolean,
    Column,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from repositories.database import Base


class UsersMaster(Base):
    """
    Modelo de usuario principal.

    Esta clase define el modelo principal de usuario correspondiente a la tabla "users_master"
    en el esquema "users". Contiene campos que almacenan información esencial sobre los usuarios,
    como ID de usuario, tipo de usuario, nombre, dirección, información de contacto, etc.

    Atributos:
        id (int): ID único del usuario (clave primaria).
        user_id (str): ID único del usuario.
        location_id (int): ID de ubicación del usuario.
        user_id_bubble (str): ID de usuario en Bubble.
        user_type_id (int): ID de tipo de usuario.
        user_subtype_id (int): ID de subtipo de usuario.
        ... (otros atributos)

    """

    __tablename__ = "users_master"

    __table_args__ = {"schema": "users"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(70), primary_key=True, index=True)
    location_id = Column(Integer)
    user_id_bubble = Column(String(70))
    user_type_id = Column(Integer)
    user_subtype_id = Column(Integer)
    status_id = Column(String(70))
    substatus_id = Column(String(70))
    stage_id = Column(String(70))
    type_identification_id = Column(Integer)
    first_name = Column(String(150))
    last_name = Column(String(150))
    birthday_date = Column(TIMESTAMP(timezone=False), nullable=True, default=None)
    identity_document = Column(String(50))
    country_phone_code_id = Column(Integer)
    phone_number = Column(Numeric)
    email = Column(String(255))
    confirm_email = Column(Boolean, default=False)
    image_link = Column(Text())
    address = Column(String(255))
    zip_code = Column(String(20))
    country_id = Column(Integer)
    hubspot_id = Column(Integer)
    other_identification = Column(ARRAY(JSON))
    load_date = Column(TIMESTAMP(timezone=False))
    update_date = Column(TIMESTAMP(timezone=False))
    Payment = relationship("Payment")
