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
    )
    # TODO 2: devolver respuesta JSON y manejar errores.
    try:
        with urlopen(req, timeout=timeout) as response:
            response_data = response.read().decode("utf-8")
            return json.loads(response_data)
    except HTTPError as e:
        return {"status": "error", "message": f"HTTP error: {e.code}"}
    except URLError as e:
        return {"status": "error", "message": f"URL error: {e.reason}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def serve(host="127.0.0.1", port=19000):
    # TODO 3: abrir socket UDP y escuchar datagramas.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #inicializamos el socket UDP
    sock.bind((host, port))  # bind requiere una tupla (host, puerto)
    
    # Cache para retransmisiones: clave (cliente_addr, seq) -> respuesta codificada
    cache = {}
    
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
            
            sock.sendto(response, addr)
            
        except Exception as e:
            print(f"[ERROR] {e}")
if __name__ == "__main__": serve()
