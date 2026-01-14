"""
Módulo: datos_puerto_ordaz.py
Descripción: Datos de la red urbana de Puerto Ordaz, Venezuela
             Incluye intersecciones principales y calles de la zona céntrica
Autor: CityNavigator
Fecha: Enero 2026
"""

from grafo import Grafo
from persistencia import GestorPersistencia


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
        # ID (nombre descriptivo), Nombre completo, Coordenadas (lon, lat)
        ("Guayana-Bolivia", "Av. Guayana con Calle Bolivia", (-62.745, 8.285)),
        ("Guayana-Chile", "Av. Guayana con Calle Chile", (-62.730, 8.285)),
        ("Guayana-Perú", "Av. Guayana con Calle Perú", (-62.715, 8.285)),
        ("Guayana-Venezuela", "Av. Guayana con Calle Venezuela", (-62.700, 8.285)),
        
        ("LasAméricas-Bolivia", "Av. Las Américas con Calle Bolivia", (-62.745, 8.270)),
        ("LasAméricas-Chile", "Av. Las Américas con Calle Chile", (-62.730, 8.270)),
        ("LasAméricas-Perú", "Av. Las Américas con Calle Perú", (-62.715, 8.270)),
        ("LasAméricas-Venezuela", "Av. Las Américas con Calle Venezuela", (-62.700, 8.270)),
        
        ("VillaAsia-Bolivia", "Av. Villa Asia con Calle Bolivia", (-62.745, 8.255)),
        ("VillaAsia-Chile", "Av. Villa Asia con Calle Chile", (-62.730, 8.255)),
        ("VillaAsia-Perú", "Av. Villa Asia con Calle Perú", (-62.715, 8.255)),
        ("VillaAsia-Venezuela", "Av. Villa Asia con Calle Venezuela", (-62.700, 8.255)),
        
        ("CentroCívico", "Centro Cívico", (-62.720, 8.240)),
        ("PlazaMayor", "Plaza Mayor Alta Vista", (-62.720, 8.300)),
        ("Terminal", "Terminal de Autobuses", (-62.755, 8.265)),
    ]
    
    for id_vertice, nombre, coordenadas in vertices:
        grafo.agregar_vertice(id_vertice, nombre, coordenadas)
    
    # ========== DEFINICIÓN DE ARISTAS (CALLES DIRIGIDAS) ==========
    # Cada arista representa una calle de un solo sentido
    # Formato: (origen, destino, distancia_metros, tiempo_minutos)
    
    aristas = [
        # Avenida Guayana (sentido oeste-este)
        ("Guayana-Bolivia", "Guayana-Chile", 300, 2.5),
        ("Guayana-Chile", "Guayana-Perú", 350, 3.0),
        ("Guayana-Perú", "Guayana-Venezuela", 300, 2.5),
        
        # Avenida Guayana (sentido este-oeste por otra vía)
        ("Guayana-Venezuela", "Guayana-Perú", 320, 3.0),
        ("Guayana-Perú", "Guayana-Chile", 360, 3.2),
        ("Guayana-Chile", "Guayana-Bolivia", 310, 2.8),
        
        # Avenida Las Américas (sentido oeste-este)
        ("LasAméricas-Bolivia", "LasAméricas-Chile", 280, 2.2),
        ("LasAméricas-Chile", "LasAméricas-Perú", 320, 2.8),
        ("LasAméricas-Perú", "LasAméricas-Venezuela", 280, 2.3),
        
        # Avenida Las Américas (sentido este-oeste)
        ("LasAméricas-Venezuela", "LasAméricas-Perú", 290, 2.5),
        ("LasAméricas-Perú", "LasAméricas-Chile", 330, 2.9),
        ("LasAméricas-Chile", "LasAméricas-Bolivia", 290, 2.4),
        
        # Avenida Villa Asia (sentido oeste-este)
        ("VillaAsia-Bolivia", "VillaAsia-Chile", 300, 2.6),
        ("VillaAsia-Chile", "VillaAsia-Perú", 340, 3.1),
        ("VillaAsia-Perú", "VillaAsia-Venezuela", 300, 2.7),
        
        # Avenida Villa Asia (sentido este-oeste)
        ("VillaAsia-Venezuela", "VillaAsia-Perú", 310, 2.8),
        ("VillaAsia-Perú", "VillaAsia-Chile", 350, 3.2),
        ("VillaAsia-Chile", "VillaAsia-Bolivia", 310, 2.7),
        
        # Calles transversales - Calle Bolivia (norte-sur)
        ("Guayana-Bolivia", "LasAméricas-Bolivia", 400, 4.0),
        ("LasAméricas-Bolivia", "VillaAsia-Bolivia", 380, 3.8),
        
        # Calles transversales - Calle Bolivia (sur-norte, retorno)
        ("VillaAsia-Bolivia", "LasAméricas-Bolivia", 390, 4.2),
        ("LasAméricas-Bolivia", "Guayana-Bolivia", 410, 4.3),
        
        # Calles transversales - Calle Chile (norte-sur)
        ("Guayana-Chile", "LasAméricas-Chile", 420, 4.5),
        ("LasAméricas-Chile", "VillaAsia-Chile", 400, 4.2),
        
        # Calles transversales - Calle Chile (sur-norte)
        ("VillaAsia-Chile", "LasAméricas-Chile", 410, 4.3),
        ("LasAméricas-Chile", "Guayana-Chile", 430, 4.6),
        
        # Calles transversales - Calle Perú (norte-sur)
        ("Guayana-Perú", "LasAméricas-Perú", 390, 4.0),
        ("LasAméricas-Perú", "VillaAsia-Perú", 410, 4.3),
        
        # Calles transversales - Calle Perú (sur-norte)
        ("VillaAsia-Perú", "LasAméricas-Perú", 400, 4.1),
        ("LasAméricas-Perú", "Guayana-Perú", 400, 4.2),
        
        # Calles transversales - Calle Venezuela (norte-sur)
        ("Guayana-Venezuela", "LasAméricas-Venezuela", 380, 3.9),
        ("LasAméricas-Venezuela", "VillaAsia-Venezuela", 390, 4.0),
        
        # Calles transversales - Calle Venezuela (sur-norte)
        ("VillaAsia-Venezuela", "LasAméricas-Venezuela", 390, 4.1),
        ("LasAméricas-Venezuela", "Guayana-Venezuela", 390, 4.0),
        
        # Conexiones con Plaza Mayor Alta Vista
        ("PlazaMayor", "Guayana-Bolivia", 450, 5.0),
        ("PlazaMayor", "Guayana-Chile", 400, 4.5),
        ("PlazaMayor", "Guayana-Perú", 400, 4.5),
        ("Guayana-Chile", "PlazaMayor", 410, 4.6),
        
        # Conexiones con Centro Cívico
        ("VillaAsia-Chile", "CentroCívico", 600, 6.5),
        ("VillaAsia-Perú", "CentroCívico", 550, 6.0),
        ("CentroCívico", "VillaAsia-Chile", 610, 6.8),
        ("CentroCívico", "VillaAsia-Perú", 560, 6.2),
        
        # Conexiones con Terminal de Autobuses
        ("Terminal", "LasAméricas-Bolivia", 250, 2.0),
        ("Terminal", "VillaAsia-Bolivia", 350, 3.0),
        ("LasAméricas-Bolivia", "Terminal", 260, 2.2),
        ("VillaAsia-Bolivia", "Terminal", 360, 3.2),
        
        # Conexiones adicionales para mejorar la red
        ("Guayana-Bolivia", "LasAméricas-Chile", 500, 5.5),  # Atajo diagonal
        ("LasAméricas-Perú", "VillaAsia-Venezuela", 520, 5.8),  # Atajo diagonal
        ("LasAméricas-Chile", "VillaAsia-Perú", 480, 5.2),  # Conexión central
        ("Guayana-Perú", "LasAméricas-Chile", 450, 5.0),   # Conexión cruzada
    ]
    
    for origen, destino, distancia, tiempo in aristas:
        grafo.agregar_arista(origen, destino, distancia, tiempo)
    
    # ========== CARGAR DATOS PERSONALIZADOS DEL USUARIO ==========
    gestor = GestorPersistencia()
    
    # Cargar nodos personalizados
    for nodo in gestor.obtener_nodos():
        grafo.agregar_vertice(
            nodo["id"],
            nodo["nombre"],
            tuple(nodo["coordenadas"])
        )
    
    # Cargar conexiones personalizadas
    for conexion in gestor.obtener_conexiones():
        grafo.agregar_arista(
            conexion["origen"],
            conexion["destino"],
            conexion["distancia"],
            conexion["tiempo"]
        )
    
    return grafo


def obtener_puntos_interes() -> dict:
    """
    Retorna un diccionario con puntos de interés mapeados a vértices.
    
    Returns:
        dict: Diccionario con categorías de puntos de interés
    """
    return {
        "Comercial": {
            "Plaza Mayor Alta Vista": "PlazaMayor",
            "Centro Cívico": "CentroCívico",
        },
        "Transporte": {
            "Terminal de Autobuses": "Terminal",
        },
        "Intersecciones Principales": {
            "Guayana - Bolivia": "Guayana-Bolivia",
            "Guayana - Chile": "Guayana-Chile",
            "Guayana - Perú": "Guayana-Perú",
            "Guayana - Venezuela": "Guayana-Venezuela",
            "Las Américas - Bolivia": "LasAméricas-Bolivia",
            "Las Américas - Chile": "LasAméricas-Chile",
            "Las Américas - Perú": "LasAméricas-Perú",
            "Las Américas - Venezuela": "LasAméricas-Venezuela",
            "Villa Asia - Bolivia": "VillaAsia-Bolivia",
            "Villa Asia - Chile": "VillaAsia-Chile",
            "Villa Asia - Perú": "VillaAsia-Perú",
            "Villa Asia - Venezuela": "VillaAsia-Venezuela",
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
