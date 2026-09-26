# MAPA DE EVIDENCIA — Post-Mortem P3_OPS_SEC

**Propósito:** Cada afirmación del post-mortem apunta a una fuente cruda verificable.
**Fecha:** 2026-09-21
**Fuentes del corpus:** `_LAMC_EVOLUCION/textos/` — documentos internos del operador,
**no publicados** (ver la nota sobre fuentes en §6).

---

## 1. AFIRMACIONES SOBRE EL INCIDENTE

| # | Afirmación en POSTMORTEM.md | Fuente cruda | Línea/Sección |
|---|----------------------------|--------------|---------------|
| 1 | "Nodo edge basado en hardware de bajo consumo" | `LAMC_CORE_NODE_Resumen_Sesion.md` | Línea 3: "transición oficial desde una infraestructura basada principalmente en Raspberry Pi" |
| 2 | "Corrupción parcial del filesystem EXT4" | `LAMC_Incident_Transitional_Policy_v4_2_2.md` | SS17, línea 6: "corrupción parcial del filesystem EXT4" |
| 3 | "Archivos críticos Debian, DNS y sistema de paquetes afectados" | `LAMC_Incident_Transitional_Policy_v4_2_2.md` | SS17, línea 6: "corrupción de archivos críticos Debian, DNS y sistema de paquetes" |
| 4 | "Binario tailscaled corrupto" | `LAMC_Incident_Transitional_Policy_v4_2_2.md` | SS17, línea 8: "El binario tailscaled fue encontrado corrupto" |
| 5 | "Degradación runtime severa" | `LAMC_Incident_Transitional_Policy_v4_2_2.md` | SS17, línea 7: "presentaba degradación runtime severa" |
| 6 | "Acceso parcial mantenido" | `LAMC_Incident_Transitional_Policy_v4_2_2.md` | SS17, línea 7: "mantenía acceso parcial" |
| 7 | "Decisión: EDGE NODE != CORE INFRASTRUCTURE" | `LAMC_Incident_Transitional_Policy_v4_2_2.md` | SS19, línea 14 |
| 8 | "NO EXPERIMENTS IN PROD" | `LAMC_Incident_Transitional_Policy_v4_2_2.md` | SS20, línea 19 |
| 9 | "SQLite requiere WAL mode, integrity_check y backups" | `LAMC_Incident_Transitional_Policy_v4_2_2.md` | SS20, línea 20 |
| 10 | "Observabilidad obligatoria: SMART, IO, EXT4 warnings" | `LAMC_Incident_Transitional_Policy_v4_2_2.md` | SS20, línea 21 |
| 11 | "R12 — VSCode Zero-Trust" | `LAMC_Incident_Transitional_Policy_v4_2_2.md` | SS20, línea 23 |
| 12 | "Recovery first: reconstrucción rápida y controlada" | `LAMC_Incident_Transitional_Policy_v4_2_2.md` | SS21, línea 25 |

---

## 2. AFIRMACIONES SOBRE SECRETOS Y VIOLACIONES

| # | Afirmación en POSTMORTEM.md | Fuente cruda | Verificación |
|---|----------------------------|--------------|--------------|
| 13 | "Política: secretos JAMÁS hardcodeados" | `LAMC_Master_Architecture_Document.md` | §6, líneas 115-119: "Los secretos JAMÁS deben quedar: hardcodeados; en GitHub; en documentación pública" |
| 14 | "Secretos deben vivir en el gestor de secretos" | `LAMC_Master_Architecture_Document.md` | §6, líneas 120-121 |
| 15 | "Se encontró API key hardcodeada en finanzas/api.py" | `finanzas/api.py` (corpus interno) | **Reproducible en parte; el detalle de la «línea 10 original» es `UNKNOWN`.** Verificado 2026-09-25: `finanzas/api.py` línea 10 contiene hoy `API_KEY = os.environ.get("API_KEY")`, sin fallback. El corpus conserva un valor literal hardcodeado en `finanzas/api.py.bak` L6, `finanzas/api_FUNCIONANDO.py` L6, `finanzas/start.sh` L5, `filesfinanzaspersonales/start.sh` L5 y dos `.pyc`. El estado **original** de `finanzas/api.py` no está en el corpus: no se puede comprobar qué decía su línea 10 → `UNKNOWN`. El patrón *fallback con valor por defecto* en línea 10 está en `filesfinanzaspersonales/api.py` (archivo distinto del citado). |
| 16 | "Token completo de Telegram en `safefactorbot.md`" (real y comprometido) | `safefactorbot.md` + historial del repositorio del corpus (registro interno, **no publicado**) | **Existencia ESTABLECIDA; valor no reproducido.** El patrón de token de Telegram `[0-9]{8,12}:[A-Za-z0-9_-]{30,}` aparece en **2 commits** del historial del corpus (`f1d3841`, 2026-09-23, lo introduce; `1dadccd`, 2026-09-24, lo retira), sobre `_LAMC_EVOLUCION/textos/safefactorbot.md`. El registro interno (no publicado, 2026-09-23) documenta que el token era real y que seguía en todos los commits. En el árbol de trabajo actual el archivo solo tiene los marcadores `CAMBIA_ESTE_TOKEN` y `CAMBIA_ESTE_CHAT_ID` (patrón → 0), lo que no elimina el valor del historial. **`UNKNOWN`: el inventario actual completo de dónde sigue vivo el valor** — localización, no existencia. La rotación sigue **pendiente**: es una acción del operador. |

> **CORRECCIÓN 2026-09-25:** la fila 15 afirmaba algo que no resistía la comprobación contra
> la fuente citada: que `finanzas/api.py` «línea 10 original» tenía un fallback hardcodeado.
> Verificado contra el corpus, no es reproducible (el estado original del archivo no está) y
> se degrada a `UNKNOWN` con el motivo, en vez de dejarla en pie.
>
> **CORRECCIÓN 2026-09-26:** la fila 16 degradaba el token de Telegram a `UNKNOWN` y **lo
> sacaba del alcance de rotación**. El registro interno (el registro interno (no publicado), 2026-09-23) documenta
> que el token era **real** y que **seguía en todos los commits**; el patrón reaparece en el
> historial del corpus. La existencia queda establecida y el `UNKNOWN` se reubica en la
> **localización actual** del valor. La rotación permanece en la rotación de credenciales **pendiente**.

---

## 3. AFIRMACIONES SOBRE ARQUITECTURA Y DECISIONES

| # | Afirmación en POSTMORTEM.md | Fuente cruda | Línea/Sección |
|---|----------------------------|--------------|---------------|
| 17 | "Separación estricta PROD vs LAB" | `LAMC_Incident_Transitional_Policy_v4_2_2.md` | SS20, línea 18 |
| 18 | "Migración a CORE NODE (un mini PC)" | `LAMC_CORE_NODE_Resumen_Sesion.md` | Línea 11: "Mini PC un mini PC convertido en LAMC CORE NODE" |
| 19 | "EDGE NODE relegado a funciones secundarias" | `LAMC_Incident_Transitional_Policy_v4_2_2.md` | SS19, línea 16: "La Raspberry quedará relegada a funciones edge/lightweight" |
| 20 | "Estructura la infraestructura interna con secretos dedicados" | `LAMC_CORE_NODE_Resumen_Sesion.md` | Líneas 32-41: listado de estructura incluyendo `el gestor de secretos` |
| 21 | "Docker Compose para contenedorización" | `LAMC_Master_Architecture_Document.md` | §7, líneas 130-137 |
| 22 | "Uptime Kuma para observabilidad" | `LAMC_CORE_NODE_Resumen_Sesion.md` | Línea 20: "Uptime Kuma desplegado correctamente" |

---

## 4. AFIRMACIONES SOBRE PRINCIPIOS Y GOBERNANZA

| # | Afirmación en POSTMORTEM.md | Fuente cruda | Línea/Sección |
|---|----------------------------|--------------|---------------|
| 23 | "Principio Recovery First" | `LAMC_MASTER_CONSTITUTION_v5.md` | P2, línea 17 |
| 24 | "Principio Zero Trust" | `LAMC_MASTER_CONSTITUTION_v5.md` | P4, línea 19 |
| 25 | "Principio Producción Intocable" | `LAMC_MASTER_CONSTITUTION_v5.md` | P8, línea 23 |
| 26 | "10 reglas obligatorias de bots" | `LAMC_BOT_POLICY_IA_INSTRUCTIONS.md` | Líneas 17-26: "REGLAS OBLIGATORIAS" |
| 27 | "Un bot = un propósito = un servicio systemd" | `LAMC_BOT_POLICY_IA_INSTRUCTIONS.md` | Línea 5 |
| 28 | "Tokens en directorio dedicado" | `LAMC_BOT_POLICY_IA_INSTRUCTIONS.md` | Línea 19: "Todo token vive en [ruta del gestor de secretos]" |

---

## 5. AFIRMACIONES SOBRE COSTES E IMPACTO

| # | Afirmación en POSTMORTEM.md | Fuente cruda | Notas |
|---|----------------------------|--------------|-------|
| 29 | "Coste estimado: UNKNOWN" | N/A | **No existe fuente de cuantificación de costes en el corpus** |
| 30 | "Pérdida de datos financieros: UNKNOWN" | N/A | **No existe documentación que confirme o niegue pérdida de finanzas.db** |
| 31 | "Causa raíz de corrupción: UNKNOWN" | N/A | **El documento de transición no especifica la causa, solo describe los efectos** |

---

## 6. FUENTES CONSULTADAS (catálogo)

| Archivo | Ruta completa | Contenido relevante |
|---------|---------------|---------------------|
| Incident Policy v4.2.2 | `_LAMC_EVOLUCION/textos/LAMC_Incident_Transitional_Policy_v4_2_2.md` | Hechos del incidente, decisiones, políticas derivadas |
| Master Architecture Doc | `_LAMC_EVOLUCION/textos/LAMC_Master_Architecture_Document.md` | Política de secretos, estructura, contenedorización |
| Bot Policy | `_LAMC_EVOLUCION/textos/LAMC_BOT_POLICY_IA_INSTRUCTIONS.md` | 10 reglas de bots, ficha obligatoria |
| Core Node Session | `_LAMC_EVOLUCION/textos/LAMC_CORE_NODE_Resumen_Sesion.md` | Migración, stack implementado |
| Master Constitution v5 | `_LAMC_EVOLUCION/textos/LAMC_MASTER_CONSTITUTION_v5.md` | Principios P2, P4, P8 |
| Charter P3 | `proyectos/P3_OPS_SEC/CHARTER.md` | Encargo del proyecto, hechos extraídos |

> **NOTA SOBRE LAS FUENTES 2026-09-25:** los cinco documentos de `_LAMC_EVOLUCION/textos/`
> (y los archivos del corpus `finanzas/` y `safefactorbot.md`) son **documentos internos
> del operador y NO se publican** en este paquete. Se citan por su nombre y su ruta interna
> porque son la fuente real del post-mortem, pero **un verificador externo no puede
> abrirlos ni comprobarlos**: ese tramo del mapa de evidencia es `UNKNOWN` para un tercero.
> Se conservan las citas —son la trazabilidad— y se declara su límite en vez de esconderlo.

---

## 7. NOTAS METODOLÓGICAS

1. **Anonimato:** se eliminaron rutas que contengan `[directorio del operador]/` o identificadores personales. Las rutas en el mapa de evidencia usan la forma `(ruta interna omitida)`, que es el directorio de trabajo del programa.

2. **Corpus inmutable:** los archivos `finanzas/api.py` y `safefactorbot.md` son parte del corpus crudo y NO fueron modificados por este post-mortem. La remediación de `api.py` se realizó fuera de este documento como acción correctiva separada.

3. **Patrón de verificación de credenciales:** se usó `grep -cE "[0-9]{8,12}:[A-Za-z0-9_-]{30,}"` para detectar tokens de Telegram sin exponer valores completos. Sobre el `safefactorbot.md` **actual** ese patrón devuelve 0 (árbol de trabajo ya limpio, 2026-09-25); sobre el **historial** del corpus identifica **2 commits** que contienen el valor (2026-09-24). La fila 16 **no** queda como «no reproducible»: queda como token **real y comprometido**, con la **localización actual del valor** en `UNKNOWN`.

4. **UNKNOWN legítimo:** los ítems marcados como UNKNOWN (costes, pérdida de datos, causa raíz, estado original de `finanzas/api.py`, **localización actual del token de Telegram —no su existencia—**) se documentan como "aún no establecido" (axioma A1) y NO se inferirieron por ausencia de evidencia (axioma A3).

> **CORRECCIÓN 2026-09-25:** en la nota 1 había quedado una ruta como comillas invertidas
> vacías (dos backticks sin contenido). Se ha escrito `(ruta interna omitida)` en su lugar.
> En §6 se declara, además, que los documentos internos citados no son verificables por un
> tercero.

---

*Mapa de evidencia generado por el equipo del proyecto P3 — cada afirmación es rastreable
a su fuente — revisado 2026-09-25.*
