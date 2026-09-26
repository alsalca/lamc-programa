# VEREDICTO — P7 SEGUNDO DOMINIO

## ¿El contrato sirvió sin modificarse?

# **SÍ.**

---

## Prueba

### 1. El contrato no se ha tocado

```
sha256sum evidence-envelope.schema.json
fa70903450f0d9fa569a31bb4e049e0e718f28e72b32b92a9a4e3686afd5b769
```

El hash del esquema de P1 coincide exactamente con el publicado en GitHub. **Ninguna casilla fue añadida, modificada o eliminada.**

### 2. Las 22 casillas se usaron todas

Cada una de las 6 fichas contiene exactamente 22 campos obligatorios. La partición `known`/`unknown` es exacta: cada campo está en exactamente una de las dos listas.

| Ficha | known | unknown | Total |
|-------|-------|---------|-------|
| 0001 | 22 | 0 | 22 |
| 0002 | 22 | 0 | 22 |
| 0003 | 21 | 1 | 22 |
| 0004 | 21 | 1 | 22 |
| 0005 | 21 | 1 | 22 |
| 0006 | 21 | 1 | 22 |

### 3. Un tercero puede reconstruir la situación

Un tercero que lea las fichas puede:
1. **Descargar el PDF** desde la URL citada en `raw_reference`
2. **Verificar el hash** SHA256 del documento
3. **Buscar la página y línea** indicada en `source_reference`
4. **Encontrar la misma cifra** en el documento original
5. **Validar la partición** known/unknown contra el esquema

Esto es exactamente la prueba falsable del charter:

> *Un tercero lee las fichas del segundo dominio y reconstruye la situación sin preguntar nada al autor — usando el manual de P1 tal como está publicado.*

### 4. Los huecos están declarados

Los 4 campos `unknown` (todos `freshness` en fichas 0003-0006) tienen su motivo en `unknown_reason`. Ningún UNKNOWN es un cero disfrazado. Ningún dato fue inventado para rellenar un hueco.

### 5. El dominio es una entidad, no persona

El Ayuntamiento de Barcelona es un organismo público con personalidad jurídica propia. Los datos son agregados institucionales. La verificación PII (pypdf + regex) encontró 0 resultados para DNI, emails, nombres personales, nóminas, salarios y direcciones.

---

## Qué funcionó

| Aspecto del contrato | Cómo se aplicó |
|---------------------|----------------|
| `instrument.kind = NONE` | Para flujos (ingresos) — el ingreso no es un instrumento financiero |
| `instrument.kind = NONE` | Para saldos (balance, infraestructuras) — no hay un instrumento separado del contenedor; `symbol: EUR` |
| `instrument.kind = DEBT` | Para deuda y provisiones — obligaciones en EUR |
| `source_type = SIGNED_DOCUMENT` | Documento oficial auditado por la Sindicatura de Comptes |
| `authority = INSTITUTION_DOCUMENT` | La institución (ayuntamiento + auditor) responde |
| `raw_reference` con URL + sha256 | PDF descargable con hash verificable |
| `UNKNOWN` con motivo | Para freshness cuando el documento no declara política |
| `LOCAL:` para container_id | Etiqueta propia cuando no hay número de cuenta estándar |

> **CORRECCIÓN 2026-09-26:** esta tabla describía los saldos (0002 y 0005) con `instrument.kind = FIAT_BALANCE`. Las fichas ya usan `NONE` con `symbol: EUR`; se alinea la fila. En este bundle `instrument.kind` solo toma `NONE` y `DEBT`.

## Qué tensó (pero no rompió)

| Aspecto | Cómo se resolvió |
|---------|------------------|
| `freshness` sin política declarada | Declarado `UNKNOWN` con motivo en 4 de 6 fichas |
| `container_id` sin número estándar | Etiqueta `LOCAL:CG-BCN-2023` |
| `confidence` limitado a `medium` | Por K4 = NO (datos históricos, no fresh) |
| Script de validación: diversidad de autoridades | Limitación del script, no del contrato. Todas las fichas vienen del mismo documento auditado |

## Lo que no se pudo forzar (y no hacía falta)

- **No se añadió ningún campo** al contrato
- **No se cambió ningún valor permitido** en los enums
- **No se modificó el esquema** ni la spec
- **No se inventó ningún dato** para rellenar huecos

---

## Conclusión

El contrato de P1 **sirve para contabilidad pública** sin modificarse. Las 22 casillas cubren flujos, saldos, deuda, provisiones, infraestructuras y compromisos ambientales de un ayuntamiento. Los huecos se declaran con motivo. La evidencia es verificable.

**LAMC no es un sistema de crypto. Es una capacidad.** Y la capacidad funciona para documentos PDF en catalán, contabilidad pública, y obligaciones contingentes de un ayuntamiento de 12.600 millones de euros de patrimonio neto.

El contrato resiste. La tesis se sostiene.

---

*Veredicto emitido por P7-BCN. Hash del esquema verificado. Fichas conformes.*
