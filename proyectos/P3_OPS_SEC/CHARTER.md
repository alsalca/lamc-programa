# CHARTER — P3 `OPS_SEC`

**Estado:** ✅ **PUBLICADO** · **Ola:** 1 · **Coste estimado:** 4–6 días
**Chat responsable:** quien construye el entregable P3 · **Checker:** la revisión independiente · **Aprobado:** 2026-09-21 (D-001)

---

## 1. OBJETIVO

Producir dos documentos que juntos son **la credencial** para entrar a la conversación
del riesgo operacional en DeFi:

1. Un **post-mortem honesto** del incidente de infraestructura propio.
2. Un **estándar de seguridad operacional** para posiciones DeFi — el que las
   aseguradoras dicen que no existe.

**Frase falsifiable:** *un tercero puede auditar su propia operación de DeFi contra
el estándar, ítem por ítem, y cada afirmación del post-mortem cita una fuente cruda.*

---

## 2. POR QUÉ ES EL PROYECTO MÁS DIFÍCIL DE COPIAR

El mercado verificó (2026-09-21):

> *"Muchos de los mayores hackeos se originaron off-chain por fallos de seguridad
> operacional."* — Hugh Karp, fundador de Nexus Mutual
>
> *"Esos escenarios son mucho más difíciles de asegurar porque los equipos a menudo
> carecen de prácticas de seguridad operacional estandarizadas. Sin estándares claros,
> las aseguradoras no pueden tarifar el riesgo de forma fiable."*

**El cuello de botella del mercado de seguros de DeFi no es capital: es la ausencia de
un estándar.** Y un estándar solo lo puede escribir alguien que haya operado de verdad
y haya fallado de verdad.

Este proyecto es la única cosa en el portafolio que **convierte el incidente en activo**
en lugar de en vergüenza.

---

## 3. EVIDENCIA DISPONIBLE

| Fuente | Qué aporta | Ruta |
|---|---|---|
| `LAMC_Incident_Transitional_Policy_v4_2_2.md` | El incidente completo: qué pasó, decisión, reglas nuevas | `_LAMC_EVOLUCION/textos/` |
| `LAMC_Master_Architecture_Document.md` | Política de secretos, `la infraestructura interna`, CORE+EDGE, backups | `_LAMC_EVOLUCION/textos/` |
| `LAMC_BOT_POLICY_IA_INSTRUCTIONS.md` | Las 10 reglas obligatorias de bots, ficha, separación PROD/exp | `_LAMC_EVOLUCION/textos/` |
| `LAMC_CORE_NODE_Resumen_Sesion.md` | La migración, stack implementado | `_LAMC_EVOLUCION/textos/` |
| `LAMC_MASTER_CONSTITUTION_v5.md` | P2 Recovery First, P4 Zero Trust, P8 Producción Intocable | `_LAMC_EVOLUCION/textos/` |

### Hechos ya extraídos (no re-investigar)

**El incidente:** *"corrupción parcial del filesystem EXT4 acompañada de corrupción de
archivos críticos Debian, DNS y sistema de paquetes"*; el equipo *"todavía arrancaba
correctamente y mantenía acceso parcial, pero presentaba degradación runtime severa"*;
el binario `tailscaled` fue hallado corrupto, *"confirmando corrupción filesystem y no un
fallo aislado de Tailscale"*.

**La decisión:** *"EDGE NODE != CORE INFRASTRUCTURE"*; *"NO EXPERIMENTS IN PROD"*;
*"SQLite requiere disciplina operacional: WAL mode, integrity_check y backups automáticos"*;
*"Nueva regla R12 — VSCode Zero-Trust"*; *"El objetivo ya no es evitar fallos, sino
reconstrucción rápida y controlada"*.

**Lo que NO consta:** el día exacto del incidente, y **si hubo pérdida de datos**.
Ambos son `UNKNOWN` y deben declararse como tales.

---

## 4. ENTREGABLE

| # | Artefacto | Descripción |
|---|---|---|
| E-P3-01 | `POSTMORTEM.md` | El incidente: cronología, evidencia forense, decisión, coste, lecciones |
| E-P3-02 | `STANDARD.md` | El estándar de seguridad operacional, con ítems verificables uno por uno |
| E-P3-03 | `CHECKLIST.md` | Versión operativa del estándar, auditable en una sesión |
| E-P3-04 | `EVIDENCIA.md` | Mapa afirmación → fuente cruda, para el post-mortem |

---

## 5. ESTRUCTURA DEL ESTÁNDAR (mínimo)

Cada ítem debe ser **verificable binariamente** (se cumple o no), no aspiracional.

| Área | Ítems mínimos |
|---|---|
| **Custodia de claves** | Hardware wallet, separación de roles, política de firma, recuperación |
| **Multisig** | Umbral, distribución de firmantes, verificación fuera de banda |
| **Secretos** | Nunca en repo, nunca hardcodeados, gestor dedicado, rotación |
| **Backups** | Frecuencia, verificación de restauración, ubicación, cifrado |
| **Base de datos** | WAL mode, `integrity_check` programado, backups automáticos |
| **Observabilidad** | SMART, IO, warnings de EXT4, health checks, alertas |
| **Superficie de ataque** | Superficie mínima, separación PROD/LAB, *"no experiments in prod"* |
| **Recovery** | RTO declarado, procedimiento probado, no solo documentado |
| **Terceros** | Proveedores, permisos, revocación, dependencias |
| **Higiene operativa** | Zero-trust en desarrollo, no scripts desconocidos, allowlists |

**Inspiración directa:** las 10 reglas de `BOT_POLICY` y las políticas SS20 del incidente.
Ya existen; el trabajo es **generalizarlas** de "cómo opero mi Raspberry Pi" a
"cómo debe operarse una posición DeFi".

---

## 6. VALIDACIÓN DETERMINÍSTICA

```bash
cd proyectos/P3_OPS_SEC/entregables

# 1. Cada ítem del estándar es verificable (formato binario)
grep -c "^- \[ \]" STANDARD.md CHECKLIST.md

# 2. El post-mortem cita fuentes
grep -c "LAMC_Incident_Transitional_Policy_v4_2_2\|LAMC_CORE_NODE_Resumen_Sesion\|LAMC_Master_Architecture_Document" POSTMORTEM.md

# 3. Existe declaración explícita de UNKNOWN
grep -ci "UNKNOWN\|NO_CONSTA\|no consta" POSTMORTEM.md

# 4. CERO credenciales en los documentos (CRÍTICO)
grep -riE "(api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_.:-]{12,}" . && echo "!!! FUGA DE CREDENCIAL !!!" || echo "OK sin credenciales"

# 5. El mapa de evidencia cubre todas las afirmaciones
wc -l EVIDENCIA.md
```

**Criterio:** los cinco pasos pasan. **El paso 4 es bloqueante**: si hay una sola
credencial en los documentos, el proyecto es `BLOCK`.

---

## 7. FUERA DE ALCANCE

- ❌ Acusar a terceros o a proveedores por nombre
- ❌ Reproducir valores de credenciales **en ninguna forma, ni parcialmente**
- ❌ Publicar (requiere HG-001 **y** HG-002)
- ❌ Prometer certificación, auditoría o cumplimiento
- ❌ Convertirlo en producto de software

---

## 8. RIESGOS

| ID | Riesgo | Mitigación |
|---|---|---|
| **R-004** | **Exponer credenciales al publicar** | **HG-002 bloqueante.** Paso 4 de validación. Revisión manual del la revisión independiente |
| R-013 | El estándar se vuelve aspiracional y no auditable | Todo ítem en formato `- [ ]` binario; prohibido "considerar" o "evaluar" |
| R-014 | El post-mortem se lee como autocomplacencia | Incluir obligatoriamente lo que se hizo mal (credenciales hardcodeadas, `tabsfix`) |
| R-015 | Atribución de culpa a un tercero | Prohibido por §7 |

---

## 9. MISIONES

| ID | Misión | Salida |
|---|---|---|
| **M-P3-01** | Redactar el post-mortem con mapa de evidencia | `POSTMORTEM.md` + `EVIDENCIA.md` |
| **M-P3-02** | Redactar el estándar y la checklist | `STANDARD.md` + `CHECKLIST.md` |
| **M-P3-03** | Verificar ausencia de credenciales | Salida del paso 4 |
| **M-P3-04** | Reportar y esperar HG-002 | `ESTADO.md` |

**M-P3-03 y HG-002 son precondición de cualquier publicación.**

---

## 10. CRITERIO DE TERMINADO

`PASS` cuando:
1. Cada ítem del estándar es binario y verificable.
2. Cada afirmación del post-mortem cita una fuente cruda.
3. **Cero credenciales** en los entregables (verificado con el paso 4).
4. Los `UNKNOWN` (día exacto del incidente, pérdida de datos) están declarados.

---

## 11. HUMAN GATES

- **HG-002** — rotación de credenciales. **Bloqueante.** Ver `log.md` [2026-09-21] riesgo R-004
- **HG-001** — publicación externa (posterior a HG-002)
