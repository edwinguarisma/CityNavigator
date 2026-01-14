"""
Módulo: persistencia.py
Descripción: Maneja la persistencia de nodos y conexiones personalizadas
Autor: CityNavigator
Fecha: Enero 2026
"""

import json
import os
from typing import Dict, List, Tuple

# Archivo donde se guardan los datos personalizados
ARCHIVO_DATOS_PERSONALIZADOS = "datos_personalizados.json"


class GestorPersistencia:
    """Gestiona el guardado y carga de datos personalizados del usuario."""
    
    def __init__(self, archivo: str = ARCHIVO_DATOS_PERSONALIZADOS):
        """
        Inicializa el gestor de persistencia.
        
        Args:
            archivo: Nombre del archivo JSON donde guardar los datos
        """
        self.archivo = archivo
        self.datos = self._cargar_datos()
    
    def _cargar_datos(self) -> Dict:
        """
        Carga los datos personalizados desde el archivo JSON.
        
        Returns:
            Dict con estructura:
            {
                "nodos": [
                    {
                        "id": "Hospital_Uyapar",
                        "nombre": "Hospital Uyapar",
                        "coordenadas": [-62.725, 8.275]
                    },
                    ...
                ],
                "conexiones": [
                    {
                        "origen": "Hospital_Uyapar",
                        "destino": "PlazaMayor",
                        "distancia": 350.0,
                        "tiempo": 3.5
                    },
                    ...
                ]
            }
        """
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error al cargar datos personalizados: {e}")
                return {"nodos": [], "conexiones": []}
        else:
            return {"nodos": [], "conexiones": []}
    
    def guardar_datos(self):
        """Guarda los datos actuales en el archivo JSON."""
        try:
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump(self.datos, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Error al guardar datos personalizados: {e}")
            return False
    
    def agregar_nodo(self, id_nodo: str, nombre: str, coordenadas: Tuple[float, float]):
        """
        Agrega un nodo personalizado.
        
        Args:
            id_nodo: Identificador único del nodo
            nombre: Nombre descriptivo
            coordenadas: Tupla (lon, lat)
        """
        # Verificar si ya existe
        for nodo in self.datos["nodos"]:
            if nodo["id"] == id_nodo:
                # Actualizar si ya existe
                nodo["nombre"] = nombre
                nodo["coordenadas"] = list(coordenadas)
                self.guardar_datos()
                return
        
        # Agregar nuevo nodo
        self.datos["nodos"].append({
            "id": id_nodo,
            "nombre": nombre,
            "coordenadas": list(coordenadas)
        })
        self.guardar_datos()
    
    def agregar_conexion(self, origen: str, destino: str, distancia: float, tiempo: float):
        """
        Agrega una conexión personalizada.
        
        Args:
            origen: ID del nodo origen
            destino: ID del nodo destino
            distancia: Distancia en metros
            tiempo: Tiempo en minutos
        """
        # Verificar si ya existe esta conexión
        for conexion in self.datos["conexiones"]:
            if conexion["origen"] == origen and conexion["destino"] == destino:
                # Actualizar si ya existe
                conexion["distancia"] = distancia
                conexion["tiempo"] = tiempo
                self.guardar_datos()
                return
        
        # Agregar nueva conexión
        self.datos["conexiones"].append({
            "origen": origen,
            "destino": destino,
            "distancia": distancia,
            "tiempo": tiempo
        })
        self.guardar_datos()
    
    def obtener_nodos(self) -> List[Dict]:
        """Retorna la lista de nodos personalizados."""
        return self.datos["nodos"]
    
    def obtener_conexiones(self) -> List[Dict]:
        """Retorna la lista de conexiones personalizadas."""
        return self.datos["conexiones"]
    
    def eliminar_nodo(self, id_nodo: str) -> bool:
        """
        Elimina un nodo personalizado y todas sus conexiones.
        
        Args:
            id_nodo: ID del nodo a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        # Eliminar el nodo
        self.datos["nodos"] = [n for n in self.datos["nodos"] if n["id"] != id_nodo]
        
        # Eliminar todas las conexiones relacionadas
        self.datos["conexiones"] = [
            c for c in self.datos["conexiones"]
            if c["origen"] != id_nodo and c["destino"] != id_nodo
        ]
        
        return self.guardar_datos()
    
    def eliminar_conexion(self, origen: str, destino: str) -> bool:
        """
        Elimina una conexión específica.
        
        Args:
            origen: ID del nodo origen
            destino: ID del nodo destino
            
        Returns:
            bool: True si se eliminó correctamente
        """
        self.datos["conexiones"] = [
            c for c in self.datos["conexiones"]
            if not (c["origen"] == origen and c["destino"] == destino)
        ]
        
        return self.guardar_datos()
    
    def editar_nodo(self, id_nodo: str, nuevo_nombre: str = None, 
                   nuevas_coordenadas: Tuple[float, float] = None) -> bool:
        """
        Edita un nodo existente.
        
        Args:
            id_nodo: ID del nodo a editar
            nuevo_nombre: Nuevo nombre (opcional)
            nuevas_coordenadas: Nuevas coordenadas (opcional)
            
        Returns:
            bool: True si se editó correctamente
        """
        for nodo in self.datos["nodos"]:
            if nodo["id"] == id_nodo:
                if nuevo_nombre:
                    nodo["nombre"] = nuevo_nombre
                if nuevas_coordenadas:
                    nodo["coordenadas"] = list(nuevas_coordenadas)
                return self.guardar_datos()
        
        return False
    
    def editar_conexion(self, origen: str, destino: str, 
                       nueva_distancia: float = None, nuevo_tiempo: float = None) -> bool:
        """
        Edita una conexión existente.
        
        Args:
            origen: ID del nodo origen
            destino: ID del nodo destino
            nueva_distancia: Nueva distancia (opcional)
            nuevo_tiempo: Nuevo tiempo (opcional)
            
        Returns:
            bool: True si se editó correctamente
        """
        for conexion in self.datos["conexiones"]:
            if conexion["origen"] == origen and conexion["destino"] == destino:
                if nueva_distancia is not None:
                    conexion["distancia"] = nueva_distancia
                if nuevo_tiempo is not None:
                    conexion["tiempo"] = nuevo_tiempo
                return self.guardar_datos()
        
        return False
    
    def es_nodo_personalizado(self, id_nodo: str) -> bool:
        """
        Verifica si un nodo es personalizado (creado por el usuario).
        
        Args:
            id_nodo: ID del nodo a verificar
            
        Returns:
            bool: True si es personalizado
        """
        return any(nodo["id"] == id_nodo for nodo in self.datos["nodos"])
    
    def limpiar_todo(self) -> bool:
        """Elimina todos los datos personalizados."""
        self.datos = {"nodos": [], "conexiones": []}
        return self.guardar_datos()
