import socket
from protocol import encode_message, decode_message

def send_reliably(address, payload, seq=1, timeout=0.5, max_retries=3, sock=None):
    """
    Si sock es None --> own vale True: la función tendrá que crear y cerrar su propio socket.
    Si se recibió un socket como argumento --> own vale False: el socket pertenece a quien llamó a la función.
    """
    own = sock is None 

    # TODO 1: crear socket solo si sock es None.
    
    # TODO 2: enviar DATA con seq y payload.
    # TODO 3: esperar ACK de la misma secuencia.
    # TODO 4: retransmitir al vencer timeout, hasta max_retries.
    # TODO 5: ignorar mensajes inválidos y ACK incorrectos.
    # TODO 6: cerrar solo el socket creado por esta función.
    pass
