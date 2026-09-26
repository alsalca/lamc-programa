# REASONING.md — Razonamiento paso a paso

Un tercero puede seguir esta secuencia y llegar a la misma conclusión: el ledger
`bundle/ledger.json` concatena 7 fichas de blockchain y 6 de contabilidad pública,
sin fusionar dominios ni inventar datos.

---

## Paso 1 — Tomar las 7 fichas de blockchain

**Fuente:** `P2_DEMO_RECONSTRUCCION/entregables/bundle/positions.json` (7 fichas,
`LAMC-P2-2026-0001` … `0007`, sujeto **Aave DAO AHAB Safe**).

- Las fichas 0001–0006 son lecturas **on-chain** ancladas a bloque:
  - 0001 colateral total Aave (Ethereum, bloque 26040185)
  - 0002 deuda total Aave (Ethereum)
  - 0003 rETH en wallet (Ethereum)
  - 0004 colateral total Aave (Base, bloque 51691143)
  - 0005 health factor (Base) — `quantity` UNKNOWN porque Aave devuelve deuda 0 y HF `2^256-1`
  - 0006 wstETH — saldo medido 0
- La 0007 es **documental** (publicación de la dirección del Safe): `STRUCTURED_EXPORT`.

Cada ficha se copia **sin modificar sus 22 campos**. **No se le añade nada**: el
`_meta` que se pensó añadir violaba el contrato y se retiró (ver §4.3 de `DOMINIOS.md`).
`reconciliation_status` permanece `unreconciled`.

## Paso 2 — Tomar las 6 fichas de contabilidad pública

**Fuente:** `P7_SEGUNDO_DOMINIO/entregables/bundle/fichas.json` (6 fichas,
`P7-BCN-2026-0001` … `0006`, sujeto **Ayuntamiento de Barcelona**, Cuenta General 2023).

- 0001 ingresos de gestión ordinaria (flujo, `NONE`)
- 0002 patrimonio neto (stock, `NONE`)
- 0003 deuda financiera LP (pasivo, `DEBT`)
- 0004 provisiones LP (pasivo contingente, `DEBT`)
- 0005 infraestructuras a coste histórico (activo, `NONE`)
- 0006 obligaciones ambientales (pasivo, `DEBT`)

> **CORRECCIÓN 2026-09-26:** esta lista describía 0002 y 0005 con `FIAT_BALANCE`. Las fichas ya usan `NONE` (con `symbol: EUR`); se alinea el texto. En el ledger, `instrument.kind` del dominio contabilidad pública solo toma `NONE` y `DEBT`.

Cada ficha se copia **sin modificar sus 22 campos**. **No se le añade nada**: el
`_meta` que se pensó añadir violaba el contrato y se retiró (ver §4.3 de `DOMINIOS.md`).
`reconciliation_status` permanece `unreconciled`.

## Paso 3 — Concatenar en un solo array, sin fusionar

El ledger es la **unión ordenada** de las dos listas (primero blockchain, luego
contabilidad pública). No hay suma ni resta entre fichas de dominios distintos.

**Verificación de no-fusión** — en cada ficha del ledger se pueden leer **cinco señales**
independientes que la anclan a su dominio:

| Señal | blockchain | contabilidad_publica |
|---|---|---|
| `source_type` | `ONCHAIN` (0001–0006) / `STRUCTURED_EXPORT` (0007) | `SIGNED_DOCUMENT` |
| `container.type` | `BLOCKCHAIN_WALLET` | `DOCUMENTARY_ASSET` / `CREDIT_ACCOUNT` |
| `authority` | `PUBLIC_CHAIN` (0001–0006) / `INSTITUTION_DOCUMENT` (0007) | `INSTITUTION_DOCUMENT` |
| prefijo `claim_id` | `LAMC-P2-*` | `P7-BCN-*` |
| `producer` | `LAMC-P2/*` | `P7-BCN/*` |

> **CORRECCIÓN 2026-09-26:** la señal de `source_type` atribuía `SIGNED_DOCUMENT` a la ficha `LAMC-P2-2026-0007`. El ledger ya la tiene en `STRUCTURED_EXPORT`; se alinea la tabla.

## Paso 4 — Verificar integridad (22 casillas intactas)

Para cada ficha del ledger se compara contra la original: los 22 campos son
**idénticos** y **no se añade ningún campo**. Comprobación realizada programáticamente
al emitir el bundle.

## Paso 5 — Clasificar la naturaleza económica (activo/pasivo/flujo/control/contexto)

Se etiqueta cada ficha respecto **al sujeto que la afirma** (ver `reconciliacion.md`, §3).
No se cruzan clasificaciones entre dominios.

## Paso 6 — Declarar los huecos, sin colapsarlos

Se preservan los `unknown` / `unknown_reason` de cada ficha tal cual venían de la
fuente. Se añaden los huecos propios de la reconciliación (ver `unknowns.md`): R1
(no hay segunda fuente por sujeto → todo sigue `unreconciled`), R2 (los dominios no
comparten magnitud comparable), R3 (sin vigencia futura del registro).

## Paso 7 — Validación determinística

```bash
python3 herramientas/validar_evidencia.py \
    proyectos/P8_RECONCILIACION
```
→ `RESULTADO: APROBADO` (13 fichas, 2 autoridades: `PUBLIC_CHAIN`, `INSTITUTION_DOCUMENT`).

```bash
grep -c '"source_type"' proyectos/P8_RECONCILIACION/entregables/bundle/ledger.json
# 26  (cada ficha menciona "source_type" dos veces: como campo y dentro de la lista "known")
grep -o '"source_type":"[^"]*"' proyectos/P8_RECONCILIACION/entregables/bundle/ledger.json | sort -u
# "source_type":"ONCHAIN"
# "source_type":"SIGNED_DOCUMENT"
```

Ambos valores aparecen → los dos dominios están representados y distinguibles.

---

## Conclusiones alcanzables

1. El ledger **no fusiona** dominios: cada ficha se rastrea a su dominio exacto.
2. Toda cifra proviene de un bundle existente (P2 o P7); **no se inventa nada**.
3. Las 22 casillas de **cada** ficha quedan intactas; **no se añade ni se quita ningún campo**.
4. Los huecos se declaran y se preservan, **sin colapsarlos ni rellenarlos por inferencia**.
5. `reconciliation_status` queda en `unreconciled` por ser la **primera emisión** del ledger.