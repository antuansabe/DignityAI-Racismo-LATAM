# DignityAI-Racismo-LATAM

> Parte de [DignityAI](https://sin-odio.vercel.app/dignityai): recursos abiertos para detectar y estudiar discriminación en el español de América Latina.

**Advertencia de contenido.** Este dataset contiene lenguaje de discriminación racial explícito y sutil. Existe para entrenar y evaluar sistemas que **detectan** discriminación, nunca para generarla.

**Estado:** 🛑 datos sintéticos · 🛑 sin validación comunitaria · versión recomendada **1.1**

*English summary: synthetic, template-based Spanish dataset on racial discrimination across 5 countries, with contrastive non-discriminatory alternatives. Version 1.1 removes duplicates and near-duplicates and provides leakage-free splits. Best used for stress-testing and taxonomy work, not as the sole training source for a detector. License CC BY-NC-SA 4.0.*

## Qué contiene

Textos discriminatorios escritos a partir de plantillas combinatorias, cada uno etiquetado con país, categoría, subcategoría, nivel de sutileza y contexto (redes sociales, trabajo, apps de citas, etc.), más un conjunto de textos de contraste no discriminatorios.

- **Países:** México, Argentina, Colombia, Chile, Perú
- **Taxonomía:** 5 categorías, 21 subcategorías, niveles de sutileza: explícito, normalizado, sutil, sistémico

| Categoría | Subcategorías | Textos únicos |
|---|---|---:|
| `colorismo` | `blanqueamiento_aspiracional`, `denigracion_piel_oscura`, `jerarquia_racial_intragrupo`, `preferencia_piel_clara` | 6,050 |
| `microagresiones_raciales` | `comentarios_pelo_afro`, `exotizacion`, `negacion_racismo`, `sorpresa_competencia`, `tokenismo` | 3,499 |
| `racismo_anti_afrolatino` | `criminalizacion`, `estereotipos_afrodescendientes`, `hipersexualizacion`, `negacion_afrolatinidad` | 4,497 |
| `racismo_anti_indigena` | `desprecio_lenguas_originarias`, `estereotipos_indigenas`, `folclorizacion_deshumanizante`, `negacion_identidad_indigena` | 4,505 |
| `racismo_institucional` | `discriminacion_laboral`, `exclusion_espacial`, `perfilamiento_racial`, `violencia_simbolica_institucional` | 2,934 |

## Versiones

| Versión | Carpeta | Formato | Recomendación |
|---|---|---|---|
| **1.1** | [`v1.1/`](v1.1/) | Una fila por texto: `texto`, `etiqueta` (1 discriminatorio, 0 contraste), `tipo`, `pais`, `categoria`, `subcategoria`, `nivel_sutileza`, `contexto` | **Usar esta** |
| 1.0 | [`dignityai-racism-latam/`](dignityai-racism-latam/) | Pares (texto discriminatorio + alternativa) con metadatos extendidos | Solo para consultar los pares; **no uses sus splits** |

## Cifras medidas (noviembre 2026)

Calculadas con [`scripts/build_v1_1.py`](scripts/build_v1_1.py); el detalle está en [`v1.1/reporte_v1_1.json`](v1.1/reporte_v1_1.json).

| Medida | Valor |
|---|---:|
| Filas en v1.0 (pares) | 32,351 |
| Textos en formato largo | 64,702 |
| Tras quitar duplicados exactos | 26,535 |
| **Tras quitar casi-duplicados (v1.1)** | **22,769** |
| Discriminatorios / contraste | 21,485 / 1,284 |
| Train / validación / prueba | 15,938 / 3,415 / 3,416 |
| Fuga entre train y prueba (v1.1) | 0.0% |

Textos discriminatorios únicos por país:

| País | Textos |
|---|---:|
| México | 5,157 |
| Argentina | 4,305 |
| Colombia | 4,097 |
| Perú | 4,082 |
| Chile | 3,844 |

### Qué tan difícil es (baselines TF-IDF + regresión logística, F1 macro)

| Tarea | F1 |
|---|---:|
| Discriminatorio vs. contraste, partición v1.1 | 0.996 |
| Discriminatorio vs. contraste, **subcategorías no vistas** | **0.779** |
| Clasificar la categoría | 0.993 |

Que un modelo tan simple llegue a ~0.99 significa que los textos se distinguen por el estilo de la plantilla, no por comprensión. **La fila de subcategorías no vistas es la cifra honesta de generalización.**

## Limitaciones medidas

- **Es sintético.** Las plantillas no capturan la variedad del lenguaje real. El ruido (typos, abreviaturas, risas) se añadió con un script solo al lado discriminatorio, así que un modelo puede aprender que "escribir informal" = discriminación.
- **Los contrastes son pocos.** Solo 1,284 textos de contraste únicos frente a 21,485 discriminatorios (longitud mediana 55 vs. 43 caracteres).
- **La v1.0 tenía fuga.** Sus splits repetían en prueba casi el 100% de los textos de contraste de entrenamiento. Por eso existe la v1.1.
- **Sin validación comunitaria.** Ninguna organización ni comunidad afectada ha revisado los ejemplos todavía.

### Qué no cubre

- Racismo contra personas asiático-latinoamericanas, de origen árabe o judío.
- Caribe hispanohablante (Cuba, República Dominicana, Puerto Rico) y Centroamérica.
- Racismo codificado o de "silbato para perros" que depende de contexto.
- Intersecciones con discapacidad o diversidad sexual, salvo casos aislados.

## Cómo usarlo

```python
import pandas as pd

base = "https://raw.githubusercontent.com/antuansabe/DignityAI-Racismo-LATAM/main/v1.1"
train = pd.read_csv(f"{base}/train.csv")
test = pd.read_csv(f"{base}/test.csv")
print(train.groupby(["pais", "categoria"]).size())
```

**Usos recomendados:** pruebas de estrés de detectores y LLMs, estudio de la taxonomía, materiales de formación con advertencia de contenido, aumento de datos **junto con** corpus reales (ver el [directorio de datos reales](https://sin-odio.vercel.app/dignityai#directorio)).

**No lo uses para:** generar contenido discriminatorio, entrenar un detector solo con estos datos, tomar decisiones automáticas sobre personas o fines comerciales sin autorización.
- Guía de uso responsable: [`GUIA_USO_RESPONSABLE.md`](dignityai-racism-latam/GUIA_USO_RESPONSABLE.md)
- Contexto histórico: [`CONTEXTO_HISTORICO.md`](dignityai-racism-latam/CONTEXTO_HISTORICO.md)

## Licencia

[CC BY-NC-SA 4.0](LICENSE). Uso libre para investigación, educación, organizaciones civiles y periodismo. Para uso comercial, escribe a antuansabe@gmail.com.

## Cómo citar

Usa el archivo [`CITATION.cff`](CITATION.cff) (GitHub muestra el botón "Cite this repository") o:

```bibtex
@misc{dromundo2025racismo,
  author = {Dromundo, Antonio},
  title  = {DignityAI-Racismo-LATAM: dataset sintético de discriminación racial en español},
  year   = {2025},
  note   = {Versión 1.1 (2026)},
  url    = {https://github.com/antuansabe/DignityAI-Racismo-LATAM}
}
```

## Contacto y contribuciones

- Errores, sesgos o ejemplos que deban retirarse: abre un [issue](https://github.com/antuansabe/DignityAI-Racismo-LATAM/issues) o escribe a antuansabe@gmail.com.
- Si eres parte de una comunidad afectada, tu revisión tiene prioridad sobre cualquier métrica.

Proyecto independiente de Antonio Dromundo ([GitHub](https://github.com/antuansabe), [Hugging Face](https://huggingface.co/antonn-dromundo)). No está afiliado a ninguna organización mencionada en este repositorio.
