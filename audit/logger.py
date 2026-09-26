"""
Módulo de Auditoría Transaccional.
Implementación aplicando SOLID: el Auditor depende de abstracciones
de persistencia (IAuditWriter) y de tiempo (IRelojProveedor) (DIP).
"""

from abc import ABC, abstractmethod
from datetime import datetime
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


class IRelojProveedor(ABC):
    @abstractmethod
    def ahora(self) -> str:
        pass


class RelojSistema(IRelojProveedor):
    def ahora(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class Auditor:
    """
    Motor de auditoría transaccional (SRP: coordina registro/lectura,
    delega persistencia en IAuditWriter y la hora en IRelojProveedor).
    """

    def __init__(self, writer: IAuditWriter = None, reloj: IRelojProveedor = None):
        self._writer = writer or ArchivoAuditWriter()
        self._reloj = reloj or RelojSistema()

    def registrar(self, evento: str) -> None:
        marca_tiempo = self._reloj.ahora()
        self._writer.escribir(f"[{marca_tiempo}] {evento}")

    def leer_log(self) -> None:
        contenido = self._writer.leer_todo()
        if not contenido:
            print("El registro de auditoría está vacío.")
            return
        print("=== Registro de Auditoría ===")
        print(contenido)