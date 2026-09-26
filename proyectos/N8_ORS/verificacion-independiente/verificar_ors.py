#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificador INDEPENDIENTE del ORS definido en N8_ORS/entregables/MODELO.md.

Reproduce el suelo verificado (§5.3, peso uniforme) y la variante de sensibilidad
(§9, peso igual por seccion) a partir de:
  - el estandar P3 (tamano de cada seccion y lista de controles)
  - los estados por control / conteos publicados por P4 (evidence.md)
  - mediciones.json (se comprueba si contiene o no los estados; NO se usa como
    fuente de estados si no los tiene)

Uso:  python3 verificar_ors.py
No lee ningun archivo del proyecto N8_ORS salvo MODELO.md (no lo necesita para
calcular; la formula esta transcrita aqui abajo).
"""

import json
import re
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

# Ruta relativa a este archivo, para que funcione en cualquier copia del programa
# (antes tenía una ruta absoluta de la máquina del autor: no puede publicarse así).
ROOT = Path(__file__).resolve().parent.parent.parent
MED = ROOT / "P4_CAPA_CONTROLES/entregables/bundle/mediciones.json"
EVID = ROOT / "P4_CAPA_CONTROLES/entregables/bundle/evidence.md"
STD = ROOT / "P3_OPS_SEC/entregables/STANDARD.md"

FORMULA = "ORS = 100 * (sum P_i) / (sum A_i)   [§5.3, peso uniforme]"
FORMULA_SEC = "ORS_sec = 100 * (1/n) * sum(P_i / A_i)  sobre secciones aplicables [§9]"


def r2(x):
    return float(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


# ---------------------------------------------------------------------------
# 1) Estandar P3: seccion -> numero de controles
# ---------------------------------------------------------------------------
std = STD.read_text(encoding="utf-8")
tam = {}
control_seccion = {}
for m in re.finditer(r"^\|\s*(\d+)\.(\d+)\s*\|", std, re.M):
    s = int(m.group(1))
    tam[s] = tam.get(s, 0) + 1
    control_seccion[f"{s}.{m.group(2)}"] = s

assert sum(tam.values()) == 52, f"el estandar no tiene 52 controles: {tam}"
print("Estandar P3: tamano por seccion:", dict(sorted(tam.items())),
      "| total =", sum(tam.values()))

# ---------------------------------------------------------------------------
# 2) mediciones.json: comprobar si trae estados por control
# ---------------------------------------------------------------------------
claims = json.loads(MED.read_text(encoding="utf-8"))
tiene_estados = False
for c in claims:
    plano = json.dumps(c)
    if re.search(r'"(presente|ausente|unknown|no_aplica)"', plano) and \
       any(k not in ("known", "unknown", "unknown_reason") for k in c if "control" in k.lower()):
        tiene_estados = True
print("\nmediciones.json -> fichas:", len(claims),
      "| claves de nivel control:", [k for c in claims for k in c
                                     if any(t in k.lower() for t in ("control", "estado", "seccion"))] or "NINGUNA",
      "| ¿contiene estados por control?:", tiene_estados)
for c in claims:
    print(f"   - {c['claim_id']} {c['subject']['label']}: quantity={c['quantity']}"

          )

# ---------------------------------------------------------------------------
# 3) Conteos agregados desde evidence.md ("Procedencia por ficha")
# ---------------------------------------------------------------------------
ev = EVID.read_text(encoding="utf-8")
bloques = re.split(r"^###\s+`(P4-CTRL-[0-9-]+)`\s*$", ev, flags=re.M)
conteos = {}
for i in range(1, len(bloques), 2):
    cid, cuerpo = bloques[i], bloques[i + 1]
    m = re.search(r"\*\*controles\*\*\s*—\s*(\{[^}]*\})", cuerpo)
    conteos[cid] = json.loads(m.group(1))

# ---------------------------------------------------------------------------
# 4) Estados por control desde las tablas de evidence.md
# ---------------------------------------------------------------------------
def parse_tabla(texto):
    """Devuelve {control_id: estado} de las filas '| §X.Y | veredicto | ...'."""
    out = {}
    patron = re.compile(r"^\|\s*§((?:\d+\.\d+)(?:\s*[–-]\s*\d+\.\d+)?)\s*\|\s*([^|]+?)\s*\|", re.M)
    for m in patron.finditer(texto):
        spec, celda = m.group(1), m.group(2)
        if "no aplica" in celda.lower():
            estado = "no_aplica"
        elif "presente" in celda.lower():
            estado = "presente"
        elif "ausente" in celda.lower():
            estado = "ausente"
        else:
            estado = "unknown"
        ids = re.split(r"\s*[–-]\s*", spec)
        if len(ids) == 2:
            s0, c0 = map(int, ids[0].split("."))
            s1, c1 = map(int, ids[1].split("."))
            for s in range(s0, s1 + 1):
                for c in range(c0 if s == s0 else 1, (c1 if s == s1 else c1) + 1):
                    out[f"{s}.{c}"] = estado
        else:
            out[spec] = estado
    return out


# separar evidence.md por protocolo (orden de las tablas)
partes = re.split(r"^###\s+(AVAA\s*/\s*AAVE DAO|UNISWAP\s*/\s*UNISWAP DAO|LIQUITY \(V1\))\s*$",
                  ev, flags=re.M)
tablas = {}
for i in range(1, len(partes), 2):
    titulo = re.sub(r"\s*/\s*.*", "", partes[i]).strip()
    tablas[titulo] = parse_tabla(partes[i + 1])

orden_prot = [c["claim_id"] for c in claims]
nombres = [c["subject"]["label"] for c in claims]
# el orden de las tablas en evidence.md es Aave, Uniswap, Liquity (igual que las fichas)
tabla_por_claim = dict(zip(orden_prot, list(tablas.values())))

# ---------------------------------------------------------------------------
# 5) Calculo
# ---------------------------------------------------------------------------
filas = []
for cid, nombre in zip(orden_prot, nombres):
    cnt = conteos[cid]
    estados = {}
    for ctrl, s in control_seccion.items():
        estados[ctrl] = tabla_por_claim[cid].get(ctrl, "unknown")

    # coherencia tabla vs conteos agregados
    for est in ("presente", "ausente", "no_aplica"):
        n_tabla = sum(1 for v in estados.values() if v == est)
        assert n_tabla == cnt[est], \
            f"{nombre}: tabla dice {est}={n_tabla}, conteo agregado dice {cnt[est]}"
    assert sum(cnt[k] for k in ("presente", "ausente", "unknown", "no_aplica")) == cnt["total"]

    P = {s: 0 for s in tam}
    NA = {s: 0 for s in tam}
    for ctrl, est in estados.items():
        s = control_seccion[ctrl]
        if est == "presente":
            P[s] += 1
        elif est == "no_aplica":
            NA[s] += 1
    A = {s: tam[s] - NA[s] for s in tam}

    aplicables = sum(A.values())
    presentes = sum(P.values())
    assert aplicables == cnt["total"] - cnt["no_aplica"]
    assert presentes == cnt["presente"]

    ors_uniforme = 100 * presentes / aplicables
    secciones_apl = [s for s in sorted(tam) if A[s] > 0]
    n = len(secciones_apl)
    ors_seccion = 100 * sum(P[s] / A[s] for s in secciones_apl) / n
    ce = 100 * (cnt["presente"] + cnt["ausente"]) / aplicables
    techo = 100 * (cnt["presente"] + cnt["unknown"]) / aplicables

    filas.append(dict(nombre=nombre, cid=cid, cnt=cnt, P=P, A=A, NA=NA,
                      aplicables=aplicables, presentes=presentes, n=n,
                      uniforme=ors_uniforme, seccion=ors_seccion, ce=ce, techo=techo,
                      secciones_apl=secciones_apl))

# ---------------------------------------------------------------------------
# 6) Informe
# ---------------------------------------------------------------------------
print("\n" + "=" * 72)
print(FORMULA)
print(FORMULA_SEC)
print("=" * 72)
for f in filas:
    print(f"\n### {f['nombre']}  ({f['cid']})")
    c = f["cnt"]
    print(f"  controles: total={c['total']}  aplicables={f['aplicables']}  "
          f"presente={c['presente']}  ausente={c['ausente']}  unknown={c['unknown']}  "
          f"no_aplica={c['no_aplica']}")
    print(f"  peso uniforme (§5.3): ORS = 100 * {f['presentes']}/{f['aplicables']} "
          f"= {f['uniforme']:.6f} -> {r2(f['uniforme']):.2f}")
    print(f"  peso igual por seccion (§9): n={f['n']} secciones aplicables "
          f"{f['secciones_apl']} = {f['seccion']:.6f} -> {r2(f['seccion']):.2f}")
    print(f"  [ejes §7: CE={r2(f['ce']):.2f}  techo={r2(f['techo']):.2f}]")
    print("  desglose seccion: " + " | ".join(
        f"§{s}: P={f['P'][s]}/A={f['A'][s]}" for s in sorted(tam)))

print("\n" + "=" * 72)
print("ORDEN (mayor a menor)")
for etiqueta, clave in (("peso uniforme (§5.3)", "uniforme"),
                        ("peso igual por seccion (§9)", "seccion")):
    rank = sorted(filas, key=lambda f: -f[clave])
    print(f"  {etiqueta}: " + " > ".join(f"{f['nombre']} ({r2(f[clave]):.2f})" for f in rank))
print("=" * 72)
