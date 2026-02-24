import hashlib
import math
import os

# ==========================================================
# CONFIGURACIÓN GLOBAL
# ==========================================================

BASE2_PERMITIDAS = [4, 8, 16, 32, 64, 128, 256, 512, 1024]
BASE5_PERMITIDAS = [25, 125, 625, 3125, 15625]

MODO_DETALLADO = True
ANCHO_VISUAL = 64

# ==========================================================
# COLORES ANSI PROFESIONALES
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


# ==========================================================
# OPTIMIZACIÓN AUTOMÁTICA
# ==========================================================

def optimizar_bloque_base2(potencia):
    k = int(potencia).bit_length() - 1
    return k * 2  # equilibrio eficiencia / claridad


def optimizar_bloque_base5(potencia):
    return math.ceil(math.log2(potencia)) * 2


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
    print(f"{C.AZUL}Padding aplicado:{C.RESET} {padding} bits")

    return bloques, padding


# ==========================================================
# BASE 2
# ==========================================================

def codificar_base2(bloques, potencia, tamaño_bloque):
    panel("CODIFICACIÓN BASE 2")

    resultados = []
    k = int(potencia).bit_length() - 1
    mascara = (2 ** k) - 1

    for i, bloque in enumerate(bloques):
        numero = int(bloque, 2)
        ventana = numero & mascara
        desplazado = numero >> k

        if MODO_DETALLADO and i < 5:
            subpanel(f"Bloque {i+1}")
            print(f"Binario: {bloque}")
            print(f"Decimal: {numero}")
            print(f"Ventana: {ventana}")
            print(f"Desplazado: {desplazado}")

        resultados.append((ventana, desplazado))

    return resultados


def decodificar_base2(resultados, potencia, tamaño_bloque):
    panel("DECODIFICACIÓN BASE 2")

    reconstruido = ""
    k = int(potencia).bit_length() - 1

    for ventana, desplazado in resultados:
        numero = (desplazado << k) | ventana
        reconstruido += format(numero, f'0{tamaño_bloque}b')

    return reconstruido


# ==========================================================
# BASE 5
# ==========================================================

def codificar_base5(bloques, potencia):
    panel("CODIFICACIÓN BASE 5")

    resultados = []

    for i, bloque in enumerate(bloques):
        numero = int(bloque, 2)
        residuos = []
        n = numero

        while n > 0:
            residuos.append(n % potencia)
            n //= potencia

        resultados.append(residuos)

    return resultados


def decodificar_base5(resultados, potencia, tamaño_bloque):
    panel("DECODIFICACIÓN BASE 5")

    reconstruido = ""

    for residuos in resultados:
        numero = 0
        for i, r in enumerate(residuos):
            numero += r * (potencia ** i)
        reconstruido += format(numero, f'0{tamaño_bloque}b')

    return reconstruido


# ==========================================================
# PROCESAMIENTO IMAGEN
# ==========================================================

def procesar_imagen(ruta, base, potencia):

    with open(ruta, "rb") as f:
        datos = f.read()

    binario = ''.join(format(byte, '08b') for byte in datos)
    guardar_binario_visible(binario, "imagen_original_binaria.txt")

    if base == 2:
        tamaño_bloque = optimizar_bloque_base2(potencia)
    else:
        tamaño_bloque = optimizar_bloque_base5(potencia)

    bloques, padding = segmentar_bits(binario, tamaño_bloque)

    if base == 2:
        codificado = codificar_base2(bloques, potencia, tamaño_bloque)
        reconstruido = decodificar_base2(codificado, potencia, tamaño_bloque)
    else:
        codificado = codificar_base5(bloques, potencia)
        reconstruido = decodificar_base5(codificado, potencia, tamaño_bloque)

    if padding > 0:
        reconstruido = reconstruido[:-padding]

    guardar_binario_visible(reconstruido, "imagen_reconstruida_binaria.txt")

    bytes_reconstruidos = bytes(
        int(reconstruido[i:i+8], 2)
        for i in range(0, len(reconstruido), 8)
    )

    with open("imagen_reconstruida.bin", "wb") as f:
        f.write(bytes_reconstruidos)

    panel("VERIFICACIÓN SHA-256")
    print(f"{C.AMARILLO}Hash original:{C.RESET}", sha256_bytes(datos))
    print(f"{C.AMARILLO}Hash reconstruido:{C.RESET}", sha256_bytes(bytes_reconstruidos))

    if sha256_bytes(datos) == sha256_bytes(bytes_reconstruidos):
        print(f"{C.VERDE}✔ Integridad verificada{C.RESET}")
    else:
        print(f"{C.ROJO}✘ Error de integridad{C.RESET}")


# ==========================================================
# MENÚ AVANZADO
# ==========================================================

def menu_principal():
    panel("SISTEMA PROFESIONAL DE CODIFICACIÓN")

    print("1️⃣  Texto")
    print("2️⃣  Imagen")
    opcion = input("Seleccione opción: ")

    if opcion not in ["1", "2"]:
        print("Opción inválida.")
        return

    base = int(input("Base (2 o 5): "))

    if base == 2:
        print("Potencias disponibles:", BASE2_PERMITIDAS)
    else:
        print("Potencias disponibles:", BASE5_PERMITIDAS)

    potencia = int(input("Seleccione potencia: "))

    if opcion == "1":
        mensaje = input("Ingrese mensaje: ")
        binario = texto_a_binario(mensaje)
        guardar_binario_visible(binario, "texto_original_binario.txt")

        if base == 2:
            tamaño_bloque = optimizar_bloque_base2(potencia)
        else:
            tamaño_bloque = optimizar_bloque_base5(potencia)

        bloques, padding = segmentar_bits(binario, tamaño_bloque)

        if base == 2:
            codificado = codificar_base2(bloques, potencia, tamaño_bloque)
            reconstruido = decodificar_base2(codificado, potencia, tamaño_bloque)
        else:
            codificado = codificar_base5(bloques, potencia)
            reconstruido = decodificar_base5(codificado, potencia, tamaño_bloque)

        if padding > 0:
            reconstruido = reconstruido[:-padding]

        guardar_binario_visible(reconstruido, "texto_reconstruido_binario.txt")

        panel("RESULTADO FINAL")
        print(f"{C.VERDE}Mensaje reconstruido:{C.RESET}", binario_a_texto(reconstruido))

    else:
        ruta = input("Ruta de imagen: ")
        procesar_imagen(ruta, base, potencia)


if __name__ == "__main__":
    menu_principal()