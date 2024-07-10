from fastapi import APIRouter

from clients.treli import planes

router = APIRouter(tags=["Treli planes"])


@router.get("/get_plans/")
def get_plans_endpoint(plan_id: int = None):
    """
    Obtiene una lista de planes disponibles o información detallada de un plan específico.

    Parameters:
        plan_id (int, optional): El identificador único del plan que se desea obtener información detallada.

    Returns:
        dict: Un diccionario que contiene el resultado de la operación.
              El diccionario puede contener las siguientes claves:
              - 'success' (bool): Un indicador que indica si la operación fue exitosa o no.
              - 'plans' (list/dict): Una lista de planes disponibles o información detallada de un plan específico.
              - 'message' (str): Un mensaje descriptivo que indica el resultado de la operación.
              - Otras claves adicionales en caso de ser necesario.

    Raises:
        HTTPException: Si ocurre algún error durante la operación, se lanzará una excepción con el código de error adecuado.

    Example:
        Un ejemplo de solicitud GET a '/get_plans/' podría ser:

        /get_plans/

        Si la operación es exitosa y hay planes disponibles, la respuesta podría ser:

        {
            'success': True,
            'plans': [
                {
                    'plan_id': 1,
                    'name': 'Plan básico',
                    'price': 20.0,
                    'description': 'Este es el plan básico que incluye características limitadas.'
                },
                {
                    'plan_id': 2,
                    'name': 'Plan premium',
                    'price': 50.0,
                    'description': 'Este es el plan premium con acceso completo a todas las características.'
                }
            ],
            'message': 'Lista de planes obtenida exitosamente.'
        }

        Si se proporciona el plan_id, la respuesta podría ser:

        {
            'success': True,
            'plans': {
                'plan_id': 1,
                'name': 'Plan básico',
                'price': 20.0,
                'description': 'Este es el plan básico que incluye características limitadas.'
            },
            'message': 'Información detallada del plan obtenida exitosamente.'
        }

        Si no hay planes disponibles o no se encuentra el plan con el plan_id proporcionado, la respuesta podría ser:

        {
            'success': True,
            'plans': None,
            'message': 'No se encontraron planes con los criterios de búsqueda proporcionados.'
        }
    """
    return planes.get_plans(plan_id)


@router.post("/create_plan/")
def create_plan_endpoint(
    name: str = None,
    description: str = None,
    sku: str = None,
    trackqty: bool = False,
    inventory: int = None,
    stockstatus: str = None,
    image_url: str = None,
    productstatus: str = None,
    product_type: str = None,
    subs_plans: list = None,
):
    """
    Crea un nuevo plan o producto para su venta o suscripción.

    Parameters:
        name (str): Nombre del plan o producto.
        description (str): Descripción detallada del plan o producto.
        sku (str): Número de SKU (Stock Keeping Unit) asociado al plan o producto.
        trackqty (bool): Indica si se debe realizar seguimiento del inventario del plan o producto.
        inventory (int): Cantidad disponible en el inventario para el plan o producto.
        stockstatus (str): Estado del inventario (por ejemplo, 'in_stock', 'out_of_stock', etc.).
        image_url (str): URL de la imagen del plan o producto.
        productstatus (str): Estado del plan o producto (por ejemplo, 'active', 'inactive', etc.).
        product_type (str): Tipo de plan o producto (por ejemplo, 'subscription', 'one-time-purchase', etc.).
        subs_plans (list): Lista de planes de suscripción asociados al plan o producto.

    Returns:
        dict: Un diccionario que contiene el resultado de la operación.
              El diccionario puede contener las siguientes claves:
              - 'success' (bool): Un indicador que indica si la operación fue exitosa o no.
              - 'plan_id' (int): El identificador único del plan o producto creado.
              - 'message' (str): Un mensaje descriptivo que indica el resultado de la operación.
              - Otras claves adicionales en caso de ser necesario.

    Raises:
        HTTPException: Si ocurre algún error durante la operación, se lanzará una excepción con el código de error adecuado.

    Example:
        Un ejemplo de solicitud POST a '/create_plan/' podría ser:

        {
            "name": "Plan Básico",
            "description": "Este es un plan básico de suscripción mensual.",
            "sku": "PLN-BSC-001",
            "trackqty": True,
            "inventory": 100,
            "stockstatus": "in_stock",
            "image_url": "https://example.com/images/plan_basic.png",
            "productstatus": "active",
            "product_type": "subscription",
            "subs_plans": [
                {
                    "name": "Suscripción Mensual",
                    "price": 10.0,
                    "duration": "1 month"
                },
                {
                    "name": "Suscripción Anual",
                    "price": 100.0,
                    "duration": "1 year"
                }
            ]
        }

        Si la operación es exitosa, la respuesta podría ser:

        {
            'success': True,
            'plan_id': 12345,
            'message': 'Plan creado exitosamente.'
        }
    """
    return planes.create_plan(
        name=name,
        description=description,
        sku=sku,
        trackqty=trackqty,
        inventory=inventory,
        stockstatus=stockstatus,
        image_url=image_url,
        productstatus=productstatus,
        product_type=product_type,
        subs_plans=subs_plans,
    )


@router.post("/update_plan/")
async def update_plan_endpoint(
    plan_id: int = None, subscription_plan_id: int = None, subs_plan: dict = None
):
    """
    Actualiza un plan o producto existente o sus planes de suscripción asociados.

    Parameters:
        plan_id (int, optional): El identificador único del plan o producto que se desea actualizar.
        subscription_plan_id (int, optional): El identificador único del plan de suscripción que se desea actualizar.
        subs_plan (dict, optional): Un diccionario que contiene la información actualizada del plan de suscripción.
                                    El diccionario debe contener al menos los siguientes campos:
                                    - 'name' (str): Nombre actualizado del plan de suscripción.
                                    - 'price' (float): Precio actualizado del plan de suscripción.
                                    - 'duration' (str): Duración actualizada del plan de suscripción.

    Returns:
        dict: Un diccionario que contiene el resultado de la operación.
              El diccionario puede contener las siguientes claves:
              - 'success' (bool): Un indicador que indica si la operación fue exitosa o no.
              - 'message' (str): Un mensaje descriptivo que indica el resultado de la operación.
              - Otras claves adicionales en caso de ser necesario.

    Raises:
        HTTPException: Si ocurre algún error durante la operación, se lanzará una excepción con el código de error adecuado.

    Example:
        Un ejemplo de solicitud POST a '/update_plan/' podría ser:

        {
            "plan_id": 12345,
            "subs_plan": {
                "name": "Suscripción Anual",
                "price": 100.0,
                "duration": "1 year"
            }
        }

        Si la operación es exitosa, la respuesta podría ser:

        {
            'success': True,
            'message': 'Plan actualizado exitosamente.'
        }
    """
    return planes.update_plan(
        plan_id=plan_id,
        subscription_plan_id=subscription_plan_id,
        subs_plan=subs_plan,
    )
