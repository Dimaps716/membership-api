from fastapi import APIRouter

from clients.treli import pasarelas

router = APIRouter(tags=["Treli Pasarelas"])


@router.get("/get_payment_gateways/")
def get_payment_gateways_endpoint():
    """
    Obtiene la lista de pasarelas de pago disponibles.

    Returns:
        dict: Un diccionario que contiene el resultado de la operación.
                El diccionario puede contener las siguientes claves:
                - 'success' (bool): Un indicador que indica si la operación fue exitosa o no.
                - 'payment_gateways' (list): Una lista de pasarelas de pago disponibles.
                - 'message' (str): Un mensaje descriptivo que indica el resultado de la operación.
                - Otras claves adicionales en caso de ser necesario.

    Raises:
        HTTPException: Si ocurre algún error durante la operación, se lanzará una excepción con el código de error adecuado.

    Example:
        Un ejemplo de solicitud GET a '/get_payment_gateways/' podría ser:

        /get_payment_gateways/

        Si la operación es exitosa y hay pasarelas de pago disponibles, la respuesta podría ser:

        {
            'success': True,
            'payment_gateways': [
                {
                    'gateway_id': 1,
                    'name': 'Pasarela 1',
                    'description': 'Esta es la primera pasarela de pago.'
                },
                {
                    'gateway_id': 2,
                    'name': 'Pasarela 2',
                    'description': 'Esta es otra pasarela de pago con características adicionales.'
                }
            ],
            'message': 'Pasarelas de pago obtenidas exitosamente.'
        }

        Si no hay pasarelas de pago disponibles, la respuesta podría ser:

        {
            'success': True,
            'payment_gateways': [],
            'message': 'No hay pasarelas de pago disponibles en el momento.'
        }
    """
    return pasarelas.get_payment_gateways()
