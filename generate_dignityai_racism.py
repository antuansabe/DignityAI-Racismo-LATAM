#!/usr/bin/env python3
"""
DignityAI-Racism-LATAM Dataset Generator

Genera 35,000 ejemplos de discriminación racial usando templates + combinatoria
Parte de la iniciativa DignityAI - Protecting human dignity through AI

Author: Antonio Dromundo
Date: 2025
License: CC BY-NC-SA 4.0
"""

import random
import pandas as pd
import json
from datetime import datetime
from pathlib import Path
import hashlib
from typing import Dict, List, Tuple

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

TOTAL_EJEMPLOS = 35000
PAISES = ["México", "Argentina", "Colombia", "Chile", "Perú"]
EJEMPLOS_POR_PAIS = TOTAL_EJEMPLOS // len(PAISES)  # 7,000 por país

# ============================================================================
# CATEGORÍAS Y PESOS
# ============================================================================

CATEGORIAS = {
    "colorismo": {
        "peso": 0.25,
        "subcategorias": [
            "preferencia_piel_clara",
            "denigracion_piel_oscura",
            "jerarquia_racial_intragrupo",
            "blanqueamiento_aspiracional"
        ]
    },
    "racismo_anti_indigena": {
        "peso": 0.20,
        "subcategorias": [
            "estereotipos_indigenas",
            "negacion_identidad_indigena",
            "desprecio_lenguas_originarias",
            "folclorizacion_deshumanizante"
        ]
    },
    "racismo_anti_afrolatino": {
        "peso": 0.20,
        "subcategorias": [
            "estereotipos_afrodescendientes",
            "hipersexualizacion",
            "criminalizacion",
            "negacion_afrolatinidad"
        ]
    },
    "microagresiones_raciales": {
        "peso": 0.20,
        "subcategorias": [
            "comentarios_pelo_afro",
            "sorpresa_competencia",
            "exotizacion",
            "negacion_racismo",
            "tokenismo"
        ]
    },
    "racismo_institucional": {
        "peso": 0.15,
        "subcategorias": [
            "exclusion_espacial",
            "discriminacion_laboral",
            "perfilamiento_racial",
            "violencia_simbolica_institucional"
        ]
    }
}

# ============================================================================
# MODISMOS REGIONALES POR PAÍS
# ============================================================================

MODISMOS_RACISM = {
    "México": {
        "colorismo": {
            "piel_clara_positivo": [
                "güero", "güera", "blanquito", "blanquita",
                "catrín", "catrina", "de razón", "fresa"
            ],
            "piel_oscura_negativo": [
                "prieto", "prieta", "negro", "negra",
                "negruzco", "moreno retinto", "quemado", "tostado"
            ],
            "expresiones_colorismo": [
                "mejorar la raza", "está bonito para prieto",
                "pelo malo", "nariz de indio", "que salgan güeritos"
            ]
        },
        "anti_indigena": {
            "insultos": [
                "indio", "naco", "narizón", "indito",
                "teporocho", "oaxaquito", "indio maría"
            ],
            "estereotipos": [
                "indios ignorantes", "indios borrachos",
                "viene del cerro", "huarache"
            ]
        },
        "anti_afrolatino": {
            "insultos": [
                "negro", "negra", "mayate", "carbón",
                "negrito", "negrita", "azabache"
            ],
            "estereotipos": [
                "negro bailarín", "negro costeño",
                "negro callejero"
            ]
        },
        "zonas_geograficas": {
            "privilegiadas": ["Polanco", "Santa Fe", "Lomas", "Condesa"],
            "marginadas": ["Tepito", "Iztapalapa", "Ecatepec", "el sur"]
        },
        "conectores": ["wey", "pinche", "no mames", "órale", "compa"]
    },

    "Argentina": {
        "colorismo_clasismo": {
            "insultos": [
                "negro", "negra", "cabecita negra", "negrada",
                "morocho", "morocha", "negro villero"
            ],
            "expresiones": [
                "negro de mierda", "argentino de bien",
                "gente bien", "rubios de Recoleta"
            ]
        },
        "xenofobia_racializada": {
            "migrantes_paises_vecinos": [
                "bolita", "paragua", "peruca", "chilote"
            ],
            "estereotipos": [
                "invasión boliviana", "sucios paraguayos",
                "vienen a robar trabajo"
            ]
        },
        "anti_indigena": {
            "insultos": [
                "indio", "cabecita", "cholo", "provincianos"
            ],
            "estereotipos": [
                "indios del norte", "provincias atrasadas"
            ]
        },
        "invisibilizacion_afro": [
            "en Argentina no hay negros",
            "los negros desaparecieron",
            "somos todos europeos"
        ],
        "zonas_geograficas": {
            "privilegiadas": ["Palermo", "Recoleta", "Belgrano", "Puerto Madero"],
            "marginadas": ["villa", "conurbano", "La Matanza"]
        },
        "conectores": ["boludo", "che", "pelotudo", "gil", "flaco"]
    },

    "Colombia": {
        "colorismo": {
            "piel_clara_positivo": [
                "mono", "mona", "blanquito", "blanquita",
                "catire", "catira", "de buena familia"
            ],
            "piel_oscura_negativo": [
                "negro", "negra", "niche", "chombo",
                "prieto", "prieta", "azabache", "bemba", "bembón"
            ],
            "expresiones": [
                "mejorar la raza", "pelo malo",
                "nariz ancha", "labios gruesos"
            ]
        },
        "anti_afrolatino": {
            "insultos": [
                "negro", "negra", "chombo", "niche",
                "palenquero", "negro bembón"
            ],
            "estereotipos": [
                "negros calientes", "negros bailarines",
                "costeños flojos", "negros brutos",
                "solo sirven para deporte"
            ],
            "geografico": [
                "chocoano", "del Chocó", "pacífico pobre"
            ]
        },
        "anti_indigena": {
            "insultos": ["indio", "guambito", "salvaje"],
            "estereotipos": ["indios ignorantes", "atrasados"]
        },
        "zonas_geograficas": {
            "privilegiadas": ["Rosales", "Chicó", "El Poblado", "zona norte"],
            "marginadas": ["Ciudad Bolívar", "Soacha", "Chocó", "Pacífico"]
        },
        "conectores": ["parce", "parcero", "gonorrea", "marica", "llave"]
    },

    "Chile": {
        "colorismo": {
            "piel_clara_positivo": [
                "rubio", "rubia", "blanquito", "cuico", "pituco"
            ],
            "piel_oscura_negativo": [
                "negro", "negra", "moreno", "prieto", "negruzco"
            ]
        },
        "anti_indigena": {
            "insultos": [
                "indio", "mapuche", "roto", "flaite"
            ],
            "estereotipos": [
                "indios terroristas", "mapuches violentos",
                "indios borrachos", "problema mapuche"
            ],
            "conflicto_politico": [
                "terroristas mapuches", "conflicto araucano"
            ]
        },
        "xenofobia_racializada": {
            "migrantes": [
                "peruco", "boliviano", "colla",
                "haitiano culiao", "dominicano"
            ],
            "estereotipos": [
                "peruanos ladrones", "bolivianos sucios",
                "invasión haitiana"
            ]
        },
        "anti_afro": {
            "invisibilizacion": ["en Chile no hay negros"],
            "insultos": ["negro", "haitiano", "negro flaite"]
        },
        "zonas_geograficas": {
            "privilegiadas": ["Las Condes", "Vitacura", "Providencia", "Lo Barnechea"],
            "marginadas": ["La Pincoya", "Cerro Navia", "Puente Alto", "población"]
        },
        "conectores": ["weon", "wea", "conchetumare", "culiao", "perkin"]
    },

    "Perú": {
        "colorismo": {
            "piel_clara_positivo": [
                "blanquito", "blanquita", "pituco", "pituca",
                "de Miraflores", "de San Isidro"
            ],
            "piel_oscura_negativo": [
                "cholo", "chola", "cholito", "serrano",
                "negro", "negra", "zambo", "achorado"
            ],
            "expresiones": [
                "mejorar la raza", "blanquear la familia",
                "cholito de mierda", "cholificación"
            ]
        },
        "anti_indigena": {
            "insultos": [
                "cholo", "chola", "serrano", "serrana",
                "indio", "indígena bruto", "llama"
            ],
            "estereotipos": [
                "serranos ignorantes", "cholos sucios",
                "de la sierra", "provincianos",
                "indios de Puno", "de Cusco"
            ],
            "geografico": [
                "viene de la puna", "bajó del cerro",
                "serrano migrante"
            ]
        },
        "anti_afrolatino": {
            "insultos": [
                "negro", "negra", "zambo", "zamba",
                "negro retinto", "mayate"
            ],
            "estereotipos": [
                "negros futbolistas", "negros de la costa",
                "afroperuanos musicales"
            ]
        },
        "jerarquia_racial_peru": [
            "blancos limeños", "mestizos", "cholos", "indígenas", "afro"
        ],
        "zonas_geograficas": {
            "privilegiadas": ["San Isidro", "Miraflores", "La Molina", "Surco"],
            "marginadas": ["Comas", "Villa El Salvador", "San Juan de Lurigancho"]
        },
        "conectores": ["causa", "pata", "brother", "huevón", "compadre"]
    }
}

# ============================================================================
# CONTEXTOS
# ============================================================================

CONTEXTOS = [
    "redes_sociales",
    "conversacion_laboral",
    "interaccion_servicio_cliente",
    "comentario_politico",
    "discusion_familiar",
    "entorno_educativo",
    "espacio_publico",
    "medios_comunicacion",
    "foro_online",
    "app_citas",
    "grupo_whatsapp",
    "comentario_youtube",
    "interaccion_policial",
    "proceso_contratacion"
]

# ============================================================================
# TEMPLATES POR CATEGORÍA Y SUBCATEGORÍA
# ============================================================================

TEMPLATES = {
    "colorismo": {
        "preferencia_piel_clara": {
            "racista": [
                "Busco {tipo_persona} de piel {tono_claro} para {contexto}",
                "{termino_claro} sí entran, {termino_oscuro} no",
                "Prefiero {termino_claro}, los {termino_oscuro} no me gustan",
                "Que salgan {termino_claro} los hijos, no {termino_oscuro}",
                "Necesito alguien {caracteristica_positiva_clara} para {rol_publico}",
                "{conector}, solo {termino_claro} aquí, {termino_oscuro} no",
                "Mi familia es de {termino_claro}, no nos mezclamos con {termino_oscuro}",
                "Para {contexto_laboral} buscamos {caracteristica_estetica_clara}",
                "Los {termino_claro} son más {estereotipo_positivo} que los {termino_oscuro}",
                "{termino_claro} sí, {termino_oscuro} definitivamente no",
                "Buscando pareja {termino_claro}, para {razon_blanqueamiento}",
                "En {zona_privilegiada} solo {termino_claro}, así debe ser",
                "Los {termino_oscuro} que se vayan a {zona_marginal}",
                "Aquí puro {termino_claro}, gente de bien",
                "No me junto con {termino_oscuro}, soy {termino_claro}"
            ],
            "antirracista": [
                "Busco {tipo_persona} capacitada para {contexto}, sin importar {caracteristica_fisica}",
                "El valor de una persona no depende de {tono_piel}",
                "Respeto a todas las personas independientemente de {caracteristica_racial}",
                "La belleza existe en {diversidad_tonos}, no solo en {ideal_eurocéntrico}",
                "{cualidad_personal} es lo que importa, no {apariencia_racial}",
                "Todos los {tonos_piel} son igualmente {valor_positivo}",
                "Valoro a las personas por {cualidades_internas}, no por {color_piel}",
                "La discriminación por {tono_piel} es inaceptable en {contexto}",
                "Celebro la {diversidad_racial} en mi {contexto_social}",
                "No existe raza superior o inferior, todos somos {igualdad_humana}",
                "El colorismo es una forma de racismo que debemos combatir",
                "La preferencia por piel clara es producto del colonialismo",
                "Rechazo los estándares de belleza eurocéntricos",
                "Todos los tonos de piel son hermosos y válidos",
                "El privilegio de piel clara debe ser reconocido y cuestionado"
            ],
            "variables": {
                "tipo_persona": ["empleado", "pareja", "amigos", "compañero", "persona", "candidato", "inquilino"],
                "tono_claro": ["clara", "blanca", "muy clara"],
                "termino_claro": [],  # Se rellena dinámicamente por país
                "termino_oscuro": [],  # Se rellena dinámicamente por país
                "contexto": ["el trabajo", "mi familia", "este lugar", "mi círculo", "esta empresa"],
                "caracteristica_positiva_clara": ["de buena presencia", "bien presentado", "imagen apropiada", "aspecto profesional"],
                "rol_publico": ["atención al cliente", "recepción", "ventas", "imagen corporativa"],
                "conector": [],  # Se rellena dinámicamente por país
                "contexto_laboral": ["recepción", "ventas", "imagen", "atención al público"],
                "caracteristica_estetica_clara": ["buena presencia", "imagen apropiada", "presentación adecuada"],
                "estereotipo_positivo": ["educados", "limpios", "inteligentes", "trabajadores", "confiables"],
                "razon_blanqueamiento": ["mejorar la raza", "que salgan bonitos los hijos", "blanquear la familia"],
                "zona_privilegiada": [],  # Se rellena dinámicamente por país
                "zona_marginal": [],  # Se rellena dinámicamente por país
                "caracteristica_fisica": ["su color de piel", "su apariencia física", "su tono de piel", "características raciales"],
                "tono_piel": ["el color de piel", "el tono de piel", "la pigmentación", "la melanina"],
                "caracteristica_racial": ["su raza", "su color", "su origen étnico", "su apariencia física"],
                "diversidad_tonos": ["todos los tonos", "toda la gama de colores", "toda pigmentación", "todas las pieles"],
                "ideal_eurocéntrico": ["un solo estándar", "piel clara únicamente", "modelos europeos"],
                "cualidad_personal": ["el carácter", "la integridad", "la capacidad", "el esfuerzo", "el talento"],
                "apariencia_racial": ["el color de piel", "la apariencia física", "características raciales"],
                "tonos_piel": ["colores de piel", "tonos", "pigmentaciones"],
                "valor_positivo": ["hermosos", "valiosos", "dignos de respeto", "válidos", "importantes"],
                "cualidades_internas": ["su carácter", "sus valores", "sus capacidades", "su humanidad", "su integridad"],
                "color_piel": ["el color de piel", "el tono", "la apariencia"],
                "contexto_social": ["comunidad", "familia", "círculo social", "entorno", "grupo"],
                "diversidad_racial": ["diversidad de pieles", "pluralidad racial", "mezcla de culturas", "multiculturalidad"],
                "igualdad_humana": ["igualmente humanos", "igualmente dignos", "parte de la humanidad", "seres humanos valiosos"]
            }
        },

        "denigracion_piel_oscura": {
            "racista": [
                "Pinche {insulto_piel_oscura}, vete a {lugar_despectivo}",
                "{insulto_piel_oscura} de mierda, no {accion_permitida} aquí",
                "Qué hace este {insulto_piel_oscura} en {zona_privilegiada}",
                "{conector}, {insulto_piel_oscura}, {orden_exclusion}",
                "Este {insulto_piel_oscura} está muy {estereotipo_negativo}",
                "Los {insulto_piel_oscura} siempre {estereotipo_comportamiento}",
                "{insulto_piel_oscura} como tú no deberían {derecho_basico}",
                "Eres muy {insulto_piel_oscura} para {actividad_reservada}",
                "Pareces {insulto_piel_oscura}, {observacion_negativa}",
                "No me junto con {insulto_piel_oscura}, {razon_prejuiciosa}",
                "{insulto_piel_oscura} mugroso, {insulto_adicional}",
                "Qué asco de {insulto_piel_oscura}",
                "Los {insulto_piel_oscura} no tienen {cualidad_humana}",
                "Mejor me voy, llegaron los {insulto_piel_oscura}",
                "{insulto_piel_oscura} tenía que ser"
            ],
            "antirracista": [
                "El tono de piel no define {valor_humano}",
                "Respeto a todas las personas independientemente de {caracteristica_racial}",
                "La discriminación por {color_piel} es inaceptable",
                "Todos merecemos {derecho} sin importar nuestro {tono_piel}",
                "El racismo por {color_piel} es una forma de {violencia_tipo}",
                "Celebro la {diversidad_pieles} en nuestra sociedad",
                "No existe piel 'mejor' o 'peor', solo {diversidad_humana}",
                "Insultar por {color_piel} es {tipo_discriminacion}",
                "Valoro a las personas por {cualidades_internas}, no por {apariencia}",
                "El {tono_piel} no determina {capacidad_valor}",
                "Los insultos raciales son violencia y deben ser condenados",
                "La dignidad humana no depende del color de piel",
                "Defiendo el derecho de todas las personas a ser respetadas",
                "El racismo es inaceptable en cualquier forma o contexto",
                "Rechazo completamente la discriminación por tono de piel"
            ],
            "variables": {
                "insulto_piel_oscura": [],  # Se rellena dinámicamente por país
                "lugar_despectivo": ["tu barrio", "tu rancho", "de donde saliste", "tu favela", "tu agujero"],
                "accion_permitida": ["entras", "estás", "trabajas", "vives", "quedarte"],
                "zona_privilegiada": [],  # Se rellena dinámicamente por país
                "conector": [],  # Se rellena dinámicamente por país
                "orden_exclusion": ["lárgate", "fuera de aquí", "no perteneces", "vete", "no eres bienvenido"],
                "estereotipo_negativo": ["sucio", "feo", "oscuro", "quemado", "tostado"],
                "estereotipo_comportamiento": ["roban", "son flojos", "huelen mal", "no se bañan", "son ignorantes"],
                "derecho_basico": ["estar aquí", "trabajar aquí", "vivir aquí", "estudiar aquí", "entrar aquí"],
                "actividad_reservada": ["este trabajo", "este lugar", "esta escuela", "este club", "este evento"],
                "observacion_negativa": ["da mala imagen", "no encajas", "bajas el nivel", "no perteneces", "estás fuera de lugar"],
                "razon_prejuiciosa": ["son inferiores", "no son de mi nivel", "bajan mi estatus", "no son mi clase"],
                "insulto_adicional": ["vete de aquí", "no perteneces", "eres basura", "das asco"],
                "cualidad_humana": ["dignidad", "valor", "educación", "cultura"],
                "valor_humano": ["tu valor", "tu dignidad", "quién eres", "tus capacidades", "tu humanidad"],
                "caracteristica_racial": ["su color de piel", "su apariencia racial", "su tono", "su pigmentación"],
                "color_piel": ["color de piel", "tono de piel", "apariencia racial"],
                "derecho": ["respeto", "dignidad", "oportunidades", "trato justo", "acceso"],
                "tono_piel": ["tono de piel", "color", "pigmentación", "apariencia física"],
                "violencia_tipo": ["violencia", "opresión", "discriminación", "injusticia", "abuso"],
                "diversidad_pieles": ["diversidad de pieles", "variedad de tonos", "pluralidad racial", "multiculturalidad"],
                "diversidad_humana": ["diversidad humana", "variedad natural", "riqueza de la humanidad"],
                "tipo_discriminacion": ["racismo", "discriminación", "violencia verbal", "prejuicio inaceptable"],
                "cualidades_internas": ["su carácter", "sus valores", "su esfuerzo", "sus capacidades", "su humanidad"],
                "apariencia": ["su apariencia", "su físico", "cómo lucen", "su color de piel"],
                "capacidad_valor": ["tu valor", "tus capacidades", "tu inteligencia", "tu potencial", "tu humanidad"]
            }
        },

        "jerarquia_racial_intragrupo": {
            "racista": [
                "Al menos no soy tan {termino_oscuro} como {grupo_mas_oscuro}",
                "Yo soy {tono_intermedio}, no como esos {termino_muy_oscuro}",
                "En mi familia somos {tono_claro}, no {tono_oscuro}",
                "Prefiero que mi hijo se case con alguien {comparacion_clara}, no {comparacion_oscura}",
                "{conector}, soy {tono_claro}, no me compares con {tono_oscuro}",
                "Gracias a Dios salí {tono_claro} y no {tono_oscuro} como {familiar}",
                "Los más {termino_oscuro} de la familia siempre {estereotipo_negativo}",
                "Yo tengo {caracteristica_eurocentrica}, no soy {termino_oscuro}",
                "Mi pelo es {tipo_pelo_eurocentrico}, no {tipo_pelo_afro} como los {termino_oscuro}",
                "Al menos tengo {rasgo_europeo}, no como los {termino_oscuro}"
            ],
            "antirracista": [
                "El colorismo internalizado daña a nuestras propias comunidades",
                "No existe jerarquía dentro de los tonos de piel",
                "Rechazar a personas de nuestra comunidad por ser más oscuras es racismo",
                "El colorismo intragrupo es producto del colonialismo",
                "Todos los tonos en nuestra comunidad merecen igual respeto",
                "Compararnos por tonos de piel perpetúa el racismo sistémico",
                "La unidad de nuestra comunidad requiere rechazar el colorismo",
                "Valorar piel más clara es internalizar opresión colonial",
                "No hay 'mejor' o 'peor' tono dentro de nuestra comunidad",
                "El colorismo divide y debilita a comunidades racializadas"
            ],
            "variables": {
                "termino_oscuro": [],  # Se rellena dinámicamente por país
                "grupo_mas_oscuro": ["los del pueblo", "los de la costa", "los del campo", "ellos"],
                "tono_intermedio": ["moreno claro", "trigueño", "mestizo", "medio"],
                "termino_muy_oscuro": [],  # Se rellena dinámicamente por país
                "tono_claro": ["clarito", "blanquito", "güerito", "de piel clara"],
                "tono_oscuro": ["oscuro", "retinto", "muy moreno", "negro"],
                "comparacion_clara": ["más claro", "blanquito", "de piel clara", "güero"],
                "comparacion_oscura": ["oscuro", "negro", "retinto", "muy moreno"],
                "conector": [],  # Se rellena dinámicamente por país
                "familiar": ["mi hermano", "mi prima", "mi tío", "mi padre"],
                "estereotipo_negativo": ["tienen problemas", "no salen adelante", "tienen mala suerte", "sufren más"],
                "caracteristica_eurocentrica": ["nariz fina", "pelo liso", "ojos claros", "piel clara"],
                "tipo_pelo_eurocentrico": ["lacio", "liso", "fino", "suave"],
                "tipo_pelo_afro": ["crespo", "rizado", "chino", "malo"],
                "rasgo_europeo": ["nariz respingada", "pelo lacio", "ojos claros", "labios finos"]
            }
        },

        "blanqueamiento_aspiracional": {
            "racista": [
                "Busco pareja {termino_claro} para {razon_blanqueamiento}",
                "Espero que mis hijos salgan {termino_claro}, no {termino_oscuro}",
                "Necesito {accion_blanqueamiento} para {objetivo_social}",
                "Con suerte los nietos saldrán más {termino_claro}",
                "{conector}, hay que {accion_blanqueamiento} la familia",
                "Si te casas con {termino_claro}, tus hijos {beneficio_blanqueamiento}",
                "Los {termino_oscuro} deben buscar {termino_claro} para mejorar",
                "Cada generación más {termino_claro} es mejor",
                "Hay que {accion_blanqueamiento} para que los hijos {objetivo_movilidad}",
                "Gracias a Dios mi hijo salió {termino_claro}"
            ],
            "antirracista": [
                "El 'blanqueamiento' es una ideología racista colonial",
                "No hay nada que 'mejorar' en la raza, somos valiosos como somos",
                "Buscar 'blanquear' descendencia es internalizar racismo",
                "Las políticas de blanqueamiento fueron genocidio cultural",
                "Todas las combinaciones de tonos de piel son hermosas",
                "El orgullo de nuestro color de piel debe ser celebrado",
                "Rechazar el blanqueamiento aspiracional es un acto de resistencia",
                "No necesitamos 'mejorar la raza', necesitamos combatir el racismo",
                "El concepto de 'mejorar la raza' es inherentemente racista",
                "Valorar nuestra apariencia sin aspirar a la blanquitud es liberador"
            ],
            "variables": {
                "termino_claro": [],  # Se rellena dinámicamente por país
                "razon_blanqueamiento": ["mejorar la raza", "que salgan bonitos", "blanquear la familia", "subir de nivel"],
                "termino_oscuro": [],  # Se rellena dinámicamente por país
                "accion_blanqueamiento": ["mejorar la raza", "blanquear", "aclarar", "mejorar"],
                "objetivo_social": ["subir socialmente", "mejorar la familia", "tener éxito", "progresar"],
                "conector": [],  # Se rellena dinámicamente por país
                "beneficio_blanqueamiento": ["saldrán mejor", "tendrán más oportunidades", "no sufrirán racismo", "serán aceptados"],
                "objetivo_movilidad": ["tengan éxito", "no sufran", "sean aceptados", "progresen"]
            }
        }
    },

    "racismo_anti_indigena": {
        "estereotipos_indigenas": {
            "racista": [
                "Los {termino_indigena} son {estereotipo_negativo}",
                "{insulto_indigena} de mierda, {observacion_despectiva}",
                "Pinche {insulto_indigena}, {acusacion_estereotipada}",
                "{conector}, los {termino_indigena} siempre {comportamiento_estereotipado}",
                "Es un {insulto_indigena}, no {capacidad_negada}",
                "Los {termino_indigena} solo sirven para {rol_servil}",
                "{insulto_indigena} ignorante, {insulto_adicional}",
                "Pareces {insulto_indigena}, {critica_apariencia}",
                "Los {termino_indigena} no {habilidad_intelectual}",
                "Ese {insulto_indigena} viene de {lugar_marginal}",
                "Pinche {insulto_indigena}, {observacion_despectiva}",
                "{termino_indigena} tenía que ser",
                "Los {termino_indigena} siempre {comportamiento_estereotipado}",
                "Qué hace este {insulto_indigena} aquí",
                "{insulto_indigena} mugroso"
            ],
            "antirracista": [
                "Los pueblos indígenas tienen {derecho_reconocimiento}",
                "Respeto profundamente {cultura_indigena}",
                "Los estereotipos sobre {pueblos_indigenas} son {tipo_daño}",
                "Las comunidades indígenas merecen {reconocimiento}",
                "Valoro {conocimiento_ancestral} de los pueblos originarios",
                "La discriminación contra {indigenas} es {tipo_violencia}",
                "Los {pueblos_originarios} son {reconocimiento_positivo}",
                "No existe ninguna {jerarquia_racial} entre culturas",
                "Celebro {diversidad_cultural} de nuestros pueblos originarios",
                "Los {indigenas} tienen derecho a {derechos_basicos}",
                "Los pueblos indígenas son guardianes de conocimiento ancestral",
                "La cultura indígena es parte fundamental de nuestra identidad",
                "Rechazo completamente los estereotipos sobre pueblos indígenas",
                "Los pueblos originarios merecen respeto y autodeterminación",
                "La discriminación anti-indígena es racismo colonial persistente"
            ],
            "variables": {
                "termino_indigena": [],  # Se rellena dinámicamente por país
                "estereotipo_negativo": ["ignorantes", "flojos", "borrachos", "sucios", "atrasados", "brutos"],
                "insulto_indigena": [],  # Se rellena dinámicamente por país
                "observacion_despectiva": ["hueles mal", "estás sucio", "eres ignorante", "no sabes nada", "eres atrasado"],
                "acusacion_estereotipada": ["seguro vienes borracho", "siempre robando", "no sabes hablar bien"],
                "conector": [],  # Se rellena dinámicamente por país
                "comportamiento_estereotipado": ["están borrachos", "roban", "son flojos", "huelen mal", "no trabajan"],
                "capacidad_negada": ["entiende", "sabe", "puede aprender", "piensa", "razona"],
                "rol_servil": ["limpiar", "cargar", "trabajo pesado", "servir", "obedecer"],
                "insulto_adicional": ["no sabes nada", "eres bruto", "eres atrasado", "vienes del monte"],
                "critica_apariencia": ["qué feo", "qué corriente", "qué mal vestido", "qué sucio"],
                "habilidad_intelectual": ["entienden", "aprenden", "piensan", "razonan", "estudian"],
                "lugar_marginal": ["el cerro", "el monte", "la selva", "el pueblo", "la sierra"],
                "derecho_reconocimiento": ["derecho a su tierra", "derecho a su cultura", "derecho a la autodeterminación"],
                "cultura_indigena": ["la cultura indígena", "las tradiciones ancestrales", "el conocimiento originario"],
                "pueblos_indigenas": ["pueblos indígenas", "comunidades originarias", "pueblos originarios"],
                "tipo_daño": ["dañinos", "racistas", "ofensivos", "discriminatorios", "violentos"],
                "reconocimiento": ["respeto y reconocimiento", "dignidad", "sus derechos", "justicia"],
                "conocimiento_ancestral": ["el conocimiento ancestral", "la sabiduría milenaria", "las tradiciones", "la cosmovisión"],
                "indigenas": ["pueblos indígenas", "comunidades originarias", "personas indígenas"],
                "tipo_violencia": ["racismo", "discriminación", "violencia colonial", "opresión histórica"],
                "pueblos_originarios": ["pueblos originarios", "comunidades indígenas", "naciones originarias"],
                "reconocimiento_positivo": ["guardianes de la tierra", "portadores de sabiduría", "pilares culturales", "parte fundamental"],
                "jerarquia_racial": ["jerarquía racial", "superioridad cultural", "raza superior"],
                "diversidad_cultural": ["la diversidad cultural", "la riqueza cultural", "la pluralidad"],
                "derechos_basicos": ["mantener su cultura", "hablar su lengua", "vivir en su territorio", "preservar tradiciones"]
            }
        },

        "negacion_identidad_indigena": {
            "racista": [
                "Ya no hay {termino_indigena}, todos somos {identidad_nacional}",
                "Los {termino_indigena} son cosa del pasado",
                "{conector}, olvídate de esas {expresion_despectiva} indígenas",
                "Mejor {accion_asimilacion} y deja de ser {insulto_indigena}",
                "En este país no hay {termino_indigena}, somos {identidad_mestiza}",
                "Los {termino_indigena} deberían {accion_asimilacion_forzada}",
                "Deja de hacerte el {insulto_indigena}, eres {identidad_impuesta}",
                "Ya supera eso de ser {termino_indigena}",
                "No te hagas el {insulto_indigena}, habla bien",
                "Aquí somos todos {identidad_nacional}, no {termino_indigena}"
            ],
            "antirracista": [
                "La identidad indígena es válida y debe ser respetada",
                "Negar la existencia de pueblos indígenas es {tipo_violencia}",
                "Los pueblos indígenas tienen derecho a {derecho_identidad}",
                "La asimilación forzada es genocidio cultural",
                "Cada pueblo indígena tiene derecho a {autodeterminacion}",
                "La identidad mestiza no debe borrar la indígena",
                "Reconocer y celebrar la identidad indígena es fundamental",
                "El orgullo indígena debe ser apoyado, no reprimido",
                "La diversidad de identidades indígenas enriquece nuestra sociedad",
                "Negar la indigenidad es continuar la colonización"
            ],
            "variables": {
                "termino_indigena": [],  # Se rellena dinámicamente por país
                "identidad_nacional": ["mexicanos", "argentinos", "colombianos", "chilenos", "peruanos"],
                "conector": [],  # Se rellena dinámicamente por país
                "expresion_despectiva": ["tonterías", "cosas", "costumbres", "tradiciones"],
                "accion_asimilacion": ["modernízate", "civilízate", "progresa", "asimílate"],
                "insulto_indigena": [],  # Se rellena dinámicamente por país
                "identidad_mestiza": ["mestizos", "mezclados", "modernos", "civilizados"],
                "accion_asimilacion_forzada": ["asimilarse", "modernizarse", "civilizarse", "olvidar sus costumbres"],
                "identidad_impuesta": ["mestizo", "moderno", "normal", "como todos"],
                "tipo_violencia": ["genocidio cultural", "racismo estructural", "colonialismo persistente"],
                "derecho_identidad": ["mantener su identidad", "ser quienes son", "preservar su cultura"],
                "autodeterminacion": ["autodeterminarse", "definir su identidad", "mantener sus tradiciones"]
            }
        },

        "desprecio_lenguas_originarias": {
            "racista": [
                "Habla bien, no en {lengua_indigena}",
                "Esa lengua de {insulto_indigena} no sirve para nada",
                "{conector}, habla {idioma_dominante}, no {despectivo_lengua}",
                "Las lenguas indígenas son {caracterizacion_negativa}",
                "Deja de hablar {lengua_indigena}, estamos en {pais}",
                "Qué feo suena ese {despectivo_lengua}",
                "Aprende a hablar bien, no como {insulto_indigena}",
                "Esas lenguas no sirven para {contexto_moderno}",
                "{lengua_indigena} es lengua de {insulto_indigena}",
                "Habla como persona, no en {despectivo_lengua}"
            ],
            "antirracista": [
                "Las lenguas indígenas son patrimonio cultural invaluable",
                "Cada lengua originaria representa {valor_cultural}",
                "El multilingüismo enriquece nuestra sociedad",
                "Las lenguas indígenas tienen {derecho_linguistico}",
                "Respetar las lenguas originarias es respetar los derechos humanos",
                "La diversidad lingüística debe ser protegida y celebrada",
                "Las lenguas indígenas son tan válidas como cualquier otra",
                "Ridiculizar lenguas indígenas es racismo lingüístico",
                "Cada lengua originaria contiene conocimiento ancestral único",
                "El derecho a hablar lenguas indígenas debe ser garantizado"
            ],
            "variables": {
                "lengua_indigena": ["náhuatl", "quechua", "mapudungun", "guaraní", "maya", "zapoteco", "aymara"],
                "insulto_indigena": [],  # Se rellena dinámicamente por país
                "conector": [],  # Se rellena dinámicamente por país
                "idioma_dominante": ["español", "castellano", "bien"],
                "despectivo_lengua": ["dialecto", "jerga", "idioma raro", "lengua de indios"],
                "caracterizacion_negativa": ["atrasadas", "inútiles", "primitivas", "del pasado"],
                "pais": ["México", "Argentina", "Colombia", "Chile", "Perú"],
                "contexto_moderno": ["el trabajo", "la educación", "los negocios", "la vida moderna"],
                "valor_cultural": ["sabiduría milenaria", "patrimonio cultural", "riqueza lingüística"],
                "derecho_linguistico": ["derecho a existir", "igual validez", "reconocimiento oficial"]
            }
        },

        "folclorizacion_deshumanizante": {
            "racista": [
                "Los {termino_indigena} son buenos para {actividad_folclorica}, nada más",
                "Qué lindo {expresion_condescendiente} con su {elemento_folclore}",
                "Los {termino_indigena} son del pasado, {observacion_museo}",
                "{conector}, los {termino_indigena} solo sirven para {uso_turistico}",
                "Vamos a ver a los {termino_indigena} como {objeto_turistico}",
                "Los {termino_indigena} deben quedarse en {lugar_turistico}",
                "Son como un {objeto_museo}, del pasado",
                "Qué pintoresco ver {termino_indigena} con {vestimenta_tradicional}",
                "Los {termino_indigena} son para {contexto_turistico}, no para {contexto_moderno}",
                "Bonito folklore, pero no son para {actividad_moderna}"
            ],
            "antirracista": [
                "Los pueblos indígenas son culturas vivas, no folklore",
                "Reducir pueblos indígenas a {objeto_folclore} es deshumanizante",
                "Las culturas indígenas son contemporáneas y dinámicas",
                "Los pueblos originarios tienen derecho a {vida_moderna_propia}",
                "No son del pasado, son parte viva de nuestra sociedad",
                "La folclorización invisibiliza las luchas actuales indígenas",
                "Los pueblos indígenas definen su propia relación con la modernidad",
                "Respetar significa ver pueblos vivos, no reliquias",
                "Las comunidades indígenas son sujetos políticos contemporáneos",
                "La cultura indígena no es espectáculo para turistas"
            ],
            "variables": {
                "termino_indigena": [],  # Se rellena dinámicamente por país
                "actividad_folclorica": ["bailar", "hacer artesanías", "decoración", "turismo"],
                "expresion_condescendiente": ["el indito", "el indígena", "el nativo"],
                "elemento_folclore": ["traje típico", "artesanía", "baile", "música"],
                "observacion_museo": ["cosa del pasado", "de museo", "reliquias", "extintos"],
                "conector": [],  # Se rellena dinámicamente por país
                "uso_turistico": ["turismo", "fotos", "decoración", "espectáculo"],
                "objeto_turistico": ["atracción turística", "espectáculo", "entretenimiento"],
                "lugar_turistico": ["sus pueblos", "el campo", "la reserva", "el museo"],
                "objeto_museo": ["pieza de museo", "reliquia", "fósil", "anacronismo"],
                "vestimenta_tradicional": ["sus trajes", "su ropa típica", "su vestimenta tradicional"],
                "contexto_turistico": ["fotos", "turismo", "espectáculo", "folklore"],
                "contexto_moderno": ["trabajos importantes", "política", "la ciudad", "el presente"],
                "objeto_folclore": ["folklore", "espectáculo", "decoración"],
                "vida_moderna_propia": ["vivir en el presente", "definir su modernidad", "participar en la sociedad"],
                "actividad_moderna": ["política", "profesiones", "educación superior", "liderazgo"]
            }
        }
    },

    "racismo_anti_afrolatino": {
        "estereotipos_afrodescendientes": {
            "racista": [
                "Los {termino_afro} solo sirven para {estereotipo_rol}",
                "{insulto_afro} de mierda, {acusacion}",
                "Seguro ese {termino_afro} {estereotipo_criminal}",
                "Los {termino_afro} son {estereotipo_fisico}",
                "{conector}, ese {insulto_afro} {prediccion_negativa}",
                "No contrato {termino_afro}, {razon_discriminatoria}",
                "Ese {termino_afro} debe ser {profesion_estereotipada}",
                "Los {termino_afro} tienen {caracteristica_estereotipada}",
                "{insulto_afro}, seguro {asuncion_criminal}",
                "Los {termino_afro} no {capacidad_intelectual}",
                "Todos los {termino_afro} son {estereotipo_deportivo}",
                "{termino_afro} tenía que ser",
                "Los {termino_afro} siempre {comportamiento_estereotipado}",
                "Con ese {insulto_afro} cuidado",
                "Pinche {insulto_afro} {estereotipo_negativo}"
            ],
            "antirracista": [
                "Las personas afrodescendientes tienen {derecho}",
                "Los estereotipos sobre {afrodescendientes} son {calificativo_negativo}",
                "Respeto {diversidad_afro} en nuestra sociedad",
                "La discriminación contra {afrodescendientes} es {tipo_violencia}",
                "Valoro a las personas por {cualidades}, no por {raza}",
                "Los {afrolatinos} son {reconocimiento_positivo}",
                "Rechazo {estereotipos_raciales} contra comunidades afro",
                "La {afrodescendencia} es parte fundamental de {identidad_latam}",
                "Todos merecemos {trato_digno} sin importar {color_piel}",
                "Celebro {contribuciones_afro} a nuestra cultura",
                "Los estereotipos afroraciales son dañinos y falsos",
                "Las personas afrodescendientes merecen respeto pleno",
                "Rechazo la reducción de personas afro a estereotipos",
                "La diversidad afrolatina enriquece nuestra región",
                "No tolero discriminación contra afrodescendientes"
            ],
            "variables": {
                "termino_afro": [],  # Se rellena dinámicamente por país
                "estereotipo_rol": ["fútbol", "bailar", "música", "deportes", "trabajo físico"],
                "insulto_afro": [],  # Se rellena dinámicamente por país
                "acusacion": ["seguro robaste algo", "eres un delincuente", "vienes a hacer problemas"],
                "estereotipo_criminal": ["es ladrón", "es delincuente", "anda en malos pasos", "es peligroso", "es violento"],
                "estereotipo_fisico": ["buenos para deportes", "fuertes pero brutos", "calientes", "agresivos"],
                "conector": [],  # Se rellena dinámicamente por país
                "prediccion_negativa": ["va a robar", "va a causar problemas", "es peligroso", "anda en malas"],
                "razon_discriminatoria": ["dan mala imagen", "asustan a los clientes", "no son confiables", "son problemáticos"],
                "profesion_estereotipada": ["futbolista", "bailarín", "músico", "guardia", "cargador"],
                "caracteristica_estereotipada": ["ritmo natural", "habilidad física", "temperamento caliente", "fuerza bruta"],
                "asuncion_criminal": ["anda robando", "está armado", "es peligroso", "anda en malos pasos"],
                "capacidad_intelectual": ["son inteligentes", "estudian bien", "piensan", "razonan", "son profesionales"],
                "estereotipo_deportivo": ["buenos para fútbol", "atléticos", "fuertes"],
                "comportamiento_estereotipado": ["roban", "son violentos", "andan en malas", "son flojos"],
                "estereotipo_negativo": ["peligroso", "ladrón", "violento", "ignorante"],
                "derecho": ["los mismos derechos", "dignidad plena", "respeto absoluto", "oportunidades iguales"],
                "afrodescendientes": ["personas afrodescendientes", "comunidades afro", "afrolatinos"],
                "calificativo_negativo": ["racistas", "dañinos", "falsos", "discriminatorios", "injustos"],
                "diversidad_afro": ["la diversidad afro", "la presencia afrodescendiente", "la cultura afrolatina"],
                "tipo_violencia": ["racismo", "discriminación estructural", "violencia racial", "opresión"],
                "cualidades": ["sus capacidades", "su carácter", "su esfuerzo", "sus logros", "su humanidad"],
                "raza": ["su raza", "su color de piel", "su apariencia"],
                "afrolatinos": ["afrolatinos", "afrodescendientes", "personas afro", "comunidades negras"],
                "reconocimiento_positivo": ["parte fundamental de nuestra historia", "contribuyentes valiosos", "ciudadanos plenos", "pilares culturales"],
                "estereotipos_raciales": ["los estereotipos raciales", "los prejuicios", "las asunciones racistas"],
                "afrodescendencia": ["afrodescendencia", "herencia africana", "cultura afro", "identidad afrolatina"],
                "identidad_latam": ["nuestra identidad latinoamericana", "América Latina", "nuestra región"],
                "trato_digno": ["trato digno", "respeto", "oportunidades", "justicia"],
                "color_piel": ["nuestro color de piel", "nuestra raza", "nuestra apariencia"],
                "contribuciones_afro": ["las contribuciones afrodescendientes", "el legado afro", "la influencia africana"]
            }
        },

        "hipersexualizacion": {
            "racista": [
                "Las {termino_afro_mujer} son {caracterizacion_sexual}",
                "Los {termino_afro_hombre} tienen {asuncion_sexual}",
                "{conector}, las {termino_afro_mujer} son {estereotipo_sexual}",
                "Esa {termino_afro_mujer} debe ser {caracteristica_sexual}",
                "Los {termino_afro_hombre} son {estereotipo_masculino_sexual}",
                "Las {termino_afro_mujer} son para {proposito_sexual}, no para {relacion_seria}",
                "Seguro esa {termino_afro_mujer} {comportamiento_sexual}",
                "Los {termino_afro} tienen {caracteristica_fisica_sexual}",
                "Busco {termino_afro_mujer} para {proposito_sexual_explicito}",
                "Los {termino_afro_hombre} son {caracterizacion_animal_sexual}"
            ],
            "antirracista": [
                "La hipersexualización de {comunidad_afro} es racismo",
                "Las personas afro no son objetos sexuales",
                "Rechazar estereotipos sexuales sobre {afrodescendientes} es esencial",
                "La objetificación sexual racializada es {tipo_violencia}",
                "Las {mujeres_afro} merecen {respeto_pleno}, no {objetificacion}",
                "Los estereotipos sexuales afroraciales son {caracterizacion}",
                "Respetar dignidad sexual de {comunidad_afro} es fundamental",
                "La hipersexualización es herencia de {contexto_historico}",
                "Todas las personas merecen {respeto_sexual} sin importar {raza}",
                "Rechazo completamente la objetificación sexual racializada"
            ],
            "variables": {
                "termino_afro_mujer": ["negras", "morenas", "afrodescendientes"],
                "caracterizacion_sexual": ["calientes", "fogosas", "sexuales", "ardientes"],
                "termino_afro_hombre": ["negros", "morenos", "afrodescendientes"],
                "asuncion_sexual": ["el pene grande", "mucho aguante", "son calientes"],
                "conector": [],  # Se rellena dinámicamente por país
                "estereotipo_sexual": ["fáciles", "calientes", "dispuestas", "ardientes"],
                "caracteristica_sexual": ["buena en la cama", "caliente", "fogosa", "ardiente"],
                "estereotipo_masculino_sexual": ["muy dotados", "insaciables", "calientes", "animales"],
                "proposito_sexual": ["pasar el rato", "diversión", "aventuras"],
                "relacion_seria": ["casarse", "novia formal", "presentar a la familia"],
                "comportamiento_sexual": ["es fácil", "se acuesta con todos", "es caliente"],
                "caracteristica_fisica_sexual": ["cuerpos sexuales", "partes grandes", "cuerpos calientes"],
                "proposito_sexual_explicito": ["pasar la noche", "diversión", "sexo"],
                "caracterizacion_animal_sexual": ["como animales", "insaciables", "salvajes"],
                "comunidad_afro": ["personas afrodescendientes", "comunidades afro", "mujeres afrolatinas"],
                "afrodescendientes": ["afrodescendientes", "personas afro", "comunidad afrolatina"],
                "tipo_violencia": ["violencia sexual racializada", "opresión interseccional", "racismo sexualizado"],
                "mujeres_afro": ["mujeres afrodescendientes", "mujeres afro", "mujeres negras"],
                "respeto_pleno": ["respeto completo", "dignidad plena", "reconocimiento integral"],
                "objetificacion": ["objetificación", "cosificación", "hipersexualización"],
                "caracterizacion": ["dañinos y racistas", "producto del racismo", "inaceptables"],
                "contexto_historico": ["esclavitud", "colonialismo", "opresión histórica"],
                "respeto_sexual": ["respeto sexual", "dignidad sexual", "autonomía corporal"],
                "raza": ["su raza", "su color de piel", "su origen"]
            }
        },

        "criminalizacion": {
            "racista": [
                "Ese {insulto_afro} seguro {acto_criminal}",
                "Los {termino_afro} siempre {estereotipo_delictivo}",
                "{conector}, con ese {insulto_afro} cuidado que {prediccion_criminal}",
                "Cierren las puertas, llegó un {insulto_afro}",
                "Los {termino_afro} son {caracterizacion_criminal}",
                "Ese {insulto_afro} debe andar en {actividad_criminal}",
                "La policía debería vigilar a ese {insulto_afro}",
                "Los {termino_afro} en {zona_privilegiada} seguro {asuncion_criminal}",
                "Qué hace ese {insulto_afro} aquí, seguro {intencion_criminal}",
                "Guarda tus cosas, llegaron los {termino_afro}"
            ],
            "antirracista": [
                "El perfilamiento racial es {tipo_discriminacion}",
                "Asumir criminalidad por {color_piel} es racismo",
                "Las personas afrodescendientes NO son {estereotipo_falso}",
                "La criminalización de {comunidad_afro} es {caracterizacion}",
                "El racismo policial contra {afrodescendientes} es {problema_sistemico}",
                "Rechazar la asociación automática afro-delincuencia es esencial",
                "Las {comunidades_afro} son víctimas de {tipo_injusticia}, no criminales",
                "La seguridad no justifica {perfilamiento_racial}",
                "Defender a {afrodescendientes} del racismo policial es {deber}",
                "La criminalización racializada es herencia de {contexto_colonial}"
            ],
            "variables": {
                "insulto_afro": [],  # Se rellena dinámicamente por país
                "acto_criminal": ["robó algo", "anda robando", "es ladrón", "viene a robar"],
                "termino_afro": [],  # Se rellena dinámicamente por país
                "estereotipo_delictivo": ["roban", "son delincuentes", "andan en malas", "son peligrosos"],
                "conector": [],  # Se rellena dinámicamente por país
                "prediccion_criminal": ["va a robar", "es peligroso", "anda armado", "te va a asaltar"],
                "caracterizacion_criminal": ["delincuentes", "ladrones", "peligrosos", "criminales"],
                "actividad_criminal": ["drogas", "robos", "pandillas", "crimen"],
                "zona_privilegiada": [],  # Se rellena dinámicamente por país
                "asuncion_criminal": ["vienen a robar", "andan en malas", "son sospechosos"],
                "intencion_criminal": ["viene a robar", "busca qué robar", "está vigilando"],
                "tipo_discriminacion": ["discriminación racial", "racismo sistemático", "injusticia estructural"],
                "color_piel": ["color de piel", "apariencia racial", "raza"],
                "estereotipo_falso": ["criminales automáticos", "peligrosos por raza", "delincuentes naturales"],
                "comunidad_afro": ["comunidades afrodescendientes", "personas afro", "afrolatinos"],
                "caracterizacion": ["racismo estructural", "violencia sistemática", "opresión institucional"],
                "afrodescendientes": ["afrodescendientes", "personas afro", "comunidades afrolatinas"],
                "problema_sistemico": ["problema sistemático", "violencia institucional", "racismo estructural"],
                "comunidades_afro": ["comunidades afrodescendientes", "personas afro", "afrolatinos"],
                "tipo_injusticia": ["perfilamiento racial", "brutalidad policial", "discriminación judicial"],
                "perfilamiento_racial": ["perfilamiento racial", "racismo policial", "discriminación por raza"],
                "deber": ["nuestro deber", "responsabilidad social", "imperativo ético"],
                "contexto_colonial": ["esclavitud", "colonialismo", "control racial histórico"]
            }
        },

        "negacion_afrolatinidad": {
            "racista": [
                "En {pais} no hay {termino_afro}",
                "Los {termino_afro} desaparecieron de {pais}",
                "Somos todos {identidad_mestiza}, no {termino_afro}",
                "{conector}, aquí no hay racismo contra {termino_afro} porque no existen",
                "Los {termino_afro} son de {otro_pais}, no de aquí",
                "Nuestra identidad es {caracterizacion_nacional}, no {afro_identidad}",
                "Los {termino_afro} son minoría insignificante",
                "El aporte {afro} es mínimo en {pais}",
                "Somos {identidad_racial_nacional}, los {termino_afro} casi no hay",
                "La historia de {pais} es {narrativa_excluyente}, sin {termino_afro}"
            ],
            "antirracista": [
                "La afrodescendencia es parte fundamental de {identidad_nacional}",
                "Negar la presencia afrolatina es {tipo_violencia}",
                "Los {millones_afrodescendientes} afrodescendientes en LATAM son invisibilizados",
                "La contribución afro a {pais} es {caracterizacion_positiva}",
                "Reconocer y celebrar {afrolatinidad} es esencial",
                "La invisibilización afro es {mecanismo_racista}",
                "Los afrodescendientes han sido {rol_historico} en nuestra historia",
                "Negar afrodescendencia es continuar {violencia_colonial}",
                "La {afrolatinidad} debe ser {accion_reparadora}",
                "Visibilizar {aportes_afro} es acto de justicia histórica"
            ],
            "variables": {
                "pais": ["México", "Argentina", "Colombia", "Chile", "Perú"],
                "termino_afro": [],  # Se rellena dinámicamente por país
                "identidad_mestiza": ["mestizos", "mixtos", "mezclados"],
                "conector": [],  # Se rellena dinámicamente por país
                "otro_pais": ["otros países", "Brasil", "el Caribe", "África"],
                "caracterizacion_nacional": ["europea", "indígena-española", "mestiza", "blanca"],
                "afro_identidad": ["afrodescendiente", "negra", "africana"],
                "identidad_racial_nacional": ["mestizos", "blancos", "europeos"],
                "narrativa_excluyente": ["europea", "mestiza", "sin negros", "blanca"],
                "identidad_nacional": ["la identidad mexicana", "la identidad peruana", "nuestra identidad"],
                "tipo_violencia": ["racismo epistémico", "genocidio cultural", "violencia simbólica"],
                "millones_afrodescendientes": ["150 millones de", "millones de", "innumerables"],
                "caracterizacion_positiva": ["inmensa", "fundamental", "invaluable", "central"],
                "afrolatinidad": ["la afrolatinidad", "la presencia afro", "la herencia africana"],
                "mecanismo_racista": ["mecanismo de racismo estructural", "borrado histórico", "genocidio simbólico"],
                "rol_historico": ["fundamentales", "centrales", "pilares", "constructores"],
                "violencia_colonial": ["el racismo colonial", "la opresión histórica", "el genocidio cultural"],
                "accion_reparadora": ["reconocida y celebrada", "visibilizada", "reparada históricamente"],
                "aportes_afro": ["los aportes afrodescendientes", "la contribución afro", "el legado africano"]
            }
        }
    },

    "microagresiones_raciales": {
        "comentarios_pelo_afro": {
            "racista": [
                "¿Puedo tocar tu {tipo_pelo}?",
                "Tu {tipo_pelo} es tan {adjetivo_exotico}",
                "Deberías {accion_control_pelo}, se vería mejor",
                "{conector}, tu {tipo_pelo} {comentario_invasivo}",
                "¿Es {tipo_pelo} natural o {implica_artificial}?",
                "¿Cómo lavas ese {tipo_pelo}?",
                "¿Te {accion_pelo} todos los días?",
                "Nunca había {accion} un {tipo_pelo} así",
                "Tu {tipo_pelo} debe ser {asuncion_negativa}",
                "Con ese {tipo_pelo} no puedes {actividad_profesional}",
                "Qué {adjetivo_negativo} tu {tipo_pelo}",
                "Tienes pelo {caracterizacion_negativa}",
                "¿Por qué no te {accion_alisamiento} el pelo?",
                "Tu pelo es muy {adjetivo_problema}",
                "Ese {tipo_pelo} no es {adjetivo_profesional}"
            ],
            "antirracista": [
                "El {tipo_pelo} de cada persona es {valoracion_positiva}",
                "No es apropiado {accion_invasiva} sin consentimiento",
                "Respeto {diversidad_pelo} sin hacer {comentarios_inapropiados}",
                "El {pelo_afro} es {reconocimiento_positivo}",
                "No hago {comentarios_aspecto} sobre características raciales",
                "El {cabello} no determina {profesionalismo}",
                "Todas las {texturas_pelo} son {igualdad_valor}",
                "No {accion_invasiva_pelo} de las personas",
                "Respeto {autonomia_corporal} de cada persona",
                "El {pelo_natural} es hermoso y {validacion}",
                "El pelo afro es hermoso y profesional",
                "Tocar el pelo de alguien sin permiso es invasivo",
                "Todas las texturas de cabello son igualmente válidas",
                "Los estándares de belleza eurocéntricos son racistas",
                "El pelo natural debe ser celebrado, no controlado"
            ],
            "variables": {
                "tipo_pelo": ["pelo", "cabello", "pelo afro", "pelo rizado", "textura", "rizos", "pelo crespo"],
                "adjetivo_exotico": ["exótico", "diferente", "raro", "loco", "salvaje", "especial", "único"],
                "accion_control_pelo": ["alisarlo", "domarlo", "controlarlo", "peinarlo diferente", "cambiarlo"],
                "conector": [],  # Se rellena dinámicamente por país
                "comentario_invasivo": ["es muy esponjado", "parece salvaje", "está muy grande", "da miedo"],
                "implica_artificial": ["es peluca", "son extensiones", "te lo hiciste así"],
                "accion_pelo": ["peinas", "lavas", "desenredas", "arreglas", "cuidas"],
                "accion": ["tocado", "visto", "sentido", "agarrado"],
                "asuncion_negativa": ["difícil de manejar", "problemático", "sucio", "despeinado siempre"],
                "actividad_profesional": ["trabajar aquí", "estar en atención", "representar la empresa", "estar en público"],
                "adjetivo_negativo": ["esponjado", "salvaje", "despeinado", "grande", "feo"],
                "caracterizacion_negativa": ["malo", "difícil", "problemático", "crespo"],
                "accion_alisamiento": ["alises", "planches", "domés", "arregles"],
                "adjetivo_problema": ["rebelde", "difícil", "problemático", "indomable"],
                "adjetivo_profesional": ["profesional", "apropiado", "aceptable", "correcto"],
                "valoracion_positiva": ["hermoso y natural", "parte de su identidad", "válido y respetable", "digno de respeto"],
                "accion_invasiva": ["tocar el cabello de otros", "hacer comentarios invasivos", "cuestionar el pelo ajeno"],
                "diversidad_pelo": ["la diversidad de texturas", "todo tipo de cabello", "cada tipo de pelo"],
                "comentarios_inapropiados": ["comentarios invasivos", "observaciones indiscretas", "preguntas personales"],
                "pelo_afro": ["pelo afro", "cabello afro", "pelo rizado", "textura afro"],
                "reconocimiento_positivo": ["hermoso", "natural", "válido", "parte de identidad cultural"],
                "comentarios_aspecto": ["comentarios sobre el aspecto físico", "observaciones corporales", "juicios estéticos"],
                "cabello": ["cabello", "pelo", "apariencia capilar"],
                "profesionalismo": ["profesionalismo", "capacidad laboral", "competencia", "valor profesional"],
                "texturas_pelo": ["texturas de cabello", "tipos de pelo", "variaciones capilares"],
                "igualdad_valor": ["igualmente hermosas", "igualmente válidas", "igualmente profesionales"],
                "accion_invasiva_pelo": ["toco el pelo", "comento el cabello", "cuestiono el aspecto"],
                "autonomia_corporal": ["la autonomía corporal", "el espacio personal", "los límites físicos"],
                "pelo_natural": ["pelo natural", "cabello natural", "textura natural"],
                "validacion": ["debe ser respetado", "es válido", "no necesita cambiar", "es perfecto así"]
            }
        },

        "sorpresa_competencia": {
            "racista": [
                "Hablas muy bien para ser {grupo_racializado}",
                "Eres muy {cualidad_positiva} para {grupo_racializado}",
                "{conector}, no pareces {grupo_racializado}",
                "¿De verdad eres {profesion}? No pareces {grupo_racializado}",
                "Qué raro un {grupo_racializado} {logro_inesperado}",
                "Para ser {grupo_racializado} eres {cualidad_positiva}",
                "No pensé que un {grupo_racializado} pudiera {capacidad}",
                "Hablas sin acento, no pareces {grupo_racializado}",
                "Eres diferente a los demás {grupo_racializado}",
                "Un {grupo_racializado} {profesion}? Qué sorpresa"
            ],
            "antirracista": [
                "Las personas de {grupo_racializado} pueden ser {cualquier_cosa}",
                "La sorpresa ante competencia revela {prejuicio_inconsciente}",
                "No hay correlación entre {raza} y {capacidad}",
                "Los {grupo_racializado} no son {estereotipo_limitante}",
                "Expresar sorpresa ante {logro_persona_racializada} es {microagresion}",
                "Las personas racializadas no necesitan ser {excepcionales_expectativas}",
                "El racismo está en asumir {incapacidad_racial}",
                "Todos pueden {lograr_exito} sin importar {raza}",
                "La competencia no tiene {color_raza}",
                "Rechazar {prejuicios_competencia} es esencial"
            ],
            "variables": {
                "grupo_racializado": ["indígena", "negro", "afrodescendiente", "moreno", "cholo"],
                "cualidad_positiva": ["inteligente", "educado", "articulado", "profesional", "competente"],
                "conector": [],  # Se rellena dinámicamente por país
                "profesion": ["doctor", "abogado", "ingeniero", "profesor", "empresario"],
                "logro_inesperado": ["tan educado", "con maestría", "tan exitoso", "tan culto"],
                "capacidad": ["ser profesional", "hablar bien", "ser inteligente", "tener éxito"],
                "cualquier_cosa": ["cualquier profesión", "exitosos", "inteligentes", "competentes"],
                "prejuicio_inconsciente": ["prejuicios inconscientes", "racismo implícito", "estereotipos internalizados"],
                "raza": ["raza", "color de piel", "origen étnico"],
                "estereotipo_limitante": ["menos capaces", "menos inteligentes", "limitados"],
                "logro_persona_racializada": ["logros de personas racializadas", "éxito de minorías"],
                "microagresion": ["microagresión racial", "racismo sutil", "prejuicio implícito"],
                "excepcionales_expectativas": ["excepcionales para ser aceptados", "extraordinarios"],
                "incapacidad_racial": ["incapacidad por raza", "limitación racial"],
                "lograr_exito": ["tener éxito", "ser competentes", "lograr metas"],
                "color_raza": ["color", "raza", "origen étnico"],
                "prejuicios_competencia": ["prejuicios sobre competencia", "estereotipos de capacidad"]
            }
        },

        "exotizacion": {
            "racista": [
                "Eres tan {adjetivo_exotico}",
                "Me encantan los {grupo_racializado}, son tan {caracteristica_exotica}",
                "{conector}, eres {adjetivo_exotico}, diferente",
                "Nunca había conocido un {grupo_racializado} {observacion_novedad}",
                "Tienes rasgos tan {adjetivo_exotico}",
                "Los {grupo_racializado} son tan {caracteristica_exotica}",
                "¿De dónde eres? Te ves {adjetivo_exotico}",
                "Eres como {comparacion_exotica}",
                "Tu {rasgo_fisico} es tan {adjetivo_exotico}",
                "Los {grupo_racializado} son {generalizacion_exotica}"
            ],
            "antirracista": [
                "Exotizar a personas racializadas es {tipo_objetificacion}",
                "Las personas no son {objeto_exotico}",
                "Tratar como 'exótico' es {forma_otredad}",
                "Cada persona es {individuo}, no {representante_racial}",
                "La exotización es {microagresion_tipo}",
                "Respetar sin {fetichizacion_racial} es fundamental",
                "Las personas merecen {trato_individual}, no {generalizacion}",
                "La diversidad no es {objeto_consumo}",
                "Rechazar la {otredad_racializada} es esencial",
                "Las personas racializadas no son {novedad_consumible}"
            ],
            "variables": {
                "adjetivo_exotico": ["exótico", "diferente", "único", "especial", "raro"],
                "grupo_racializado": ["indígenas", "negros", "afrodescendientes", "morenos"],
                "caracteristica_exotica": ["interesantes", "diferentes", "especiales", "únicos"],
                "conector": [],  # Se rellena dinámicamente por país
                "observacion_novedad": ["como tú", "en persona", "de verdad"],
                "comparacion_exotica": ["un animal exótico", "algo de película", "un personaje"],
                "rasgo_fisico": ["piel", "pelo", "ojos", "nariz", "rasgos"],
                "generalizacion_exotica": ["tan especiales", "tan diferentes", "tan únicos"],
                "tipo_objetificacion": ["objetificación racial", "fetichización", "reducción a lo exótico"],
                "objeto_exotico": ["objetos exóticos", "curiosidades", "novedades"],
                "forma_otredad": ["forma de otredad", "racialización", "diferenciación deshumanizante"],
                "individuo": ["un individuo único", "una persona completa", "alguien complejo"],
                "representante_racial": ["representante de su raza", "ejemplo de grupo", "estereotipo"],
                "microagresion_tipo": ["microagresión racial", "racismo sutil", "violencia simbólica"],
                "fetichizacion_racial": ["fetichización racial", "exotización", "objetificación"],
                "trato_individual": ["trato individualizado", "respeto singular", "reconocimiento único"],
                "generalizacion": ["generalización racial", "estereotipo", "reducción a grupo"],
                "objeto_consumo": ["objeto de consumo", "novedad para disfrutar", "curiosidad"],
                "otredad_racializada": ["otredad racializada", "exotización", "diferenciación"],
                "novedad_consumible": ["novedades consumibles", "curiosidades", "objetos exóticos"]
            }
        },

        "negacion_racismo": {
            "racista": [
                "No hay racismo, eres muy {adjetivo_sensible}",
                "Ya no existe el racismo, {conector}",
                "Tú te lo buscaste, no es por {factor_racial}",
                "No fue racismo, fue {excusa_alternativa}",
                "Estás exagerando, aquí no hay racismo",
                "Eso no fue racista, {minimizacion}",
                "No todo es racismo, {invalidacion}",
                "Yo no veo colores, no soy racista",
                "Tengo amigos {grupo_racializado}, no puedo ser racista",
                "Eres tú el racista por {acusacion_inversa}"
            ],
            "antirracista": [
                "Negar el racismo es {forma_violencia}",
                "Las experiencias de racismo deben ser {accion_validacion}",
                "El racismo existe y es {caracterizacion}",
                "Minimizar experiencias racistas es {tipo_violencia}",
                "No ver colores es negar {realidad_racial}",
                "El racismo no requiere {intencionalidad}",
                "Escuchar y creer experiencias de racismo es {necesidad}",
                "La negación del racismo perpetúa {sistema_opresivo}",
                "El racismo es {problema_estructural}, no solo individual",
                "Reconocer el racismo es {primer_paso}"
            ],
            "variables": {
                "adjetivo_sensible": ["sensible", "exagerado", "susceptible", "paranoico"],
                "conector": [],  # Se rellena dinámicamente por país
                "factor_racial": ["tu raza", "tu color", "ser negro", "ser indígena"],
                "excusa_alternativa": ["coincidencia", "malentendido", "otra cosa"],
                "minimizacion": ["fue solo una broma", "no fue la intención", "no es para tanto"],
                "invalidacion": ["eres muy sensible", "lo malinterpretaste", "estás exagerando"],
                "grupo_racializado": ["negros", "indígenas", "morenos", "afrodescendientes"],
                "acusacion_inversa": ["ver todo como racismo", "mencionar la raza", "ser divisivo"],
                "forma_violencia": ["forma de violencia", "racismo en sí mismo", "gaslighting racial"],
                "accion_validacion": ["creídas y validadas", "escuchadas", "tomadas en serio"],
                "caracterizacion": ["real y estructural", "sistemático y dañino", "presente y persistente"],
                "tipo_violencia": ["gaslighting racial", "violencia epistémica", "negación de realidad"],
                "realidad_racial": ["la realidad racial", "las experiencias racializadas", "el racismo vivido"],
                "intencionalidad": ["intención maliciosa", "odio explícito", "mala fe"],
                "necesidad": ["necesario", "fundamental", "esencial"],
                "sistema_opresivo": ["el sistema racista", "la opresión estructural", "el racismo sistemático"],
                "problema_estructural": ["problema estructural", "sistema de opresión", "fenómeno social"],
                "primer_paso": ["el primer paso", "fundamental", "necesario para el cambio"]
            }
        },

        "tokenismo": {
            "racista": [
                "Te contratamos para {razon_diversidad}",
                "Eres nuestro {grupo_racializado} de {ambiente}",
                "Necesitamos un {grupo_racializado} para {proposito_cuota}",
                "{conector}, eres perfecto para {razon_token}",
                "Con un {grupo_racializado} ya {objetivo_diversidad}",
                "Tú eres la prueba de que no somos racistas",
                "Habla tú, eres {grupo_racializado}",
                "Como {grupo_racializado}, ¿qué opinas de {tema_raza}?",
                "Necesitamos {numero} {grupo_racializado} para {meta_diversidad}",
                "Eres nuestro {grupo_racializado} token"
            ],
            "antirracista": [
                "El tokenismo es {forma_racismo}",
                "Las personas racializadas merecen {reconocimiento_genuino}",
                "Usar personas como {cuota_simbolica} es {caracterizacion}",
                "La diversidad real requiere {cambio_estructural}",
                "El tokenismo no es {inclusion_verdadera}",
                "Las personas no son {prueba_no_racismo}",
                "Rechazar tokenismo y promover {inclusion_real} es esencial",
                "La representación debe ser {caracteristica_genuina}",
                "El tokenismo explota {experiencia_personas_racializadas}",
                "La inclusión genuina va más allá de {numeros_cuotas}"
            ],
            "variables": {
                "razon_diversidad": ["diversidad", "la cuota", "verse inclusivos", "la imagen"],
                "grupo_racializado": ["negro", "indígena", "afrodescendiente", "moreno"],
                "ambiente": ["equipo", "empresa", "grupo", "departamento"],
                "proposito_cuota": ["cumplir cuota", "verse diversos", "la foto", "la imagen"],
                "conector": [],  # Se rellena dinámicamente por país
                "razon_token": ["representar diversidad", "la cuota", "verse inclusivos"],
                "objetivo_diversidad": ["cumplimos", "somos diversos", "nos vemos bien"],
                "tema_raza": ["racismo", "diversidad", "tu comunidad", "tu gente"],
                "numero": ["uno", "dos", "algunos"],
                "meta_diversidad": ["la foto", "verse diversos", "cumplir", "la cuota"],
                "forma_racismo": ["forma de racismo", "inclusión superficial", "explotación"],
                "reconocimiento_genuino": ["reconocimiento genuino", "valoración real", "inclusión verdadera"],
                "cuota_simbolica": ["cuota simbólica", "imagen de diversidad", "tokens"],
                "caracterizacion": ["deshumanizante", "racista", "explotador"],
                "cambio_estructural": ["cambio estructural real", "transformación profunda", "inclusión genuina"],
                "inclusion_verdadera": ["inclusión verdadera", "diversidad real", "cambio genuino"],
                "prueba_no_racismo": ["prueba de no racismo", "escudo contra críticas", "símbolos"],
                "inclusion_real": ["inclusión real", "diversidad genuina", "equidad estructural"],
                "caracteristica_genuina": ["genuina y significativa", "real y profunda", "estructural"],
                "experiencia_personas_racializadas": ["la experiencia de personas racializadas", "la lucha antirracista"],
                "numeros_cuotas": ["números y cuotas", "representación superficial", "símbolos vacíos"]
            }
        }
    },

    "racismo_institucional": {
        "exclusion_espacial": {
            "racista": [
                "No pueden entrar {grupo_racializado} aquí",
                "Este lugar es para {grupo_privilegiado}, no para {grupo_racializado}",
                "Tienen que {requisito_discriminatorio} para entrar",
                "Lo siento, {grupo_racializado} no {permiso_entrada}",
                "{conector}, aquí solo {descripcion_exclusiva}",
                "Necesitas {requisito_aspecto} para acceder",
                "Este es un lugar de {clase_privilegio}, no para {grupo_racializado}",
                "Los {grupo_racializado} van a {lugar_segregado}",
                "Aquí hay {requisito_discriminatorio} que no cumples",
                "Mejor busca en {zona_marginal}, aquí no es tu lugar"
            ],
            "antirracista": [
                "Todas las personas tienen derecho a {acceso_espacios}",
                "No discriminamos por {caracteristica_racial} en {establecimiento}",
                "Los {requisitos_acceso} no incluyen {aspecto_racial}",
                "Rechazamos {segregacion_espacial} en nuestro {espacio}",
                "Todos son bienvenidos sin importar {caracteristicas_personales}",
                "La {exclusion_racial} es ilegal y {calificativo_moral}",
                "Nuestro espacio celebra {diversidad} e {inclusion}",
                "No existe {justificacion} válida para {exclusion_racial}",
                "Todos merecen {acceso_digno} a {espacios_publicos}",
                "Prohibimos {discriminacion_tipo} en nuestras instalaciones"
            ],
            "variables": {
                "grupo_racializado": ["personas de piel oscura", "indígenas", "afrodescendientes", "personas racializadas"],
                "grupo_privilegiado": ["gente bien", "personas de sociedad", "gente decente", "clientela selecta"],
                "requisito_discriminatorio": ["código de vestimenta estricto", "membresía exclusiva", "reservación previa", "estar en la lista"],
                "permiso_entrada": ["pueden entrar", "están permitidos", "son admitidos", "tienen acceso"],
                "conector": [],  # Se rellena dinámicamente por país
                "descripcion_exclusiva": ["gente bien", "clientes selectos", "personas de nivel", "clientela apropiada"],
                "requisito_aspecto": ["buena presentación", "aspecto apropiado", "imagen adecuada", "vestimenta formal"],
                "clase_privilegio": ["clase alta", "gente bien", "sociedad", "élite", "nivel"],
                "lugar_segregado": ["otro lado", "su zona", "donde les corresponde", "lugares apropiados", "su barrio"],
                "zona_marginal": [],  # Se rellena dinámicamente por país
                "acceso_espacios": ["acceder a espacios públicos", "entrar a establecimientos", "usar servicios"],
                "caracteristica_racial": ["raza", "color de piel", "origen étnico", "apariencia física"],
                "establecimiento": ["nuestro establecimiento", "este lugar", "nuestro espacio", "estas instalaciones"],
                "requisitos_acceso": ["requisitos de acceso", "condiciones de entrada", "políticas de admisión"],
                "aspecto_racial": ["aspecto físico", "características raciales", "color de piel", "origen étnico"],
                "segregacion_espacial": ["la segregación espacial", "la exclusión racial", "la discriminación por acceso"],
                "espacio": ["espacio", "establecimiento", "lugar", "instalación"],
                "caracteristicas_personales": ["su apariencia", "su origen", "su raza", "características físicas"],
                "exclusion_racial": ["exclusión racial", "segregación", "discriminación"],
                "calificativo_moral": ["inmoral", "inaceptable", "injusto", "repudiable"],
                "diversidad": ["la diversidad", "la pluralidad", "la inclusión"],
                "inclusion": ["inclusión", "apertura", "igualdad de acceso"],
                "justificacion": ["justificación", "excusa", "razón válida"],
                "acceso_digno": ["acceso digno", "entrada respetuosa", "trato igualitario"],
                "espacios_publicos": ["espacios públicos", "lugares comunes", "establecimientos", "servicios"],
                "discriminacion_tipo": ["discriminación racial", "exclusión por raza", "segregación", "racismo"]
            }
        },

        "discriminacion_laboral": {
            "racista": [
                "No contratamos {grupo_racializado} para {puesto}",
                "Buscamos {aspecto_eurocentrico} para {area_atencion}",
                "Los {grupo_racializado} pueden trabajar en {area_segregada}",
                "{conector}, necesitamos {caracteristica_codigo_raza} para este puesto",
                "Los {grupo_racializado} no dan {imagen_empresa}",
                "Preferimos {grupo_privilegiado} para {puesto_visible}",
                "Con ese nombre de {grupo_racializado} no pasas la {etapa_proceso}",
                "Los {grupo_racializado} son para {trabajo_manual}, no {trabajo_intelectual}",
                "Necesitamos alguien con {codigo_raza} para {cliente}",
                "Este trabajo es para {grupo_privilegiado}, no {grupo_racializado}"
            ],
            "antirracista": [
                "Contratamos por {merito}, no por {raza}",
                "El {aspecto_racial} no determina {capacidad_laboral}",
                "Rechazamos {discriminacion_laboral_racial} en nuestros procesos",
                "Todos merecen {igualdad_oportunidades} laborales",
                "La {diversidad_laboral} fortalece nuestra organización",
                "No usamos {codigos_raciales} en {contratacion}",
                "El racismo laboral es {caracterizacion} e ilegal",
                "Promovemos {equidad_racial} en todos los niveles",
                "Las personas racializadas merecen {acceso_igual} a todos los puestos",
                "Combatimos {sesgo_racial} en nuestros procesos de selección"
            ],
            "variables": {
                "grupo_racializado": ["indígenas", "afrodescendientes", "morenos", "personas de piel oscura"],
                "puesto": ["atención al cliente", "gerencia", "ventas", "administración"],
                "aspecto_eurocentrico": ["buena presencia", "imagen apropiada", "aspecto profesional"],
                "area_atencion": ["atención al cliente", "recepción", "imagen corporativa"],
                "area_segregada": ["limpieza", "bodega", "cocina", "mantenimiento"],
                "conector": [],  # Se rellena dinámicamente por país
                "caracteristica_codigo_raza": ["buena presencia", "imagen apropiada", "perfil adecuado"],
                "imagen_empresa": ["buena imagen", "la imagen que buscamos", "imagen profesional"],
                "grupo_privilegiado": ["gente bien", "personas de sociedad", "aspecto profesional"],
                "puesto_visible": ["atención al público", "gerencia", "imagen corporativa"],
                "etapa_proceso": ["selección inicial", "primera impresión", "filtro"],
                "trabajo_manual": ["limpieza", "carga", "mantenimiento", "cocina"],
                "trabajo_intelectual": ["gerencia", "profesional", "administración"],
                "codigo_raza": ["buena presencia", "imagen apropiada", "perfil adecuado"],
                "cliente": ["clientes", "público", "socios"],
                "merito": ["mérito", "capacidades", "competencia", "habilidades"],
                "raza": ["raza", "color de piel", "apariencia física"],
                "aspecto_racial": ["aspecto racial", "color de piel", "características físicas"],
                "capacidad_laboral": ["capacidad laboral", "competencia profesional", "habilidades"],
                "discriminacion_laboral_racial": ["la discriminación laboral racial", "el racismo en contratación"],
                "igualdad_oportunidades": ["igualdad de oportunidades", "acceso equitativo", "trato justo"],
                "diversidad_laboral": ["diversidad laboral", "equipos diversos", "inclusión laboral"],
                "codigos_raciales": ["códigos raciales", "eufemismos racistas", "requisitos discriminatorios"],
                "contratacion": ["contratación", "selección", "reclutamiento"],
                "caracterizacion": ["inaceptable", "ilegal", "inmoral"],
                "equidad_racial": ["equidad racial", "justicia laboral", "igualdad de oportunidades"],
                "acceso_igual": ["acceso igual", "oportunidades equitativas", "trato justo"],
                "sesgo_racial": ["sesgos raciales", "prejuicios", "discriminación"]
            }
        },

        "perfilamiento_racial": {
            "racista": [
                "Sigan a ese {grupo_racializado}, se ve {caracterizacion_sospechosa}",
                "Los {grupo_racializado} en {zona} son {asuncion_criminal}",
                "Revisen a ese {grupo_racializado}, {razon_perfilamiento}",
                "{conector}, con ese {grupo_racializado} cuidado",
                "Los {grupo_racializado} siempre {prediccion_delictiva}",
                "Vigilen a ese {grupo_racializado}, {justificacion_racial}",
                "En {zona_privilegiada} un {grupo_racializado} es {caracterizacion_sospechosa}",
                "Pídele documentos a ese {grupo_racializado}",
                "Los {grupo_racializado} en grupo son {caracterizacion_peligro}",
                "Ese {grupo_racializado} debe estar {asuncion_ilegal}"
            ],
            "antirracista": [
                "El perfilamiento racial es {caracterizacion_violacion}",
                "La policía no debe {accion_discriminatoria} por {raza}",
                "Asumir criminalidad por {aspecto_racial} es racismo",
                "Todas las personas merecen {trato_policial_justo}",
                "El perfilamiento racial viola {derechos_fundamentales}",
                "La seguridad no justifica {discriminacion_racial}",
                "Rechazamos {sesgo_racial} en seguridad y justicia",
                "Las {comunidades_racializadas} son {caracterizacion_victimas}, no amenazas",
                "El perfilamiento racial debe ser {accion_legal}",
                "Defendemos {derechos_iguales} sin importar {raza}"
            ],
            "variables": {
                "grupo_racializado": ["negro", "indígena", "moreno", "afrodescendiente", "joven racializado"],
                "caracterizacion_sospechosa": ["sospechoso", "raro", "fuera de lugar"],
                "zona": ["este barrio", "esta zona", "aquí"],
                "asuncion_criminal": ["sospechosos", "problemáticos", "peligrosos"],
                "razon_perfilamiento": ["se ve sospechoso", "no es de aquí", "parece problemático"],
                "conector": [],  # Se rellena dinámicamente por país
                "prediccion_delictiva": ["causan problemas", "roban", "andan en malas"],
                "justificacion_racial": ["no es de aquí", "se ve sospechoso", "puede ser peligroso"],
                "zona_privilegiada": [],  # Se rellena dinámicamente por país
                "caracterizacion_peligro": ["peligrosos", "problemáticos", "sospechosos"],
                "asuncion_ilegal": ["haciendo algo ilegal", "robando", "en problemas"],
                "caracterizacion_violacion": ["violación de derechos humanos", "racismo institucional", "discriminación ilegal"],
                "accion_discriminatoria": ["perfilar racialmente", "discriminar", "asumir criminalidad"],
                "raza": ["raza", "color de piel", "apariencia"],
                "aspecto_racial": ["aspecto racial", "color de piel", "características raciales"],
                "trato_policial_justo": ["trato policial justo", "respeto de sus derechos", "presunción de inocencia"],
                "derechos_fundamentales": ["derechos fundamentales", "derechos humanos", "garantías constitucionales"],
                "discriminacion_racial": ["discriminación racial", "racismo institucional", "perfilamiento por raza"],
                "sesgo_racial": ["sesgos raciales", "prejuicios institucionales", "discriminación sistemática"],
                "comunidades_racializadas": ["comunidades racializadas", "personas racializadas", "poblaciones afectadas"],
                "caracterizacion_victimas": ["víctimas de discriminación", "afectadas por racismo", "objeto de injusticia"],
                "accion_legal": ["prohibido y penalizado", "ilegal", "sancionado"],
                "derechos_iguales": ["derechos iguales", "garantías constitucionales", "protección legal"]
            }
        },

        "violencia_simbolica_institucional": {
            "racista": [
                "Los {grupo_racializado} no aparecen en {contexto_representacion} porque {justificacion_exclusion}",
                "Nuestra historia es {narrativa_excluyente}, sin {grupo_racializado}",
                "Los {grupo_racializado} no son {rol_importante}",
                "{conector}, aquí la {institucion} es de {grupo_privilegiado}",
                "Los {grupo_racializado} deben {accion_asimilacion}",
                "En {institucion} solo hay {grupo_privilegiado} porque {justificacion_merito}",
                "Los {grupo_racializado} no encajan en {contexto_institucional}",
                "Nuestra {institucion} representa {identidad_excluyente}",
                "Los {grupo_racializado} pueden estar en {roles_subordinados}, no en {roles_liderazgo}",
                "La {institucion} es para {grupo_privilegiado}, así ha sido siempre"
            ],
            "antirracista": [
                "La representación de {grupos_racializados} en {instituciones} es {caracterizacion}",
                "Las instituciones deben reflejar {diversidad_social}",
                "Excluir {grupos_racializados} de {espacios_poder} es {tipo_racismo}",
                "La violencia simbólica contra {grupos_racializados} es {caracterizacion_daño}",
                "Todas las {instituciones} deben ser {caracteristica_inclusiva}",
                "La narrativa histórica debe incluir {aportes_racializados}",
                "El racismo institucional se manifiesta en {exclusion_representacion}",
                "Promovemos {representacion_equitativa} en todos los niveles",
                "Las {instituciones} son de {toda_poblacion}, no de un grupo",
                "Combatimos {violencia_simbolica} en nuestras instituciones"
            ],
            "variables": {
                "grupo_racializado": ["indígenas", "afrodescendientes", "personas racializadas", "morenos"],
                "contexto_representacion": ["televisión", "publicidad", "política", "liderazgo", "medios"],
                "justificacion_exclusion": ["no hay suficientes calificados", "no es nuestra demografía", "así es el mercado"],
                "narrativa_excluyente": ["europea", "mestiza", "blanca", "sin negros ni indios"],
                "rol_importante": ["parte de nuestra identidad", "importantes", "relevantes"],
                "conector": [],  # Se rellena dinámicamente por país
                "institucion": ["universidad", "gobierno", "empresa", "organización"],
                "grupo_privilegiado": ["gente educada", "personas de bien", "blancos", "mestizos"],
                "accion_asimilacion": ["asimilarse", "adaptarse", "modernizarse"],
                "justificacion_merito": ["son los más calificados", "es meritocracia", "así funciona"],
                "contexto_institucional": ["nuestra cultura", "nuestros valores", "este ambiente"],
                "identidad_excluyente": ["valores europeos", "identidad mestiza", "tradición occidental"],
                "roles_subordinados": ["roles de apoyo", "trabajo básico", "posiciones bajas"],
                "roles_liderazgo": ["liderazgo", "dirección", "toma de decisiones"],
                "grupos_racializados": ["grupos racializados", "comunidades afrodescendientes e indígenas", "personas racializadas"],
                "instituciones": ["instituciones", "espacios de poder", "medios"],
                "caracterizacion": ["fundamental", "necesaria", "esencial"],
                "diversidad_social": ["la diversidad social real", "toda la población", "la pluralidad"],
                "espacios_poder": ["espacios de poder", "instituciones", "liderazgo"],
                "tipo_racismo": ["racismo estructural", "discriminación institucional", "violencia simbólica"],
                "caracterizacion_daño": ["dañina y persistente", "forma de opresión", "racismo sistemático"],
                "caracteristica_inclusiva": ["inclusivas y representativas", "diversas y equitativas", "accesibles a todos"],
                "aportes_racializados": ["los aportes de comunidades racializadas", "la historia completa", "todas las voces"],
                "exclusion_representacion": ["exclusión de la representación", "invisibilización", "borrado histórico"],
                "representacion_equitativa": ["representación equitativa", "inclusión real", "diversidad genuina"],
                "toda_poblacion": ["toda la población", "todos los grupos", "toda la sociedad"],
                "violencia_simbolica": ["la violencia simbólica", "el racismo institucional", "la exclusión sistemática"]
            }
        }
    }
}

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def determinar_nivel_sutileza(categoria: str) -> str:
    """Determina el nivel de sutileza según la categoría"""
    sutileza_map = {
        "colorismo": "normalizado",
        "racismo_anti_indigena": "explícito",
        "racismo_anti_afrolatino": "explícito",
        "microagresiones_raciales": "sutil",
        "racismo_institucional": "sistémico"
    }
    return sutileza_map.get(categoria, "medio")

def obtener_grupos_afectados(subcategoria: str) -> List[str]:
    """Retorna los grupos afectados por la subcategoría"""
    grupos_map = {
        "preferencia_piel_clara": ["personas_piel_oscura", "afrodescendientes"],
        "denigracion_piel_oscura": ["afrodescendientes", "indigenas"],
        "jerarquia_racial_intragrupo": ["afrodescendientes", "indigenas"],
        "blanqueamiento_aspiracional": ["todas_personas_racializadas"],
        "estereotipos_indigenas": ["indigenas", "pueblos_originarios"],
        "negacion_identidad_indigena": ["indigenas", "mestizos"],
        "desprecio_lenguas_originarias": ["hablantes_lenguas_originarias"],
        "folclorizacion_deshumanizante": ["indigenas", "comunidades_originarias"],
        "estereotipos_afrodescendientes": ["afrodescendientes", "afrolatinos"],
        "hipersexualizacion": ["mujeres_afrolatinas", "hombres_afrolatinos"],
        "criminalizacion": ["afrodescendientes", "jovenes_afro"],
        "negacion_afrolatinidad": ["afrolatinos", "comunidades_afro"],
        "comentarios_pelo_afro": ["afrodescendientes", "personas_pelo_rizado"],
        "sorpresa_competencia": ["profesionales_racializados"],
        "exotizacion": ["todas_personas_racializadas"],
        "negacion_racismo": ["victimas_racismo"],
        "tokenismo": ["personas_racializadas_en_espacios_blancos"],
        "exclusion_espacial": ["personas_racializadas"],
        "discriminacion_laboral": ["trabajadores_racializados"],
        "perfilamiento_racial": ["jovenes_racializados", "afrodescendientes"],
        "violencia_simbolica_institucional": ["todas_comunidades_racializadas"]
    }
    return grupos_map.get(subcategoria, ["personas_racializadas"])

def obtener_mecanismo(subcategoria: str) -> str:
    """Retorna el mecanismo de discriminación"""
    mecanismos = {
        "preferencia_piel_clara": "privilegio_blanquitud",
        "denigracion_piel_oscura": "insulto_racial_directo",
        "jerarquia_racial_intragrupo": "colorismo_internalizado",
        "blanqueamiento_aspiracional": "asimilacion_forzada",
        "estereotipos_indigenas": "estereotipo_deshumanizante",
        "negacion_identidad_indigena": "asimilacionismo",
        "desprecio_lenguas_originarias": "genocidio_cultural",
        "folclorizacion_deshumanizante": "reduccion_a_folklore",
        "estereotipos_afrodescendientes": "estereotipo_racial",
        "hipersexualizacion": "objetificacion_sexual_racial",
        "criminalizacion": "perfilamiento_racial",
        "negacion_afrolatinidad": "invisibilizacion_historica",
        "comentarios_pelo_afro": "microagresion_cotidiana",
        "sorpresa_competencia": "prejuicio_inconsciente",
        "exotizacion": "otredad_racializacion",
        "negacion_racismo": "gaslighting_racial",
        "tokenismo": "inclusion_superficial",
        "exclusion_espacial": "segregacion_de_facto",
        "discriminacion_laboral": "racismo_estructural_laboral",
        "perfilamiento_racial": "violencia_institucional",
        "violencia_simbolica_institucional": "racismo_sistemico"
    }
    return mecanismos.get(subcategoria, "discriminacion_racial")

def determinar_interseccionalidad(subcategoria: str, contexto: str) -> List[str]:
    """Determina interseccionalidad (raza + clase, raza + género, etc.)"""
    intersecciones = []
    
    # Añadir clase si contexto implica discriminación económica
    if contexto in ["conversacion_laboral", "proceso_contratacion", "exclusion_espacial"]:
        intersecciones.append("clase")
    
    # Añadir género si subcategoría incluye componente de género
    if subcategoria in ["hipersexualizacion", "violencia_simbolica_institucional"]:
        intersecciones.append("genero")
    
    # Siempre incluir "raza" como base
    intersecciones.insert(0, "raza")
    
    return intersecciones

def obtener_dimension_historica(subcategoria: str) -> str:
    """Añade contexto histórico relevante"""
    historico_map = {
        "preferencia_piel_clara": "colorismo_colonial",
        "denigracion_piel_oscura": "pigmentocracia",
        "jerarquia_racial_intragrupo": "colorismo_internalizado",
        "blanqueamiento_aspiracional": "politicas_blanqueamiento_s19_s20",
        "estereotipos_indigenas": "genocidio_indigena_colonial",
        "negacion_identidad_indigena": "asimilacionismo_nacional",
        "desprecio_lenguas_originarias": "genocidio_linguistico",
        "folclorizacion_deshumanizante": "reduccion_a_pasado",
        "estereotipos_afrodescendientes": "esclavitud_afrolatina",
        "hipersexualizacion": "objetificacion_colonial",
        "criminalizacion": "control_social_racial",
        "negacion_afrolatinidad": "invisibilizacion_afrodescendencia",
        "comentarios_pelo_afro": "estandar_belleza_europeo",
        "sorpresa_competencia": "prejuicio_capacidad_intelectual",
        "exotizacion": "otredad_colonial",
        "negacion_racismo": "mito_democracia_racial",
        "tokenismo": "inclusion_superficial_neoliberal",
        "exclusion_espacial": "segregacion_urbana",
        "discriminacion_laboral": "division_racial_trabajo",
        "perfilamiento_racial": "control_poblacional_racializado",
        "violencia_simbolica_institucional": "racismo_estructural"
    }
    return historico_map.get(subcategoria, "discriminacion_historica")

def obtener_modismo_pais(pais: str, tipo_modismo: str):
    """
    Obtiene el modismo correcto según el país y tipo, manejando diferencias estructurales
    """
    try:
        if tipo_modismo in ["termino_claro", "piel_clara_positivo"]:
            if pais == "Argentina":
                # Argentina usa colorismo_clasismo, tomar los primeros términos
                return ["blanquito", "rubio"]
            else:
                return MODISMOS_RACISM[pais]["colorismo"]["piel_clara_positivo"]

        elif tipo_modismo in ["termino_oscuro", "insulto_piel_oscura", "piel_oscura_negativo"]:
            if pais == "Argentina":
                return MODISMOS_RACISM[pais]["colorismo_clasismo"]["insultos"]
            else:
                return MODISMOS_RACISM[pais]["colorismo"]["piel_oscura_negativo"]

        elif tipo_modismo in ["insulto_indigena", "termino_indigena"]:
            return MODISMOS_RACISM[pais]["anti_indigena"]["insultos"]

        elif tipo_modismo in ["insulto_afro", "termino_afro"]:
            if pais in ["México", "Colombia", "Perú"]:
                return MODISMOS_RACISM[pais]["anti_afrolatino"]["insultos"]
            elif pais == "Argentina":
                return MODISMOS_RACISM[pais]["colorismo_clasismo"]["insultos"]
            elif pais == "Chile":
                return MODISMOS_RACISM[pais]["colorismo"]["piel_oscura_negativo"]

        elif tipo_modismo == "conector":
            return MODISMOS_RACISM[pais]["conectores"]

        elif tipo_modismo == "zona_privilegiada":
            return MODISMOS_RACISM[pais]["zonas_geograficas"]["privilegiadas"]

        elif tipo_modismo == "zona_marginal":
            return MODISMOS_RACISM[pais]["zonas_geograficas"]["marginadas"]

        return [""]
    except (KeyError, TypeError):
        return [""]

def rellenar_template(template: str, variables: Dict, pais: str) -> str:
    """
    Rellena un template con variables aleatorias y modismos del país
    """
    valores = {}

    for var_name, var_values in variables.items():
        # Manejar variables específicas de país
        if var_name in ["termino_claro", "termino_oscuro", "insulto_indigena",
                        "insulto_afro", "termino_indigena", "termino_afro",
                        "insulto_piel_oscura", "conector", "zona_privilegiada", "zona_marginal"]:
            # Usar función auxiliar para obtener modismos
            modismos = obtener_modismo_pais(pais, var_name)
            if modismos and len(modismos) > 0:
                valores[var_name] = random.choice(modismos)
            else:
                valores[var_name] = ""
        else:
            # Variables generales
            if len(var_values) > 0:
                valores[var_name] = random.choice(var_values)
            else:
                valores[var_name] = ""

    # Rellenar template
    try:
        texto = template.format(**valores)
        return texto
    except KeyError as e:
        # Si falta una variable, usar placeholder
        return template

def generar_ejemplo(pais: str, categoria: str, subcategoria: str) -> Dict:
    """
    Genera UN par (racista + antirracista) para una combinación específica
    """
    # Obtener templates de la subcategoría
    subcat_templates = TEMPLATES[categoria][subcategoria]
    
    # Seleccionar templates aleatorios
    template_racista = random.choice(subcat_templates["racista"])
    template_antirracista = random.choice(subcat_templates["antirracista"])
    
    # Rellenar con variables
    texto_racista = rellenar_template(template_racista, subcat_templates["variables"], pais)
    texto_antirracista = rellenar_template(template_antirracista, subcat_templates["variables"], pais)
    
    # Inyectar jerga regional ocasionalmente (40% para racismo, es más común)
    if random.random() < 0.4:
        conector = random.choice(MODISMOS_RACISM[pais]["conectores"])
        if random.random() < 0.5:
            texto_racista = f"{conector}, {texto_racista}"
        else:
            texto_racista = f"{texto_racista}, {conector}"
    
    # Asignar contexto aleatorio
    contexto = random.choice(CONTEXTOS)
    
    # Construir ejemplo completo con metadata rica
    ejemplo = {
        "pais": pais,
        "categoria": categoria,
        "subcategoria": subcategoria,
        "texto_racista": texto_racista,
        "texto_antirracista": texto_antirracista,
        "contexto": contexto,
        "nivel_sutileza": determinar_nivel_sutileza(categoria),
        "grupos_afectados": obtener_grupos_afectados(subcategoria),
        "mecanismo_discriminacion": obtener_mecanismo(subcategoria),
        "interseccionalidad": determinar_interseccionalidad(subcategoria, contexto),
        "jerga_regional": True,
        "sensibilidad": "alta",
        "dimension_historica": obtener_dimension_historica(subcategoria),
        "generado_en": datetime.now().isoformat(),
        "id": hashlib.md5(f"{texto_racista}{texto_antirracista}".encode()).hexdigest()[:16]
    }
    
    return ejemplo

# ============================================================================
# GENERACIÓN DEL DATASET COMPLETO
# ============================================================================

def generar_dataset_completo() -> List[Dict]:
    """
    Genera el dataset completo de 35,000 ejemplos con balance perfecto
    """
    dataset = []
    total_generados = 0
    
    print("=" * 80)
    print("🚀 GENERANDO DIGNITYAI-RACISM-LATAM DATASET")
    print("=" * 80)
    print("\n⚠️  ADVERTENCIA ÉTICA: Este dataset documenta lenguaje racista")
    print("   con fines EXCLUSIVAMENTE educativos y de investigación.")
    print("=" * 80)
    
    for pais in PAISES:
        print(f"\n🌎 PAÍS: {pais}")
        print("-" * 80)
        
        for categoria, config in CATEGORIAS.items():
            num_ejemplos_categoria = int(EJEMPLOS_POR_PAIS * config["peso"])
            ejemplos_por_subcat = num_ejemplos_categoria // len(config["subcategorias"])
            
            print(f"\n  📁 Categoría: {categoria}")
            print(f"     Total categoría: {num_ejemplos_categoria} ejemplos")
            
            for subcategoria in config["subcategorias"]:
                print(f"     → {subcategoria}: {ejemplos_por_subcat} ejemplos", end=" ")
                
                for i in range(ejemplos_por_subcat):
                    ejemplo = generar_ejemplo(pais, categoria, subcategoria)
                    dataset.append(ejemplo)
                    total_generados += 1
                    
                    # Progress indicator
                    if (i + 1) % 50 == 0:
                        print(".", end="", flush=True)
                
                print(f" ✓ ({ejemplos_por_subcat} ejemplos)")
    
    print("\n" + "=" * 80)
    print(f"✅ GENERACIÓN COMPLETADA: {total_generados:,} ejemplos")
    print("=" * 80)
    
    return dataset

# ============================================================================
# VALIDACIÓN
# ============================================================================

def validar_dataset(dataset: List[Dict]) -> pd.DataFrame:
    """
    Valida la calidad del dataset y elimina duplicados
    """
    print("\n" + "=" * 80)
    print("🔍 VALIDANDO DATASET")
    print("=" * 80)
    
    df = pd.DataFrame(dataset)
    
    # 1. Estadísticas básicas
    print("\n📊 ESTADÍSTICAS GENERALES:")
    print(f"   Total ejemplos: {len(df):,}")
    print(f"   Países únicos: {df['pais'].nunique()}")
    print(f"   Categorías únicas: {df['categoria'].nunique()}")
    print(f"   Subcategorías únicas: {df['subcategoria'].nunique()}")
    print(f"   Contextos únicos: {df['contexto'].nunique()}")
    
    # 2. Distribución por país
    print("\n🌎 DISTRIBUCIÓN POR PAÍS:")
    for pais, count in df['pais'].value_counts().sort_index().items():
        porcentaje = (count / len(df)) * 100
        print(f"   {pais}: {count:,} ({porcentaje:.1f}%)")
    
    # 3. Distribución por categoría
    print("\n📁 DISTRIBUCIÓN POR CATEGORÍA:")
    for cat, count in df['categoria'].value_counts().items():
        porcentaje = (count / len(df)) * 100
        peso_esperado = CATEGORIAS[cat]["peso"] * 100
        print(f"   {cat}: {count:,} ({porcentaje:.1f}% | esperado: {peso_esperado:.0f}%)")
    
    # 4. Deduplicación
    print("\n🧹 DEDUPLICACIÓN:")
    antes = len(df)
    df = df.drop_duplicates(subset=['texto_racista', 'texto_antirracista'])
    despues = len(df)
    duplicados = antes - despues
    print(f"   Duplicados eliminados: {duplicados:,} ({(duplicados/antes)*100:.2f}%)")
    print(f"   Ejemplos únicos: {despues:,}")
    
    # 5. Validar textos vacíos
    print("\n✅ VALIDACIÓN DE CONTENIDO:")
    vacios_racista = df[df['texto_racista'].str.strip() == ''].shape[0]
    vacios_antirracista = df[df['texto_antirracista'].str.strip() == ''].shape[0]
    print(f"   Textos racistas vacíos: {vacios_racista}")
    print(f"   Textos antirracistas vacíos: {vacios_antirracista}")
    
    # 6. Validación de sensibilidad
    print("\n⚠️  ANÁLISIS DE SENSIBILIDAD:")
    alta_sensibilidad = df[df['sensibilidad'] == 'alta'].shape[0]
    print(f"   Ejemplos de alta sensibilidad: {alta_sensibilidad:,} ({(alta_sensibilidad/len(df))*100:.1f}%)")
    print(f"   ⚠️  Estos ejemplos requieren uso EXTREMADAMENTE cuidadoso")
    
    # 7. Estadísticas de longitud
    print("\n📏 LONGITUD DE TEXTOS:")
    print(f"   Texto racista promedio: {df['texto_racista'].str.len().mean():.0f} caracteres")
    print(f"   Texto racista mín-máx: {df['texto_racista'].str.len().min()}-{df['texto_racista'].str.len().max()}")
    print(f"   Texto antirracista promedio: {df['texto_antirracista'].str.len().mean():.0f} caracteres")
    print(f"   Texto antirracista mín-máx: {df['texto_antirracista'].str.len().min()}-{df['texto_antirracista'].str.len().max()}")
    
    # 8. Balance general
    print("\n⚖️  MÉTRICAS DE BALANCE:")
    desv_paises = df['pais'].value_counts().std() / df['pais'].value_counts().mean()
    desv_categorias = df['categoria'].value_counts().std() / df['categoria'].value_counts().mean()
    print(f"   Desviación países: {desv_paises:.2%}")
    print(f"   Desviación categorías: {desv_categorias:.2%}")
    
    if desv_paises < 0.05 and desv_categorias < 0.10:
        print("   ✅ Balance EXCELENTE")
    elif desv_paises < 0.10 and desv_categorias < 0.15:
        print("   ✓ Balance BUENO")
    else:
        print("   ⚠️  Balance mejorable")
    
    # 9. ADVERTENCIA FINAL
    print("\n" + "=" * 80)
    print("⚠️  RECORDATORIO ÉTICO CRÍTICO")
    print("=" * 80)
    print("Este dataset contiene lenguaje ALTAMENTE SENSIBLE que documenta")
    print("racismo real con fines educativos. Uso irresponsable puede:")
    print("   • Perpetuar estereotipos dañinos")
    print("   • Ofender comunidades afectadas")
    print("   • Trivializar trauma histórico")
    print("\n✅ REQUERIDO ANTES DE PUBLICACIÓN:")
    print("   1. Revisión por académicos de estudios raciales")
    print("   2. Consulta con organizaciones afrodescendientes e indígenas")
    print("   3. Validación regional por país")
    print("   4. Content warnings reforzados en TODOS los materiales")
    print("=" * 80)
    
    return df


# ============================================================================
# CREAR SPLITS
# ============================================================================

def crear_splits(df: pd.DataFrame, output_dir: Path) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Crea splits train/validation/test estratificados
    """
    from sklearn.model_selection import train_test_split
    
    print("\n" + "=" * 80)
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

# ============================================================================
# EXPORTAR DATASET
# ============================================================================

def exportar_dataset(df: pd.DataFrame, output_dir: str = "dignityai-racism-latam") -> Path:
    """
    Guarda el dataset en múltiples formatos
    """
    print("\n" + "=" * 80)
    print("💾 EXPORTANDO DATASET")
    print("=" * 80)
    
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # 1. CSV
    print("\n📄 Guardando CSV...")
    df.to_csv(output_dir / "dataset.csv", index=False, encoding='utf-8')
    size_csv = (output_dir / "dataset.csv").stat().st_size / (1024 * 1024)
    print(f"   ✓ dataset.csv ({size_csv:.1f} MB)")
    
    # 2. JSON
    print("\n📄 Guardando JSON...")
    df.to_json(output_dir / "dataset.json", orient='records', force_ascii=False, indent=2)
    size_json = (output_dir / "dataset.json").stat().st_size / (1024 * 1024)
    print(f"   ✓ dataset.json ({size_json:.1f} MB)")
    
    # 3. Parquet
    print("\n📄 Guardando Parquet...")
    df.to_parquet(output_dir / "dataset.parquet", index=False)
    size_parquet = (output_dir / "dataset.parquet").stat().st_size / (1024 * 1024)
    print(f"   ✓ dataset.parquet ({size_parquet:.1f} MB)")
    
    # 4. Splits
    train_df, val_df, test_df = crear_splits(df, output_dir)
    
    # 5. Metadata
    print("\n📄 Guardando metadata...")
    metadata = {
        "nombre": "DignityAI-Racism-LATAM",
        "version": "1.0.0",
        "descripcion": "Dataset de discriminación racial en español latinoamericano",
        "total_ejemplos": len(df),
        "paises": df['pais'].unique().tolist(),
        "categorias": df['categoria'].unique().tolist(),
        "fecha_generacion": datetime.now().isoformat(),
        "autor": "Antonio Dromundo",
        "licencia": "CC BY-NC-SA 4.0",
        "parte_de": "Iniciativa DignityAI",
        "advertencia_uso": "CONTENIDO ALTAMENTE SENSIBLE - Uso exclusivo para investigación y educación",
        "contacto": {
            "linkedin": "https://www.linkedin.com/in/antonndromundo/",
            "github": "https://github.com/antuansabe",
            "email": "antuansabe@gmail.com"
        },
        "estadisticas": {
            "por_pais": df['pais'].value_counts().to_dict(),
            "por_categoria": df['categoria'].value_counts().to_dict(),
            "por_contexto": df['contexto'].value_counts().to_dict(),
            "por_nivel_sutileza": df['nivel_sutileza'].value_counts().to_dict()
        },
        "validacion_requerida": [
            "Revisión por académicos de estudios raciales",
            "Consulta con organizaciones afrodescendientes",
            "Consulta con organizaciones indígenas",
            "Validación regional por país",
            "Revisión ética institucional"
        ]
    }
    
    with open(output_dir / "metadata.json", 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"   ✓ metadata.json")
    
    print("\n" + "=" * 80)
    print("✅ DATASET EXPORTADO EXITOSAMENTE")
    print("=" * 80)
    print(f"\n📁 Directorio: {output_dir.absolute()}/")
    print(f"\n📦 Archivos generados:")
    print(f"   • dataset.csv ({size_csv:.1f} MB)")
    print(f"   • dataset.json ({size_json:.1f} MB)")
    print(f"   • dataset.parquet ({size_parquet:.1f} MB)")
    print(f"   • train.csv ({len(train_df):,} ejemplos)")
    print(f"   • validation.csv ({len(val_df):,} ejemplos)")
    print(f"   • test.csv ({len(test_df):,} ejemplos)")
    print(f"   • metadata.json")
    
    return output_dir

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal que ejecuta todo el proceso"""
    import time
    start_time = time.time()
    
    print("\n")
    print("=" * 80)
    print("🌟 DIGNITYAI-RACISM-LATAM DATASET GENERATOR")
    print("=" * 80)
    print("\nProtecting human dignity through AI")
    print("Part of the DignityAI Initiative\n")
    print("⚠️  CONTENIDO ALTAMENTE SENSIBLE")
    print("   Uso exclusivo para investigación y educación\n")
    print("=" * 80)
    
    # Confirmación del usuario
    print("\n⚠️  CONFIRMACIÓN REQUERIDA:")
    print("   Este script generará contenido racial EXPLÍCITO con fines educativos.")
    print("   ¿Entiendes los riesgos éticos y te comprometes al uso responsable?")
    confirmacion = input("\n   Escribe 'SÍ, ENTIENDO' para continuar: ")
    
    if confirmacion.strip().upper() != "SÍ, ENTIENDO":
        print("\n❌ Generación cancelada. Lee la guía de uso responsable primero.")
        return
    
    # PASO 1: Generar dataset
    print("\n🚀 PASO 1: Generando ejemplos...")
    dataset = generar_dataset_completo()
    
    # PASO 2: Validar y limpiar
    print("\n✅ PASO 2: Validando dataset...")
    df = validar_dataset(dataset)
    
    # PASO 3: Exportar
    print("\n💾 PASO 3: Exportando archivos...")
    output_dir = exportar_dataset(df)
    
    # Tiempo total
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    
    print("\n" + "=" * 80)
    print("🎉 ¡DATASET COMPLETADO!")
    print("=" * 80)
    print(f"\n⏱️  Tiempo total: {minutes}m {seconds}s")
    print(f"📁 Ubicación: {output_dir.absolute()}/")
    print(f"📊 Total ejemplos: {len(df):,}")
    
    print("\n📋 PRÓXIMOS PASOS **OBLIGATORIOS**:")
    print("   1. ✅ Revisar manualmente 500+ ejemplos aleatorios")
    print("   2. ✅ Consultar con académicos de estudios raciales")
    print("   3. ✅ Consultar con organizaciones afrodescendientes")
    print("   4. ✅ Consultar con organizaciones indígenas")
    print("   5. ✅ Validar regionalmente por país")
    print("   6. ✅ Obtener IRB approval si en institución")
    print("   7. ⚠️  Ajustar según feedback comunitario")
    print("   8. 📤 Subir a GitHub con warnings claros")
    print("   9. 📤 Publicar en HuggingFace con restricciones")
    print("   10. 🎊 Celebrar RESPONSABLEMENTE")
    
    print("\n" + "=" * 80)
    print("⚠️  RECORDATORIO FINAL")
    print("=" * 80)
    print("Este dataset documenta TRAUMA HISTÓRICO y ACTUAL.")
    print("Úsalo con el respeto que las comunidades afectadas merecen.")
    print("Primero no dañar. Siempre consultar. Nunca perpetuar.")
    print("=" * 80)
    print("\n🌟 DignityAI - Protecting human dignity through AI")
    print("=" * 80)
    print()

if __name__ == "__main__":
    main()
