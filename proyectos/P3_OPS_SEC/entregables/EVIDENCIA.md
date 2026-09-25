# MAPA DE EVIDENCIA — Post-Mortem P3_OPS_SEC

**Propósito:** Cada afirmación del post-mortem apunta a una fuente cruda verificable.
**Fecha:** 2026-09-21
**Fuentes del corpus:** `_LAMC_EVOLUCION/textos/`

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
| 15 | "Se encontró API key hardcodeada en finanzas/api.py" | `finanzas/api.py` (corpus crudo) | Verificación directa: línea 10 original tenía `os.environ.get("API_KEY", "valor_hardcodeado")` → REMEDIADO |
| 16 | "Token completo en safefactorbot.md" | `safefactorbot.md` (corpus crudo) | Verificación directa: patrón `8-12 números:30+ caracteres` encontrado 1 vez |

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

---

## 7. NOTAS METODOLÓGICAS

1. **Anonimato:** se eliminaron rutas que contengan `[directorio del operador]/` o identificadores personales. Las rutas en el mapa de evidencia usan la forma `` que es el directorio de trabajo del programa.

2. **Corpus inmutable:** los archivos `finanzas/api.py` y `safefactorbot.md` son parte del corpus crudo y NO fueron modificados por este post-mortem. La remediación de `api.py` se realizó fuera de este documento como acción correctiva separada.

3. **Patrón de verificación de credenciales:** se usó `grep -E "[0-9]{8,12}:[A-Za-z0-9_-]{30,}"` para detectar tokens de Telegram sin exponer valores completos.

4. **UNKNOWN legítimo:** los ítems marcados como UNKNOWN (costes, pérdida de datos, causa raíz) se documentan como "aún no establecido" (axioma A1) y NO se inferirieron por ausencia de evidencia (axioma A3).

---

*Mapa de evidencia generado por quien construye el entregable P3 — cada afirmación es rastreable a su fuente.*
