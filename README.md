# Trabajo de Investigación de Análisis Numérico
**Semestre 2027-1** | Facultad de Ingeniería, UNAM  
**Profesor:** Ing. Ángel Brito Segura

Programa en Python que simula cinco problemas de una línea de ensamblaje automotriz y resuelve cada uno con los métodos numéricos vistos en el curso.

##  Integrantes
* Marín Pérez Daniela - *Ingeniería en Computación*
* Karen Joselin Barrera Castañeda  - *Ingeniería Eléctrica Electrónica*
* Emilio Alexander Chávez Suárez - *Ingeniería Eléctrica Electrónica*
* Valente Agama José Ángel - *Ingeniería Mecánica*

##  Contenido del Repositorio
* `codigo/ensamblaje_automotriz.py` — Programa principal.
* `escrito/` — Trabajo escrito (PDF).
* `presentacion/` — Material para la exposición.
* `README.md` — Este archivo informativa.

## ¿Qué hace el programa?

| Opción | Estación de la Línea | Métodos Numéricos | Tema |
| :---: | :--- | :--- | :---: |
| **1** | Brazo robótico de soldadura | Newton-Raphson | 2 |
| **2** | Circuito del motor de la banda | Gauss-Jordan, LU (Doolittle), Jacobi, Gauss-Seidel | 3 |
| **3** | Trayectoria y velocidad del robot pick-and-place | Lagrange y diferencias finitas hacia adelante | 4 |
| **4** | Energía de una estación de ensamble | Trapecio, Simpson 1/3 y 3/8 | 4 |
| **5** | Arranque del motor de la banda | Euler, Euler-Gauss, Runge-Kutta 4 | 5 |

##  Notas Técnicas y Validación
* **Criterio de paro:** Los métodos iterativos se detienen con el error relativo porcentual (Tema 1).
* **Robustez:** Todas las entradas se validan con bloques `try/except`. El programa no se cierra ante letras, campos vacíos, valores fuera de rango o el comando `Ctrl + C`.
* **Navegación:** En cualquier pregunta del sistema se puede escribir `q` para regresar al menú principal.
