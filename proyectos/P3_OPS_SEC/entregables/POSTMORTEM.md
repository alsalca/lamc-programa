# POST-MORTEM — Incidente de Infraestructura EXT4

**Fecha del incidente:** UNKNOWN (ocurrido en mayo de 2026, día exacto no registrado)
**Fecha del documento:** 2026-09-21
**Estado:** Post-mortem institucional, pre-publicación (requiere HG-002)

---

## 1. RESUMEN EJECUTIVO

Un nodo edge de infraestructura basado en hardware de bajo consumo experimentó corrupción parcial del filesystem EXT4, afectando archivos críticos del sistema operativo, DNS y sistema de paquetes. El nodo mantuvo funcionalidad parcial de arranque pero con degradación severa de rendimiento. El binario de un servicio de red fue encontrado corrupto, confirmando que la corrupción afectaba al filesystem completo y no era un fallo aislado de un componente específico.

**Coste estimado:** UNKNOWN (no se cuantificó formalmente el impacto operacional)
**Pérdida de datos financieros:** UNKNOWN (no consta si la base de datos de finanzas fue afectada)

---

## 2. CRONOLOGÍA (basada en evidencia documental)

| Fase | Hecho | Fuente |
|------|-------|--------|
| **Pre-incidente** | El nodo edge ejecutaba servicios productivos incluyendo una API financiera, bot de mensajería y base de datos SQLite | `LAMC_MASTER_ARCHITECTURE_v6.md` §3, `LAMC_BOT_POLICY_IA_INSTRUCTIONS.md` |
| **Detección** | Se confirmó corrupción parcial del filesystem EXT4 acompañada de corrupción de archivos críticos Debian, DNS y sistema de paquetes | `LAMC_Incident_Transitional_Policy_v4_2_2.md` SS17 |
| **Diagnóstico** | El binario `tailscaled` fue encontrado corrupto, confirmando corrupción filesystem y no un fallo aislado | `LAMC_Incident_Transitional_Policy_v4_2_2.md` SS17 |
| **Estado observado** | El nodo todavía arrancaba correctamente y mantenía acceso parcial, pero presentaba degradación runtime severa | `LAMC_Incident_Transitional_Policy_v4_2_2.md` SS17 |
| **Decisión** | Se oficializó no continuar desarrollo productivo sobre el nodo actual; el nodo entró en estado STANDBY/OFFLINE | `LAMC_Incident_Transitional_Policy_v4_2_2.md` SS18 |
| **Post-decisión** | Se definieron nuevas políticas operacionales: separación estricta PROD vs LAB, NO EXPERIMENTS IN PROD, disciplina SQLite | `LAMC_Incident_Transitional_Policy_v4_2_2.md` SS20 |

---

## 3. EVIDENCIA FORENSE

### 3.1 Lo que se observó
- **Corrupción filesystem:** archivos críticos del sistema Debian, DNS y sistema de paquetes afectados
- **Binario corrupto:** el servicio de red `tailscaled` contenía datos corrompidos
- **Degradación runtime:** el sistema mantuvo arranque pero con funcionamiento severamente degradado
- **Acceso parcial:** funcionalidad de red limitada pero presente

### 3.2 Lo que NO se observó (UNKNOWN)
- **Causa raíz de la corrupción:** UNKNOWN (no se determinó si fue hardware, software, o externa)
- **Fecha exacta del incidente:** UNKNOWN (solo se conoce que ocurrió en mayo de 2026)
- **Pérdida de datos financieros:** UNKNOWN (no consta si `finanzas.db` o datos de la API financiera fueron afectados)
- **Alcance completo de archivos dañados:** UNKNOWN (no se realizó análisis forense completo documentado)

---

## 4. DECISIÓN TOMADA

La decisión fue **correcta y consistente** con los principios de seguridad:

> **"EDGE NODE != CORE INFRASTRUCTURE"** — `LAMC_Incident_Transitional_Policy_v4_2_2.md` SS19

Se reconoció que:
1. Un nodo edge no debe ser nodo core de producción
2. Los experimentos no deben ejecutarse en producción
3. La infraestructura debe ser reproducible y recuperable

---

## 5. LECCIONES APRENDIDAS

### 5.1 Lo que funcionó
- **Detección:** se identificó la corrupción antes de que causara pérdida total
- **Decisión rápida:** se detuvo la operación productiva en el nodo afectado
- **Documentación:** se creó un documento de transición con políticas claras

### 5.2 Lo que se hizo MAL (hallazgos del post-mortem)

#### ❌ **Secretos hardcodeados en código fuente**
- Se encontró una API key hardcodeada como valor por defecto en el archivo `finanzas/api.py`
- **Ubicación:** línea 10 del archivo original
- **Violación:** la política de LAMC establece que "Los secretos JAMÁS deben quedar: hardcodeados; en GitHub; en documentación pública" (`LAMC_Master_Architecture_Document.md` §6)
- **Estado actual:** REMEDIADO (se eliminó el fallback hardcodeado, ahora requiere variable de entorno)
- **Nota:** el corpus crudo (archivos .bak, .env, scripts de inicio) aún contiene este valor; requiere rotaciónHG-002

#### ❌ **Token de Telegram completo en documentación**
- Se encontró un token completo de Telegram en `safefactorbot.md`
- **Violación:** misma política de secretos de LAMC
- **Estado:** el archivo está en corpus crudo (inmutable); requiere rotación HG-002

#### ❌ **Ausencia de integridad filesystem**
- No existían mecanismos de verificación de integridad del filesystem (como `fsck`, `integrity_check` o monitoreo SMART)
- **Consecuencia:** la corrupción pudo avanzar sin detección hasta alcanzar archivos críticos
- **Política derivada:** SS20 estableció "Observabilidad obligatoria: SMART, IO, EXT4 warnings" (`LAMC_Incident_Transitional_Policy_v4_2_2.md` SS20)

#### ❌ **Mezcla de roles en un solo nodo**
- El mismo hardware ejecutaba funciones core (API financiera, base de datos) y funciones edge
- **Violación:** principio de separación de responsabilidades
- **Política derivada:** SS19 estableció "EDGE NODE != CORE INFRASTRUCTURE"

#### ❌ **Ausencia de verificación de integridad de base de datos**
- No se mencionan controles de integridad para SQLite (WAL mode, integrity_check)
- **Consecuencia:** UNKNOWN si la corrupción afectó la base de datos financiera
- **Política derivada:** SS20 estableció "SQLite requiere disciplina operacional: WAL mode, integrity_check y backups automáticos"

---

## 6. CAMBIOS DERIVADOS (ya implementados)

1. **Nueva arquitectura CORE+EDGE:** separación física de responsabilidades (`LAMC_CORE_NODE_Resumen_Sesion.md`)
2. **Política de secretos:** todos los secretos en `el gestor de secretos` con permisos restringidos (`LAMC_Master_Architecture_Document.md` §6)
3. **Observabilidad obligatoria:** monitoreo de salud filesystem, IO, integridad de base de datos (`LAMC_Incident_Transitional_Policy_v4_2_2.md` SS20)
4. **Zero-trust en desarrollo:** regla R12 — VSCode Zero-Trust (`LAMC_Incident_Transitional_Policy_v4_2_2.md` SS20)
5. **Filosofía de recovery:** "El objetivo ya no es evitar fallos, sino reconstrucción rápida y controlada" (`LAMC_Incident_Transitional_Policy_v4_2_2.md` SS21)

---

## 7. ESTADO ACTUAL

- **Nodo edge original:** OFFLINE / STANDBY
- **Desarrollo productivo:** PAUSADO en el nodo original
- **Migración a nueva infraestructura:** EN PROGRESO (CORE NODE operativo,edge NODE en transición)
- **Observabilidad:** PRIORIDAD CRÍTICA (parcialmente implementada)
- **Supply-chain Security:** PRIORIDAD CRÍTICA (parcialmente implementada)

---

## 8. IMPLICACIONES PARA EL ESTÁNDAR DE SEGURIDAD

Este incidente demuestra que:

1. **La ausencia de controles no significa ausencia de riesgo** (axioma A3)
2. **Un solo punto de fallo puede degradar servicios críticos** sin causar pérdida total
3. **Los secretos en código fuente son un riesgo silencioso** que persiste incluso después del incidente
4. **La recovery-first architecture es esencial** cuando los fallos son inevitables

El estándar derivado de este incidente debe incluir verificables binarios para cada uno de estos controles.

---

*Documento generado por quien construye el entregable P3 como parte del proyecto P3_OPS_SEC del Programa LAMC.*
*Este post-mortem NO es un documento de publicación — requiere HG-002 (rotación de credenciales) y HG-001 (publicación externa).*
