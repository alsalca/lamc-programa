#!/usr/bin/env python3
"""
Validador del Evidence Envelope de LAMC — SIN DEPENDENCIAS.

No necesita instalar nada. Usa solo lo que Python trae de fábrica.
Motivo: el entorno bloquea la instalación de paquetes, así que cualquier
comprobación que dependa de una pieza externa falla. Esta no falla.

USO:
    python3 validar_evidencia.py <carpeta_del_proyecto>

Ejemplo (desde la raíz del repositorio, donde está este archivo en
`herramientas/`):

    python3 herramientas/validar_evidencia.py proyectos/P2_DEMO_RECONSTRUCCION

La carpeta tiene que ser la del PROYECTO (o su `entregables/`), no la raíz del
repositorio: la herramienta mira dentro de la carpeta que se le da, y en la raíz
no hay fichas que mirar. Antes esta ayuda sugería pasar `.`, que no encontraba
nada y parecía un fallo de las fichas.

El esquema se busca primero en la carpeta indicada y en su subcarpeta
`entregables/`. Si no aparece ahí, y existe el proyecto P1 de este programa en
su ubicación canónica, se usa el esquema de ahí.

QUÉ EXIGE A QUIÉN — CORRECCIÓN 2026-09-25
-----------------------------------------
Este validador aplicaba a CUALQUIER carpeta tres mínimos que en realidad eran
requisitos del CHARTER DE P1 sobre SUS EJEMPLOS:

    «3 ejemplos reales»                      (CHARTER de P1, E-P1-03)
    «los ejemplos cubren >= 2 autoridades»   (CHARTER de P1, §8.4)

Al generalizarlos, la herramienta SUSPENDÍA proyectos completos: P7 tiene una
sola autoridad POR DISEÑO —es un dominio nuevo, no una demostración de que el
sobre generaliza— y P3 no tiene ni un archivo JSON, porque sus entregables son
documentos de texto. El fallo parecía del entregable y era del instrumento.

Y era grave: la regla del programa es que un nivel no se pasa sin pasar su
prueba. Si la prueba dice «falla» sobre algo bien hecho, lo roto es la prueba.

Ahora los mínimos se DECLARAN por proyecto en `registro/entregables.json`:

    "validacion": {"ejemplos_min": 3, "fichas_min": 0, "autoridades_min": 2,
                   "_fuente": "CHARTER.md §8.4 y E-P1-03"}

Un mínimo que nadie declara se informa como «no exigido» —NO se aprueba en
silencio— para que se vea la diferencia entre «cumple» y «no se le pedía».

MÍNIMOS CUALITATIVOS — AMPLIACIÓN 2026-09-26 (misión H-2)
---------------------------------------------------------
Los tres números de arriba no saben expresar los mínimos que NO son un conteo
de archivos ni de autoridades. La auditoría independiente lo midió: recortando
P2, P7 o P8 a una sola ficha, el validador decía APROBADO (exit 0) y solo
imprimía «no exigido». Pero sus contratos sí exigen cosas:

    P2  CHARTER.md:101  «Actividad en >=2 cadenas (demuestra el multi-cadena)»
    P8  CHARTER.md:97   «Deben aparecer al menos los dos valores: ONCHAIN y
                         PUBLIC_API (o el que corresponda a cada dominio)»
    P7  CHARTER.md:184  «Existe al menos un hueco declarado»

Ahora `validacion` admite tres mínimos más, cada uno atado al campo EXISTENTE
del sobre que lo expresa —no se inventa ningún nombre del contrato—:

    cadenas_min        valores distintos de `container.chain`        (P2)
    tipos_fuente_min   valores distintos de `source_type`            (P8)
    huecos_min         fichas con `unknown` NO vacío                 (P7)

Son acumulativos, no sustitutos: un proyecto puede declarar los seis.

IDENTIFICACIÓN POR MENCIONES — CORRECCIÓN 2026-09-26 (misión H-6)
-----------------------------------------------------------------
Cuando el nombre de la carpeta no está en el registro, este validador leía el
`CHARTER.md` y elegía «el que más se menciona». Una copia de P7 llamada de otra
forma se identificaba como P1_ESQUEMA_EVIDENCIA **y se le aplicaban los mínimos
de P1**: rechazar algo bueno con un mínimo ajeno, o exigir lo que no toca.
Una mención en un texto NO es una identidad. Ahora, cuando la identificación es
por menciones, se dice QUIÉN se menciona, se dice EN VOZ ALTA que no se aplica
ningún mínimo, y no se aplica ninguno. La identidad la fija el nombre de la
carpeta; el texto solo informa.

CÓDIGOS DE SALIDA:
    0  APROBADO        — todo lo aplicable pasa
    1  PROBLEMAS       — hay algo que corregir
    2  ERROR DE USO    — falta la carpeta o el argumento
    3  NO APLICA       — no hay nada que este validador pueda comprobar aquí
                         (por ejemplo un proyecto de documentos de texto)

El 3 existe para que «no se comprobó nada» NUNCA se lea como «está bien».
"""

import json
import re
import sys
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────
# LOS 22 CAMPOS DEL SOBRE
# Aprobados por la decision HG-004 (2026-09-21). Fuente: el documento interno de
# propuesta, §5.
#
# CORRECCIÓN 2026-09-21: la versión anterior declaraba «21 campos» y solo
# comprobaba 14 — faltaban 7. El error lo detectó quien construia el entregable
# al declarar su objetivo. Habría producido un APROBADO falso. Corregido.
#
# CORRECCIÓN 2026-09-23 (puerta de publicación): este ENCABEZADO seguía
# diciendo «21» mientras la lista de abajo tenía 22 desde que se añadió
# `quantity`. La lista era correcta y el comentario no. Es el mismo defecto de
# L-01 y §9.quater —una constante repetida, creída por estar escrita— vivo
# dentro de la herramienta que existe para detectarlo. Se CUENTA la lista;
# no se copia el número.
# ─────────────────────────────────────────────────────────────────────
CAMPOS = [
    # identidad
    "claim_id",
    # sujeto y lugar
    "subject", "container", "instrument",
    # CUÁNTO — añadido en v0.2.0 (HG-010, 2026-09-21).
    # La v0.1.0 no tenía dónde poner la cifra: el sobre describía la procedencia
    # de un importe pero no tenía renglón para el importe. Ver L-06 en
    # el registro interno de lecciones. Puede valer el centinela "UNKNOWN".
    "quantity",
    # procedencia
    "source_type", "source_reference", "capture_method",
    # tiempo
    "observed_at", "effective_at", "freshness",
    # confiabilidad
    "authority", "verification_status", "confidence",
    # respaldo
    "raw_reference", "evidence_hash",
    # estado
    "reconciliation_status",
    # LO QUE NO SE SABE — el corazón del sobre
    "known", "unknown", "unknown_reason",
    # trazabilidad
    "producer", "schema_version",
]

# ─────────────────────────────────────────────────────────────────────
# AQUÍ VIVÍAN CINCO LISTAS ESCRITAS A MANO (2026-09-26, misión M-T2b)
#
#     AUTORIDADES · VERIFICACION · CONFIANZA · RECONCILIACION · SUJETOS
#
# Eran copias de otras tantas enumeraciones del esquema. Envejecieron: no
# incluían el centinela "UNKNOWN" que el contrato SÍ admite en `authority`
# (A1: «no lo sé» es una respuesta legítima), así que la herramienta RECHAZABA
# fichas válidas. Una copia de una regla es una regla que puede divergir de su
# fuente; la fuente es el esquema. Ya no hay copia: las enumeraciones se
# comprueban recorriendo el esquema (ver `validar_esquema`).
# ─────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────
# REGLA CENTRAL — «NO LO SÉ ES VÁLIDO»  (aprobada 2026-09-21)
#
# El centinela "UNKNOWN" se admite en los 16 CAMPOS DEL HECHO y NUNCA en los
# 6 CAMPOS DEL REGISTRO (`claim_id`, `known`, `unknown`, `unknown_reason`,
# `producer`, `schema_version`): esos son la identidad y la contabilidad del
# sobre, no su contenido.
# Cuando un campo del hecho vale el centinela, NO está establecido y debe
# figurar en `unknown` con su motivo. Cuando no lo vale, está establecido y
# debe figurar en `known`.
#
# Esto sustituye la lista anterior de «qué campos admiten el centinela»
# (eran 7 de 22). La lista era la causa raíz de tres rondas de fallos:
# cada caso real encontraba un campo fuera de ella, y había que inventar
# un valor con forma de dato. Ver la leccion L-12 en el registro interno de lecciones.
#
# CORRECCIÓN 2026-09-23: este comentario decía «CUALQUIERA de los 22 campos»,
# que es la regla de la v0.4.0 — SUPERADA en la v0.5.0, al descubrir que aplicar
# el centinela a los campos del registro DISUELVE la regla de bloqueo
# (`known: "UNKNOWN"` no exige nada). El CÓDIGO ya aplicaba la regla buena; el
# comentario describía la vieja. Otra constante creída por estar escrita
# (§9.quater), esta vez dentro del programa en vez de en el entregable.
# ─────────────────────────────────────────────────────────────────────
CENTINELA = "UNKNOWN"

# Los 6 campos del REGISTRO: la identidad y la contabilidad del sobre, no su
# contenido. El centinela NUNCA se admite en ellos.
#
# CORRECCIÓN 2026-09-25 (revisión de publicación). Antes esta comprobación se
# aplicaba solo a `known` y `unknown` —los dos que recorre el bucle—, así que
# **`producer: "UNKNOWN"` pasaba APROBADO** con solo declararlo en `unknown` con
# su motivo: la partición quedaba satisfecha y nadie miraba el valor.
# Lo encontró una revisión independiente, no la herramienta.
#
# Y es el fallo que esta herramienta existe para perseguir: la regla central del
# contrato dice «nunca en los 6», y el validador comprobaba dos.
CAMPOS_REGISTRO = ("claim_id", "known", "unknown", "unknown_reason",
                   "producer", "schema_version")

# Campos que no describen el hecho en sí, sino la contabilidad del propio sobre.
# No cuentan para exigir que «al menos algo esté establecido».
CAMPOS_CONTABLES = ("known", "unknown", "unknown_reason")

# NOTA (2026-09-26, M-T2b): aquí vivían también `CAMPOS_QUE_PUEDEN_IR_VACIOS`,
# `VACIO` y `esta_establecido`, que decidían a mano qué valores eran «vacíos».
# Esa decisión la declara el propio contrato con `required`, `minLength`,
# `minItems`, `minProperties`, `anyOf` y `const`, y ahora la aplica
# `validar_esquema` campo por campo, en cualquier nivel.

def fallo(msg):
    print(f"  ✗ {msg}")
    return 1


def ok(msg):
    print(f"  ✓ {msg}")
    return 0


def buscar(carpeta, nombre):
    """Busca un archivo por nombre en la carpeta y en subcarpetas obvias."""
    for base in (carpeta, carpeta / "entregables", carpeta / "bundle"):
        p = base / nombre
        if p.exists():
            return p
    return None


def buscar_esquema(carpeta):
    """Busca el esquema. Primero en la carpeta dada; si no, SUBIENDO desde donde
    vive este script y mirando unos pocos niveles hacia abajo.

    CORRECCIÓN 2026-09-21: antes solo miraba la carpeta dada, así que al validar
    una carpeta que solo contenía fichas (por ejemplo una prueba de suficiencia)
    decía «no encontré ningún archivo *.schema.json» y el bloque [1] fallaba sin
    que la ficha tuviera culpa. Lo detectó un agente de prueba ciega.

    CORRECCIÓN 2026-09-23 (1): el respaldo era una ruta fija al proyecto interno
    del autor. Publicada, esa ruta no existe en la máquina de nadie más —y revela
    la estructura privada del programa—. Se cambió por subir por el árbol.

    CORRECCIÓN 2026-09-23 (2): **y al hacerlo se rompió.** Subir por el árbol no
    basta: el esquema canónico vive dentro de una carpeta de proyecto, a dos
    niveles de profundidad, y el respaldo no miraba hacia abajo. Validar
    cualquier proyecto del programa —P2, por ejemplo— decía «no encontré ningún
    archivo *.schema.json» y el fallo parecía de la ficha. Lo encontró el Chat
    Jefe al preparar el traspaso de P2, no una prueba.

    Ahora se busca por PATRÓN a profundidad acotada, sin nombrar ninguna carpeta:
    así encuentra el esquema en cualquier disposición, y sigue sin llevar dentro
    ni una ruta del programa.
    """
    for base in (carpeta, carpeta / "entregables"):
        if base.exists():
            for p in base.glob("*.schema.json"):
                return p
    # Respaldo: subir desde la ubicación de este script, mirando unos niveles
    # hacia abajo por PATRÓN. Nunca por nombre: un nombre escrito a mano envejece
    # o delata; un patrón, no.
    patrones = (
        "*.schema.json",
        "entregables/*.schema.json",
        "*/entregables/*.schema.json",
        "*/*/entregables/*.schema.json",
    )
    aqui = Path(__file__).resolve().parent
    for base in (aqui, *aqui.parents):
        if not base.exists():
            continue
        for patron in patrones:
            for p in sorted(base.glob(patron)):
                return p
    return None


def cargar_registro():
    """Lo que cada proyecto declara. Devuelve {} si no se encuentra.

    Se busca en `registro/entregables.json` subiendo desde donde vive este
    script. En el paquete publicado no existe, y no pasa nada: sin registro no
    hay mínimos declarados, y entonces los mínimos se reportan como «no
    exigido» en vez de inventarse. Es la diferencia entre no comprobar y
    aprobar: aquí se dice cuál de las dos cosas está pasando.
    """
    for base in (Path(__file__).resolve().parent, *Path(__file__).resolve().parent.parents):
        p = base / "registro" / "entregables.json"
        if p.exists():
            try:
                d = json.loads(p.read_text(encoding="utf-8"))
                return {k: v for k, v in d.items()
                        if not k.startswith("_") and isinstance(v, dict)}
            except Exception:
                return {}
    return {}


def proyecto_de(carpeta, registro):
    """Qué proyecto del registro es esta carpeta, si lo es, y CÓMO se identificó.

    Devuelve `(nombre, info, metodo)` con `metodo` en `("carpeta", "menciones")`
    o `None` si no se reconoce. `info` es SIEMPRE `{}` cuando el método es
    `"menciones"`: ver la corrección H-6, abajo.

    Se mira la carpeta y sus padres: así funciona tanto si se le pasa la raíz
    del proyecto como si se le pasa `entregables/` o `entregables/bundle/`.
    Si no coincide con ninguno, devuelve `(None, {}, None)` — y entonces no se
    exige ningún mínimo, en vez de aplicar los de otro.

    ── CORRECCIÓN 2026-09-25 (auditoría, revisión 2, hallazgo 3) ──
    Identificar al proyecto **solo por el nombre de su carpeta** dejaba un hueco
    silencioso: P4 recortado a 1 ficha y copiado como `P4_RENOMBRADO` daba
    **APROBADO (exit 0)**, porque con otro nombre no se le exigía su mínimo. Una
    copia, un ZIP o un checkout con otro nombre se aprobaban sin sus mínimos.

    Un proyecto no se reconoce solo por cómo se llama su carpeta: se reconoce
    **por lo que él mismo declara**. Así que, si el nombre no coincide, se lee su
    `CHARTER.md` y se busca qué proyecto se nombra en él. Se elige el que más
    veces aparece, para que una mención de pasada a otro proyecto no confunda.

    ── CORRECCIÓN 2026-09-26 (auditoría, hallazgo H-6) ──
    Lo de arriba arregló un fallo y abrió otro PEOR: la mención identificaba al
    proyecto y **se le aplicaban sus mínimos**. Una copia de P7 con otro nombre
    se identificaba como `P1_ESQUEMA_EVIDENCIA` —P1 se nombra mucho en cualquier
    charter, por ser el contrato común— y se le exigían los mínimos DE P1: tres
    ejemplos y dos autoridades. La copia de un proyecto correcto se rechazaba
    con las reglas de otro, o se le exigía lo que no le tocaba.

    La raíz es que **una mención no es una identidad**: el texto de un charter
    nombra a muchos proyectos, y contar menciones es una heurística, no una
    declaración. La identidad la fija el nombre de la carpeta. Por eso ahora la
    mención solo INFORMA —dice qué proyecto parece ser— y NUNCA aplica mínimos:
    devuelve `info = {}` y el aviso se imprime en voz alta. Es la opción más
    segura de las dos que planteaba el hallazgo, porque no depende de que la
    mención sea «inequívoca» (algo que un contador no puede decidir).
    """
    for p in (carpeta, *carpeta.parents):
        if p.name in registro:
            return p.name, registro[p.name], "carpeta"

    for p in (carpeta, *carpeta.parents):
        charter = p / "CHARTER.md"
        if not charter.exists():
            continue
        try:
            texto = charter.read_text(encoding="utf-8")
        except Exception:
            continue
        cuenta = {k: texto.count(k) for k in registro}
        mejor = max(cuenta, key=cuenta.get) if cuenta else None
        if mejor and cuenta[mejor] > 0:
            # H-6: se informa de la mención, NO se aplican sus mínimos.
            return mejor, {}, "menciones"
    return None, {}, None


# ─────────────────────────────────────────────────────────────────────
# EL CONTRATO COMO FUENTE ÚNICA — VALIDADOR DIRIGIDO POR EL ESQUEMA
#
# POR QUÉ (2026-09-26, misión M-T2b)
# ----------------------------------
# Hasta aquí la herramienta llevaba su PROPIA copia de las reglas: tres
# recorridos a mano (`claves_prohibidas`, `valores_fuera_de_lista`,
# `patrones_incumplidos`) y una lista de valores escrita a mano por cada
# enumeración. Esa copia envejeció, y por eso la auditoría R3 encontró a la vez
# falsos aprobados y falsos rechazos:
#
#   ACEPTABA lo que el contrato prohíbe
#     · `pattern` solo se aplicaba en el primer nivel, sin entrar en las ramas
#       `anyOf`/`oneOf`: `quantity:"cinco"`, `quantity:"-5"`,
#       `evidence_hash:"md5:abc"` y `effective_at:"ayer"` pasaban APROBADOS.
#     · no se comprobaban `type`, `minLength`/`maxLength` ni `uniqueItems`.
#
#   RECHAZABA lo que el contrato admite
#     · las listas a mano se olvidaron del centinela "UNKNOWN" y tumbaban
#       `authority:"UNKNOWN"` y `subject:"UNKNOWN"` — contra el axioma A1.
#
# La lección es la de §9.quater: mientras el validador mantenga su copia de una
# regla, esa copia puede divergir de la fuente. Ahora la fuente es el ESQUEMA:
# se recorre la INSTANCIA contra el ESQUEMA, en cualquier nivel (raíz, `subject`,
# `container`, `instrument`, `freshness`, elementos de `known`/`unknown`), y se
# aplican TODAS las palabras clave que el contrato usa:
#
#   type · enum · const · pattern · minLength · maxLength · minimum
#   minItems · uniqueItems · minProperties
#   required · properties · additionalProperties · items · contains
#   anyOf · oneOf · allOf · if · then
#
# Añadir una regla al contrato la comprueba sin tocar este archivo. Y como el
# esquema es el mismo que se publica, el validador no puede quedarse atrás.
#
# DOS REGLAS DEL CONTRATO QUE EL ESQUEMA NO EXPRESAN siguen escritas a mano,
# más abajo, en el bucle de fichas y bien señaladas:
#   1. el centinela "UNKNOWN" NUNCA se admite en los 6 CAMPOS DEL REGISTRO
#      (el esquema solo lo impide en algunos, y solo por patrón); y
#   2. la REGLA BLOQUEANTE: si `unknown` no está vacío, `unknown_reason` es
#      obligatorio y no puede estar vacío.
# También siguen a mano las reglas que el esquema no declara: C2 (todo motivo
# de `unknown_reason` corresponde a un campo de `unknown`) y «al menos un campo
# del hecho establecido».
#
# CALIDAD DEL MENSAJE: cada problema nombra la RUTA, el VALOR y la REGLA del
# contrato. Un «no cumple el esquema» genérico obligaría a adivinar qué
# corregir, que es justo lo que esta herramienta existe para evitar.
# ─────────────────────────────────────────────────────────────────────
def _tipo_py(valor):
    """El tipo JSON del valor. `bool` se separa de `int` (en Python son parientes)."""
    if isinstance(valor, bool):
        return "boolean"
    if isinstance(valor, int):
        return "integer"
    if isinstance(valor, float):
        return "number"
    if isinstance(valor, str):
        return "string"
    if isinstance(valor, list):
        return "array"
    if isinstance(valor, dict):
        return "object"
    if valor is None:
        return "null"
    return type(valor).__name__


def _tipo_ok(valor, tipo):
    """¿El valor es del tipo JSON que el contrato nombra? Un tipo desconocido no se inventa."""
    if tipo == "boolean":
        return isinstance(valor, bool)
    if tipo == "integer":
        return isinstance(valor, int) and not isinstance(valor, bool)
    if tipo == "number":
        return isinstance(valor, (int, float)) and not isinstance(valor, bool)
    if tipo == "string":
        return isinstance(valor, str)
    if tipo == "array":
        return isinstance(valor, list)
    if tipo == "object":
        return isinstance(valor, dict)
    if tipo == "null":
        return valor is None
    return True


def _corto(valor):
    """El valor en una línea y recortado: un mensaje útil no vuelca la ficha entera."""
    try:
        texto = json.dumps(valor, ensure_ascii=False)
    except (TypeError, ValueError):
        texto = repr(valor)
    return texto if len(texto) <= 120 else texto[:117] + "..."


def _valor_para_mensaje(instancia):
    """El valor para el mensaje: los escalares se citan; un objeto o lista, no.

    En un fallo de `anyOf`/`oneOf` sobre un objeto, volcar el objeto entero no
    informa —el motivo está en un subcampo, y los suberrores ya lo nombran— y
    tapa el mensaje. Para un escalar sí es útil: hay que ver QUÉ valor se rechaza.
    """
    if isinstance(instancia, (dict, list)):
        return ""
    return f" = {_corto(instancia)}"


def _pista_variantes(ramas, validas):
    """Cuando `oneOf` deja pasar varias ramas, intenta decir QUÉ campo se repite.

    El contrato usa `oneOf` para la partición exacta: cada campo del sobre está
    en `known` o en `unknown`, y en UNA SOLA de las dos. Las ramas de esa
    partición tienen la forma `properties.<lista>.contains.const = <campo>`.
    Si todas las ramas válidas comparten el mismo `const` y cambian de lista,
    el problema es que el campo figura en las dos, y se dice con su nombre en
    vez de con un índice.
    """
    parejas = []
    for i in validas:
        rama = ramas[i]
        props = rama.get("properties") if isinstance(rama, dict) else None
        if not isinstance(props, dict) or len(props) != 1:
            return ""
        lista, sub = next(iter(props.items()))
        if not isinstance(sub, dict) or not isinstance(sub.get("contains"), dict):
            return ""
        valor = sub["contains"].get("const")
        if not isinstance(valor, str):
            return ""
        parejas.append((lista, valor))
    if parejas and len({v for _, v in parejas}) == 1:
        return f"'{parejas[0][1]}' figura a la vez en {sorted({l for l, _ in parejas})}"
    return ""


def _detalle_variantes(fallos, tope=3):
    """Por qué falló cada variante de un `anyOf`/`oneOf`, sin quedarse en el primer error.

    Enseñar solo el PRIMER error de cada rama escondía el específico: con
    `subject: {"type": "ALIENIGENA"}` la rama falla por el `subject_id` que falta
    Y por el `type` fuera de la lista, y el mensaje útil es el segundo. Se unen
    los errores de cada variante (hasta `tope`, para no volcar el esquema entero).
    """
    partes = []
    for i, errs in fallos:
        cuerpo = " | ".join(errs[:tope])
        if len(errs) > tope:
            cuerpo += f" | ... y {len(errs) - tope} más"
        partes.append(f"variante {i+1}: {cuerpo}")
    return "; ".join(partes)


def validar_esquema(instancia, esq, ruta=""):
    """Comprueba la instancia CONTRA EL ESQUEMA, en cualquier nivel.

    Devuelve la lista de problemas. Cada uno nombra la RUTA, el VALOR y la REGLA
    del contrato que no se cumple: es la diferencia entre un informe que se puede
    corregir y un «no cumple el esquema» que obliga a adivinar.
    """
    problemas = []
    if not isinstance(esq, dict):
        return problemas

    def hijo(nombre):
        return f"{ruta}.{nombre}" if ruta else nombre

    # ── type ──
    if "type" in esq:
        tipos = esq["type"]
        tipos = tipos if isinstance(tipos, list) else [tipos]
        if not any(_tipo_ok(instancia, t) for t in tipos):
            problemas.append(
                f"{ruta or '(raíz)'}: el contrato exige tipo {'/'.join(map(str, tipos))} "
                f"(type); es {_tipo_py(instancia)}")

    # ── enum ──
    if isinstance(esq.get("enum"), list) and instancia not in esq["enum"]:
        problemas.append(
            f"{ruta} = {_corto(instancia)}: no figura en la lista cerrada del contrato "
            f"(enum); se admite: {sorted(map(str, esq['enum']))}")

    # ── const ──
    if "const" in esq and instancia != esq["const"]:
        problemas.append(
            f"{ruta} = {_corto(instancia)}: el contrato exige el valor fijo "
            f"{esq['const']!r} (const)")

    # ── cadenas ──
    if isinstance(instancia, str):
        if "pattern" in esq:
            try:
                if not re.search(esq["pattern"], instancia):
                    problemas.append(
                        f"{ruta} = {_corto(instancia)}: no cumple el patrón del contrato "
                        f"(pattern {esq['pattern']!r})")
            except re.error:
                pass          # un patrón ilegible no es culpa del dato
        if "minLength" in esq and len(instancia) < esq["minLength"]:
            problemas.append(
                f"{ruta} = {_corto(instancia)}: más corto de lo que el contrato admite "
                f"(minLength {esq['minLength']}; tiene {len(instancia)})")
        if "maxLength" in esq and len(instancia) > esq["maxLength"]:
            problemas.append(
                f"{ruta} = {_corto(instancia)}: más largo de lo que el contrato admite "
                f"(maxLength {esq['maxLength']}; tiene {len(instancia)})")

    # ── números ──
    if isinstance(instancia, (int, float)) and not isinstance(instancia, bool):
        if "minimum" in esq and instancia < esq["minimum"]:
            problemas.append(
                f"{ruta} = {instancia!r}: menor que el mínimo del contrato "
                f"(minimum {esq['minimum']})")

    # ── listas ──
    if isinstance(instancia, list):
        if "minItems" in esq and len(instancia) < esq["minItems"]:
            problemas.append(
                f"{ruta}: tiene {len(instancia)} elemento(s); el contrato exige al menos "
                f"{esq['minItems']} (minItems)")
        if "maxItems" in esq and len(instancia) > esq["maxItems"]:
            problemas.append(
                f"{ruta}: tiene {len(instancia)} elemento(s); el contrato admite como mucho "
                f"{esq['maxItems']} (maxItems)")
        if esq.get("uniqueItems") is True:
            vistos, repetidos = {}, []
            for i, x in enumerate(instancia):
                clave = json.dumps(x, sort_keys=True, ensure_ascii=False, default=repr)
                if clave in vistos:
                    repetidos.append(f"[{vistos[clave]}] y [{i}] = {_corto(x)}")
                else:
                    vistos[clave] = i
            if repetidos:
                problemas.append(
                    f"{ruta}: elementos repetidos (uniqueItems: true): "
                    + "; ".join(repetidos))
        items = esq.get("items")
        if isinstance(items, list):            # forma de tupla: el contrato no la usa
            for i, (x, sub) in enumerate(zip(instancia, items)):
                problemas += validar_esquema(x, sub, f"{ruta}[{i}]")
        elif isinstance(items, dict):
            for i, x in enumerate(instancia):
                problemas += validar_esquema(x, items, f"{ruta}[{i}]")
        if isinstance(esq.get("contains"), dict):
            if not any(not validar_esquema(x, esq["contains"]) for x in instancia):
                problemas.append(
                    f"{ruta}: ningún elemento cumple lo que el contrato exige para la lista "
                    f"(contains {_corto(esq['contains'])})")

    # ── objetos ──
    if isinstance(instancia, dict):
        props = esq.get("properties") if isinstance(esq.get("properties"), dict) else {}
        for nombre in esq.get("required", []):
            if nombre not in instancia:
                problemas.append(
                    f"{ruta}: falta el campo obligatorio '{nombre}' (required)")
        for nombre, valor in instancia.items():
            if nombre in props:
                problemas += validar_esquema(valor, props[nombre], hijo(nombre))
                continue
            extra = esq.get("additionalProperties", True)
            if extra is False:
                problemas.append(
                    f"{hijo(nombre)}: clave que el contrato NO admite "
                    f"(additionalProperties: false)")
            elif isinstance(extra, dict):
                problemas += validar_esquema(valor, extra, hijo(nombre))
        if "minProperties" in esq and len(instancia) < esq["minProperties"]:
            problemas.append(
                f"{ruta}: tiene {len(instancia)} propiedad(es); el contrato exige al menos "
                f"{esq['minProperties']} (minProperties)")
        if "maxProperties" in esq and len(instancia) > esq["maxProperties"]:
            problemas.append(
                f"{ruta}: tiene {len(instancia)} propiedad(es); el contrato admite como mucho "
                f"{esq['maxProperties']} (maxProperties)")

    # ── allOf: TODAS las ramas ──
    for rama in esq.get("allOf", []):
        if isinstance(rama, dict):
            problemas += validar_esquema(instancia, rama, ruta)

    # ── anyOf: AL MENOS una rama ──
    if isinstance(esq.get("anyOf"), list) and esq["anyOf"]:
        fallos = []
        for rama in esq["anyOf"]:
            e = validar_esquema(instancia, rama, ruta)
            if not e:
                break
            fallos.append((len(fallos), e))
        else:
            problemas.append(
                f"{ruta or '(raíz)'}{_valor_para_mensaje(instancia)}: no cumple ninguna de las "
                f"{len(esq['anyOf'])} variantes del contrato (anyOf) — "
                f"{_detalle_variantes(fallos)}")

    # ── oneOf: EXACTAMENTE una rama ──
    if isinstance(esq.get("oneOf"), list) and esq["oneOf"]:
        validas = [i for i, rama in enumerate(esq["oneOf"])
                   if not validar_esquema(instancia, rama, ruta)]
        if not validas:
            fallos = [(i, validar_esquema(instancia, rama, ruta))
                      for i, rama in enumerate(esq["oneOf"])]
            problemas.append(
                f"{ruta or '(raíz)'}{_valor_para_mensaje(instancia)}: no cumple ninguna de las "
                f"{len(esq['oneOf'])} variantes del contrato (oneOf) — "
                f"{_detalle_variantes(fallos)}")
        elif len(validas) > 1:
            pista = _pista_variantes(esq["oneOf"], validas)
            problemas.append(
                f"{ruta or '(raíz)'}: cumple MÁS DE UNA variante del contrato, que exige "
                f"exactamente una (oneOf: variantes {[i+1 for i in validas]})"
                + (f" — {pista}" if pista else ""))

    # ── if / then / else ──
    if "if" in esq:
        if not validar_esquema(instancia, esq["if"]):
            if "then" in esq:
                problemas += validar_esquema(instancia, esq["then"], ruta)
        elif "else" in esq:
            problemas += validar_esquema(instancia, esq["else"], ruta)

    return problemas


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2

    carpeta = Path(sys.argv[1]).resolve()
    if not carpeta.exists():
        print(f"ERROR: no existe {carpeta}")
        return 2

    registro = cargar_registro()
    proyecto, info, metodo = proyecto_de(carpeta, registro)
    por_mencion = (metodo == "menciones")
    val = info.get("validacion", {}) if isinstance(info.get("validacion"), dict) else {}
    ejemplos_min = val.get("ejemplos_min", 0)
    fichas_min = val.get("fichas_min", 0)
    autoridades_min = val.get("autoridades_min", 0)
    # Mínimos CUALITATIVOS (misión H-2): no son un conteo de archivos ni de
    # autoridades, son una propiedad del CONTENIDO de las fichas. Se declaran
    # aparte y se comprueban aparte, pero con la misma regla: sin `_fuente`
    # citada no se eximen; se informan como «no exigido».
    cadenas_min = val.get("cadenas_min", 0)
    tipos_fuente_min = val.get("tipos_fuente_min", 0)
    huecos_min = val.get("huecos_min", 0)
    fuente_min = val.get("_fuente", "sin declarar")
    hay_minimos = bool(ejemplos_min or fichas_min or autoridades_min
                       or cadenas_min or tipos_fuente_min or huecos_min)
    # Para los mensajes de «no exigido»: si la carpeta no está declarada —o se
    # identificó solo por menciones—, los mínimos NO se aplican, y decir «X no
    # declara mínimo» sería falso (H-6: X sí lo declara; lo que pasa es que no
    # se le aplica). Seis campos, un solo rótulo.
    etiq_min = proyecto if (proyecto and not por_mencion) else "esta carpeta"

    errores = 0
    print(f"\nVALIDADOR DE EVIDENCIA — {carpeta.name}")
    print("=" * 60)
    if por_mencion:
        # H-6: la mención informa, no identifica. Se dice en voz alta ANTES de
        # nada, porque el resultado de abajo NO va a comprobar mínimo alguno.
        print(f"  ⚠️  IDENTIFICADO POR MENCIONES, NO POR EL NOMBRE DE LA CARPETA.")
        print(f"      El CHARTER.md de esta carpeta nombra a {proyecto}, pero la carpeta")
        print(f"      se llama «{carpeta.name}». Una mención en un texto no es una")
        print(f"      identidad: una copia con otro nombre puede nombrar a cualquiera en")
        print(f"      su charter, y aplicar los mínimos del proyecto MENCIONADO rechazaría")
        print(f"      algo bueno con un mínimo ajeno, o exigiría lo que no toca (H-6).")
        print(f"      Por eso AQUÍ NO SE APLICA NINGÚN MÍNIMO. Solo se comprueba el")
        print(f"      contrato, ficha por ficha.")
    elif proyecto:
        print(f"  proyecto declarado: {proyecto} "
              f"(mínimos: ejemplos={ejemplos_min} fichas={fichas_min} "
              f"autoridades={autoridades_min} cadenas={cadenas_min} "
              f"tipos_fuente={tipos_fuente_min} huecos={huecos_min} · {fuente_min})")
    else:
        print("  carpeta no declarada en registro/entregables.json: "
              "no se exige ningún mínimo; solo se comprueba lo que hay")

    # ── 1. El esquema es un archivo legible y declara los 22 campos ──
    print("\n[1] ESQUEMA")
    esquema_p = buscar_esquema(carpeta)
    if not esquema_p:
        errores += fallo("no encontré ningún archivo *.schema.json")
        esquema = None
    else:
        try:
            esquema = json.loads(esquema_p.read_text(encoding="utf-8"))
            ok(f"se lee correctamente: {esquema_p.name}")
        except Exception as e:
            errores += fallo(f"no se puede leer: {e}")
            esquema = None

        if esquema is not None:
            req = set(esquema.get("required", []))
            faltan = set(CAMPOS) - req
            if faltan:
                errores += fallo(f"campos que NO están declarados como obligatorios: {sorted(faltan)}")
            else:
                ok(f"los {len(CAMPOS)} campos están declarados como obligatorios")

            # enumeraciones cerradas
            texto = json.dumps(esquema)
            n_enum = texto.count('"enum"')
            if n_enum >= 4:
                ok(f"hay {n_enum} listas cerradas de valores permitidos")
            else:
                errores += fallo(f"solo {n_enum} listas cerradas; se esperan al menos 4 "
                                 "(authority, verification_status, confidence, reconciliation_status)")

    # ── 2. Los ejemplos ──
    # Se busca en las ubicaciones donde cada proyecto deja su trabajo.
    # CORRECCIÓN 2026-09-21: faltaba 'entregables/bundle', que es donde P2
    # deja su bundle. El validador no lo encontraba.
    print("\n[2] EJEMPLOS")
    ejemplos = []
    for base in (carpeta / "entregables" / "examples",
                 carpeta / "examples",
                 carpeta / "entregables" / "bundle",
                 carpeta / "bundle",
                 carpeta / "entregables",
                 carpeta):
        if base.exists():
            encontrados = sorted(
                p for p in base.glob("*.json")
                if "schema" not in p.name.lower()
            )
            if encontrados:
                ejemplos = encontrados
                break

    if not ejemplos:
        # Un proyecto que DECLARA un mínimo sobre el contenido de las fichas y no
        # trae ninguna ficha no puede cumplirlo. Antes esto solo se miraba para
        # `ejemplos_min`, así que BORRAR el bundle entero (en vez de recortarlo)
        # salía por la puerta del «3 NO APLICA» — que no es un APROBADO, pero
        # tampoco nombra el incumplimiento. Ahora se nombra.
        contenido_min = [("fichas", fichas_min), ("autoridades", autoridades_min),
                         ("cadenas", cadenas_min), ("tipos de fuente", tipos_fuente_min),
                         ("huecos", huecos_min)]
        declarados = [f"{n}={v}" for n, v in contenido_min if v]
        if ejemplos_min:
            errores += fallo(f"no encontré ejemplos (*.json) y {proyecto or 'este proyecto'} "
                             f"declara un mínimo de {ejemplos_min} ({fuente_min})")
        elif declarados:
            errores += fallo(f"no encontré ninguna ficha (*.json) y {proyecto} declara mínimos "
                             f"sobre el CONTENIDO de las fichas ({', '.join(declarados)}): sin "
                             f"fichas no pueden cumplirse ({fuente_min})")
        else:
            print("  — no aplica: esta carpeta no contiene ejemplos (*.json) y "
                  "ningún proyecto declarado exige que los haya")
    else:
        ok(f"encontré {len(ejemplos)} archivo(s) de ejemplo")
        if ejemplos_min and len(ejemplos) < ejemplos_min:
            errores += fallo(f"{len(ejemplos)} ejemplo(s); {proyecto} declara un mínimo "
                             f"de {ejemplos_min} ({fuente_min})")
        elif ejemplos_min:
            ok(f"{len(ejemplos)} ejemplo(s) — cumple el mínimo de {ejemplos_min} "
               f"({fuente_min})")
        autoridades = set()
        total_fichas = 0
        # Acumuladores de los mínimos CUALITATIVOS (H-2). Se llenan ficha a
        # ficha, con los valores ESTABLECIDOS: el centinela "UNKNOWN" no es una
        # cadena, ni un tipo de fuente, ni un hueco «declarado» — es un campo
        # del que no sabemos nada, y A1 dice que no es cero.
        cadenas = set()
        tipos_fuente = set()
        fichas_con_hueco = 0

        for p in ejemplos:
            try:
                d = json.loads(p.read_text(encoding="utf-8"))
            except Exception as e:
                errores += fallo(f"{p.name}: no se puede leer ({e})")
                continue

            # Un archivo puede traer UNA ficha, o VARIAS dentro.
            # Se acepta: una lista, o un objeto con 'positions' / 'claims' / 'fichas'.
            if isinstance(d, list):
                fichas = [x for x in d if isinstance(x, dict)]
            elif isinstance(d, dict):
                for clave in ("positions", "claims", "fichas"):
                    if isinstance(d.get(clave), list):
                        fichas = [x for x in d[clave] if isinstance(x, dict)]
                        break
                else:
                    fichas = [d]
            else:
                fichas = []

            if not fichas:
                errores += fallo(f"{p.name}: no contiene ninguna ficha")
                continue

            total_fichas += len(fichas)

            # Las comprobaciones se hacen SOBRE CADA FICHA, no sobre el archivo.
            problemas = []
            for i, f in enumerate(fichas, 1):
                etq = f"{p.name} ficha {i}" if len(fichas) > 1 else p.name

                # (0) LA INSTANCIA CONTRA EL ESQUEMA, EN CUALQUIER NIVEL.
                #
                # Un solo recorrido dirigido por el contrato aplica TODAS las
                # palabras clave que el esquema declara: `type`, `enum`, `const`,
                # `pattern`, longitudes, `minimum`, `minItems`, `uniqueItems`,
                # `minProperties`, `required`, `additionalProperties`, `items`,
                # `contains`, `anyOf`, `oneOf`, `allOf` e `if`/`then` — también
                # dentro de `subject`, `container`, `instrument`, `freshness` y de
                # los elementos de `known`/`unknown`.
                #
                # Sustituye a los tres recorridos a mano que se quedaban cortos
                # (`pattern` solo en el primer nivel, sin `type`, sin
                # `uniqueItems`) y a las listas de valores copiadas a mano, que se
                # olvidaron del centinela. El esquema es la fuente; esto es su
                # intérprete, y por eso una regla nueva del contrato se comprueba
                # sin tocar este archivo.
                if esquema is not None:
                    contra_contrato = validar_esquema(f, esquema)
                    problemas += [f"{etq}: {x}" for x in contra_contrato]

                # (2) REGLA «NO LO SÉ ES VÁLIDO» — correspondencia valor ↔ lista.
                #     Un campo vale el centinela  ⟺  figura en `unknown`.
                #     Si no lo vale  ⟺  figura en `known`.
                _conocido = f.get("known")
                _desconocido = f.get("unknown")
                if isinstance(_conocido, list) and isinstance(_desconocido, list):
                    for c in CAMPOS:
                        if c not in f:
                            continue
                        es_centinela = (f[c] == CENTINELA)
                        en_unknown = (c in _desconocido)
                        en_known = (c in _conocido)
                        if es_centinela and not en_unknown:
                            problemas.append(
                                f"{etq}: '{c}' vale \"UNKNOWN\" pero no figura en 'unknown'")
                        if not es_centinela and not en_known:
                            problemas.append(
                                f"{etq}: '{c}' tiene valor pero no figura en 'known'")

                # (3) Al menos UN campo del hecho debe estar establecido.
                #     Una ficha que no afirma nada no es una ficha.
                sustantivos = [c for c in CAMPOS if c not in CAMPOS_CONTABLES]
                establecidos = [c for c in sustantivos
                                if c in f and f[c] != CENTINELA]
                if not establecidos:
                    problemas.append(
                        f"{etq}: ningún campo del hecho está establecido — la ficha no afirma nada")

                # (3.bis) PARTICIPACIÓN known / unknown — reglas C5, C6 y C7 de SPEC.md.
                #
                # CORRECCIÓN 2026-09-26 (M-T2b): estas tres reglas SE QUITAN de
                # aquí porque el contrato YA LAS DECLARA y `validar_esquema` las
                # aplica. El esquema parte los 22 campos con un `allOf` de 22
                # `oneOf` (cada campo, en `known` o en `unknown`, y en una sola de
                # las dos) y limita los elementos de ambas listas con `items.enum`:
                #   · C5 (un campo en las dos listas) → su `oneOf` deja pasar DOS
                #     ramas; el mensaje dice qué campo se repite.
                #   · C6 (un nombre con punto en `unknown`) → no está en `items.enum`.
                #   · C7 (un campo fuera de las dos listas, o un nombre que no es
                #     campo del sobre) → su `oneOf` no deja pasar ninguna rama, o
                #     el nombre no está en `items.enum`.
                # Tenerlas además escritas a mano era justo el defecto de esta
                # misión: una copia de la regla que puede divergir de la fuente.

                conocido = f.get("known")
                desconocido = f.get("unknown")

                # (3.bis.0) LO QUE NO PUEDE SER UNA LISTA, NO ES UNA LISTA.
                #
                # CORRECCIÓN 2026-09-23 (puerta de publicación): antes, si 'known'
                # no era una lista, TODAS las comprobaciones de participación se
                # SALTABAN EN SILENCIO — el `if isinstance(...)` era la única
                # puerta. Una ficha con `known: "UNKNOWN"` —el centinela en un
                # campo del REGISTRO, prohibido— pasaba el validador sin que se
                # mirara NADA, y salía APROBADO. FALLAR ABIERTO es peor que
                # fallar: la comprobación PARECE hecha.
                #
                # El esquema ya declara `type: array` para ambas listas y
                # `validar_esquema` lo comprueba; este guardia se MANTIENE porque
                # protege a las reglas escritas a mano de abajo, que si no se
                # saltarían en silencio. No es una copia de una regla del
                # contrato: es la puerta que impide que las reglas de abajo
                # fallen abiertas.
                for _nombre, _valor in (("known", conocido), ("unknown", desconocido)):
                    if _valor == CENTINELA:
                        problemas.append(
                            f"{etq}: el centinela 'UNKNOWN' NO se admite en '{_nombre}' — "
                            f"es contabilidad del sobre (campo del REGISTRO), no un hecho. "
                            f"Aplicado aquí disuelve la regla que sostiene todo lo demás")
                    elif not isinstance(_valor, list):
                        problemas.append(
                            f"{etq}: '{_nombre}' debe ser una LISTA de nombres de campo; "
                            f"es {type(_valor).__name__}")

                # (3.bis.0.bis) REGLA 1 DEL CONTRATO — EL CENTINELA, EN LOS SEIS
                # CAMPOS DEL REGISTRO. Escrita a mano A PROPÓSITO: el esquema solo
                # lo impide en algunos, y solo por patrón (hueco declarado en
                # SPEC.md que cubre la herramienta). La regla central dice «nunca
                # en los 6»: `producer: "UNKNOWN"` —declarado en `unknown` con su
                # motivo— satisfacía la partición y pasaba APROBADO. Se comprueban
                # los 6, sin excepción.
                for _c in CAMPOS_REGISTRO:
                    if _c in ("known", "unknown"):
                        continue          # ya comprobados arriba, con más detalle
                    if f.get(_c) == CENTINELA:
                        problemas.append(
                            f"{etq}: BLOQUEANTE — '{_c}' vale \"UNKNOWN\" y es un campo del "
                            f"REGISTRO: el centinela NUNCA se admite en los 6 campos de "
                            f"identidad y contabilidad del sobre (claim_id, known, unknown, "
                            f"unknown_reason, producer, schema_version)")

                # (3.ter) C2 — cada clave de 'unknown_reason' debe estar en 'unknown'.
                # El esquema NO expresa esta regla (deja las claves de
                # `unknown_reason` libres), así que sigue escrita a mano.
                razones = f.get("unknown_reason")
                if isinstance(razones, dict) and isinstance(desconocido, list):
                    fuera = [k for k in razones if k not in desconocido]
                    if fuera:
                        problemas.append(
                            f"{etq}: C2 — 'unknown_reason' explica campos que no están "
                            f"en 'unknown': {fuera}")

                # (4) VALORES DE LAS LISTAS CERRADAS — ya no hay copia a mano.
                #
                # CORRECCIÓN 2026-09-26 (M-T2b): aquí vivía un bucle con cuatro
                # conjuntos escritos a mano (`AUTORIDADES`, `VERIFICACION`,
                # `CONFIANZA`, `RECONCILIACION`) y, aparte, `SUJETOS` para
                # `subject.type`. Eran copias de las enumeraciones del esquema y se
                # olvidaron del centinela "UNKNOWN", así que RECHAZABAN
                # `authority: "UNKNOWN"` —que el contrato admite (A1)—. Ahora las
                # comprueba `validar_esquema` contra el `enum` del propio esquema,
                # en cualquier nivel: `authority`, `verification_status`,
                # `confidence`, `reconciliation_status`, `subject.type`,
                # `container.type`, `instrument.kind`, `freshness.status`,
                # `source_type` y los elementos de `known`/`unknown`.

                # (5) LA REGLA BLOQUEANTE — escrita a mano A PROPÓSITO.
                # El esquema la expresa con `if`/`then` (y `validar_esquema` la
                # aplica), pero el contrato la declara BLOQUEANTE y el mensaje debe
                # nombrarla así: «hay 'unknown' sin 'unknown_reason'». Se mantiene.
                if f.get("unknown") and not f.get("unknown_reason"):
                    problemas.append(f"{etq}: BLOQUEANTE — hay 'unknown' sin 'unknown_reason'")

                # (6) Acumular autoridades de CADA ficha.
                # El conjunto de valores válidos lo declara el `enum` del esquema y
                # ya lo comprobó `validar_esquema`; aquí solo se cuentan las
                # autoridades ESTABLECIDAS (el centinela no es una autoridad) para
                # el mínimo de diversidad que cada proyecto declara.
                if isinstance(f.get("authority"), str) and f["authority"] not in ("", CENTINELA):
                    autoridades.add(f["authority"])

                # (7) Acumular los valores de los mínimos CUALITATIVOS.
                #
                # `container` puede ser el centinela (la ficha entera no está
                # establecida) o un objeto; solo cuenta una `chain` establecida.
                # `source_type` puede ser "UNKNOWN": no es un dominio probado.
                # Y un «hueco declarado» es una ficha cuyo campo `unknown` —la
                # lista de lo que NO está establecido— no está vacío.
                _cont = f.get("container")
                if isinstance(_cont, dict):
                    _cad = _cont.get("chain")
                    if isinstance(_cad, str) and _cad not in ("", CENTINELA):
                        cadenas.add(_cad)
                _st = f.get("source_type")
                if isinstance(_st, str) and _st not in ("", CENTINELA):
                    tipos_fuente.add(_st)
                if isinstance(f.get("unknown"), list) and f["unknown"]:
                    fichas_con_hueco += 1

            if problemas:
                errores += fallo(f"{p.name}: {len(problemas)} problema(s)")
                for x in problemas[:12]:
                    print(f"      - {x}")
                if len(problemas) > 12:
                    print(f"      ... y {len(problemas)-12} más")
            else:
                ok(f"{p.name}: {len(fichas)} ficha(s) correcta(s)")

        # ── 3. Número mínimo de fichas ──
        # Un archivo puede traer varias fichas dentro. El mínimo es un requisito
        # del proyecto, no una regla del sobre: se declara, no se supone.
        print("\n[3] NÚMERO DE FICHAS")
        if not fichas_min:
            print(f"  — no exigido: {etiq_min} no declara mínimo de "
                  f"fichas. Hay {total_fichas}.")
        elif total_fichas >= fichas_min:
            ok(f"{total_fichas} fichas en total — cumple el mínimo de {fichas_min} ({fuente_min})")
        else:
            errores += fallo(
                f"solo {total_fichas} ficha(s); {proyecto} declara un mínimo de "
                f"{fichas_min} ({fuente_min}). Un archivo con varias fichas dentro también cuenta.")

        # ── 4. Diversidad de autoridades ──
        # P1 exigía >= 2 para demostrar que el sobre generaliza. NO es una regla
        # universal: P7 tiene una sola autoridad por diseño, porque es UN dominio
        # nuevo, no una muestra de que el sobre sirva en varios.
        print("\n[4] DIVERSIDAD DE AUTORIDADES")
        if not autoridades_min:
            print(f"  — no exigido: {etiq_min} no declara mínimo de "
                  f"autoridades. Hay {len(autoridades)}: {sorted(autoridades)}")
        elif len(autoridades) >= autoridades_min:
            ok(f"{len(autoridades)} autoridades distintas: {sorted(autoridades)} "
               f"— cumple el mínimo de {autoridades_min} ({fuente_min})")
        else:
            errores += fallo(f"solo {len(autoridades)} autoridad(es): {sorted(autoridades)}. "
                             f"{proyecto} declara un mínimo de {autoridades_min} ({fuente_min})")

        # ── 5. Cadenas distintas (`container.chain`) — mínimo CUALITATIVO ──
        # Es el campo que el contrato SÍ tiene para «multi-cadena». P2 lo exige
        # (CHARTER.md:101) y con una sola cadena el recorte pasaba APROBADO.
        # El sobre no tiene ningún campo de «protocolo»: no se inventa uno.
        print("\n[5] CADENAS DISTINTAS (container.chain)")
        if not cadenas_min:
            print(f"  — no exigido: {etiq_min} no declara mínimo de cadenas "
                  f"distintas. Hay {len(cadenas)}: {sorted(cadenas)}")
        elif len(cadenas) >= cadenas_min:
            ok(f"{len(cadenas)} cadena(s) distinta(s) en 'container.chain': {sorted(cadenas)} "
               f"— cumple el mínimo de {cadenas_min} ({fuente_min})")
        else:
            errores += fallo(
                f"solo {len(cadenas)} cadena(s) distinta(s) en el campo 'container.chain': "
                f"{sorted(cadenas)}. {proyecto} declara un mínimo de {cadenas_min} "
                f"({fuente_min}). El centinela \"UNKNOWN\" no cuenta como cadena.")

        # ── 6. Tipos de fuente distintos (`source_type`) — mínimo CUALITATIVO ──
        # P8 exige que el ledger cubra sus dos dominios (CHARTER.md:97); el
        # charter admite «o el que corresponda a cada dominio», así que se exige
        # DIVERSIDAD (>=2 valores), no los dos literales ONCHAIN/PUBLIC_API.
        print("\n[6] TIPOS DE FUENTE DISTINTOS (source_type)")
        if not tipos_fuente_min:
            print(f"  — no exigido: {etiq_min} no declara mínimo de tipos de "
                  f"fuente distintos. Hay {len(tipos_fuente)}: {sorted(tipos_fuente)}")
        elif len(tipos_fuente) >= tipos_fuente_min:
            ok(f"{len(tipos_fuente)} valor(es) distinto(s) en 'source_type': {sorted(tipos_fuente)} "
               f"— cumple el mínimo de {tipos_fuente_min} ({fuente_min})")
        else:
            errores += fallo(
                f"solo {len(tipos_fuente)} valor(es) distinto(s) en el campo 'source_type': "
                f"{sorted(tipos_fuente)}. {proyecto} declara un mínimo de {tipos_fuente_min} "
                f"({fuente_min}). El centinela \"UNKNOWN\" no cuenta como dominio.")

        # ── 7. Huecos declarados (`unknown` no vacío) — mínimo CUALITATIVO ──
        # P7 exige que al menos una ficha declare un hueco (CHARTER.md:184). Es
        # el mínimo que más importa: una ficha sin ningún hueco no está
        # «completa», está sin auditar (axioma A3).
        print("\n[7] HUECOS DECLARADOS (fichas con 'unknown' no vacío)")
        if not huecos_min:
            print(f"  — no exigido: {etiq_min} no declara mínimo de fichas con "
                  f"hueco. Hay {fichas_con_hueco}.")
        elif fichas_con_hueco >= huecos_min:
            ok(f"{fichas_con_hueco} ficha(s) con 'unknown' no vacío — cumple el mínimo "
               f"de {huecos_min} ({fuente_min})")
        else:
            errores += fallo(
                f"solo {fichas_con_hueco} ficha(s) con 'unknown' no vacío — y 'unknown' es "
                f"la lista de los campos NO establecidos. {proyecto} declara un mínimo de "
                f"{huecos_min} ({fuente_min}).")

    # ── Resultado ──
    #
    # AVISO OBLIGATORIO (revisión 2, hallazgo 3): si hay fichas pero la carpeta no
    # se reconoce como un proyecto declarado, NO se comprobaron sus mínimos — y el
    # código de salida sigue siendo 0, porque lo que sí se comprobó está bien. Eso
    # puede leerse como «todo bien» cuando en realidad **falta una comprobación**.
    # Así que se dice en voz alta, justo antes del resultado: la diferencia entre
    # «no se le pedía» y «no se miró» tiene que verse.
    if ejemplos and not hay_minimos and not proyecto:
        print("\n  ℹ️  MÍNIMOS POR PROYECTO: no se aplican en esta carpeta.")
        print("      Que haya un número mínimo de fichas, o que vengan de fuentes distintas,")
        print("      es un requisito de CADA proyecto, y se declara en su propio registro.")
        print("      Esta carpeta no trae ese registro, así que no se le exige ninguno: el")
        print("      resultado de abajo NO afirma nada sobre ese punto.")
        print("      Lo que sí se comprobó, ficha por ficha: las 22 casillas, los valores")
        print("      permitidos y las claves que el contrato no admite.")

    # H-6: el caso de la MENCIÓN. Se repite aquí, junto al resultado, porque es
    # donde se lee el veredicto: un APROBADO sin mínimos comprobados no puede
    # parecer un APROBADO con ellos.
    if ejemplos and por_mencion:
        print(f"\n  ⚠️  MÍNIMOS NO APLICADOS: {proyecto} se identificó por MENCIONES en el")
        print("      CHARTER.md, no por el nombre de la carpeta. Sus mínimos NO se han")
        print("      comprobado: un APROBADO de arriba NO afirma que los cumpla. Para")
        print("      comprobarlos, la carpeta tiene que llamarse como el proyecto.")

    print("\n" + "=" * 60)
    if errores == 0:
        if not ejemplos:
            print("RESULTADO: NO APLICA — no hay ninguna ficha del sobre que comprobar "
                  "en esta carpeta. NO significa que esté bien: significa que este "
                  "validador no la ha mirado.")
            return 3
        print("RESULTADO: APROBADO — todo lo aplicable pasa")
        return 0
    print(f"RESULTADO: {errores} PROBLEMA(S) — hay que corregir antes de reportar")
    return 1


if __name__ == "__main__":
    sys.exit(main())
