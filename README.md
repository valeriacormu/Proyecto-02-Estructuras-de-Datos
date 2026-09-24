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