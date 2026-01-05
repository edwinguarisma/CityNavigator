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
from modal_resultados import crear_modal_resultados


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
        self.ventana.geometry("1600x900")  # Ventana más grande
        self.ventana.state('zoomed')  # Maximizar ventana al iniciar
        self.ventana.configure(bg='#f0f0f0')
        
        # Cargar el grafo de Puerto Ordaz
        self.grafo = crear_grafo_puerto_ordaz()
        self.puntos_interes = obtener_puntos_interes()
        
        # Variables de interfaz
        self.vertice_origen = tk.StringVar()
        self.vertice_destino = tk.StringVar()
        self.criterio_busqueda = tk.StringVar(value='distancia')
        self.algoritmo_seleccionado = tk.StringVar(value='dijkstra')
        
        # Variables para resultados
        self.ultima_ruta = None
        self.ultimo_coste = None
        self.ultimo_criterio = None
        self.ultimo_algoritmo = None
        
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
        panel_controles = tk.Frame(self.ventana, bg='white', width=400, padx=15, pady=15)
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
                                        width=35)
        self.combo_origen.pack(pady=5, fill='x')
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
                                         width=35)
        self.combo_destino.pack(pady=5, fill='x')
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
        
        # ===== BOTÓN VER RESULTADOS (OCULTO INICIALMENTE) =====
        self.boton_ver_resultados = tk.Button(frame_botones,
                                              text="📋 Ver Detalles",
                                              command=self.mostrar_modal_resultados,
                                              bg='#9b59b6',
                                              fg='white',
                                              font=('Segoe UI', 11, 'bold'),
                                              cursor='hand2',
                                              relief='raised',
                                              bd=2,
                                              state='disabled')  # Deshabilitado inicialmente
        self.boton_ver_resultados.pack(fill='x', pady=5)
        
        # ===== INFORMACIÓN DEL PROYECTO =====
        # frame_info = tk.Frame(panel_controles, bg='#ecf0f1', bd=2, relief='groove')
        # frame_info.pack(fill='x', side='bottom', pady=(10, 0))
        
        # tk.Label(frame_info,
        #         text="ℹ️ Información",
        #         font=('Segoe UI', 9, 'bold'),
        #         bg='#ecf0f1').pack(pady=(5, 2))
        
        # tk.Label(frame_info,
        #         text="Proyecto: Grafos Urbanos\nEstructura de Datos\n2026",
        #         font=('Segoe UI', 8),
        #         bg='#ecf0f1',
        #         justify='center').pack(pady=(0, 5))
        
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
        
        # Crear figura de matplotlib con mejor tamaño
        self.figura = Figure(figsize=(12, 7), dpi=100)
        self.ax = self.figura.add_subplot(111)
        self.figura.tight_layout(pad=3.0)
        
        # Canvas para el gráfico
        self.canvas = FigureCanvasTkAgg(self.figura, frame_grafico)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def obtener_lista_vertices(self):
        """
        Genera una lista formateada de vértices para los combobox.
        
        Returns:
            list: Lista de strings con formato "ID - Nombre"
        """
        vertices = []
        for vertice in sorted(self.grafo.vertices):
            nombre = self.grafo.nombres_vertices.get(vertice, vertice)
            # Acortar nombres muy largos para mejor visualización
            if len(nombre) > 40:
                nombre = nombre[:37] + "..."
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
        # Guardar resultados para el modal
        self.ultima_ruta = ruta
        self.ultimo_coste = coste
        self.ultimo_criterio = criterio
        self.ultimo_algoritmo = 'Dijkstra'
        
        # Actualizar visualización con la ruta
        self.actualizar_visualizacion(ruta)
        
        # Habilitar botón de resultados
        self.boton_ver_resultados.config(state='normal', bg='#9b59b6')
        
        # Mostrar notificación
        if ruta and coste != float('inf'):
            if criterio == 'distancia':
                mensaje = f"Ruta encontrada: {coste:.0f} metros ({len(ruta)} intersecciones)"
            else:
                mensaje = f"Ruta encontrada: {coste:.1f} minutos ({len(ruta)} intersecciones)"
            messagebox.showinfo("✅ Ruta Encontrada", mensaje)
        else:
            messagebox.showwarning("❌ Sin Ruta", "No se encontró una ruta entre los puntos seleccionados")
    
    def mostrar_resultados_busqueda(self, ruta, encontrado, nombre_algoritmo):
        """
        Muestra los resultados de BFS o DFS.
        
        Args:
            ruta: Lista de vértices de la ruta
            encontrado: Boolean indicando si se encontró conexión
            nombre_algoritmo: Nombre del algoritmo usado
        """
        # Guardar resultados para el modal
        self.ultima_ruta = ruta if encontrado else []
        self.ultimo_coste = len(ruta) if encontrado else float('inf')
        self.ultimo_criterio = 'conexion'
        self.ultimo_algoritmo = nombre_algoritmo
        
        # Actualizar visualización
        self.actualizar_visualizacion(ruta if encontrado else None)
        
        # Habilitar botón de resultados si se encontró ruta
        if encontrado:
            self.boton_ver_resultados.config(state='normal', bg='#9b59b6')
        else:
            self.boton_ver_resultados.config(state='disabled', bg='#cccccc')
        
        # Mostrar notificación
        if encontrado:
            messagebox.showinfo("✅ Conexión Encontrada",
                               f"Se encontró un camino con {len(ruta)} intersecciones\n\n"
                               f"Presione 'Ver Detalles de la Ruta' para más información")
        else:
            messagebox.showwarning("❌ Sin Conexión",
                                  "No existe un camino entre los puntos seleccionados")
    
    def limpiar_resultados(self):
        """Limpia los resultados y resetea la visualización."""
        # Deshabilitar botón de resultados
        self.boton_ver_resultados.config(state='disabled', bg='#cccccc')
        
        # Limpiar variables de resultados
        self.ultima_ruta = None
        self.ultimo_coste = None
        self.ultimo_criterio = None
        self.ultimo_algoritmo = None
        
        # Resetear selecciones
        self.combo_origen.set("Seleccione origen...")
        self.combo_destino.set("Seleccione destino...")
        
        # Actualizar visualización
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
    
    def mostrar_modal_resultados(self):
        """Muestra la ventana modal con los detalles de la ruta."""
        if self.ultima_ruta is None:
            messagebox.showwarning("Sin Resultados",
                                  "No hay resultados para mostrar.\n"
                                  "Primero busque una ruta.")
            return
        
        crear_modal_resultados(
            self.ventana,
            self.ultima_ruta,
            self.ultimo_coste,
            self.ultimo_criterio,
            self.ultimo_algoritmo,
            self.grafo
        )
    
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
