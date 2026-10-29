import socket
import random
import time
from protocol import encode_message, decode_message

def send_reliably(address, payload, seq=1, timeout=0.5, max_retries=3, sock=None):
    """
    Si sock es None --> own vale True: la función tendrá que crear y cerrar su propio socket.
    Si se recibió un socket como argumento --> own vale False: el socket pertenece a quien llamó a la función.
    """
    # TODO 1: crear socket solo si sock es None.
    if (sock is None):
        sock = socket.socket()
        puerto = random.uniform(50000, 100000)
        sock.bind(address, puerto)
    # TODO 2: enviar DATA con seq y payload.
    #udp_packet = IP(dst=address)/UDP(dport=puerto, sport=5000)/Raw(load=payload + seq)
    #udp_packet.show() # Inspeccionamos el paquete antes de mandarlo
    # Mandamos el paquete
    #send(udp_packet)
    # TODO 3: esperar ACK de la misma secuencia.
    sock.bind('').listen(1)
    
    # TODO 4: retransmitir al vencer timeout, hasta max_retries.
    while(max_retries >0):
        time.sleep(timeout)
        max_retries-= max_retries
    # TODO 5: ignorar mensajes inválidos y ACK incorrectos.
    
    # TODO 6: cerrar solo el socket creado por esta función.
    
    pass
