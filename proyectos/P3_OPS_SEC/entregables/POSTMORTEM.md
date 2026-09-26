# POST-MORTEM — Incidente de Infraestructura EXT4

**Fecha del incidente:** UNKNOWN (ocurrido en mayo de 2026, día exacto no registrado)
**Fecha del documento:** 2026-09-21
**Estado:** Post-mortem técnico, pre-publicación. Para un lector externo, sus fuentes son
documentos internos no publicados y **no puede comprobarlas** (ver §2). La rotación de las
credenciales comprometidas sigue pendiente y **no consta** que se haya hecho.

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

> **NOTA SOBRE LAS FUENTES 2026-09-25:** los documentos citados en esta tabla
> (`LAMC_*`) y los archivos del corpus son **documentos internos del operador y NO se
> publican** en este paquete. Se citan porque son la fuente real de cada afirmación, pero
> **un verificador externo no puede abrirlos ni comprobarlos**: ese tramo del mapa de
> evidencia es `UNKNOWN` para un tercero. Se conservan las citas —son la trazabilidad del
> post-mortem— y se declara el límite en vez de esconderlo.

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
- Se encontró una API key hardcodeada en el sistema de finanzas.
- **Ubicación verificada (2026-09-25):** un valor literal hardcodeado en `finanzas/api.py.bak` (línea 6), `finanzas/api_FUNCIONANDO.py` (línea 6), `finanzas/start.sh` (línea 5), `filesfinanzaspersonales/start.sh` (línea 5) y dos archivos `.pyc`. `finanzas/api.py` (línea 10) ya está en forma remediada, sin fallback.
- **`UNKNOWN`:** qué contenía la «línea 10 original» de `finanzas/api.py`. El estado original del archivo no está en el corpus y no puede comprobarse.
- **Violación:** la política de LAMC establece que "Los secretos JAMÁS deben quedar: hardcodeados; en GitHub; en documentación pública" (`LAMC_Master_Architecture_Document.md` §6)
- **Estado actual:** REMEDIADO en `finanzas/api.py` (lee `os.environ.get("API_KEY")` y falla si no está definida).
- **Nota:** el corpus crudo (copias `.bak`, scripts de inicio, bytecode) aún contiene ese valor; requiere la rotación de la credencial antes de publicar. **No consta** que se haya hecho.

#### ❌ **Token de Telegram real, comprometido en el corpus**
- Se encontró un token completo de Telegram en `safefactorbot.md` y el valor **quedó en el
  historial del repositorio del corpus**, no solo en el árbol de trabajo.
- **Existencia — establecida (comprobación 2026-09-26, sin reproducir el valor):** el patrón
  de token de Telegram `[0-9]{8,12}:[A-Za-z0-9_-]{30,}` aparece en **2 commits** del
  repositorio del corpus —`f1d3841` (2026-09-23), que lo introduce, y `1dadccd` (2026-09-24),
  que lo retira— sobre `_LAMC_EVOLUCION/textos/safefactorbot.md`. El **registro interno del
  programa** —documento interno, **no publicado**, entradas del 2026-09-23— documenta que el
  token era **real** y que **seguía en todos los commits**. No se reproduce su valor.
  *(El registro interno no forma parte de lo que se publica: para un verificador externo, ese
  tramo es `UNKNOWN`. Lo que sí puede comprobar cualquiera es el historial: los dos commits
  citados arriba están nombrados con su identificador.)*
- **Árbol de trabajo — limpio (2026-09-25):** el archivo actual solo contiene los marcadores
  `CAMBIA_ESTE_TOKEN` y `CAMBIA_ESTE_CHAT_ID`; el mismo patrón devuelve **0** sobre el archivo
  de hoy. Que el valor ya no esté ahí **no lo elimina del historial ni de las demás copias**.
- **`UNKNOWN`:** el **inventario actual completo de dónde sigue vivo el valor** (historial,
  respaldos, cachés). El `UNKNOWN` es de **localización**, **no de existencia**: el token era
  real y quedó comprometido.
- **Violación:** la política de LAMC establece que "Los secretos JAMÁS deben quedar:
  hardcodeados; en GitHub; en documentación pública" (`LAMC_Master_Architecture_Document.md` §6).
- **Estado:** la rotación de este token **sigue siendo obligatoria** y forma parte de la rotación de credenciales **pendiente**
  (registro interno, **no publicado**: el riesgo de rotación aplazada y la autorización pendiente del operador). **No consta** que se haya
  rotado. Retirarlo del alcance de rotación sería A3 al revés: «no lo encontré» → «no hace
  falta».

> **CORRECCIÓN 2026-09-26:** esta sección degradaba el token a `UNKNOWN` y **lo sacaba del
> alcance de rotación** —«no hay token que rotar»— porque el `grep` del archivo citado daba
> 0. El error no estaba en el `grep`, sino en la conclusión: el registro interno del programa
> documenta que el token era real y que seguía en todos los commits, y el patrón reaparece en
> el historial del corpus. El `0` del archivo solo prueba que el árbol de trabajo ya no lo
> tiene. Se restituye el token al alcance de rotación (rotación de credenciales **pendiente**, autorización del operador) y el `UNKNOWN` se reubica en la
> **localización actual** del valor. Igualmente, la ubicación «línea 10 del archivo original»
> de la API key se corrige arriba: lo verificable son las seis copias del corpus, no el estado
> original.

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
- **Migración a nueva infraestructura:** EN PROGRESO (CORE NODE operativo, edge NODE en transición)
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

*Documento generado por el equipo del proyecto P3_OPS_SEC — revisado 2026-09-25.*

**Límites de este documento para un lector externo:** el post-mortem cita documentos
internos del operador que **no se publican**; un verificador externo no puede abrirlos y,
por tanto, ese tramo de la evidencia es `UNKNOWN` para él. Además, la rotación de las
credenciales comprometidas **no consta como realizada** y sigue siendo condición previa a
cualquier publicación. Este documento no certifica su propia publicación ni la rotación.

> **CORRECCIÓN 2026-09-25:** la nota final decía que este post-mortem «NO es un documento
> de publicación» y que «requiere» dos autorizaciones internas numeradas. Se reescribe para
> que diga la verdad del documento —qué límites tiene para un lector externo— sin invocar
> autorizaciones internas, y **sin afirmar que la autorización se haya dado**: no consta.
