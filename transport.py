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
    # TODO 1: Crear socket solo si sock es None.
    own = False
    if sock is None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #inicializamos el socket UDP
        own = True

    #timeout del socket para controlar la espera del ACK
    sock.settimeout(timeout)

    # Preparar el paquete DATA con el número de secuencia y el payload
    
    payload_bytes = payload.encode('utf-8')
   

    # Definir el formato del mensaje DATA y el ACK esperado
    # Ejemplo de protocolo simple basado en texto/bytes:
    data_packet = f"DATA:{seq}:".encode('utf-8') + payload_bytes
    expected_ack = f"ACK:{seq}".encode('utf-8')

    success = False
    attempts = 0

    # TODO 4: Retransmitir al vencer timeout, hasta max_retries.
    while attempts <= max_retries:
        try:
            # TODO 2: Enviar DATA con seq y payload.
            sock.sendto(data_packet, address)
            
            # TODO 3 y TODO 5: Esperar ACK de la misma secuencia e ignorar mensajes inválidos.
            while True:
                response, _ = sock.recvfrom(1024)
                
                # Si recibimos el ACK correcto para esta secuencia, salimos del ciclo de espera
                if response == expected_ack:
                    success = True
                    break
                else:
                    # Ignorar mensajes inválidos, duplicados o ACKs de otras secuencias
                    continue
                    
            if success:
                break
                
        except socket.timeout:
            # Se venció el timeout sin recibir el ACK esperado
            attempts += 1
            if attempts > max_retries:
                # Se agotaron los reintentos permitidos
                break
            # El bucle continuará para retransmitir el paquete

    # TODO 6: Cerrar solo el socket creado por esta función.
    if own:
        sock.close()

    return success

