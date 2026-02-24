import hashlib
import math
import os

# ==========================================================
# CONFIGURACIÓN GLOBAL
# ==========================================================

BASE2_PERMITIDAS = [4, 8, 16, 32, 64, 128, 256, 512, 1024]
BASE5_PERMITIDAS = [25, 125, 625, 3125, 15625]

TAMANOS_BLOQUE_PERMITIDOS = [10, 20, 30, 40, 50, 60]

MODO_DETALLADO = True
ANCHO_VISUAL = 64


# ==========================================================
# COLORES ANSI
# ==========================================================

class C:
    HEADER = "\033[95m"
    AZUL = "\033[94m"
    CYAN = "\033[96m"
    VERDE = "\033[92m"
    AMARILLO = "\033[93m"
    ROJO = "\033[91m"
    NEGRITA = "\033[1m"
    RESET = "\033[0m"


def panel(titulo):
    print(f"\n{C.HEADER}{C.NEGRITA}" + "═" * 70)
    print(f" {titulo}")
    print("═" * 70 + C.RESET)


def subpanel(titulo):
    print(f"\n{C.CYAN}" + "─" * 60)
    print(f" {titulo}")
    print("─" * 60 + C.RESET)


# ==========================================================
# UTILIDADES
# ==========================================================

def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def guardar_binario_visible(binario, nombre):
    with open(nombre, "w") as f:
        for i in range(0, len(binario), ANCHO_VISUAL):
            f.write(binario[i:i+ANCHO_VISUAL] + "\n")


def cargar_binario_visible(nombre):
    with open(nombre, "r") as f:
        return f.read().replace("\n", "")


# ==========================================================
# CONVERSIÓN TEXTO
# ==========================================================

def texto_a_binario(texto):
    panel("CONVERSIÓN TEXTO → BINARIO")
    resultado = ""
    for c in texto:
        bin_char = format(ord(c), '08b')
        if MODO_DETALLADO:
            print(f"{C.AMARILLO}{c}{C.RESET} → ASCII({ord(c)}) → {C.VERDE}{bin_char}{C.RESET}")
        resultado += bin_char
    return resultado


def binario_a_texto(binario):
    texto = ""
    for i in range(0, len(binario), 8):
        texto += chr(int(binario[i:i+8], 2))
    return texto


# ==========================================================
# SEGMENTACIÓN
# ==========================================================

def segmentar_bits(binario, tamaño_bloque):
    bloques = []
    padding = 0

    for i in range(0, len(binario), tamaño_bloque):
        bloque = binario[i:i+tamaño_bloque]
        if len(bloque) < tamaño_bloque:
            padding = tamaño_bloque - len(bloque)
            bloque += "0" * padding
        bloques.append(bloque)

    panel("PADDING Y SEGMENTACIÓN")
    print(f"{C.AZUL}Longitud total:{C.RESET} {len(binario)} bits")
    print(f"{C.AZUL}Tamaño bloque:{C.RESET} {tamaño_bloque} bits")
    print(f"{C.AZUL}Total de bloques generados:{C.RESET} {len(bloques)}")
    print(f"{C.AZUL}Padding aplicado:{C.RESET} {padding} bits")

    return bloques, padding


def mostrar_bloques_paginados(bloques):
    panel("VISUALIZACIÓN DE BLOQUES")

    for i, bloque in enumerate(bloques):
        print(f"{C.CYAN}Bloque {i+1}:{C.RESET} {bloque}")

        if (i + 1) % 10 == 0:
            input(f"{C.AMARILLO}Presione Enter para continuar...{C.RESET}")


# ==========================================================
# BASE 2
# ==========================================================

def codificar_base2(bloques, potencia, tamaño_bloque):
    panel("CODIFICACIÓN BASE 2")

    resultados = []
    k = int(potencia).bit_length() - 1
    mascara = (2 ** k) - 1

    for bloque in bloques:
        numero = int(bloque, 2)
        ventana = numero & mascara
        desplazado = numero >> k
        resultados.append((ventana, desplazado))

    return resultados


def decodificar_base2(resultados, potencia, tamaño_bloque):
    reconstruido = ""
    k = int(potencia).bit_length() - 1

    for ventana, desplazado in resultados:
        numero = (desplazado << k) | ventana
        reconstruido += format(numero, f'0{tamaño_bloque}b')

    return reconstruido


# ==========================================================
# MENÚ
# ==========================================================

def menu_principal():
    panel("SISTEMA PROFESIONAL MEJORADO")

    print("1️⃣  Texto")
    print("2️⃣  Imagen")
    opcion = input("Seleccione opción: ")

    base = int(input("Base (2 o 5): "))

    if base == 2:
        print("Potencias disponibles:", BASE2_PERMITIDAS)
    else:
        print("Potencias disponibles:", BASE5_PERMITIDAS)

    potencia = int(input("Seleccione potencia: "))

    print("Tamaños de bloque permitidos:", TAMANOS_BLOQUE_PERMITIDOS)
    tamaño_bloque = int(input("Seleccione tamaño de bloque en bits: "))

    if tamaño_bloque not in TAMANOS_BLOQUE_PERMITIDOS:
        print("Tamaño no permitido.")
        return

    if opcion == "1":
        mensaje = input("Ingrese mensaje: ")
        binario = texto_a_binario(mensaje)
        guardar_binario_visible(binario, "texto_original_binario.txt")

        bloques, padding = segmentar_bits(binario, tamaño_bloque)
        mostrar_bloques_paginados(bloques)

        codificado = codificar_base2(bloques, potencia, tamaño_bloque)
        reconstruido = decodificar_base2(codificado, potencia, tamaño_bloque)

        if padding > 0:
            reconstruido = reconstruido[:-padding]

        guardar_binario_visible(reconstruido, "texto_reconstruido_binario.txt")

        panel("RESULTADO FINAL")
        print(f"{C.VERDE}Mensaje reconstruido:{C.RESET}", binario_a_texto(reconstruido))

    preguntar_decodificacion()


# ==========================================================
# DECODIFICACIÓN FINAL
# ==========================================================

def preguntar_decodificacion():
    print("\n¿Desea decodificar un archivo binario visible?")
    opcion = input("S / N: ").upper()

    if opcion == "S":
        nombre = input("Nombre del archivo (.txt): ")

        if not os.path.exists(nombre):
            print("Archivo no encontrado.")
            return

        binario = cargar_binario_visible(nombre)

        print(f"{C.VERDE}Texto decodificado:{C.RESET}")
        print(binario_a_texto(binario))


if __name__ == "__main__":
    menu_principal()