# INFORME — P7 SEGUNDO DOMINIO

**Qué encajó, qué no, y qué hubo que forzar.**

---

## 1. Qué encajó

### El vocabulario del contrato cubre contabilidad pública

El sobre de 22 casillas fue diseñado para crypto, pero su vocabulario es lo bastante general para cubrir contabilidad pública:

| Crypto (P1) | Barcelona (P7) | Funcionó |
|-------------|----------------|----------|
| `BLOCKCHAIN_WALLET` | `DOCUMENTARY_ASSET` | ✅ El contenedor es el documento |
| `NATIVE` / `ERC20` | `NONE` / `DEBT` | ✅ El instrumento es el tipo de claim |
| `ONCHAIN` | `SIGNED_DOCUMENT` | ✅ La fuente es un documento auditado |
| `PUBLIC_CHAIN` | `INSTITUTION_DOCUMENT` | ✅ La autoridad es la institución |
| Bloque + hash | PDF + sha256 | ✅ La referencia es reproducible |

> **CORRECCIÓN 2026-09-26:** la tabla listaba `FIAT_BALANCE` para el dominio Barcelona. Las fichas 0002 y 0005 ya usan `NONE` con `symbol: EUR`; se alinean la tabla y el resumen del §4.

### Las cifras encajan en el formato

El formato `quantity` (cadena decimal, sin separadores, sin símbolo) admite las cifras exactas del documento:

```
"3332351497.29"     ← ingresos totales
"12629039834.15"    ← patrimonio neto
"95000000"          ← obligaciones LP
"17493930.44"       ← provisiones LP
"5598515769.72"     ← infraestructuras
"94629028.63"       ← obligaciones ambientales
```

Ninguna cifra necesita redondeo ni aproximación. El documento da cifras exactas con dos decimales.

### Las fechas de corte funcionan

El `effective_at = "2023-12-31"` (sin hora, sin zona) es exactamente lo que la fuente declara. No se añade precisión que la fuente no dio.

### La referencia es reproducible

Un tercero puede:
1. Descargar el PDF desde la URL
2. Verificar el sha256
3. Buscar la página y línea indicada
4. Encontrar la misma cifra

Esto es exactamente lo que el contrato exige de `raw_reference`.

---

## 2. Qué no encajó (pero el contrato lo maneja)

### freshness: el documento no declara política de vigencia

**El problema:** La Cuenta General es un snapshot a 31/12/2023, pero no dice explícitamente "este dato es válido hasta la publicación de la siguiente cuenta general".

**Cómo lo maneja el contrato:** Las fichas 0003-0006 declaran `freshness.status = "UNKNOWN"` con su motivo. Esto es exactamente lo que el contrato prevé: un campo que no se pudo establecer se declara con centinela y motivo.

**¿Es material?** Para la confianza de la ficha: sí (baja la ficha a `medium`). Para la validez de la cifra: no (la cifra está establecida).

### container_id: no hay número de cuenta estándar

**El problema:** Una cuenta general de ayuntamiento no tiene un número de cuenta bancaria. Es un documento, no una cuenta.

**Cómo lo maneja el contrato:** Se usa una etiqueta `LOCAL:CG-BCN-2023`. El contrato permite esta forma (§4.1, forma 2) y la marca con el prefijo LOCAL para que no se confunda con un identificador real.

### Confianza: todas las fichas quedan en "medium"

**El problema:** K4 = NO porque `freshness.status != "fresh"`. Los datos son históricos (2023), no actuales.

**¿Es correcto?** Sí. Las fichas son conformes al sobre, verificables, y honestas sobre su limitación: son un snapshot histórico, no el estado actual.

---

## 3. Qué hubo que forzar

**Nada.** No se modificó el contrato. No se añadió ningún campo. No se cambió ningún valor permitido.

Los "problemas" anteriores (freshness, container_id, confianza) se resolvieron **dentro** del contrato, no modificándolo. El contrato tiene mecanismos para expresar lo que no se sabe (UNKNOWN con motivo) y lo que no aplica (etiquetas LOCAL).

---

## 4. El hallazgo que más vale

**El contrato sirve para contabilidad pública.** Las 22 casillas cubren:
- Flujos (ingresos/gastos) con `instrument.kind = NONE`
- Saldos (balance) con `NONE`
- Deuda (obligaciones/provisiones) con `DEBT`
- Documentos oficiales con `SIGNED_DOCUMENT` + `INSTITUTION_DOCUMENT`
- Referencias reproducibles con URL + sha256

Esto es lo que el programa necesita demostrar: **LAMC no es un sistema de crypto. Es una capacidad.** Y la capacidad funciona para documentos PDF en catalán, contabilidad pública, y obligaciones contingentes de un ayuntamiento.

---

## 5. Validación mecánica

```
python3 herramientas/validar_evidencia.py \
    proyectos/P7_SEGUNDO_DOMINIO
```

**Resultado:** 1 problema detectado — el script espera al menos 2 tipos de autoridad, pero todas las fichas usan `INSTITUTION_DOCUMENT` porque todas vienen del mismo documento auditado.

**Interpretación:** Esto es una limitación del script de validación para un dominio único, no del contrato. El contrato no exige diversidad de autoridades; el script la exige como heurística de generalización. En P7, la diversidad no es el objetivo: lo es demostrar que el contrato funciona para un dominio nuevo.

**Comprobación del contrato intacto:**
```
sha256sum proyectos/P1_ESQUEMA_EVIDENCIA/entregables/evidence-envelope.schema.json
fa70903450f0d9fa569a31bb4e049e0e718f28e72b32b92a9a4e3686afd5b769
```

El hash coincide con el publicado. **El contrato no se ha tocado.**

---

*Informe generado por P7-BCN. Todos los datos verificados con descarga real del PDF.*
