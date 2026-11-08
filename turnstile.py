import argparse, uuid #recibir argumentos por línea de comandos
from routing import shortest_path
from topology import GRAPH, HEADERS
from transport import send_reliably

def build_transaction(card_id, amount, station):
    "Recibe el identificador de la tarjeta, el importe y la estación donde está el molinete."
    # TODO 1: validar monto y estación.
    #primero validamos que la estación esté en el grafo y que el monto sea positivo.
    if station not in GRAPH:
        raise ValueError(f"Estación '{station}' no encontrada en el grafo.")
    if amount <= 0:
        raise ValueError("El monto debe ser un número positivo.")
    # TODO 2: elegir la cabecera alcanzable de menor costo.
    #para esto, primero calculamos la ruta más corta desde la estación a cada cabecera y guardamos el costo.
    costos = {}
    for cabecera in HEADERS:
        ruta = shortest_path(GRAPH, station, cabecera) #esto me da la ruta más corta desde la estación a cada cabecera, o [] si no hay ruta.
        if ruta: #basicamente si la ruta no es vacía, calculamos el costo sumando los pesos de las aristas en la ruta.
            costos[cabecera] = sum(GRAPH[actual][siguiente] for actual, siguiente in zip(ruta[:-1], ruta[1:])) #sumamos los pesos de las aristas en la ruta para obtener el costo total.
    # TODO 3: generar transaction_id y construir la transacción.
    transaction_id = str(uuid.uuid4())
    #si no hay cabeceras alcanzables, lanzamos un error.
    if not costos: #esta condición se cumple si el diccionario de costos está vacío, es decir, no hay cabeceras alcanzables desde la estación.
        raise ValueError(f"No hay cabeceras alcanzables desde la estación '{station}'.")
    #elegimos la cabecera de menor costo.
    cabecera_elegida = min(costos, key=costos.get) #elegimos la mas barata
    transaction = { 
        "transaction_id": transaction_id,
        "card_id": card_id,
        "amount": amount,
        "station": station,
        "header": cabecera_elegida,
    }
    return transaction
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--card", default="SUBE-001")
    parser.add_argument("--amount", type=float, default=100)
    parser.add_argument("--station", default="Medrano")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=19000)
    parser.add_argument("--sim-loss", choices=["data", "ack", "none"], default="none", help="Simular pérdida de data o ack")
    args = parser.parse_args()
    tx = build_transaction(args.card, args.amount, args.station)
    print("Transacción:", tx)
    # Pasamos el parámetro de simulación a send_reliably
    sim = args.sim_loss if args.sim_loss != "none" else None
    try: print("Respuesta:", send_reliably((args.host,args.port),tx,seq=1,timeout=1,max_retries=3, simulate_loss=sim))
    except TimeoutError as exc: print("No se pudo completar el cobro:", exc)

if __name__ == "__main__": main()
