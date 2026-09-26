# EVIDENCIA — Puntuaciones ORS (N8)

**Fecha:** 2026-09-25 · **Modelo:** ORS v1.0.0 (`entregables/MODELO.md`)  
**Bundle:** `entregables/bundle/puntuaciones.json` (6 fichas)  
**Estado:** CANDIDATO — no publicado. Pendiente de checker y **HG-001**.

---

## 1. FUENTE ÚNICA

Todas las puntuaciones derivan **exclusivamente** de la medición de P4:

| Artefacto | Ruta | sha256 |
|---|---|---|
| Mediciones (datos de entrada) | `proyectos/P4_CAPA_CONTROLES/entregables/bundle/mediciones.json` | `41354fbe0ca5742194b7ca28b5f3112b7bcd98ddda43392cd58a0fea5a0c0d85` |
| Mapa de evidencia por control | `proyectos/P4_CAPA_CONTROLES/entregables/bundle/evidence.md` | *(citado por URL en cada fila)* |
| Estándar aplicado | `proyectos/P3_OPS_SEC/entregables/STANDARD.md` | — |

No se ha añadido ningún control, fuente ni criterio distinto de los de P4/P3. El ORS
**no vuelve a medir**; traduce conteos ya publicados.

---

## 2. CADENA DE PROCEDENCIA (ficha N8 → ficha P4)

| Ficha de puntuación (N8) | Protocolo | Ficha de insumo (N8) | Ficha P4 de origen | Autoridad P4 |
|---|---|---|---|---|
| `LAMC-N8-2026-0001` | Aave | `LAMC-N8-2026-0004` | `P4-CTRL-2026-0001` | `PUBLIC_CHAIN` |
| `LAMC-N8-2026-0002` | Uniswap | `LAMC-N8-2026-0005` | `P4-CTRL-2026-0002` | `PUBLIC_CHAIN` |
| `LAMC-N8-2026-0003` | Liquity (V1) | `LAMC-N8-2026-0006` | `P4-CTRL-2026-0003` | `DERIVED` |

Las **fichas de insumo** transcriben los conteos de P4 y conservan su autoridad
(transcribir no cambia quién responde). Las **fichas de puntuación** llevan
`authority = DERIVED`, porque la puntuación es un cálculo nuestro sobre esas
mediciones. Por eso el bundle contiene ambas: la cadena de procedencia es explícita.

---

## 3. BASE POR CONTROL (lo que P4 marcó, y su fuente pública)

De los 52 controles, P4 solo pudo marcar 6 en Aave/Uniswap y 5+8 en Liquity. El resto
es `unknown` con motivo (ver `P4/.../bundle/unknowns.md`). Fuente pública de cada marca:

| Control | Aave | Uniswap | Liquity | Fuente pública (citada por P4) |
|---|---|---|---|---|
| §2.1 multisig | ✅ | ? | ➖ | Aave: SAFEs 2-of-3 y Community Guardian 5-of-9 — `governance.aave.com/t/arfc-june-update-signers-and-safe-configuration/25023`, `aave.com/security`. Uniswap: tesorería bajo timelock de la DAO, no multisig 2-de-3 ⇒ `?` — `developers.uniswap.org/docs/ecosystem/governance/technical-reference`. Liquity: inmutable/governance-free ⇒ `➖` — `liquity.org/features/governance-free`. |
| §3.1 secretos | ✅ | ✅ | ✅ | Grep de `.env`/`.env.example` a HEAD en repos públicos de cada org; sin secreto de producción (hallazgos de transparencia documentados por P4, no reproducidos aquí). |
| §6.1 observabilidad | ✅ | ✅ | ✅ | Aave: subgraphs + `aave-api-v2.aave.com`. Uniswap: `status.uniswap.org` + subgraphs. Liquity: subgraph `liquity/liquity` + `github.com/liquity/cr-monitor`. |
| §9.4 terceros/oráculo | ❌ | ✅ | ✅ | Aave: proveedor único Chainlink con fallback desactivado (`AaveOracle.sol`, propuesta #351). Uniswap: Api3/Pyth/RedStone/Chainlink documentados. Liquity: Chainlink primario + Tellor fallback (`PriceFeed.sol`). |
| §10.3 dependencias | ✅ | ? | ✅ | Aave: Dependabot + dependency-review en CI. Uniswap: **sin configuración observable desde el repositorio público**, pero con evidencia indirecta de que el proceso existe (Dependabot activo por ajustes de organización) ⇒ `?` **no observable**, no `ausente` (axioma A3). Liquity: Dependabot npm daily. |
| §10.7 credenciales | ✅ | ✅ | ✅ | Mismo grep que §3.1. |

**Leyenda:** ✅ presente · ❌ ausente · ? unknown · ➖ no aplica.  
Detalle completo y URLs: `proyectos/P4_CAPA_CONTROLES/entregables/bundle/evidence.md`.

> **No se reproduce ningún valor de credencial.** Los hallazgos de transparencia que
> P4 registró (claves cliente-públicas, IDs públicos) se citan por referencia, sin
> copiar su contenido. Sin datos personales.

---

## 4. ARITMÉTICA REPRODUCIBLE

Regla (MODELO.md §5): `ORS = 100 × presente / aplicables`, con `aplicables = 52 − no_aplica`.
`unknown` **no recibe valor**. Ejes: `techo = 100 × (presente + unknown) / aplicables`,
`CE = 100 × (presente + ausente) / aplicables`.

### 4.1 Aave — `LAMC-N8-2026-0001`

- Conteos P4: `presente 5 · ausente 1 · unknown 46 · no_aplica 0` → `aplicables 52`
- **ORS = 100 × 5 / 52 = 9.6154 → 9.62** · techo = 100 × 51/52 = 98.08 · CE = 100 × 6/52 = 11.54
- Desglose por sección (`presente/aplicables`): §2 `1/4`, §3 `1/5`, §6 `1/6`, §10 `2/7`; resto `0`.

### 4.2 Uniswap — `LAMC-N8-2026-0002`

- Conteos P4: `presente 4 · ausente 0 · unknown 48 · no_aplica 0` → `aplicables 52`
- **ORS = 100 × 4 / 52 = 7.6923 → 7.69** · techo = 100 × 52/52 = 100.00 · CE = 100 × 4/52 = 7.69
- Desglose: §3 `1/5`, §6 `1/6`, §9 `1/5`, §10 `1/7`; resto `0`.

### 4.3 Liquity (V1) — `LAMC-N8-2026-0003`

- Conteos P4: `presente 5 · ausente 0 · unknown 39 · no_aplica 8` → `aplicables 44`
- **ORS = 100 × 5 / 44 = 11.3636 → 11.36** · techo = 100 × 44/44 = 100.00 · CE = 100 × 5/44 = 11.36
- §1 y §2 quedan enteras en `no_aplica` (inmutable/governance-free) y se excluyen.
- Desglose: §3 `1/5`, §6 `1/6`, §9 `1/5`, §10 `2/7`; resto `0`.

### 4.4 Sensibilidad (peso uniforme vs. peso igual por sección)

| Protocolo | ORS (uniforme, primario) | ORS (igual por sección) |
|---|---:|---:|
| Aave | 9.62 | 9.02 |
| Uniswap | 7.69 | 7.10 |
| Liquity (V1) | 11.36 | 10.65 |

Mismo orden bajo las dos reglas: **Liquity > Aave > Uniswap**.

---

## 5. DE QUÉ DEPENDE CADA DIFERENCIA (no es ruido del modelo)

El modelo es **determinístico**: no hay componente aleatorio. Cada diferencia se
atribuye a controles concretos:

| Diferencia | Magnitud (pp) | Control(es) que la producen |
|---|---:|---|
| Aave − Uniswap | +1.92 (=1/52) | §2.1 Aave ✅ vs. Uniswap ? (multisig 2-de-3); §10.3 Aave ✅ vs. Uniswap ?; §9.4 Aave ❌ vs. Uniswap ✅. Neto: +1 presente en Aave. |
| Liquity − Aave | +1.75 | Mismo numerador (5) con denominador menor: 44 vs. 52 (`no_aplica` de §1/§2). **No** es cobertura adicional verificada. |
| Liquity − Uniswap | +3.67 | Uniswap tiene 4 presentes y ninguno ausente recuperable; Liquity 5 con denominador 44. |

**Consecuencia honesta:** las diferencias son **atribuibles**, pero **pequeñas** frente
a la incertidumbre de la medición (§4.1: techo ≈ 98 con suelo ≈ 10). El ORS **ordena
cobertura verificada**, no riesgo.

---

## 6. VALIDACIÓN DETERMINÍSTICA

```bash
python3 herramientas/validar_evidencia.py proyectos/N8_ORS
```

Resultado: **APROBADO — los 3 bloques pasan** (`[1]` esquema P1 · `[2]` 6 fichas
correctas · `[3]` 6 fichas · `[4]` 2 autoridades: `DERIVED`, `PUBLIC_CHAIN`).

---

*Evidencia generada por quien construye el entregable — 2026-09-25. Reproducible desde P4 sin volver a medir.*

---

## Procedencia por ficha

> Estas notas estaban dentro del JSON, en una clave `_meta` que viajaba
> **dentro de cada ficha**. El contrato no la admite (`additionalProperties: false`),
> así que las fichas no validaban contra su propio esquema. El contenido es el mismo,
> y aquí —al lado de la evidencia— se lee mejor.

### `LAMC-N8-2026-0001`

- **protocolo** — Aave
- **rol** — puntuacion_ors
- **modelo** — ORS v1.0.0
- **controles** — {"presente": 5, "ausente": 1, "unknown": 46, "no_aplica": 0, "aplicables": 52, "total": 52}
- **ors_suelo** — 9.62
- **ors_techo** — 98.08
- **completitud_ce** — 11.54
- **desglose_por_seccion** — {"1": {"presente": 0, "aplicables": 4, "score": 0.0}, "2": {"presente": 1, "aplicables": 4, "score": 0.25}, "3": {"presente": 1, "aplicables": 5, "score": 0.2}, "4": {"presente": 0, "aplicables": 6, "score": 0.0}, "5": {"presente": 0, "aplicables": 5, "score": 0.0}, "6": {"presente": 1, "aplicables": 6, "score": 0.1667}, "7": {"presente": 0, "aplicables": 5, "score": 0.0}, "8": {"presente": 0, "aplicables": 5, "score": 0.0}, "9": {"presente": 0, "aplicables": 5, "score": 0.0}, "10": {"presente": 2, "aplicables": 7, "score": 0.2857}}
- **nota** — El ORS es un suelo verificado, no una nota de seguridad. unknown sin valor (A1/A3).

### `LAMC-N8-2026-0002`

- **protocolo** — Uniswap
- **rol** — puntuacion_ors
- **modelo** — ORS v1.0.0
- **controles** — {"presente": 4, "ausente": 0, "unknown": 48, "no_aplica": 0, "aplicables": 52, "total": 52}
- **ors_suelo** — 7.69
- **ors_techo** — 100.00
- **completitud_ce** — 7.69
- **desglose_por_seccion** — {"1": {"presente": 0, "aplicables": 4, "score": 0.0}, "2": {"presente": 0, "aplicables": 4, "score": 0.0}, "3": {"presente": 1, "aplicables": 5, "score": 0.2}, "4": {"presente": 0, "aplicables": 6, "score": 0.0}, "5": {"presente": 0, "aplicables": 5, "score": 0.0}, "6": {"presente": 1, "aplicables": 6, "score": 0.1667}, "7": {"presente": 0, "aplicables": 5, "score": 0.0}, "8": {"presente": 0, "aplicables": 5, "score": 0.0}, "9": {"presente": 1, "aplicables": 5, "score": 0.2}, "10": {"presente": 1, "aplicables": 7, "score": 0.1429}}
- **nota** — El ORS es un suelo verificado, no una nota de seguridad. unknown sin valor (A1/A3).

### `LAMC-N8-2026-0003`

- **protocolo** — Liquity
- **rol** — puntuacion_ors
- **modelo** — ORS v1.0.0
- **controles** — {"presente": 5, "ausente": 0, "unknown": 39, "no_aplica": 8, "aplicables": 44, "total": 52}
- **ors_suelo** — 11.36
- **ors_techo** — 100.00
- **completitud_ce** — 11.36
- **desglose_por_seccion** — {"3": {"presente": 1, "aplicables": 5, "score": 0.2}, "4": {"presente": 0, "aplicables": 6, "score": 0.0}, "5": {"presente": 0, "aplicables": 5, "score": 0.0}, "6": {"presente": 1, "aplicables": 6, "score": 0.1667}, "7": {"presente": 0, "aplicables": 5, "score": 0.0}, "8": {"presente": 0, "aplicables": 5, "score": 0.0}, "9": {"presente": 1, "aplicables": 5, "score": 0.2}, "10": {"presente": 2, "aplicables": 7, "score": 0.2857}}
- **nota** — El ORS es un suelo verificado, no una nota de seguridad. unknown sin valor (A1/A3).

### `LAMC-N8-2026-0004`

- **protocolo** — Aave
- **rol** — insumo_p4
- **p4_claim** — P4-CTRL-2026-0001
- **conteos_p4** — {"presente": 5, "ausente": 1, "unknown": 46, "no_aplica": 0, "total": 52}
- **autoridad_p4** — PUBLIC_CHAIN
- **nota** — Transcribe la medición de P4; la autoridad se conserva porque transcribir no cambia quién responde.

### `LAMC-N8-2026-0005`

- **protocolo** — Uniswap
- **rol** — insumo_p4
- **p4_claim** — P4-CTRL-2026-0002
- **conteos_p4** — {"presente": 4, "ausente": 0, "unknown": 48, "no_aplica": 0, "total": 52}
- **autoridad_p4** — PUBLIC_CHAIN
- **nota** — Transcribe la medición de P4; la autoridad se conserva porque transcribir no cambia quién responde.

### `LAMC-N8-2026-0006`

- **protocolo** — Liquity
- **rol** — insumo_p4
- **p4_claim** — P4-CTRL-2026-0003
- **conteos_p4** — {"presente": 5, "ausente": 0, "unknown": 39, "no_aplica": 8, "total": 52}
- **autoridad_p4** — DERIVED
- **nota** — Transcribe la medición de P4; la autoridad se conserva porque transcribir no cambia quién responde.
