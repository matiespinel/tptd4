import json, socket
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from protocol import decode_message, encode_message, validate_transaction
#no usamos scrapy porque no es necesario, solo necesitamos hacer un POST HTTP al banco y recibir la respuesta, no necesitamos parsear HTML ni nada de eso

BANK_URL = "http://127.0.0.1:18080/charge"

def charge_bank(tx, url=BANK_URL, timeout=2.0):
    "Esta función se ocupa de la comunicación HTTP entre el gateway y el banco."
    # TODO 1: validar y enviar POST HTTP al banco.
    if not validate_transaction(tx):
        return {"status": "error", "message": "Invalid transaction"}
    req = Request(
        url, 
        data=json.dumps(tx).encode("utf-8"), 
        headers={"Content-Type": "application/json"}, 
        method="POST"
    ) #aramos la solicitud HTTP POST con el JSON de la transacción y el encabezado Content-Type adecuado.
    # TODO 2: devolver respuesta JSON y manejar errores.
    try:
        with urlopen(req, timeout=timeout) as response: #hacemos la solicitud y esperamos la respuesta, con un tiempo de espera definido.
            response_data = response.read().decode("utf-8") #leemos la respuesta y la decodificamos de bytes a string
            return json.loads(response_data)
    except HTTPError as e:
        return {"status": "error", "message": f"HTTP error: {e.code}"}
    except URLError as e:
        return {"status": "error", "message": f"URL error: {e.reason}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def serve(host="127.0.0.1", port=19000, simulate_loss=None):
    # TODO 3: abrir socket UDP y escuchar datagramas.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #inicializamos el socket UDP
    sock.bind((host, port))  # bind requiere una tupla (host, puerto)
    
    # Cache para retransmisiones: clave (cliente_addr, seq) -> respuesta codificada
    cache = {}
    ack_attempts = {}
    
    print(f"Servidor UDP escuchando en {host}:{port}")
    
    while True:
        print("ready to serve")
        try:
            packet, addr = sock.recvfrom(1024)
            data = decode_message(packet)
            
            if data is None:
                continue
                
            seq = data.get("seq")
            client_key = (addr, seq)
            
            ack_attempts[client_key] = ack_attempts.get(client_key, 0) + 1 #si no existe la clave, la inicializamos en 0 y le sumamos 1. Si ya existe, le sumamos 1.
            if client_key in cache:
                response = cache[client_key]
            else:
                # INVOCAR AL BANCO REALMENTE
                bank_result = charge_bank(data)
                
                # Construir la respuesta estructurada con la secuencia correspondiente
                response_data = {
                    "seq": seq,
                    **bank_result
                }
                response = encode_message(response_data)
                cache[client_key] = response
            
            # SIMULACIÓN DE PÉRDIDA DE ACK:
            # Evaluamos si debemos enviar el ACK o descartarlo
            debe_enviar_ack = True
            if simulate_loss == "ack" and ack_attempts[client_key] == 1:
                print(f"[SIMULACIÓN] ACK para seq={seq} generado pero descartado intencionalmente (no se envía).")
                debe_enviar_ack = False
            
            # El sendto ahora está protegido por la bandera y el flujo del servidor no se rompe
            if debe_enviar_ack:
                sock.sendto(response, addr)
            
        except Exception as e:
            print(f"[ERROR] {e}")

#en caso de simular perdida de ack, se descarta el primer ACK generado para cada secuencia, pero el servidor sigue funcionando y puede recibir retransmisiones del cliente.
if __name__ == "__main__": serve(simulate_loss="ack")  # Cambiar a "ack" para simular pérdida de ACK, o "data" para simular pérdida de DATA
