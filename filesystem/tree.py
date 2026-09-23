"""
Módulo de Sistema de Archivos basado en Árbol General.
Implementación aplicando principios SOLID (SRP, OCP, LSP, DIP)
y eficiencia asintótica O(k) para navegación por ruta.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional, List


# Interfaz Abstracta para Audit Logging
class ILogger(ABC):
    @abstractmethod
    def log(self, mensaje: str) -> None:
        pass


class ConsoleLogger(ILogger):
    def log(self, mensaje: str) -> None:
        print(f"[AUDIT] {mensaje}")


# Elemento Base del Sistema de Archivos
class ElementoSistemaArchivos(ABC):
    def __init__(self, nombre: str, padre: Optional['Carpeta'] = None):
        self.nombre = nombre
        self.padre = padre

    @abstractmethod
    def es_carpeta(self) -> bool:
        pass

    @abstractmethod
    def obtener_tamano(self) -> int:
        pass

# Representa un archivo (nodo hoja del arbol)
class Archivo(ElementoSistemaArchivos):
    def __init__(self, nombre: str, tamano: int = 0, padre: Optional['Carpeta'] = None):
        super().__init__(nombre, padre)
        self._tamano = tamano

    def es_carpeta(self) -> bool:
        return False

    def obtener_tamano(self) -> int:
        return self._tamano

# Representa una carpeta (nodo interno/raíz).
class Carpeta(ElementoSistemaArchivos):
    def __init__(self, nombre: str, padre: Optional['Carpeta'] = None):
        super().__init__(nombre, padre)
        self.hijos: Dict[str, ElementoSistemaArchivos] = {}

    def es_carpeta(self) -> bool:
        return True

    def agregar_hijo(self, elemento: ElementoSistemaArchivos) -> None:
        elemento.padre = self
        self.hijos[elemento.nombre] = elemento

    def remover_hijo(self, nombre: str) -> Optional[ElementoSistemaArchivos]:
        return self.hijos.pop(nombre, None)

    def obtener_tamano(self) -> int:
        return sum(hijo.obtener_tamano() for hijo in self.hijos.values())


# Árbol de Directorios
class ArbolDirectorios:
    def __init__(self, logger: Optional[ILogger] = None):
        self.raiz = Carpeta("/")
        self.logger = logger or ConsoleLogger()

    # Navega hacia un elemento dada su ruta absoluta 
    def navegar_a_ruta(self, ruta: str) -> Optional[ElementoSistemaArchivos]:
        if not ruta or ruta == "/":
            return self.raiz

        partes = [p for p in ruta.split("/") if p]
        actual: ElementoSistemaArchivos = self.raiz

        for parte in partes:
            if not actual.es_carpeta():
                return None
            actual = actual.hijos.get(parte)
            if actual is None:
                return None

        return actual

    def crear_elemento(self, ruta_padre: str, nombre: str, es_carpeta: bool, tamano: int = 0) -> bool:
        padre = self.navegar_a_ruta(ruta_padre)
        if not padre or not padre.es_carpeta():
            self.logger.log(f"Error: Ruta padre inalcanzable '{ruta_padre}'.")
            return False

        if nombre in padre.hijos:
            self.logger.log(f"Error: El elemento '{nombre}' ya existe en '{ruta_padre}'.")
            return False

        nuevo: ElementoSistemaArchivos = (
            Carpeta(nombre) if es_carpeta else Archivo(nombre, tamano)
        )
        padre.agregar_hijo(nuevo)
        self.logger.log(f"Creado {'Carpeta' if es_carpeta else 'Archivo'} '{nombre}' en '{ruta_padre}'.")
        return True

    # Elimina en cascada el subárbol completo (Recorrido Postorden / Bottom-Up)
    def eliminar_en_cascada(self, ruta_objetivo: str) -> bool:
        if ruta_objetivo == "/":
            self.logger.log("Error: No se permite eliminar la raíz '/'.")
            return False

        nodo = self.navegar_a_ruta(ruta_objetivo)
        if not nodo:
            self.logger.log(f"Error: No se encontró '{ruta_objetivo}' para eliminar.")
            return False

        padre = nodo.padre
        self._liberar_subarbol(nodo)

        if padre and padre.es_carpeta():
            padre.remover_hijo(nodo.nombre)

        self.logger.log(f"Eliminado en cascada con éxito: '{ruta_objetivo}'.")
        return True

    def _liberar_subarbol(self, elemento: ElementoSistemaArchivos) -> None:
        if elemento.es_carpeta():
            carpeta: Carpeta = elemento
            nombres_hijos = list(carpeta.hijos.keys())
            for nombre in nombres_hijos:
                hijo = carpeta.remover_hijo(nombre)
                if hijo:
                    self._liberar_subarbol(hijo)
        elemento.padre = None

    def mostrar_arbol(self, nodo_actual: Optional[ElementoSistemaArchivos] = None, nivel: int = 0) -> None:
        if nodo_actual is None:
            nodo_actual = self.raiz

        prefijo = "  " * nivel + ("📁 " if nodo_actual.es_carpeta() else "📄 ")
        print(f"{prefijo}{nodo_actual.nombre}")

        if nodo_actual.es_carpeta():
            for hijo in nodo_actual.hijos.values():
                self.mostrar_arbol(hijo, nivel + 1)