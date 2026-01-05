"""
Módulo: visualizador.py
Descripción: Funciones para visualizar el grafo y las rutas encontradas
Autor: CityNavigator
Fecha: Enero 2026
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import List, Tuple
import networkx as nx


def dibujar_grafo(grafo, ax, ruta_resaltada: List[str] = None):
    """
    Dibuja el grafo en un eje de matplotlib.
    
    Args:
        grafo: Instancia de la clase Grafo
        ax: Eje de matplotlib donde dibujar
        ruta_resaltada: Lista de vértices que forman la ruta a resaltar
    """
    ax.clear()
    
    # Configurar el gráfico
    ax.set_title('Red Urbana de Puerto Ordaz', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Posición Oeste-Este', fontsize=10)
    ax.set_ylabel('Posición Sur-Norte', fontsize=10)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Dibujar aristas (calles)
    for vertice_origen in grafo.vertices:
        x1, y1 = grafo.coordenadas.get(vertice_origen, (0, 0))
        
        for vertice_destino, distancia, tiempo in grafo.obtener_vecinos(vertice_origen):
            x2, y2 = grafo.coordenadas.get(vertice_destino, (0, 0))
            
            # Determinar si esta arista es parte de la ruta resaltada
            es_ruta = False
            if ruta_resaltada and len(ruta_resaltada) > 1:
                for i in range(len(ruta_resaltada) - 1):
                    if ruta_resaltada[i] == vertice_origen and ruta_resaltada[i+1] == vertice_destino:
                        es_ruta = True
                        break
            
            if es_ruta:
                # Dibujar arista de la ruta en color destacado
                ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                           arrowprops=dict(arrowstyle='->', lw=3, color='red', 
                                         connectionstyle="arc3,rad=0.1"))
            else:
                # Dibujar arista normal
                ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                           arrowprops=dict(arrowstyle='->', lw=1, color='gray', 
                                         alpha=0.4, connectionstyle="arc3,rad=0.1"))
    
    # Dibujar vértices (intersecciones)
    for vertice in grafo.vertices:
        x, y = grafo.coordenadas.get(vertice, (0, 0))
        
        # Determinar el color y tamaño según si es parte de la ruta
        if ruta_resaltada:
            if vertice == ruta_resaltada[0]:
                # Vértice de inicio
                color = 'green'
                tamaño = 400
                marcador = 'o'
            elif vertice == ruta_resaltada[-1]:
                # Vértice de destino
                color = 'red'
                tamaño = 400
                marcador = 's'
            elif vertice in ruta_resaltada:
                # Vértice intermedio en la ruta
                color = 'orange'
                tamaño = 300
                marcador = 'o'
            else:
                # Vértice no en la ruta
                color = 'lightblue'
                tamaño = 200
                marcador = 'o'
        else:
            color = 'lightblue'
            tamaño = 200
            marcador = 'o'
        
        ax.scatter(x, y, c=color, s=tamaño, marker=marcador, 
                  edgecolors='black', linewidths=2, zorder=3)
        
        # Agregar etiquetas con el nombre del vértice
        nombre = grafo.nombres_vertices.get(vertice, vertice)
        # Mostrar solo el ID para no saturar
        ax.text(x, y + 0.3, vertice, fontsize=8, ha='center', 
               fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', 
               facecolor='white', alpha=0.8))
    
    # Crear leyenda
    leyenda_elementos = [
        mpatches.Patch(color='lightblue', label='Intersección'),
    ]
    
    if ruta_resaltada:
        leyenda_elementos.extend([
            mpatches.Patch(color='green', label='Inicio'),
            mpatches.Patch(color='red', label='Destino'),
            mpatches.Patch(color='orange', label='Ruta'),
        ])
    
    ax.legend(handles=leyenda_elementos, loc='upper right', fontsize=9)
    
    # Ajustar los límites del gráfico
    if grafo.coordenadas:
        xs = [coord[0] for coord in grafo.coordenadas.values()]
        ys = [coord[1] for coord in grafo.coordenadas.values()]
        margen = 0.5
        ax.set_xlim(min(xs) - margen, max(xs) + margen)
        ax.set_ylim(min(ys) - margen, max(ys) + margen)
    
    ax.set_aspect('equal')


def crear_grafo_networkx(grafo):
    """
    Convierte el grafo personalizado a un grafo de NetworkX para análisis adicional.
    
    Args:
        grafo: Instancia de la clase Grafo
        
    Returns:
        nx.DiGraph: Grafo dirigido de NetworkX
    """
    G = nx.DiGraph()
    
    # Agregar nodos con sus atributos
    for vertice in grafo.vertices:
        nombre = grafo.nombres_vertices.get(vertice, vertice)
        coords = grafo.coordenadas.get(vertice, (0, 0))
        G.add_node(vertice, nombre=nombre, pos=coords)
    
    # Agregar aristas con sus pesos
    for origen in grafo.vertices:
        for destino, distancia, tiempo in grafo.obtener_vecinos(origen):
            G.add_edge(origen, destino, distancia=distancia, tiempo=tiempo)
    
    return G


def mostrar_info_ruta(ruta: List[str], coste: float, criterio: str, grafo) -> str:
    """
    Genera un texto formateado con la información de una ruta.
    
    Args:
        ruta: Lista de vértices que forman la ruta
        coste: Coste total de la ruta
        criterio: 'distancia' o 'tiempo'
        grafo: Instancia de la clase Grafo
        
    Returns:
        str: Texto formateado con la información de la ruta
    """
    if not ruta or coste == float('inf'):
        return "❌ No se encontró una ruta válida entre los puntos seleccionados."
    
    texto = "✅ RUTA ÓPTIMA ENCONTRADA\n"
    texto += "=" * 50 + "\n\n"
    
    # Información del criterio
    if criterio == 'distancia':
        texto += f"📏 Distancia total: {coste:.0f} metros ({coste/1000:.2f} km)\n"
    else:
        texto += f"⏱️ Tiempo total: {coste:.1f} minutos\n"
    
    texto += f"📍 Número de intersecciones: {len(ruta)}\n\n"
    
    # Detalles de la ruta
    texto += "🗺️ RECORRIDO DETALLADO:\n"
    texto += "-" * 50 + "\n\n"
    
    for i, vertice in enumerate(ruta):
        nombre = grafo.nombres_vertices.get(vertice, vertice)
        texto += f"{i+1}. {vertice}: {nombre}\n"
        
        # Mostrar información del tramo si no es el último vértice
        if i < len(ruta) - 1:
            siguiente = ruta[i + 1]
            # Buscar la arista entre los dos vértices
            for vecino, dist, tiemp in grafo.obtener_vecinos(vertice):
                if vecino == siguiente:
                    texto += f"   ↓ {dist:.0f}m ({tiemp:.1f} min)\n"
                    break
    
    return texto
