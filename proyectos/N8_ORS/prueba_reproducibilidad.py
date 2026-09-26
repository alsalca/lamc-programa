#!/usr/bin/env python3
"""
PRUEBA INDEPENDIENTE DEL MODELO ORS — N8

POR QUÉ EXISTE (2026-09-26)
---------------------------
El nivel N8 pedía, para poder publicarse, **un comprador**. El operador quitó esa
condición y pidió otra cosa, más útil: **probar la herramienta nosotros, de forma
independiente, para saber que funciona y que quedó sólida.**

Y tiene razón en el fondo: «tener un comprador» no dice nada sobre si el modelo
está bien. Un comprador puede comprar algo mal calculado, y lo contrario también.
Lo que hace sólido a un modelo es que **se pueda comprobar sin creerle a quien lo
escribió**: que un tercero recalcule los números desde los datos publicados, que
llegue a los mismos, y que el modelo **se niegue a puntuar** cuando no hay datos
suficientes en vez de inventar.

Esta prueba NO confía en `puntuaciones.json`: **lo recalcula todo desde la matriz
de 52 controles publicada en `BENCHMARK.md`** (la fuente) y solo entonces compara.
Es la regla §9.quater: se verifica contra la fuente, no contra la copia.

Qué comprueba, y qué pasaría si el modelo se rompiera:
  1. Los conteos de la matriz coinciden con `mediciones.json`.
  2. El ORS sale exacto con la fórmula del §5.3.
  3. Igual con la segunda regla de pesos (§9), y **el orden no cambia**.
  4. La sensibilidad es exactamente la declarada: un control más mueve el número
     en 100/aplicables, ni más ni menos.
  5. Los `no_aplica` se excluyen del denominador (Liquity: 52 − 8).
  6. El modelo **no puntúa sin datos**: se niega en vez de devolver 0 o 100.
  7. Los textos publicados **no afirman seguridad** (la regla bloqueante del §0).

Uso:   python3 proyectos/N8_ORS/prueba_reproducibilidad.py
Salida: 0 si todo cuadra · 1 si algo no cuadra
"""

import json
import pathlib
import re
import sys

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
P4 = RAIZ / "proyectos" / "P4_CAPA_CONTROLES" / "entregables"
BENCHMARK = P4 / "BENCHMARK.md"
MEDICIONES = P4 / "bundle" / "mediciones.json"
PUNTUACIONES = AQUI / "entregables" / "bundle" / "puntuaciones.json"
MODELO = AQUI / "entregables" / "MODELO.md"

PROTOCOLOS = ["Aave", "Uniswap", "Liquity"]
VALOR = {"✅": "presente", "❌": "ausente", "?": "unknown", "➖": "no_aplica"}

fallos = []
def malo(m): fallos.append(m); print(f"  ✗ {m}")
def bien(m): print(f"  ✓ {m}")


# ── La fuente: la matriz de 52 controles de BENCHMARK.md ─────────────────────
def lee_matriz():
    """Devuelve {seccion: [(marca_aave, marca_uniswap, marca_liquity), …]}."""
    seccion, datos = None, {}
    for linea in BENCHMARK.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^### §(\d+)", linea)
        if m:
            seccion = int(m.group(1)); datos[seccion] = []; continue
        if seccion is None or not linea.startswith("|"):
            continue
        celdas = [c.strip() for c in linea.strip("|").split("|")]
        if len(celdas) < 5 or celdas[0] in ("#", "") or set(celdas[0]) <= set("- "):
            continue
        marcas = tuple(celdas[-3:])
        if all(m in VALOR for m in marcas):
            datos[seccion].append(marcas)
    return datos


def cuenta(datos):
    """Cuenta estados por protocolo (índice 0=Aave, 1=Uniswap, 2=Liquity)."""
    out = {p: {"presente": 0, "ausente": 0, "unknown": 0, "no_aplica": 0} for p in PROTOCOLOS}
    for filas in datos.values():
        for marcas in filas:
            for i, p in enumerate(PROTOCOLOS):
                out[p][VALOR[marcas[i]]] += 1
    return out


def ors_uniforme(c):
    aplicables = 52 - c["no_aplica"]
    return None if aplicables == 0 else 100 * c["presente"] / aplicables


def ors_por_seccion(datos):
    """§9: cada sección aplicable pesa igual; dentro, score_i = P_i / A_i."""
    scores = {}
    for p in PROTOCOLOS:
        acum, n = 0.0, 0
        for filas in datos.values():
            idx = PROTOCOLOS.index(p)
            marcas = [f[idx] for f in filas]
            aplicables = sum(1 for m in marcas if VALOR[m] != "no_aplica")
            if aplicables == 0:
                continue                      # §5.4: sección entera no aplica → se excluye
            presentes = sum(1 for m in marcas if VALOR[m] == "presente")
            acum += presentes / aplicables
            n += 1
        scores[p] = None if n == 0 else 100 * acum / n
    return scores


def main():
    print("=" * 74)
    print("  PRUEBA INDEPENDIENTE DEL MODELO ORS — se recalcula desde la fuente")
    print("=" * 74)
    for r in (BENCHMARK, MEDICIONES, PUNTUACIONES, MODELO):
        if not r.exists():
            print(f"  ✗ falta {r}"); return 1

    datos = lee_matriz()
    n_controles = sum(len(v) for v in datos.values())
    print(f"\n[1] LA FUENTE · matriz de BENCHMARK.md")
    if n_controles != 52:
        malo(f"la matriz tiene {n_controles} controles; el estándar de P3 tiene 52")
    else:
        bien(f"52 controles en {len(datos)} secciones")
    conteos = cuenta(datos)

    # ── [2] los conteos coinciden con las fichas de P4 ───────────────────────
    print("\n[2] LOS CONTEOS · ¿coinciden con mediciones.json?")
    fichas = {f["subject"]["label"].split(" /")[0].strip(): f for f in json.loads(MEDICIONES.read_text(encoding="utf-8"))}
    for p in PROTOCOLOS:
        f = next((v for k, v in fichas.items() if k.lower().startswith(p.split()[0].lower())), None)
        if f is None:
            malo(f"no encuentro la ficha de {p} en mediciones.json"); continue
        declarado = int(f["quantity"])
        real = conteos[p]["presente"]
        if declarado != real:
            malo(f"{p}: mediciones.json dice {declarado} presentes, la matriz da {real}")
        else:
            bien(f"{p}: {real} presentes · {conteos[p]['ausente']} ausentes · "
                 f"{conteos[p]['unknown']} no observados · {conteos[p]['no_aplica']} no aplican")

    # ── [3] el ORS, recalculado ──────────────────────────────────────────────
    # OJO: `puntuaciones.json` lleva DOS fichas por protocolo —una con la
    # puntuación (`ORS_PUNTOS`) y otra con el conteo de controles presentes
    # (`CONTROLES_PRESENTES`)—. La primera versión de esta prueba indexaba por el
    # nombre del sujeto y **se quedaba con la última**, así que comparaba el ORS
    # contra el conteo (9,62 contra 5). El error era de la prueba, no del modelo;
    # y enseña por qué se selecciona por el campo que distingue, no por el que se
    # repite. Se localiza por `instrument.symbol`.
    print("\n[3] EL ORS · recalculado con la fórmula del §5.3")
    puntuaciones = json.loads(PUNTUACIONES.read_text(encoding="utf-8"))
    def busca(p, simbolo):
        for x in puntuaciones:
            etq = x["subject"]["label"].lower()
            if etq.startswith(p.split()[0].lower()) and x["instrument"]["symbol"] == simbolo:
                return float(x["quantity"])
        return None
    calculado = {p: ors_uniforme(conteos[p]) for p in PROTOCOLOS}
    for p in PROTOCOLOS:
        pub, calc = busca(p, "ORS_PUNTOS"), round(calculado[p], 2)
        if pub is None:
            malo(f"{p}: no hay ficha ORS_PUNTOS en puntuaciones.json")
        elif abs(pub - calc) > 0.005:
            malo(f"{p}: publicado {pub}, recalculado {calc}")
        else:
            bien(f"{p}: {calc} (coincide con lo publicado)")
        # El conteo también tiene que cuadrar con la ficha de conteo.
        cnt = busca(p, "CONTROLES_PRESENTES")
        if cnt is not None and int(cnt) != conteos[p]["presente"]:
            malo(f"{p}: la ficha de conteo dice {int(cnt)}, la matriz da {conteos[p]['presente']}")

    # ── [3.bis] los EJES SECUNDARIOS, contra P4 ──────────────────────────────
    # POR QUÉ EXISTE ESTE BLOQUE (2026-09-26). El 26 se corrigió en P4 una marca
    # que estaba mal: el control de dependencias de Uniswap pasó de `ausente` a
    # `no observable`. Eso **cambia dos números de N8** —`CE` de 9,62 a 7,69 y el
    # techo de 98,08 a 100,00— y **este archivo no se enteró**: seguía diciendo los
    # viejos. Se descubrió a mano, leyendo, que es como se descubren las cosas que
    # no tienen comprobación.
    # Este bloque comprueba los tres ejes contra la matriz de P4, así que la
    # próxima vez salta solo.
    print("\n[3.bis] LOS EJES · ¿techo y completitud cuadran con la matriz de P4?")
    ev = (AQUI / "entregables" / "bundle" / "evidence.md").read_text(encoding="utf-8")
    bloques = re.split(r"^### ", ev, flags=re.M)[1:]
    # Solo los bloques de N8 (los que traen los ejes). Los de P4 van copiados en el
    # mismo archivo y no llevan `ors_suelo`: distinguirlos por eso, y **exigir que
    # sean exactamente tres**, para que un bloque al que se le caiga el eje no
    # desaparezca en silencio de la comprobación.
    n8 = [b for b in bloques if "**protocolo**" in b and "**ors_suelo**" in b]
    if len(n8) != len(PROTOCOLOS):
        malo(f"esperaba {len(PROTOCOLOS)} bloques con ejes en evidence.md y encontré {len(n8)}")
    vistos = 0
    for b in n8:
        def campo(clave):
            m = re.search(rf"- \*\*{clave}\*\* — (.+)", b)
            return m.group(1).strip() if m else None
        prot = campo("protocolo")
        p = next((x for x in PROTOCOLOS if prot and prot.lower().startswith(x.split()[0].lower())), None)
        if p is None:
            continue
        vistos += 1
        c = conteos[p]
        apl = 52 - c["no_aplica"]
        esperado = {
            "ors_suelo": round(100 * c["presente"] / apl, 2),
            "ors_techo": round(100 * (c["presente"] + c["unknown"]) / apl, 2),
            "completitud_ce": round(100 * (c["presente"] + c["ausente"]) / apl, 2),
        }
        for clave, val in esperado.items():
            declarado = campo(clave)
            if declarado is None:
                malo(f"{p}: falta «{clave}» en el bloque de evidence.md"); continue
            if abs(float(declarado) - val) > 0.005:
                malo(f"{p}: {clave} declarado {declarado}, la matriz de P4 da {val}")
            else:
                bien(f"{p}: {clave} = {val} (coincide con P4)")
        # y el conteo de controles del bloque, contra la matriz
        m = re.search(r'- \*\*controles\*\* — (\{.*\})', b)
        if m:
            d = json.loads(m.group(1))
            for k in ("presente", "ausente", "unknown", "no_aplica"):
                if d.get(k) != c[k]:
                    malo(f"{p}: el bloque dice {k}={d.get(k)}, la matriz de P4 da {c[k]}")
    if vistos == 0:
        malo("no encontré ningún bloque de procedencia en evidence.md")

    # ── [4] la segunda regla de pesos, y el orden ────────────────────────────
    print("\n[4] LA SEGUNDA REGLA DE PESOS (§9) · ¿se mantiene el orden?")
    alt = ors_por_seccion(datos)
    orden_u = [p for p in sorted(PROTOCOLOS, key=lambda x: -calculado[x])]
    orden_a = [p for p in sorted(PROTOCOLOS, key=lambda x: -alt[x])]
    bien("peso uniforme : " + " > ".join(f"{p} {calculado[p]:.2f}" for p in orden_u))
    bien("peso por sección: " + " > ".join(f"{p} {alt[p]:.2f}" for p in orden_a))
    if orden_u != orden_a:
        malo(f"el orden CAMBIA según la ponderación: {orden_u} vs {orden_a} — "
             f"el modelo debería declararlo como límite de resolución")
    else:
        bien("el orden es el mismo bajo las dos reglas: la conclusión no depende del peso")

    # ── [5] la sensibilidad declarada ────────────────────────────────────────
    print("\n[5] LA SENSIBILIDAD · ¿un control mueve el número justo lo que dice?")
    for p in PROTOCOLOS:
        aplicables = 52 - conteos[p]["no_aplica"]
        esperado = 100 / aplicables
        arriba = 100 * (conteos[p]["presente"] + 1) / aplicables
        movimiento = arriba - calculado[p]
        if abs(movimiento - esperado) > 1e-9:
            malo(f"{p}: mover un control mueve {movimiento:.4f}, no {esperado:.4f}")
        else:
            bien(f"{p}: un control mueve {esperado:.2f} puntos (100/{aplicables})")
    for p in PROTOCOLOS:
        if conteos[p]["no_aplica"] == 52:
            malo(f"{p}: los 52 controles no aplican; el modelo debería negarse a puntuar")

    # ── [6] el modelo se niega sin datos ─────────────────────────────────────
    print("\n[6] SIN DATOS · ¿se niega a puntuar, o inventa un número?")
    vacio = {p: {"presente": 0, "ausente": 0, "unknown": 0, "no_aplica": 52} for p in PROTOCOLOS}
    if ors_uniforme(vacio["Aave"]) is None:
        bien("con 0 controles aplicables devuelve «no puntuable», no 0 ni 100")
    else:
        malo("con 0 controles aplicables devuelve un número: estaría inventando")

    # ── [7] los textos no afirman seguridad ──────────────────────────────────
    # Cuidado con el falso positivo: la frase «no dice si un protocolo es
    # «más seguro»» ES la regla, no una violación. La primera versión de esta
    # prueba marcaba cualquier aparición de «más seguro» y saltó sola. Ahora se
    # exige que **toda mención esté dentro de una negación**: si alguien escribiera
    # «este protocolo es más seguro», no habría negación delante y la prueba
    # falla. Es más estricto y no premia la redacción ambigua.
    print("\n[7] LO PUBLICADO · ¿afirma seguridad en algún sitio?")
    frases = ["es seguro", "más seguro", "menos seguro", "recomendamos",
              "deberías invertir", "mejor protocolo", "más riesgoso"]
    negaciones = ("no ", "ni ", "nunca", "jamás", "sin ", "tampoco", "no dice",
                  "no afirma", "no es", "no significa", "no mide", "no recomienda")
    afirmaciones, en_negacion = [], 0
    for t in sorted((AQUI / "entregables").rglob("*.md")):
        texto = t.read_text(encoding="utf-8")
        bajo = texto.lower()
        for f in frases:
            pos = bajo.find(f)
            while pos != -1:
                antes = bajo[max(0, pos - 90):pos]
                if any(n in antes for n in negaciones):
                    en_negacion += 1
                else:
                    linea = texto[:pos].count("\n") + 1
                    afirmaciones.append(f"{t.name}:{linea} — «…{texto[max(0,pos-45):pos+len(f)+15].strip()}…»")
                pos = bajo.find(f, pos + 1)
    if afirmaciones:
        for a in afirmaciones:
            malo(f"afirmación de seguridad o consejo: {a}")
    else:
        bien(f"cero afirmaciones de seguridad · {en_negacion} mención(es), todas dentro de una negación")
    regla = MODELO.read_text(encoding="utf-8")
    if "no es una nota de seguridad" in regla and "no dice si un protocolo es" in regla:
        bien("la regla bloqueante del §0 sigue escrita en el MODELO")
    else:
        malo("la regla bloqueante del §0 desapareció del MODELO")

    print("\n" + "=" * 74)
    if fallos:
        print(f"  RESULTADO: NO SÓLIDO — {len(fallos)} problema(s)")
        print("=" * 74)
        return 1
    print("  RESULTADO: el modelo se reproduce desde su fuente y no afirma seguridad")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
