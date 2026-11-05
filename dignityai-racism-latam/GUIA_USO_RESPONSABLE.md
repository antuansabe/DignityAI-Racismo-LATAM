# Guía de Uso Responsable - DignityAI-Racism-LATAM

## ⚠️ ADVERTENCIA ÉTICA CRÍTICA

Este dataset contiene **lenguaje racial ALTAMENTE SENSIBLE** que documenta racismo real con fines **EXCLUSIVAMENTE educativos y de investigación**.

---

## ❌ USOS PROHIBIDOS

Este dataset **NO DEBE** ser usado para:

### 1. Generar Contenido Racista

❌ **Entrenar modelos generativos** sin supervisión ética estricta
- **Riesgo**: Crear nuevas formas de racismo
- **Riesgo**: Amplificar estereotipos existentes
- **Riesgo**: Automatizar violencia racial

**Ejemplo de uso prohibido:**
```python
# ❌ NUNCA HACER ESTO
modelo_generativo.train(dataset['texto_racista'])
# Esto podría crear un bot racista
```

### 2. Mostrar Ejemplos Sin Contexto

❌ **Presentar textos racistas** sin explicación educativa
- **Riesgo**: Normalizar lenguaje racista
- **Riesgo**: Ofender comunidades afectadas
- **Riesgo**: Trivializar trauma histórico

**Ejemplo de uso prohibido:**
```python
# ❌ NUNCA HACER ESTO
for ejemplo in dataset:
    print(ejemplo['texto_racista'])  # Sin contexto ni advertencia
```

### 3. Uso Comercial Sin Consulta

❌ **Aplicaciones comerciales** sin beneficio comunitario
- **Riesgo**: Extractivismo de trauma
- **Riesgo**: "Profit from pain"
- **Riesgo**: Perpetuar injusticias

**Ejemplos prohibidos:**
- Apps de "detección de racismo" vendidas sin consulta
- Modelos propietarios entrenados sin compartir beneficios
- Servicios SaaS que monetizan sin retornar a comunidades

### 4. Entrenamiento Sin Auditoría de Sesgo

❌ **Modelos sin validación ética** rigurosa
- **Riesgo**: Bias amplificado
- **Riesgo**: Falsos positivos contra grupos afectados
- **Riesgo**: Perpetuar discriminación algorítmica

**Lo que NO hacer:**
- Entrenar sin métricas de equidad racial
- Deployer sin auditorías de sesgo
- Usar en producción sin monitoreo continuo

---

## ✅ USOS APROPIADOS

Este dataset PUEDE y DEBE ser usado para:

### 1. Investigación Académica Rigurosa

✅ **Estudios sobre racismo estructural**

**Requisitos:**
- IRB/CEIC approval obligatorio
- Content warnings en todos los materiales
- Contextualización histórica
- Citar apropiadamente

**Ejemplo apropiado:**
```python
# ✅ ESTO ESTÁ BIEN
# Paper: "Colorism Patterns in Mexican Social Media"
# IRB #12345 - Approved
# Content Warning at beginning of paper

dataset = load_dataset("dignityai-racism-latam")
# Analizar patrones, no mostrar textos raw
```

### 2. Entrenar Modelos de DETECCIÓN (No Generación)

✅ **Clasificadores para moderar contenido**

**Requisitos:**
- Solo para detectar/clasificar racismo
- Nunca para generar racismo
- Validación ética continua
- Auditorías de sesgo

**Ejemplo apropiado:**
```python
# ✅ ESTO ESTÁ BIEN
# Classifier para detectar racismo anti-indígena

from transformers import AutoModelForSequenceClassification

# Entrenar clasificador binario
# 1 = racista (para REMOVER/FLAG)
# 0 = no racista

model = AutoModelForSequenceClassification.from_pretrained(
    "dccuchile/bert-base-spanish-wwm-uncased",
    num_labels=2
)

# IMPORTANTE: Auditar con métricas de equidad
# - Equal Opportunity
# - Demographic Parity
# - False Positive Rate por grupo
```

### 3. Educación en Contextos Apropiados

✅ **Talleres, seminarios, cursos universitarios**

**Requisitos:**
- Facilitadores capacitados en estudios raciales
- Content warnings claros
- Espacio seguro para comunidades afectadas
- Énfasis en desmantelar racismo, no exhibirlo

**Ejemplo apropiado:**
```
Curso: "Racismo en Redes Sociales Latinoamericanas"
Semana 5: Colorismo

[CONTENT WARNING: Esta sesión contiene lenguaje racista explícito
con fines educativos. Si perteneces a comunidades afectadas y
necesitas apoyo, recursos disponibles en...]

Objetivo: Entender mecanismos de colorismo para combatirlos
```

### 4. Desarrollo de Herramientas de Moderación

✅ **Sistemas para proteger comunidades**

**Requisitos:**
- Beneficio DIRECTO a comunidades afectadas
- Consulta con esas comunidades
- Transparencia sobre limitaciones
- No reemplazar moderadores humanos

**Ejemplo apropiado:**
```python
# ✅ ESTO ESTÁ BIEN
# Sistema de alerta temprana para plataformas comunitarias

# Detector de racismo anti-afrolatino
detector = RacismDetector(
    model="fine-tuned-beto",
    categories=["racismo_anti_afrolatino"],
    action="flag_for_human_review",  # No auto-borrar
    transparency=True  # Explicar por qué se flagged
)

# Consultar con comunidad afrodescendiente sobre:
# - Threshold de detección
# - Proceso de apelación
# - Política de transparencia
```

---

## 📋 CHECKLIST PRE-USO

**Antes de usar este dataset, DEBES completar:**

### Aprobaciones Institucionales

- [ ] **IRB/CEIC approval** obtenido (si aplica)
- [ ] **Advisor/Supervisor** informado y de acuerdo
- [ ] **Comité de ética** revisó el protocolo

### Consulta Comunitaria

- [ ] **Académicos de estudios raciales** consultados
- [ ] **Organizaciones afrodescendientes** contactadas
- [ ] **Organizaciones indígenas** contactadas
- [ ] **Feedback comunitario** documentado e integrado

### Documentación y Transparencia

- [ ] **Content warnings** en TODOS los materiales
- [ ] **Contexto histórico** documentado
- [ ] **Limitaciones del dataset** reconocidas
- [ ] **Plan de mitigación de daños** elaborado

### Salvaguardas Técnicas

- [ ] **Auditorías de sesgo** planificadas
- [ ] **Métricas de equidad racial** definidas
- [ ] **Proceso de apelación** para falsos positivos
- [ ] **Monitoreo continuo** implementado

### Beneficio Comunitario

- [ ] **Resultados compartidos** con comunidades
- [ ] **Beneficio tangible** identificado
- [ ] **Crédito apropiado** a comunidades
- [ ] **Retribución** considerada (si comercial)

---

## 🛡️ PRINCIPIOS ÉTICOS

### 1. Primum Non Nocere (Primero No Dañar)

**"Antes de ayudar, asegúrate de no dañar"**

**Aplicado a este dataset:**
- ✅ Anticipar usos maliciosos y prevenirlos
- ✅ Priorizar protección de comunidades sobre innovación
- ✅ Tener plan de respuesta ante uso inapropiado
- ✅ Humildad: reconocer cuando no sabes

**Preguntas guía:**
- ¿Cómo podría esto dañar a comunidades racializadas?
- ¿Qué mecanismos tengo para prevenir daño?
- ¿Tengo la expertise para usar esto responsablemente?

### 2. Nada Sobre Nosotros Sin Nosotros

**"Nothing About Us Without Us"**

**Aplicado a este dataset:**
- ✅ Comunidades afectadas tienen VOZ en cómo se usa
- ✅ Su consentimiento informado es OBLIGATORIO
- ✅ Pueden pedir cambios o remoción
- ✅ Son COAUTORAS, no sujetos de estudio

**Preguntas guía:**
- ¿He consultado con las comunidades afectadas?
- ¿Tienen poder real para influir en mi trabajo?
- ¿Estoy centrando SUS necesidades o las mías?

### 3. Beneficio Comunitario Tangible

**"No extractivismo, sino reciprocidad"**

**Aplicado a este dataset:**
- ✅ El uso debe AYUDAR a comunidades afectadas
- ✅ No solo beneficio académico/comercial para mí
- ✅ Compartir resultados y herramientas
- ✅ Retribuir si hay ganancia económica

**Preguntas guía:**
- ¿Cómo beneficia CONCRETAMENTE esto a comunidades afectadas?
- ¿Estoy compartiendo poder/recursos/conocimiento?
- ¿O solo estoy "tomando" su trauma para mi CV?

### 4. Transparencia Radical

**"Honestidad sobre lo que sé y no sé"**

**Aplicado a este dataset:**
- ✅ Documentar limitaciones claramente
- ✅ Reconocer sesgos en la creación
- ✅ Ser honesto sobre qué NO puede hacer
- ✅ Admitir cuando cometo errores

**Preguntas guía:**
- ¿Estoy siendo honesto sobre las limitaciones?
- ¿He documentado mis propios sesgos?
- ¿Puedo explicar claramente qué NO debe hacerse?

---

## 🚨 MITIGACIÓN DE RIESGOS

### Riesgo 1: Perpetuar Estereotipos

**Descripción del riesgo:**
Modelos entrenados podrían aprender y amplificar estereotipos raciales existentes.

**Mitigación:**
✅ **Incluir SIEMPRE ejemplos antirracistas pareados**
- Ratio 1:1 racista:antirracista
- Enseñar al modelo AMBOS lados

✅ **Contextualizar históricamente**
- Explicar por qué el racismo existe
- No solo "esto es racista" sino "por qué"

✅ **Validar con comunidades afectadas**
- Mostrar resultados antes de publicar
- Ajustar según su feedback

**Métrica:**
- **Stereotype Score**: ¿El modelo replica estereotipos?
- Test: ¿Asocia "negro" con "criminal"? → FAIL
- Target: Zero stereotype replication

### Riesgo 2: Ofender Comunidades

**Descripción del riesgo:**
Mostrar lenguaje racista sin cuidado puede retraumatizar.

**Mitigación:**
✅ **Content warnings reforzados**
```
⚠️  ADVERTENCIA DE CONTENIDO

Este material contiene lenguaje racista explícito contra
[comunidades específicas]. Si perteneces a estas comunidades
y necesitas apoyo:

- [Recursos de salud mental]
- [Organizaciones de apoyo]
- [Líneas de crisis]

Puedes saltear esta sección sin penalización.
```

✅ **Consulta continua**
- Check-ins periódicos con comunidades
- Espacio para expresar incomodidad
- Poder de veto real

✅ **Mecanismo de feedback/remoción**
- Email para reportar daño
- Proceso de remoción rápido
- Disculpas públicas si es necesario

**Métrica:**
- **Harm Reports**: # de quejas recibidas
- Target: <5 per year, respuesta <48hrs

### Riesgo 3: Amplificar Sesgos en Modelos

**Descripción del riesgo:**
Modelos ML pueden amplificar sesgos sutiles en los datos.

**Mitigación:**
✅ **Auditorías de equidad racial OBLIGATORIAS**

**Métricas requeridas:**
```python
# Métricas de equidad por grupo afectado

metrics = {
    "Equal Opportunity": {
        "afrodescendientes": 0.85,
        "indigenas": 0.82,
        "mestizos": 0.88,
        "target": "> 0.80 para todos"
    },
    "Demographic Parity": {
        "max_difference": 0.05,
        "target": "< 0.10"
    },
    "False Positive Rate": {
        "afrodescendientes": 0.12,
        "indigenas": 0.15,
        "target": "< 0.15 para todos"
    }
}
```

✅ **Pruebas adversarias**
```python
# Test: ¿El modelo flagea mal contenido neutro de comunidades afectadas?

neutral_afro_tweets = [
    "Orgulloso de ser afrodescendiente",
    "Mi pelo afro es hermoso",
    "La cultura afrolatina es rica"
]

# Si modelo los flagea como racistas → FAIL
# Target: 0% false positives en contenido de orgullo racial
```

✅ **Debiasing techniques**
- Adversarial debiasing
- Counterfactual data augmentation
- Group-aware training

**Métrica:**
- **Fairness Score**: Composite de métricas arriba
- Target: > 0.85 en todas las métricas

### Riesgo 4: Uso Malicioso

**Descripción del riesgo:**
Actores malintencionados usan dataset para entrenar bots racistas.

**Mitigación:**
✅ **Licencia restrictiva (CC BY-NC-SA 4.0)**
- No comercial sin permiso
- Compartir igual si modifican
- Atribución obligatoria

✅ **Monitoreo de uso**
- Rastrear citaciones
- Buscar modelos sospechosos
- Denunciar uso inapropiado

✅ **Proceso de denuncia**
```
Si encuentras uso malicioso de este dataset:

1. Email: antuansabe@gmail.com
2. Asunto: "DENUNCIA - Uso Malicioso DignityAI-Racism"
3. Incluir:
   - URL o ubicación del uso malicioso
   - Descripción del daño
   - Screenshots si posible

Respuesta garantizada en 48hrs.
Acción legal si es necesario.
```

✅ **Takedown procedure**
- Contactar plataforma donde está hosteado
- Invocar licencia CC para remoción
- DMCA si ignoran

**Métrica:**
- **Malicious Use Reports**: # de casos detectados
- **Response Time**: Tiempo hasta acción
- Target: Response < 48hrs, Takedown < 7 días

---

## 📞 CONTACTO PARA DUDAS ÉTICAS

**Si tienes dudas sobre si tu uso es apropiado, contacta ANTES de usar:**

### Contacto

**Antonio Dromundo** (creador del dataset)
- Email: antuansabe@gmail.com
- GitHub: [github.com/antuansabe](https://github.com/antuansabe)
- Issues: [DignityAI-Racismo-LATAM/issues](https://github.com/antuansabe/DignityAI-Racismo-LATAM/issues)

### Organizaciones de referencia (no afiliadas)

Estas organizaciones trabajan en la región y son buenos puntos de partida para buscar consulta comunitaria. **No han revisado ni respaldan este dataset**; se listan solo como referencia.

**Afrodescendientes:**
- Red de Mujeres Afrolatinoamericanas, Afrocaribeñas y de la Diáspora

**Pueblos indígenas:**
- FILAC (Fondo para el Desarrollo de los Pueblos Indígenas de América Latina y el Caribe)
- COICA (Coordinadora de las Organizaciones Indígenas de la Cuenca Amazónica)

### Si Representas a una Comunidad Afectada

**Tu voz es PRIORITARIA. Por favor contacta si:**
- ❓ Tienes preguntas sobre el dataset
- 😟 Te sientes incómodo/a con su existencia
- 💡 Tienes sugerencias de mejora
- ❌ Quieres que se remueva contenido específico
- 🤝 Quieres colaborar en validación

**Tu feedback es vinculante, no consultivo.**

---

## 📚 LECTURAS OBLIGATORIAS

**Antes de usar este dataset, DEBES leer:**

### Sobre Ética en ML

1. **Data Feminism** - Catherine D'Ignazio & Lauren Klein
   - Por qué: Frameworks éticos para data science
   - [Link](https://data-feminism.mitpress.mit.edu/)

2. **Race After Technology** - Ruha Benjamin
   - Por qué: Cómo tecnología perpetúa racismo
   - Enfoque en "New Jim Code"

3. **Algorithms of Oppression** - Safiya Noble
   - Por qué: Sesgo racial en algoritmos
   - Caso de estudio: Google search

4. **Weapons of Math Destruction** - Cathy O'Neil
   - Por qué: Consecuencias de algoritmos no auditados

### Sobre Racismo en LATAM

1. **Pigmentocracies** - Edward Telles
   - Por qué: EL libro sobre colorismo en LATAM

2. **Race and Ethnicity in Latin America** - Peter Wade
   - Por qué: Overview comprehensivo

3. **Racial Subordination in Latin America** - Tanya Hernández
   - Por qué: Aspectos legales e institucionales

### Guías Técnicas

1. **Fairness and Machine Learning** - Barocas, Hardt, Narayanan
   - [Libro gratis online](https://fairmlbook.org/)
   - Por qué: Métricas de equidad explicadas

2. **AI Fairness 360** - IBM Toolkit
   - [GitHub](https://github.com/Trusted-AI/AIF360)
   - Por qué: Herramientas prácticas de debiasing

---

## ⚖️ IMPLICACIONES LEGALES

### Cumplimiento Legal

❗ **Este dataset NO constituye asesoría legal**

**Debes consultar:**
- ✅ Leyes locales sobre hate speech
- ✅ Regulaciones de privacidad (GDPR, CCPA, etc.)
- ✅ Términos de servicio de plataformas
- ✅ Requisitos institucionales (IRB, etc.)

### Jurisdicciones Específicas

**Unión Europea (GDPR)**
- Dataset no contiene datos personales identificables
- Pero outputs de modelos podrían generar contenido prohibido
- AI Act: sistemas de alto riesgo requieren auditorías

**Estados Unidos**
- Primer Enmienda protege hate speech (con excepciones)
- Pero plataformas privadas pueden prohibirlo
- Section 230: immunity si usas para moderación

**América Latina**
- Leyes varían por país
- Algunos países criminalizan hate speech
- Consultar jurídico local

### Protección de Responsabilidad

**Si usas este dataset:**

✅ **Disclaimer obligatorio:**
```
Este sistema usa DignityAI-Racism-LATAM para DETECTAR racismo.
Los textos racistas en el dataset son documentación de discriminación
real, NO representan las opiniones del desarrollador.

Este sistema tiene limitaciones [describir].
Falsos positivos son posibles. Si crees que fuiste incorrectamente
flagged, [proceso de apelación].
```

✅ **Terms of Service actualizados**
- Mencionar uso de ML
- Explicar posibilidad de errores
- Detallar proceso de apelación

---

## 🙏 AGRADECIMIENTOS A COMUNIDADES

**Este dataset solo existe gracias al conocimiento (y dolor) compartido por:**

- 🖤 Organizaciones afrodescendientes en 5 países
- 🌾 Comunidades indígenas
- 📚 Académicos de estudios raciales
- ✊ Activistas antirracistas

### Reconocimiento de Trauma

**Su trauma NO es nuestra data.**

Cada texto racista en este dataset representa:
- Dolor real experimentado por personas reales
- Historia de opresión de 500+ años
- Violencia continuada en el presente

**No lo olvides. No lo trivialices. No lo perpetúes.**

### Compromiso

Al usar este dataset, te comprometes a:

✅ **Honrar su experiencia**
- Tratarla con el respeto que merece
- No como "datos" sino como testimonio

✅ **Usar para sanar, no para herir**
- Objetivo: desmantelar racismo
- No: lucro personal o curiosidad académica vacía

✅ **Retribuir**
- Compartir resultados
- Ofrecer herramientas creadas
- Citar y dar crédito apropiadamente

---

## 🔚 CONCLUSIÓN

### Pregunta Final Antes de Usar

**¿Estoy usando esto para hacer el mundo MENOS racista o más racista?**

Si la respuesta no es clara, **NO LO USES**.

### Regla de Oro

> "Si no puedes cumplir con TODAS las directrices en esta guía,
> NO uses este dataset."

### No es Negociable

- ❌ No puedes saltarte IRB "porque es urgente"
- ❌ No puedes omitir consulta comunitaria "porque es difícil"
- ❌ No puedes ignorar content warnings "porque molesta al lector"
- ❌ No puedes evitar auditorías "porque son caras"

**Si no tienes tiempo/recursos para hacerlo bien, no lo hagas.**

### Recuerda

**La dignidad humana no es negociable.**
**El racismo no es un juego.**
**Este dataset es una responsabilidad, no un derecho.**

---

## 📝 Declaración de Compromiso

**Si usas este dataset, firma (conceptualmente) este compromiso:**

```
Yo, [nombre], me comprometo a:

✅ Usar DignityAI-Racism-LATAM EXCLUSIVAMENTE para combatir racismo
✅ Obtener todas las aprobaciones éticas necesarias
✅ Consultar con comunidades afectadas de buena fe
✅ Implementar todas las salvaguardas técnicas requeridas
✅ Publicar resultados con transparencia y humildad
✅ Reconocer limitaciones honestamente
✅ Retribuir a comunidades que hicieron esto posible
✅ Detener mi trabajo si causa daño

❌ NO generaré contenido racista
❌ NO mostraré ejemplos sin contexto
❌ NO usaré comercialmente sin consulta
❌ NO evitaré auditorías de sesgo
❌ NO ignoraré feedback comunitario
❌ NO pondré mi carrera/profit sobre dignidad humana

Entiendo que violar este compromiso no solo es antiético,
sino que daña a personas reales y perpetúa sistemas de opresión.

Firmo esto sabiendo que la comunidad académica y las comunidades
afectadas me harán responsable.

Fecha: [________]
Firma: [________]
```

---

**Primero no dañar. Siempre consultar. Nunca perpetuar.**

---

*Guía creada como parte de DignityAI-Racism-LATAM*
*Última actualización: Enero 2025*
*Versión: 1.0.0*
