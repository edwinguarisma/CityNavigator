"""
Módulo: interfaz_grafica.py
Descripción: Interfaz gráfica de usuario para CityNavigator
             utilizando Tkinter para interacción amigable
Autor: CityNavigator
Fecha: Enero 2026
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from grafo import Grafo
from datos_puerto_ordaz import crear_grafo_puerto_ordaz, obtener_puntos_interes
from visualizador import dibujar_grafo, mostrar_info_ruta
from modal_resultados import crear_modal_resultados
from persistencia import GestorPersistencia


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
        
        # Modos de edición
        self.modo_agregar_nodo = False
        self.modo_conectar_nodos = False
        self.nodo_origen_conexion = None
        
        # Gestor de persistencia
        self.gestor_persistencia = GestorPersistencia()
        
        # Configurar la interfaz
        self.configurar_interfaz()
        
        # Dibujar el grafo inicial
        self.actualizar_visualizacion()
        
        # Conectar evento de clic en el mapa
        self.canvas.mpl_connect('button_press_event', self.on_click_mapa)
    
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
        
        # ========== PANEL IZQUIERDO - CONTROLES CON SCROLL ==========
        # Frame contenedor fijo
        contenedor_panel = tk.Frame(self.ventana, bg='white', width=400)
        contenedor_panel.pack(fill='y', side='left', padx=10, pady=10)
        contenedor_panel.pack_propagate(False)
        
        # Título fijo arriba
        tk.Label(contenedor_panel,
                text="⚙️ Panel de Control",
                font=('Segoe UI', 14, 'bold'),
                bg='white').pack(pady=10)
        
        # Canvas con scrollbar para el contenido
        canvas_controles = tk.Canvas(contenedor_panel, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(contenedor_panel, orient='vertical', command=canvas_controles.yview)
        
        # Frame interior donde van todos los controles
        panel_controles = tk.Frame(canvas_controles, bg='white', padx=15, pady=5)
        
        # Configurar canvas
        panel_controles.bind(
            '<Configure>',
            lambda e: canvas_controles.configure(scrollregion=canvas_controles.bbox('all'))
        )
        
        canvas_controles.create_window((0, 0), window=panel_controles, anchor='nw')
        canvas_controles.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar canvas y scrollbar
        scrollbar.pack(side='right', fill='y')
        canvas_controles.pack(side='left', fill='both', expand=True)
        
        # Habilitar scroll con rueda del mouse
        def on_mousewheel(event):
            canvas_controles.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def on_mousewheel_linux(event):
            canvas_controles.yview_scroll(-1, "units")
        
        def on_mousewheel_linux_down(event):
            canvas_controles.yview_scroll(1, "units")
        
        # Bind para Windows/Mac
        canvas_controles.bind_all("<MouseWheel>", on_mousewheel)
        # Bind para Linux
        canvas_controles.bind_all("<Button-4>", on_mousewheel_linux)
        canvas_controles.bind_all("<Button-5>", on_mousewheel_linux_down)
        
        # ===== SECCIÓN: Selección de Origen =====
        frame_origen = tk.LabelFrame(panel_controles, text="📍 Punto de Origen",
                                     font=('Segoe UI', 10, 'bold'),
                                     bg='white', padx=10, pady=5)
        frame_origen.pack(fill='x', pady=(0, 8))
        
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
                                      bg='white', padx=10, pady=5)
        frame_destino.pack(fill='x', pady=(0, 8))
        
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
                                       bg='white', padx=10, pady=5)
        frame_criterio.pack(fill='x', pady=(0, 8))
        
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
                                        bg='white', padx=10, pady=5)
        frame_algoritmo.pack(fill='x', pady=(0, 8))
        
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
        frame_botones.pack(fill='x', pady=(10, 5))
        
        boton_buscar = tk.Button(frame_botones,
                                text="🔍 Buscar Ruta",
                                command=self.buscar_ruta,
                                bg='#27ae60',
                                fg='white',
                                font=('Segoe UI', 10, 'bold'),
                                cursor='hand2',
                                relief='raised',
                                bd=2)
        boton_buscar.pack(fill='x', pady=3)
        
        boton_limpiar = tk.Button(frame_botones,
                                 text="🔄 Limpiar",
                                 command=self.limpiar_resultados,
                                 bg='#e74c3c',
                                 fg='white',
                                 font=('Segoe UI', 9),
                                 cursor='hand2',
                                 relief='raised',
                                 bd=2)
        boton_limpiar.pack(fill='x', pady=3)
        
        boton_estadisticas = tk.Button(frame_botones,
                                      text="📊 Estadísticas del Grafo",
                                      command=self.mostrar_estadisticas,
                                      bg='#3498db',
                                      fg='white',
                                      font=('Segoe UI', 9),
                                      cursor='hand2',
                                      relief='raised',
                                      bd=2)
        boton_estadisticas.pack(fill='x', pady=3)
        
        # ===== BOTÓN VER RESULTADOS (OCULTO INICIALMENTE) =====
        self.boton_ver_resultados = tk.Button(frame_botones,
                                              text="📋 Ver Detalles",
                                              command=self.mostrar_modal_resultados,
                                              bg='#9b59b6',
                                              fg='white',
                                              font=('Segoe UI', 9, 'bold'),
                                              cursor='hand2',
                                              relief='raised',
                                              bd=2,
                                              state='disabled')  # Deshabilitado inicialmente
        self.boton_ver_resultados.pack(fill='x', pady=3)
        
        # ===== BOTÓN AGREGAR NODO =====
        self.boton_agregar_nodo = tk.Button(frame_botones,
                                            text="➕ Agregar Nodo",
                                            command=self.toggle_modo_agregar_nodo,
                                            bg='#f39c12',
                                            fg='white',
                                            font=('Segoe UI', 9),
                                            cursor='hand2',
                                            relief='raised',
                                            bd=2)
        self.boton_agregar_nodo.pack(fill='x', pady=3)
        
        # ===== BOTÓN CONECTAR NODOS =====
        self.boton_conectar_nodos = tk.Button(frame_botones,
                                              text="🔗 Conectar Nodos",
                                              command=self.toggle_modo_conectar_nodos,
                                              bg='#16a085',
                                              fg='white',
                                              font=('Segoe UI', 9),
                                              cursor='hand2',
                                              relief='raised',
                                              bd=2)
        self.boton_conectar_nodos.pack(fill='x', pady=3)
        
        # ===== BOTÓN GESTIONAR DATOS =====
        self.boton_gestionar = tk.Button(frame_botones,
                                         text="⚙️ Gestionar Datos",
                                         command=self.abrir_ventana_gestion,
                                         bg='#8e44ad',
                                         fg='white',
                                         font=('Segoe UI', 9),
                                         cursor='hand2',
                                         relief='raised',
                                         bd=2)
        self.boton_gestionar.pack(fill='x', pady=3)
        
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
    
    def toggle_modo_agregar_nodo(self):
        """Activa/desactiva el modo de agregar nodos."""
        self.modo_agregar_nodo = not self.modo_agregar_nodo
        
        if self.modo_agregar_nodo:
            self.boton_agregar_nodo.config(bg='#e67e22', text="✖ Cancelar Agregar")
            messagebox.showinfo("Modo Agregar Nodo",
                              "Haga clic en el mapa donde desea agregar un nuevo nodo.\n\n"
                              "Se le pedirá el nombre del nodo después de hacer clic.")
        else:
            self.boton_agregar_nodo.config(bg='#f39c12', text="➕ Agregar Nodo")
    
    def toggle_modo_conectar_nodos(self):
        """Activa/desactiva el modo de conectar nodos."""
        self.modo_conectar_nodos = not self.modo_conectar_nodos
        
        if self.modo_conectar_nodos:
            self.boton_conectar_nodos.config(bg='#138d75', text="✖ Cancelar Conectar")
            self.nodo_origen_conexion = None
            messagebox.showinfo("Modo Conectar Nodos",
                              "Haga clic en el PRIMER nodo (origen).\n"
                              "Luego haga clic en el SEGUNDO nodo (destino).\n\n"
                              "Se le pedirá la distancia y tiempo de la conexión.")
        else:
            self.boton_conectar_nodos.config(bg='#16a085', text="🔗 Conectar Nodos")
            self.nodo_origen_conexion = None
    
    def on_click_mapa(self, event):
        """
        Maneja el clic en el mapa para agregar nodos o conectarlos.
        
        Args:
            event: Evento de clic de matplotlib
        """
        # Verificar que el clic es dentro del gráfico
        if event.inaxes != self.ax:
            return
        
        # MODO AGREGAR NODO
        if self.modo_agregar_nodo:
            self.agregar_nodo_en_posicion(event.xdata, event.ydata)
            return
        
        # MODO CONECTAR NODOS
        if self.modo_conectar_nodos:
            self.conectar_nodo_en_posicion(event.xdata, event.ydata)
            return
    
    def agregar_nodo_en_posicion(self, lon, lat):
        """Agrega un nodo en la posición especificada."""
        
        # Pedir nombre del nodo
        nombre = simpledialog.askstring(
            "Nuevo Nodo",
            f"Ingrese el nombre del nodo:\n\nCoordenadas: ({lon:.4f}, {lat:.4f})",
            parent=self.ventana
        )
        
        if nombre and nombre.strip():
            # Generar ID único basado en el nombre
            id_nodo = nombre.strip().replace(" ", "_")
            
            # Verificar que no exista
            contador = 1
            id_original = id_nodo
            while id_nodo in self.grafo.vertices:
                id_nodo = f"{id_original}_{contador}"
                contador += 1
            
            # Agregar el nodo al grafo
            self.grafo.agregar_vertice(id_nodo, nombre.strip(), (lon, lat))
            
            # GUARDAR EN PERSISTENCIA
            self.gestor_persistencia.agregar_nodo(id_nodo, nombre.strip(), (lon, lat))
            
            # Actualizar la lista de vértices en los combobox
            self.combo_origen['values'] = self.obtener_lista_vertices()
            self.combo_destino['values'] = self.obtener_lista_vertices()
            
            # Actualizar visualización
            self.actualizar_visualizacion()
            
            # Desactivar modo agregar
            self.modo_agregar_nodo = False
            self.boton_agregar_nodo.config(bg='#f39c12', text="➕ Agregar Nodo")
            
            messagebox.showinfo("Nodo Agregado",
                              f"✅ Nodo '{nombre}' agregado exitosamente\n\n"
                              f"ID: {id_nodo}\n"
                              f"Coordenadas: ({lon:.4f}, {lat:.4f})\n\n"
                              f"Ahora puede conectarlo con otros nodos.\n\n"
                              f"💾 Guardado automáticamente.")
        else:
            # Cancelar si no se ingresó nombre
            self.modo_agregar_nodo = False
            self.boton_agregar_nodo.config(bg='#f39c12', text="➕ Agregar Nodo")
    
    def conectar_nodo_en_posicion(self, lon, lat):
        """Conecta nodos haciendo clic en ellos."""
        # Encontrar el nodo más cercano al clic
        nodo_cercano = None
        distancia_minima = float('inf')
        
        for vertice in self.grafo.vertices:
            x, y = self.grafo.coordenadas.get(vertice, (0, 0))
            distancia = ((x - lon)**2 + (y - lat)**2)**0.5
            if distancia < distancia_minima:
                distancia_minima = distancia
                nodo_cercano = vertice
        
        # Umbral de cercanía (ajustar según necesidad)
        umbral = 0.01
        if distancia_minima > umbral:
            messagebox.showwarning("Nodo No Encontrado",
                                  "No hay ningún nodo cerca del clic.\n"
                                  "Haga clic más cerca de un nodo.")
            return
        
        # Si es el primer nodo (origen)
        if self.nodo_origen_conexion is None:
            self.nodo_origen_conexion = nodo_cercano
            nombre_origen = self.grafo.nombres_vertices.get(nodo_cercano, nodo_cercano)
            messagebox.showinfo("Nodo Origen Seleccionado",
                              f"✅ Nodo origen: {nombre_origen}\n\n"
                              f"Ahora haga clic en el nodo DESTINO.")
        else:
            # Es el segundo nodo (destino)
            nodo_destino = nodo_cercano
            
            # No permitir conectar un nodo consigo mismo
            if self.nodo_origen_conexion == nodo_destino:
                messagebox.showwarning("Nodos Iguales",
                                      "No puede conectar un nodo consigo mismo.\n"
                                      "Seleccione un nodo diferente.")
                return
            
            # Pedir distancia y tiempo
            distancia = simpledialog.askfloat(
                "Distancia",
                f"Ingrese la distancia en metros:\n\n"
                f"De: {self.grafo.nombres_vertices.get(self.nodo_origen_conexion, self.nodo_origen_conexion)}\n"
                f"A: {self.grafo.nombres_vertices.get(nodo_destino, nodo_destino)}",
                parent=self.ventana,
                minvalue=0.0
            )
            
            if distancia is None:
                self.nodo_origen_conexion = None
                return
            
            tiempo = simpledialog.askfloat(
                "Tiempo",
                f"Ingrese el tiempo en minutos:",
                parent=self.ventana,
                minvalue=0.0
            )
            
            if tiempo is None:
                self.nodo_origen_conexion = None
                return
            
            # Agregar la arista
            self.grafo.agregar_arista(self.nodo_origen_conexion, nodo_destino, distancia, tiempo)
            
            # GUARDAR EN PERSISTENCIA
            self.gestor_persistencia.agregar_conexion(
                self.nodo_origen_conexion, nodo_destino, distancia, tiempo
            )
            
            # Actualizar visualización
            self.actualizar_visualizacion()
            
            # Resetear
            nombre_origen = self.grafo.nombres_vertices.get(self.nodo_origen_conexion, self.nodo_origen_conexion)
            nombre_destino = self.grafo.nombres_vertices.get(nodo_destino, nodo_destino)
            
            self.nodo_origen_conexion = None
            self.modo_conectar_nodos = False
            self.boton_conectar_nodos.config(bg='#16a085', text="🔗 Conectar Nodos")
            
            messagebox.showinfo("Conexión Agregada",
                              f"✅ Conexión agregada exitosamente\n\n"
                              f"De: {nombre_origen}\n"
                              f"A: {nombre_destino}\n"
                              f"Distancia: {distancia} metros\n"
                              f"Tiempo: {tiempo} minutos\n\n"
                              f"💾 Guardado automáticamente.")
    
    def abrir_ventana_gestion(self):
        """Abre una ventana para gestionar (editar/eliminar) nodos y conexiones personalizadas."""
        ventana_gestion = tk.Toplevel(self.ventana)
        ventana_gestion.title("⚙️ Gestionar Datos Personalizados")
        ventana_gestion.geometry("700x600")
        ventana_gestion.configure(bg='white')
        
        # Título
        tk.Label(ventana_gestion,
                text="⚙️ Gestionar Datos Personalizados",
                font=('Segoe UI', 16, 'bold'),
                bg='white').pack(pady=15)
        
        # Notebook (pestañas)
        notebook = ttk.Notebook(ventana_gestion)
        notebook.pack(fill='both', expand=True, padx=15, pady=10)
        
        # ===== PESTAÑA: NODOS =====
        frame_nodos = tk.Frame(notebook, bg='white')
        notebook.add(frame_nodos, text='📍 Nodos Personalizados')
        
        tk.Label(frame_nodos,
                text="Nodos creados por usted:",
                font=('Segoe UI', 11, 'bold'),
                bg='white').pack(pady=10)
        
        # Listbox con nodos
        frame_lista_nodos = tk.Frame(frame_nodos, bg='white')
        frame_lista_nodos.pack(fill='both', expand=True, padx=15, pady=5)
        
        scrollbar_nodos = tk.Scrollbar(frame_lista_nodos)
        scrollbar_nodos.pack(side='right', fill='y')
        
        listbox_nodos = tk.Listbox(frame_lista_nodos,
                                   yscrollcommand=scrollbar_nodos.set,
                                   font=('Segoe UI', 10),
                                   height=15)
        listbox_nodos.pack(side='left', fill='both', expand=True)
        scrollbar_nodos.config(command=listbox_nodos.yview)
        
        # Cargar nodos personalizados
        nodos_personalizados = self.gestor_persistencia.obtener_nodos()
        for nodo in nodos_personalizados:
            listbox_nodos.insert(tk.END, f"{nodo['nombre']} (ID: {nodo['id']})")
        
        # Botones para nodos
        frame_botones_nodos = tk.Frame(frame_nodos, bg='white')
        frame_botones_nodos.pack(pady=10)
        
        def editar_nodo():
            seleccion = listbox_nodos.curselection()
            if not seleccion:
                messagebox.showwarning("Sin Selección", "Seleccione un nodo para editar.")
                return
            
            idx = seleccion[0]
            nodo = nodos_personalizados[idx]
            
            # Pedir nuevo nombre
            nuevo_nombre = simpledialog.askstring(
                "Editar Nodo",
                f"Nombre actual: {nodo['nombre']}\n\nIngrese el nuevo nombre:",
                initialvalue=nodo['nombre'],
                parent=ventana_gestion
            )
            
            if nuevo_nombre and nuevo_nombre.strip():
                self.gestor_persistencia.editar_nodo(nodo['id'], nuevo_nombre=nuevo_nombre.strip())
                messagebox.showinfo("Éxito", "Nodo editado correctamente.\n\nReinicie la aplicación para ver los cambios.")
                ventana_gestion.destroy()
        
        def eliminar_nodo():
            seleccion = listbox_nodos.curselection()
            if not seleccion:
                messagebox.showwarning("Sin Selección", "Seleccione un nodo para eliminar.")
                return
            
            idx = seleccion[0]
            nodo = nodos_personalizados[idx]
            
            confirmar = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro de eliminar el nodo '{nodo['nombre']}'?\n\n"
                f"Se eliminarán también todas sus conexiones."
            )
            
            if confirmar:
                self.gestor_persistencia.eliminar_nodo(nodo['id'])
                messagebox.showinfo("Éxito", "Nodo eliminado correctamente.\n\nReinicie la aplicación para ver los cambios.")
                ventana_gestion.destroy()
        
        tk.Button(frame_botones_nodos,
                 text="✏️ Editar Nombre",
                 command=editar_nodo,
                 bg='#3498db',
                 fg='white',
                 font=('Segoe UI', 10),
                 cursor='hand2',
                 width=15).pack(side='left', padx=5)
        
        tk.Button(frame_botones_nodos,
                 text="🗑️ Eliminar",
                 command=eliminar_nodo,
                 bg='#e74c3c',
                 fg='white',
                 font=('Segoe UI', 10),
                 cursor='hand2',
                 width=15).pack(side='left', padx=5)
        
        # ===== PESTAÑA: CONEXIONES =====
        frame_conexiones = tk.Frame(notebook, bg='white')
        notebook.add(frame_conexiones, text='🔗 Conexiones Personalizadas')
        
        tk.Label(frame_conexiones,
                text="Conexiones creadas por usted:",
                font=('Segoe UI', 11, 'bold'),
                bg='white').pack(pady=10)
        
        # Listbox con conexiones
        frame_lista_conexiones = tk.Frame(frame_conexiones, bg='white')
        frame_lista_conexiones.pack(fill='both', expand=True, padx=15, pady=5)
        
        scrollbar_conexiones = tk.Scrollbar(frame_lista_conexiones)
        scrollbar_conexiones.pack(side='right', fill='y')
        
        listbox_conexiones = tk.Listbox(frame_lista_conexiones,
                                        yscrollcommand=scrollbar_conexiones.set,
                                        font=('Segoe UI', 10),
                                        height=15)
        listbox_conexiones.pack(side='left', fill='both', expand=True)
        scrollbar_conexiones.config(command=listbox_conexiones.yview)
        
        # Cargar conexiones personalizadas
        conexiones_personalizadas = self.gestor_persistencia.obtener_conexiones()
        for conexion in conexiones_personalizadas:
            origen_nombre = self.grafo.nombres_vertices.get(conexion['origen'], conexion['origen'])
            destino_nombre = self.grafo.nombres_vertices.get(conexion['destino'], conexion['destino'])
            listbox_conexiones.insert(
                tk.END,
                f"{origen_nombre} → {destino_nombre} ({conexion['distancia']}m, {conexion['tiempo']}min)"
            )
        
        # Botones para conexiones
        frame_botones_conexiones = tk.Frame(frame_conexiones, bg='white')
        frame_botones_conexiones.pack(pady=10)
        
        def editar_conexion():
            seleccion = listbox_conexiones.curselection()
            if not seleccion:
                messagebox.showwarning("Sin Selección", "Seleccione una conexión para editar.")
                return
            
            idx = seleccion[0]
            conexion = conexiones_personalizadas[idx]
            
            # Pedir nueva distancia
            nueva_distancia = simpledialog.askfloat(
                "Editar Conexión",
                f"Distancia actual: {conexion['distancia']} metros\n\nIngrese la nueva distancia:",
                initialvalue=conexion['distancia'],
                minvalue=0.0,
                parent=ventana_gestion
            )
            
            if nueva_distancia is None:
                return
            
            # Pedir nuevo tiempo
            nuevo_tiempo = simpledialog.askfloat(
                "Editar Conexión",
                f"Tiempo actual: {conexion['tiempo']} minutos\n\nIngrese el nuevo tiempo:",
                initialvalue=conexion['tiempo'],
                minvalue=0.0,
                parent=ventana_gestion
            )
            
            if nuevo_tiempo is None:
                return
            
            self.gestor_persistencia.editar_conexion(
                conexion['origen'],
                conexion['destino'],
                nueva_distancia=nueva_distancia,
                nuevo_tiempo=nuevo_tiempo
            )
            messagebox.showinfo("Éxito", "Conexión editada correctamente.\n\nReinicie la aplicación para ver los cambios.")
            ventana_gestion.destroy()
        
        def eliminar_conexion():
            seleccion = listbox_conexiones.curselection()
            if not seleccion:
                messagebox.showwarning("Sin Selección", "Seleccione una conexión para eliminar.")
                return
            
            idx = seleccion[0]
            conexion = conexiones_personalizadas[idx]
            
            origen_nombre = self.grafo.nombres_vertices.get(conexion['origen'], conexion['origen'])
            destino_nombre = self.grafo.nombres_vertices.get(conexion['destino'], conexion['destino'])
            
            confirmar = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro de eliminar la conexión?\n\n"
                f"De: {origen_nombre}\n"
                f"A: {destino_nombre}"
            )
            
            if confirmar:
                self.gestor_persistencia.eliminar_conexion(conexion['origen'], conexion['destino'])
                messagebox.showinfo("Éxito", "Conexión eliminada correctamente.\n\nReinicie la aplicación para ver los cambios.")
                ventana_gestion.destroy()
        
        tk.Button(frame_botones_conexiones,
                 text="✏️ Editar Distancia/Tiempo",
                 command=editar_conexion,
                 bg='#3498db',
                 fg='white',
                 font=('Segoe UI', 10),
                 cursor='hand2',
                 width=20).pack(side='left', padx=5)
        
        tk.Button(frame_botones_conexiones,
                 text="🗑️ Eliminar",
                 command=eliminar_conexion,
                 bg='#e74c3c',
                 fg='white',
                 font=('Segoe UI', 10),
                 cursor='hand2',
                 width=15).pack(side='left', padx=5)
        
        # Botón cerrar
        tk.Button(ventana_gestion,
                 text="Cerrar",
                 command=ventana_gestion.destroy,
                 bg='#95a5a6',
                 fg='white',
                 font=('Segoe UI', 10),
                 cursor='hand2',
                 width=15).pack(pady=10)
    
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
