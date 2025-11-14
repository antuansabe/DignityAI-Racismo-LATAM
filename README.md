# DignityAI-Racism-LATAM

<div align="center">

![DignityAI](https://img.shields.io/badge/DignityAI-Racism%20Detection-red)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-green)
![Language](https://img.shields.io/badge/language-Spanish%20(LATAM)-yellow)
![Samples](https://img.shields.io/badge/samples-32%2C351-orange)

**Protecting Human Dignity Through AI**

</div>

---

## ⚠️ CONTENT WARNING | ADVERTENCIA DE CONTENIDO

**🔴 THIS DATASET CONTAINS HIGHLY SENSITIVE RACIAL CONTENT**

This dataset documents **explicit racist language and discrimination** found in Latin American Spanish-speaking communities. It is designed **EXCLUSIVELY for:**

- ✅ Academic research on racism
- ✅ Training AI models to **DETECT** (not generate) racist content
- ✅ Educational purposes in controlled environments
- ✅ Development of content moderation tools

**❌ This dataset should NEVER be used to:**
- Generate racist content
- Train models without ethical oversight
- Display examples without educational context
- Commercial applications without community consultation

**By accessing this dataset, you acknowledge:**
1. The severe ethical responsibility involved
2. The potential to cause harm if misused
3. The commitment to responsible usage
4. The need for content warnings when presenting findings

---

## 📚 About DignityAI

**DignityAI** is an open-source initiative dedicated to protecting human dignity through AI, with a focus on detecting and preventing discrimination in Spanish-speaking communities.

### The DignityAI Family

This dataset is part of a comprehensive suite addressing different forms of discrimination in Latin America:

| Dataset | Focus | Size | Status |
|---------|-------|------|--------|
| [SinOdio-LATAM](https://huggingface.co/datasets/Nohyc/SinOdio-LATAM) | General hate speech | 20,000 | ✅ Published |
| [DignityAI-Machismo-LATAM](https://huggingface.co/datasets/Nohyc/DignityAI-Machismo-LATAM) | Machismo & sexism | 18,000 | ✅ Published |
| [DignityAI-Clasismo-LATAM](https://huggingface.co/datasets/Nohyc/DignityAI-Clasismo-LATAM) | Classism | 30,000 | ✅ Published |
| **DignityAI-Racism-LATAM** | **Racial discrimination** | **32,351** | **🆕 This dataset** |

---

## 🎯 Dataset Overview

### What makes this dataset unique?

**DignityAI-Racism-LATAM** is the first comprehensive dataset of racial discrimination in Latin American Spanish, with special emphasis on:

1. **Colorism** - The dominant form of racism in LATAM (preference for lighter skin)
2. **Anti-Indigenous racism** - Against 60M+ indigenous peoples
3. **Anti-Afro-Latino racism** - Against 150M+ Afro-descendants
4. **Racial microaggressions** - Normalized everyday racism
5. **Institutional racism** - Structural discrimination

### Key Statistics

- **32,351 unique examples** (after deduplication)
- **5 countries**: Mexico, Argentina, Colombia, Chile, Peru
- **5 major categories** of racial discrimination
- **18 detailed subcategories**
- **Contrastive pairs**: Each racist text paired with anti-racist counterpart
- **Rich metadata**: Intersectionality, historical context, sensitivity levels
- **Regional authenticity**: Country-specific slang and expressions

### Dataset Structure

```
dignityai-racism-latam/
├── dataset.csv           # Full dataset (11 MB)
├── dataset.json          # JSON format (22 MB)
├── dataset.parquet       # Efficient format (1.3 MB)
├── train.csv             # 70% (22,645 samples)
├── validation.csv        # 15% (4,853 samples)
├── test.csv              # 15% (4,853 samples)
└── metadata.json         # Dataset metadata
```

---

## 📊 Category Distribution

| Category | % | Examples | Description |
|----------|---|----------|-------------|
| **Colorism** | 25% | 8,088 | Discrimination by skin tone - dominant form in LATAM |
| **Anti-Indigenous** | 20% | 6,470 | Against indigenous peoples (60M+ in LATAM) |
| **Anti-Afro-Latino** | 20% | 6,470 | Against Afro-descendants (150M+ in LATAM) |
| **Microaggressions** | 20% | 6,470 | Normalized everyday racial discrimination |
| **Institutional** | 15% | 4,853 | Structural and systematic racism |

### Subcategories (18 total)

<details>
<summary><strong>Colorism (4 subcategories)</strong></summary>

1. **Preference for light skin** - Privilege of whiteness
2. **Denigration of dark skin** - Insults based on darker skin
3. **Intra-group racial hierarchy** - Colorism within racialized communities
4. **Aspirational whitening** - Desire to "whiten" descendants

</details>

<details>
<summary><strong>Anti-Indigenous Racism (4 subcategories)</strong></summary>

1. **Indigenous stereotypes** - Dehumanizing stereotypes
2. **Denial of indigenous identity** - Forced assimilation
3. **Disdain for original languages** - Linguistic racism
4. **Dehumanizing folklorization** - Reducing culture to folklore

</details>

<details>
<summary><strong>Anti-Afro-Latino Racism (4 subcategories)</strong></summary>

1. **Afro-descendant stereotypes** - Harmful racial stereotypes
2. **Hypersexualization** - Sexual objectification
3. **Criminalization** - Automatic association with crime
4. **Denial of Afro-Latinidad** - Invisibilization of Afro-descendants

</details>

<details>
<summary><strong>Racial Microaggressions (5 subcategories)</strong></summary>

1. **Afro hair comments** - Invasive comments about textured hair
2. **Surprise at competence** - Shock when racialized people are competent
3. **Exoticization** - Treating as exotic/different
4. **Denial of racism** - Gaslighting racial experiences
5. **Tokenism** - Using as diversity quotas

</details>

<details>
<summary><strong>Institutional Racism (4 subcategories)</strong></summary>

1. **Spatial exclusion** - De facto segregation
2. **Labor discrimination** - Hiring/promotion discrimination
3. **Racial profiling** - By police and security
4. **Institutional symbolic violence** - Systemic erasure

</details>

---

## 💾 Data Fields

Each example contains:

| Field | Type | Description |
|-------|------|-------------|
| `pais` | string | Country (México, Argentina, Colombia, Chile, Perú) |
| `categoria` | string | Main category (5 types) |
| `subcategoria` | string | Specific subcategory (18 types) |
| `texto_racista` | string | **Racist text** (explicit content) |
| `texto_antirracista` | string | Anti-racist counterpart |
| `contexto` | string | Context where racism occurs |
| `nivel_sutileza` | string | Subtlety level (explícito, sutil, normalizado, sistémico) |
| `grupos_afectados` | list | Affected racialized groups |
| `mecanismo_discriminacion` | string | Discrimination mechanism |
| `interseccionalidad` | list | Intersectionality (race + class/gender) |
| `jerga_regional` | bool | Contains regional slang |
| `sensibilidad` | string | Sensitivity level (all are "alta" = high) |
| `dimension_historica` | string | Historical context (colonialism, slavery, etc.) |
| `generado_en` | string | Generation timestamp |
| `id` | string | Unique identifier |

---

## 🔍 Example (Sanitized)

⚠️ **Content Warning**: This example contains racist language for educational purposes.

```json
{
  "pais": "México",
  "categoria": "colorismo",
  "subcategoria": "preferencia_piel_clara",
  "texto_racista": "Busco empleado de piel clara para atención al cliente",
  "texto_antirracista": "Busco persona capacitada para el trabajo, sin importar su color de piel",
  "contexto": "conversacion_laboral",
  "nivel_sutileza": "normalizado",
  "grupos_afectados": ["personas_piel_oscura", "afrodescendientes"],
  "mecanismo_discriminacion": "privilegio_blanquitud",
  "interseccionalidad": ["raza", "clase"],
  "dimension_historica": "colorismo_colonial"
}
```

---

## 🛠️ Methodology

### Generation Process

This dataset was created using a **template-based combinatorial approach** to ensure:

✅ **High variability** - 32,351 unique combinations
✅ **Perfect balance** - Stratified distribution across countries and categories
✅ **Regional authenticity** - Country-specific slang validated culturally
✅ **Ethical safeguards** - Contrastive pairs, rich metadata, sensitivity markers

### Formula

```
Templates × Regional Variables × Contexts × Countries × Deduplication = 32,351 unique examples
```

### Quality Assurance

- ✅ Manual review of 500+ random samples
- ✅ Deduplication (removed ~7% duplicates)
- ✅ Balance validation (CV < 0.17 across categories)
- ✅ Regional slang validation

### ⚠️ Validation Required Before Publication

As stated in the dataset generation process, this dataset **REQUIRES**:

1. ✅ Review by academics specializing in racial studies
2. ✅ Consultation with Afro-descendant organizations
3. ✅ Consultation with indigenous organizations
4. ✅ Regional validation per country
5. ✅ IRB/Ethics approval (if in institution)
6. ✅ Community feedback integration

---

## 📖 Usage Examples

### Loading the Dataset

```python
from datasets import load_dataset

# Load full dataset
dataset = load_dataset("path/to/dignityai-racism-latam")

# Load specific split
train_data = load_dataset("path/to/dignityai-racism-latam", split="train")
```

### Training a Classifier

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Example: Binary classifier for racist content detection
model_name = "dccuchile/bert-base-spanish-wwm-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Create labels: 1 = racist, 0 = anti-racist
# IMPORTANT: Only use to DETECT racism, never to GENERATE it
```

### Analyzing by Country

```python
import pandas as pd

df = pd.read_csv("dataset.csv")

# Distribution by country
print(df['pais'].value_counts())

# Filter by specific type of racism
colorism_mx = df[(df['categoria'] == 'colorismo') & (df['pais'] == 'México')]
```

---

## ⚖️ Ethical Considerations

### Historical Context

Racism in Latin America has unique characteristics:

1. **Colorism vs. Binary Racism**: Unlike the US black/white binary, LATAM has a spectrum of skin tones with discrimination intensity varying accordingly
2. **Colonial Legacy**: Caste systems from 1500s-1800s created 16+ racial categories
3. **Indigenous Genocide**: 90% of indigenous population eliminated 1492-1600
4. **Afro-Latino Enslavement**: 4M+ Africans enslaved; Brazil was last to abolish (1888)
5. **Whitening Policies**: 1800s-1900s governments incentivized European immigration to "mejorate la raza" (improve the race)
6. **Myth of Racial Democracy**: "We're all mestizos" narrative masks deep inequalities

### Why This Matters

- **Income Gap**: Light-skinned people earn 20-30% more
- **Media Representation**: 90% of TV shows only light-skinned people
- **Incarceration**: Afro-descendants 3x more likely to be imprisoned
- **Indigenous Rights**: Ongoing land theft and cultural genocide
- **Political Power**: Near-zero representation in leadership

### Potential Harms

**This dataset can cause harm if:**

❌ Used to generate racist content
❌ Deployed without bias auditing
❌ Presented without content warnings
❌ Used for commercial gain without community benefit
❌ Applied outside intended detection use case

### Recommended Safeguards

✅ **Content warnings** on all materials
✅ **Bias audits** for models trained on this data
✅ **Fairness metrics** disaggregated by affected groups
✅ **Adversarial testing** for potential misuse
✅ **Community consultation** before deployment
✅ **Transparency** about limitations

---

## 🚧 Limitations

### What this dataset does NOT cover

- ❌ Racism against Asian Latin Americans
- ❌ Racism against Middle Eastern Latin Americans
- ❌ Anti-Semitism
- ❌ Racism in Brazil (Portuguese, not Spanish)
- ❌ Caribbean Spanish (Dominican Republic, Cuba, Puerto Rico)
- ❌ Central American countries
- ❌ Coded racism (dog whistles, subtle references)

### Known Biases

1. **Generation Method**: Template-based, may miss rare phrasings
2. **Regional Coverage**: Only 5 countries of 20+ in LATAM
3. **Historical Moment**: Reflects 2025 language patterns
4. **Class Bias**: May under-represent upper-class coded racism
5. **Intersectionality**: Limited coverage of race + disability, race + LGBTQ+

### Quality Issues

- Some templates may have grammatical variations
- Regional slang may not cover all dialects
- Contrastive pairs may not be perfectly balanced in tone

---

## 📜 License

**CC BY-NC-SA 4.0** (Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International)

**You are free to:**
- ✅ Share - copy and redistribute
- ✅ Adapt - remix, transform, build upon

**Under the following terms:**
- **Attribution** - Give appropriate credit
- **NonCommercial** - Not for commercial purposes without permission
- **ShareAlike** - Distribute contributions under same license

**Special Conditions:**
- ⚠️  Commercial use requires community consultation
- ⚠️  Must maintain content warnings
- ⚠️  Must cite this dataset properly

---

## 📚 Citation

If you use this dataset in your research, please cite:

```bibtex
@dataset{dignityai_racism_latam_2025,
  title = {DignityAI-Racism-LATAM: A Dataset of Racial Discrimination in Latin American Spanish},
  author = {Dromundo, Antonio},
  year = {2025},
  publisher = {HuggingFace},
  version = {1.0.0},
  url = {https://huggingface.co/datasets/Nohyc/DignityAI-Racism-LATAM},
  note = {Part of the DignityAI initiative}
}
```

**APA Format:**
```
Dromundo, A. (2025). DignityAI-Racism-LATAM: A Dataset of Racial Discrimination in
Latin American Spanish (Version 1.0.0) [Data set]. HuggingFace.
https://huggingface.co/datasets/Nohyc/DignityAI-Racism-LATAM
```

---

## 👥 Contact & Contribution

### Author

**Antonio Dromundo**
- LinkedIn: [linkedin.com/in/antonio-dromundo](https://linkedin.com/in/antonio-dromundo)
- Twitter: [@antonnDromundo](https://twitter.com/antonnDromundo)
- GitHub: [github.com/antonnDromundo](https://github.com/antonnDromundo)
- Email: antuansabe@gmail.com

### How to Contribute

We welcome contributions from researchers, activists, and community members:

1. 🐛 **Report Issues**: Found errors or bias? Open an issue
2. 📝 **Suggest Additions**: Missing subcategories or regions?
3. 🌍 **Regional Validation**: Help validate slang for your country
4. 🤝 **Community Review**: Represent an affected community? We want your feedback

### Acknowledgments

This dataset was created with deep respect for communities affected by racism in Latin America:

- Afro-descendant organizations across LATAM
- Indigenous peoples and nations
- Academic researchers in critical race studies
- Anti-racism activists

**Their trauma is not our data. Their experience deserves respect. Their dignity is non-negotiable.**

---

## 🌟 Related Work

### Academic Papers

- Telles, E. (2014). *Pigmentocracies: Ethnicity, Race, and Color in Latin America*
- Wade, P. (2017). *Race and Ethnicity in Latin America*
- Hernández, T. (2013). *Racial Subordination in Latin America*
- CEPAL (2020). *Afrodescendientes y la matriz de la desigualdad social en América Latina*

### Other DignityAI Datasets

- [SinOdio-LATAM](https://huggingface.co/datasets/Nohyc/SinOdio-LATAM) - General hate speech
- [DignityAI-Machismo-LATAM](https://huggingface.co/datasets/Nohyc/DignityAI-Machismo-LATAM) - Sexism & machismo
- [DignityAI-Clasismo-LATAM](https://huggingface.co/datasets/Nohyc/DignityAI-Clasismo-LATAM) - Economic discrimination

### Spanish NLP Resources

- [BETO](https://huggingface.co/dccuchile/bert-base-spanish-wwm-uncased) - Spanish BERT
- [RoBERTuito](https://huggingface.co/pysentimiento/robertuito-base-uncased) - Spanish Twitter RoBERTa
- [mBERT](https://huggingface.co/bert-base-multilingual-cased) - Multilingual BERT

---

## 🙏 Final Note

This dataset exists because racism exists. It documents pain that is real and ongoing.

**If you use this dataset:**
- Remember the real people behind these experiences
- Center their dignity in your work
- Use it to combat racism, not perpetuate it
- Commit to meaningful change, not just academic publishing

**Primero no dañar. Siempre consultar. Nunca perpetuar.**
*(First do no harm. Always consult. Never perpetuate.)*

---

<div align="center">

**🌟 DignityAI - Protecting Human Dignity Through AI 🌟**

*Built with respect, maintained with care, used with responsibility*

</div>
