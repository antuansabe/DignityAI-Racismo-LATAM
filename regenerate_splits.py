#!/usr/bin/env python3
"""
Regenera los splits (train/validation/test) después de mejorar el dataset
"""

import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

def crear_splits(df: pd.DataFrame, output_dir: Path):
    """
    Crea splits train/validation/test estratificados
    """
    print("=" * 80)
    print("✂️ CREANDO SPLITS (Train/Val/Test)")
    print("=" * 80)

    # Shuffle dataset
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    # 70% train, 30% temp
    train_df, temp_df = train_test_split(
        df,
        test_size=0.30,
        random_state=42,
        stratify=df[['pais', 'categoria']]
    )

    # 50% val, 50% test (del 30% temp)
    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.50,
        random_state=42,
        stratify=temp_df[['pais', 'categoria']]
    )

    print(f"\n📊 SPLITS CREADOS:")
    print(f"   Train: {len(train_df):,} ejemplos ({len(train_df)/len(df)*100:.1f}%)")
    print(f"   Validation: {len(val_df):,} ejemplos ({len(val_df)/len(df)*100:.1f}%)")
    print(f"   Test: {len(test_df):,} ejemplos ({len(test_df)/len(df)*100:.1f}%)")

    # Guardar splits
    train_df.to_csv(output_dir / "train.csv", index=False, encoding='utf-8')
    val_df.to_csv(output_dir / "validation.csv", index=False, encoding='utf-8')
    test_df.to_csv(output_dir / "test.csv", index=False, encoding='utf-8')

    print(f"\n✅ Splits guardados en: {output_dir}/")

    return train_df, val_df, test_df


def main():
    """
    Regenera los splits desde el dataset mejorado
    """
    print("🔄 Regenerando splits desde dataset mejorado...\n")

    # Cargar dataset mejorado
    dataset_path = Path("dignityai-racism-latam/dataset.csv")
    print(f"📁 Cargando dataset desde: {dataset_path}")
    df = pd.read_csv(dataset_path)
    print(f"✓ Dataset cargado: {len(df):,} ejemplos\n")

    # Crear splits
    output_dir = Path("dignityai-racism-latam")
    crear_splits(df, output_dir)

    print("\n" + "=" * 80)
    print("✅ SPLITS REGENERADOS EXITOSAMENTE")
    print("=" * 80)


if __name__ == "__main__":
    main()
