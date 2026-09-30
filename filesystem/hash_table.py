"""
Módulo de Tabla Hash para Autenticación de Usuarios.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Optional


class IHashFunction(ABC):
    @abstractmethod
    def hash(self, clave: str, capacidad: int) -> int:
        pass


class PolynomialHashFunction(IHashFunction):

    def __init__(self, base_primo: int = 31):
        self.p = base_primo

    def hash(self, clave: str, capacidad: int) -> int:
        val_hash = 0
        for caracter in clave:
            val_hash = (val_hash * self.p + ord(caracter)) % capacidad
        return val_hash

# Nodo de lista enlazada para manejar colisiones en cada posición de la tabla.
class NodoHash:
    def __init__(self, clave: str, valor: Any):
        self.clave = clave
        self.valor = valor
        self.siguiente: Optional['NodoHash'] = None


class TablaHashAutenticacion:
    def __init__(self, capacidad_inicial: int = 17, hash_fn: Optional[IHashFunction] = None):
        self._capacidad = capacidad_inicial
        self._tamano = 0
        self._factor_carga_max = 0.75
        self._tabla: List[Optional[NodoHash]] = [None] * self._capacidad
        self._hash_fn = hash_fn or PolynomialHashFunction()

    @property
    def capacidad(self) -> int:
        return self._capacidad

    @property
    def tamano(self) -> int:
        return self._tamano

    def _obtener_indice(self, clave: str) -> int:
        return self._hash_fn.hash(clave, self._capacidad)

# Inserta un ususario a la tabla.
    def registrar_usuario(self, usuario: str, password_hash: str) -> bool:
        if self.obtener_password(usuario) is not None:
            return False  # El usuario ya existe

        if (self._tamano + 1) / self._capacidad >= self._factor_carga_max:
            self._rehashing()

        indice = self._obtener_indice(usuario)
        nuevo_nodo = NodoHash(usuario, password_hash)
        nuevo_nodo.siguiente = self._tabla[indice]
        self._tabla[indice] = nuevo_nodo
        self._tamano += 1
        return True

# Busca la contraseña alamacenada de un usuario.center()
    def obtener_password(self, usuario: str) -> Optional[str]:
        indice = self._obtener_indice(usuario)
        actual = self._tabla[indice]
        while actual:
            if actual.clave == usuario:
                return actual.valor
            actual = actual.siguiente
        return None

# Valida las credenciales de un usuario
    def autenticar(self, usuario: str, password_hash: str) -> bool:
        pwd_guardado = self.obtener_password(usuario)
        if pwd_guardado is None:
            return False
        return pwd_guardado == password_hash

# Duplica la capacidad a un número primo superior y redistribuye las claves existentes.
    def _rehashing(self) -> None:
        capacidad_anterior = self._capacidad
        tabla_anterior = self._tabla

        self._capacidad = self._siguiente_primo(self._capacidad * 2)
        self._tabla = [None] * self._capacidad
        self._tamano = 0

        for i in range(capacidad_anterior):
            actual = tabla_anterior[i]
            while actual:
                self.registrar_usuario(actual.clave, actual.valor)
                actual = actual.siguiente

    @staticmethod
    def _es_primo(n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    def _siguiente_primo(self, n: int) -> int:
        while not self._es_primo(n):
            n += 1
        return n