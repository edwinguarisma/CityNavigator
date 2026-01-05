"""
Módulo: prueba_grafo.py
Descripción: Script de prueba para verificar el funcionamiento del grafo
Autor: CityNavigator
Fecha: Enero 2026
"""

import sys
import io

# Configurar salida UTF-8 para evitar problemas con emojis en Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from datos_puerto_ordaz import crear_grafo_puerto_ordaz, obtener_puntos_interes


def probar_creacion_grafo():
    """Prueba la creación del grafo de Puerto Ordaz."""
    print("=" * 60)
    print("PRUEBA 1: Creación del Grafo")
    print("=" * 60)
    
    grafo = crear_grafo_puerto_ordaz()
    stats = grafo.obtener_estadisticas()
    
    print(f"✅ Grafo creado exitosamente")
    print(f"   - Vértices: {stats['num_vertices']}")
    print(f"   - Aristas: {stats['num_aristas']}")
    print(f"   - Densidad: {stats['densidad']:.3f}")
    print()
    
    return grafo


def probar_dijkstra(grafo):
    """Prueba el algoritmo de Dijkstra."""
    print("=" * 60)
    print("PRUEBA 2: Algoritmo de Dijkstra")
    print("=" * 60)
    
    # Prueba 1: De Plaza Mayor a Centro Cívico por distancia
    print("\n📍 Prueba 2.1: V14 → V13 (por distancia)")
    ruta, coste = grafo.dijkstra('V14', 'V13', 'distancia')
    
    if ruta:
        print(f"✅ Ruta encontrada:")
        print(f"   - Camino: {' → '.join(ruta)}")
        print(f"   - Distancia: {coste:.0f} metros ({coste/1000:.2f} km)")
    else:
        print("❌ No se encontró ruta")
    
    # Prueba 2: De Plaza Mayor a Centro Cívico por tiempo
    print("\n📍 Prueba 2.2: V14 → V13 (por tiempo)")
    ruta, coste = grafo.dijkstra('V14', 'V13', 'tiempo')
    
    if ruta:
        print(f"✅ Ruta encontrada:")
        print(f"   - Camino: {' → '.join(ruta)}")
        print(f"   - Tiempo: {coste:.1f} minutos")
    else:
        print("❌ No se encontró ruta")
    
    # Prueba 3: De V1 a V12
    print("\n📍 Prueba 2.3: V1 → V12 (por distancia)")
    ruta, coste = grafo.dijkstra('V1', 'V12', 'distancia')
    
    if ruta:
        print(f"✅ Ruta encontrada:")
        print(f"   - Camino: {' → '.join(ruta)}")
        print(f"   - Distancia: {coste:.0f} metros")
        print(f"   - Intersecciones: {len(ruta)}")
    else:
        print("❌ No se encontró ruta")
    
    print()


def probar_bfs(grafo):
    """Prueba el algoritmo BFS."""
    print("=" * 60)
    print("PRUEBA 3: Algoritmo BFS")
    print("=" * 60)
    
    print("\n📍 Prueba 3.1: V15 → V12")
    encontrado, ruta = grafo.bfs('V15', 'V12')
    
    if encontrado:
        print(f"✅ Conexión encontrada:")
        print(f"   - Camino: {' → '.join(ruta)}")
        print(f"   - Intersecciones: {len(ruta)}")
    else:
        print("❌ No hay conexión")
    
    print("\n📍 Prueba 3.2: V1 → V13")
    encontrado, ruta = grafo.bfs('V1', 'V13')
    
    if encontrado:
        print(f"✅ Conexión encontrada:")
        print(f"   - Camino: {' → '.join(ruta)}")
        print(f"   - Intersecciones: {len(ruta)}")
    else:
        print("❌ No hay conexión")
    
    print()


def probar_dfs(grafo):
    """Prueba el algoritmo DFS."""
    print("=" * 60)
    print("PRUEBA 4: Algoritmo DFS")
    print("=" * 60)
    
    print("\n📍 Prueba 4.1: V1 → V8")
    encontrado, ruta = grafo.dfs('V1', 'V8')
    
    if encontrado:
        print(f"✅ Conexión encontrada:")
        print(f"   - Camino: {' → '.join(ruta)}")
        print(f"   - Intersecciones: {len(ruta)}")
    else:
        print("❌ No hay conexión")
    
    print()


def probar_puntos_interes():
    """Muestra los puntos de interés."""
    print("=" * 60)
    print("PRUEBA 5: Puntos de Interés")
    print("=" * 60)
    
    puntos = obtener_puntos_interes()
    
    for categoria, lugares in puntos.items():
        print(f"\n📌 {categoria}:")
        for nombre, vertice in lugares.items():
            print(f"   - {nombre}: {vertice}")
    
    print()


def comparar_algoritmos(grafo):
    """Compara los resultados de los tres algoritmos."""
    print("=" * 60)
    print("PRUEBA 6: Comparación de Algoritmos")
    print("=" * 60)
    
    origen = 'V1'
    destino = 'V13'
    
    print(f"\n🎯 Ruta: {origen} → {destino}\n")
    
    # Dijkstra por distancia
    ruta_d, coste_d = grafo.dijkstra(origen, destino, 'distancia')
    print(f"📏 Dijkstra (distancia):")
    print(f"   - Camino: {' → '.join(ruta_d)}")
    print(f"   - Distancia: {coste_d:.0f} m")
    print(f"   - Intersecciones: {len(ruta_d)}")
    
    # Dijkstra por tiempo
    ruta_t, coste_t = grafo.dijkstra(origen, destino, 'tiempo')
    print(f"\n⏱️  Dijkstra (tiempo):")
    print(f"   - Camino: {' → '.join(ruta_t)}")
    print(f"   - Tiempo: {coste_t:.1f} min")
    print(f"   - Intersecciones: {len(ruta_t)}")
    
    # BFS
    encontrado_b, ruta_b = grafo.bfs(origen, destino)
    print(f"\n🔍 BFS:")
    print(f"   - Camino: {' → '.join(ruta_b)}")
    print(f"   - Intersecciones: {len(ruta_b)}")
    
    # DFS
    encontrado_f, ruta_f = grafo.dfs(origen, destino)
    print(f"\n🔎 DFS:")
    print(f"   - Camino: {' → '.join(ruta_f)}")
    print(f"   - Intersecciones: {len(ruta_f)}")
    
    print()


def main():
    """Función principal de prueba."""
    print("\n" + "=" * 60)
    print("  SUITE DE PRUEBAS - CITYNAVIGATOR")
    print("  Puerto Ordaz, Venezuela")
    print("=" * 60 + "\n")
    
    try:
        # Ejecutar pruebas
        grafo = probar_creacion_grafo()
        probar_dijkstra(grafo)
        probar_bfs(grafo)
        probar_dfs(grafo)
        probar_puntos_interes()
        comparar_algoritmos(grafo)
        
        print("=" * 60)
        print("✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("=" * 60)
        print()
        
    except Exception as e:
        print(f"\n❌ ERROR en las pruebas: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
