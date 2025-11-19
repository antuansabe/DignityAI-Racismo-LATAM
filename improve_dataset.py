#!/usr/bin/env python3
"""
DignityAI-Racism-LATAM Dataset Improver

Agrega ruido natural a los textos sintéticos para hacerlos más realistas
y similares a contenido real de internet.

Author: Antonio Dromundo
Date: 2025
License: CC BY-NC-SA 4.0
"""

import random
import pandas as pd
from pathlib import Path
import re

# ============================================================================
# FUNCIONES DE RUIDO NATURAL
# ============================================================================

def introduce_typos(text: str) -> str:
    """
    Introduce errores ortográficos comunes y typos realistas
    """
    # Errores comunes en español latino
    typos = {
        'h': '',  # Omitir h (común: "acer" por "hacer")
        'v': 'b', # Confusión v/b
        'b': 'v',
        's': 'z', # Seseo
        'z': 's',
        'c': 's', # Seseo con c
        'll': 'y', # Yeísmo
        'y': 'll',
    }

    # Palabras comunes con errores típicos
    common_errors = {
        'había': 'habia',
        'hacía': 'hacia',
        'más': 'mas',
        'sí': 'si',
        'tú': 'tu',
        'él': 'el',
        'está': 'esta',
        'qué': 'que',
        'cómo': 'como',
        'dónde': 'donde',
    }

    # Aplicar errores de acentos (muy común en internet)
    for correct, wrong in common_errors.items():
        if random.random() < 0.3 and correct in text:
            text = text.replace(correct, wrong)

    # Aplicar typos aleatorios (5% de las letras)
    words = text.split()
    modified_words = []

    for word in words:
        if random.random() < 0.15:  # 15% de probabilidad por palabra
            # Seleccionar un tipo de error
            error_type = random.choice(['substitution', 'omission', 'duplication'])

            if error_type == 'substitution' and len(word) > 2:
                # Sustituir una letra
                pos = random.randint(0, len(word) - 1)
                letter = word[pos].lower()
                if letter in typos:
                    replacement = typos[letter]
                    word = word[:pos] + replacement + word[pos+1:]

            elif error_type == 'omission' and len(word) > 3:
                # Omitir una letra (común con h, u)
                if 'h' in word.lower():
                    word = word.replace('h', '').replace('H', '')
                elif random.random() < 0.5:
                    pos = random.randint(1, len(word) - 2)
                    word = word[:pos] + word[pos+1:]

            elif error_type == 'duplication' and len(word) > 2:
                # Duplicar una letra (typo común)
                pos = random.randint(0, len(word) - 1)
                word = word[:pos] + word[pos] + word[pos:]

        modified_words.append(word)

    return ' '.join(modified_words)


def randomize_capitalization(text: str) -> str:
    """
    Mezcla mayúsculas y minúsculas de forma caótica (estilo internet)
    """
    styles = [
        'all_caps',      # TODO EN MAYÚSCULAS
        'no_caps',       # todo en minúsculas
        'random_caps',   # MeZcLaDo AlEaToRiO
        'first_only'     # Solo primera mayúscula
    ]

    style = random.choice(styles)

    if style == 'all_caps':
        return text.upper()
    elif style == 'no_caps':
        return text.lower()
    elif style == 'random_caps':
        # Mezclar mayúsculas/minúsculas aleatoriamente
        return ''.join(c.upper() if random.random() > 0.5 else c.lower() for c in text)
    else:  # first_only
        return text[0].upper() + text[1:].lower() if text else text


def add_natural_noise(text: str) -> str:
    """
    Agrega ruido realista a texto sintético para hacerlo más natural

    Transformaciones aplicadas:
    - Typos/errores ortográficos (30% probabilidad)
    - Abreviaciones de internet (aplicadas selectivamente)
    - Eliminación de puntuación formal (40% probabilidad)
    - Mayúsculas caóticas (15% probabilidad)
    - Emojis/expresiones (10% probabilidad)
    """

    # 1. Typos/errores ortográficos (30% probabilidad)
    if random.random() < 0.3:
        text = introduce_typos(text)

    # 2. Abreviaciones de internet (aplicadas a palabras específicas)
    internet_abbrevs = {
        'porque': ['xq', 'pq', 'xk', 'pk'],
        'que': ['q', 'ke', 'k'],
        'para': ['pa', 'pr'],
        'por qué': ['xq', 'x q', 'pq'],
        'también': ['tb', 'tmb', 'tambien'],
        'estoy': ['toy', 'stoy'],
        'estar': ['sta', 'star'],
        'ahora': ['aora', 'ora'],
        'verdad': ['vdd', 'vrdd'],
        'todo': ['td', 'todo'],
        'nada': ['nd', 'nada'],
        'mucho': ['muxo', 'mcho'],
        'gracias': ['grax', 'grcs'],
    }

    for word, abbrevs in internet_abbrevs.items():
        if word in text.lower() and random.random() < 0.25:
            # Preservar mayúsculas si las había
            if word in text:
                replacement = random.choice(abbrevs + [word])
                text = text.replace(word, replacement)
            elif word.capitalize() in text:
                replacement = random.choice(abbrevs + [word]).capitalize()
                text = text.replace(word.capitalize(), replacement)

    # 3. Eliminar/modificar puntuación formal (40% probabilidad)
    if random.random() < 0.4:
        # Eliminar puntos finales
        text = text.rstrip('.')

        # A veces también eliminar comas (menos frecuente)
        if random.random() < 0.3:
            text = text.replace(',', '')

    # 4. Mayúsculas caóticas (15% probabilidad)
    if random.random() < 0.15:
        text = randomize_capitalization(text)

    # 5. Emojis/expresiones contextualmente apropiadas (10% probabilidad)
    if random.random() < 0.1:
        endings = [
            ' jaja', ' jajaja', ' jeje', ' lol',
            ' 😂', ' 🤣', ' 🤷‍♂️', ' 🙄', ' 😏',
            ' jajaj', ' xD', ' XD', ' :v'
        ]
        text += random.choice(endings)

    # 6. Espacios inconsistentes (5% probabilidad)
    if random.random() < 0.05:
        # Agregar/eliminar espacios aleatoriamente
        if random.random() < 0.5:
            # Eliminar espacio después de coma
            text = text.replace(', ', ',')
        else:
            # Agregar espacios extras
            text = re.sub(r'([.,!?])', r'\1 ', text)

    # 7. Repetición de letras para énfasis (8% probabilidad)
    if random.random() < 0.08:
        words = text.split()
        if words:
            # Seleccionar una palabra al azar para enfatizar
            idx = random.randint(0, len(words) - 1)
            word = words[idx]
            if len(word) > 2:
                # Repetir la última vocal o consonante
                for i in range(len(word) - 1, -1, -1):
                    if word[i].lower() in 'aeiou':
                        # Extender vocal: "nooo", "siiii"
                        words[idx] = word[:i+1] + word[i] * random.randint(1, 3) + word[i+1:]
                        break
        text = ' '.join(words)

    return text


# ============================================================================
# APLICACIÓN AL DATASET
# ============================================================================

def improve_dataset(input_file: str = "dignityai-racism-latam/dataset.csv",
                   output_file: str = "dignityai-racism-latam/dataset_improved.csv",
                   apply_to_column: str = "texto_racista",
                   noise_probability: float = 0.7) -> pd.DataFrame:
    """
    Carga el dataset y aplica ruido natural a la columna especificada

    Args:
        input_file: Ruta al archivo CSV de entrada
        output_file: Ruta al archivo CSV de salida
        apply_to_column: Columna a la que aplicar el ruido
        noise_probability: Probabilidad de aplicar ruido a cada fila (0.7 = 70%)

    Returns:
        DataFrame mejorado
    """
    print("=" * 80)
    print("🔧 MEJORANDO DIGNITYAI-RACISM-LATAM DATASET")
    print("=" * 80)
    print(f"\n📁 Cargando dataset desde: {input_file}")

    # Cargar dataset
    df = pd.read_csv(input_file)
    total_rows = len(df)
    print(f"✓ Dataset cargado: {total_rows:,} ejemplos")

    # Crear nueva columna con ruido aplicado
    print(f"\n🎲 Aplicando ruido natural a columna '{apply_to_column}'...")
    print(f"   Probabilidad de ruido: {noise_probability:.0%}")

    # Aplicar ruido
    noisy_texts = []
    rows_modified = 0

    for idx, text in enumerate(df[apply_to_column]):
        if random.random() < noise_probability:
            noisy_text = add_natural_noise(str(text))
            noisy_texts.append(noisy_text)
            rows_modified += 1
        else:
            noisy_texts.append(text)

        # Mostrar progreso cada 5000 filas
        if (idx + 1) % 5000 == 0:
            print(f"   Procesadas {idx + 1:,}/{total_rows:,} filas...")

    # Crear nueva columna o reemplazar la existente
    new_column_name = f"{apply_to_column}_mejorado"
    df[new_column_name] = noisy_texts

    print(f"\n✓ Ruido aplicado a {rows_modified:,}/{total_rows:,} filas ({rows_modified/total_rows:.1%})")

    # Guardar dataset mejorado
    print(f"\n💾 Guardando dataset mejorado en: {output_file}")
    df.to_csv(output_file, index=False)
    print("✓ Dataset guardado exitosamente")

    # Mostrar ejemplos
    print("\n" + "=" * 80)
    print("📊 EJEMPLOS DE TRANSFORMACIONES")
    print("=" * 80)

    sample_indices = random.sample(range(len(df)), min(5, len(df)))
    for idx in sample_indices:
        original = df.loc[idx, apply_to_column]
        improved = df.loc[idx, new_column_name]

        if original != improved:
            print(f"\n🔹 Ejemplo {idx + 1}:")
            print(f"   ORIGINAL:  {original}")
            print(f"   MEJORADO:  {improved}")

    print("\n" + "=" * 80)
    print("✅ PROCESO COMPLETADO")
    print("=" * 80)

    return df


# ============================================================================
# FUNCIÓN PARA REEMPLAZAR COLUMNA ORIGINAL
# ============================================================================

def replace_original_column(input_file: str = "dignityai-racism-latam/dataset_improved.csv",
                           output_file: str = "dignityai-racism-latam/dataset.csv",
                           improved_column: str = "texto_racista_mejorado",
                           original_column: str = "texto_racista"):
    """
    Reemplaza la columna original con la versión mejorada y elimina la columna temporal
    """
    print(f"\n🔄 Reemplazando columna '{original_column}' con '{improved_column}'...")

    df = pd.read_csv(input_file)

    # Reemplazar columna original
    df[original_column] = df[improved_column]

    # Eliminar columna mejorada temporal
    df = df.drop(columns=[improved_column])

    # Guardar
    df.to_csv(output_file, index=False)
    print(f"✓ Columna reemplazada y guardada en: {output_file}")

    return df


# ============================================================================
# MAIN
# ============================================================================

def main():
    """
    Función principal para mejorar el dataset
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Mejora el dataset DignityAI-Racism-LATAM agregando ruido natural"
    )
    parser.add_argument(
        "--input", "-i",
        default="dignityai-racism-latam/dataset.csv",
        help="Archivo CSV de entrada"
    )
    parser.add_argument(
        "--output", "-o",
        default="dignityai-racism-latam/dataset_improved.csv",
        help="Archivo CSV de salida"
    )
    parser.add_argument(
        "--column", "-c",
        default="texto_racista",
        help="Columna a la que aplicar ruido"
    )
    parser.add_argument(
        "--probability", "-p",
        type=float,
        default=0.7,
        help="Probabilidad de aplicar ruido (0.0-1.0)"
    )
    parser.add_argument(
        "--replace", "-r",
        action="store_true",
        help="Reemplazar columna original en lugar de crear una nueva"
    )

    args = parser.parse_args()

    # Aplicar mejoras
    df = improve_dataset(
        input_file=args.input,
        output_file=args.output,
        apply_to_column=args.column,
        noise_probability=args.probability
    )

    # Si se especificó --replace, reemplazar la columna original
    if args.replace:
        replace_original_column(
            input_file=args.output,
            output_file=args.input,
            improved_column=f"{args.column}_mejorado",
            original_column=args.column
        )
        print(f"\n✓ Columna '{args.column}' reemplazada exitosamente")


if __name__ == "__main__":
    main()
