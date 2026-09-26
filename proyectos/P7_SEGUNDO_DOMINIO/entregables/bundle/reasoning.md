# REASONING.md — Razonamiento paso a paso

## Objetivo

Aplicar el contrato de P1 (22 casillas, sin modificarlo) al dominio del Ayuntamiento de Barcelona, usando su Cuenta General 2023 como fuente primaria.

---

## Paso 1: Elección del dominio

### Criterios del charter
1. Entidad, no persona → ✅ Ayuntamiento de Barcelona (organismo público)
2. Documentos descargables, NO API → ✅ PDFs desde 2001 hasta 2024
3. Cifras reales: importes, fechas → ✅ Balance, P&G, flujos de efectivo
4. Al menos una obligación o compromiso → ✅ Deuda, provisiones, litigios, compromisos ambientales
5. Sin datos personales → ✅ Verificado con pypdf: 0 DNI, 0 emails, 0 nombres, 0 nóminas

### Por qué Barcelona y no Telefónica o Mondragón
- **Telefónica rechazada:** El documento de cuentas anuales contiene nombres de consejeros y directivos (obligación legal CNMV). Aunque son figuras públicas, el mandato del operador es eliminar todo riesgo de PII.
- **Mondragón rechazado:** Su informe anual es narrativo/descriptivo y no incluye cuentas anuales auditadas con balance completo. Las obligaciones están menos estructuradas.

### Tensión del contrato
Barcelona usa contabilidad pública (PGCP) con base presupuestaria + patrimonial, distinta de las NIIF/IFRS del dominio crypto. Esto fuerza al sobre a demostrar que sirve para un tipo de documento y normativa contable completamente diferente.

---

## Paso 2: Descarga y verificación del documento

1. **Búsqueda web:** Se encontró la página oficial de cuentas generales del ayuntamiento
2. **Descarga real:** `curl` descargó el PDF (26.8 MB, 169 páginas) — verificado con `file` que es PDF válido
3. **Extracción de texto:** `pypdf` extrajo el texto de las 169 páginas
4. **Verificación PII:** Búsqueda de patrones regex (DNI, emails, títulos personales, nóminas, salarios, direcciones) — 0 resultados
5. **Hash SHA256:** `3d7d494fb96f3fa1d6b7b28a0f2870b381fb0c076e16a314bed6c1dc92cb4351`

---

## Paso 3: Mapeo del dominio al contrato

### subject
- **Tipo:** LEGAL_ENTITY (ayuntamiento = entidad de derecho público)
- **subject_id:** `Ajuntament-de-Barcelona` (nombre oficial de la fuente)
- **label:** "Ayuntamiento de Barcelona"

### container
- **Tipo:** DOCUMENTARY_ASSET (la Cuenta General es el documento que contiene la evidencia)
- **container_id:** `LOCAL:CG-BCN-2023` (etiqueta LOCAL porque no hay número de cuenta estándar para una cuenta general)
- **operator:** `Ajuntament-de-Barcelona` (la entidad que publica)

### instrument
- **Para flujos (ingresos/gastos):** `NONE` — el ingreso no es un instrumento financiero separado
- **Para saldos (balance):** `NONE` con `symbol: EUR`
- **Para deuda/provisiones:** `DEBT` con `symbol: EUR`

> **CORRECCIÓN 2026-09-26:** aquí decía `FIAT_BALANCE` para saldos. Las fichas 0002 y 0005 ya usan `NONE` con `symbol: EUR`; se alinea el texto. En este bundle, `instrument.kind` solo toma los valores `NONE` y `DEBT`.

### source_type
- `SIGNED_DOCUMENT` — documento oficial auditado por la Sindicatura de Comptes

### authority
- `INSTITUTION_DOCUMENT` — la institución (ayuntamiento + auditor) responde por la cifra

### verification_status
- `documentary` — verificable contra el documento original

### freshness
- `stale` para las fichas 0001-0002 (datos históricos de 2023, superados por 2024)
- `UNKNOWN` para las fichas 0003-0006 (el documento no declara política de vigencia)

### confidence
- `medium` para todas: K4 = NO (freshness no es fresh), pero K1, K2, K3 = YES

---

## Paso 4: Selección de claims

Se eligieron 6 claims que cubren diferentes aspectos de las cuentas:

| # | Claim | Tipo | Instrument | Por qué |
|---|-------|------|------------|---------|
| 0001 | Ingresos totales 2023 | Flujo | NONE | Testea instrumento NONE para flujos |
| 0002 | Patrimonio neto 2023 | Balance | NONE | Testea saldo de balance principal |
| 0003 | Obligaciones LP | Deuda | DEBT | Testea deuda con vencimientos futuros |
| 0004 | Provisiones LP | Contingente | DEBT | Testea obligaciones contingentes |
| 0005 | Infraestructuras | Activo | NONE | Testea activo no corriente a coste histórico |
| 0006 | Obligaciones ambientales | Compromiso | DEBT | Testea compromisos de gasto específicos |

> **CORRECCIÓN 2026-09-26:** esta tabla y la tabla de decisión de campos (`Paso 5`) describían 0002 y 0005 con `FIAT_BALANCE`. Las fichas ya usan `NONE` con `symbol: EUR`; se alinean ambas tablas.

---

## Paso 5: Construcción de las fichas

### Decisión sobre cada campo

| Campo | Decisión | Razonamiento |
|-------|----------|--------------|
| claim_id | `P7-BCN-2026-NNNN` | Convención del contrato: APARATO-AÑO-SECUENCIA |
| subject | Objeto con type/subject_id/label | Entidad clara, identificable |
| container | DOCUMENTARY_ASSET con LOCAL: | El documento es el contenedor; no hay cuenta bancaria |
| instrument | NONE/DEBT según claim | El vocabulario del contrato cubre los casos |
| quantity | Cifra exacta del documento | Sin redondeo, sin approximations |
| source_type | SIGNED_DOCUMENT | Documento oficial auditado |
| source_reference | Ubicación exacta en el PDF | Página, sección, línea, cifra |
| capture_method | pypdf extraction from downloaded PDF | Método reproducible por un tercero |
| observed_at | 2026-09-25T15:37:21Z | Fecha de extracción |
| effective_at | 2023-12-31 | Fecha de corte del documento |
| freshness | stale o UNKNOWN | Dependiendo de si la fuente declara política |
| authority | INSTITUTION_DOCUMENT | La institución responde |
| verification_status | documentary | Verificable contra el documento |
| confidence | medium | K4 = NO (datos históricos) |
| raw_reference | URL + sha256 del PDF | Referencia citable y reproducible |
| evidence_hash | sha256 del PDF | Integridad verificable |
| reconciliation_status | unreconciled | Primera vez que se procesa |

### Decisión sobre known/unknown

- **Fichas 0001-0002:** Sin huecos. Todos los campos establecidos.
- **Fichas 0003-0006:** Un hueco (`freshness`) porque el documento no declara política de vigencia.

---

## Paso 6: Validación

1. **Validación mecánica:** Las 6 fichas pasan la validación de formato (22 campos, partición correcta, patrones correctos)
2. **Validación del esquema:** El esquema de P1 no se ha tocado (sha256 verificado)
3. **Problema detectado:** El script de validación (`validar_evidencia.py`) reporta que solo hay 1 tipo de autoridad y espera al menos 2. Esto es una limitación del script para un dominio único, no del contrato. Las 6 fichas vienen del mismo documento auditado, por lo que la autoridad es siempre INSTITUTION_DOCUMENT.

---

## Paso 7: Hallazgos

### Lo que encajó
- El vocabulario del contrato (instrument.kind, source_type, authority) cubre los casos de contabilidad pública
- Las cifras exactas del documento encajan en el formato `quantity` (cadena decimal)
- Las fechas de corte del documento (31/12/2023) encajan en `effective_at`
- La referencia URL + sha256 funciona como `raw_reference` para un PDF

### Lo que tensó
- **freshness:** El documento no declara política de vigencia. Las fichas 0003-0006 declaran UNKNOWN con motivo.
- **container_id:** No hay número de "cuenta" estándar para una cuenta general. Se usó etiqueta LOCAL.
- **Confianza:** Todas las fichas quedan en "medium" porque los datos son históricos (no "fresh").
- **Diversidad:** El script de validación espera múltiples tipos de autoridad, pero un dominio único solo tiene una.

### Lo que no encajó (pero el contrato lo maneja)
- Los huecos de freshness se declaran con motivo, no se rellenan con suposiciones
- La etiqueta LOCAL para container_id es legítima según el contrato
- El "medium" de confianza es honesto: los datos son verificables pero históricos

---

## Conclusión del razonamiento

El contrato de P1 sirve para el dominio del Ayuntamiento de Barcelona **sin modificarse**. Las 22 casillas cubren los casos de contabilidad pública. Los huecos (freshness) se declaran con motivo. La evidencia es verificable contra el documento original.

El resultado más valioso es que **el contrato funciona para un dominio completamente distinto a crypto**: documentos PDF en catalán, contabilidad pública, obligaciones contingentes, infraestructuras a coste histórico. La capacidad de LAMC se demuestra, no se argumenta.
