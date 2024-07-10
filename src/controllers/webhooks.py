from fastapi import APIRouter, BackgroundTasks

from services import process_payment, process_subscription
from utils.list_product import plazos
from utils.webhooks_example import schema_extra

router = APIRouter(tags=["Treli webhooks"])


@router.post("/treli/webhooks")
async def treli_webhooks(
    background_tasks: BackgroundTasks, payment: dict = schema_extra, test: bool = None
):
    """
    Procesa los webhooks enviados por Treli.

    Esta función toma una lista de datos (webhooks) enviados por Treli y agrega una tarea a la cola de background_tasks
    para procesar los eventos asincrónicamente.

    Parameters:
        payment (dict): datos que contiene los webhooks enviados por Treli.
        background_tasks (BackgroundTasks): Una instancia de la clase BackgroundTasks que permite agregar tareas a la cola
                                            de procesamiento en segundo plano.
        test

    Returns:
        str: Un mensaje de confirmación de que los webhooks han sido recibidos y se procesarán asincrónicamente.

    Example:
        Un ejemplo de solicitud POST a '/treli/webhooks' podría ser:

        [
            {
                "event_type": "payment_approved",
                "data": {
                    "payment_id": 12345,
                    "amount": 29.99,
                    "status": "approved"
                }
            },
            {
                "event_type": "payment_pending",
                "data": {
                    "payment_id": 67890,
                    "amount": 19.99,
                    "status": "pending"
                }
            }
        ]

        Si se reciben webhooks con eventos de pago aprobados y pendientes, se agregarán las tareas a la cola de background_tasks
        para procesarlos asincrónicamente y la respuesta será:

        "Los webhooks han sido recibidos y se procesarán asincrónicamente."

    Note:
        Esta función asume que los webhooks enviados por Treli tienen la estructura adecuada. Se recomienda verificar la
        documentación de Treli para asegurarse de que los datos recibidos sean los esperados.
    """
    relevant_events = {"payment_approved", "payment_failed"}
    event_type = payment.get("event_type")
    product_name = (
        payment.get("content", {})
        .get("items", [{}])[0]
        .get("name", "Nombre del producto no encontrado")
    )

    if event_type in relevant_events and product_name in plazos:
        if test:
            result = process_payment.process_payment(payment)
        else:
            background_tasks.add_task(process_payment.process_payment, payment)
            result = "Los webhooks han sido recibidos y se procesarán asincrónicamente."
    else:
        if test:
            result = process_subscription.subscription(payment)
        else:
            background_tasks.add_task(process_subscription.subscription(payment))
            result = "Los webhooks han sido recibidos y se procesarán asincrónicamente."

    if result is not None:
        return result
    else:
        return "Los webhooks han sido recibidos pero no se encontraron eventos relevantes para procesar."
