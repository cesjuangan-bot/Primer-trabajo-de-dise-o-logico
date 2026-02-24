import hashlib
import time
import os

# ==============================
# CONFIGURACIÓN DE BASES
# ==============================

BASE2_PERMITIDAS = [4, 8, 16, 32, 64, 128, 256, 512, 1024]
BASE5_PERMITIDAS = [25, 125, 625, 3125, 15625]


# ==============================
# UTILIDADES GENERALES
# ==============================

def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def texto_a_binario(texto):
    return ''.join(format(ord(c), '08b') for c in texto)


def binario_a_texto(binario):
    texto = ""
    for i in range(0, len(binario), 8):
        byte = binario[i:i+8]
        if len(byte) == 8:
            texto += chr(int(byte, 2))
    return texto


def segmentar_bits(binario, tamaño_bloque):
    bloques = []
    padding = 0

    for i in range(0, len(binario), tamaño_bloque):
        bloque = binario[i:i+tamaño_bloque]
        if len(bloque) < tamaño_bloque:
            padding = tamaño_bloque - len(bloque)
            bloque += "0" * padding
        bloques.append(bloque)

    return bloques, padding


# ==============================
# CODIFICACIÓN BASE 2
# ==============================

def codificar_base2(bloques, potencia):
    print("\n--- PROCESO BASE 2 ---")
    resultados = []

    k = int(potencia).bit_length() - 1
    mascara = (2 ** k) - 1

    print(f"Potencia seleccionada: {potencia} (2^{k})")
    print(f"Máscara utilizada: {mascara}")

    for bloque in bloques:
        numero = int(bloque, 2)
        print(f"\nBloque binario: {bloque}")
        print(f"Decimal equivalente: {numero}")

        ventana = numero & mascara
        desplazado = numero >> k

        print(f"Ventana extraída: {ventana}")
        print(f"Resultado desplazado: {desplazado}")

        resultados.append((ventana, desplazado))

    return resultados


def decodificar_base2(resultados, potencia, tamaño_bloque):
    print("\n--- DECODIFICACIÓN BASE 2 ---")

    k = int(potencia).bit_length() - 1
    reconstruido = ""

    for ventana, desplazado in resultados:
        numero = (desplazado << k) | ventana
        binario = format(numero, f'0{tamaño_bloque}b')

        print(f"\nVentana: {ventana}")
        print(f"Desplazado: {desplazado}")
        print(f"Reconstruido decimal: {numero}")
        print(f"Reconstruido binario: {binario}")

        reconstruido += binario

    return reconstruido


# ==============================
# CODIFICACIÓN BASE 5
# ==============================

def codificar_base5(bloques, potencia):
    print("\n--- PROCESO BASE 5 ---")
    resultados = []

    for bloque in bloques:
        numero = int(bloque, 2)
        print(f"\nBloque binario: {bloque}")
        print(f"Decimal equivalente: {numero}")

        residuos = []
        n = numero

        while n > 0:
            cociente = n // potencia
            residuo = n % potencia
            print(f"{n} ÷ {potencia} = {cociente}, residuo {residuo}")
            residuos.append(residuo)
            n = cociente

        resultados.append(residuos)

    return resultados


def decodificar_base5(resultados, potencia, tamaño_bloque):
    print("\n--- DECODIFICACIÓN BASE 5 ---")
    reconstruido = ""

    for residuos in resultados:
        numero = 0
        for i, r in enumerate(residuos):
            numero += r * (potencia ** i)

        binario = format(numero, f'0{tamaño_bloque}b')

        print(f"\nResiduos: {residuos}")
        print(f"Reconstruido decimal: {numero}")
        print(f"Reconstruido binario: {binario}")

        reconstruido += binario

    return reconstruido


# ==============================
# PROCESAMIENTO DE IMÁGENES
# ==============================

def procesar_imagen(ruta, base, potencia, tamaño_bloque):
    with open(ruta, "rb") as f:
        datos = f.read()

    hash_original = sha256_bytes(datos)
    binario = ''.join(format(byte, '08b') for byte in datos)

    bloques, padding = segmentar_bits(binario, tamaño_bloque)

    if base == 2:
        codificado = codificar_base2(bloques, potencia)
        reconstruido_bin = decodificar_base2(codificado, potencia, tamaño_bloque)
    else:
        codificado = codificar_base5(bloques, potencia)
        reconstruido_bin = decodificar_base5(codificado, potencia, tamaño_bloque)

    if padding > 0:
        reconstruido_bin = reconstruido_bin[:-padding]

    bytes_reconstruidos = bytes(
        int(reconstruido_bin[i:i+8], 2)
        for i in range(0, len(reconstruido_bin), 8)
    )

    hash_nuevo = sha256_bytes(bytes_reconstruidos)

    print("\nHash original:", hash_original)
    print("Hash reconstruido:", hash_nuevo)

    if hash_original == hash_nuevo:
        print("Integridad verificada.")
    else:
        print("Error: los hashes no coinciden.")

    with open("imagen_reconstruida.bin", "wb") as f:
        f.write(bytes_reconstruidos)


# ==============================
# MENÚ PRINCIPAL
# ==============================

def main():
    print("Sistema Universal Actualizado")

    tipo = input("¿Deseas codificar Texto (T) o Imagen (I)? ").upper()

    base = int(input("Selecciona base (2 o 5): "))
    potencia = int(input("Selecciona potencia permitida: "))
    tamaño_bloque = int(input("Tamaño de bloque en bits: "))

    if base == 2 and potencia not in BASE2_PERMITIDAS:
        raise ValueError("Potencia no permitida para Base 2.")
    if base == 5 and potencia not in BASE5_PERMITIDAS:
        raise ValueError("Potencia no permitida para Base 5.")

    if tipo == "T":
        mensaje = input("Ingresa tu mensaje: ")

        binario = texto_a_binario(mensaje)
        bloques, padding = segmentar_bits(binario, tamaño_bloque)

        if base == 2:
            codificado = codificar_base2(bloques, potencia)
            reconstruido = decodificar_base2(codificado, potencia, tamaño_bloque)
        else:
            codificado = codificar_base5(bloques, potencia)
            reconstruido = decodificar_base5(codificado, potencia, tamaño_bloque)

        if padding > 0:
            reconstruido = reconstruido[:-padding]

        texto_final = binario_a_texto(reconstruido)

        print("\nMensaje reconstruido:", texto_final)

    elif tipo == "I":
        ruta = input("Ruta de la imagen: ")
        procesar_imagen(ruta, base, potencia, tamaño_bloque)


if __name__ == "__main__":
    main()
