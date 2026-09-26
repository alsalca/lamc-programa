# RECONCILIACION.md — Qué está conciliado, qué no, y por qué

**Proyecto:** P8_RECONCILIACION
**Ledger:** `bundle/ledger.json` (13 fichas)
**Fecha de reconciliación:** 2026-09-25
**Estado:** 🟦 Primer pase — primera vez que se reconcilia este ledger (todas las fichas en `unreconciled`).

---

## 1. Qué significa «conciliar» aquí

Las fichas de **distintos dominios** no se restan ni se suman: pertenecen a sujetos
distintos (Aave DAO AHAB Safe ≠ Ayuntamiento de Barcelona). Conciliar no es fusionar
cuentas. En este ledger, reconcilia:

- **Clasificar:** cada ficha se etiqueta como activo, pasivo, flujo, control o contexto
  **del sujeto que la afirma**.
- **Trazar procedencia:** cada ficha identifica su dominio de origen (`source_type` +
  `container.type` + `authority` + prefijo de `claim_id` + `producer`).
- **Declarar huecos:** lo que no se pudo establecer se declara con su motivo.

Lo que **NO** se hace: no se suma colateral Aave + patrimonio Barcelona; no se resta
deuda Aave de deuda Barcelona; no se colapsan los dos dominios en uno.

---

## 2. Qué SÍ está conciliado

Cada una de las 13 fichas llega al ledger idéntica a su fuente, con sus 22 casillas
intactas. La reconciliación de **procedencia** está completa:

| Dominio | Fichas | Cuántas | source_type | Sujeto |
|---|---|---|---|---|
| **blockchain** | `LAMC-P2-2026-0001` … `0007` | 7 | `ONCHAIN` (0001–0006) / `STRUCTURED_EXPORT` (0007) | Aave DAO AHAB Safe |
| **contabilidad_publica** | `P7-BCN-2026-0001` … `0006` | 6 | `SIGNED_DOCUMENT` | Ayuntamiento de Barcelona |

> **CORRECCIÓN 2026-09-26:** esta tabla atribuía `SIGNED_DOCUMENT` a la ficha `LAMC-P2-2026-0007`. La fuente ya lo corrigió: el `.sol` de GitHub no está firmado y su `source_type` es `STRUCTURED_EXPORT`. El ledger ya tenía el valor nuevo; se alinea el texto.

Cada ficha conserva su **sujeto original** — los dominios no se han fusionado. Un
tercero puede leer el ledger y separar, línea a línea, qué es blockchain y qué es
contabilidad pública por **cinco señales independientes**:

1. `source_type`
2. `container.type` (`BLOCKCHAIN_WALLET` vs `DOCUMENTARY_ASSET` / `CREDIT_ACCOUNT`)
3. `authority` (`PUBLIC_CHAIN` / `INSTITUTION_DOCUMENT` vs `INSTITUTION_DOCUMENT`)
4. prefijo de `claim_id` (`LAMC-P2-*` vs `P7-BCN-*`)
5. `producer` (`LAMC-P2/*` vs `P7-BCN/*`)

---

## 3. Clasificación activo / pasivo / flujo / control / contexto

### Dominio blockchain — Aave DAO AHAB Safe

| Ficha | Naturaleza | Clasificación | Explicación |
|---|---|---|---|
| LAMC-P2-2026-0001 | Colateral total Aave (Ethereum) | **Activo** | Derecho económico del sujeto sobre el protocolo |
| LAMC-P2-2026-0002 | Deuda total Aave (Ethereum) | **Pasivo** | Obligación del sujeto frente al protocolo |
| LAMC-P2-2026-0003 | rETH en wallet (Ethereum) | **Activo** | Token holding, propiedad del sujeto |
| LAMC-P2-2026-0004 | Colateral total Aave (Base) | **Activo** | Derecho económico en Base |
| LAMC-P2-2026-0005 | Health Factor (Base) | **Control** | Métrica de riesgo; no es activo ni pasivo |
| LAMC-P2-2026-0006 | wstETH — saldo cero | **Activo (cero)** | Saldo medido = 0; no hay posición |
| LAMC-P2-2026-0007 | Publicación de dirección | **Contexto** | Documentación, no financiero |

### Dominio contabilidad pública — Ayuntamiento de Barcelona

| Ficha | Naturaleza | Clasificación | Explicación |
|---|---|---|---|
| P7-BCN-2026-0001 | Ingresos de gestión ordinaria | **Flujo (ingreso)** | Resultado del ejercicio, no balance |
| P7-BCN-2026-0002 | Patrimonio neto | **Patrimonio** | Diferencia activo − pasivo |
| P7-BCN-2026-0003 | Deuda financiera LP | **Pasivo** | Obligación frente a acreedores |
| P7-BCN-2026-0004 | Provisiones LP | **Pasivo** | Obligación contingente |
| P7-BCN-2026-0005 | Infraestructuras (coste) | **Activo** | Activo no corriente |
| P7-BCN-2026-0006 | Obligaciones ambientales | **Pasivo** | Compromiso de gasto |

---

## 4. Qué NO está conciliado (y por qué)

### 4.1 Reconciliación transversal entre dominios — NO aplica

No hay una cifra de blockchain que contrastar contra una cifra del Ayuntamiento:
pertenecen a **sujetos económicos distintos**, no existe ninguna cuenta en común y no
hay ningún par de evidencias que deba coincidir. Cruzarlas sería inventar una
relación que la fuente no declara. Por eso la **unión de dominios en un solo ledger
es una concatenación, no una resta ni una suma**.

### 4.2 `reconciliation_status` se mantiene en `unreconciled`

Es la **primera vez** que se emite este ledger. No hay aún un segundo registro del mismo
sujeto que contraste cada ficha, por lo que **ninguna ficha se marca `reconciled` ni
`disputed`**. Este pase sienta la *columna vertebral*: qué entra, de qué dominio, con
qué clasificación y qué huecos tiene. La marcación transversal (`reconciled` / `disputed`)
quedaría para pases subsiguientes cuando exista una segunda fuente que contrastar.

### 4.3 Huecos heredados — NO resueltos por este pase

Este ledger **no rellena** los huecos que las fuentes ya declararon (ver
`unknowns.md`). Copiarlos tal cual y declararlos de nuevo es la conducta correcta:
un hueco de P2/P7 no desaparece por entrar en el ledger.

---

## 5. El contrato de P1

- Se copian los 22 campos de cada ficha **sin modificarlos**.
- **No se toca** `evidence-envelope.schema.json` v0.2.0.
- Cada ficha pasa la validación contra el esquema v0.2.0 → `RESULTADO: APROBADO`.

> **CORRECCIÓN 2026-09-25 (auditoría independiente, hallazgo 15).** Aquí decía que «solo se
> añade `_meta` (campo no controlado por el esquema; **las fichas de P2 y P7 ya lo
> usaban**)». **Dos cosas falsas en una frase:**
> 1. `_meta` **sí está controlado** por el esquema: viajaba dentro de cada ficha, cada ficha
>    es el sobre, y el sobre declara `additionalProperties: false`. Las 13 fichas **no
>    validaban** contra su propio contrato.
> 2. **P2 nunca usó `_meta`**: `positions.json` no lo tiene. Se justificó la violación con
>    un hecho que no ocurría — y ese es el fallo del que este programa dice ocuparse.
>
> `_meta` se eliminó y su contenido está ahora en la sección «Procedencia por ficha» de este
> documento. Con la clave fuera, **la afirmación de conformidad de esta sección es cierta**.

---

## 6. Resumen

| Aspecto | Estado |
|---|---|
| Procedencia de cada ficha | ✅ Conciliada (rastreada a su dominio exacto) |
| Dominios separados, no fusionados | ✅ |
| Las 13 fichas idénticas a su fuente | ✅ (22 casillas intactas) |
| `reconciliation_status` | `unreconciled` (primera emisión del ledger) |
| Huecos declarados sin colapsar | ✅ (ver `unknowns.md`) |
| Datos nuevos inventados | ❌ Ninguno |

---

## Procedencia por ficha

> Estas notas estaban dentro del JSON, en una clave `_meta` que viajaba
> **dentro de cada ficha**. El contrato no la admite (`additionalProperties: false`),
> así que las fichas no validaban contra su propio esquema. El contenido es el mismo,
> y aquí —al lado de la evidencia— se lee mejor.

### `LAMC-P2-2026-0001`

- **domain** — blockchain
- **original_producer** — LAMC-P2/ethereum-aave-rpc
- **p8_reconciliation** — 2026-09-25
- **note** — Blockchain: colateral total en Aave V3 sobre Ethereum (activo del Aave DAO AHAB Safe).

### `LAMC-P2-2026-0002`

- **domain** — blockchain
- **original_producer** — LAMC-P2/ethereum-aave-rpc
- **p8_reconciliation** — 2026-09-25
- **note** — Blockchain: deuda total en Aave V3 sobre Ethereum (pasivo del Aave DAO AHAB Safe).

### `LAMC-P2-2026-0003`

- **domain** — blockchain
- **original_producer** — LAMC-P2/ethereum-token-rpc
- **p8_reconciliation** — 2026-09-25
- **note** — Blockchain: holding de rETH en wallet Ethereum del AHAB Safe (activo).

### `LAMC-P2-2026-0004`

- **domain** — blockchain
- **original_producer** — LAMC-P2/base-aave-rpc
- **p8_reconciliation** — 2026-09-25
- **note** — Blockchain: colateral total en Aave V3 sobre Base (activo del AHAB Safe).

### `LAMC-P2-2026-0005`

- **domain** — blockchain
- **original_producer** — LAMC-P2/base-aave-rpc
- **p8_reconciliation** — 2026-09-25
- **note** — Blockchain: health factor en Base; sin deuda, HF max (control de riesgo, no activo ni pasivo).

### `LAMC-P2-2026-0006`

- **domain** — blockchain
- **original_producer** — LAMC-P2/ethereum-token-rpc
- **p8_reconciliation** — 2026-09-25
- **note** — Blockchain: wstETH con saldo cero medido en Ethereum (activo cero, sin posicion).

### `LAMC-P2-2026-0007`

- **domain** — blockchain
- **original_producer** — LAMC-P2/institution-document
- **p8_reconciliation** — 2026-09-25
- **note** — Blockchain: publicacion documental de la direccion del AHAB Safe (contexto, no financiero).

### `P7-BCN-2026-0001`

- **domain** — contabilidad_publica
- **original_producer** — P7-BCN/manual-entry
- **p8_reconciliation** — 2026-09-25
- **note** — Contabilidad publica: flujo de ingresos de gestion ordinaria 2023 del Ayuntamiento de Barcelona (resultado, no balance).

### `P7-BCN-2026-0002`

- **domain** — contabilidad_publica
- **original_producer** — P7-BCN/manual-entry
- **p8_reconciliation** — 2026-09-25
- **note** — Contabilidad publica: patrimonio neto ECPN a 31/12/2023 del Ayuntamiento de Barcelona (stock de balance).

### `P7-BCN-2026-0003`

- **domain** — contabilidad_publica
- **original_producer** — P7-BCN/manual-entry
- **p8_reconciliation** — 2026-09-25
- **note** — Contabilidad publica: deuda financiera a largo plazo (obligaciones) del Ayuntamiento de Barcelona (pasivo).

### `P7-BCN-2026-0004`

- **domain** — contabilidad_publica
- **original_producer** — P7-BCN/manual-entry
- **p8_reconciliation** — 2026-09-25
- **note** — Contabilidad publica: provisiones a largo plazo del Ayuntamiento de Barcelona (pasivo contingente).

### `P7-BCN-2026-0005`

- **domain** — contabilidad_publica
- **original_producer** — P7-BCN/manual-entry
- **p8_reconciliation** — 2026-09-25
- **note** — Contabilidad publica: infraestructuras a coste historico del Ayuntamiento de Barcelona (activo no corriente).

### `P7-BCN-2026-0006`

- **domain** — contabilidad_publica
- **original_producer** — P7-BCN/manual-entry
- **p8_reconciliation** — 2026-09-25
- **note** — Contabilidad publica: obligaciones ambientales reconocidas 2023 del Ayuntamiento de Barcelona (compromiso de gasto).
