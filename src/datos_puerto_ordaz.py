"""
Módulo: datos_puerto_ordaz.py
Descripción: Datos de la red urbana de Puerto Ordaz, Venezuela
             Incluye intersecciones principales y calles de la zona céntrica
Autor: CityNavigator
Fecha: Enero 2026
"""

from grafo import Grafo


def crear_grafo_puerto_ordaz() -> Grafo:
    """
    Crea y retorna un grafo representando una zona de Puerto Ordaz.
    
    La zona modelada incluye intersecciones principales de:
    - Alta Vista
    - Villa Asia
    - Unare
    - Centro Cívico
    
    Returns:
        Grafo: Instancia del grafo con la red urbana de Puerto Ordaz
    """
    grafo = Grafo()
    
    # ========== DEFINICIÓN DE VÉRTICES (INTERSECCIONES) ==========
    # Cada vértice representa una intersección importante
    # Coordenadas aproximadas basadas en la ubicación real de Puerto Ordaz
    # (longitud, latitud) - ajustadas para mejor visualización tipo mapa
    
    vertices = [
        # ID, Nombre, Coordenadas (lon, lat) - aproximadas para visualización
        ("V1", "Av. Guayana con Calle Bolivia", (-62.745, 8.285)),
        ("V2", "Av. Guayana con Calle Chile", (-62.730, 8.285)),
        ("V3", "Av. Guayana con Calle Perú", (-62.715, 8.285)),
        ("V4", "Av. Guayana con Calle Venezuela", (-62.700, 8.285)),
        
        ("V5", "Av. Las Américas con Calle Bolivia", (-62.745, 8.270)),
        ("V6", "Av. Las Américas con Calle Chile", (-62.730, 8.270)),
        ("V7", "Av. Las Américas con Calle Perú", (-62.715, 8.270)),
        ("V8", "Av. Las Américas con Calle Venezuela", (-62.700, 8.270)),
        
        ("V9", "Av. Villa Asia con Calle Bolivia", (-62.745, 8.255)),
        ("V10", "Av. Villa Asia con Calle Chile", (-62.730, 8.255)),
        ("V11", "Av. Villa Asia con Calle Perú", (-62.715, 8.255)),
        ("V12", "Av. Villa Asia con Calle Venezuela", (-62.700, 8.255)),
        
        ("V13", "Centro Cívico", (-62.720, 8.240)),
        ("V14", "Plaza Mayor Alta Vista", (-62.720, 8.300)),
        ("V15", "Terminal de Autobuses", (-62.755, 8.265)),
    ]
    
    for id_vertice, nombre, coordenadas in vertices:
        grafo.agregar_vertice(id_vertice, nombre, coordenadas)
    
    # ========== DEFINICIÓN DE ARISTAS (CALLES DIRIGIDAS) ==========
    # Cada arista representa una calle de un solo sentido
    # Formato: (origen, destino, distancia_metros, tiempo_minutos)
    
    aristas = [
        # Avenida Guayana (sentido oeste-este)
        ("V1", "V2", 300, 2.5),
        ("V2", "V3", 350, 3.0),
        ("V3", "V4", 300, 2.5),
        
        # Avenida Guayana (sentido este-oeste por otra vía)
        ("V4", "V3", 320, 3.0),
        ("V3", "V2", 360, 3.2),
        ("V2", "V1", 310, 2.8),
        
        # Avenida Las Américas (sentido oeste-este)
        ("V5", "V6", 280, 2.2),
        ("V6", "V7", 320, 2.8),
        ("V7", "V8", 280, 2.3),
        
        # Avenida Las Américas (sentido este-oeste)
        ("V8", "V7", 290, 2.5),
        ("V7", "V6", 330, 2.9),
        ("V6", "V5", 290, 2.4),
        
        # Avenida Villa Asia (sentido oeste-este)
        ("V9", "V10", 300, 2.6),
        ("V10", "V11", 340, 3.1),
        ("V11", "V12", 300, 2.7),
        
        # Avenida Villa Asia (sentido este-oeste)
        ("V12", "V11", 310, 2.8),
        ("V11", "V10", 350, 3.2),
        ("V10", "V9", 310, 2.7),
        
        # Calles transversales - Calle Bolivia (norte-sur)
        ("V1", "V5", 400, 4.0),
        ("V5", "V9", 380, 3.8),
        
        # Calles transversales - Calle Bolivia (sur-norte, retorno)
        ("V9", "V5", 390, 4.2),
        ("V5", "V1", 410, 4.3),
        
        # Calles transversales - Calle Chile (norte-sur)
        ("V2", "V6", 420, 4.5),
        ("V6", "V10", 400, 4.2),
        
        # Calles transversales - Calle Chile (sur-norte)
        ("V10", "V6", 410, 4.3),
        ("V6", "V2", 430, 4.6),
        
        # Calles transversales - Calle Perú (norte-sur)
        ("V3", "V7", 390, 4.0),
        ("V7", "V11", 410, 4.3),
        
        # Calles transversales - Calle Perú (sur-norte)
        ("V11", "V7", 400, 4.1),
        ("V7", "V3", 400, 4.2),
        
        # Calles transversales - Calle Venezuela (norte-sur)
        ("V4", "V8", 380, 3.9),
        ("V8", "V12", 390, 4.0),
        
        # Calles transversales - Calle Venezuela (sur-norte)
        ("V12", "V8", 390, 4.1),
        ("V8", "V4", 390, 4.0),
        
        # Conexiones con Plaza Mayor Alta Vista
        ("V14", "V1", 450, 5.0),
        ("V14", "V2", 400, 4.5),
        ("V14", "V3", 400, 4.5),
        ("V2", "V14", 410, 4.6),
        
        # Conexiones con Centro Cívico
        ("V10", "V13", 600, 6.5),
        ("V11", "V13", 550, 6.0),
        ("V13", "V10", 610, 6.8),
        ("V13", "V11", 560, 6.2),
        
        # Conexiones con Terminal de Autobuses
        ("V15", "V5", 250, 2.0),
        ("V15", "V9", 350, 3.0),
        ("V5", "V15", 260, 2.2),
        ("V9", "V15", 360, 3.2),
        
        # Conexiones adicionales para mejorar la red
        ("V1", "V6", 500, 5.5),  # Atajo diagonal
        ("V7", "V12", 520, 5.8),  # Atajo diagonal
        ("V6", "V11", 480, 5.2),  # Conexión central
        ("V3", "V6", 450, 5.0),   # Conexión cruzada
    ]
    
    for origen, destino, distancia, tiempo in aristas:
        grafo.agregar_arista(origen, destino, distancia, tiempo)
    
    return grafo


def obtener_puntos_interes() -> dict:
    """
    Retorna un diccionario con puntos de interés mapeados a vértices.
    
    Returns:
        dict: Diccionario con categorías de puntos de interés
    """
    return {
        "Comercial": {
            "Plaza Mayor Alta Vista": "V14",
            "Centro Cívico": "V13",
        },
        "Transporte": {
            "Terminal de Autobuses": "V15",
        },
        "Intersecciones Principales": {
            "Guayana - Bolivia": "V1",
            "Guayana - Chile": "V2",
            "Guayana - Perú": "V3",
            "Guayana - Venezuela": "V4",
            "Las Américas - Bolivia": "V5",
            "Las Américas - Chile": "V6",
            "Las Américas - Perú": "V7",
            "Las Américas - Venezuela": "V8",
            "Villa Asia - Bolivia": "V9",
            "Villa Asia - Chile": "V10",
            "Villa Asia - Perú": "V11",
            "Villa Asia - Venezuela": "V12",
        }
    }


if __name__ == "__main__":
    # Prueba de creación del grafo
    grafo = crear_grafo_puerto_ordaz()
    stats = grafo.obtener_estadisticas()
    
    print("=== Grafo de Puerto Ordaz ===")
    print(f"Vértices: {stats['num_vertices']}")
    print(f"Aristas: {stats['num_aristas']}")
    print(f"Densidad: {stats['densidad']:.3f}")
    
    print("\n=== Puntos de Interés ===")
    puntos = obtener_puntos_interes()
    for categoria, lugares in puntos.items():
        print(f"\n{categoria}:")
        for nombre, vertice in lugares.items():
            print(f"  - {nombre}: {vertice}")
