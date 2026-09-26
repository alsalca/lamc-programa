# INFORME — P4_CAPA_CONTROLES · Benchmark de seguridad operacional

**Fecha:** 2026-09-25
**Proyecto:** P4_CAPA_CONTROLES · **Nivel:** N7 (el ORS es N8, no se construye aquí)
**Autoría:** quien construye el entregable · **Estado:** entrega lista para verificación independiente

---

## 1. QUÉ ES ESTO

Un **benchmark de seguridad operacional** que aplica el estándar de P3
(`proyectos/P3_OPS_SEC/entregables/STANDARD.md`, 52 ítems en 10 áreas) a **3 protocolos reales**
desde **acceso público**: qué controles tienen evidencia pública de estar presentes (`✓`) o
ausentes (`✗`), cuáles no se pueden observar (`?` = UNKNOWN) y cuáles no aplican (`➖`).

> **El benchmark NO afirma que un protocolo sea «con controles verificables» que otro.** Solo comunica qué
> controles son verificables públicamente. La interpretación es del lector. (Regla bloqueante
> del charter.)

---

## 2. RESULTADOS (resumen)

| Protocolo | ✅ presente | ❌ ausente | ? UNKNOWN | ➖ no aplica | Total |
|---|---:|---:|---:|---:|---:|
| Aave | 5 | 1 | 46 | 0 | 52 |
| Uniswap | 4 | 0 | 48 | 0 | 52 |
| Liquity (V1) | 5 | 0 | 39 | 8 | 52 |

Los `✓` corresponden a: §2.1 esquema de gobernanza/tesorería (§2.1 on-chain), §3.1 sin secretos
de producción en el repo, §6.1 superficie de monitorización pública, §10.3 gestión de
dependencias y §10.7 sin credenciales hardcodeadas. Los `✗`: Aave §9.4 (proveedor único de
precio, Chainlink con fallback desactivado) y Uniswap §10.3 (sin config de dependencias a HEAD).
Detalle completo en `BENCHMARK.md`.

---

## 3. POR QUÉ HAY TANTOS UNKNOWN (y por qué es correcto)

Los ítems `?` son en su mayoría **operación interna** de la entidad que opera cada protocolo
(custodia física de claves, backups, base de datos, retención de logs, RTO, drills, separación
PROD/LAB). Un tercero sin acceso interno **no puede verificarlos desde fuentes públicas**. Por
axioma A3, eso **no** es un `✓` implícito ni un fallo: es el **límite honesto del benchmark
público**. Un auditor con acceso interno los resolvería. Ver `unknowns.md` §1.

---

## 4. CASOS PARTICULARES RELEVANTES

- **Uniswap §2.1 = `?`:** la tesorería está bajo **timelock gobernado por voto on-chain de la
  DAO**, un mecanismo distinto del multisig 2-de-3 que exige el estándar. No se marca presente
  ni ausente; se documenta la estructura.
- **Liquity §1 y §2 = `➖`:** protocolo inmutable y governance-free (sin llaves, contrato
  `renounceOwnership` on-chain, no-proxy); custodia y multisig no aplican estructuralmente.
- **Aave §9.4 = `✗`:** evidencia pública de un único proveedor de precio (Chainlink), fallback
  desactivado.

---

## 5. LIMITACIONES DECLARADAS

1. **Alcance del grep de secretos:** Aave (34/153 repos inspeccionados), Uniswap (barrido de
   archivos de alto valor; rate-limit en docs/interface), Liquity (monorepo `dev`). No se
   garantiza un barrido byte-a-byte total. Ver `unknowns.md` §4.
2. **Tolerancia sobre literales:** se fijó una convención (§3.1/§10.7 = "sin secreto de
   producción"). Claves cliente-públicas (`NEXT_PUBLIC_*`, walletConnectProjectId, `.nx/key.ini`)
   se documentan como hallazgo pero no marcan `✗`. Un revisor con otra tolerancia obtendría un
   resultado distinto en esos ítems. Ver `evidence.md` (convención) y `unknowns.md` §3.
3. **La medición es un snapshot al 2026-09-25.** Repositorios, gobernanza y servicios públicos
   cambian con el tiempo; la frescura se declara en cada ficha.
4. **Sin acceso interno:** la mayoría de los controles operacionales quedan `?` por diseño.

---

## 6. VALIDACIÓN DETERMINÍSTICA

```bash
python3 herramientas/validar_evidencia.py proyectos/P4_CAPA_CONTROLES
```

Resultado: **RESULTADO: APROBADO — todo lo aplicable pasa.**

- [1] Esquema: los 22 campos obligatorios, 11 listas cerradas.
- [2] Ejemplos: 3 fichas correctas en `mediciones.json`.
- [3] Número de fichas: 3 — **cumple el mínimo de 3** que declara el charter
  (`CHARTER.md` §4 y §6.2: «al menos 3 protocolos»).
- [4] Autoridades: 2 distintas (PUBLIC_CHAIN, DERIVED) — **no exigido**: este proyecto no
  declara mínimo de autoridades, así que el validador lo informa, no lo aprueba.

> **CORRECCIÓN 2026-09-25 (auditoría independiente, hallazgos 7 y 21).** Esta lista decía
> «los **3** bloques pasan» —el validador tiene 4— y presentaba [3] y [4] como mínimos
> **cumplidos** («el charter exige ≥3»), cuando la herramienta imprime **«no exigido»** en
> [4]. La distinción no es un tecnicismo: es lo que impide que «no se le pedía» se lea como
> «lo cumple». Aquí se copia la salida real.

---

## 7. ENTREGABLES EN ESTA ENTREGA (M-P4-02 a M-P4-04)

| Artefacto | Ruta |
|---|---|
| E-P4-01 `BENCHMARK.md` | `entregables/BENCHMARK.md` |
| E-P4-02 `bundle/mediciones.json` | `entregables/bundle/mediciones.json` |
| E-P4-03 `bundle/evidence.md` | `entregables/bundle/evidence.md` |
| E-P4-04 `bundle/unknowns.md` | `entregables/bundle/unknowns.md` |
| E-P4-05 `bundle/reasoning.md` | `entregables/bundle/reasoning.md` |
| E-P4-06 `INFORME.md` | `entregables/INFORME.md` |

La selección de la muestra quedó registrada en `entregables/PROTOCOLOS.md` (M-P4-01).

---

## 8. FUERA DE ALCANCE (confirmado)

- ❌ **No se construye el ORS** (operational risk score): es N8, no N7.
- ❌ No se auditan protocolos ni se emiten opiniones de seguridad.
- ❌ No se acusa a ningún protocolo.
- ❌ No hay datos personales ni se reproducen valores de credenciales.
- ❌ No se publica nada externamente (requiere HG-001).

---

## 9. CERTIFICACIÓN

Este trabajo está listo para revisión por el **verificación independiente**. **Yo NO marco
PASS.** La certificación la hace el checker, verificando reproducibilidad y conformidad (charter
§8).

---

*Informe generado por quien construye el entregable — 2026-09-25.*