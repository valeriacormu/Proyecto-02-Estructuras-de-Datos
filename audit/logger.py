"""
Módulo de Auditoría Transaccional.
Implementación aplicando SOLID: el Auditor depende de abstracciones
de persistencia (IAuditWriter) y de tiempo (IRelojProveedor) (DIP).
"""

from abc import ABC, abstractmethod


class IAuditWriter(ABC):
    @abstractmethod
    def escribir(self, linea: str) -> None:
        pass

    @abstractmethod
    def leer_todo(self) -> str:
        pass