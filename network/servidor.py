"""
Servidor del Network OS: cada servidor posee su propio disco (árbol de
directorios) y su propia base de credenciales (tabla hash).
"""

import hashlib
from typing import Optional

from audit.logger import Auditor
from filesystem.hash_table import TablaHashAutenticacion
from filesystem.tree import ArbolDirectorios, ILogger


class AuditoriaTreeLogger(ILogger):
    """Adaptador: redirige los logs del árbol al motor de auditoría (con el nombre del servidor)."""

    def __init__(self, auditor: Auditor, nombre_servidor: str):
        self._auditor = auditor
        self._servidor = nombre_servidor

    def log(self, mensaje: str) -> None:
        self._auditor.registrar(f"[{self._servidor}] {mensaje}")


class Servidor:
    def __init__(self, nombre: str, auditor: Auditor):
        self.nombre = nombre
        self._auditor = auditor
        self.arbol = ArbolDirectorios(logger=AuditoriaTreeLogger(auditor, nombre))
        self.usuarios = TablaHashAutenticacion()
        self.sesion: Optional[str] = None

    @staticmethod
    def _cifrar(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def registrar_usuario(self, usuario: str, password: str) -> bool:
        ok = self.usuarios.registrar_usuario(usuario, self._cifrar(password))
        self._auditor.registrar(
            f"[{self.nombre}] Registro de usuario '{usuario}': {'exitoso' if ok else 'fallido (ya existe)'}"
        )
        return ok

    def iniciar_sesion(self, usuario: str, password: str) -> bool:
        ok = self.usuarios.autenticar(usuario, self._cifrar(password))
        self._auditor.registrar(
            f"[{self.nombre}] Inicio de sesión de '{usuario}': {'EXITOSO' if ok else 'FALLIDO'}"
        )
        self.sesion = usuario if ok else None
        return ok

    def cerrar_sesion(self) -> None:
        if self.sesion:
            self._auditor.registrar(f"[{self.nombre}] Cierre de sesión de '{self.sesion}'")
        self.sesion = None
