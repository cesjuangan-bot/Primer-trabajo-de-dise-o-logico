#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Codificador/Decodificador Universal Totalmente Reversible
Especializado en Teoría de la Información y Sistemas Reversibles

Este sistema implementa un codificador matemáticamente transparente
que trabaja a nivel de bits con bases y potencias restringidas.
"""

import hashlib
import time
from typing import List, Tuple, Dict, Any
from pathlib import Path


class ConfiguracionInvalidaError(Exception):
    """Excepción lanzada cuando se intenta usar una configuración inválida"""
    pass


class CodificadorUniversal:
    """
    Codificador/Decodificador Universal con restricciones estrictas
    en bases, potencias y tamaños de bloque.
    """
    
    # Definición estricta de potencias permitidas
    POTENCIAS_BASE_2 = [2**1, 2**2, 2**4, 2**8, 2**16, 2**32, 2**64]
    POTENCIAS_BASE_5 = [5**1, 5**2, 5**3, 5**4]  # 5, 25, 125, 625
    
    # Rango de tamaño de bloque permitido
    BITS_MINIMO = 10
    BITS_MAXIMO = 1000
    
    def __init__(self, base: int, potencia: int, bits_por_bloque: int, verbose: bool = True):
        """
        Inicializa el codificador con parámetros estrictos.
        
        Args:
            base: Base numérica (2 o 5 únicamente)
            potencia: Potencia de la base (debe estar en las listas permitidas)
            bits_por_bloque: Tamaño del bloque en bits (10-1000)
            verbose: Si True, imprime información detallada del proceso
        
        Raises:
            ConfiguracionInvalidaError: Si algún parámetro es inválido
        """
        self.verbose = verbose
        
        # Validación estricta de base
        if base not in [2, 5]:
            raise ConfiguracionInvalidaError(
                f"Base {base} no permitida. Solo se permiten bases 2 y 5."
            )
        
        # Validación estricta de potencia según la base
        if base == 2:
            if potencia not in self.POTENCIAS_BASE_2:
                raise ConfiguracionInvalidaError(
                    f"Potencia {potencia} no permitida para base 2. "
                    f"Potencias permitidas: {self.POTENCIAS_BASE_2}"
                )
        elif base == 5:
            if potencia not in self.POTENCIAS_BASE_5:
                raise ConfiguracionInvalidaError(
                    f"Potencia {potencia} no permitida para base 5. "
                    f"Potencias permitidas: {self.POTENCIAS_BASE_5}"
                )
        
        # Validación estricta de tamaño de bloque
        if not (self.BITS_MINIMO <= bits_por_bloque <= self.BITS_MAXIMO):
            raise ConfiguracionInvalidaError(
                f"Tamaño de bloque {bits_por_bloque} fuera de rango. "
                f"Permitido: {self.BITS_MINIMO}-{self.BITS_MAXIMO} bits"
            )
        
        self.base = base
        self.potencia = potencia
        self.bits_por_bloque = bits_por_bloque
        
        if self.verbose:
            print(f"\n{'='*70}")
            print(f"CODIFICADOR UNIVERSAL INICIALIZADO")
            print(f"{'='*70}")
            print(f"Base: {self.base}")
            print(f"Potencia: {self.potencia}")
            print(f"Bits por bloque: {self.bits_por_bloque}")
            print(f"{'='*70}\n")
    
    def binario_a_bloques(self, datos_binarios: str) -> Tuple[List[str], int]:
        """
        Segmenta una cadena binaria en bloques de tamaño fijo.
        Aplica padding si es necesario.
        
        Args:
            datos_binarios: Cadena de bits (solo '0' y '1')
        
        Returns:
            Tupla (lista_de_bloques, bits_de_padding_añadidos)
        """
        bloques = []
        bits_padding = 0
        
        # Segmentar en bloques
        for i in range(0, len(datos_binarios), self.bits_por_bloque):
            bloque = datos_binarios[i:i + self.bits_por_bloque]
            
            # Aplicar padding si el último bloque es incompleto
            if len(bloque) < self.bits_por_bloque:
                bits_padding = self.bits_por_bloque - len(bloque)
                bloque = bloque + '0' * bits_padding
                
                if self.verbose:
                    print(f"\n⚠️  PADDING APLICADO:")
                    print(f"   Bloque incompleto con {len(datos_binarios[i:])} bits")
                    print(f"   Se añadieron {bits_padding} ceros de padding")
            
            bloques.append(bloque)
        
        return bloques, bits_padding
    
    def codificar_bloque_base2(self, bloque_binario: str, numero_bloque: int) -> List[int]:
        """
        Codifica un bloque usando desplazamientos binarios y máscaras.
        
        Args:
            bloque_binario: Cadena de bits del bloque
            numero_bloque: Número de bloque para registro
        
        Returns:
            Lista de valores codificados (ventanas binarias)
        """
        # Paso 1: Conversión a decimal
        valor_decimal = int(bloque_binario, 2)
        
        if self.verbose:
            print(f"\n{'─'*70}")
            print(f"CODIFICACIÓN BLOQUE #{numero_bloque} (BASE 2)")
            print(f"{'─'*70}")
            print(f"Bloque binario original ({len(bloque_binario)} bits):")
            print(f"  {bloque_binario}")
            print(f"\nPaso 1 - Conversión a decimal:")
            print(f"  Valor decimal: {valor_decimal}")
        
        # Paso 2: Aplicar desplazamientos y máscaras
        ventanas = []
        bits_ventana = self.potencia.bit_length() - 1  # Ancho de la ventana
        mascara = self.potencia - 1  # Máscara para extraer bits
        
        valor_actual = valor_decimal
        posicion = 0
        
        if self.verbose:
            print(f"\nPaso 2 - Desplazamientos binarios:")
            print(f"  Ancho de ventana: {bits_ventana} bits")
            print(f"  Máscara: {bin(mascara)} ({mascara})")
            print(f"\n  Proceso de extracción:")
        
        while valor_actual > 0:
            ventana = valor_actual & mascara
            ventanas.append(ventana)
            
            if self.verbose:
                print(f"    Posición {posicion}: {valor_actual} & {mascara} = {ventana}")
            
            valor_actual >>= bits_ventana
            posicion += 1
        
        if not ventanas:  # Bloque completamente de ceros
            ventanas = [0]
        
        if self.verbose:
            print(f"\n  Valores de ventanas extraídos: {ventanas}")
        
        return ventanas
    
    def codificar_bloque_base5(self, bloque_binario: str, numero_bloque: int) -> List[int]:
        """
        Codifica un bloque usando divisiones sucesivas por la potencia de base 5.
        
        Args:
            bloque_binario: Cadena de bits del bloque
            numero_bloque: Número de bloque para registro
        
        Returns:
            Lista de residuos (representación en base 5)
        """
        # Paso 1: Conversión a decimal
        valor_decimal = int(bloque_binario, 2)
        
        if self.verbose:
            print(f"\n{'─'*70}")
            print(f"CODIFICACIÓN BLOQUE #{numero_bloque} (BASE 5)")
            print(f"{'─'*70}")
            print(f"Bloque binario original ({len(bloque_binario)} bits):")
            print(f"  {bloque_binario}")
            print(f"\nPaso 1 - Conversión a decimal:")
            print(f"  Valor decimal: {valor_decimal}")
        
        # Paso 2: Divisiones sucesivas
        residuos = []
        cociente = valor_decimal
        iteracion = 0
        
        if self.verbose:
            print(f"\nPaso 2 - Divisiones sucesivas por {self.potencia}:")
            print(f"  {'Iteración':<10} {'Cociente':<20} {'÷ {self.potencia}':<15} {'= Q':<20} {'R':<10}")
            print(f"  {'-'*75}")
        
        while cociente > 0:
            residuo = cociente % self.potencia
            cociente = cociente // self.potencia
            residuos.append(residuo)
            
            if self.verbose:
                print(f"  {iteracion:<10} {cociente * self.potencia + residuo:<20} "
                      f"{'÷ ' + str(self.potencia):<15} {cociente:<20} {residuo:<10}")
            
            iteracion += 1
        
        if not residuos:  # Valor es cero
            residuos = [0]
        
        if self.verbose:
            print(f"\n  Residuos obtenidos: {residuos}")
        
        return residuos
    
    def codificar(self, datos_binarios: str) -> Dict[str, Any]:
        """
        Codifica una cadena binaria completa.
        
        Args:
            datos_binarios: Cadena de bits a codificar
        
        Returns:
            Diccionario con datos codificados y metadatos
        """
        inicio = time.time()
        
        # Segmentar en bloques
        bloques, bits_padding = self.binario_a_bloques(datos_binarios)
        
        if self.verbose:
            print(f"\n{'='*70}")
            print(f"INICIO DE CODIFICACIÓN")
            print(f"{'='*70}")
            print(f"Total de bits: {len(datos_binarios)}")
            print(f"Número de bloques: {len(bloques)}")
            print(f"Bits de padding: {bits_padding}")
            print(f"{'='*70}")
        
        # Codificar cada bloque
        bloques_codificados = []
        
        for idx, bloque in enumerate(bloques, 1):
            if self.base == 2:
                valores = self.codificar_bloque_base2(bloque, idx)
            else:  # base == 5
                valores = self.codificar_bloque_base5(bloque, idx)
            
            bloques_codificados.append(valores)
        
        tiempo_codificacion = time.time() - inicio
        
        resultado = {
            'bloques_codificados': bloques_codificados,
            'bits_padding': bits_padding,
            'base': self.base,
            'potencia': self.potencia,
            'bits_por_bloque': self.bits_por_bloque,
            'num_bloques': len(bloques),
            'bits_originales': len(datos_binarios),
            'tiempo_codificacion': tiempo_codificacion
        }
        
        if self.verbose:
            print(f"\n{'='*70}")
            print(f"CODIFICACIÓN COMPLETADA")
            print(f"{'='*70}")
            print(f"Tiempo de codificación: {tiempo_codificacion:.6f} segundos")
            print(f"{'='*70}\n")
        
        return resultado
    
    def decodificar_bloque_base2(self, valores: List[int], numero_bloque: int) -> str:
        """
        Decodifica un bloque codificado en base 2.
        
        Args:
            valores: Lista de ventanas binarias
            numero_bloque: Número de bloque para registro
        
        Returns:
            Cadena binaria reconstruida
        """
        if self.verbose:
            print(f"\n{'─'*70}")
            print(f"DECODIFICACIÓN BLOQUE #{numero_bloque} (BASE 2)")
            print(f"{'─'*70}")
            print(f"Valores codificados: {valores}")
        
        # Reconstruir el valor decimal
        bits_ventana = self.potencia.bit_length() - 1
        valor_reconstruido = 0
        
        if self.verbose:
            print(f"\nReconstrucción mediante desplazamientos:")
            print(f"  Ancho de ventana: {bits_ventana} bits")
        
        for idx, ventana in enumerate(valores):
            valor_reconstruido |= (ventana << (idx * bits_ventana))
            
            if self.verbose:
                print(f"  Posición {idx}: valor |= ({ventana} << {idx * bits_ventana})")
        
        # Convertir a binario
        if valor_reconstruido == 0:
            bloque_binario = '0' * self.bits_por_bloque
        else:
            bloque_binario = bin(valor_reconstruido)[2:].zfill(self.bits_por_bloque)
        
        if self.verbose:
            print(f"\nValor decimal reconstruido: {valor_reconstruido}")
            print(f"Bloque binario reconstruido ({len(bloque_binario)} bits):")
            print(f"  {bloque_binario}")
        
        return bloque_binario
    
    def decodificar_bloque_base5(self, residuos: List[int], numero_bloque: int) -> str:
        """
        Decodifica un bloque codificado en base 5.
        
        Args:
            residuos: Lista de residuos
            numero_bloque: Número de bloque para registro
        
        Returns:
            Cadena binaria reconstruida
        """
        if self.verbose:
            print(f"\n{'─'*70}")
            print(f"DECODIFICACIÓN BLOQUE #{numero_bloque} (BASE 5)")
            print(f"{'─'*70}")
            print(f"Residuos codificados: {residuos}")
        
        # Reconstruir el valor decimal
        valor_reconstruido = 0
        
        if self.verbose:
            print(f"\nReconstrucción desde residuos:")
        
        for idx, residuo in enumerate(residuos):
            contribucion = residuo * (self.potencia ** idx)
            valor_reconstruido += contribucion
            
            if self.verbose:
                print(f"  Posición {idx}: {residuo} × {self.potencia}^{idx} = {contribucion}")
        
        # Convertir a binario
        if valor_reconstruido == 0:
            bloque_binario = '0' * self.bits_por_bloque
        else:
            bloque_binario = bin(valor_reconstruido)[2:].zfill(self.bits_por_bloque)
        
        if self.verbose:
            print(f"\nValor decimal reconstruido: {valor_reconstruido}")
            print(f"Bloque binario reconstruido ({len(bloque_binario)} bits):")
            print(f"  {bloque_binario}")
        
        return bloque_binario
    
    def decodificar(self, datos_codificados: Dict[str, Any]) -> str:
        """
        Decodifica datos previamente codificados.
        
        Args:
            datos_codificados: Diccionario con datos codificados y metadatos
        
        Returns:
            Cadena binaria original reconstruida
        """
        inicio = time.time()
        
        # Validar que los parámetros coincidan
        if datos_codificados['base'] != self.base:
            raise ValueError("La base no coincide con la configuración del codificador")
        if datos_codificados['potencia'] != self.potencia:
            raise ValueError("La potencia no coincide con la configuración del codificador")
        if datos_codificados['bits_por_bloque'] != self.bits_por_bloque:
            raise ValueError("El tamaño de bloque no coincide con la configuración")
        
        if self.verbose:
            print(f"\n{'='*70}")
            print(f"INICIO DE DECODIFICACIÓN")
            print(f"{'='*70}")
            print(f"Número de bloques: {datos_codificados['num_bloques']}")
            print(f"Bits de padding a eliminar: {datos_codificados['bits_padding']}")
            print(f"{'='*70}")
        
        # Decodificar cada bloque
        bloques_decodificados = []
        
        for idx, valores in enumerate(datos_codificados['bloques_codificados'], 1):
            if self.base == 2:
                bloque = self.decodificar_bloque_base2(valores, idx)
            else:  # base == 5
                bloque = self.decodificar_bloque_base5(valores, idx)
            
            bloques_decodificados.append(bloque)
        
        # Unir todos los bloques
        datos_reconstruidos = ''.join(bloques_decodificados)
        
        # Eliminar padding del último bloque
        if datos_codificados['bits_padding'] > 0:
            datos_reconstruidos = datos_reconstruidos[:-datos_codificados['bits_padding']]
            
            if self.verbose:
                print(f"\n⚠️  ELIMINACIÓN DE PADDING:")
                print(f"   Se eliminaron {datos_codificados['bits_padding']} bits de padding")
        
        tiempo_decodificacion = time.time() - inicio
        
        if self.verbose:
            print(f"\n{'='*70}")
            print(f"DECODIFICACIÓN COMPLETADA")
            print(f"{'='*70}")
            print(f"Bits reconstruidos: {len(datos_reconstruidos)}")
            print(f"Tiempo de decodificación: {tiempo_decodificacion:.6f} segundos")
            print(f"{'='*70}\n")
        
        return datos_reconstruidos


class AnalizadorEficiencia:
    """
    Módulo para analizar la eficiencia y verificar la integridad
    del proceso de codificación/decodificación.
    """
    
    @staticmethod
    def calcular_sha256(datos_binarios: str) -> str:
        """
        Calcula el hash SHA-256 de una cadena binaria.
        
        Args:
            datos_binarios: Cadena de bits
        
        Returns:
            Hash SHA-256 en hexadecimal
        """
        # Convertir la cadena binaria a bytes
        # Asegurar que la longitud sea múltiplo de 8
        padding_bytes = (8 - len(datos_binarios) % 8) % 8
        datos_padded = datos_binarios + '0' * padding_bytes
        
        bytes_data = int(datos_padded, 2).to_bytes(len(datos_padded) // 8, byteorder='big')
        
        return hashlib.sha256(bytes_data).hexdigest()
    
    @staticmethod
    def verificar_integridad(original: str, decodificado: str) -> bool:
        """
        Verifica que los datos decodificados sean idénticos al original.
        
        Args:
            original: Cadena binaria original
            decodificado: Cadena binaria decodificada
        
        Returns:
            True si son idénticos, False en caso contrario
        """
        print(f"\n{'='*70}")
        print(f"VERIFICACIÓN DE INTEGRIDAD")
        print(f"{'='*70}")
        
        # Comparación bit a bit
        coinciden_bits = original == decodificado
        print(f"Comparación bit a bit: {'✓ COINCIDEN' if coinciden_bits else '✗ NO COINCIDEN'}")
        
        # Comparación de longitud
        print(f"Longitud original: {len(original)} bits")
        print(f"Longitud decodificada: {len(decodificado)} bits")
        
        # Comparación de hash
        hash_original = AnalizadorEficiencia.calcular_sha256(original)
        hash_decodificado = AnalizadorEficiencia.calcular_sha256(decodificado)
        
        print(f"\nSHA-256 Original:     {hash_original}")
        print(f"SHA-256 Decodificado: {hash_decodificado}")
        
        coinciden_hash = hash_original == hash_decodificado
        print(f"Hashes: {'✓ IDÉNTICOS' if coinciden_hash else '✗ DIFERENTES'}")
        
        # Resultado final
        integridad_ok = coinciden_bits and coinciden_hash
        
        if integridad_ok:
            print(f"\n{'✓'*35}")
            print(f"INTEGRIDAD VERIFICADA - REVERSIBILIDAD TOTAL")
            print(f"{'✓'*35}")
        else:
            print(f"\n{'✗'*35}")
            print(f"⚠️  FALLO CRÍTICO - PÉRDIDA DE INFORMACIÓN")
            print(f"{'✗'*35}")
        
        print(f"{'='*70}\n")
        
        return integridad_ok
    
    @staticmethod
    def calcular_metricas(datos_originales: str, datos_codificados: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calcula métricas de eficiencia del proceso.
        
        Args:
            datos_originales: Cadena binaria original
            datos_codificados: Diccionario con datos codificados
        
        Returns:
            Diccionario con métricas calculadas
        """
        print(f"\n{'='*70}")
        print(f"ANÁLISIS DE EFICIENCIA")
        print(f"{'='*70}")
        
        # Calcular tamaño codificado (suma de todos los valores)
        total_valores = sum(len(bloque) for bloque in datos_codificados['bloques_codificados'])
        bits_por_valor = max(max(v.bit_length() for v in bloque) 
                            for bloque in datos_codificados['bloques_codificados'] 
                            if bloque)
        
        bits_codificados = total_valores * bits_por_valor
        
        # Tasa de expansión
        tasa_expansion = bits_codificados / len(datos_originales)
        
        print(f"Bits originales: {len(datos_originales)}")
        print(f"Bits codificados (estimado): {bits_codificados}")
        print(f"Tasa de expansión: {tasa_expansion:.4f}")
        print(f"Tiempo de codificación: {datos_codificados['tiempo_codificacion']:.6f} seg")
        
        metricas = {
            'bits_originales': len(datos_originales),
            'bits_codificados': bits_codificados,
            'tasa_expansion': tasa_expansion,
            'tiempo_codificacion': datos_codificados['tiempo_codificacion'],
            'num_bloques': datos_codificados['num_bloques']
        }
        
        print(f"{'='*70}\n")
        
        return metricas


def bytes_a_binario(datos_bytes: bytes) -> str:
    """
    Convierte bytes a una cadena binaria.
    
    Args:
        datos_bytes: Datos en formato bytes
    
    Returns:
        Cadena de bits
    """
    return ''.join(format(byte, '08b') for byte in datos_bytes)


def binario_a_bytes(datos_binarios: str) -> bytes:
    """
    Convierte una cadena binaria a bytes.
    
    Args:
        datos_binarios: Cadena de bits
    
    Returns:
        Datos en formato bytes
    """
    # Asegurar que la longitud sea múltiplo de 8
    padding = (8 - len(datos_binarios) % 8) % 8
    datos_padded = datos_binarios + '0' * padding
    
    return int(datos_padded, 2).to_bytes(len(datos_padded) // 8, byteorder='big')


def demostrar_sistema():
    """
    Función de demostración que ejecuta un ejemplo completo del sistema.
    """
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  DEMOSTRACIÓN DEL CODIFICADOR/DECODIFICADOR UNIVERSAL".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70 + "\n")
    
    # Ejemplo con Base 5, Potencia 625, Bloques de 40 bits
    print("\n📌 CONFIGURACIÓN DEL EJEMPLO:")
    print("   Base: 5")
    print("   Potencia: 625 (5^4)")
    print("   Bloques: 40 bits\n")
    
    # Crear datos de prueba
    texto_prueba = "Hola, este es un sistema reversible!"
    datos_bytes = texto_prueba.encode('utf-8')
    datos_binarios = bytes_a_binario(datos_bytes)
    
    print(f"Texto original: '{texto_prueba}'")
    print(f"Longitud en bits: {len(datos_binarios)}")
    print(f"Primeros 80 bits: {datos_binarios[:80]}...\n")
    
    # Crear codificador
    codificador = CodificadorUniversal(
        base=5,
        potencia=625,
        bits_por_bloque=40,
        verbose=True
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
    
    # Calcular métricas
    metricas = AnalizadorEficiencia.calcular_metricas(
        datos_binarios,
        datos_codificados
    )
    
    # Reconstruir texto
    datos_reconstruidos_bytes = binario_a_bytes(datos_decodificados)
    texto_reconstruido = datos_reconstruidos_bytes[:len(datos_bytes)].decode('utf-8', errors='ignore')
    
    print(f"Texto reconstruido: '{texto_reconstruido}'")
    print(f"Texto coincide: {'✓ SÍ' if texto_prueba == texto_reconstruido else '✗ NO'}\n")
    
    return integridad_ok


if __name__ == "__main__":
    demostrar_sistema()
