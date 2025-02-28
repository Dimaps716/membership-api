import os

import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

Base = declarative_base()

load_dotenv()


def create_session(return_engine=False) -> Session:
    """
    Crea una sesión de base de datos y retorna una instancia de sesión.

    Esta función configura y crea una sesión de base de datos para interactuar con la base
    de datos PostgreSQL. Dependiendo del entorno ("DEV" o Cloud Run), utiliza diferentes
    configuraciones de conexión. Si `return_engine` es `True`, la función retorna la instancia
    del motor de base de datos en lugar de la sesión.

    Args:
        return_engine (bool, opcional): Si es `True`, retorna la instancia del motor.

    Returns:
        Session or Engine: Una instancia de sesión de SQLAlchemy o del motor de base de datos.

    """
    connection_name = os.getenv("DB_CONNECTION_NAME")
    db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
    db_name = os.getenv("DB_NAME")
    username = os.getenv("DB_USER_USERNAME")
    password = os.getenv("DB_USER_PASS")
    db_port = os.getenv("DB_PORT")
    db_host = os.getenv("DB_HOST", "127.0.0.1")

    if os.getenv("MACHINE") == "DEV":
        # SQL Instance for Local machine
        engine = create_engine(
            # Equivalent URL:
            # postgresql+pg8000://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
            sqlalchemy.engine.url.URL(
                drivername="postgresql+pg8000",
                username=username,  # e.g. "my-database-user"
                password=password,  # e.g. "my-database-password"
                host=db_host,  # e.g. "127.0.0.1"
                port=db_port,  # e.g. 5432
                database=db_name,  # e.g. "my-database-name",
                # connect_args={"timeout": 30},
            ),
            poolclass=NullPool,
        )
    else:
        # SQL Instance for Cloud Run
        engine = create_engine(
            # Equivalent URL:
            # postgresql+pg8000://<db_user>:<db_pass>@/<db_name>
            #                         ?unix_sock=<socket_path>/<cloud_sql_instance_name>/.s.PGSQL.5432
            sqlalchemy.engine.url.URL.create(
                drivername="postgresql+pg8000",
                username=username,  # e.g. "my-database-user"
                password=password,  # e.g. "my-database-password"
                database=db_name,  # e.g. "my-database-name"
                query={
                    "unix_sock": "{}/{}/.s.PGSQL.5432".format(
                        db_socket_dir, connection_name  # e.g. "/cloudsql"
                    )  # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
                },
            ),
            poolclass=NullPool,
        )

    if return_engine:
        return engine
    # Connect and create session
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    return session
