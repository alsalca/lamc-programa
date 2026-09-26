# EVIDENCE.md — Cada cifra con su fuente citable

**Dominio:** Ayuntamiento de Barcelona — Cuenta General 2023
**Fuente primaria:** [Cuenta General del Ayuntamiento de Barcelona 2023](https://ajuntament.barcelona.cat/pressupostosifinances/sites/default/files/COMPTE%20GENERAL%202023.pdf)
**SHA256 del PDF:** `3d7d494fb96f3fa1d6b7b28a0f2870b381fb0c076e16a314bed6c1dc92cb4351`
**Tamaño:** 26.860.658 bytes · 169 páginas
**Idioma original:** Catalán
**Fecha de extracción:** 2026-09-25

---

## Ficha 0001 — Ingresos totales de gestión ordinaria 2023

| Campo | Valor |
|-------|-------|
| **Cifra** | **3.332.351.497,29 EUR** |
| **Ubicación en documento** | Página 7: Compte del Resultat Econòmic Patrimonial |
| **Línea exacta** | `A) TOTAL INGRESSOS DE GESTIÓ ORDINÀRIA (1+2+3+4+5+6+7)` |
| **Desglose** | Ingressos 1.456.820.510,65 + Transferències i subvencions rebudes 1.620.525.972,49 + Vendes i prestacions de servei 54.448.562,90 + Altres ingressos 144.517.852,23 + Excessos de provisions 56.038.599,02 |
| **Tipo de claim** | Flujo (NO es balance) |
| **Instrumento** | NONE (ingreso, no instrumento financiero) |

---

## Ficha 0002 — Patrimonio neto ECPN a 31/12/2023

| Campo | Valor |
|-------|-------|
| **Cifra** | **12.629.039.834,15 EUR** |
| **Ubicación en documento** | Página 6: Balanc a 31 de Desembre de 2023 |
| **Línea exacta** | `A) PATRIMONI NET ECPN` |
| **Desglose** | I. Patrimoni 7.787.674.637,92 + II. Patrimoni generat 3.844.509.951,31 + IV. Subvencions rebudes pendents d'imputació 996.855.244,92 |
| **Cambio vs 2022** | +409.757.289,38 EUR (+3,35%) |
| **Tipo de claim** | Balance (stock) |
| **Instrumento** | NONE (EUR) |

---

## Ficha 0003 — Obligaciones y otros valores negociables a largo plazo

| Campo | Valor |
|-------|-------|
| **Cifra** | **95.000.000,00 EUR** |
| **Ubicación en documento** | Página 6: Balanc, sección B) PASSIU NO CORRENT, línea II. Deutes a llarg termini, sublínea 1 |
| **Línea exacta** | `1. Obligacions i altres valors negociables` |
| **Igualdad 2022-2023** | Exactamente igual: 95.000.000,00 EUR en ambos ejercicios |
| **Detalle memoria** | Página 51: Préstamos con vencimiento 2037-2043. Total deuda financiera LP: 1.104.988.571,37 EUR |
| **Tipo de claim** | Deuda (obligación) |
| **Instrumento** | DEBT (EUR) |

---

## Ficha 0004 — Provisiones a largo plazo

| Campo | Valor |
|-------|-------|
| **Cifra** | **17.493.930,44 EUR** |
| **Ubicación en documento** | Página 6: Balanc, sección B) PASSIU NO CORRENT, línea I. Provisions a llarg termini |
| **Línea exacta** | `I. Provisions a llarg termini 16` |
| **Cambio vs 2022** | -909.794,44 EUR (-4,94%) — disminución |
| **Nota 16** | Detalle de provisiones en memoria (causas, movimientos) |
| **Tipo de claim** | Obligación contingente |
| **Instrumento** | DEBT (EUR) |

---

## Ficha 0005 — Infraestructuras (coste acumulado)

| Campo | Valor |
|-------|-------|
| **Cifra** | **5.598.515.769,72 EUR** |
| **Ubicación en documento** | Página 41: Nota 5.4 Infraestructures |
| **Desglose** | Vials 3.707.227.004,23 + Parcs i jardins 1.319.861.460,51 + Mixte 458.001.476,71 + Forestal 60.457.445,40 + Industrial 21.538.366,85 + Sistemes 10.120.958,13 + Edificis 10.995.624,12 + Equipaments 9.865.843,58 + Rústic 447.590,19 |
| **Nota** | Vials (carreteras) = 66% del total |
| **Tipo de claim** | Activo no corriente (coste histórico) |
| **Instrumento** | NONE (EUR) |

---

## Ficha 0006 — Obligaciones medioambientales reconocidas 2023

| Campo | Valor |
|-------|-------|
| **Cifra** | **94.629.028,63 EUR** |
| **Ubicación en documento** | Página 61: Nota 17. Informació sobre el medi ambient |
| **Desglose** | Construcció i manteniment d'espais verds 86.245.264,31 + Biodiversitat 27.037,16 + Intervenció mediambiental 3.822.167,98 + Intervenció acústica ambiental 415.088,64 + Educació mediambiental 1.645.640,05 + Gestió de residus energètics locals 1.487.913,26 + Coordinació urbana. Vehicle elèctric 614.253,85 + Coordinació Urbana. Obres 229.200,16 + Coordinació d'obres. Resiliència Urbana 142.463,22 |
| **Tipo de claim** | Compromiso de gasto ambiental |
| **Instrumento** | DEBT (EUR) |

---

## Observaciones sobre el contrato

### Lo que encajó directamente
- **subject:** Ayuntamiento de Barcelona es claramente LEGAL_ENTITY con identificador estable
- **container:** DOCUMENTARY_ASSET para la Cuenta General — el documento ES el contenedor de la evidencia
- **instrument:** NONE para flujos y saldos, DEBT para obligaciones — el vocabulario cubre los casos
- **quantity:** Las cifras exactas del documento encajan en el formato decimal del contrato
- **source_type:** SIGNED_DOCUMENT — documento oficial auditado
- **authority:** INSTITUTION_DOCUMENT — la Sindicatura de Comptes responde por la auditoría

> **CORRECCIÓN 2026-09-26:** las fichas 0002 y 0005 ya no usan `instrument.kind: FIAT_BALANCE`; usan `NONE` con `symbol: EUR`. Se alinean con ellas la tabla de la ficha 0002, la de la ficha 0005 y esta observación. Ninguna ficha del bundle usa ya `FIAT_BALANCE`.

### Lo que tensó el contrato
- **freshness:** El documento no declara explícitamente una política de vigencia. Las fichas 0003-0006 declaran UNKNOWN en freshness con su motivo
- **container_id:** No hay un número de "cuenta" estándar para una cuenta general de ayuntamiento — se usó una etiqueta LOCAL
- **Confianza:** Todas las fichas quedan en "medium" porque freshness no es "fresh" (datos históricos)
- **Diversidad de autoridades:** Las 6 fichas usan la misma autoridad (INSTITUTION_DOCUMENT) porque todas vienen del mismo documento. Esto es esperado para un dominio único

### Huecos declarados
Ver `unknowns.md` para el detalle completo.

---

## Procedencia por ficha

> Estas notas estaban dentro del JSON, en una clave `_meta` que viajaba
> **dentro de cada ficha**. El contrato no la admite (`additionalProperties: false`),
> así que las fichas no validaban contra su propio esquema. El contenido es el mismo,
> y aquí —al lado de la evidencia— se lee mejor.

### `P7-BCN-2026-0001`

- **domain** — Ayuntamiento de Barcelona
- **document** — Cuenta General 2023 (Comptes Generals 2023)
- **language** — Catalan
- **pdf_url** — https://ajuntament.barcelona.cat/pressupostosifinances/sites/default/files/COMPTE%20GENERAL%202023.pdf
- **pdf_sha256** — 3d7d494fb96f3fa1d6b7b28a0f2870b381fb0c076e16a314bed6c1dc92cb4351
- **pdf_bytes** — 26860658
- **pdf_pages** — 169
- **extraction_date** — 2026-09-25
- **extraction_method** — pypdf text extraction from downloaded PDF
- **note** — Ingresos totales de gestion ordinaria 2023. Instrument=NONE porque es un flujo, no un instrumento financiero.

### `P7-BCN-2026-0002`

- **domain** — Ayuntamiento de Barcelona
- **document** — Cuenta General 2023 (Comptes Generals 2023)
- **language** — Catalan
- **pdf_url** — https://ajuntament.barcelona.cat/pressupostosifinances/sites/default/files/COMPTE%20GENERAL%202023.pdf
- **pdf_sha256** — 3d7d494fb96f3fa1d6b7b28a0f2870b381fb0c076e16a314bed6c1dc92cb4351
- **pdf_bytes** — 26860658
- **pdf_pages** — 169
- **extraction_date** — 2026-09-25
- **extraction_method** — pypdf text extraction from downloaded PDF
- **note** — Patrimonio neto ECPN a 31/12/2023. Balance general de la entidad.

### `P7-BCN-2026-0003`

- **domain** — Ayuntamiento de Barcelona
- **document** — Cuenta General 2023 (Comptes Generals 2023)
- **language** — Catalan
- **pdf_url** — https://ajuntament.barcelona.cat/pressupostosifinances/sites/default/files/COMPTE%20GENERAL%202023.pdf
- **pdf_sha256** — 3d7d494fb96f3fa1d6b7b28a0f2870b381fb0c076e16a314bed6c1dc92cb4351
- **pdf_bytes** — 26860658
- **pdf_pages** — 169
- **extraction_date** — 2026-09-25
- **extraction_method** — pypdf text extraction from downloaded PDF
- **note** — Obligaciones y otros valores negociables a largo plazo. El saldo de 95M EUR es IDENTICO en 2022 y 2023: la entidad no amortizo ni emitio nuevas obligaciones en el ejercicio. La memoria (pag 51) muestra prestamos con vencimientos de 2037 a 2043.

### `P7-BCN-2026-0004`

- **domain** — Ayuntamiento de Barcelona
- **document** — Cuenta General 2023 (Comptes Generals 2023)
- **language** — Catalan
- **pdf_url** — https://ajuntament.barcelona.cat/pressupostosifinances/sites/default/files/COMPTE%20GENERAL%202023.pdf
- **pdf_sha256** — 3d7d494fb96f3fa1d6b7b28a0f2870b381fb0c076e16a314bed6c1dc92cb4351
- **pdf_bytes** — 26860658
- **pdf_pages** — 169
- **extraction_date** — 2026-09-25
- **extraction_method** — pypdf text extraction from downloaded PDF
- **note** — Provisiones a largo plazo. Disminuyeron de 18,4M a 17,5M entre 2022 y 2023. La memoria (nota 16) detalla las causas.

### `P7-BCN-2026-0005`

- **domain** — Ayuntamiento de Barcelona
- **document** — Cuenta General 2023 (Comptes Generals 2023)
- **language** — Catalan
- **pdf_url** — https://ajuntament.barcelona.cat/pressupostosifinances/sites/default/files/COMPTE%20GENERAL%202023.pdf
- **pdf_sha256** — 3d7d494fb96f3fa1d6b7b28a0f2870b381fb0c076e16a314bed6c1dc92cb4351
- **pdf_bytes** — 26860658
- **pdf_pages** — 169
- **extraction_date** — 2026-09-25
- **extraction_method** — pypdf text extraction from downloaded PDF
- **note** — Valor coste historico de infraestructuras del Ayuntamiento. La partida mas grande es Vials (carreteras): 3.707M EUR, el 66% del total. El dato es coste, no valor razonable.

### `P7-BCN-2026-0006`

- **domain** — Ayuntamiento de Barcelona
- **document** — Cuenta General 2023 (Comptes Generals 2023)
- **language** — Catalan
- **pdf_url** — https://ajuntament.barcelona.cat/pressupostosifinances/sites/default/files/COMPTE%20GENERAL%202023.pdf
- **pdf_sha256** — 3d7d494fb96f3fa1d6b7b28a0f2870b381fb0c076e16a314bed6c1dc92cb4351
- **pdf_bytes** — 26860658
- **pdf_pages** — 169
- **extraction_date** — 2026-09-25
- **extraction_method** — pypdf text extraction from downloaded PDF
- **note** — Obligaciones medioambientales reconocidas en 2023. La mayoria (86,2M) corresponde a construccion y mantenimiento de espacios verdes. Son compromisos de gasto, no deuda financiera.
