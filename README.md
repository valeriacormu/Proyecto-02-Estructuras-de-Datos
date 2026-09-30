# Proyecto-02-Estructuras-de-Datos
Sistema de Archivos Distribuido y Enrutador de Red

### 4. Topología y Enrutamiento de Red "network/graph.py"

* **Prompt:**
  > *"Implementa un Grafo ponderado en Python aplicando SOLID, con Dijkstra mediante cola de prioridad y BFS/DFS para diagnóstico de red, usando interfaces inyectables para el algoritmo de ruta y la auditoría."*
* **Adaptación e Integración:**
  - Se separó el algoritmo de ruteo en la clase "DijkstraStrategy" mediante la interfaz "IAlgoritmoRuta", permitiendo intercambiar el algoritmo sin modificar la clase "Grafo".
  - Se usó una cola de prioridad ("heapq") en vez de búsqueda lineal del costo mínimo.
  - Se implementaron "BFSDiagnostico" y "DFSDiagnostico" como clases independientes para detectar servidores aislados.


### 5. Auditoría Transaccional "audit/logger.py"

* **Prompt:**
  > *"Crea un motor de auditoría en Python que registre eventos con fecha y hora en un archivo de texto, aplicando inyección de dependencias para poder probar la clase sin tocar el sistema de archivos real."*
* **Adaptación e Integración:**
  - Se separó la persistencia ("IAuditWriter"/"ArchivoAuditWriter") y el origen del tiempo ("IRelojProveedor"/"RelojSistema") de la clase "Auditor", permitiendo inyectar dobles de prueba en los tests.


### 6. Pruebas Unitarias "tests/test_graph.py" y "tests/test_logger.py"

* **Prompt:**
  > *"Crea las pruebas unitarias en Python con unittest para validar el algoritmo de Dijkstra, el diagnóstico de red mediante BFS, la eliminación de servidores/conexiones, y el registro/lectura de eventos de auditoría."*
* **Adaptación e Integración:**
  - Se verificaron los casos de prueba ante rutas inexistentes, servidores aislados en la red, eliminación de conexiones y servidores, y registro/lectura de eventos de auditoría usando dobles de prueba en lugar de acceso real a disco.