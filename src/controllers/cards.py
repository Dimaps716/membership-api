from fastapi import APIRouter

from clients.treli import cards

router = APIRouter(tags=["Treli Cards"])


@router.post("/add_card_token/")
async def add_card_token_endpoint(gateway: str = None, token_info: dict = None):
    """
    Agrega un nuevo token de tarjeta asociado a una pasarela específica.

    Parameters:
        gateway (str): Nombre de la pasarela para la cual se desea agregar el token de tarjeta.
        token_info (dict): Un diccionario que contiene la información del token de tarjeta a agregar.
                            El diccionario debe contener al menos los siguientes campos:
                            - 'card_number' (str): Número de tarjeta (generalmente oculto parcialmente por motivos de seguridad).
                            - 'expiration_date' (str): Fecha de vencimiento de la tarjeta en formato 'MM/YY'.
                            - 'cardholder_name' (str): Nombre del titular de la tarjeta.

    Returns:
        dict: Un diccionario que contiene el resultado de la operación.
                El diccionario puede contener las siguientes claves:
                - 'success' (bool): Un indicador que indica si la operación fue exitosa o no.
                - 'message' (str): Un mensaje descriptivo que indica el resultado de la operación.
                - Otras claves adicionales en caso de ser necesario.

    Raises:
        HTTPException: Si ocurre algún error durante la operación, se lanzará una excepción con el código de error adecuado.

    Example:
        Si se hace una solicitud POST a '/add_card_token/' con los siguientes parámetros:

        gateway='pasarela1'
        token_info={
            'card_number': '************1234',
            'expiration_date': '12/25',
            'cardholder_name': 'John Doe'
        }

        La función intentará agregar el token de tarjeta proporcionado a la pasarela especificada.
        Si la operación es exitosa, la respuesta podría ser:

        {
            'success': True,
            'message': 'Token de tarjeta agregado exitosamente.'
        }
    """
    return cards.add_card_token(gateway, token_info)


@router.get("/get_tokens/")
def get_tokens_endpoint(email: str = None, gateway: str = None):
    """
    Obtiene los tokens asociados a un correo electrónico y una pasarela determinada.

    Parameters:
        email (str): Correo electrónico del usuario.
        gateway (str): Nombre de la pasarela para la cual se desean obtener los tokens.

    Returns:
        dict: Un diccionario que contiene los tokens asociados al correo electrónico y la pasarela especificada.
              El diccionario puede contener las siguientes claves:
              - 'success' (bool): Un indicador que indica si la operación fue exitosa o no.
              - 'tokens' (list): Una lista de tokens asociados al correo electrónico y la pasarela especificada.
              - 'message' (str): Un mensaje descriptivo que indica el resultado de la operación.
              - Otras claves adicionales en caso de ser necesario.

    Example:
        Si se hace una solicitud GET a '/get_tokens/' con los parámetros email='usuario@ejemplo.com'
        y gateway='pasarela1', se podría obtener la siguiente respuesta:

        {
            'success': True,
            'tokens': ['token1', 'token2'],
            'message': 'Tokens obtenidos exitosamente.'
        }
    """
    return cards.get_tokens(email, gateway)
