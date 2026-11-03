from http.server import BaseHTTPRequestHandler, HTTPServer
import json, threading
from protocol import validate_transaction

INITIAL_BALANCES = {"SUBE-001": 1500.0, "SUBE-002": 300.0}#son datos ficticios para probar se pueden agregar mas
_balances = dict(INITIAL_BALANCES)
_processed = {}
_lock = threading.Lock()

def reset_state():
    global _balances, _processed
    with _lock:
        _balances, _processed = dict(INITIAL_BALANCES), {}

def process_transaction(tx):
    # TODO 1: validar transacción.
    if not validate_transaction(tx):
        return {"status": "error", "reason": "Invalid transaction"}
    # TODO 2: procesar transaction_id como máximo una vez.
    if tx["transaction_id"] in _processed:
        return {"status": "error", "reason": "Duplicate transaction"}
    # TODO 3: validar tarjeta/saldo y descontar solo si se aprueba.
    if tx["card_id"] not in _balances:
        return {"status": "error", "reason": "Card not found"}
    if _balances[tx["card_id"]] < tx["amount"]:
        return {"status": "error", "reason": "Insufficient balance"}
    _balances[tx["card_id"]] -= tx["amount"]
    # TODO 4: devolver status, reason, balance y duplicate.
    return {"status": "success", "reason": None, "balance": _balances[tx["card_id"]], "duplicate": False}

class BankHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # TODO 5: aceptar POST /charge, leer JSON e invocar process_transaction.
        
        # TODO 6: responder JSON con Content-Type y Content-Length.
        # TODO 7: 404 para rutas desconocidas y 400 para JSON inválido.
        pass
    def log_message(self, fmt, *args):
        print("[BANK]", fmt % args)

def run_server(host="127.0.0.1", port=18080):
    server = HTTPServer((host, port), BankHandler)
    print(f"Banco HTTP escuchando en http://{host}:{port}")
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()

if __name__ == "__main__": run_server()
