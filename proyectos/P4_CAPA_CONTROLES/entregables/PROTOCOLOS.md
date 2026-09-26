# SELECCIÓN DE PROTOCOLOS — M-P4-01

**Proyecto:** P4_CAPA_CONTROLES · **Misión:** M-P4-01 · **Fecha:** 2026-09-25
**Estado:** ✅ **SUPERADO — la medición se hizo.** Resultados en `BENCHMARK.md`
(52 controles × 3 protocolos) e `INFORME.md`. *(Esta línea decía «EN ESPERA DE HG-009 ·
No se ha medido nada todavía» el 2026-09-25. HG-009 se resolvió y M-P4-02 se ejecutó.
La corrección se deja visible a propósito: un estado que no se actualiza no es un
documento histórico, es una afirmación falsa.)*

---

## PROPÓSITO

Seleccionar **3 protocolos con acceso público** para aplicar el estándar de P3
(`proyectos/P3_OPS_SEC/entregables/STANDARD.md`, 52 ítems en 10 áreas). El criterio
de selección es **exclusivamente la accesibilidad pública de la evidencia**: que un
tercero independiente pueda verificar cada ítem desde fuentes públicas, o declararlo
`UNKNOWN` con motivo (axiomas A1/A3, charter §4).

> **Esta tabla NO afirma que un protocolo sea «con controles verificables» que otro.** Solo documenta
> qué superficie pública de evidencia existe para medir cuáles de los 52 controles. La
> interpretación de «presente / ausente / no observable» es del lector.

---

## CRITERIOS DE SELECCIÓN (fijados por CHARTER §3 y §4)

| Criterio | Exigencia |
|---|---|
| C1 — Muestra real | Protocolos DeFi reales, no hipotéticos |
| C2 — Acceso público | Un tercero puede inspeccionar código, contratos, gobernanza y documentación pública |
| C3 — Verificable o `UNKNOWN` | Cada ítem del estándar termina en `presente` / `ausente` / `UNKNOWN` con motivo; nunca se infiere por ausencia (A3) |
| C4 — Sin datos personales | Ningún sujeto identificable |
| C5 — Sin ranking de seguridad | El benchmark no ordena protocolos por «seguridad» |

---

## MUESTRA SELECCIONADA

| # | Protocolo | Rol en la muestra | Gobernanza pública | Código fuente | Contratos on-chain | Observabilidad misma de los 10 áreas* |
|---|---|---|---|---|---|---|
| P-A | **Aave** | Lending descentralizado, DAO de largo recorrido | DAO con ejecutor on-chain y multisig Gnosis Safe (`aave-dao/aave-permissions-book` en GitHub) | Abierto en GitHub | Públicos, configurables (oráculos, parámetros, permisos) | §1, §2, §6, §7, §9 parcialmente observables; §1, §3, §4, §5, §8, §10 mayormente privados |
| P-B | **Uniswap** | Exchange descentralizado, DAO con timelock | Uniswap Governance con Timelock; referencia técnica pública | Abierto en GitHub | Públicos, algunos parámetros bajo gobernanza | §1, §2, §6, §7, §9 parcialmente observables; resto privado |
| P-C | **Liquity (V1)** | Protocolo **inmutable / governance-free**: sin claves de propietario ni actualizaciones | Sin gobernanza (no hay llaves que custodiar ni multisig de DAO) | Abierto en GitHub | Públicos e inmutables | §1 y §2 estructuralmente NO APLICAN; §3, §4, §5, §8, §10 mayormente privados |

\* Las áreas se numeran como en `STANDARD.md`: §1 Custodia de claves · §2 Multisig · §3 Secretos ·
§4 Backups · §5 Base de datos · §6 Observabilidad · §7 Superficie de ataque · §8 Recovery ·
§9 Terceros · §10 Higiene operacional.

---

## POR QUÉ ESTA MUESTRA (justificación de acceso, no de seguridad)

1. **Cobertura del estándar completo.** Los tres exponen públicamente el mismo conjunto
   de artefactos observables: repositorio de código, contratos desplegados, gobernanza y
   documentación. Un tercero puede aplicar el mismo protocolo de medición a los tres.

2. **Diversidad de postura de gobernanza — útil para el benchmark, no para ranking.**
   Aave y Uniswap tienen DAO con firmas/multisig observables; Liquity (V1) es inmutable y
   sin claves. Esto hace que algunos ítems del estándar **no apliquen estructuralmente** en
   Liquity (p. ej. §1 y §2), y ese contraste se registra tal cual, sin valorarlo.

3. **Todos los protocolos tienen repositorio y contratos públicos**, de modo que los ítems
   verificables desde fuente pública (secretos en repositorio §3.1/§3.5, superficies de red
   de frontends/APIs públicas §7, dependencias de terceros §9) se pueden comprobar; el resto
   se declara `UNKNOWN` con su motivo.

---

## OBSERVABILIDAD ESPERADA POR ÁREA — **PLAN** (el plan se ejecutó; los resultados están en `BENCHMARK.md`)

> **CORRECCIÓN 2026-09-25 (auditoría independiente, hallazgo 9).** Este título decía
> «ESTO SE MEDIRÁ, **AÚN NO SE HA MEDIDO**». Era falso: la medición se hizo (M-P4-02) y sus
> resultados están en `BENCHMARK.md` y en `bundle/mediciones.json`. **La tabla de abajo sí es
> un plan** y por eso se conserva tal cual: los huecos `[ ? ]` son lo que se esperaba medir,
> no lo que se midió. Lo que se corrige es solo la afirmación de estado, no el contenido.

> Adelanto metodológico: muchas de las 10 áreas miden **operaciones internas** (custodia
> física de la clave de administración, backups, WAL de la base de datos, retención de
> logs). Para un tercero sin acceso interno, esos ítems serán **`UNKNOWN` legítimo** en los
> tres protocolos (axioma A3). El benchmark comunica exactamente eso: qué se puede verificar
> públicamente y qué no. No es un vacío de rigor; es el límite honesto del acceso público.
> **Se cumplió:** de los 52 ítems por protocolo, la mayoría quedó en `UNKNOWN` con motivo, y
> el informe lo declara como el límite del acceso público, no como un resultado.


```
ÁREA                      Aave     Uniswap   Liquity(V1)
§1 Custodia de claves     [ ? ]    [ ? ]     NO APLICA (inmutable)
§2 Multisig               [ ? ]    [ ? ]     NO APLICA (inmutable)
§3 Secretos               [ ? ]    [ ? ]     [ ? ]   ← se verifica en repositorios
§4 Backups                [ ? ]    [ ? ]     [ ? ]   ← interno → UNKNOWN por defecto
§5 Base de datos          [ ? ]    [ ? ]     [ ? ]   ← interno → UNKNOWN por defecto
§6 Observabilidad         [ ? ]    [ ? ]     [ ? ]   ← parcialmente pública (APIs)
§7 Superficie de ataque   [ ? ]    [ ? ]     [ ? ]   ← parcialmente pública
§8 Recovery               [ ? ]    [ ? ]     [ ? ]   ← interno → UNKNOWN por defecto
§9 Terceros               [ ? ]    [ ? ]     [ ? ]   ← parcialmente pública
§10 Higiene operacional   [ ? ]    [ ? ]     [ ? ]   ← parcialmente pública
```

Los `[ ? ]` son huecos **que se midieron en M-P4-02**. Esta tabla es **el plan**, no el
benchmark: los resultados están en `BENCHMARK.md`. Se conserva sin rellenar a propósito —
una tabla de plan rellenada con resultados deja de ser un plan y pasa a ser un informe
duplicado que puede desviarse del bueno.

---

## HISTORIA DEL GATE — HG-009

Según `CHARTER.md` §9, la aprobación de los 3 protocolos es el Human Gate **HG-009**, filtro
de la verificación independiente. La medición (M-P4-02) no se inició hasta recibir esa aprobación.

> **CORRECCIÓN 2026-09-25 (revisión del verificador independiente):** esta sección decía «EN ESPERA — HG-009»
> con los dos gates `⏸️`. Ya no era cierto: **HG-009 se resolvió** y **HG-001 también**
> (P1, P2 y P3 están publicados en `github.com/alsalca/lamc-programa`). Se conserva el
> registro con el estado real.

| Gate | Estado real | Qué pasó |
|---|---|---|
| **HG-009** | ✅ RESUELTO | La verificación independiente aprobó la muestra (fitness técnico, autoridad delegada); M-P4-02 se ejecutó |
| HG-001 | ✅ RESUELTO | Publicación externa ejecutada — ver `publicacion/PAQUETE/` |

---

*Tabla de selección generada por quien construye el entregable — M-P4-01. El filtro HG-009 se resolvió y
esta tabla se usó como base de M-P4-02; los resultados están en `BENCHMARK.md`.*