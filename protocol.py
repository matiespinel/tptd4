import json

def encode_message(message):
    # Provisto: codificación JSON sobre UTF-8.
    return json.dumps(message, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
"""transaction = {
        "transaction_id": transaction_id,
        "card_id": card_id,
        "amount": amount,
        "station": station,
        "header": cabecera_elegida,
    }""" 
def decode_message(data):
    # TODO 1: decodificar JSON y verificar que sea un diccionario.
    data.decode("utf-8")
    
    pass

def validate_transaction(tx):
    # TODO 2: verificar campos requeridos, tipos y monto estrictamente positivo.
    # transaction_id, card_id, amount, station, route
    pass
