# UNKNOWS.md — Los huecos declarados

**Regla A1:** UNKNOWN ≠ 0. Lo que no se sabe no es cero.
**Regla A3:** La ausencia de evidencia no constituye evidencia.

---

## Resumen

| Ficha | Campos unknown | Motivo principal |
|-------|----------------|------------------|
| P7-BCN-2026-0001 | 0 | Sin huecos |
| P7-BCN-2026-0002 | 0 | Sin huecos |
| P7-BCN-2026-0003 | 1 | freshness |
| P7-BCN-2026-0004 | 1 | freshness |
| P7-BCN-2026-0005 | 1 | freshness |
| P7-BCN-2026-0006 | 1 | freshness |

**Total de campos unknown: 4** (de 132 posibles = 6 fichas × 22 campos)

---

## Detalle por ficha

### P7-BCN-2026-0001 — Ingresos totales 2023
**Sin huecos.** Todos los 22 campos están establecidos.

La cifra (3.332.351.497,29 EUR) está directamente en el documento. El instrumento es NONE porque es un flujo, no un activo. La fecha de efecto (31/12/2023) es la del cierre del ejercicio.

### P7-BCN-2026-0002 — Patrimonio neto 2023
**Sin huecos.** Todos los 22 campos están establecidos.

El patrimonio neto (12.629.039.834,15 EUR) es la cifra de cierre del balance. Compuesto por patrimonio, patrimonio generado y subvenciones pendientes.

### P7-BCN-2026-0003 — Obligaciones LP

| Campo | Valor | Motivo del hueco |
|-------|-------|------------------|
| `freshness` | `"UNKNOWN"` | El documento no declara explícitamente una política de vigencia para los saldos de deuda. La fecha de corte (31/12/2023) va en `effective_at`, pero la duración de validez del dato como estado actual no está declarada por la fuente. |

**Detalle anidado:**
- `freshness.valid_until`: La fecha de vencimiento de las obligaciones no está en el balanc; se detalla parcialmente en la memoria (página 51) con vencimientos escalonados hasta 2043, pero no hay un único vencimiento que defina la vigencia del dato.

**Nota:** La cifra (95M EUR) es exactamente igual en 2022 y 2023, lo que indica que no hubo emisión ni amortización de obligaciones en el ejercicio. Este dato está establecido.

### P7-BCN-2026-0004 — Provisiones LP

| Campo | Valor | Motivo del hueco |
|-------|-------|------------------|
| `freshness` | `"UNKNOWN"` | El documento no declara política de vigencia para provisiones. Las provisiones son obligaciones contingentes cuyo vencimiento depende de eventos futuros no determinados. |

**Nota:** Las provisiones disminuyeron de 18,4M a 17,5M EUR entre 2022 y 2023. La memoria (nota 16) detalla las causas.

### P7-BCN-2026-0005 — Infraestructuras

| Campo | Valor | Motivo del hueco |
|-------|-------|------------------|
| `freshness` | `"UNKNOWN"` | Las infraestructuras son activos no corrientes a coste histórico. No hay política de vigencia declarada; el dato representa el coste acumulado a 31/12/2023, no un valor razonable. |

**Nota:** El dato es coste histórico, no valor razonable. La partida más grande es Vials (carreteras): 3.707M EUR, el 66% del total.

### P7-BCN-2026-0006 — Obligaciones ambientales

| Campo | Valor | Motivo del hueco |
|-------|-------|------------------|
| `freshness` | `"UNKNOWN"` | Obligaciones ambientales reconocidas durante el ejercicio 2023. No se declara política de vigencia; representan compromisos de gasto para políticas ambientales. |

**Nota:** La mayoría (86,2M EUR) corresponde a construcción y mantenimiento de espacios verdes. Son compromisos de gasto, no deuda financiera.

---

## Hallazgos sobre los huecos

### 1. freshness es el hueco recurrente
El patrón es claro: el documento de cuentas anuales **no declara explícitamente** una política de vigencia para sus datos. Esto es esperado en contabilidad pública: las cuentas son un snapshot a una fecha de corte, y la "vigencia" es implícita (hasta la siguiente cuenta general).

**¿Es material?** No para las cifras mismas (todas están establecidas), pero sí para la capacidad de usar las fichas como evidencia actual. Las fichas son conformes al sobre pero sus datos son históricos.

### 2. No hay otros huecos de primer nivel
Las 6 fichas tienen todas las cifras, fechas, fuentes y referencias establecidas. Los únicos huecos son de `freshness`, que es un campo que el contrato permite declarar como UNKNOWN con motivo.

### 3. Los huecos anidados son menores
Solo la ficha 0003 tiene `unknown_detail` (para `freshness.valid_until`). Los demás campos compuestos están completamente establecidos.

---

*Los huecos están declarados con su motivo. Ninguno es un cero disfrazado.*
