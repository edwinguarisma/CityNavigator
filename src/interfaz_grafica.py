"""
Módulo: interfaz_grafica.py
Descripción: Interfaz gráfica de usuario para CityNavigator
             utilizando Tkinter para interacción amigable
Autor: CityNavigator
Fecha: Enero 2026
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from grafo import Grafo
from datos_puerto_ordaz import crear_grafo_puerto_ordaz, obtener_puntos_interes
from visualizador import dibujar_grafo, mostrar_info_ruta


class AplicacionCityNavigator:
    """
    Clase principal de la aplicación CityNavigator.
    Maneja la interfaz gráfica y la lógica de navegación.
    """
    
    def __init__(self, ventana_principal):
        """
        Inicializa la aplicación.
        
        Args:
            ventana_principal: Ventana raíz de Tkinter
        """
        self.ventana = ventana_principal
        self.ventana.title("CityNavigator - Puerto Ordaz")
        self.ventana.geometry("1400x800")
        self.ventana.configure(bg='#f0f0f0')
        
        # Cargar el grafo de Puerto Ordaz
        self.grafo = crear_grafo_puerto_ordaz()
        self.puntos_interes = obtener_puntos_interes()
        
        # Variables de interfaz
        self.vertice_origen = tk.StringVar()
        self.vertice_destino = tk.StringVar()
        self.criterio_busqueda = tk.StringVar(value='distancia')
        self.algoritmo_seleccionado = tk.StringVar(value='dijkstra')
        
        # Configurar la interfaz
        self.configurar_interfaz()
        
        # Dibujar el grafo inicial
        self.actualizar_visualizacion()
    
    def configurar_interfaz(self):
        """Configura todos los elementos de la interfaz gráfica."""
        
        # ========== PANEL SUPERIOR - TÍTULO ==========
        panel_titulo = tk.Frame(self.ventana, bg='#2c3e50', height=80)
        panel_titulo.pack(fill='x', side='top')
        
        titulo = tk.Label(panel_titulo, 
                         text="🗺️ CityNavigator",
                         font=('Segoe UI', 24, 'bold'),
                         bg='#2c3e50', fg='white')
        titulo.pack(pady=10)
        
        subtitulo = tk.Label(panel_titulo,
                            text="Sistema de Navegación Urbana - Puerto Ordaz, Venezuela",
                            font=('Segoe UI', 12),
                            bg='#2c3e50', fg='#ecf0f1')
        subtitulo.pack()
        
        # ========== PANEL IZQUIERDO - CONTROLES ==========
        panel_controles = tk.Frame(self.ventana, bg='white', width=350, padx=15, pady=15)
        panel_controles.pack(fill='y', side='left', padx=10, pady=10)
        panel_controles.pack_propagate(False)
        
        # Título de controles
        tk.Label(panel_controles,
                text="⚙️ Panel de Control",
                font=('Segoe UI', 14, 'bold'),
                bg='white').pack(pady=(0, 15))
        
        # ===== SECCIÓN: Selección de Origen =====
        frame_origen = tk.LabelFrame(panel_controles, text="📍 Punto de Origen",
                                     font=('Segoe UI', 10, 'bold'),
                                     bg='white', padx=10, pady=10)
        frame_origen.pack(fill='x', pady=(0, 10))
        
        self.combo_origen = ttk.Combobox(frame_origen,
                                        textvariable=self.vertice_origen,
                                        values=self.obtener_lista_vertices(),
                                        state='readonly',
                                        font=('Segoe UI', 9),
                                        width=30)
        self.combo_origen.pack(pady=5)
        self.combo_origen.set("Seleccione origen...")
        
        # ===== SECCIÓN: Selección de Destino =====
        frame_destino = tk.LabelFrame(panel_controles, text="📍 Punto de Destino",
                                      font=('Segoe UI', 10, 'bold'),
                                      bg='white', padx=10, pady=10)
        frame_destino.pack(fill='x', pady=(0, 10))
        
        self.combo_destino = ttk.Combobox(frame_destino,
                                         textvariable=self.vertice_destino,
                                         values=self.obtener_lista_vertices(),
                                         state='readonly',
                                         font=('Segoe UI', 9),
                                         width=30)
        self.combo_destino.pack(pady=5)
        self.combo_destino.set("Seleccione destino...")
        
        # ===== SECCIÓN: Criterio de Búsqueda =====
        frame_criterio = tk.LabelFrame(panel_controles, text="🎯 Criterio de Optimización",
                                       font=('Segoe UI', 10, 'bold'),
                                       bg='white', padx=10, pady=10)
        frame_criterio.pack(fill='x', pady=(0, 10))
        
        tk.Radiobutton(frame_criterio,
                      text="📏 Distancia más corta (metros)",
                      variable=self.criterio_busqueda,
                      value='distancia',
                      bg='white',
                      font=('Segoe UI', 9)).pack(anchor='w', pady=2)
        
        tk.Radiobutton(frame_criterio,
                      text="⏱️ Tiempo más rápido (minutos)",
                      variable=self.criterio_busqueda,
                      value='tiempo',
                      bg='white',
                      font=('Segoe UI', 9)).pack(anchor='w', pady=2)
        
        # ===== SECCIÓN: Algoritmo =====
        frame_algoritmo = tk.LabelFrame(panel_controles, text="🔍 Algoritmo de Búsqueda",
                                        font=('Segoe UI', 10, 'bold'),
                                        bg='white', padx=10, pady=10)
        frame_algoritmo.pack(fill='x', pady=(0, 10))
        
        tk.Radiobutton(frame_algoritmo,
                      text="Dijkstra (Ruta Óptima)",
                      variable=self.algoritmo_seleccionado,
                      value='dijkstra',
                      bg='white',
                      font=('Segoe UI', 9)).pack(anchor='w', pady=2)
        
        tk.Radiobutton(frame_algoritmo,
                      text="BFS (Búsqueda en Anchura)",
                      variable=self.algoritmo_seleccionado,
                      value='bfs',
                      bg='white',
                      font=('Segoe UI', 9)).pack(anchor='w', pady=2)
        
        tk.Radiobutton(frame_algoritmo,
                      text="DFS (Búsqueda en Profundidad)",
                      variable=self.algoritmo_seleccionado,
                      value='dfs',
                      bg='white',
                      font=('Segoe UI', 9)).pack(anchor='w', pady=2)
        
        # ===== BOTONES DE ACCIÓN =====
        frame_botones = tk.Frame(panel_controles, bg='white')
        frame_botones.pack(fill='x', pady=(15, 10))
        
        boton_buscar = tk.Button(frame_botones,
                                text="🔍 Buscar Ruta",
                                command=self.buscar_ruta,
                                bg='#27ae60',
                                fg='white',
                                font=('Segoe UI', 11, 'bold'),
                                cursor='hand2',
                                relief='raised',
                                bd=2)
        boton_buscar.pack(fill='x', pady=5)
        
        boton_limpiar = tk.Button(frame_botones,
                                 text="🔄 Limpiar",
                                 command=self.limpiar_resultados,
                                 bg='#e74c3c',
                                 fg='white',
                                 font=('Segoe UI', 10),
                                 cursor='hand2',
                                 relief='raised',
                                 bd=2)
        boton_limpiar.pack(fill='x', pady=5)
        
        boton_estadisticas = tk.Button(frame_botones,
                                      text="📊 Estadísticas del Grafo",
                                      command=self.mostrar_estadisticas,
                                      bg='#3498db',
                                      fg='white',
                                      font=('Segoe UI', 10),
                                      cursor='hand2',
                                      relief='raised',
                                      bd=2)
        boton_estadisticas.pack(fill='x', pady=5)
        
        # ===== INFORMACIÓN DEL PROYECTO =====
        frame_info = tk.Frame(panel_controles, bg='#ecf0f1', bd=2, relief='groove')
        frame_info.pack(fill='x', side='bottom', pady=(10, 0))
        
        tk.Label(frame_info,
                text="ℹ️ Información",
                font=('Segoe UI', 9, 'bold'),
                bg='#ecf0f1').pack(pady=(5, 2))
        
        tk.Label(frame_info,
                text="Proyecto: Grafos Urbanos\nEstructura de Datos\n2026",
                font=('Segoe UI', 8),
                bg='#ecf0f1',
                justify='center').pack(pady=(0, 5))
        
        # ========== PANEL DERECHO - VISUALIZACIÓN Y RESULTADOS ==========
        panel_derecho = tk.Frame(self.ventana, bg='#f0f0f0')
        panel_derecho.pack(fill='both', expand=True, side='right', padx=(0, 10), pady=10)
        
        # ===== VISUALIZACIÓN DEL GRAFO =====
        frame_grafico = tk.LabelFrame(panel_derecho,
                                      text="🗺️ Visualización de la Red Urbana",
                                      font=('Segoe UI', 11, 'bold'),
                                      bg='white',
                                      padx=10, pady=10)
        frame_grafico.pack(fill='both', expand=True, pady=(0, 10))
        
        # Crear figura de matplotlib
        self.figura = Figure(figsize=(10, 6), dpi=100)
        self.ax = self.figura.add_subplot(111)
        
        # Canvas para el gráfico
        self.canvas = FigureCanvasTkAgg(self.figura, frame_grafico)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # ===== PANEL DE RESULTADOS =====
        frame_resultados = tk.LabelFrame(panel_derecho,
                                        text="📋 Resultados de la Búsqueda",
                                        font=('Segoe UI', 11, 'bold'),
                                        bg='white',
                                        padx=10, pady=10)
        frame_resultados.pack(fill='both', pady=(0, 0))
        
        self.texto_resultados = scrolledtext.ScrolledText(frame_resultados,
                                                          height=12,
                                                          font=('Consolas', 9),
                                                          wrap=tk.WORD,
                                                          bg='#f9f9f9')
        self.texto_resultados.pack(fill='both', expand=True)
        
        # Mensaje inicial
        self.texto_resultados.insert('1.0', 
            "Bienvenido a CityNavigator 🗺️\n\n"
            "Seleccione un punto de origen y destino para comenzar.\n"
            "Luego elija el criterio de optimización y presione 'Buscar Ruta'.\n\n"
            "El sistema encontrará la mejor ruta según sus preferencias.")
    
    def obtener_lista_vertices(self):
        """
        Genera una lista formateada de vértices para los combobox.
        
        Returns:
            list: Lista de strings con formato "ID - Nombre"
        """
        vertices = []
        for vertice in sorted(self.grafo.vertices):
            nombre = self.grafo.nombres_vertices.get(vertice, vertice)
            vertices.append(f"{vertice} - {nombre}")
        return vertices
    
    def extraer_id_vertice(self, texto_combo):
        """
        Extrae el ID del vértice del texto del combobox.
        
        Args:
            texto_combo: Texto del formato "ID - Nombre"
            
        Returns:
            str: ID del vértice
        """
        if " - " in texto_combo:
            return texto_combo.split(" - ")[0]
        return texto_combo
    
    def buscar_ruta(self):
        """Ejecuta el algoritmo de búsqueda de ruta seleccionado."""
        # Validar selecciones
        origen_texto = self.vertice_origen.get()
        destino_texto = self.vertice_destino.get()
        
        if "Seleccione" in origen_texto or "Seleccione" in destino_texto:
            messagebox.showwarning("Advertencia", 
                                  "Por favor seleccione origen y destino")
            return
        
        # Extraer IDs de vértices
        origen = self.extraer_id_vertice(origen_texto)
        destino = self.extraer_id_vertice(destino_texto)
        
        if origen == destino:
            messagebox.showinfo("Información",
                               "El origen y destino son el mismo punto")
            return
        
        # Ejecutar el algoritmo seleccionado
        algoritmo = self.algoritmo_seleccionado.get()
        
        if algoritmo == 'dijkstra':
            criterio = self.criterio_busqueda.get()
            ruta, coste = self.grafo.dijkstra(origen, destino, criterio)
            self.mostrar_resultados_dijkstra(ruta, coste, criterio)
        elif algoritmo == 'bfs':
            encontrado, ruta = self.grafo.bfs(origen, destino)
            self.mostrar_resultados_busqueda(ruta, encontrado, 'BFS')
        elif algoritmo == 'dfs':
            encontrado, ruta = self.grafo.dfs(origen, destino)
            self.mostrar_resultados_busqueda(ruta, encontrado, 'DFS')
    
    def mostrar_resultados_dijkstra(self, ruta, coste, criterio):
        """
        Muestra los resultados del algoritmo de Dijkstra.
        
        Args:
            ruta: Lista de vértices de la ruta
            coste: Coste total de la ruta
            criterio: Criterio usado ('distancia' o 'tiempo')
        """
        # Limpiar resultados anteriores
        self.texto_resultados.delete('1.0', tk.END)
        
        # Generar texto de resultados
        texto = mostrar_info_ruta(ruta, coste, criterio, self.grafo)
        self.texto_resultados.insert('1.0', texto)
        
        # Actualizar visualización con la ruta
        self.actualizar_visualizacion(ruta)
        
        # Mostrar notificación
        if ruta and coste != float('inf'):
            messagebox.showinfo("✅ Ruta Encontrada",
                               f"Se encontró una ruta óptima con {len(ruta)} intersecciones")
    
    def mostrar_resultados_busqueda(self, ruta, encontrado, nombre_algoritmo):
        """
        Muestra los resultados de BFS o DFS.
        
        Args:
            ruta: Lista de vértices de la ruta
            encontrado: Boolean indicando si se encontró conexión
            nombre_algoritmo: Nombre del algoritmo usado
        """
        self.texto_resultados.delete('1.0', tk.END)
        
        if encontrado:
            texto = f"✅ CONEXIÓN ENCONTRADA ({nombre_algoritmo})\n"
            texto += "=" * 50 + "\n\n"
            texto += f"📍 Número de intersecciones: {len(ruta)}\n\n"
            texto += f"🗺️ RECORRIDO:\n"
            texto += "-" * 50 + "\n\n"
            
            for i, vertice in enumerate(ruta):
                nombre = self.grafo.nombres_vertices.get(vertice, vertice)
                texto += f"{i+1}. {vertice}: {nombre}\n"
            
            texto += f"\n⚠️ Nota: {nombre_algoritmo} encuentra un camino pero no "
            texto += "garantiza que sea el más corto u óptimo."
        else:
            texto = f"❌ NO SE ENCONTRÓ CONEXIÓN ({nombre_algoritmo})\n\n"
            texto += "No existe un camino entre el origen y destino seleccionados.\n"
            texto += "Esto puede deberse a calles de un solo sentido que no permiten la conexión."
        
        self.texto_resultados.insert('1.0', texto)
        self.actualizar_visualizacion(ruta if encontrado else None)
        
        if encontrado:
            messagebox.showinfo("✅ Conexión Encontrada",
                               f"Se encontró un camino con {len(ruta)} intersecciones")
        else:
            messagebox.showwarning("❌ Sin Conexión",
                                  "No existe un camino entre los puntos seleccionados")
    
    def limpiar_resultados(self):
        """Limpia los resultados y resetea la visualización."""
        self.texto_resultados.delete('1.0', tk.END)
        self.texto_resultados.insert('1.0',
            "Resultados limpiados.\n\n"
            "Seleccione nuevos puntos para buscar otra ruta.")
        
        self.combo_origen.set("Seleccione origen...")
        self.combo_destino.set("Seleccione destino...")
        self.actualizar_visualizacion()
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas del grafo en una ventana emergente."""
        stats = self.grafo.obtener_estadisticas()
        
        mensaje = f"""📊 ESTADÍSTICAS DE LA RED URBANA
        
🔹 Número de intersecciones: {stats['num_vertices']}
🔹 Número de calles (dirigidas): {stats['num_aristas']}
🔹 Densidad del grafo: {stats['densidad']:.3f}

📍 Puntos de Interés:
"""
        
        for categoria, lugares in self.puntos_interes.items():
            mensaje += f"\n{categoria}:\n"
            for nombre in lugares.keys():
                mensaje += f"  • {nombre}\n"
        
        messagebox.showinfo("Estadísticas del Grafo", mensaje)
    
    def actualizar_visualizacion(self, ruta=None):
        """
        Actualiza la visualización del grafo.
        
        Args:
            ruta: Lista opcional de vértices para resaltar
        """
        dibujar_grafo(self.grafo, self.ax, ruta)
        self.canvas.draw()


def iniciar_aplicacion():
    """Función principal para iniciar la aplicación."""
    ventana_principal = tk.Tk()
    app = AplicacionCityNavigator(ventana_principal)
    ventana_principal.mainloop()


if __name__ == "__main__":
    iniciar_aplicacion()
