#!/usr/bin/env python3
"""
COMPROBADOR DE COINCIDENCIA — prosa contra esquema.

Para qué sirve: cinco rondas de trabajo fallaron por lo mismo — **una regla escrita
en dos sitios, y uno de los dos cambiado sin el otro**. Esta herramienta lo detecta.

NO lee prosa de forma inteligente: es una HEURÍSTICA. Busca valores que PARECEN
valores de lista cerrada y comprueba si están en el esquema. Da indicios, no verdades.

USO:
    python3 comprobar_coincidencia.py <carpeta_del_proyecto>

Lee `entregables/evidence-envelope.schema.json` y `entregables/SPEC.md`.
"""

import json
import re
import sys
from pathlib import Path

# Palabras en mayúsculas que NO son valores de lista cerrada. Si el comprobador
# las reporta, es ruido: van aquí para no dar falsas alarmas.
RUIDO = {
    "SPEC", "JSON", "SCHEMA", "API", "URL", "URI", "HTTP", "HTTPS", "RPC", "SQL",
    "ID", "IDS", "OK", "NO", "SI", "SÍ", "UNKNOWN", "NOT", "AND", "OR", "TODO",
    "PASS", "FAIL", "SHA256", "KECCAK256", "SHA", "MD5", "RFC", "UTC", "EUR",
    "USD", "ETH", "BTC", "WBTC", "WSTETH", "SOL", "XAUT", "EVM", "ABI", "NFT",
    "LP", "DEX", "CEX", "DAO", "DEFI", "CEFI", "RWA", "PII", "KYC", "AML",
    "EDGE", "CORE", "HQ", "MVP", "SLA", "TOC",
    # Nombres de archivo PÚBLICOS del paquete.
    # CORRECCIÓN 2026-09-23: aquí estaban también los nombres de los documentos
    # INTERNOS del programa (planes, contratos, encargos, estados). Se quitaron
    # al anonimizar el paquete: si alguno reapareciera en la prosa, es que se
    # coló, y entonces conviene que el comprobador lo señale en vez de taparlo.
    "VERSION", "LICENSE", "SPEC", "README",
    # énfasis en prosa española (no son valores de lista)
    "APARATO", "APROBADO", "OPCIONAL", "OBLIGATORIO", "CAMPOS", "CENTINELA",
    "BLOQUEANTE", "ANIDADOS", "ESTABILIDAD_DEL_SOBRE", "FRESHNESS_ENFORCEMENT",
    "RECONCILIATION_RULES", "ESTABILIDAD_DEL_SOBRE_DE_22_CAMPOS",
}


def enums_del_esquema(esquema):
    """Todos los valores de todas las listas cerradas, y a qué campo pertenecen."""
    por_campo = {}
    todos = set()

    def recorrer(nodo, ruta=""):
        if isinstance(nodo, dict):
            if "enum" in nodo and isinstance(nodo["enum"], list):
                vals = [v for v in nodo["enum"] if isinstance(v, str)]
                # ¿de qué campo es? se deduce de la ruta o del enum mismo
                campo = None
                for c in ("authority", "verification_status", "confidence",
                          "reconciliation_status", "type", "kind", "status",
                          "source_type"):
                    if c in ruta:
                        campo = c
                        break
                if campo:
                    por_campo.setdefault(campo, set()).update(vals)
                todos.update(vals)
            for k, v in nodo.items():
                recorrer(v, f"{ruta}.{k}")
        elif isinstance(nodo, list):
            for v in nodo:
                recorrer(v, ruta)

    recorrer(esquema)
    return por_campo, todos


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    carpeta = Path(sys.argv[1]).resolve()
    ent = carpeta / "entregables" if (carpeta / "entregables").exists() else carpeta

    esquema_p = next(ent.glob("*.schema.json"), None)
    spec_p = ent / "SPEC.md"
    if not esquema_p or not spec_p.exists():
        print("  Faltan el esquema o SPEC.md")
        return 2

    esquema = json.loads(esquema_p.read_text(encoding="utf-8"))
    spec = spec_p.read_text(encoding="utf-8")

    print(f"\nCOMPROBADOR DE COINCIDENCIA — {carpeta.name}")
    print("=" * 62)
    problemas = 0

    # ── 1. Los campos obligatorios del esquema, ¿aparecen en la prosa? ──
    print("\n[1] CAMPOS OBLIGATORIOS DEL ESQUEMA")
    req = esquema.get("required", [])
    ausentes = [c for c in req if not re.search(rf"\b{re.escape(c)}\b", spec)]
    if ausentes:
        print(f"  ✗ el esquema exige {len(req)} campos; estos NO aparecen en la prosa:")
        for c in ausentes:
            print(f"      - {c}")
        problemas += 1
    else:
        print(f"  ✓ los {len(req)} campos del esquema aparecen en la prosa")

    # ── 2. Campos que la prosa menciona y el esquema no declara ──
    print("\n[2] CAMPOS QUE LA PROSA MENCIONA Y EL ESQUEMA NO DECLARA")
    props = set(esquema.get("properties", {}).keys())
    # candidatos: nombres en snake_case entre acentos graves
    candidatos = set(re.findall(r"`([a-z][a-z0-9_]{3,})`", spec))
    # nombres que son subcampos legítimos
    subcampos = set()
    def recoger_sub(nodo):
        if isinstance(nodo, dict):
            if "properties" in nodo:
                subcampos.update(nodo["properties"].keys())
            for v in nodo.values():
                recoger_sub(v)
        elif isinstance(nodo, list):
            for v in nodo:
                recoger_sub(v)
    recoger_sub(esquema)
    desconocidos = sorted(candidatos - props - subcampos - RUIDO)
    # filtrar palabras que claramente no son campos
    desconocidos = [c for c in desconocidos if "_" in c]
    if desconocidos:
        print(f"  ? revisar ({len(desconocidos)}) — podrían ser nombres de campo ajenos al esquema:")
        for c in desconocidos[:15]:
            print(f"      - {c}")
        problemas += 1
    else:
        print("  ✓ ningún nombre de campo ajeno al esquema")

    # ── 3. Valores de lista cerrada: ¿los del esquema están en la prosa? ──
    print("\n[3] VALORES DE LISTA CERRADA DEL ESQUEMA, ¿EN LA PROSA?")
    por_campo, todos = enums_del_esquema(esquema)
    faltan_todos = sorted(v for v in todos if not re.search(rf"\b{re.escape(v)}\b", spec))
    if faltan_todos:
        print(f"  ✗ el esquema admite {len(todos)} valores; estos NO aparecen en la prosa:")
        for v in faltan_todos:
            print(f"      - {v}")
        problemas += 1
    else:
        print(f"  ✓ los {len(todos)} valores del esquema aparecen en la prosa")

    # ── 4. Valores EN MAYÚSCULAS en la prosa que el esquema no admite ──
    # SOLO se marcan los que PARECEN un identificador de lista cerrada:
    #   · llevan guion bajo (PUBLIC_CHAIN, INSTITUTION_DOCUMENT) → casi seguro enum
    #   · o van entre acentos graves (`MANUAL_ASSERTION`)
    # NO se marcan las palabras en mayúsculas de énfasis en prosa (CAMPOS, CENTINELA…):
    # eso producía 100 falsas alarmas. Un comprobador que grita de más no sirve.
    print("\n[4] VALORES EN MAYÚSCULAS DE LA PROSA QUE EL ESQUEMA NO ADMITE")
    con_guion = set(re.findall(r"\b([A-Z][A-Z0-9]*_[A-Z0-9_]+)\b", spec))
    entre_acentos = set(re.findall(r"`([A-Z][A-Z0-9_]{2,})`", spec))
    candidatos = con_guion | entre_acentos
    ajenos = sorted(candidatos - todos - RUIDO)
    if ajenos:
        print(f"  · lista para revisar a mano ({len(ajenos)}) — puede haber valores ajenos al esquema:")
        for v in ajenos[:12]:
            print(f"      - {v}")
        print("      (INFORMATIVO: este bloque es heurístico y no cuenta como fallo)")
    else:
        print("  ✓ ningún valor en mayúsculas ajeno al esquema")

    print("\n" + "=" * 62)
    if problemas == 0:
        print("RESULTADO: SIN INDICIOS DE DESACUERDO")
    else:
        print(f"RESULTADO: {problemas} bloque(s) con indicios — REVISAR A MANO")
    print("Recuerda: es una HEURÍSTICA. Da indicios, no verdades.")
    print("=" * 62 + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
