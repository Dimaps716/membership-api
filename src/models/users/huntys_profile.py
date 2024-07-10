from sqlalchemy import (
    ARRAY,
    JSON,
    TIMESTAMP,
    VARCHAR,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)

from repositories.database import Base


class UserHunties(Base):
    """
    Modelo de usuario para la tabla user_Hunties.

    Esta clase define el modelo de usuario correspondiente a la tabla "huntys_profile"
    en el esquema "users_profile". Contiene campos que almacenan información detallada
    sobre los usuarios, como ID de usuario, área de vacante, moneda, modalidad de oficina,
    información sobre áreas y subáreas de vacantes, habilidades, idiomas, etc.

    Atributos:
        id (int): ID único del usuario (clave primaria).
        user_id (str): ID del usuario asociado (clave foránea a la tabla users_master).
        vacancy_area_id (int): ID del área de vacante.
        currency_id (int): ID de la moneda.
        office_modality_id (int): ID de la modalidad de oficina.
        ... (otros atributos)

    """

    __tablename__ = "huntys_profile"

    __table_args__ = {"schema": "users_profile"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        String(70), ForeignKey("users.users_master.user_id"), nullable=True
    )
    vacancy_area_id = Column(Integer)
    currency_id = Column(Integer)
    office_modality_id = Column(Integer)
    vacancy_area_custom = Column(String)
    vacancy_subarea_ids = Column(ARRAY(Integer))
    vacancy_subarea_custom = Column(ARRAY(VARCHAR))
    wish_role_job_ids = Column(ARRAY(Integer))
    wish_role_job_custom = Column(ARRAY(VARCHAR))
    wage_aspiration = Column(Numeric)
    current_wage = Column(Numeric)
    change_city = Column(Boolean, default=False)
    location_change_city_ids = Column(ARRAY(Integer))
    linkedin_link = Column(Text)
    employment_status = Column(Boolean, default=False)
    hard_skill_ids = Column(ARRAY(Integer))
    hard_skills_custom = Column(ARRAY(VARCHAR))
    languages_level = Column(ARRAY(JSON))
    degrees = Column(ARRAY(JSON))
    wish_enterprise = Column(ARRAY(VARCHAR))
    years_experience = Column(JSON)
    assigned_mentor = Column(String(70))
    reassigned_mentor = Column(Boolean, default=False)
    curriculum = Column(ARRAY(JSON))
    work_modality_id = Column(Integer)
    contract = Column(String)
    load_date = Column(TIMESTAMP(timezone=False))
    update_date = Column(TIMESTAMP(timezone=False))
    created_date = Column(TIMESTAMP(timezone=False))
