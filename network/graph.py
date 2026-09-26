"""
Módulo de Topología y Enrutamiento de Red (Grafo Ponderado).
Implementación aplicando SOLID: el Grafo depende de abstracciones
(IAuditor, IAlgoritmoRuta), no de implementaciones concretas (DIP).
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional, Set
import heapq


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


class DijkstraStrategy(IAlgoritmoRuta):
    """Estrategia concreta: algoritmo de Dijkstra con cola de prioridad (heap)."""

    def calcular(
        self, adyacencia: Dict[str, List[Tuple[str, float]]], origen: str, destino: str
    ) -> Tuple[Optional[List[str]], float]:
        if origen not in adyacencia or destino not in adyacencia:
            return None, float("inf")

        costos_minimos = {nodo: float("inf") for nodo in adyacencia}
        costos_minimos[origen] = 0
        previos: Dict[str, Optional[str]] = {nodo: None for nodo in adyacencia}
        visitados: Set[str] = set()

        cola_prioridad: List[Tuple[float, str]] = [(0, origen)]

        while cola_prioridad:
            costo_actual, nodo_actual = heapq.heappop(cola_prioridad)

            if nodo_actual in visitados:
                continue
            visitados.add(nodo_actual)

            if nodo_actual == destino:
                break

            for vecino, peso in adyacencia[nodo_actual]:
                nuevo_costo = costo_actual + peso
                if nuevo_costo < costos_minimos[vecino]:
                    costos_minimos[vecino] = nuevo_costo
                    previos[vecino] = nodo_actual
                    heapq.heappush(cola_prioridad, (nuevo_costo, vecino))

        if costos_minimos[destino] == float("inf"):
            return None, float("inf")

        ruta = []
        nodo: Optional[str] = destino
        while nodo is not None:
            ruta.append(nodo)
            nodo = previos[nodo]
        ruta.reverse()

        return ruta, costos_minimos[destino]


class BFSDiagnostico:
    """Estrategia de diagnóstico de red mediante recorrido en anchura."""

    def recorrer(self, adyacencia: Dict[str, List[Tuple[str, float]]], inicio: str) -> Set[str]:
        if inicio not in adyacencia:
            return set()

        visitados = {inicio}
        cola = [inicio]

        while cola:
            actual = cola.pop(0)
            for vecino, _ in adyacencia[actual]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append(vecino)

        return visitados