"""
Módulo: grafo.py
Descripción: Implementación de un grafo dirigido y ponderado para representar
             una red urbana con intersecciones y calles.
Autor: CityNavigator
Fecha: Enero 2026
"""

from collections import defaultdict, deque
import heapq
from typing import List, Tuple, Dict, Optional


class Grafo:
    """
    Clase que representa un grafo dirigido y ponderado para modelar una red urbana.
    
    Atributos:
        vertices (set): Conjunto de todos los vértices (intersecciones)
        adyacencias (dict): Diccionario de listas de adyacencia
                           estructura: {vertice_origen: [(vertice_destino, distancia, tiempo), ...]}
    """
    
    def __init__(self):
        """Inicializa un grafo vacío."""
        self.vertices = set()
        self.adyacencias = defaultdict(list)
        self.nombres_vertices = {}  # Mapeo de ID a nombre legible
        self.coordenadas = {}  # Coordenadas (x, y) para visualización
    
    def agregar_vertice(self, vertice: str, nombre: str = None, coordenadas: Tuple[float, float] = None):
        """
        Agrega un vértice (intersección) al grafo.
        
        Args:
            vertice (str): Identificador único del vértice
            nombre (str): Nombre descriptivo de la intersección
            coordenadas (tuple): Coordenadas (x, y) para visualización
        """
        self.vertices.add(vertice)
        if nombre:
            self.nombres_vertices[vertice] = nombre
        if coordenadas:
            self.coordenadas[vertice] = coordenadas
    
    def agregar_arista(self, origen: str, destino: str, distancia: float, tiempo: float):
        """
        Agrega una arista dirigida (calle de un solo sentido) al grafo.
        
        Args:
            origen (str): Vértice de origen
            destino (str): Vértice de destino
            distancia (float): Distancia en metros
            tiempo (float): Tiempo promedio en minutos
        """
        if origen not in self.vertices:
            self.agregar_vertice(origen)
        if destino not in self.vertices:
            self.agregar_vertice(destino)
        
        self.adyacencias[origen].append((destino, distancia, tiempo))
    
    def obtener_vecinos(self, vertice: str) -> List[Tuple[str, float, float]]:
        """
        Obtiene la lista de vecinos de un vértice.
        
        Args:
            vertice (str): Vértice del cual obtener vecinos
            
        Returns:
            List[Tuple]: Lista de tuplas (vertice_destino, distancia, tiempo)
        """
        return self.adyacencias.get(vertice, [])
    
    def dijkstra(self, origen: str, destino: str, criterio: str = 'distancia') -> Tuple[List[str], float]:
        """
        Implementa el algoritmo de Dijkstra para encontrar el camino más corto.
        
        Args:
            origen (str): Vértice de inicio
            destino (str): Vértice de destino
            criterio (str): 'distancia' o 'tiempo' - métrica a minimizar
            
        Returns:
            Tuple[List[str], float]: (camino_optimo, coste_total)
                                     donde camino_optimo es la secuencia de vértices
                                     y coste_total es la suma de distancias o tiempos
        """
        # Validar que los vértices existen
        if origen not in self.vertices or destino not in self.vertices:
            return [], float('inf')
        
        # Inicializar estructuras de datos
        distancias = {v: float('inf') for v in self.vertices}
        distancias[origen] = 0
        predecesores = {v: None for v in self.vertices}
        visitados = set()
        
        # Cola de prioridad: (distancia_acumulada, vertice)
        cola_prioridad = [(0, origen)]
        
        while cola_prioridad:
            distancia_actual, vertice_actual = heapq.heappop(cola_prioridad)
            
            # Si ya visitamos este vértice, continuar
            if vertice_actual in visitados:
                continue
            
            visitados.add(vertice_actual)
            
            # Si llegamos al destino, podemos terminar
            if vertice_actual == destino:
                break
            
            # Relajar aristas salientes
            for vecino, dist, tiemp in self.obtener_vecinos(vertice_actual):
                if vecino in visitados:
                    continue
                
                # Seleccionar la métrica según el criterio
                peso = dist if criterio == 'distancia' else tiemp
                nueva_distancia = distancias[vertice_actual] + peso
                
                # Si encontramos un camino mejor, actualizar
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    predecesores[vecino] = vertice_actual
                    heapq.heappush(cola_prioridad, (nueva_distancia, vecino))
        
        # Reconstruir el camino desde el destino hasta el origen
        camino = []
        vertice_actual = destino
        
        while vertice_actual is not None:
            camino.append(vertice_actual)
            vertice_actual = predecesores[vertice_actual]
        
        camino.reverse()
        
        # Si el camino no empieza en el origen, no hay conexión
        if not camino or camino[0] != origen:
            return [], float('inf')
        
        return camino, distancias[destino]
    
    def bfs(self, origen: str, destino: str) -> Tuple[bool, List[str]]:
        """
        Búsqueda en anchura (BFS) para verificar conectividad.
        
        Args:
            origen (str): Vértice de inicio
            destino (str): Vértice de destino
            
        Returns:
            Tuple[bool, List[str]]: (es_alcanzable, camino)
        """
        if origen not in self.vertices or destino not in self.vertices:
            return False, []
        
        if origen == destino:
            return True, [origen]
        
        visitados = set([origen])
        cola = deque([(origen, [origen])])
        
        while cola:
            vertice_actual, camino = cola.popleft()
            
            for vecino, _, _ in self.obtener_vecinos(vertice_actual):
                if vecino not in visitados:
                    nuevo_camino = camino + [vecino]
                    
                    if vecino == destino:
                        return True, nuevo_camino
                    
                    visitados.add(vecino)
                    cola.append((vecino, nuevo_camino))
        
        return False, []
    
    def dfs(self, origen: str, destino: str) -> Tuple[bool, List[str]]:
        """
        Búsqueda en profundidad (DFS) para verificar conectividad.
        
        Args:
            origen (str): Vértice de inicio
            destino (str): Vértice de destino
            
        Returns:
            Tuple[bool, List[str]]: (es_alcanzable, camino)
        """
        if origen not in self.vertices or destino not in self.vertices:
            return False, []
        
        visitados = set()
        camino = []
        
        def dfs_recursivo(vertice_actual):
            if vertice_actual == destino:
                camino.append(vertice_actual)
                return True
            
            visitados.add(vertice_actual)
            camino.append(vertice_actual)
            
            for vecino, _, _ in self.obtener_vecinos(vertice_actual):
                if vecino not in visitados:
                    if dfs_recursivo(vecino):
                        return True
            
            camino.pop()
            return False
        
        encontrado = dfs_recursivo(origen)
        return encontrado, camino if encontrado else []
    
    def obtener_info_vertice(self, vertice: str) -> Dict:
        """
        Obtiene información detallada de un vértice.
        
        Args:
            vertice (str): Identificador del vértice
            
        Returns:
            Dict: Diccionario con información del vértice
        """
        return {
            'id': vertice,
            'nombre': self.nombres_vertices.get(vertice, vertice),
            'coordenadas': self.coordenadas.get(vertice, (0, 0)),
            'grado_salida': len(self.adyacencias.get(vertice, []))
        }
    
    def obtener_todos_vertices(self) -> List[str]:
        """Retorna una lista ordenada de todos los vértices."""
        return sorted(list(self.vertices))
    
    def obtener_estadisticas(self) -> Dict:
        """
        Calcula estadísticas generales del grafo.
        
        Returns:
            Dict: Diccionario con estadísticas
        """
        num_vertices = len(self.vertices)
        num_aristas = sum(len(vecinos) for vecinos in self.adyacencias.values())
        
        return {
            'num_vertices': num_vertices,
            'num_aristas': num_aristas,
            'densidad': num_aristas / (num_vertices * (num_vertices - 1)) if num_vertices > 1 else 0
        }
