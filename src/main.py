"""
Módulo: main.py
Descripción: Punto de entrada principal para la aplicación CityNavigator
Autor: CityNavigator
Fecha: Enero 2026
"""

import sys
from interfaz_grafica import iniciar_aplicacion


def main():
    """
    Función principal que inicia la aplicación CityNavigator.
    """
    print("=" * 60)
    print("  CityNavigator - Sistema de Navegación Urbana")
    print("  Puerto Ordaz, Venezuela")
    print("=" * 60)
    print("\nIniciando interfaz gráfica...")
    
    try:
        iniciar_aplicacion()
    except Exception as e:
        print(f"\n❌ Error al iniciar la aplicación: {e}")
        sys.exit(1)
    
    print("\n¡Gracias por usar CityNavigator!")


if __name__ == "__main__":
    main()
