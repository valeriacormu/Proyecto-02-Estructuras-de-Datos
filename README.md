# Proyecto-02-Estructuras-de-Datos
Sistema de Archivos Distribuido y Enrutador de Red

## Bitácora de Inteligencia Artificial

Se documentan los prompts utilizados con Inteligencia Artificial Gemini como herramienta de apoyo, junto con la adaptación validación realizada para cumplir con los requerimientos y la arquitectura del sistema.

### 1. Sistema de Archivos "filesystem/tree.py"


* **Prompt:**
  > *"Genera la clase para un Árbol de directorios en Python aplicando los principios SOLID (SRP, OCP, LSP, DIP).*
* **Adaptación e Integración:**
  - Se implementó la abstracción base "ElementoSistemaArchivos" para "Archivo" y "Carpeta".
  - Se utilizó un mapa hash interno en cada instancia de "Carpeta" para resolver la búsqueda de hijos directos.
  - Se programó la eliminación recursiva en cascada garantizando un recorrido postorden que asigna "padre = None" y vacía los punteros de los hijos para evitar nodos huérfanos en memoria.


### 2. Autenticación con Tabla Hash "filesystem/hash_table.py"

* **Prompt:**
  > *"Escribe una clase de Tabla Hash en Python desde cero, sin diccionarios nativos. Debe incluir una función de hash polinomial, manejo de colisiones por encadenamiento con listas enlazadas y un mecanismo de Rehashing automático"*
* **Adaptación e Integración:**
  - Se construyó la clase "PolynomialHashFunction" aplicando el algoritmo de Horner sobre los caracteres ASCII del usuario.
  - Se modeló la estructura de colisiones con la clase auxiliar "NodoHash".


### 3. Pruebas Unitarias "tests/test_tree.py" y "tests/test_hash_table.py"

* **Prompt:**
  > *"Crea las pruebas unitarias en Python con unittest para validar el correcto funcionamiento de la navegación del árbol, la eliminación en cascada, la resolución de colisiones en la tabla hash y el rehashing automático."*
* **Adaptación e Integración:**
  - Se verificaron los casos de prueba ante rutas inexistentes, nombres duplicados en el mismo nivel de directorio y fallos de credenciales en la tabla hash.
  - Se verificaron los casos de prueba ante rutas inexistentes, nombres duplicados en el mismo nivel de directorio y fallos de credenciales en la tabla hash.

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
