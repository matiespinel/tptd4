import json, socket
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from protocol import decode_message, encode_message, validate_transaction

BANK_URL = "http://127.0.0.1:18080/charge"

def charge_bank(tx, url=BANK_URL, timeout=2.0):
    "Esta función se ocupa de la comunicación HTTP entre el gateway y el banco."
    # TODO 1: validar y enviar POST HTTP al banco.
    # TODO 2: devolver respuesta JSON y manejar errores.
    pass

def serve(host="127.0.0.1", port=19000):
    # TODO 3: abrir socket UDP y escuchar datagramas.
    # TODO 4: procesar DATA y responder ACK con la misma secuencia.
    # TODO 5: cachear respuesta por (cliente, seq) ante retransmisiones.
    pass

if __name__ == "__main__": serve()
