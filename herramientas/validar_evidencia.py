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

CÓDIGOS DE SALIDA:
    0  APROBADO        — todo lo aplicable pasa
    1  PROBLEMAS       — hay algo que corregir
    2  ERROR DE USO    — falta la carpeta o el argumento
    3  NO APLICA       — no hay nada que este validador pueda comprobar aquí
                         (por ejemplo un proyecto de documentos de texto)

El 3 existe para que «no se comprobó nada» NUNCA se lea como «está bien».
"""

import json
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

AUTORIDADES = {"PUBLIC_CHAIN", "INSTITUTION", "INSTITUTION_DOCUMENT", "HUMAN", "DERIVED"}
VERIFICACION = {"deterministic", "authenticated", "documentary", "unverified"}
CONFIANZA = {"high", "medium", "low"}
RECONCILIACION = {"unreconciled", "reconciled", "disputed"}
SUJETOS = {"NATURAL_PERSON", "LEGAL_ENTITY", "GROUP"}

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

# Campos que no describen el hecho en sí, sino la contabilidad del propio sobre.
# No cuentan para exigir que «al menos algo esté establecido».
CAMPOS_CONTABLES = ("known", "unknown", "unknown_reason")

# Estos dos PUEDEN estar vacíos con legitimidad cuando no hay nada desconocido:
# `unknown: []` es correcto si todo está establecido, y `unknown_reason: {}`
# es correcto entonces. `known` nunca puede estar vacío (algo debe afirmarse).
CAMPOS_QUE_PUEDEN_IR_VACIOS = ("unknown", "unknown_reason")

VACIO = (None, "", [], {})


def esta_establecido(campo, valor):
    """¿El campo tiene un valor establecido, o declara no saberlo?"""
    return valor != CENTINELA


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
    """Qué proyecto del registro es esta carpeta, si lo es.

    Se mira la carpeta y sus padres: así funciona tanto si se le pasa la raíz
    del proyecto como si se le pasa `entregables/` o `entregables/bundle/`.
    Si no coincide con ninguno, devuelve (None, {}) — y entonces no se exige
    ningún mínimo, en vez de aplicar los de otro.

    ── CORRECCIÓN 2026-09-25 (auditoría, revisión 2, hallazgo 3) ──
    Identificar al proyecto **solo por el nombre de su carpeta** dejaba un hueco
    silencioso: P4 recortado a 1 ficha y copiado como `P4_RENOMBRADO` daba
    **APROBADO (exit 0)**, porque con otro nombre no se le exigía su mínimo. Una
    copia, un ZIP o un checkout con otro nombre se aprobaban sin sus mínimos.

    Un proyecto no se reconoce solo por cómo se llama su carpeta: se reconoce
    **por lo que él mismo declara**. Así que, si el nombre no coincide, se lee su
    `CHARTER.md` y se busca qué proyecto se nombra en él. Se elige el que más
    veces aparece, para que una mención de pasada a otro proyecto no confunda.
    """
    for p in (carpeta, *carpeta.parents):
        if p.name in registro:
            return p.name, registro[p.name]

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
            return mejor, registro[mejor]
    return None, {}


def _props_permitidas(esq):
    """Nombres de propiedad que un esquema admite, mirando también sus ramas."""
    props = dict(esq.get("properties", {}))
    for rama in esq.get("anyOf", []) + esq.get("allOf", []) + esq.get("oneOf", []):
        if isinstance(rama, dict):
            props.update(_props_permitidas(rama))
    return props


def _subesquema(esq, clave):
    """El subesquema que describe `clave`, buscando también en las ramas."""
    if clave in esq.get("properties", {}):
        return esq["properties"][clave]
    for rama in esq.get("anyOf", []) + esq.get("allOf", []) + esq.get("oneOf", []):
        if isinstance(rama, dict):
            r = _subesquema(rama, clave)
            if r:
                return r
    return None


def claves_prohibidas(instancia, esq, ruta=""):
    """Claves que el contrato NO admite, allí donde declara `additionalProperties: false`.

    POR QUÉ ESTA COMPROBACIÓN FALTABA (2026-09-25)
    ----------------------------------------------
    El esquema publicado prohíbe claves no declaradas en 5 sitios. El validador
    **no lo comprobaba**, así que decía APROBADO sobre:
      - los 4 ejemplos publicados, que llevaban `_example` en la raíz
      - los bundles de P7, P8, P4 y N8, que llevaban `_meta` dentro de cada ficha

    Lo encontró una auditoría independiente, no la herramienta. Es L-02 y L-15
    otra vez: **un validador más laxo que el contrato no valida, aprueba.**
    Y era peor que un fallo aislado: los ejemplos son el modelo que un tercero
    copia, y no pasaban su propio contrato.

    `additionalProperties` solo mira las propiedades declaradas EN EL MISMO
    objeto del esquema —no las de las ramas `allOf`/`anyOf`, que es la trampa
    clásica—, así que para las ramas se usa la unión de lo que admiten: una
    clave se tolera si alguna rama la declara, y se reporta si no la declara
    ninguna.
    """
    problemas = []
    if not isinstance(esq, dict) or not isinstance(instancia, (dict, list)):
        return problemas

    if isinstance(instancia, dict):
        ramas = [r for r in (esq.get("anyOf", []) + esq.get("allOf", [])
                             + esq.get("oneOf", [])) if isinstance(r, dict)]
        prohibe = (esq.get("additionalProperties") is False
                   or any(r.get("additionalProperties") is False for r in ramas))
        if prohibe:
            admitidas = _props_permitidas(esq)
            for k in instancia:
                if k not in admitidas:
                    problemas.append(f"{ruta}.{k}" if ruta else str(k))
        for k, v in instancia.items():
            sub = _subesquema(esq, k)
            if sub:
                problemas += claves_prohibidas(v, sub, f"{ruta}.{k}" if ruta else k)
    else:
        items = esq.get("items", {})
        for i, v in enumerate(instancia):
            problemas += claves_prohibidas(v, items, f"{ruta}[{i}]")
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
    proyecto, info = proyecto_de(carpeta, registro)
    val = info.get("validacion", {}) if isinstance(info.get("validacion"), dict) else {}
    ejemplos_min = val.get("ejemplos_min", 0)
    fichas_min = val.get("fichas_min", 0)
    autoridades_min = val.get("autoridades_min", 0)
    fuente_min = val.get("_fuente", "sin declarar")

    errores = 0
    print(f"\nVALIDADOR DE EVIDENCIA — {carpeta.name}")
    print("=" * 60)
    if proyecto:
        print(f"  proyecto declarado: {proyecto} "
              f"(mínimos: ejemplos={ejemplos_min} fichas={fichas_min} "
              f"autoridades={autoridades_min} · {fuente_min})")
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
        if ejemplos_min:
            errores += fallo(f"no encontré ejemplos (*.json) y {proyecto or 'este proyecto'} "
                             f"declara un mínimo de {ejemplos_min} ({fuente_min})")
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

                # (0) El contrato prohíbe claves no declaradas. Se comprueba.
                if esquema is not None:
                    sobrantes_esq = claves_prohibidas(f, esquema)
                    if sobrantes_esq:
                        problemas.append(
                            f"{etq}: claves que el contrato NO admite "
                            f"(`additionalProperties: false`): {sobrantes_esq}")

                # (1) TODOS los 22 campos deben existir y ser no vacíos.
                #     El centinela "UNKNOWN" ES contenido válido (§ regla central).
                #     Excepción: `unknown` y `unknown_reason` pueden estar vacíos
                #     cuando no hay nada desconocido que declarar.
                for c in CAMPOS:
                    if c not in f:
                        problemas.append(f"{etq}: falta el campo: {c}")
                        continue
                    if c in CAMPOS_QUE_PUEDEN_IR_VACIOS:
                        continue
                    if f[c] in VACIO and f[c] != CENTINELA:
                        problemas.append(f"{etq}: vacío: {c}")

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

                # (3.bis) PARTICIPACIÓN known / unknown — reglas C5, C6 y C7 de SPEC.md
                # Incorporadas el 2026-09-21 a propuesta de quien construyo el entregable, que las
                # detectó con una comprobación propia. El validador era más laxo que el
                # contrato: aprobaba fichas con solapes y con huecos escondidos.
                conocido = f.get("known")
                desconocido = f.get("unknown")

                # (3.bis.0) LO QUE NO PUEDE SER UNA LISTA, NO ES UNA LISTA.
                #
                # CORRECCIÓN 2026-09-23 (puerta de publicación): antes, si 'known'
                # no era una lista, TODAS las comprobaciones C5/C6/C7 de abajo se
                # SALTABAN EN SILENCIO — el `if isinstance(...)` de la línea
                # siguiente era la única puerta. Una ficha con `known: "UNKNOWN"`
                # —el centinela en un campo del REGISTRO, prohibido— pasaba el
                # validador sin que se mirara NADA, y salía APROBADO.
                #
                # FALLAR ABIERTO es peor que fallar: la comprobación PARECE hecha.
                # Cinco pruebas ciegas no lo vieron porque probaban el CONTRATO,
                # no la HERRAMIENTA. Lo encontró un ataque contra el propio
                # validador: 13 fichas malformadas, una pasó.
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

                if isinstance(conocido, list) and isinstance(desconocido, list):
                    # C6 — 'unknown' solo admite nombres de campo de PRIMER nivel
                    anidados = [x for x in desconocido if isinstance(x, str) and "." in x]
                    if anidados:
                        problemas.append(
                            f"{etq}: C6 — 'unknown' solo admite campos de primer nivel; "
                            f"usa 'unknown_detail' para: {anidados}")

                    # C5 — sin elementos compartidos
                    solape = set(conocido) & set(desconocido)
                    if solape:
                        problemas.append(
                            f"{etq}: C5 — el mismo campo en 'known' y en 'unknown': {sorted(solape)}")

                    # C7 — la unión debe ser EXACTAMENTE los 22 campos
                    faltantes = set(CAMPOS) - set(conocido) - set(desconocido)
                    sobrantes = (set(conocido) | set(desconocido)) - set(CAMPOS)
                    if faltantes:
                        problemas.append(
                            f"{etq}: C7 — huecos escondidos (no están en ninguna lista): "
                            f"{sorted(faltantes)}")
                    if sobrantes:
                        problemas.append(
                            f"{etq}: C7 — nombres que no son campos del sobre: {sorted(sobrantes)}")

                # (3.ter) C2 — cada clave de 'unknown_reason' debe estar en 'unknown'
                razones = f.get("unknown_reason")
                if isinstance(razones, dict) and isinstance(desconocido, list):
                    fuera = [k for k in razones if k not in desconocido]
                    if fuera:
                        problemas.append(
                            f"{etq}: C2 — 'unknown_reason' explica campos que no están "
                            f"en 'unknown': {fuera}")

                # (4) Valores dentro de las listas permitidas
                for campo, permitidos in (("authority", AUTORIDADES),
                                          ("verification_status", VERIFICACION),
                                          ("confidence", CONFIANZA),
                                          ("reconciliation_status", RECONCILIACION)):
                    v = f.get(campo)
                    if v and v not in permitidos:
                        problemas.append(f"{etq}: {campo}={v!r} no está permitido")

                # (5) subject: exactamente un sujeto, de tipo válido
                s = f.get("subject")
                if isinstance(s, dict):
                    if s.get("type") not in SUJETOS:
                        problemas.append(f"{etq}: subject.type={s.get('type')!r} no está permitido")
                elif s:
                    problemas.append(f"{etq}: subject debe ser un objeto con 'type'")

                # (6) LA REGLA BLOQUEANTE
                if f.get("unknown") and not f.get("unknown_reason"):
                    problemas.append(f"{etq}: BLOQUEANTE — hay 'unknown' sin 'unknown_reason'")

                # (7) Acumular autoridades de CADA ficha
                if f.get("authority") in AUTORIDADES:
                    autoridades.add(f["authority"])

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
            print(f"  — no exigido: {proyecto or 'esta carpeta'} no declara mínimo de "
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
            print(f"  — no exigido: {proyecto or 'esta carpeta'} no declara mínimo de "
                  f"autoridades. Hay {len(autoridades)}: {sorted(autoridades)}")
        elif len(autoridades) >= autoridades_min:
            ok(f"{len(autoridades)} autoridades distintas: {sorted(autoridades)} "
               f"— cumple el mínimo de {autoridades_min} ({fuente_min})")
        else:
            errores += fallo(f"solo {len(autoridades)} autoridad(es): {sorted(autoridades)}. "
                             f"{proyecto} declara un mínimo de {autoridades_min} ({fuente_min})")

    # ── Resultado ──
    #
    # AVISO OBLIGATORIO (revisión 2, hallazgo 3): si hay fichas pero la carpeta no
    # se reconoce como un proyecto declarado, NO se comprobaron sus mínimos — y el
    # código de salida sigue siendo 0, porque lo que sí se comprobó está bien. Eso
    # puede leerse como «todo bien» cuando en realidad **falta una comprobación**.
    # Así que se dice en voz alta, justo antes del resultado: la diferencia entre
    # «no se le pedía» y «no se miró» tiene que verse.
    if ejemplos and not proyecto and not (fichas_min or autoridades_min or ejemplos_min):
        print("\n  ⚠️  NO COMPROBADO: los mínimos de este proyecto (nº de fichas, diversidad")
        print("      de autoridades). La carpeta no se reconoce como un proyecto declarado")
        print("      —ni por su nombre ni por lo que declara su CHARTER.md—, así que no se")
        print("      le exige ninguno. Lo que SÍ se comprobó, ficha por ficha: las 22")
        print("      casillas, los valores permitidos y las claves de más.")

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
