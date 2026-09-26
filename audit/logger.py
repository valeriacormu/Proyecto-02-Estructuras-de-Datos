"""
Módulo de Auditoría Transaccional.
Implementación aplicando SOLID: el Auditor depende de abstracciones
de persistencia (IAuditWriter) y de tiempo (IRelojProveedor) (DIP).
"""

from abc import ABC, abstractmethod
import os


class IAuditWriter(ABC):
    @abstractmethod
    def escribir(self, linea: str) -> None:
        pass

    @abstractmethod
    def leer_todo(self) -> str:
        pass


class ArchivoAuditWriter(IAuditWriter):
    """Implementación concreta: persistencia en archivo de texto plano."""

    def __init__(self, ruta_archivo: str = "network_audit_log.txt"):
        self._ruta = ruta_archivo
        if not os.path.exists(self._ruta):
            open(self._ruta, "a", encoding="utf-8").close()

    def escribir(self, linea: str) -> None:
        with open(self._ruta, "a", encoding="utf-8") as f:
            f.write(linea + "\n")

    def leer_todo(self) -> str:
        if not os.path.exists(self._ruta) or os.path.getsize(self._ruta) == 0:
            return ""
        with open(self._ruta, "r", encoding="utf-8") as f:
            return f.read()