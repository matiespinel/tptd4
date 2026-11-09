import socket
import random
import time
from protocol import encode_message, decode_message

def send_reliably(address, payload, seq=1, timeout=0.5, max_retries=3, sock=None, simulate_loss=None):
    """
    Si sock es None --> own vale True: la función tendrá que crear y cerrar su propio socket.
    Si se recibió un socket como argumento --> own vale False: el socket pertenece a quien llamó a la función.
    """
    
    own = False
    if sock is None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        own = True

    sock.settimeout(timeout)

    # Adjuntamos el número de secuencia al payload para que el servidor lo reconozca
    message = {
        "seq": seq,
        **payload
    }
    data_packet = encode_message(message)

    success = False
    attempts = 0

    while attempts <= max_retries:
        try:
            # SIMULACIÓN DE PÉRDIDA DE DATA:
            # Si se solicita simular pérdida de data y es el primer intento (attempts == 0)
            if simulate_loss == "data" and attempts == 0:
                print(f"[SIMULACIÓN] Paquete DATA (seq={seq}) descartado intencionalmente (pérdida simulada).")
                # No enviamos el paquete, forzando el timeout en recvfrom()
            else:
                sock.sendto(data_packet, address)
            
            while True:
                response_bytes, _ = sock.recvfrom(1024)
                response_data = decode_message(response_bytes)
                
                # Verificamos que sea un diccionario y responda a la misma secuencia
                if response_data and response_data.get("seq") == seq:
                    success = True
                    # el num de seq es el correcto, podemos salir del bucle interno y del externo
                    break #salimos del bucle interno
                else:
                    continue
                    
            if success:
                break #salimos del bucle exeterno
                
        except socket.timeout:
            attempts += 1
            print(f"Timeout esperando ACK para seq {seq}. Reintentando ({attempts}/{max_retries})...")
    # Si se creó el socket dentro de esta función, cerrarlo al final
    if own:
        sock.close()

    return success #si no se recibió ACK después de max_retries, devolvemos False. Si se recibió, devolvemos True.

