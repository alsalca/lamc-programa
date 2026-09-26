# DOMINIOS.md — Diseño del Ledger Reconciliado P8

**Proyecto:** P8_RECONCILIACION
**Estado:** ✅ **EJECUTADO** — el ledger se emitió (`bundle/ledger.json`, 13 fichas). El
diseño de abajo es el que se aplicó.
**Versión:** 1.1.0
**Creado:** 2026-09-25 · **Corregido:** 2026-09-25 (auditoría independiente)

> **CORRECCIÓN 2026-09-25 (hallazgos 16 y 17 de la auditoría independiente).**
> 1. Esta línea decía «📋 Diseño (**pendiente HG-009**)» y el ledger ya estaba emitido:
>    o la línea era falsa, o **se había pasado un Human Gate sin dejar registro**. El
>    auditor no pudo decidir cuál, y con razón. **Se resolvió el 2026-09-25 por el Chat
>    Jefe** (que es la autoridad de HG-009 para el filtro técnico), con el diseño y el
>    ledger a la vista, y **se registra aquí**: el diseño del ledger es correcto en lo
>    esencial — los 22 campos intactos, los dos dominios sin fusionar, la reconciliación
>    declarada. La objeción del §4.3 sobre `_meta` era **errónea** y está corregida abajo.
>    Queda escrito que **la ejecución precedió al registro**: eso es un fallo de proceso,
>    no un mérito, y por eso se dice en lugar de disimularse.
> 2. El §1 titulaba el segundo dominio «Contabilidad pública (**PUBLIC_API**)» mientras la
>    propia fila de tipo de fuente decía `SIGNED_DOCUMENT`. El charter §6 esperaba
>    `PUBLIC_API`; la fuente real resultó ser un **documento firmado descargable**, no una
>    API. Manda la realidad: el dominio es de fuente `SIGNED_DOCUMENT`.

---

## 1. Los dos dominios

| Característica | Blockchain (ONCHAIN) | Contabilidad pública (**SIGNED_DOCUMENT**) |
|---|---|---|
| **Proyecto origen** | P2_DEMO_RECONSTRUCCION + P3_OPS_SEC | P7_SEGUNDO_DOMINIO |
| **Sujeto** | Aave DAO AHAB Safe (LEGAL_ENTITY) | Ayuntamiento de Barcelona (LEGAL_ENTITY) |
| **Documento fuente** | positions.json (P2 bundle) | fichas.json (P7 bundle) |
| **Esquema** | evidence-envelope.schema.json v0.2.0 | evidence-envelope.schema.json v0.2.0 |
| **Tipo de fuente** | ONCHAIN / STRUCTURED_EXPORT | SIGNED_DOCUMENT |
| **Naturaleza** | Estado puntual de protocolo DeFi (snapshot por bloque) | Cuenta General anual auditada (stock + flujo) |
| **Divisa** | USD (Aave base units con 8 decimales) / ETH (rETH, wstETH) | EUR |
| **Cantidad de fichas** | 7 (positions.json) | 6 (fichas.json) |
| **Contenedores** | BLOCKCHAIN_WALLET (Ethereum + Base) | DOCUMENTARY_ASSET, CREDIT_ACCOUNT |
| **Instrumentos** | LENDING_POSITION, DEBT, ERC20, NONE | NONE, DEBT |

---

## 2. Fichas del dominio blockchain — qué entra

Se toman las 7 fichas de `P2_DEMO_RECONSTRUCCION/entregables/bundle/positions.json` **sin modificaciones en su contenido**.

- `source_type` ya está en `ONCHAIN` (fichas 0001–0006) y `STRUCTURED_EXPORT` (0007).
- Se pensó añadir un campo `_meta.domain` para traza. **RETIRADO** — el contrato no admite ningún campo dentro de la ficha que él no declare (ver §4.3). **Lo que se copia no lleva nada añadido.**
- `reconciliation_status`: se planteó pasar de `"unreconciled"` a `"reconciled"` o `"disputed"`. **No ocurrió, y fue deliberado:** lo que se reconcilia es la **procedencia** entre dominios, no las cifras —dos sujetos distintos no se suman ni se restan—, así que las 13 fichas quedan en `"unreconciled"`. El ledger lo declara así.

### Fichas blockchain admitidas (7)

| claim_id | `instrument.kind` | `instrument.symbol` | Cantidad | Efectivo a | Nota |
|---|---|---|---|---|---|
| LAMC-P2-2026-0001 | `LENDING_POSITION` | `USD` | 24.783.691,41 USD | 2026-09-23 | Ethereum — colateral total |
| LAMC-P2-2026-0002 | `DEBT` | `AAVE_ACCOUNT_DEBT_BASE_USD` | 2.369.837,79 USD | 2026-09-23 | Ethereum — deuda total |
| LAMC-P2-2026-0003 | `ERC20` | `rETH` | 51,628217546317516669 rETH | 2026-09-23 | Ethereum — token holding |
| LAMC-P2-2026-0004 | `LENDING_POSITION` | `USD` | 14.985,88 USD | 2026-09-23 | Base — colateral total |
| LAMC-P2-2026-0005 | `NONE` | `AAVE_HEALTH_FACTOR` | UNKNOWN | 2026-09-23 | Base — sin deuda, el HF no aplica |
| LAMC-P2-2026-0006 | `ERC20` | `wstETH` | 0 | 2026-09-23 | Ethereum — saldo cero medido |
| LAMC-P2-2026-0007 | `NONE` | — (sin símbolo) | UNKNOWN | UNKNOWN | Doc — publicación de dirección, no un instrumento |

> **CORRECCIÓN 2026-09-26 (residual de la Revisión 3).** Esta tabla tenía **una sola columna,
> «Instrumento», que mezclaba dos conceptos distintos**: en unas filas ponía el **tipo**
> (`instrument.kind`) y en otras el **símbolo** (`instrument.symbol`). Ahora son **dos columnas**
> y cada una dice lo que es. No era un dato falso —los valores eran correctos—, pero **una
> columna que significa dos cosas distintas se lee mal y se cita peor.**

Además se referencia el estándar P3 (`STANDARD.md`) como documentación de controles operacionales del dominio blockchain — no como fichas de ledger, sino como contexto de seguridad.

> **CORRECCIÓN 2026-09-25 (revisión de publicación).** Esta tabla describía las fichas de P2 **con datos que P2 ya no tiene**. Decía que sus instrumentos eran «NATIVE, TOKEN, OTHER» — y `TOKEN` y `OTHER` **no existen en el contrato**: el enum de `instrument.kind` admite `NATIVE`, `ERC20`, `SPL`, `JETTON`, `BEP20`, `ERC721`, `ERC1155`, `LP_POSITION`, `LENDING_POSITION`, `CASH`, `FIAT_BALANCE`, `DEBT` y `NONE`. Cinco de las siete fichas usaban un valor inventado y **la herramienta no lo comprobaba**, así que decía `APROBADO`. Ya se corrigieron las fichas (0002 → `DEBT`; 0003 y 0006 → `ERC20`; 0005 y 0007 → `NONE`) y **la herramienta ahora recorre todos los enums del contrato**.
>
> Y la ficha 0003 aparecía con «51.6282 rETH»: era un redondeo de `51.628217546317516669`, presentado como si fuera el valor. Aquí va el valor de la ficha.
>
> **Esta página es de P8 y no la corrigió quien arregló P2**, precisamente para que el cambio no se hiciera en un solo sitio: si el ledger y su descripción se separan, una de las dos miente.

---

## 3. Fichas del dominio contabilidad pública — qué entra

Se toman las 6 fichas de `P7_SEGUNDO_DOMINIO/entregables/bundle/fichas.json` **sin modificaciones en su contenido**, solo se añade:

- `source_type` ya está en `SIGNED_DOCUMENT`.
- Se añade campo `_meta.domain` con valor `"contabilidad_publica"` para traza. **RETIRADO** — el contrato no admite ese campo dentro de la ficha (ver §4.3).
- `reconciliation_status` **queda en `unreconciled`** en las 13 fichas, y fue deliberado: lo que se reconcilia es la **procedencia** entre dominios, no las cifras —cada dominio tiene un sujeto distinto, así que no se suman ni se restan—, y por eso ninguna pasa a `reconciled` ni a `disputed`. El ledger lo declara así; misma decisión que en el dominio blockchain (§2).

### Fichas contabilidad admitidas (6)

| claim_id | Instrumento | Cantidad | Efectivo a | Nota |
|---|---|---|---|---|
| P7-BCN-2026-0001 | NONE (EUR) — ingresos gestión ordinaria | 3.332.351.497,29 EUR | 2023-12-31 | Flujo de ingresos |
| P7-BCN-2026-0002 | NONE (EUR) — patrimonio neto | 12.629.039.834,15 EUR | 2023-12-31 | Stock de patrimonio |
| P7-BCN-2026-0003 | DEBT (EUR) — obligaciones LP | 95.000.000,00 EUR | 2023-12-31 | Deuda financiera LP |
| P7-BCN-2026-0004 | DEBT (EUR) — provisiones LP | 17.493.930,44 EUR | 2023-12-31 | Obligaciones contingentes |
| P7-BCN-2026-0005 | NONE (EUR) — infraestructuras | 5.598.515.769,72 EUR | 2023-12-31 | Activo no corriente (coste histórico) |
| P7-BCN-2026-0006 | DEBT (EUR) — obligaciones ambientales | 94.629.028,63 EUR | 2023-12-31 | Compromisos de gasto |

---

## 4. Diseño del ledger: estructura

El ledger será un **array JSON** donde cada elemento es una ficha conforme al esquema `evidence-envelope.schema.json` v0.2.0.

### 4.1 Criterios de distinción de dominios

Cada ficha del ledger debe poder trazarse a su dominio de origen. Se usan estos campos:

| Campo | Blockchain | Contabilidad pública |
|---|---|---|
| `source_type` | `ONCHAIN` (fichas 0001–0006) / `STRUCTURED_EXPORT` (0007) | `SIGNED_DOCUMENT` |
| `container.type` | `BLOCKCHAIN_WALLET` | `DOCUMENTARY_ASSET` / `CREDIT_ACCOUNT` |
| `authority` | `PUBLIC_CHAIN` (fichas 0001–0006) / `INSTITUTION_DOCUMENT` (0007) | `INSTITUTION_DOCUMENT` |
| `claim_id` prefijo | `LAMC-P2-*` | `P7-BCN-*` |
| `producer` | `LAMC-P2/*` | `P7-BCN/*` |
| `_meta.domain` (campo agregado) — **RETIRADO**, ver §4.3 | `"blockchain"` | `"contabilidad_publica"` |

### 4.2 Campo `_meta` agregado — **RETIRADO** (ver §4.3 y la corrección de cabecera)

> Se conserva el diseño tal como se escribió, porque **explica qué se intentó**. Pero
> **no se aplicó**: este campo viajaba dentro de cada ficha y el contrato no lo admite.
> Su contenido vive ahora en la tabla de §6 y en `bundle/reconciliacion.md`.

Cada ficha del ledger llevará un campo `_meta` (no validado por el esquema) con:

```json
"_meta": {
  "domain": "blockchain" | "contabilidad_publica",
  "original_producer": "LAMC-P2/..." | "P7-BCN/...",
  "p8_reconciliation": "2026-09-25",
  "note": "Breve descripción de la naturaleza de la ficha en contexto del ledger"
}
```

### 4.3 Conservación de integridad

- Ninguna ficha existente se modifica en sus 22 campos obligatorios.
- **`_meta` se eliminó el 2026-09-25.** Aquí decía que era «un campo adicional no controlado
  por el esquema, permitido porque `additionalProperties: false` se aplica solo al sobre, no
  al documento general». **Era falso, y era el error de fondo:** `_meta` viajaba **dentro de
  cada ficha**, y cada ficha **es** el sobre. El esquema declara `additionalProperties:
  false` en la raíz, así que **las 13 fichas no validaban contra su propio contrato**. La
  segunda mitad de la frase —«las fichas de P2 y P7 ya usan `_meta`»— también era falsa en
  el caso de P2: `positions.json` nunca lo usó. Se usó un hecho que no ocurría para
  justificar una violación del contrato.
  Su contenido **no se perdió**: está ahora en este documento y en
  `bundle/reconciliacion.md`, al lado de la evidencia y donde sí se puede leer.
- La validación del esquema se hace contra cada ficha individual, no contra el array
  contenedor. Eso sigue siendo cierto — y ahora **las fichas también pasan**.

### 4.4 Reconciliación: qué significa

Las fichas de **distintos dominios** no se restan ni se suman: pertenecen a sujetos distintos (Aave DAO ≠ Ayuntamiento de Barcelona). La reconciliación es:

- **Clasificación:** cada ficha se etiqueta como activo o pasivo del sujeto que la afirma.
- **Procedencia:** cada ficha identifica su dominio de origen.
- **Huecos:** se declaran los campos que no se pudieron establecer.
- **Lo que NO se hace:** no se suma colateral Aave + patrimonio Barcelona; no se resta deuda Aave de deuda Barcelona; no se colapsan dominios.

### 4.5 Activación de la reconciliación

#### Dominio blockchain — activos y pasivos

| Ficha | Naturaleza | Activo/Pasivo | Explicación |
|---|---|---|---|
| LAMC-P2-2026-0001 | Colateral total en Aave (Ethereum) | **Activo** | Derecho económico del sujeto sobre el protocolo |
| LAMC-P2-2026-0002 | Deuda total en Aave (Ethereum) | **Pasivo** | Obligación del sujeto frente al protocolo |
| LAMC-P2-2026-0003 | rETH en wallet (Ethereum) | **Activo** | Token holding, propiedad del sujeto |
| LAMC-P2-2026-0004 | Colateral total en Aave (Base) | **Activo** | Derecho económico en Base |
| LAMC-P2-2026-0005 | Health Factor (Base) | **Control** | No es activo ni pasivo; es métrica de riesgo |
| LAMC-P2-2026-0006 | wstETH — saldo cero | **Activo (cero)** | Saldo medido = 0; no hay posición |
| LAMC-P2-2026-0007 | Publicación de dirección | **Contexto** | No es financiero; es documentación |

#### Dominio contabilidad pública — activos y pasivos

| Ficha | Naturaleza | Activo/Pasivo | Explicación |
|---|---|---|---|
| P7-BCN-2026-0001 | Ingresos de gestión ordinaria | **Flujo (ingreso)** | No es balance; es resultado del ejercicio |
| P7-BCN-2026-0002 | Patrimonio neto | **Patrimonio** | Diferencia activo - pasivo |
| P7-BCN-2026-0003 | Deuda financiera LP | **Pasivo** | Obligación frente a acreedores |
| P7-BCN-2026-0004 | Provisiones LP | **Pasivo** | Obligación contingente |
| P7-BCN-2026-0005 | Infraestructuras (coste) | **Activo** | Activo no corriente |
| P7-BCN-2026-0006 | Obligaciones ambientales | **Pasivo** | Compromiso de gasto |

---

## 5. Fichas que NO entran

| Razón | Detalle |
|---|---|
| Portafolio personal del operador | Fuera de alcance del charter |
| Cifras estimadas o proyectadas | Solo datos observados de fuente |
| Datos sin procedencia verificable | Toda ficha requiere source_reference |
| Estándar P3 completo | No son fichas; se referencia como contexto de seguridad |

---

## 6. Esquema de validación

```bash
python3 herramientas/validar_evidencia.py proyectos/P8_RECONCILIACION
```

Cada ficha del ledger debe pasar la validación contra `evidence-envelope.schema.json` v0.2.0.

Además:
```bash
grep -c '"source_type"' bundle/ledger.json
grep -o '"source_type":"[^"]*"' bundle/ledger.json | sort -u
```

Debe mostrar al menos los valores `ONCHAIN` y `SIGNED_DOCUMENT` (o el que corresponda a cada dominio).

---

## 7. Resumen del diseño

- **Total fichas:** 13 (7 blockchain + 6 contabilidad pública)
- **Dominios distinguibles por:** `source_type`, `container.type`, `authority`, prefijo de `claim_id` y `producer` — **cinco señales**, ninguna añadida al contrato
- **No se colapsan:** ningún cálculo cruza dominios; cada ficha conserva su sujeto original
- **No se inventa:** todas las fichas vienen de los bundles existentes de P2 y P7
- **El contrato no se toca:** 22 casillas, v0.2.0
- **Campo nuevo: NINGUNO.** Se intentó añadir `_meta.domain` y **se retiró**: el contrato no admite campos fuera de sus 22 casillas (ver §4.3)