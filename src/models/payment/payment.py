from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, TIMESTAMP
from repositories.database import Base


class Payment(Base):
    """
    Modelo para la tabla "payments" en el esquema "users_payments".

    Atributos:
        id_payments (int): Clave primaria autoincremental para los registros de pagos.
        treli_payment_id (float): ID del pago, debe ser único en la tabla.
        item_name (str): Descripción de la suscripción asociada al pago.
        user_id (str): ID del usuario relacionado con el pago, opcional.
        payment_type (str): Tipo de pago realizado (tarjeta de crédito, efectivo, etc.).
        payment_status (str): Estado actual del pago (pendiente, completado, etc.).
        payment_method (str): Método utilizado para realizar el pago (PayPal, tarjeta de crédito, etc.).
        payment_currency (str): Moneda utilizada para el pago (USD, EUR, etc.).
        subtotal_payment_amount (str): Monto del pago antes de aplicar descuentos, en formato de cadena.
        discounts_amount (str): Monto de descuentos aplicados al pago, en formato de cadena.
        total_payment_amount (str): Monto total del pago después de aplicar descuentos, en formato de cadena.
        next_payment_date (datetime): Fecha y hora del próximo pago, en formato de timestamp (sin zona horaria).
        payment_date (datetime): Fecha y hora en que se realizó el pago, en formato de timestamp (sin zona horaria).
        created_date (datetime): Fecha y hora de creación del registro, en formato de timestamp (sin zona horaria).
        update_date (datetime): Fecha y hora de la última actualización del registro, en formato de timestamp (sin zona horaria).
    """

    __tablename__ = "payments"

    __table_args__ = {"schema": "users_payments"}

    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    treli_payment_id = Column(
        Numeric,
        unique=True,
    )
    item_name = Column(String)
    user_id = Column(
        String(70), ForeignKey("users.users_master.user_id"), nullable=True
    )
    payment_type = Column(String)
    payment_status = Column(String)
    payment_method = Column(String)
    payment_currency = Column(String)
    subtotal_payment_amount = Column(String)
    discounts_amount = Column(String)
    total_payment_amount = Column(String)
    next_payment_date = Column(TIMESTAMP(timezone=False))
    payment_date = Column(TIMESTAMP(timezone=False))
    created_date = Column(TIMESTAMP(timezone=False))
    update_date = Column(TIMESTAMP(timezone=False))
