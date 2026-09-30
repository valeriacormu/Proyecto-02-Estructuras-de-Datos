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


class DFSDiagnostico:
    """Estrategia de diagnóstico de red mediante recorrido en profundidad (recursivo)."""

    def recorrer(
        self, adyacencia: Dict[str, List[Tuple[str, float]]], inicio: str, visitados: Optional[Set[str]] = None
    ) -> Set[str]:
        if visitados is None:
            visitados = set()
        if inicio not in adyacencia:
            return visitados

        visitados.add(inicio)
        for vecino, _ in adyacencia[inicio]:
            if vecino not in visitados:
                self.recorrer(adyacencia, vecino, visitados)

        return visitados


class Grafo:
    """
    Grafo ponderado no dirigido que representa la red de servidores.
    SRP: solo gestiona la topología (agregar/eliminar) y delega los
    algoritmos de ruta y diagnóstico en estrategias inyectadas (DIP/OCP).
    """

    def __init__(
        self,
        auditor: Optional[IAuditor] = None,
        estrategia_ruta: Optional[IAlgoritmoRuta] = None,
    ):
        self._adyacencia: Dict[str, List[Tuple[str, float]]] = {}
        self._auditor = auditor or AuditorNulo()
        self._estrategia_ruta = estrategia_ruta or DijkstraStrategy()

    @property
    def adyacencia(self) -> Dict[str, List[Tuple[str, float]]]:
        return self._adyacencia

    def agregar_servidor(self, nombre: str) -> None:
        if nombre not in self._adyacencia:
            self._adyacencia[nombre] = []
            self._auditor.registrar(f"Servidor agregado: {nombre}")
        else:
            self._auditor.registrar(f"Intento de agregar servidor duplicado: {nombre}")

    def eliminar_servidor(self, nombre: str) -> bool:
        if nombre not in self._adyacencia:
            self._auditor.registrar(f"Intento de eliminar servidor inexistente: {nombre}")
            return False

        for vecino in list(self._adyacencia.keys()):
            self._adyacencia[vecino] = [
                (v, p) for (v, p) in self._adyacencia[vecino] if v != nombre
            ]

        del self._adyacencia[nombre]
        self._auditor.registrar(f"Servidor eliminado: {nombre}")
        return True

    def agregar_conexion(self, origen: str, destino: str, peso: float) -> None:
        if origen not in self._adyacencia:
            self.agregar_servidor(origen)
        if destino not in self._adyacencia:
            self.agregar_servidor(destino)

        if not any(v == destino for v, _ in self._adyacencia[origen]):
            self._adyacencia[origen].append((destino, peso))
            self._adyacencia[destino].append((origen, peso))
            self._auditor.registrar(f"Conexión creada: {origen} <-> {destino} (latencia={peso}ms)")
        else:
            self._auditor.registrar(f"Conexión ya existente: {origen} <-> {destino}")

    def eliminar_conexion(self, origen: str, destino: str) -> bool:
        if origen not in self._adyacencia or destino not in self._adyacencia:
            self._auditor.registrar(f"Intento de eliminar conexión inexistente: {origen} <-> {destino}")
            return False

        self._adyacencia[origen] = [(v, p) for (v, p) in self._adyacencia[origen] if v != destino]
        self._adyacencia[destino] = [(v, p) for (v, p) in self._adyacencia[destino] if v != origen]
        self._auditor.registrar(f"Conexión eliminada: {origen} <-> {destino}")
        return True

    def calcular_ruta(self, origen: str, destino: str) -> Tuple[Optional[List[str]], float]:
        ruta, costo = self._estrategia_ruta.calcular(self._adyacencia, origen, destino)
        if ruta is None:
            self._auditor.registrar(f"No existe ruta entre {origen} y {destino}")
        else:
            self._auditor.registrar(
                f"Ruta calculada {origen} -> {destino}: {' -> '.join(ruta)} (costo total={costo}ms)"
            )
        return ruta, costo

    def imprimir_ruta(self, origen: str, destino: str) -> None:
        ruta, costo = self.calcular_ruta(origen, destino)
        if ruta is None:
            print(f"No existe una ruta disponible entre {origen} y {destino}.")
            return
        print("Ruta calculada:")
        for i, servidor in enumerate(ruta):
            print(f"  Salto {i}: {servidor}")
        print(f"Costo total: {costo} ms")

    def diagnostico_red(self) -> List[str]:
        if not self._adyacencia:
            print("La red no tiene servidores registrados.")
            return []

        servidores = list(self._adyacencia.keys())
        alcanzados = BFSDiagnostico().recorrer(self._adyacencia, servidores[0])
        aislados = [s for s in servidores if s not in alcanzados]

        print("=== Diagnóstico de Red (Ping General) ===")
        if not aislados:
            print("Todos los servidores están comunicados correctamente.")
        else:
            print("Se detectaron servidores aislados:")
            for s in aislados:
                print(f"  - {s}")

        self._auditor.registrar(
            f"Diagnóstico ejecutado. Servidores aislados: {aislados if aislados else 'ninguno'}"
        )
        return aislados