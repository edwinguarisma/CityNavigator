# 🗺️ CityNavigator: Sistema de Navegación Urbana

## Modelado y Optimización de Rutas en Puerto Ordaz

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Activo-success.svg)

---

## 📋 Descripción del Proyecto

**CityNavigator** es un sistema inteligente de navegación urbana que modela la red de calles de Puerto Ordaz, Venezuela, como un grafo dirigido y ponderado. El proyecto implementa algoritmos clásicos de teoría de grafos para encontrar rutas óptimas entre intersecciones según diferentes criterios de optimización.

### 🎯 Objetivos

- Representar una zona urbana como un grafo dirigido y ponderado
- Implementar algoritmos de búsqueda de caminos óptimos (Dijkstra, BFS, DFS)
- Proporcionar una interfaz gráfica intuitiva para consulta de rutas
- Analizar la estructura y conectividad de la red urbana

---

## 🏗️ Estructura del Proyecto

```
04_proyecto_grafos/
│
├── src/                          # Código fuente
│   ├── main.py                   # Punto de entrada principal
│   ├── grafo.py                  # Implementación de la clase Grafo
│   ├── datos_puerto_ordaz.py    # Datos de la red urbana
│   ├── interfaz_grafica.py      # Interfaz gráfica con Tkinter
│   └── visualizador.py          # Funciones de visualización
│
├── datos/                        # Directorio para datos adicionales
├── docs/                         # Documentación técnica
├── imagenes/                     # Capturas de pantalla e imágenes
│
├── requirements.txt              # Dependencias del proyecto
└── README.md                     # Este archivo
```

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Clonar o Descargar el Proyecto

```bash
cd 04_proyecto_grafos
```

### Paso 2: Instalar Dependencias

```bash
pip install -r requirements.txt
```

Las dependencias incluyen:
- `networkx` - Para análisis de grafos
- `matplotlib` - Para visualización de grafos
- `tkinter` - Para la interfaz gráfica (viene con Python)
- `pillow` - Para manejo de imágenes

### Paso 3: Ejecutar la Aplicación

```bash
cd src
python main.py
```

O alternativamente:

```bash
python src/main.py
```

---

## 💻 Uso de la Aplicación

### Interfaz Gráfica

La aplicación presenta una interfaz dividida en tres secciones principales:

#### 1. **Panel de Control** (Izquierda)

- **Punto de Origen**: Seleccione la intersección de inicio
- **Punto de Destino**: Seleccione la intersección de destino
- **Criterio de Optimización**:
  - 📏 Distancia más corta (metros)
  - ⏱️ Tiempo más rápido (minutos)
- **Algoritmo de Búsqueda**:
  - Dijkstra (Ruta Óptima)
  - BFS (Búsqueda en Anchura)
  - DFS (Búsqueda en Profundidad)

#### 2. **Visualización del Grafo** (Superior Derecha)

- Muestra la red urbana con todas las intersecciones y calles
- Resalta la ruta encontrada en color rojo
- Punto de inicio en verde, punto de destino en rojo
- Intersecciones intermedias en naranja

#### 3. **Panel de Resultados** (Inferior Derecha)

- Muestra la ruta óptima encontrada
- Detalla cada intersección del recorrido
- Indica la distancia/tiempo total
- Proporciona información paso a paso

### Ejemplo de Uso

1. **Seleccionar Origen**: V14 - Plaza Mayor Alta Vista
2. **Seleccionar Destino**: V13 - Centro Cívico
3. **Elegir Criterio**: Distancia más corta
4. **Elegir Algoritmo**: Dijkstra
5. **Presionar**: 🔍 Buscar Ruta
6. **Observar**: La ruta se visualiza en el mapa y se muestran los detalles

---

## 🧮 Algoritmos Implementados

### 1. **Dijkstra (Camino Más Corto)**

- **Complejidad**: O((|V| + |E|) log |V|)
- **Uso**: Encuentra el camino óptimo según distancia o tiempo
- **Ventaja**: Garantiza la solución óptima
- **Implementación**: Utiliza cola de prioridad (heap)

```python
ruta, coste = grafo.dijkstra(origen, destino, criterio='distancia')
```

### 2. **BFS (Búsqueda en Anchura)**

- **Complejidad**: O(|V| + |E|)
- **Uso**: Verifica conectividad y encuentra camino con menos aristas
- **Ventaja**: Encuentra el camino con menor número de intersecciones
- **Implementación**: Utiliza cola (queue)

```python
encontrado, ruta = grafo.bfs(origen, destino)
```

### 3. **DFS (Búsqueda en Profundidad)**

- **Complejidad**: O(|V| + |E|)
- **Uso**: Explora profundamente la red para encontrar conexión
- **Ventaja**: Útil para análisis de componentes conectadas
- **Implementación**: Recursiva con backtracking

```python
encontrado, ruta = grafo.dfs(origen, destino)
```

---

## 📊 Características del Grafo

### Modelado de Puerto Ordaz

- **15 intersecciones** principales
- **50+ calles dirigidas** (considerando sentido único)
- **Zonas modeladas**:
  - Alta Vista
  - Villa Asia
  - Unare
  - Centro Cívico

### Estructura de Datos

- **Representación**: Listas de adyacencia
- **Tipo**: Grafo dirigido y ponderado
- **Pesos**: (distancia en metros, tiempo en minutos)
- **Ventaja**: Eficiente para grafos dispersos

```python
# Estructura de una arista
adyacencias[origen] = [(destino, distancia, tiempo), ...]
```

---

## 🎨 Características de la Interfaz

- ✅ Interfaz gráfica amigable con Tkinter
- ✅ Visualización interactiva del grafo con Matplotlib
- ✅ Selección intuitiva mediante menús desplegables
- ✅ Resultados detallados en tiempo real
- ✅ Múltiples criterios de optimización
- ✅ Estadísticas del grafo
- ✅ Diseño moderno y profesional

---

## 📁 Descripción de Módulos

### `grafo.py`

Implementa la clase `Grafo` con:
- Estructura de listas de adyacencia
- Algoritmo de Dijkstra con dos criterios
- BFS y DFS para conectividad
- Métodos auxiliares para gestión del grafo

### `datos_puerto_ordaz.py`

Contiene:
- Definición de 15 intersecciones con coordenadas
- Más de 50 calles dirigidas con pesos
- Función para crear el grafo completo
- Puntos de interés de Puerto Ordaz

### `interfaz_grafica.py`

Gestiona:
- Interfaz de usuario con Tkinter
- Interacción con el usuario
- Llamadas a algoritmos de búsqueda
- Actualización de visualización

### `visualizador.py`

Proporciona:
- Funciones para dibujar el grafo
- Resaltado de rutas encontradas
- Formato de información de resultados
- Integración con Matplotlib

### `main.py`

Punto de entrada que:
- Inicializa la aplicación
- Maneja errores globales
- Muestra información de inicio

---

## 🧪 Ejemplos de Prueba

### Caso 1: Ruta Corta

```
Origen: V1 - Av. Guayana con Calle Bolivia
Destino: V6 - Av. Las Américas con Calle Chile
Criterio: Distancia
Resultado: ~900m en 6 intersecciones
```

### Caso 2: Ruta Rápida

```
Origen: V14 - Plaza Mayor Alta Vista
Destino: V13 - Centro Cívico
Criterio: Tiempo
Resultado: ~16 minutos
```

### Caso 3: Verificar Conectividad

```
Origen: V15 - Terminal de Autobuses
Destino: V12 - Av. Villa Asia con Calle Venezuela
Algoritmo: BFS
Resultado: Conectado (5 intersecciones)
```

---

## 📚 Documentación Adicional

Para información técnica detallada, consulte:

- **Documentación Técnica**: `docs/documentacion_tecnica.md`
- **Manual de Usuario**: `docs/manual_usuario.md`
- **Análisis de Complejidad**: `docs/analisis_complejidad.md`

---

## 👥 Autor

Proyecto desarrollado para la materia **Estructura de Datos**  
Universidad - 4to Semestre  
Enero 2026

---

## 📝 Licencia

Este proyecto es de uso educativo y está bajo licencia MIT.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes:

1. Fork el proyecto
2. Cree una rama para su característica
3. Commit sus cambios
4. Push a la rama
5. Abra un Pull Request

---

## 📞 Soporte

Para preguntas o problemas:
- Abra un issue en el repositorio
- Contacte al equipo de desarrollo

---

## 🔄 Versiones

- **v1.0.0** (Enero 2026) - Versión inicial
  - Implementación de Dijkstra, BFS, DFS
  - Interfaz gráfica completa
  - Modelo de Puerto Ordaz

---

## 🙏 Agradecimientos

- Inspirado en sistemas de navegación urbana reales
- Basado en teoría de grafos clásica
- Desarrollado con Python y bibliotecas open source

---

**¡Gracias por usar CityNavigator!** 🗺️✨
