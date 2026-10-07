# Proyecto-02-Estructuras-de-Datos
Sistema de Archivos Distribuido y Enrutador de Red (EIF207 Estructuras de Datos)

## Ejecución

```
python main.py                          # menú interactivo
python -m unittest discover -s tests -t .   # pruebas unitarias
```

Opción 11 del menú carga una red de ejemplo (usuario `admin` / `admin123` en cada servidor). Cada servidor nuevo se crea con ese usuario inicial.

## Estructura

| Módulo | Contenido |
|---|---|
| `filesystem/tree.py` | Árbol general de directorios, búsqueda recursiva, eliminación en cascada (postorden) |
| `filesystem/hash_table.py` | Tabla hash propia (hash polinomial, encadenamiento, rehashing) |
| `network/graph.py` | Grafo ponderado, Dijkstra (heap), BFS/DFS |
| `network/servidor.py` | Servidor = árbol propio + tabla hash propia + sesión |
| `audit/logger.py` | Auditoría a `network_audit_log.txt` |
| `main.py` | `NetworkOS` (integra todo) y menú interactivo |

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


### 7. Integración, menú y búsqueda recursiva "main.py", "network/servidor.py"

* **Prompt (resumido):**
  > *"Genera el main.py con el menú interactivo, la clase Servidor (árbol y tabla hash propios por servidor), la búsqueda recursiva de archivos y las pruebas de integración, conectando todo a la auditoría."*
* **Adaptación e Integración:**
  - Se creó la clase "Servidor" (árbol + tabla hash propios) y "NetworkOS" para mantener sincronizados el grafo y los servidores.
  - Se escribió "AuditoriaTreeLogger" para que los logs del árbol (antes solo a consola) lleguen a "network_audit_log.txt" con el nombre del servidor.
  - Inicio de sesión exitoso/fallido, registro de usuarios y búsquedas quedan auditados; las contraseñas se guardan como SHA-256 en la tabla hash.
  - Se agregó "buscar_recursivo" (DFS preorden) al árbol y "tests/test_integracion.py".
