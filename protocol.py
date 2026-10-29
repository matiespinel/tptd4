import json

def encode_message(message):
    # Provisto: codificación JSON sobre UTF-8.
    return json.dumps(message, ensure_ascii=False, separators=(",", ":")).encode("utf-8")

def decode_message(data):
    # TODO 1: decodificar JSON y verificar que sea un diccionario.
    pass

def validate_transaction(tx):
    # TODO 2: verificar campos requeridos, tipos y monto estrictamente positivo.
    # transaction_id, card_id, amount, station, route
    pass
