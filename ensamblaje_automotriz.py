"""
===========================================================================
 PROYECTO FINAL - ANÁLISIS NUMÉRICO (Semestre 2027-1)
 Aplicaciones del Análisis Numérico en procesos de automatización
 de ensamblaje automotriz
---------------------------------------------------------------------------
 Integrantes:
   - Marín Pérez Daniela                   (Ing. en Computación)
   - Karen Joselin Barrera Castañeda       (Ing. Eléctrica Electrónica)
   - Emilio Alexander Chávez Suárez        (Ing. Eléctrica Electrónica)
   - Valente Agama José Ángel              (Ing. Mecánica)
---------------------------------------------------------------------------
 El programa simula cinco problemas reales de una línea de ensamblaje
 automotriz y resuelve cada uno con un método numérico distinto:
 
   1. Brazo robótico de soldadura -> Newton-Raphson                 (Tema 2)
   2. Circuito del motor de la banda -> Gauss-Jordan, LU Doolittle,
      Jacobi y Gauss-Seidel                                         (Tema 3)
   3. Trayectoria del robot pick-and-place -> Interpolación de
      Lagrange y derivación por diferencias finitas                 (Tema 4)
   4. Energía consumida por una estación -> Trapecio y Simpson      (Tema 4)
   5. Arranque del motor de la banda -> Euler, Euler-Gauss y RK4    (Tema 5)
   En todos los métodos iterativos el criterio de paro es el error
   relativo porcentual entre dos iteraciones                        (Tema 1)
 
 Requisitos: Python 3.8 o superior.
 Opcional:   matplotlib (pip install matplotlib) para ver gráficas.
             Si no está instalado, el programa funciona igual, sin gráficas.
 
 Robustez: todas las entradas del usuario se validan con bloques
 try/except, de modo que letras, campos vacíos, símbolos, valores fuera
 de rango, Ctrl+C o errores numéricos NO cierran el programa.
 En cualquier pregunta se puede escribir  q  para regresar al menú.
===========================================================================
"""

import math
import sys


try:
    import matplotlib.pyplot as plt
    HAY_GRAFICAS = True
except (ImportError, Exception, KeyboardInterrupt):
    HAY_GRAFICAS = False

# ===========================================================================
#  FUNCIONES DE LECTURA 
# ===========================================================================

class EntradaCancelada(Exception):
    """Se lanza cuando el usuario escribe 'q' para volver al menú."""
 
 
def leer_texto(mensaje):
    """Lee una línea de texto. Si se cierra la entrada (EOF) cancela."""
    try:
        texto = input(mensaje).strip()
    except EOFError:
        raise EntradaCancelada
    if texto.lower() in ("q", "salir", "menu", "menú"):
        raise EntradaCancelada
    return texto
 
 
def convertir_float(texto):
    """Convierte texto a número real finito. Acepta cla coma como  decimal."""
    valor = float(texto.replace(",", "."))   # puede lanzar ValueError
    if not math.isfinite(valor):              # float("nan") e "inf" sí convierten
        raise ValueError("valor no finito")
    return valor
 
 
def leer_float(mensaje, minimo=None, maximo=None, defecto=None,
               incluir_minimo=True):
    """
    Pide un número real hasta que el usuario escriba uno válido.
      minimo / maximo : límites permitidos; None = no tiene límite
      incluir_minimo  : False si el mínimo no cumple con el estipulado
      defecto         : Si el usuario sólo presiona Enter
    """
    while True:
        sufijo = f" [Enter = {defecto}]" if defecto is not None else ""
        texto = leer_texto(f"  {mensaje}{sufijo}: ")
 
        if texto == "" and defecto is not None:
            return float(defecto)
 
        try:
            valor = convertir_float(texto)
        except ValueError:
            print("ERROR: Dato inválido. Escriba un número, por ejemplo 12.5")
            continue
 
        if minimo is not None:
            if incluir_minimo and valor < minimo:
                print(f"ERROR: El valor debe ser mayor o igual que {minimo}.")
                continue
            if not incluir_minimo and valor <= minimo:
                print(f"ERROR: El valor debe ser mayor que {minimo}.")
                continue
        if maximo is not None and valor > maximo:
            print(f"ERROR: El valor debe ser menor o igual que {maximo}.")
            continue
        return valor
 
 
def leer_entero(mensaje, minimo, maximo, defecto=None):
    """Pide un número entero dentro del rango [minimo, maximo]."""
    while True:
        sufijo = f" [Enter = {defecto}]" if defecto is not None else ""
        texto = leer_texto(f"  {mensaje} ({minimo}-{maximo}){sufijo}: ")
 
        if texto == "" and defecto is not None:
            return defecto
        try:
            valor = int(texto)
        except ValueError:
            print("ERROR: Escriba un número entero (sin decimales ni letras).")
            continue
        if not (minimo <= valor <= maximo):
            print(f"ERROR: EL valor debe estar entre {minimo} y {maximo}.")
            continue
        return valor
 
 
def leer_si_no(mensaje):
    """Pregunta s/n. Devuelve True para 's' y False para 'n'."""
    while True:
        texto = leer_texto(f"  {mensaje} (s/n): ").lower()
        if texto in ("s", "si", "sí"):
            return True
        if texto in ("n", "no"):
            return False
        print("ERROR: Responda 's' o 'n'.")
 
 
def leer_lista_floats(mensaje, cantidad, minimo=None):
    """
    Lee 'cantidad' números escritos en una sola línea, separados por
    espacios.
    """
    while True:
        texto = leer_texto(f"  {mensaje}\n  > ")
        partes = texto.split()
        if len(partes) != cantidad:
            print(f"ERROR: Escribiste {len(partes)} valores y se "
                  f"necesitan exactamente {cantidad}.")
            continue
        try:
            valores = [convertir_float(p) for p in partes]
        except ValueError:
            print("ERROR: Algún valor no es un número válido.")
            continue
        if minimo is not None and any(v < minimo for v in valores):
            print(f"ERROR: Todos los valores deben ser >= {minimo}.")
            continue
        return valores
 
 
def pausa():
    """Espera a que el usuario presione Enter (sin romperse con Ctrl+C)."""
    try:
        input("\n  Presiona Enter para volver al menú...")
    except (EOFError, KeyboardInterrupt):
        print()
 
 
def mostrar_grafica(funcion_dibujo):
    """Muestra una gráfica sólo si matplotlib existe y el usuario quiere."""
    if not HAY_GRAFICAS:
        print("  (Instala matplotlib para ver gráficas: pip install matplotlib)")
        return
    if not leer_si_no("¿Desea ver la gráfica?"):
        return
    try:
        funcion_dibujo()
        plt.show()
    except Exception as e:  
        print(f"AVISO: No se pudo mostrar la gráfica: {e}")
 
 
def encabezado(titulo):
    print("\n" + "=" * 70)
    print(f"  {titulo}")
    print("=" * 70)

# ===========================================================================
#                        Menú y validación de entradas 
# ===========================================================================

MODULOS = ["Brazo robótico de soldadura (Newton-Raphson)",
           "Circuito del motor de la banda (Gauss-Jordan / LU / Jacobi / Gauss-Seidel)",
           "Trayectoria y velocidad del robot (Lagrange / Diferencias finitas)",
           "Energía de una estación de ensamble (Trapecio / Simpson)",
           "Arranque del motor de la banda (Euler / Euler-Gauss / RK4)"]


def prueba_validacion(nombre):
    """Mientras el módulo está en desarrollo, prueba la lectura segura de datos."""
    encabezado(nombre)
    print("  Módulo en desarrollo. Prueba de validación de datos:\n")
    v = leer_float("Un valor real positivo (ej. una resistencia en ohms)", 0, 1e6,
                   10, incluir_minimo=False)
    n = leer_entero("Un número entero de puntos", 2, 10)
    datos = leer_lista_floats(f"Escribe {n} valores separados por espacios:", n)
    print(f"\n  Datos válidos recibidos: {v}, {n}, {datos}")


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    while True:
        encabezado("ANÁLISIS NUMÉRICO EN LA AUTOMATIZACIÓN DEL ENSAMBLAJE AUTOMOTRIZ")
        for i, texto in enumerate(MODULOS, 1):
            print(f"   {i}. {texto}")
        print("   0. Salir")
        print("  (En cualquier pregunta puedes escribir 'q' para volver aquí)")
        try:
            opcion = input("\n  Elige una opción: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Saliendo del programa. ¡Hasta luego!")
            break
        if opcion == "0":
            print("  Saliendo del programa. ¡Hasta luego!")
            break
        if opcion not in ("1", "2", "3", "4", "5"):
            print("    [Error] Opción no válida. Escribe un número del 0 al 5.")
            continue
        try:
            prueba_validacion(MODULOS[int(opcion) - 1])
        except EntradaCancelada:
            print("\n  Regresando al menú...")
        except KeyboardInterrupt:
            print("\n  Operación cancelada con Ctrl+C. Regresando al menú...")
        except Exception as e:
            print(f"\n    [Error inesperado] {type(e).__name__}: {e}")
        pausa()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n  Programa terminado por el usuario.")