"""
Módulo de Topología y Enrutamiento de Red (Grafo Ponderado).
Implementación aplicando SOLID: el Grafo depende de abstracciones
(IAuditor, IAlgoritmoRuta), no de implementaciones concretas (DIP).
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional


class IAuditor(ABC):
    @abstractmethod
    def registrar(self, evento: str) -> None:
        pass


class AuditorNulo(IAuditor):
    """Implementación nula (Null Object Pattern) — útil para tests sin efectos secundarios."""
    def registrar(self, evento: str) -> None:
        pass


class IAlgoritmoRuta(ABC):
    @abstractmethod
    def calcular(
        self, adyacencia: Dict[str, List[Tuple[str, float]]], origen: str, destino: str
    ) -> Tuple[Optional[List[str]], float]:
        pass