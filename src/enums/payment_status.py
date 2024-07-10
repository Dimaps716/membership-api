import enum


class PaymentStatus(enum.Enum):
    aprobado = "Aprobado"
    rechazado = "Rechazado"


class PaymentType(enum.Enum):
    pago_unico = "pago_unico"
