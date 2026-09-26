# INFORME — ORS v1.0.0 aplicado a los 3 protocolos de P4

**Proyecto:** N8_ORS · **Nivel:** N8 · Programa LAMC  
**Fecha:** 2026-09-25 · **Autoría:** quien construye el entregable · **Verificación:** independiente  
**Estado:** reproducibilidad **verificada de forma independiente el 2026-09-26** · **pendiente de la firma del operador**.

---

## 1. QUÉ SE HIZO

Se diseñó un modelo de puntuación (**ORS v1.0.0**, `entregables/MODELO.md`) que traduce
el benchmark de 52 controles de P4 a una puntuación comparable de **cobertura
verificada de controles**, y se aplicó a los tres protocolos medidos por P4 (Aave,
Uniswap, Liquity V1).

> **El ORS no es una nota de seguridad.** No dice que ningún protocolo sea «seguro» ni
> «más seguro». Solo dice qué parte de los controles del estándar P3 están
> **verificados como presentes** en fuentes públicas, y cuánto queda sin observar.

---

## 2. RESULTADO

| Protocolo | **ORS** (suelo verificado) | Techo | **CE** (completitud) | presente | ausente | unknown | no aplica |
|---|---:|---:|---:|---:|---:|---:|---:|
| Aave | **9.62** | 98.08 | 11.54 | 5 | 1 | 46 | 0 |
| Uniswap | **7.69** | 100.00 | 7.69 | 4 | 0 | 48 | 0 |
| Liquity (V1) | **11.36** | 100.00 | 11.36 | 5 | 0 | 39 | 8 |

- **ORS** = `100 × presente / aplicables` (peso uniforme por control; `unknown` no se puntúa).
- **Techo** = valor si todo lo no observado estuviera presente.
- **CE** = `100 × (presente + ausente) / aplicables` — qué parte del estándar se pudo observar.

### 2.1 Cómo se lee

Cada protocolo tiene un **intervalo**, no un número: `[ORS, techo]`.

| Protocolo | Intervalo | Lectura |
|---|---|---|
| Aave | [9.62, 98.08] | Se pudo observar **poco más del 11 % del estándar**. El 9,62 describe **cuánto se pudo verificar**, no cuánto hay: el techo llega a 98,08 |
| Uniswap | [7.69, 100.00] | **La medición más incompleta de las tres** (menos del 8 %). Su suelo es el más bajo **porque se pudo ver menos**, no porque falte más |
| Liquity (V1) | [11.36, 100.00] | Se pudo observar **poco más del 11 %**, sobre un denominador menor (44 controles aplicables en vez de 52). No es «mejor»: es **distinto** |

> **Ninguno de esos tres números dice que un protocolo tenga pocos controles.** Dicen **cuánto se
> pudo observar desde fuentes públicas**, que es otra cosa. Un número bajo aquí mide, sobre todo,
> **lo poco que se puede ver desde fuera** — no es un juicio sobre quien está dentro.

**El hallazgo principal no es la puntuación, es el ancho del intervalo.** Con `CE`
en torno al 10 %, el ORS es un **suelo**, no una estimación. La comparación es válida
como orden de cobertura verificada; **no** como juicio de riesgo.

### 2.2 Orden (y su límite)

Orden por ORS: **Liquity (11.36) > Aave (9.62) > Uniswap (7.69)**.

- La diferencia Aave − Uniswap (1.92 pp) es **exactamente un control** (§2.1: multisig
  presente en Aave, `unknown` en Uniswap). Es una diferencia real y atribuible, no
  ruido: el modelo es determinístico.
- La diferencia Liquity − Aave se debe sobre todo a que Liquity tiene **44 controles
  aplicables** (8 `no_aplica`), no a más cobertura verificada.
- **No** hay base para decir que el orden implique seguridad relativa.

---

## 3. POR QUÉ EL MODELO NO ES ARBITRARIO

`ORS_WEIGHTING` figuraba como `UNKNOWN` en el Plan Maestro y «ORS arbitrario» es una
prohibición explícita. La v1.0.0 lo aborda así:

1. **Sin constantes ajustables.** Peso uniforme (`1` por control). No hay porcentajes
   que calibrar ni que justificar.
2. **`unknown` no recibe valor** (ni 0 ni 0.5). Se publica como eje aparte (`CE`) y
   como cota (`techo`). Esto respeta A1 (`UNKNOWN ≠ 0`), A3 (la ausencia de evidencia
   no es evidencia) y A2 (completitud ≠ riesgo).
3. **Invariancia.** Bajo una segunda regla no arbitraria (peso igual por sección) el
   orden se mantiene: `Liquity > Aave > Uniswap` (9.02 / 7.10 / 10.65).
4. **Determinismo.** Misma entrada ⇒ misma salida. Cualquier diferencia es atribuible
   a controles concretos (§2.2 y `bundle/evidence.md` §5).

---

## 4. QUÉ **NO** MIDE EL ORS (declaración exigida por el charter)

El ORS **no** mide, y este informe **no** afirma:

- ❌ **Seguridad** del protocolo. No es una nota de seguridad. Un ORS alto no implica
  «seguro»; un ORS bajo no implica «inseguro».
- ❌ **Riesgo de smart contracts**: bugs, exploits, lógica económica, gobernanza.
- ❌ **Riesgo de mercado**: volatilidad, liquidez, calidad del colateral.
- ❌ **Riesgo regulatorio** ni de contraparte.
- ❌ **Calidad** de los controles: solo registra su **presencia**, no su eficacia.
- ❌ **Ausencia** de controles no observados: `unknown` **no** es `ausente`.
- ❌ **Comparaciones fuera de P4**: solo los 3 protocolos medidos con el mismo
  estándar y la misma fecha.

---

## 5. LÍMITES Y RIESGOS

| ID | Límite / riesgo | Estado |
|---|---|---|
| L1 | **Resolución baja**: `CE` ≈ 10 %; el ancho del intervalo domina la puntuación | Declarado |
| L2 | **P4 solo marca 5–6 controles por protocolo** en Aave/Uniswap | Declarado |
| L3 | **`no_aplica` favorece arquitecturas inmutables** (Liquity) al reducir el denominador | Declarado (MODELO §12.4) |
| L4 | **Calidad no evaluada**: un control presente puede ser ineficaz | Declarado |
| L5 | **Temporalidad**: foto al 2026-09-25, no se actualiza sola | Declarado |
| R-021 | **Percepción de arbitrariedad** | Mitigado: sin constantes + invariancia + determinismo |

---

## 6. ESTADO Y SIGUIENTE PASO

- **Entregables:** `MODELO.md`, `bundle/puntuaciones.json`, `bundle/evidence.md`,
  `INFORME.md` (todos candidatos).
- **Validación determinística:** `validar_evidencia.py` → **APROBADO** (6 fichas,
  2 autoridades).
- **Pendiente:** la **firma del operador** antes de publicar.
- **No se publica nada** y **no se modifica** el contrato de P1 ni ningún dato de P4.

---

## 7. CRITERIO DE TERMINADO (charter §7)

| # | Criterio | Estado |
|---|---|---|
| 1 | Modelo documentado y reproducible | ✅ `MODELO.md` §5 y §10 |
| 2 | Puntuaciones basadas en datos de P4 | ✅ `bundle/evidence.md` §1–§3 |
| 3 | Informe declara lo que el ORS **no** mide | ✅ §4 de este informe |

---

*Informe de quien construye el entregable — 2026-09-25. La certificación la hace la
verificación independiente. **Nada se publica sin la firma del operador.***
