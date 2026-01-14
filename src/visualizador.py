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
    Dibuja el grafo en un eje de matplotlib con estilo de mapa.
    
    Args:
        grafo: Instancia de la clase Grafo
        ax: Eje de matplotlib donde dibujar
        ruta_resaltada: Lista de vértices que forman la ruta a resaltar
    """
    ax.clear()
    
    # Configurar el gráfico con estilo de mapa
    ax.set_facecolor('#f5f5dc')  # Color beige claro tipo mapa
    ax.set_title('Mapa de Puerto Ordaz - Red Vial', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Longitud Oeste', fontsize=11)
    ax.set_ylabel('Latitud Norte', fontsize=11)
    ax.grid(True, alpha=0.2, linestyle=':', color='gray', linewidth=0.5)
    
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
                # Dibujar arista de la ruta en color destacado (ruta activa)
                ax.plot([x1, x2], [y1, y2], color='#FF0000', linewidth=4, 
                       alpha=0.9, zorder=2, solid_capstyle='round')
                # Añadir flecha en el medio
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                dx, dy = x2 - x1, y2 - y1
                ax.annotate('', xy=(mid_x + dx*0.1, mid_y + dy*0.1), 
                           xytext=(mid_x - dx*0.1, mid_y - dy*0.1),
                           arrowprops=dict(arrowstyle='->', lw=2.5, color='#FF0000'))
            else:
                # Dibujar arista normal (calle)
                ax.plot([x1, x2], [y1, y2], color='#696969', linewidth=2, 
                       alpha=0.3, zorder=1, solid_capstyle='round')
    
    # Dibujar vértices (intersecciones) con estilo de mapa
    for vertice in grafo.vertices:
        x, y = grafo.coordenadas.get(vertice, (0, 0))
        
        # Determinar el color y tamaño según si es parte de la ruta
        if ruta_resaltada:
            if vertice == ruta_resaltada[0]:
                # Vértice de inicio (origen)
                color = '#00AA00'
                tamaño = 500
                marcador = 'o'
                borde = 'darkgreen'
            elif vertice == ruta_resaltada[-1]:
                # Vértice de destino
                color = '#DD0000'
                tamaño = 500
                marcador = 's'
                borde = 'darkred'
            elif vertice in ruta_resaltada:
                # Vértice intermedio en la ruta
                color = '#FFA500'
                tamaño = 350
                marcador = 'o'
                borde = 'darkorange'
            else:
                # Vértice no en la ruta (intersección normal)
                color = '#4A90E2'
                tamaño = 250
                marcador = 'o'
                borde = '#2E5C8A'
        else:
            # Sin ruta seleccionada
            color = '#4A90E2'
            tamaño = 250
            marcador = 'o'
            borde = '#2E5C8A'
        
        # Dibujar el marcador
        ax.scatter(x, y, c=color, s=tamaño, marker=marcador, 
                  edgecolors=borde, linewidths=2.5, zorder=5, alpha=0.9)
        
        # Agregar etiquetas con el ID del vértice (tamaño reducido)
        nombre = grafo.nombres_vertices.get(vertice, vertice)
        # Calcular offset para la etiqueta
        offset_y = 0.0025 if ruta_resaltada and vertice in ruta_resaltada else 0.002
        
        # Reducir tamaño de fuente y ajustar padding
        ax.text(x, y + offset_y, vertice, fontsize=7, ha='center', 
               fontweight='bold', bbox=dict(boxstyle='round,pad=0.25', 
               facecolor='white', edgecolor=borde, alpha=0.95, linewidth=1.2),
               zorder=6)
    
    # Crear leyenda estilo mapa
    leyenda_elementos = [
        mpatches.Patch(color='#696969', label='Calles', alpha=0.3),
    ]
    
    if ruta_resaltada:
        leyenda_elementos.extend([
            mpatches.Patch(color='#00AA00', label='⬤ Origen'),
            mpatches.Patch(color='#DD0000', label='■ Destino'),
            mpatches.Patch(color='#FF0000', label='─ Ruta Óptima'),
            mpatches.Patch(color='#FFA500', label='⬤ Paso'),
        ])
    else:
        leyenda_elementos.append(
            mpatches.Patch(color='#4A90E2', label='⬤ Intersecciones')
        )
    
    ax.legend(handles=leyenda_elementos, loc='upper right', fontsize=10, 
             framealpha=0.95, edgecolor='black', fancybox=True, shadow=True)
    
    # Ajustar los límites del gráfico con márgenes apropiados
    if grafo.coordenadas:
        xs = [coord[0] for coord in grafo.coordenadas.values()]
        ys = [coord[1] for coord in grafo.coordenadas.values()]
        margen_x = (max(xs) - min(xs)) * 0.08
        margen_y = (max(ys) - min(ys)) * 0.08
        ax.set_xlim(min(xs) - margen_x, max(xs) + margen_x)
        ax.set_ylim(min(ys) - margen_y, max(ys) + margen_y)
    
    # Mantener aspecto para que se vea como mapa real
    ax.set_aspect('equal', adjustable='box')


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
        return ("❌ NO SE ENCONTRÓ RUTA\n\n"
                "No existe una ruta válida entre los puntos seleccionados.\n"
                "Esto puede deberse a calles de un solo sentido.")
    
    texto = "✅ RUTA ÓPTIMA ENCONTRADA\n"
    texto += "=" * 60 + "\n\n"
    
    # Información del criterio con mejor formato
    if criterio == 'distancia':
        texto += f"📏 DISTANCIA TOTAL: {coste:.0f} metros ({coste/1000:.2f} km)\n"
    else:
        texto += f"⏱️  TIEMPO TOTAL: {coste:.1f} minutos\n"
    
    texto += f"📍 INTERSECCIONES: {len(ruta)}\n"
    texto += f"🚗 TRAMOS: {len(ruta) - 1}\n\n"
    
    # Detalles de la ruta con mejor formato
    texto += "🗺️  RECORRIDO PASO A PASO:\n"
    texto += "─" * 60 + "\n\n"
    
    for i, vertice in enumerate(ruta):
        nombre = grafo.nombres_vertices.get(vertice, vertice)
        
        # Formato especial para origen y destino
        if i == 0:
            texto += f"🟢 INICIO: {vertice}\n"
        elif i == len(ruta) - 1:
            texto += f"🔴 DESTINO: {vertice}\n"
        else:
            texto += f"🟠 Paso {i}: {vertice}\n"
        
        texto += f"   {nombre}\n"
        
        # Mostrar información del tramo si no es el último vértice
        if i < len(ruta) - 1:
            siguiente = ruta[i + 1]
            # Buscar la arista entre los dos vértices
            for vecino, dist, tiemp in grafo.obtener_vecinos(vertice):
                if vecino == siguiente:
                    texto += f"   │\n"
                    texto += f"   ↓  {dist:.0f} metros • {tiemp:.1f} minutos\n"
                    texto += f"   │\n"
                    break
    
    texto += "\n" + "=" * 60 + "\n"
    return texto
