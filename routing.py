import heapq
import math

def dijkstra(graph, source):
    # TODO 1: validar el origen y los costos no negativos.
    if source not in graph:
        return None  
    
    #si bien de pre dijktra no se puede usar con pesos negativos, se valida que no haya pesos negativos en el grafo.
    for estacion, vecinos_dict in graph.items():
        for vecino, peso in vecinos_dict.items():
            if peso < 0:
                return None  
                
    # TODO 2: inicializar distancias y cola de prioridad.
    distancias = {estacion: float('inf') for estacion in graph}
    distancias[source] = 0
    
    # Cola de prioridad: almacena tuplas (distancia, nodo)
    cola = [(0, source)]
    
    # TODO 3: relajar aristas y devolver costos para nodos alcanzables.
    while cola:
        distancia_actual, nodo_actual = heapq.heappop(cola)
        
        # Si ya encontramos una ruta mejor, ignoramos este nodo
        if distancia_actual > distancias[nodo_actual]:
            continue
            
        # Explorar vecinos y relajar aristas
        for vecino, peso in graph[nodo_actual].items():
            distancia = distancia_actual + peso
            
            # Si encontramos un camino más corto hacia el vecino
            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                heapq.heappush(cola, (distancia, vecino))
                
    return distancias
    

def shortest_path(graph, source, target):
    # TODO 4: implementar Dijkstra guardando predecesores.
    distancias = dijkstra(graph, source)
    #esto me devuelve un diccionario con las distancias más cortas desde el nodo source a todos los demás nodos alcanzables en el grafo.
    if distancias is None or target not in distancias or distancias[target] == float('inf'):
        return []  # No hay ruta disponible
    # TODO 5: reconstruir la ruta; devolver [] si no hay ruta.
    ruta = []
    nodo_actual = target
    while nodo_actual != source:
        ruta.append(nodo_actual)
        # Encontrar el predecesor del nodo actual
        for vecino, peso in graph[nodo_actual].items():
            if distancias[nodo_actual] == distancias[vecino] + peso:
                nodo_actual = vecino
                break
    ruta.append(source)
    ruta.reverse()
    return ruta
    
 
