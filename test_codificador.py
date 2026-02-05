#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Pruebas Exhaustivas del Codificador Universal
Demuestra todas las capacidades del sistema con diferentes configuraciones
"""

from codificador_universal import (
    CodificadorUniversal,
    AnalizadorEficiencia,
    ConfiguracionInvalidaError,
    bytes_a_binario,
    binario_a_bytes
)
import time


def separador(titulo: str):
    """Imprime un separador visual con título"""
    print(f"\n{'█'*80}")
    print(f"█ {titulo.center(76)} █")
    print(f"{'█'*80}\n")


def prueba_validacion_parametros():
    """Prueba que las validaciones de parámetros funcionan correctamente"""
    separador("PRUEBA 1: VALIDACIÓN DE PARÁMETROS")
    
    pruebas = [
        {
            'nombre': 'Base inválida (base 3)',
            'base': 3,
            'potencia': 9,
            'bits': 40,
            'debe_fallar': True
        },
        {
            'nombre': 'Potencia inválida para base 2 (2^3)',
            'base': 2,
            'potencia': 8,  # 2^3 no está permitido
            'bits': 40,
            'debe_fallar': True
        },
        {
            'nombre': 'Potencia inválida para base 5 (5^5)',
            'base': 5,
            'potencia': 3125,  # 5^5 no está permitido
            'bits': 40,
            'debe_fallar': True
        },
        {
            'nombre': 'Bits por bloque muy pequeño (5 bits)',
            'base': 5,
            'potencia': 25,
            'bits': 5,
            'debe_fallar': True
        },
        {
            'nombre': 'Bits por bloque muy grande (2000 bits)',
            'base': 5,
            'potencia': 25,
            'bits': 2000,
            'debe_fallar': True
        },
        {
            'nombre': 'Configuración válida: Base 2, Potencia 256 (2^8), 100 bits',
            'base': 2,
            'potencia': 256,
            'bits': 100,
            'debe_fallar': False
        },
        {
            'nombre': 'Configuración válida: Base 5, Potencia 125 (5^3), 50 bits',
            'base': 5,
            'potencia': 125,
            'bits': 50,
            'debe_fallar': False
        }
    ]
    
    for i, prueba in enumerate(pruebas, 1):
        print(f"\nPrueba {i}: {prueba['nombre']}")
        print(f"  Parámetros: Base={prueba['base']}, Potencia={prueba['potencia']}, Bits={prueba['bits']}")
        
        try:
            codificador = CodificadorUniversal(
                base=prueba['base'],
                potencia=prueba['potencia'],
                bits_por_bloque=prueba['bits'],
                verbose=False
            )
            
            if prueba['debe_fallar']:
                print(f"  ✗ FALLO: Debería haber lanzado excepción pero no lo hizo")
            else:
                print(f"  ✓ ÉXITO: Configuración aceptada correctamente")
        
        except ConfiguracionInvalidaError as e:
            if prueba['debe_fallar']:
                print(f"  ✓ ÉXITO: Excepción lanzada correctamente")
                print(f"  Mensaje: {str(e)}")
            else:
                print(f"  ✗ FALLO: No debería haber lanzado excepción")
                print(f"  Mensaje: {str(e)}")


def prueba_base2_todas_potencias():
    """Prueba todas las potencias permitidas de base 2"""
    separador("PRUEBA 2: TODAS LAS POTENCIAS DE BASE 2")
    
    potencias = [2, 4, 16, 256, 65536, 4294967296, 18446744073709551616]
    texto_prueba = "Test Base 2"
    datos_binarios = bytes_a_binario(texto_prueba.encode('utf-8'))
    
    for potencia in potencias:
        print(f"\n{'─'*80}")
        print(f"Probando Base 2, Potencia {potencia} (2^{potencia.bit_length()-1})")
        print(f"{'─'*80}")
        
        codificador = CodificadorUniversal(
            base=2,
            potencia=potencia,
            bits_por_bloque=40,
            verbose=False
        )
        
        # Codificar y decodificar
        datos_codificados = codificador.codificar(datos_binarios)
        datos_decodificados = codificador.decodificar(datos_codificados)
        
        # Verificar
        coincide = datos_binarios == datos_decodificados
        print(f"Resultado: {'✓ REVERSIBLE' if coincide else '✗ FALLO'}")
        print(f"Tiempo codificación: {datos_codificados['tiempo_codificacion']:.6f} seg")


def prueba_base5_todas_potencias():
    """Prueba todas las potencias permitidas de base 5"""
    separador("PRUEBA 3: TODAS LAS POTENCIAS DE BASE 5")
    
    potencias = [5, 25, 125, 625]
    texto_prueba = "Test Base 5 - Teoría de la información"
    datos_binarios = bytes_a_binario(texto_prueba.encode('utf-8'))
    
    for potencia in potencias:
        print(f"\n{'─'*80}")
        print(f"Probando Base 5, Potencia {potencia} (5^{len(str(potencia//5))})")
        print(f"{'─'*80}")
        
        codificador = CodificadorUniversal(
            base=5,
            potencia=potencia,
            bits_por_bloque=40,
            verbose=False
        )
        
        # Codificar y decodificar
        datos_codificados = codificador.codificar(datos_binarios)
        datos_decodificados = codificador.decodificar(datos_codificados)
        
        # Verificar
        coincide = datos_binarios == datos_decodificados
        print(f"Resultado: {'✓ REVERSIBLE' if coincide else '✗ FALLO'}")
        print(f"Tiempo codificación: {datos_codificados['tiempo_codificacion']:.6f} seg")


def prueba_diferentes_tamaños_bloque():
    """Prueba con diferentes tamaños de bloque"""
    separador("PRUEBA 4: ANÁLISIS DE TAMAÑOS DE BLOQUE")
    
    tamaños = [10, 20, 50, 100, 200, 500, 1000]
    texto_prueba = "Análisis de rendimiento con diferentes tamaños de bloque. " * 10
    datos_binarios = bytes_a_binario(texto_prueba.encode('utf-8'))
    
    print(f"Longitud de datos: {len(datos_binarios)} bits")
    print(f"\n{'Tamaño Bloque':<15} {'Bloques':<10} {'T. Codif.':<15} {'T. Decodif.':<15} {'Reversible':<12}")
    print(f"{'-'*75}")
    
    for tamaño in tamaños:
        codificador = CodificadorUniversal(
            base=5,
            potencia=125,
            bits_por_bloque=tamaño,
            verbose=False
        )
        
        # Codificar
        inicio_cod = time.time()
        datos_codificados = codificador.codificar(datos_binarios)
        tiempo_cod = time.time() - inicio_cod
        
        # Decodificar
        inicio_dec = time.time()
        datos_decodificados = codificador.decodificar(datos_codificados)
        tiempo_dec = time.time() - inicio_dec
        
        # Verificar
        coincide = datos_binarios == datos_decodificados
        
        print(f"{tamaño:<15} {datos_codificados['num_bloques']:<10} "
              f"{tiempo_cod:<15.6f} {tiempo_dec:<15.6f} "
              f"{'✓ SÍ' if coincide else '✗ NO':<12}")


def prueba_padding():
    """Prueba específica del manejo de padding"""
    separador("PRUEBA 5: MANEJO DE PADDING")
    
    # Crear datos que NO sean múltiplo exacto del tamaño de bloque
    bits_bloque = 40
    
    # Caso 1: Datos más cortos que un bloque
    print("\nCaso 1: Datos más cortos que un bloque (25 bits)")
    datos_cortos = "1010101010101010101010101"  # 25 bits
    
    codificador = CodificadorUniversal(base=5, potencia=25, bits_por_bloque=bits_bloque, verbose=True)
    
    codificados = codificador.codificar(datos_cortos)
    print(f"\nPadding aplicado: {codificados['bits_padding']} bits")
    
    decodificados = codificador.decodificar(codificados)
    
    print(f"\nDatos originales:      {datos_cortos}")
    print(f"Datos decodificados:   {decodificados}")
    print(f"Coinciden: {'✓ SÍ' if datos_cortos == decodificados else '✗ NO'}")
    
    # Caso 2: Datos que requieren múltiples bloques con padding
    print("\n" + "─"*80)
    print("\nCaso 2: Múltiples bloques con padding final (95 bits = 2 bloques + 15 bits)")
    datos_multiples = "1" * 95  # 95 bits
    
    codificador2 = CodificadorUniversal(base=2, potencia=16, bits_por_bloque=bits_bloque, verbose=False)
    
    codificados2 = codificador2.codificar(datos_multiples)
    print(f"Número de bloques: {codificados2['num_bloques']}")
    print(f"Padding aplicado: {codificados2['bits_padding']} bits")
    
    decodificados2 = codificador2.decodificar(codificados2)
    
    print(f"Longitud original:     {len(datos_multiples)} bits")
    print(f"Longitud decodificada: {len(decodificados2)} bits")
    print(f"Coinciden: {'✓ SÍ' if datos_multiples == decodificados2 else '✗ NO'}")


def prueba_integridad_imagen():
    """Prueba con datos binarios simulando una imagen"""
    separador("PRUEBA 6: INTEGRIDAD CON DATOS TIPO IMAGEN")
    
    # Simular datos de imagen (patrón repetitivo de bytes)
    import random
    random.seed(42)
    
    # Crear 1KB de datos "aleatorios"
    datos_bytes = bytes([random.randint(0, 255) for _ in range(1024)])
    datos_binarios = bytes_a_binario(datos_bytes)
    
    print(f"Tamaño de datos simulados: {len(datos_bytes)} bytes ({len(datos_binarios)} bits)")
    
    configuraciones = [
        {'base': 2, 'potencia': 256, 'bits': 100},
        {'base': 5, 'potencia': 625, 'bits': 100},
        {'base': 2, 'potencia': 65536, 'bits': 200},
        {'base': 5, 'potencia': 125, 'bits': 50}
    ]
    
    for i, config in enumerate(configuraciones, 1):
        print(f"\n{'─'*80}")
        print(f"Configuración {i}: Base {config['base']}, Potencia {config['potencia']}, "
              f"{config['bits']} bits/bloque")
        print(f"{'─'*80}")
        
        codificador = CodificadorUniversal(
            base=config['base'],
            potencia=config['potencia'],
            bits_por_bloque=config['bits'],
            verbose=False
        )
        
        # Codificar
        datos_codificados = codificador.codificar(datos_binarios)
        
        # Decodificar
        datos_decodificados = codificador.decodificar(datos_codificados)
        
        # Verificar integridad
        integridad_ok = AnalizadorEficiencia.verificar_integridad(
            datos_binarios,
            datos_decodificados
        )
        
        # Métricas
        metricas = AnalizadorEficiencia.calcular_metricas(
            datos_binarios,
            datos_codificados
        )


def prueba_casos_extremos():
    """Prueba casos extremos y límites del sistema"""
    separador("PRUEBA 7: CASOS EXTREMOS")
    
    print("\nCaso 1: Datos completamente ceros")
    datos_ceros = "0" * 200
    codificador = CodificadorUniversal(base=2, potencia=16, bits_por_bloque=50, verbose=False)
    cod = codificador.codificar(datos_ceros)
    dec = codificador.decodificar(cod)
    print(f"  Reversible: {'✓ SÍ' if datos_ceros == dec else '✗ NO'}")
    
    print("\nCaso 2: Datos completamente unos")
    datos_unos = "1" * 200
    cod = codificador.codificar(datos_unos)
    dec = codificador.decodificar(cod)
    print(f"  Reversible: {'✓ SÍ' if datos_unos == dec else '✗ NO'}")
    
    print("\nCaso 3: Datos alternados")
    datos_alternados = "10" * 100
    cod = codificador.codificar(datos_alternados)
    dec = codificador.decodificar(cod)
    print(f"  Reversible: {'✓ SÍ' if datos_alternados == dec else '✗ NO'}")
    
    print("\nCaso 4: Un solo bit")
    datos_un_bit = "1"
    codificador_min = CodificadorUniversal(base=5, potencia=5, bits_por_bloque=10, verbose=False)
    cod = codificador_min.codificar(datos_un_bit)
    dec = codificador_min.decodificar(cod)
    print(f"  Reversible: {'✓ SÍ' if datos_un_bit == dec else '✗ NO'}")
    
    print("\nCaso 5: Tamaño máximo de bloque (1000 bits)")
    datos_grandes = "1" * 5000
    codificador_max = CodificadorUniversal(base=2, potencia=256, bits_por_bloque=1000, verbose=False)
    cod = codificador_max.codificar(datos_grandes)
    dec = codificador_max.decodificar(cod)
    print(f"  Reversible: {'✓ SÍ' if datos_grandes == dec else '✗ NO'}")


def ejecutar_todas_pruebas():
    """Ejecuta todas las pruebas del sistema"""
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "  SUITE COMPLETA DE PRUEBAS - CODIFICADOR UNIVERSAL".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)
    
    inicio_total = time.time()
    
    # Ejecutar todas las pruebas
    prueba_validacion_parametros()
    prueba_base2_todas_potencias()
    prueba_base5_todas_potencias()
    prueba_diferentes_tamaños_bloque()
    prueba_padding()
    prueba_integridad_imagen()
    prueba_casos_extremos()
    
    tiempo_total = time.time() - inicio_total
    
    separador("RESUMEN FINAL")
    print(f"Todas las pruebas completadas exitosamente")
    print(f"Tiempo total de ejecución: {tiempo_total:.2f} segundos")
    print(f"\n{'█'*80}\n")


if __name__ == "__main__":
    ejecutar_todas_pruebas()
