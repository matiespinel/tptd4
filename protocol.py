import json

def encode_message(message):
    # Provisto: codificación JSON sobre UTF-8.
    return json.dumps(message, ensure_ascii=False, separators=(",", ":")).encode("utf-8") #.dumps se encarga de hacer el diccionario en un string para encodearlo 
"""transaction = {
        "transaction_id": transaction_id,
        "card_id": card_id,
        "amount": amount,
        "station": station,
        "header": cabecera_elegida,
        "seq": seq #agregado para que el gateway pueda responder con la misma secuencia
    }""" 
def decode_message(data):
    # TODO 1: decodificar JSON y verificar que sea un diccionario.
    data = data.decode("utf-8")
    #ahora data es un string, lo parseamos a dict
    data = json.loads(data) #.loads se encarga de hacerlo un diccionario devuelta
    if not isinstance(data, dict):
        return None
    return data
    

def validate_transaction(tx):
    # TODO 2: verificar campos requeridos, tipos y monto estrictamente positivo.
    # transaction_id, card_id, amount, station, route
    tx_required_fields = ["transaction_id", "card_id", "amount", "station", "header", "route"]
    for field in tx_required_fields:
        if field not in tx:
            return False
        if tx[field] is None:
            return False
            
    # Validaciones específicas por tipo
    if not isinstance(tx["amount"], (int, float)) or tx["amount"] <= 0:
        return False
    if not isinstance(tx["route"], list) or len(tx["route"]) == 0:
        return False
    return True
