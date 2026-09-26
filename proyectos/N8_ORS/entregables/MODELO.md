# MODELO ORS — Operational Risk Score

**Versión:** 1.0.0  
**Fecha:** 2026-09-25  
**Proyecto:** N8_ORS · **Nivel:** N8 · Programa LAMC  
**Autoría:** quien construye el entregable · **Verificación:** independiente (ajena a la autoría)  
**Estado:** versión 1.0.0 · **reproducibilidad verificada de forma independiente el 2026-09-26** (un tercero sin contexto reprodujo los seis valores desde los datos publicados) · **pendiente de la firma del operador** para publicarse.

---

## 0. REGLA BLOQUEANTE (leer antes que nada)

> ⛔ **El ORS no es una nota de seguridad y no dice si un protocolo es «seguro».**
> Mide **una sola cosa**: qué parte de los controles del estándar de P3 están
> **verificados como presentes** en las mediciones públicas de P4.
> Un ORS alto **no** significa que un protocolo sea seguro; solo significa que una
> parte mayor de los controles observados está presente. Un ORS bajo **no** significa
> que sea inseguro; puede significar que casi nada es observable.

> ⛔ **Fuente única:** los datos de entrada son exclusivamente
> `proyectos/P4_CAPA_CONTROLES/entregables/bundle/mediciones.json` y su evidencia
> (`bundle/evidence.md`). No se añade ningún criterio, control ni fuente nueva.

> ⛔ **Sin datos personales.** Los sujetos son protocolos (entidades públicas).

---

## 1. QUÉ MIDE Y QUÉ NO MIDE

### 1.1 Qué mide

- **Cobertura verificada de controles**: proporción de controles *aplicables* del
  estándar P3 que P4 verificó como `presente`.
- **Incertidumbre declarada**: proporción de controles que P4 no pudo observar
  (`unknown`), publicada como eje separado — nunca fundida en la puntuación.
- **Diferencias atribuibles**: cada diferencia entre dos puntuaciones se puede
  descomponer en controles concretos (§8).

### 1.2 Qué NO mide

- ❌ **Seguridad** del protocolo. No es una nota de seguridad.
- ❌ **Riesgo de smart contracts** (bugs, exploits, lógica económica).
- ❌ **Riesgo de mercado** (volatilidad, liquidez, colateral).
- ❌ **Riesgo regulatorio** ni de contraparte.
- ❌ **Calidad** de un control: solo registra si está **presente**, no si es eficaz.
- ❌ **Riesgo agregado del portafolio** del operador.
- ❌ **Ausencia** de un control no observado: `unknown` no es `ausente` (axioma A1/A3).

---

## 2. FUENTE ÚNICA DE DATOS

```
proyectos/P4_CAPA_CONTROLES/entregables/BENCHMARK.md            ← el detalle control a control
proyectos/P4_CAPA_CONTROLES/entregables/bundle/mediciones.json  ← el conteo agregado por protocolo
proyectos/P4_CAPA_CONTROLES/entregables/bundle/evidence.md      ← las fuentes de cada veredicto
```

El ORS **no vuelve a medir**. Toma los conteos de P4 y los traduce a una puntuación.
La reproducción de la puntuación está garantizada por la aritmética del §5.

> **CORRECCIÓN 2026-09-26 (verificación independiente).** Aquí decía que bastaba
> `mediciones.json`. **Es falso, y lo destapó un tercero que intentó reproducir el modelo sin
> conocer el proyecto:** ese archivo contiene **tres fichas con metadatos**, y su única cifra
> es `quantity` = 5 / 4 / 5 —el número de controles `presente`, que **no está declarado como
> tal en ninguna parte**—. **Los estados control a control no están ahí.** Están en
> `BENCHMARK.md` (la matriz de 52 controles × 3 protocolos) y, con sus fuentes, en
> `evidence.md`. Quien siga este modelo tiene que empezar por la matriz, no por el JSON.
> La puntuación sí se reproduce desde `BENCHMARK.md` sin ambigüedad (ver §10).

---

## 3. UNIDAD DE MEDIDA Y APLICABILIDAD

- **Unidad:** un control del estándar P3 (`proyectos/P3_OPS_SEC/entregables/STANDARD.md`).
- **Total:** 52 controles en 10 secciones (§1–§10).
- **Aplicabilidad:** un control marcado `no_aplica` en P4 (p. ej. custodia y multisig
  en un protocolo inmutable y governance-free, como Liquity) **se excluye** del
  cálculo. Su peso se reparte proporcionalmente entre las secciones que sí aplican (§5.4).

---

## 4. PUNTUACIÓN DE CADA CONTROL

| Estado en P4 | Valor para la puntuación | Significado |
|---|---|---|
| `presente` | **1** | Verificado como presente |
| `ausente` | **0** | Verificado como ausente |
| `unknown` | **sin valor** | No observado. **No se puntúa.** El modelo publica un intervalo (§6) |
| `no_aplica` | **excluido** | No relevante para la arquitectura del protocolo |

**Nota dura (A1/A3):** `unknown` **no** recibe 0, ni 0.5, ni ningún otro valor. No se
le asigna crédito ni penalización. Se publica su proporción como eje aparte
(`CE`, §7) y el máximo alcanzable como `techo` (§6.2). Esto evita dos errores
simétricos: tratar lo no observado como presente (inventar cobertura) o como
ausente (afirmar por ausencia).

---

## 5. FÓRMULA Y PESOS

### 5.1 Puntuación de una sección

Para la sección *i*, con `P_i` controles `presente` y `A_i` controles **aplicables**
(total de la sección menos los `no_aplica`):

```
score_i = P_i / A_i          (0 ≤ score_i ≤ 1)
```

### 5.2 Peso de cada control: uniforme

```
peso de todo control = 1
```

**Por qué uniforme y no ponderado por sección.** P4 no contiene ninguna base para
decir que un control importa más que otro. Ponderar sin esa base sería un juicio de
valor **arbitrario** — exactamente lo que el programa prohíbe («ORS arbitrario») y el
riesgo R-021 («el score se percibe como arbitrario»). Con
peso uniforme, la puntuación es la proporción directa de controles aplicables
verificados como presentes. **No hay constantes que ajustar.**

### 5.3 Puntuación ORS (suelo verificado)

```
ORS = 100 × ( Σ P_i sobre secciones aplicables )
            ───────────────────────────────────
            ( Σ A_i sobre secciones aplicables )
```

Equivalente a `100 × controles_presente / controles_aplicables`.

- **Rango:** 0–100. **Mínimo** 0 (ningún control verificado presente).
- **Máximo** 100 (todos los controles aplicables verificados presentes).

### 5.4 Secciones sin controles aplicables, y controles no aplicables dentro de una sección

Dos casos distintos, y conviene no confundirlos:

1. **Sección entera en `no_aplica`** (p. ej. §1 y §2 en Liquity): se **excluye**, y su peso
   se reparte proporcionalmente entre las secciones aplicables. Con peso uniforme ocurre de
   forma natural: el denominador solo suma `A_i` de secciones con al menos un control aplicable.
2. **Algún control `no_aplica` dentro de una sección aplicable:** el control **sale del
   denominador de esa sección**, es decir `A_i` = tamaño de la sección − controles `no_aplica`
   de esa sección (lo que ya implica el §5.1). El resto de la sección se puntúa igual.

> **Precisión añadida el 2026-09-26 (verificación independiente).** El caso 2 no estaba
> escrito. Hoy no se ejercita —todos los `no_aplica` de esta medición son secciones
> completas— pero un lector tenía que deducirlo, y **una regla que hay que deducir es una
> regla que dos lectores pueden deducir distinto.**

---

## 6. MANEJO DE `UNKNOWN`: UN INTERVALO, NO UN VALOR

### 6.1 Suelo (la puntuación publicada)

`ORS` (§5.3) es el **suelo**: solo acredita lo verificado como presente.

### 6.2 Techo (máximo alcanzable)

```
techo = 100 × (porcentaje de controles aplicables que NO son ausentes)
      = 100 × (P + U) / A
```

donde `U` = controles `unknown`. Es el valor que tendría la puntuación **si todo lo
no observado estuviera presente**. No es una predicción: es una cota.

### 6.3 Lectura

La puntuación de un protocolo es el intervalo **[suelo, techo]**. Un intervalo
estrecho indica medición completa; un intervalo ancho, medición incompleta. El
modelo **no elige un punto medio**: elegirlo sería inventar (§4).

---

## 7. EJES SECUNDARIOS (no forman parte del ORS)

| Eje | Fórmula | Qué declara |
|---|---|---|
| **CE** — Completitud de evidencia | `100 × (P + A) / aplicables` | Qué parte del estándar se pudo observar (presente o ausente) |
| **Techo** | `100 × (P + U) / aplicables` | Cota superior del ORS |
| **Cobertura verificada** | `ORS` | Cota inferior del ORS |

**Axioma A2 (`EVIDENCE COMPLETENESS ≠ RISK`):** `CE` **no** se mezcla con el ORS. Un
protocolo con poca evidencia no es «más riesgoso» por eso; simplemente está menos
medido. Publicarlos juntos y separados es lo que impide confundir las dos cosas.

---

## 8. SALIDA DEL MODELO

Para cada protocolo se publica:

1. **ORS** (suelo verificado) — la puntuación comparable.
2. **Techo** — cota superior.
3. **CE** — completitud de la evidencia.
4. **Desglose por sección** — `P_i`, `A_i`, `score_i`.
5. **Diferencia atribuible** frente a otro protocolo — qué control concreto la produce.

### 8.1 Interpretación (exposición operacional, no seguridad)

| Rango del ORS (suelo) | Lectura |
|---|---|
| 0–20 | Cobertura verificada muy baja |
| 21–40 | Cobertura verificada baja |
| 41–60 | Cobertura verificada media |
| 61–80 | Cobertura verificada alta |
| 81–100 | Cobertura verificada muy alta |

> ⚠️ Estos rangos describen **cobertura verificada**, no seguridad. Con `CE` bajo, el
> rango es poco informativo: léase siempre junto al techo y a `CE`.

---

## 9. SENSIBILIDAD E INVARIANCIA DE PESOS

Para demostrar que el resultado **no depende de una ponderación arbitraria**, se
recalcula el suelo con una segunda regla no arbitraria: **peso igual por sección**
(cada sección aplicable pesa `1/nº de secciones aplicables`, y dentro de la sección
`score_i = P_i / A_i`).

**`n` = número de secciones aplicables**, es decir, las que tienen **al menos un control
aplicable**. Las secciones enteras en `no_aplica` **no cuentan en `n`** (§5.4, caso 1).

| Protocolo | ORS (peso uniforme, primario) | ORS (peso igual por sección) |
|---|---:|---:|
| Aave | 9.62 | 9.02 |
| Uniswap | 7.69 | 7.10 |
| Liquity (V1) | 11.36 | 10.65 |

**El orden es el mismo** bajo las dos reglas: `Liquity > Aave > Uniswap`. La
conclusión cualitativa es invariante a la ponderación; los valores absolutos difieren
poco. Si dos reglas no arbitrarias dieren órdenes distintos, habría que declararlo
como límite de resolución del modelo.

> **Precisión y límite declarado (2026-09-26, verificación independiente).** El valor de
> `n` **no estaba escrito**, y un tercero tuvo que decidirlo: es exactamente el tipo de
> hueco que dos lectores razonables resuelven distinto. Queda escrito arriba. Y se declara
> el efecto de la lectura alternativa, para que nadie tenga que descubrirlo: contando las
> **diez** secciones y dando 0 a las dos excluidas, **Liquity daría 8.52 en vez de 10.65**;
> Aave (9.02) y Uniswap (7.10) no cambian, porque no tienen secciones excluidas. **El orden
> se mantiene en las dos lecturas**, así que la conclusión no depende de esta elección —
> pero el número absoluto de Liquity sí, y por eso queda dicho.

---

## 10. REPRODUCIBILIDAD

Un tercero reproduce cada puntuación así:

1. Lee **la matriz de 52 controles × 3 protocolos** de `BENCHMARK.md` —ahí está el estado de
   cada control, con la marca `✅`/`❌`/`?`/`➖`— y, si quiere las fuentes, `bundle/evidence.md`.
2. Cuenta los controles `presente` y los `aplicables` (52 menos `no_aplica`).
3. Aplica `ORS = 100 × presente / aplicables` y los ejes del §7.
4. Compara con `bundle/puntuaciones.json` (ficha con `instrument.symbol = "ORS_PUNTOS"`:
   ese archivo lleva **dos fichas por protocolo** —la puntuación y el conteo de presentes—
   y hay que elegir la correcta por el símbolo, no por el nombre del sujeto).
5. Opcional, y es la prueba más fuerte: recalcula con la segunda regla del §9 y comprueba que
   **el orden no cambia**.

El desglose por sección y por control está en `bundle/evidence.md`, de modo que la
aritmética se puede repetir a mano.

> **Verificación independiente ejecutada el 2026-09-26, antes de publicar.** Un tercero
> **sin contexto** —al que solo se le dio este MODELO y los datos de P4, con prohibición
> expresa de abrir `puntuaciones.json`— reprodujo **los seis valores** (9,62 / 7,69 / 11,36 y
> 9,02 / 7,10 / 10,65) y el mismo orden, desde la definición y nada más. Esa verificación
> encontró las tres cosas que este documento corrige: la fuente equivocada en el §2, el valor
> de `n` sin definir en el §9 y el caso del `no_aplica` parcial en el §5.4. **La prueba
> automática que lo repite está en `proyectos/N8_ORS/prueba_reproducibilidad.py`.**

---

## 11. ATRIBUCIÓN DE AUTORIDAD (por qué cada ficha lleva la que lleva)

Cada puntuación viaja dentro del sobre de evidencia de P1. La autoridad se asigna con
una regla explícita:

- Las **puntuaciones** ORS son un cálculo nuestro a partir de otras evidencias ⇒
  `authority = DERIVED`.
- Las **fichas de insumo** que transcriben la medición de P4 conservan la autoridad
  que P4 asignó a esa medición (`PUBLIC_CHAIN` para Aave y Uniswap; `DERIVED` para
  Liquity), porque transcribir no cambia quién responde (criterio del propio sobre P1).

El bundle contiene ambas: la puntuación **y** el insumo del que deriva, para que la
cadena de procedencia —y la partición de autoridades— sea visible y verificable.

---

## 12. LÍMITES EXPLÍCITOS DEL MODELO

1. **Resolución.** Con `CE` ≈ 10 %, el ORS discrimina poco: casi todo el estándar es
   `unknown` en P4. La puntuación es un **suelo**, no una estimación del riesgo.
2. **Cobertura.** Solo cubre los 52 controles de P3. No cubre bugs, mercado,
   regulación ni contraparte.
3. **Calidad.** Un control `presente` puede ser ineficaz; el modelo no lo evalúa.
4. **Aplicabilidad.** Excluir `no_aplica` favorece a arquitecturas que no necesitan
   ciertos controles (p. ej. inmutabilidad). Es deliberado y se declara; no es una
   ventaja de seguridad.
5. **Temporalidad.** Foto de P4 al 2026-09-25. No se actualiza sola.
6. **Comparabilidad.** Solo válido entre protocolos medidos con el mismo estándar y
   la misma fecha (los tres de P4).
7. **Pesos.** Uniformes por decisión; existe una regla alternativa no arbitraria con
   el mismo orden (§9).

---

## 13. REFERENCIAS

- `proyectos/P3_OPS_SEC/entregables/STANDARD.md` — estándar de 52 controles.
- `proyectos/P4_CAPA_CONTROLES/entregables/bundle/mediciones.json` — datos de entrada.
- `proyectos/P4_CAPA_CONTROLES/entregables/bundle/evidence.md` — evidencia por control.
- Los axiomas del programa (A1 `UNKNOWN ≠ 0`, A2 `completitud ≠ riesgo`, A3 la ausencia de
  evidencia no es evidencia) y la prohibición de un «ORS arbitrario».
- El peso del modelo figuraba como **no establecido** en el plan del programa; esta
  v1.0.0 **lo fija y lo declara** (§5.2).

---

*Modelo diseñado por quien construye el entregable — 2026-09-25. La verificación la hace
alguien distinto de quien lo construye. **La decisión de publicarlo es del operador.***
