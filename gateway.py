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
    req = Request(url, data=json.dumps(tx).encode("utf-8"), headers={""}, method="POST")
    # TODO 2: devolver respuesta JSON y manejar errores.
    """try:
        with urlopen(req, timeout=timeout) as response:
            response_data = response.read().decode("utf-8")
            return json.loads(response_data)
    except HTTPError as e:
        return {"status": "error", "message": f"HTTP error: {e.code}"}
    except URLError as e:
        return {"status": "error", "message": f"URL error: {e.reason}"}
    except Exception as e:
        return {"status": "error", "message": str(e)} """

def serve(host="127.0.0.1", port=19000):
    # TODO 3: abrir socket UDP y escuchar datagramas.
    socketgateway =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketgateway.bind(port)
    socketgateway.listen(1) #permitimos 1 conexion simultanea, este es el socket de escucha
    while True:
        print("ready to serve")
        socketMolinete, addr = socketgateway.accept()  # Aceptar la conexión, el socketMolinete es el socket que se va a usar para comunicarse con el molinete, addr es la direccion del molinete
        try:
            data = decode_message(socketMolinete.recv(1024)) 
            break
        except data == None:
            pass
            
    #data contiene el diccionario con la transaccion, sec y ack       
    # TODO 4: procesar DATA y responder ACK con la misma secuencia.
    socketMolinete.sendto(encode_message({"ack": data["ack"], "seq": data["seq"]}), addr)    
    # TODO 5: cachear respuesta por (cliente, seq) ante retransmisiones.
    socketMolinete.close() #cerramos el socket que se usa para comunicarse con el molinete, el socket de escucha sigue abierto
    socketgateway.listen(1)
    socketgateway.settimeout(10) #10?? la verdad no tengo idea cuanto tarda 
    try :
        serve()      
    except socket.timeout:
        print("timeout")
        socketgateway.close()

if __name__ == "__main__": serve()
