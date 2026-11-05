"""
DignityAI — construcción de la versión 1.1 de un dataset contrastivo (Racismo / Clasismo).

Qué hace:
  1. Lee el dataset v1.0 (formato par: texto discriminatorio + texto de contraste).
  2. Lo convierte a formato largo (una fila por texto, con etiqueta binaria).
  3. Elimina duplicados exactos y casi-duplicados (mismo "esqueleto" tras quitar
     el ruido sintético: mayúsculas, acentos, typos de letras repetidas, abreviaturas,
     risas/emojis añadidos, puntuación).
  4. Genera splits train/validation/test AGRUPADOS por esqueleto, para que una misma
     plantilla nunca aparezca en dos splits (la v1.0 tenía ~100% de fuga en contraste).
  5. Mide baselines TF-IDF + regresión logística y escribe un reporte JSON.

Uso:
  python build_v1_1.py <carpeta_v1.0> <col_discriminatoria> <col_contraste> <carpeta_salida>
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import GroupShuffleSplit

SEED = 42
ABBREV = {
    "xq": "porque", "pq": "porque", "xk": "porque", "pk": "porque", "q": "que", "ke": "que",
    "k": "que", "pa": "para", "pr": "para", "tb": "tambien", "tmb": "tambien", "toy": "estoy",
    "stoy": "estoy", "sta": "estar", "star": "estar", "aora": "ahora", "ora": "ahora",
    "vdd": "verdad", "vrdd": "verdad", "td": "todo", "nd": "nada", "muxo": "mucho",
    "mcho": "mucho", "grax": "gracias", "grcs": "gracias",
}
LAUGHS = {"jaja", "jajaja", "jeje", "lol", "jajaj", "xd", "v"}


def skeleton(text: str) -> str:
    t = unicodedata.normalize("NFKD", str(text).lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"[^a-zñ0-9 ]+", " ", t)
    t = re.sub(r"(.)\1{1,}", r"\1", t)  # nooo -> no, paraa -> para
    words = [ABBREV.get(w, w) for w in t.split()]
    words = [w for w in words if w not in LAUGHS]
    return " ".join(words)


def main(src: str, pos: str, neg: str, out: str) -> None:
    src_p, out_p = Path(src), Path(out)
    out_p.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(src_p / "dataset.csv")
    meta_cols = [c for c in ["pais", "categoria", "subcategoria", "nivel_sutileza", "contexto"] if c in df]

    d = df[meta_cols + [pos]].rename(columns={pos: "texto"}).assign(etiqueta=1, tipo="discriminatorio")
    c = df[meta_cols + [neg]].rename(columns={neg: "texto"}).assign(etiqueta=0, tipo="contraste")
    long = pd.concat([d, c], ignore_index=True)
    long["texto"] = long["texto"].astype(str).str.strip()
    long["esqueleto"] = long["texto"].map(skeleton)

    n_long = len(long)
    exact = long.drop_duplicates(["texto", "etiqueta"])
    clean = exact.drop_duplicates(["esqueleto", "etiqueta"]).reset_index(drop=True)
    # Un mismo esqueleto con ambas etiquetas sería contradictorio: se descarta.
    conflict = clean.groupby("esqueleto")["etiqueta"].nunique()
    conflict_keys = set(conflict[conflict > 1].index)
    clean = clean[~clean["esqueleto"].isin(conflict_keys)].reset_index(drop=True)

    # Splits agrupados por esqueleto (70/15/15).
    g1 = GroupShuffleSplit(n_splits=1, test_size=0.30, random_state=SEED)
    tr_idx, rest_idx = next(g1.split(clean, groups=clean["esqueleto"]))
    rest = clean.iloc[rest_idx]
    g2 = GroupShuffleSplit(n_splits=1, test_size=0.50, random_state=SEED)
    va_rel, te_rel = next(g2.split(rest, groups=rest["esqueleto"]))
    splits = {
        "train": clean.iloc[tr_idx],
        "validation": rest.iloc[va_rel],
        "test": rest.iloc[te_rel],
    }
    cols = ["texto", "etiqueta", "tipo"] + meta_cols
    for name, part in splits.items():
        part[cols].to_csv(out_p / f"{name}.csv", index=False)
    clean[cols].to_parquet(out_p / "completo.parquet", index=False)

    tr, te = splits["train"], splits["test"]
    leak = te["esqueleto"].isin(set(tr["esqueleto"])).mean()

    # Baseline 1: binario discriminatorio vs contraste (split nuevo).
    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)
    Xtr, Xte = vec.fit_transform(tr["texto"]), vec.transform(te["texto"])
    clf = LogisticRegression(max_iter=2000, class_weight="balanced").fit(Xtr, tr["etiqueta"])
    f1_bin = f1_score(te["etiqueta"], clf.predict(Xte), average="macro")

    # Baseline 2: binario con split por SUBCATEGORÍA (prueba de generalización fuera de plantilla).
    gs = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=SEED)
    a, b = next(gs.split(clean, groups=clean["subcategoria"]))
    v2 = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)
    m2 = LogisticRegression(max_iter=2000, class_weight="balanced").fit(
        v2.fit_transform(clean.iloc[a]["texto"]), clean.iloc[a]["etiqueta"])
    f1_ood = f1_score(clean.iloc[b]["etiqueta"], m2.predict(v2.transform(clean.iloc[b]["texto"])), average="macro")

    # Baseline 3: categoría de discriminación (solo textos discriminatorios).
    trd, ted = tr[tr.etiqueta == 1], te[te.etiqueta == 1]
    v3 = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)
    m3 = LogisticRegression(max_iter=3000).fit(v3.fit_transform(trd["texto"]), trd["categoria"])
    f1_cat = f1_score(ted["categoria"], m3.predict(v3.transform(ted["texto"])), average="macro")

    report = {
        "version": "1.1.0",
        "fuente": str(src_p),
        "filas_v1_0_pares": int(len(df)),
        "textos_formato_largo": int(n_long),
        "tras_quitar_duplicados_exactos": int(len(exact)),
        "tras_quitar_casi_duplicados": int(len(clean)),
        "esqueletos_con_etiqueta_contradictoria_descartados": int(len(conflict_keys)),
        "por_etiqueta": {"discriminatorio": int((clean.etiqueta == 1).sum()), "contraste": int((clean.etiqueta == 0).sum())},
        "splits": {k: int(len(v)) for k, v in splits.items()},
        "fuga_test_train_esqueleto_pct": round(100 * float(leak), 2),
        "por_pais_discriminatorio": clean[clean.etiqueta == 1]["pais"].value_counts().to_dict(),
        "por_categoria_discriminatorio": clean[clean.etiqueta == 1]["categoria"].value_counts().to_dict(),
        "baselines_tfidf_logreg_macro_f1": {
            "binario_split_v1_1": round(float(f1_bin), 3),
            "binario_subcategorias_no_vistas": round(float(f1_ood), 3),
            "categoria_5_6_clases": round(float(f1_cat), 3),
        },
        "longitud_mediana_caracteres": {
            "discriminatorio": int(clean[clean.etiqueta == 1]["texto"].str.len().median()),
            "contraste": int(clean[clean.etiqueta == 0]["texto"].str.len().median()),
        },
    }
    (out_p / "reporte_v1_1.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main(*sys.argv[1:5])
