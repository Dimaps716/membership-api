from datetime import datetime
from typing import Union

from pydantic import BaseModel, Field


class PaymentBase(BaseModel):
    treli_payment_id: Union[int, None] = Field(
        description="ID del pago (puede ser entero o nulo)"
    )
    item_name: Union[str, None] = Field(
        description="Descripción de la suscripción (puede ser string o nulo)"
    )
    user_id: Union[str, None] = Field(
        description="ID del usuario (puede ser string o nulo)"
    )
    payment_type: Union[str, None] = Field(
        description="Tipo de pago (puede ser string o nulo)"
    )
    payment_status: Union[str, None] = Field(
        description="Estado del pago (puede ser string o nulo)"
    )
    payment_method: Union[str, None] = Field(
        description="Método de pago (puede ser string o nulo)"
    )
    payment_currency: Union[str, None] = Field(
        description="Moneda del pago (puede ser string o nulo)"
    )
    subtotal_payment_amount: Union[str, None] = Field(
        description="Cantidad del pago sin descuentos (puede ser string o nulo)"
    )
    discounts_amount: Union[str, None] = Field(
        description="Cantidad de descuentos aplicados (puede ser string o nulo)"
    )
    total_payment_amount: Union[str, None] = Field(
        description="Cantidad total del pago (puede ser string o nulo)"
    )
    next_payment_date: Union[datetime, None] = Field(
        default=datetime.utcnow(),
        description="Fecha del próximo pago (puede ser fecha o nulo, se establece en la fecha y hora actual por defecto)",
    )
    payment_date: Union[datetime, None] = Field(
        default=datetime.utcnow(),
        description="Fecha del pago (puede ser fecha o nulo, se establece en la fecha y hora actual por defecto)",
    )
    created_date: Union[datetime, None] = Field(
        default=datetime.utcnow(),
        description="Fecha de creación del registro (puede ser fecha o nulo, se establece en la fecha y hora actual por defecto)",
    )


class Payment(PaymentBase):
    class Config:
        orm_mode = False


class Subscriptions(BaseModel):
    payment_id: Union[str, None] = Field()
    user_id: Union[str, None] = Field()
    users_subscription_status: Union[str, None] = Field()
    created_date: Union[datetime, None] = Field(default=datetime.utcnow())
    update_date: Union[datetime, None] = Field(default=datetime.utcnow())
