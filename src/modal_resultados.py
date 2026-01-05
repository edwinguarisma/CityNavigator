"""
Módulo: modal_resultados.py
Descripción: Ventana modal para mostrar resultados detallados de búsqueda
Autor: CityNavigator
Fecha: Enero 2026
"""

import tkinter as tk
from tkinter import scrolledtext
from visualizador import mostrar_info_ruta


def crear_modal_resultados(ventana_padre, ruta, coste, criterio, algoritmo, grafo):
    """
    Crea y muestra una ventana modal con los resultados detallados de la búsqueda.
    
    Args:
        ventana_padre: Ventana principal de la aplicación
        ruta: Lista de vértices de la ruta
        coste: Coste total de la ruta
        criterio: Criterio usado ('distancia', 'tiempo', 'conexion')
        algoritmo: Nombre del algoritmo usado
        grafo: Instancia del grafo
    """
    # Crear ventana modal
    modal = tk.Toplevel(ventana_padre)
    modal.title(f"Detalles de la Ruta - {algoritmo}")
    modal.geometry("800x700")
    modal.configure(bg='#f0f0f0')
    
    # Hacer modal (bloquear ventana padre)
    modal.transient(ventana_padre)
    modal.grab_set()
    
    # Centrar la ventana
    modal.update_idletasks()
    x = (modal.winfo_screenwidth() // 2) - (800 // 2)
    y = (modal.winfo_screenheight() // 2) - (700 // 2)
    modal.geometry(f"800x700+{x}+{y}")
    
    # ========== ENCABEZADO ==========
    frame_encabezado = tk.Frame(modal, bg='#2c3e50', height=80)
    frame_encabezado.pack(fill='x', side='top')
    
    titulo = tk.Label(frame_encabezado,
                     text=f"📋 Detalles de la Ruta",
                     font=('Segoe UI', 20, 'bold'),
                     bg='#2c3e50', fg='white')
    titulo.pack(pady=10)
    
    subtitulo = tk.Label(frame_encabezado,
                        text=f"Algoritmo: {algoritmo}",
                        font=('Segoe UI', 11),
                        bg='#2c3e50', fg='#ecf0f1')
    subtitulo.pack()
    
    # ========== RESUMEN RÁPIDO ==========
    frame_resumen = tk.Frame(modal, bg='white', bd=2, relief='groove')
    frame_resumen.pack(fill='x', padx=20, pady=20)
    
    # Crear resumen según el tipo de búsqueda
    if criterio == 'distancia':
        icono = "📏"
        valor_principal = f"{coste:.0f} metros ({coste/1000:.2f} km)"
        tipo = "Distancia Total"
    elif criterio == 'tiempo':
        icono = "⏱️"
        valor_principal = f"{coste:.1f} minutos"
        tipo = "Tiempo Total"
    else:  # conexion (BFS/DFS)
        icono = "🔍"
        valor_principal = f"{len(ruta)} intersecciones"
        tipo = "Camino Encontrado"
    
    # Fila de resumen
    frame_resumen_contenido = tk.Frame(frame_resumen, bg='white')
    frame_resumen_contenido.pack(padx=20, pady=15)
    
    # Columna 1: Tipo y valor principal
    col1 = tk.Frame(frame_resumen_contenido, bg='white')
    col1.pack(side='left', padx=20)
    
    tk.Label(col1, text=icono, font=('Segoe UI', 32), bg='white').pack()
    tk.Label(col1, text=tipo, font=('Segoe UI', 10, 'bold'), 
            bg='white', fg='#555').pack()
    tk.Label(col1, text=valor_principal, font=('Segoe UI', 14, 'bold'), 
            bg='white', fg='#2c3e50').pack()
    
    # Separador vertical
    tk.Frame(frame_resumen_contenido, width=2, bg='#ddd').pack(side='left', 
                                                                fill='y', padx=20)
    
    # Columna 2: Intersecciones
    col2 = tk.Frame(frame_resumen_contenido, bg='white')
    col2.pack(side='left', padx=20)
    
    tk.Label(col2, text="📍", font=('Segoe UI', 32), bg='white').pack()
    tk.Label(col2, text="Intersecciones", font=('Segoe UI', 10, 'bold'), 
            bg='white', fg='#555').pack()
    tk.Label(col2, text=str(len(ruta)), font=('Segoe UI', 14, 'bold'), 
            bg='white', fg='#2c3e50').pack()
    
    # Separador vertical
    tk.Frame(frame_resumen_contenido, width=2, bg='#ddd').pack(side='left', 
                                                                fill='y', padx=20)
    
    # Columna 3: Tramos
    col3 = tk.Frame(frame_resumen_contenido, bg='white')
    col3.pack(side='left', padx=20)
    
    tk.Label(col3, text="🚗", font=('Segoe UI', 32), bg='white').pack()
    tk.Label(col3, text="Tramos", font=('Segoe UI', 10, 'bold'), 
            bg='white', fg='#555').pack()
    tk.Label(col3, text=str(len(ruta) - 1) if len(ruta) > 0 else "0", 
            font=('Segoe UI', 14, 'bold'), bg='white', fg='#2c3e50').pack()
    
    # ========== DETALLES DE LA RUTA ==========
    frame_detalles = tk.LabelFrame(modal,
                                   text="🗺️  Recorrido Detallado",
                                   font=('Segoe UI', 12, 'bold'),
                                   bg='white',
                                   padx=15, pady=15)
    frame_detalles.pack(fill='both', expand=True, padx=20, pady=(0, 20))
    
    # Área de texto con scroll
    texto_detalles = scrolledtext.ScrolledText(frame_detalles,
                                               font=('Consolas', 10),
                                               wrap=tk.WORD,
                                               bg='#f9f9f9',
                                               padx=15,
                                               pady=15)
    texto_detalles.pack(fill='both', expand=True)
    
    # Generar y mostrar el texto detallado
    if criterio in ['distancia', 'tiempo']:
        texto = mostrar_info_ruta(ruta, coste, criterio, grafo)
    else:  # BFS/DFS
        texto = generar_texto_busqueda(ruta, algoritmo, grafo)
    
    texto_detalles.insert('1.0', texto)
    texto_detalles.config(state='disabled')  # Solo lectura
    
    # ========== BOTONES ==========
    frame_botones = tk.Frame(modal, bg='#f0f0f0')
    frame_botones.pack(fill='x', padx=20, pady=(0, 20))
    
    # Botón Cerrar
    boton_cerrar = tk.Button(frame_botones,
                            text="✖ Cerrar",
                            command=modal.destroy,
                            bg='#e74c3c',
                            fg='white',
                            font=('Segoe UI', 11, 'bold'),
                            cursor='hand2',
                            relief='raised',
                            bd=2,
                            width=15)
    boton_cerrar.pack(side='right', padx=5)
    
    # Botón Copiar (opcional)
    def copiar_resultados():
        modal.clipboard_clear()
        modal.clipboard_append(texto)
        tk.messagebox.showinfo("✅ Copiado", 
                              "Los resultados se copiaron al portapapeles",
                              parent=modal)
    
    boton_copiar = tk.Button(frame_botones,
                            text="📋 Copiar Resultados",
                            command=copiar_resultados,
                            bg='#3498db',
                            fg='white',
                            font=('Segoe UI', 11, 'bold'),
                            cursor='hand2',
                            relief='raised',
                            bd=2,
                            width=20)
    boton_copiar.pack(side='right', padx=5)
    
    # Permitir cerrar con ESC
    modal.bind('<Escape>', lambda e: modal.destroy())
    
    # Esperar a que se cierre la ventana
    modal.wait_window()


def generar_texto_busqueda(ruta, algoritmo, grafo):
    """
    Genera el texto detallado para resultados de BFS/DFS.
    
    Args:
        ruta: Lista de vértices
        algoritmo: Nombre del algoritmo
        grafo: Instancia del grafo
        
    Returns:
        str: Texto formateado
    """
    if not ruta:
        return "❌ NO SE ENCONTRÓ CONEXIÓN\n\nNo existe un camino entre los puntos seleccionados."
    
    texto = f"✅ CONEXIÓN ENCONTRADA - {algoritmo}\n"
    texto += "=" * 70 + "\n\n"
    
    texto += f"📍 INTERSECCIONES: {len(ruta)}\n"
    texto += f"🚗 TRAMOS: {len(ruta) - 1}\n\n"
    
    texto += f"⚠️  NOTA IMPORTANTE:\n"
    texto += f"{algoritmo} encuentra un camino pero NO garantiza que sea el más corto.\n"
    texto += f"Para la ruta óptima, use el algoritmo de Dijkstra.\n\n"
    
    texto += "🗺️  RECORRIDO PASO A PASO:\n"
    texto += "─" * 70 + "\n\n"
    
    for i, vertice in enumerate(ruta):
        nombre = grafo.nombres_vertices.get(vertice, vertice)
        
        if i == 0:
            texto += f"🟢 INICIO: {vertice}\n"
        elif i == len(ruta) - 1:
            texto += f"🔴 DESTINO: {vertice}\n"
        else:
            texto += f"🟠 Paso {i}: {vertice}\n"
        
        texto += f"   {nombre}\n"
        
        if i < len(ruta) - 1:
            texto += f"   │\n"
            texto += f"   ↓\n"
            texto += f"   │\n"
    
    texto += "\n" + "=" * 70 + "\n"
    
    return texto
