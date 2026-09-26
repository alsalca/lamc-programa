# UNKNOWNS.md — Huecos declarados

**Regla A1:** `UNKNOWN ≠ 0` — lo que no se sabe no es cero.
**Regla A3:** la ausencia de evidencia no constituye evidencia.

Este ledger **no colapsa ni rellena** los huecos. Declara los que las fuentes (P2/P7)
ya tenían, tal cual, y añade los que son propios de la reconciliación.

---

## 1. Huecos heredados de las fuentes (declarados tal cual)

Cada ficha del ledger trae sus huecos heredados de su bundle de origen, **idénticos**:
no se han modificado los `unknown` / `unknown_reason` de ninguna ficha.

### Dominio blockchain (P2)

| Ficha | Campos unknown | Motivo |
|---|---|---|
| LAMC-P2-2026-0005 | `quantity` | Base devuelve deuda 0 y health factor `2^256-1`; no hay HF financiero aplicable. La cantidad se declara UNKNOWN con motivo. El artefacto raw es la misma respuesta `eth_call` de Base que la ficha 0004, no un archivo. El `evidence_hash` **sí está establecido** (hash del bloque, misión A4). Materialidad: la ficha no afirma cantidad, así que el hueco no altera ninguna cifra; debilita solo la prueba posterior de que la respuesta citada es la leída. |
| LAMC-P2-2026-0007 | `quantity`, `effective_at`, `evidence_hash` | La ficha documental fija la relación entidad/dirección, no un saldo; la fecha de publicación del libro de direcciones no se establece en esta captura. No hay artefacto local que hashear: la fuente es un archivo de código en un repositorio público, no un archivo del bundle; la referencia está fijada al commit `dd8bd67401e9c656061c0ac4dff777da25bca884` en vez de a la rama `blob/main`. Materialidad: el hueco no altera ninguna cifra, solo retira el ancla de integridad frente a una edición posterior del archivo. |

> **CORRECCIÓN 2026-09-26:** las filas de 0002–0006 y 0007 repetían «No se generó hash.», el motivo viejo que las fichas ya no usan, y la fila de 0007 omitía el motivo de `evidence_hash`. Se sustituyen por el motivo real de cada ficha. Además, la ficha `LAMC-P2-2026-0007` conservaba el literal «No cryptographic hash generated.»; se corrigió en `positions.json` y, en el mismo acto, en `ledger.json`, para que el ledger siga idéntico a su fuente (M-R3-5).

### Dominio contabilidad pública (P7)

| Ficha | Campos unknown | Motivo |
|---|---|---|
| P7-BCN-2026-0001 | 0 | Sin huecos. |
| P7-BCN-2026-0002 | 0 | Sin huecos. |
| P7-BCN-2026-0003 | `freshness` | El documento no declara política de vigencia para saldos de deuda. Detalle anidado: `freshness.valid_until` (memoria, página 51, vencimientos escalonados hasta 2043, sin un único vencimiento). |
| P7-BCN-2026-0004 | `freshness` | El documento no declara política de vigencia para provisiones (obligaciones contingentes). |
| P7-BCN-2026-0005 | `freshness` | Activos no corrientes a coste histórico; no hay política de vigencia declarada. |
| P7-BCN-2026-0006 | `freshness` | Obligaciones ambientales de 2023; no se declara política de vigencia. |

> **CORRECCIÓN 2026-09-26 (misión A4):** el `evidence_hash` de las seis fichas de cadena de
> P2 **ya no es un hueco**: se estableció con el **hash del bloque** que cada una cita
> (`keccak256:` del bloque, que el contrato admite como respaldo on-chain). Por eso sus
> filas desaparecen de esta tabla y el total baja. **Lo que sigue sin establecerse es el
> `evidence_hash` de la 0007**, que es documental y no cita ningún bloque: ese hueco es
> legítimo y se queda. La ficha 0005 conserva su hueco de `quantity`.

**Total de campos unknown heredados: 8** (sobre 13 fichas × 22 campos = 286). *(Era 11; el 2026-09-26 se estableció el `evidence_hash` de las seis fichas de cadena y quedó en 8.)*

---

## 2. Huecos propios de la reconciliación (no resueltos)

### R1 — Falta una segunda fuente por sujeto para contrastar (`reconciliation_status`)

`reconciliation_status` se mantiene `unreconciled` en las 13 fichas porque **este es el
primer registro** de cada sujeto en el ledger. No existe aún una segunda evidencia que
contraste y confirme (→ `reconciled`) o contradiga (→ `disputed`).

**¿Es un hueco material?** Sí, es el hueco central del propósito: la marcación
transversal de reconciliación queda **pendiente de ejecución**, no declarada como hecha.
No se simula: ninguna ficha se marca `reconciled` sin estar contrastada (A3).

### R2 — Los dos dominios no comparten ninguna magnitud comparable

No hay ninguna pareja de cifras entre blockchain y contabilidad pública que deba
coincidir ni cruzarse: son sujetos distintos (Aave DAO ≠ Ayuntamiento de Barcelona),
divisas distintas (USD/ETH vs EUR), naturalezas distintas (snapshot de protocolo vs
cuenta general anual).

**¿Es un hueco?** Es un **límite de alcance declarado**, no un dato que falte. Forzar un
cruce entre dominios sin procedencia sería inventar una relación (regla bloqueante del
charter, §4).

### R3 — Evidencia_futura: vigencia de las afirmaciones

Las fichas de P7 son datos históricos (cuenta de 2023). Las de P2 están ancladas a
bloques del 2026-09-23. **Nada en el ledger establece hasta cuándo describen el estado
actual** de sus respectivos sujetos; ésta era una limitación ya declarada en las
fuentes y que el ledger no puede resolver de nuevo.

---

## 3. Huecos que **NO** se declaran (fuera de alcance)

| No-declarado | Por qué |
|---|---|
| Portafolio personal del operador | Fuera de alcance del charter (§7). |
| Cifras estimadas o proyectadas | Solo se admiten datos observados de fuente (§7). |
| Datos sin procedencia verificable | Toda ficha exige `source_reference` / `raw_reference`. |
| Valores de mercado de los activos | Ninguna fuente del ledger los da; no se infieren (A3). |
| Composición de la deuda Aave por token | `getUserAccountData` reporta deuda agregada; no se desglosa aquí. |

---

## 4. Conclusión

- Los huecos **de contenido** vienen de las fuentes y se preservan **sin colapsar**.
- Los huecos **de reconciliación** (R1, R2) son propios de este pase: R1 queda
  **pendiente** y R2 es un **límite de alcance** honestamente declarado.
- **Ningún hueco se ha rellenado por inferencia.** Un dato que no está no se completa.