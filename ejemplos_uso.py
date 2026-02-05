#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplos Específicos de Uso del Codificador Universal
Demuestra casos de uso prácticos y escenarios comunes
"""

from codificador_universal import (
    CodificadorUniversal,
    AnalizadorEficiencia,
    bytes_a_binario,
    binario_a_bytes,
    ConfiguracionInvalidaError
)


def ejemplo_1_texto_simple():
    """Ejemplo 1: Codificar texto simple con Base 5"""
    print("\n" + "="*80)
    print("EJEMPLO 1: Codificación de Texto Simple con Base 5")
    print("="*80)
    
    texto = "Python es poderoso!"
    print(f"\nTexto original: '{texto}'")
    
    # Convertir a binario
    datos_bytes = texto.encode('utf-8')
    datos_binarios = bytes_a_binario(datos_bytes)
    
    print(f"Tamaño: {len(datos_bytes)} bytes = {len(datos_binarios)} bits")
    
    # Configurar codificador: Base 5, Potencia 125 (5^3), 50 bits por bloque
    codificador = CodificadorUniversal(
        base=5,
        potencia=125,
        bits_por_bloque=50,
        verbose=False
    )
    
    # Codificar
    print(f"\nConfigurando codificador:")
    print(f"  - Base: 5")
    print(f"  - Potencia: 125 (5³)")
    print(f"  - Bits por bloque: 50")
    
    datos_codificados = codificador.codificar(datos_binarios)
    
    print(f"\nResultados de codificación:")
    print(f"  - Bloques generados: {datos_codificados['num_bloques']}")
    print(f"  - Padding añadido: {datos_codificados['bits_padding']} bits")
    print(f"  - Tiempo: {datos_codificados['tiempo_codificacion']:.6f} seg")
    
    # Decodificar
    datos_decodificados = codificador.decodificar(datos_codificados)
    
    # Reconstruir texto
    datos_reconstruidos_bytes = binario_a_bytes(datos_decodificados)
    texto_reconstruido = datos_reconstruidos_bytes[:len(datos_bytes)].decode('utf-8')
    
    # Verificar
    coincide = texto == texto_reconstruido
    print(f"\nTexto reconstruido: '{texto_reconstruido}'")
    print(f"Verificación: {'✓ ÉXITO' if coincide else '✗ FALLO'}")
    
    # Verificar integridad completa
    integridad = AnalizadorEficiencia.verificar_integridad(datos_binarios, datos_decodificados)


def ejemplo_2_comparacion_bases():
    """Ejemplo 2: Comparar rendimiento entre Base 2 y Base 5"""
    print("\n" + "="*80)
    print("EJEMPLO 2: Comparación de Rendimiento entre Bases")
    print("="*80)
    
    # Datos de prueba
    texto = "Análisis comparativo de sistemas de codificación reversible. " * 5
    datos_bytes = texto.encode('utf-8')
    datos_binarios = bytes_a_binario(datos_bytes)
    
    print(f"\nDatos de prueba: {len(datos_binarios)} bits")
    
    configuraciones = [
        {'nombre': 'Base 2 - Potencia 256', 'base': 2, 'potencia': 256, 'bits': 100},
        {'nombre': 'Base 5 - Potencia 625', 'base': 5, 'potencia': 625, 'bits': 100},
        {'nombre': 'Base 2 - Potencia 65536', 'base': 2, 'potencia': 65536, 'bits': 200},
        {'nombre': 'Base 5 - Potencia 125', 'base': 5, 'potencia': 125, 'bits': 50},
    ]
    
    print(f"\n{'Configuración':<30} {'Bloques':<10} {'T.Cod(s)':<12} {'T.Dec(s)':<12} {'OK':<5}")
    print("-" * 80)
    
    for config in configuraciones:
        codificador = CodificadorUniversal(
            base=config['base'],
            potencia=config['potencia'],
            bits_por_bloque=config['bits'],
            verbose=False
        )
        
        # Codificar
        import time
        inicio = time.time()
        cod = codificador.codificar(datos_binarios)
        tiempo_cod = time.time() - inicio
        
        # Decodificar
        inicio = time.time()
        dec = codificador.decodificar(cod)
        tiempo_dec = time.time() - inicio
        
        # Verificar
        ok = datos_binarios == dec
        
        print(f"{config['nombre']:<30} {cod['num_bloques']:<10} "
              f"{tiempo_cod:<12.6f} {tiempo_dec:<12.6f} {'✓' if ok else '✗':<5}")


def ejemplo_3_manejo_errores():
    """Ejemplo 3: Demostración de manejo de errores"""
    print("\n" + "="*80)
    print("EJEMPLO 3: Manejo de Errores y Validaciones")
    print("="*80)
    
    casos_invalidos = [
        {
            'desc': 'Base inválida (base 10)',
            'base': 10,
            'potencia': 100,
            'bits': 40
        },
        {
            'desc': 'Potencia no permitida para Base 2 (2^5 = 32)',
            'base': 2,
            'potencia': 32,
            'bits': 40
        },
        {
            'desc': 'Bloque demasiado pequeño (5 bits)',
            'base': 5,
            'potencia': 25,
            'bits': 5
        },
        {
            'desc': 'Bloque demasiado grande (1500 bits)',
            'base': 5,
            'potencia': 25,
            'bits': 1500
        }
    ]
    
    for i, caso in enumerate(casos_invalidos, 1):
        print(f"\nCaso {i}: {caso['desc']}")
        print(f"  Intentando: Base={caso['base']}, Potencia={caso['potencia']}, Bits={caso['bits']}")
        
        try:
            codificador = CodificadorUniversal(
                base=caso['base'],
                potencia=caso['potencia'],
                bits_por_bloque=caso['bits'],
                verbose=False
            )
            print(f"  ✗ ERROR: Debería haber fallado pero se aceptó")
        except ConfiguracionInvalidaError as e:
            print(f"  ✓ CORRECTO: Rechazado apropiadamente")
            print(f"  Mensaje: {str(e)}")


def ejemplo_4_padding_detallado():
    """Ejemplo 4: Análisis detallado del manejo de padding"""
    print("\n" + "="*80)
    print("EJEMPLO 4: Análisis Detallado del Padding")
    print("="*80)
    
    # Crear datos que NO sean múltiplo del tamaño de bloque
    tamaño_bloque = 40
    
    casos = [
        {'desc': 'Datos exactos (80 bits = 2 bloques exactos)', 'bits': 80},
        {'desc': 'Datos con padding pequeño (85 bits = 2 bloques + 5 bits)', 'bits': 85},
        {'desc': 'Datos con padding grande (125 bits = 3 bloques + 5 bits)', 'bits': 125},
        {'desc': 'Datos menores a un bloque (25 bits)', 'bits': 25}
    ]
    
    codificador = CodificadorUniversal(base=2, potencia=16, bits_por_bloque=tamaño_bloque, verbose=False)
    
    print(f"\nTamaño de bloque: {tamaño_bloque} bits\n")
    print(f"{'Caso':<50} {'Bits':<8} {'Bloques':<10} {'Padding':<10} {'OK':<5}")
    print("-" * 90)
    
    for caso in casos:
        # Crear datos binarios del tamaño especificado
        datos = "1" * caso['bits']
        
        # Codificar
        cod = codificador.codificar(datos)
        
        # Decodificar
        dec = codificador.decodificar(cod)
        
        # Verificar
        ok = datos == dec
        
        print(f"{caso['desc']:<50} {caso['bits']:<8} {cod['num_bloques']:<10} "
              f"{cod['bits_padding']:<10} {'✓' if ok else '✗':<5}")


def ejemplo_5_todas_potencias():
    """Ejemplo 5: Probar todas las potencias permitidas"""
    print("\n" + "="*80)
    print("EJEMPLO 5: Prueba de Todas las Potencias Permitidas")
    print("="*80)
    
    # Datos de prueba
    texto = "Test de potencias"
    datos_binarios = bytes_a_binario(texto.encode('utf-8'))
    
    print(f"\nDatos de prueba: {len(datos_binarios)} bits")
    
    # Base 2
    print(f"\n{'─'*80}")
    print("BASE 2 - Potencias Permitidas")
    print(f"{'─'*80}")
    
    potencias_base2 = [2, 4, 16, 256, 65536, 4294967296, 18446744073709551616]
    exponentes_base2 = [1, 2, 4, 8, 16, 32, 64]
    
    print(f"\n{'Potencia (2^n)':<25} {'Valor':<25} {'Bloques':<10} {'Reversible':<12}")
    print("-" * 80)
    
    for pot, exp in zip(potencias_base2, exponentes_base2):
        codificador = CodificadorUniversal(base=2, potencia=pot, bits_por_bloque=50, verbose=False)
        cod = codificador.codificar(datos_binarios)
        dec = codificador.decodificar(cod)
        ok = datos_binarios == dec
        
        print(f"2^{exp:<22} {pot:<25} {cod['num_bloques']:<10} {'✓ SÍ' if ok else '✗ NO':<12}")
    
    # Base 5
    print(f"\n{'─'*80}")
    print("BASE 5 - Potencias Permitidas")
    print(f"{'─'*80}")
    
    potencias_base5 = [5, 25, 125, 625]
    exponentes_base5 = [1, 2, 3, 4]
    
    print(f"\n{'Potencia (5^n)':<25} {'Valor':<25} {'Bloques':<10} {'Reversible':<12}")
    print("-" * 80)
    
    for pot, exp in zip(potencias_base5, exponentes_base5):
        codificador = CodificadorUniversal(base=5, potencia=pot, bits_por_bloque=50, verbose=False)
        cod = codificador.codificar(datos_binarios)
        dec = codificador.decodificar(cod)
        ok = datos_binarios == dec
        
        print(f"5^{exp:<22} {pot:<25} {cod['num_bloques']:<10} {'✓ SÍ' if ok else '✗ NO':<12}")


def ejemplo_6_analisis_expansion():
    """Ejemplo 6: Análisis de tasa de expansión"""
    print("\n" + "="*80)
    print("EJEMPLO 6: Análisis de Tasa de Expansión")
    print("="*80)
    
    # Datos de prueba de diferentes tamaños
    tamaños = [100, 500, 1000, 5000]
    
    print(f"\n{'Tamaño Original':<20} {'Base':<8} {'Potencia':<12} {'Expansión':<12} {'Eficiencia':<15}")
    print("-" * 80)
    
    for tamaño in tamaños:
        datos = "1" * tamaño
        
        # Base 2
        cod2 = CodificadorUniversal(base=2, potencia=256, bits_por_bloque=100, verbose=False)
        resultado2 = cod2.codificar(datos)
        metricas2 = AnalizadorEficiencia.calcular_metricas(datos, resultado2)
        
        print(f"{tamaño:<20} {'2':<8} {'256':<12} {metricas2['tasa_expansion']:<12.4f} "
              f"{(1/metricas2['tasa_expansion']*100):<15.2f}%")
        
        # Base 5
        cod5 = CodificadorUniversal(base=5, potencia=625, bits_por_bloque=100, verbose=False)
        resultado5 = cod5.codificar(datos)
        metricas5 = AnalizadorEficiencia.calcular_metricas(datos, resultado5)
        
        print(f"{tamaño:<20} {'5':<8} {'625':<12} {metricas5['tasa_expansion']:<12.4f} "
              f"{(1/metricas5['tasa_expansion']*100):<15.2f}%")


def ejemplo_7_verbose_detallado():
    """Ejemplo 7: Salida detallada paso a paso"""
    print("\n" + "="*80)
    print("EJEMPLO 7: Proceso Detallado con Verbose=True")
    print("="*80)
    
    print("\nEste ejemplo muestra el proceso completo paso a paso.")
    print("Se codificará el texto 'ABC' con Base 5, Potencia 25, bloques de 30 bits")
    
    texto = "ABC"
    datos_binarios = bytes_a_binario(texto.encode('utf-8'))
    
    print(f"\nTexto: '{texto}'")
    print(f"Binario: {datos_binarios}")
    print(f"Longitud: {len(datos_binarios)} bits")
    
    # Crear codificador con verbose=True para ver todo el proceso
    codificador = CodificadorUniversal(
        base=5,
        potencia=25,
        bits_por_bloque=30,
        verbose=True  # ACTIVAR SALIDA DETALLADA
    )
    
    # Codificar (mostrará proceso detallado)
    datos_codificados = codificador.codificar(datos_binarios)
    
    # Decodificar (mostrará proceso detallado)
    datos_decodificados = codificador.decodificar(datos_codificados)
    
    # Verificar
    texto_reconstruido = binario_a_bytes(datos_decodificados)[:len(texto)].decode('utf-8')
    print(f"\nTexto reconstruido: '{texto_reconstruido}'")
    print(f"Coincide: {'✓ SÍ' if texto == texto_reconstruido else '✗ NO'}")


def ejecutar_todos_ejemplos():
    """Ejecuta todos los ejemplos en secuencia"""
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "EJEMPLOS DE USO - CODIFICADOR UNIVERSAL".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)
    
    ejemplos = [
        ejemplo_1_texto_simple,
        ejemplo_2_comparacion_bases,
        ejemplo_3_manejo_errores,
        ejemplo_4_padding_detallado,
        ejemplo_5_todas_potencias,
        ejemplo_6_analisis_expansion,
        ejemplo_7_verbose_detallado
    ]
    
    for ejemplo in ejemplos:
        ejemplo()
        print()  # Espacio entre ejemplos
    
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "TODOS LOS EJEMPLOS COMPLETADOS".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80 + "\n")


if __name__ == "__main__":
    ejecutar_todos_ejemplos()
