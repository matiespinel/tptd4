
import random
import copy


BASE_GRAPH = {
    "Medrano": {
        "Carlos Gardel": 2, "Ángel Gallardo": 3, "Malabia": 4,
    },
    "Carlos Gardel": {
        "Medrano": 2, "Pueyrredón": 2, "Ángel Gallardo": 5,
    },
    "Pueyrredón": {
        "Carlos Gardel": 2, "Callao": 2, "Diagonal Norte": 6,
    },
    "Callao": {
        "Pueyrredón": 2, "Diagonal Norte": 4, "Retiro": 7,
    },
    "Ángel Gallardo": {
        "Medrano": 3, "Malabia": 2, "Carlos Gardel": 5,
    },
    "Malabia": {
        "Ángel Gallardo": 2, "Dorrego": 3, "Medrano": 4,
    },
    "Dorrego": {
        "Malabia": 3, "Federico Lacroze": 2, "Retiro": 6,
    },
    "Federico Lacroze": {
        "Dorrego": 2, "Retiro": 8, "Diagonal Norte": 5,
    },
    "Diagonal Norte": {
        "Callao": 4, "Retiro": 3, "Pueyrredón": 6,
        "Federico Lacroze": 5,
    },
    "Retiro": {
        "Diagonal Norte": 3, "Federico Lacroze": 8,
        "Callao": 7, "Dorrego": 6,
    },
}

# Estaciones que funcionan como headers.
HEADERS = {"Retiro", "Federico Lacroze"}


def is_connected(graph):
    """
    Verifica si todas las estaciones son alcanzables desde una estación.
    """
    if not graph:
        return True

    start = next(iter(graph))
    visited = set()
    pending = [start]

    while pending:
        station = pending.pop()

        if station in visited:
            continue

        visited.add(station)

        for neighbor in graph[station]:
            if neighbor not in visited:
                pending.append(neighbor)

    return len(visited) == len(graph)


def build_topology(seed):
    """
    Genera una topología reproducible a partir de una seed.

    Asigna pesos aleatorios positivos a los enlaces y elimina
    un enlace bidireccional, manteniendo conectada la red.

    Args:
        seed: Semilla que determina la topología generada.

    Returns:
        Grafo representado como un diccionario de diccionarios.
    """
    rng = random.Random(seed)
    graph = copy.deepcopy(BASE_GRAPH)

    # Obtener cada enlace bidireccional una sola vez.
    edges = []

    for station, neighbors in graph.items():
        for neighbor in neighbors:
            if station < neighbor:
                edges.append((station, neighbor))

    # Asignar un peso aleatorio a cada enlace.
    for station, neighbor in edges:
        weight = rng.randint(1, 10)
        graph[station][neighbor] = weight
        graph[neighbor][station] = weight

    # Probar enlaces en orden aleatorio hasta encontrar
    # uno que pueda eliminarse sin desconectar la red.
    rng.shuffle(edges)

    for station, neighbor in edges:
        weight = graph[station][neighbor]

        del graph[station][neighbor]
        del graph[neighbor][station]

        if is_connected(graph):
            break

        # Restaurar el enlace si desconectaba la red.
        graph[station][neighbor] = weight
        graph[neighbor][station] = weight

    return graph


# TODO: Generar el grafo utilizando build_topology()
# y la seed asignada al grupo.
GRAPH = build_topology(seed=2)  # Reemplaza 12345 con la seed de tu grupo
