# RAZONAMIENTO — P4_CAPA_CONTROLES

**Fecha:** 2026-09-25
**Proyecto:** P4_CAPA_CONTROLES · **Misión M-P4-04**

Este documento registra **cómo se decidió cada marcación** para que un tercero pueda repetir
la medición (criterio de terminado del charter §8.3–8.4). Es el razonamiento, no la evidencia
(eso está en `evidence.md`) ni los huecos (`unknowns.md`).

---

## 1. Diseño del benchmark (decisión de método)

1. **El estándar es binario** (se cumple / no se cumple) según P3. A este benchmark se le añade
   un tercer estado `?` (UNKNOWN) y un cuarto `➖` (no aplica), porque el estándar fue escrito
   para que lo aplique quien **opera** la posición, mientras este benchmark lo aplica un
   **tercero desde fuentes públicas** (charter §4: "Solo datos observables").

2. **Escala de 4 valores:**
   - `✓` presente — hay evidencia **pública** de que el control se cumple.
   - `✗` ausente — hay evidencia **pública** de que el control no se cumple.
   - `?` UNKNOWN — no observable desde fuentes públicas en esta medición (A1/A3).
   - `➖` no aplica — el control no aplica a la estructura del protocolo.

3. **La escala no ordena.** Un protocolo con menos `✓` no es "menos seguro": hay `✓` que
   significan "sin secretos en el repo" y «✓» que significan "teoría bajo timelock"; no son
   comparables entre sí y ningún agregado se interpreta como ranking.

4. **Un `✗` no es "el protocolo es inseguro".** Es el resultado de un solo ítem binario contra
   una fuente pública concreta (p. ej. §9.4 = proveedor único). La interpretación la hace el
   lector.

---

## 2. Criterio de marcación de los ítems de SECRETOS (§3.1, §10.7)

En `evidence.md` se fijó la definición reproducible: el control cuenta como presente si no hay
**secreto de producción / alto valor** en HEAD. Esto respeta el texto del estándar ("secreto de
producción" en §3.1) y evita que ids de cliente `NEXT_PUBLIC_*` o claves de licencia
commiteadas por diseño —que por arquitectura no son secretos— marquen un falso `✗`. Todas las
excepciones se declaran en `unknowns.md` §3. **Es la única decisión interpretativa del método,
y se hace explícita para que el revisor pueda cambiarla y reproducir el resultado.**

---

## 3. Razonamiento de casos individuales

### §2.1 (multisig 2-de-3)
- **Aave → ✓.** El foro de gobernanza documenta públicamente SAFEs de tesorería 2-of-3 y un
  "Community Guardian" 5-of-9; la Safe on-chain está indexada en Etherscan. Es el caso donde el
  esquema exigido por el estándar se observa directamente.
- **Uniswap → ?** La tesorería está bajo **timelock gobernado por voto on-chain de la DAO**
  (quórum de holders), NO bajo un multisig 2-de-3 con firmantes. El mecanismo observado difiere
  del que el estándar pide. Marcar `✓` sería atribuir un control que no se ha observado con ese
  esquema; marcar `✗` requeriría confirmar que no existe ningún multisig (no confirmable).
  Por eso: `UNKNOWN`, con la estructura documentada.
- **Liquity → ➖.** No hay llaves ni DAO multisig; son contratos inmutables sin propietario.

### §9.4 (sin dependencia de un único proveedor)
- **Aave → ✗.** Evidencia pública de que el oráculo de precio es Chainlink como fuente única y
  que el fallback está desactivado (address(0)) según propuesta #351 y hilo BGD. Un único
  proveedor crítico observable → no se cumple el control.
- **Uniswap → ✓.** Documentación pública de múltiples proveedores (oráculos Api3/Pyth/RedStone
  /Chainlink; RPC Alchemy/Infura/QuickNode/…; indexadores The Graph/Goldsky/…). No hay un único
  proveedor crítico documentado.
- **Liquity → ✓.** Estructura observable: Chainlink primario + Tellor fallback (dos oráculos).
  Se reporta la estructura, sin juicio de robustez.

### §6.1 (sistema de monitoreo público)
- Los tres publican una superficie externa verificable: subgraph/API (Aave), status page
  pública (Uniswap), subgraph + estado on-chain (Liquity) → `✓`.

### §10.3 (gestión de dependencias)
- **Aave → ✓**, **Liquity → ✓** (Dependabot visible en el repo).
- **Uniswap → ✗** por falta de configuración de automatización commiteda a HEAD (aunque
  Dependabot pueda estar activo via ajustes de org; eso no es públicamente verificable).

---

## 4. Por qué es honesto (no autocomplaciente)

- **No se promueve `UNKNOWN` a `✓`.** Los 46/47 ítems internos por protocolo quedan `?` con su
  motivo (A3). Si esto "parece poco favorable", es porque mide el **límite del acceso público**,
  no porque los protocolos no tengan controles.
- **Se declaran las limitaciones del grep** (Aave 34/153 repos, Uniswap rate-limit, Liquity
  monorepo) y los **hallazgos de transparencia** (claves `NEXT_PUBLIC_*`, `.nx/key.ini`,
  walletConnectProjectId). No se esconde nada que un escáner pudiera disparar.
- **No se inventa ninguna cifra ni secreto.** No se reproducen valores completos de claves: solo
  se cita la URL y se describe la naturaleza (UUID/32-hex client-public), con `unknown_reason`.
- **No se afirma "con controles verificables"** en ningún punto del benchmark.

---

## 5. Repetibilidad (criterio del charter §8.4)

Un tercero puede:
1. Abrir `BENCHMARK.md` (resultados ítem a ítem).
2. Abrir `evidence.md` (fuente URL por marcación).
3. Abrir `unknowns.md` (motivo de todo `?` y todo hallazgo).
4. Aplicar la escala 4-valores y la convención §3.1/§10.7 y **obtener el mismo resultado, ítem
   por ítem**, dentro del alcance del grep declarado.

La principal fuente de variación entre dos auditores será (a) el alcance del grep de secretos
y (b) la tolerancia sobre claves cliente-públicas; ambas están **declaradas** para que el
resultado sea reproducible con la misma interpretación.

---

*Razonamiento documentado por quien construye el entregable — 2026-09-25. La certificación la hace la verificación independiente.*