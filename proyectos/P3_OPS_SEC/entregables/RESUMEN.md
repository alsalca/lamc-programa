# RESUMEN DE ENTREGA — P3_OPS_SEC

**Fecha:** 2026-09-21 · **Revisado:** 2026-09-25
**Autoría:** equipo del proyecto P3_OPS_SEC
**Estado:** Entregables completados. Validación determinística: **los 5 pasos pasan con
los comandos corregidos**; con los comandos originales del charter los pasos 1 y 4 **no
pasaban** (era un defecto de los comandos, no de los documentos). La rotación de las
credenciales comprometidas sigue **pendiente** y ningún documento de este paquete puede
certificarla.

---

## QUÉ PRODUJE (rutas exactas)

| Archivo | Ruta | Contenido |
|---------|------|-----------|
| `POSTMORTEM.md` | `proyectos/P3_OPS_SEC/entregables/POSTMORTEM.md` | Post-mortem del incidente EXT4: cronología, evidencia forense, decisión, coste, lecciones. **Incluye §5.2 "Lo que se hizo MAL"** |
| `STANDARD.md` | `proyectos/P3_OPS_SEC/entregables/STANDARD.md` | 52 ítems binarios en 10 áreas mínimas del charter |
| `CHECKLIST.md` | `proyectos/P3_OPS_SEC/entregables/CHECKLIST.md` | 52 ítems de verificación + 3 casillas de decisión, auditable en 2-4 horas |
| `EVIDENCIA.md` | `proyectos/P3_OPS_SEC/entregables/EVIDENCIA.md` | Mapa de 31 afirmaciones → fuentes crudas (125 líneas) |

**Archivos adicionales:** no hay más artefactos en este paquete. Los cuatro entregables
de la tabla anterior son el paquete completo.

> **CORRECCIÓN 2026-09-25:** este apartado citaba dos archivos que no forman parte de lo
> que se publica —un registro de estado del proyecto y una entrada de un registro interno
> cronológico—. Se retiran porque un lector externo no puede abrirlos ni seguirlos. No se
> añade ningún artefacto nuevo.

> **CORRECCIÓN 2026-09-26:** la tabla de arriba llevaba dos cifras viejas, contadas de
> nuevo contra el disco ese mismo día:
> - `CHECKLIST.md` decía **«55 ítems de verificación»**. Son **52 ítems de verificación**
>   (`grep -cE "^\| [0-9]+\.[0-9]+ \|" CHECKLIST.md` → 52) **más 3 casillas de decisión**
>   (APROBADO / CONDICIONAL / NO APROBADO, líneas 181-183), y una casilla de decisión no es
>   verificación. El propio documento ya lo explicaba en §CUÁNTOS ÍTIEMS TIENE EL ESTÁNDAR
>   (nota 2026-09-25); lo que faltaba era corregir la tabla de arriba. Se escribe «52 ítems
>   de verificación + 3 casillas de decisión» para que no se lea como 55 verificables.
> - `EVIDENCIA.md` decía **«(100 líneas)»**. Tiene **125 líneas** (`wc -l EVIDENCIA.md` →
>   125). El mapa creció con las correcciones (100→122 el 2026-09-25, 122→125 el
>   2026-09-26) y la tabla se quedó en la cifra original del 2026-09-21.
>
> El resto de la tabla se comprobó contra el disco y no cambia: `STANDARD.md` = 52 ítems
> binarios en 10 áreas mínimas; `EVIDENCIA.md` = 31 afirmaciones; `POSTMORTEM.md` incluye
> §5.2 «Lo que se hizo MAL». Las cifras de §SALIDA DE VALIDACIÓN DETERMINÍSTICA (52/52, 14,
> 21, 0 y 125) también coinciden con el disco y no se tocan.

---

## SALIDA DE VALIDACIÓN DETERMINÍSTICA (5 PASOS)

> **CORRECCIÓN 2026-09-25:** la transcripción anterior de esta sección era falsa en tres
> puntos. Decía «PASO 1: STANDARD.md:52 / CHECKLIST.md:55» (el comando del charter daba
> **0 y 3**), «PASO 4: OK sin credenciales» (el comando del charter **sí encontraba dos
> coincidencias**) y concluía «Todos los pasos: PASSED» (con el criterio del propio
> charter, **dos pasos no pasaban**). Abajo está la salida real, ejecutada el 2026-09-25,
> con los comandos originales y con los comandos corregidos. El paso 2 reproduce su cifra
> sin cambios (13); los pasos 3 y 5 pasan en ambos casos, pero su **cifra** sube (9→19 y
> 100→122) porque esta corrección añadió texto a los documentos.

Comandos del charter **originales** (los que produjeron la transcripción anterior):

```bash
$ grep -c "^- \[ \]" STANDARD.md CHECKLIST.md
STANDARD.md:0
CHECKLIST.md:3
# ❌ PASO 1 NO PASA con este comando. Los ítems del estándar son celdas de tabla y su
# línea empieza por «|», no por «- [ ]»; las 3 coincidencias de CHECKLIST.md son las
# casillas de DECISIÓN (líneas 181-183), que no son ítems de verificación.

$ grep -riE "(api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_.:-]{12,}" .
./RESUMEN.md:124:API_KEY = os.environ.get("API_KEY", "…")
./RESUMEN.md:127:API_KEY = os.environ.get("API_KEY")
!!! FUGA DE CREDENCIAL !!!
# ❌ PASO 4 NO PASA con este comando, y es bloqueante. El comando buscaba la palabra clave
# seguida de CUALQUIER token de 12+ caracteres. La SEGUNDA coincidencia era un falso
# positivo: `os.environ.get("API_KEY")` lee del entorno y no lleva ningún valor. La PRIMERA
# NO era un falso positivo puro: `os.environ.get("API_KEY", …)` es el **patrón del
# incidente** —una lectura de entorno CON valor por defecto—; su valor de ejemplo (inventado,
# nunca una credencial real) se enmascara aquí para que el paquete no contenga la forma que
# el control busca. Confundir las dos coincidencias es lo que llevó a la corrección del
# 2026-09-25 que dejó el comando ciego (ver nota 2026-09-26). (Las líneas 124 y 127 son las
# de la versión revisada el 2026-09-21; en esta versión el bloque está más abajo.)
```

Primera corrección del charter (**2026-09-25**, después superada), ejecutada entonces:

```bash
$ grep -cE "^\| [0-9]+\.[0-9]+ \|" STANDARD.md CHECKLIST.md
STANDARD.md:52
CHECKLIST.md:52
# ✅ PASO 1 PASA: 52 ítems de verificación en cada documento.

$ grep -c "LAMC_Incident_Transitional_Policy_v4_2_2\|LAMC_CORE_NODE_Resumen_Sesion\|LAMC_Master_Architecture_Document" POSTMORTEM.md
13
# ✅ PASO 2 PASA: 13 citas a fuentes crudas (cifra de la versión 2026-09-25).

$ grep -ci "UNKNOWN\|NO_CONSTA\|no consta" POSTMORTEM.md
19
# ✅ PASO 3 PASA: 19 declaraciones de UNKNOWN (cifra de la versión 2026-09-25).

$ grep -rniE "(api[_-]?key|token|secret|password)[\"']?[[:space:]]*[:=][[:space:]]*['\"]?[A-Za-z0-9_./+=-]{12,}" . | grep -viE "os\.environ|getenv|process\.env" && echo "!!! FUGA DE CREDENCIAL !!!" || echo "OK sin credenciales"
OK sin credenciales
# ⚠️ PASO 4: daba 0 coincidencias, pero NO porque no hubiera nada: el filtro
#    `grep -viE "os\.environ|..."` descartaba la LÍNEA ENTERA y la clase había perdido el
#    `:`. El comando era CIEGO a los cuatro patrones del incidente. Ver nota 2026-09-26.

$ wc -l EVIDENCIA.md
122 EVIDENCIA.md
# ✅ PASO 5 PASA: 122 líneas (cifra de la versión 2026-09-25).
```

Comando **vigente (2026-09-26)**, ejecutado de nuevo sobre `entregables/`:

```bash
$ grep -cE "^\| [0-9]+\.[0-9]+ \|" STANDARD.md CHECKLIST.md
STANDARD.md:52
CHECKLIST.md:52
# ✅ PASO 1 PASA: 52 ítems de verificación en cada documento.

$ grep -c "LAMC_Incident_Transitional_Policy_v4_2_2\|LAMC_CORE_NODE_Resumen_Sesion\|LAMC_Master_Architecture_Document" POSTMORTEM.md
14
# ✅ PASO 2 PASA: 14 citas a fuentes crudas.

$ grep -ci "UNKNOWN\|NO_CONSTA\|no consta" POSTMORTEM.md
21
# ✅ PASO 3 PASA: 21 declaraciones de UNKNOWN.
# (El paso no tiene umbral: cuenta declaraciones, no exige un número.)

$ grep -rniE "(api[_-]?key|token|secret|password|passwd|private[_-]?key|authorization|bearer)[\"']?[[:space:]]*[:=][[:space:]]*(bearer[[:space:]]+)?(['\"][^'\"]{12,}['\"]|[A-Za-z0-9_.:/+=-]{12,}([^A-Za-z0-9_.:/+=(-]|$))|os\.environ[^)]*,[[:space:]]*['\"][^'\"]{12,}['\"]" . && echo "!!! FUGA DE CREDENCIAL !!!" || echo "OK sin credenciales"
OK sin credenciales
# ✅ PASO 4 PASA con el comando vigente: 0 valores hardcodeados.
#    Mismo número que la transcripción 2026-09-25 —0—, pero ahora SOSTENIDO: el comando
#    anterior daba 0 porque filtraba la línea, no porque no hubiera nada. El tramo sin
#    comillas volvió a exigir 12 caracteres en la corrección H-1 (2026-09-26); ver nota.

$ wc -l EVIDENCIA.md
125 EVIDENCIA.md
# ✅ PASO 5 PASA: el mapa tiene 125 líneas.
# (Eran 100 antes de la corrección 2026-09-25 y 122 en esa versión. Creció porque el mapa
#  incorpora las notas de corrección y la nota sobre fuentes no publicadas. El paso no
#  tiene umbral; la afirmación que sostiene —el mapa es completo— sigue en pie.)
```

**Estado real de la validación:**

| Paso | Comando original (2026-09-21) | Primera corrección (2026-09-25) | Corrección intermedia (2026-09-26, superada) | Comando vigente (2026-09-26, H-1) |
|---|---|---|---|---|
| 1 · Ítems binarios | ❌ no pasa (0 y 3) | ✅ pasa (52 y 52) | ✅ pasa (52 y 52) | ✅ pasa (52 y 52) |
| 2 · Fuentes citadas | ✅ pasa (13) | ✅ pasa (13) | ✅ pasa (14) | ✅ pasa (14) |
| 3 · UNKNOWN declarados | ✅ pasa (9) | ✅ pasa (19) | ✅ pasa (21) | ✅ pasa (21) |
| 4 · Credenciales (bloqueante) | ❌ no pasa (falso positivo de código) | ⚠️ «pasa» (0) **porque dejó de mirar**: ciego a los 4 patrones | ⚠️ pasa (0) pero **ciego a los valores sin comillas de 12-15** | ✅ pasa (0), sostenido (umbral 12 sin comillas) |
| 5 · Tamaño de `EVIDENCIA.md` | ✅ pasa (100 líneas) | ✅ pasa (122 líneas) | ✅ pasa (125 líneas) | ✅ pasa (125 líneas) |

**Conclusión:** los cinco pasos pasan con el comando **vigente (2026-09-26)**. El paso 1
era un **falso negativo** con su comando original (contaba la casilla equivocada). El paso
4 pasó por dos estados: con el comando original era un **falso positivo** (marcaba la
lectura `os.environ.get` como si fuera un valor) y con la **primera corrección
(2026-09-25)** pasó porque **dejó de mirar** —el filtro `grep -v os.environ` descartaba la
línea entera y la clase había perdido el `:`—, quedando ciego a los cuatro patrones del
incidente. Ambos eran defectos del **comando**, no de los documentos. El comando vigente
alarma con los cuatro patrones y sigue sin alarmar con la lectura de entorno sin valor
(6 casos del umbral más los cuatro patrones del incidente, en §CONFIRMACIÓN DE PASO 4). La
afirmación anterior «Todos los pasos:
PASSED» no era sostenible con el comando original, y la del 2026-09-25 tampoco lo era con
el suyo.

Las cifras de los pasos 2, 3 y 5 suben entre columnas (13→14, 19→21, 122→125) porque la
corrección del token de Telegram (2026-09-26) añadió texto a `POSTMORTEM.md` y
`EVIDENCIA.md`, no porque cambiara el criterio. Las cifras 13, 19 y 122 eran correctas para
la versión del 2026-09-25.

> **CORRECCIÓN 2026-09-26 (paso 4, bloqueante) — el control había dejado de mirar.**
> **Comando original** (2026-09-21): `grep -riE
> "(api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_.:-]{12,}" .`
> **Por qué se cambió:** daba un falso positivo con expresiones de código;
> `os.environ.get` es una lectura del entorno, no un valor.
> **Qué se rompió al cambiarlo (2026-09-25):** se quitaron los `:` de la clase de
> caracteres y se añadió `| grep -viE "os\.environ|getenv|process\.env"`, que descarta la
> **línea entera**. El paso 4 pasó a dar `OK sin credenciales` porque el comando quedó
> **ciego a los cuatro patrones del incidente**: el valor por defecto de
> `os.environ.get("API_KEY", …)`, el token de Telegram (lleva `:`), `PRIVATE_KEY=<valor>`
> y `Authorization: Bearer <valor>`.
> **Cómo se cierra:** el comando vigente (arriba) no filtra líneas; distingue por forma y
> alarma con los cuatro patrones sin marcar la lectura de entorno sin valor.
>
> **Segunda corrección (2026-09-26, después superada):** el comando que cerró la ceguera
> (conservado literal abajo) distinguía por forma, pero **subió sin querer el umbral del
> tramo sin comillas a 16+ caracteres**: una credencial normal de 12 a 15 caracteres escrita
> **sin comillas** dejó de disparar la alarma. Su texto se conserva como historia:
> `grep -rniE "(api[_-]?key|token|secret|password|passwd|private[_-]?key|authorization|bearer)[\"']?[[:space:]]*[:=][[:space:]]*(bearer[[:space:]]+)?(['\"][^'\"]{12,}['\"]|[A-Za-z0-9_.:/+=-]{16,})|os\.environ[^)]*,[[:space:]]*['\"][^'\"]{12,}['\"]" .`
> **Tercera corrección — H-1 (2026-09-26):** se restaura `{12,}` en el tramo **sin
> comillas** y se añade un **terminador** que impide que una llamada de código cuente como
> valor: el token debe acabar en un carácter distinto de `(`, de modo que
> `os.environ.get(` no se toma por una credencial. El tramo **entrecomillado** ya exigía
> `{12,}`. Verificación de los **6 casos del umbral**, uno por uno, en §CONFIRMACIÓN DE
> PASO 4.

**Re-ejecución 2026-09-26** (tras la corrección del token de Telegram y de este comando):
paso 1 → 52/52 · paso 2 → **14** (una cita más a `LAMC_Master_Architecture_Document`) ·
paso 3 → **21** · paso 4 → **`OK sin credenciales`** (0 coincidencias, sostenido) ·
paso 5 → **125 líneas** de `EVIDENCIA.md`. Las cifras 13/19/122 de la transcripción
2026-09-25 corresponden a la versión anterior de los documentos, no a un cambio de
criterio.

---

## CUÁNTOS ÍTIEMS TIENE EL ESTÁNDAR

| Documento | Ítems de verificación | Casillas de decisión | Áreas cubiertas |
|-----------|-----------------------|----------------------|-----------------|
| `STANDARD.md` | **52** | 0 | 10/10 áreas mínimas del charter |
| `CHECKLIST.md` | **52** (los mismos 52, en formato operativo) | **3** | 10/10 áreas + resumen y decisión |

**Criterio de conteo:** una fila de la tabla de ítems por cada `N.M` (comando
`grep -cE "^\| [0-9]+\.[0-9]+ \|" STANDARD.md CHECKLIST.md` → `STANDARD.md:52`,
`CHECKLIST.md:52`). El estándar tiene **52 ítems**; la checklist reproduce los mismos
**52 ítems de verificación** más **3 casillas de decisión** (APROBADO / CONDICIONAL / NO
APROBADO). El total de casillas de la checklist es 52 + 3 = **55**; **no hay 107 ítems**.

> **CORRECCIÓN 2026-09-25:** antes decía «`CHECKLIST.md` · 55 ítems de verificación» y
> «Total 107». Era doble conteo: sumaba los 52 ítems del estándar y los 52 de la checklist
> como si fueran distintos, y contaba como verificación las 3 casillas de decisión. Los 3
> de diferencia entre 55 y 52 son exactamente esas casillas de decisión.

**Ítems por área:**
1. Custodia de claves: 4
2. Multisig: 4
3. Secretos: 5
4. Backups: 6
5. Base de datos: 5
6. Observabilidad: 6
7. Superficie de ataque: 5
8. Recovery: 5
9. Terceros: 5
10. Higiene operacional: 7

**Todos los ítems son binarios:** cada ítem lleva la marca `- [ ]` (se cumple o no se
cumple) dentro de su celda de tabla. **Prohibido:** "considerar", "evaluar", "tender a"
(0 ocurrencias verificadas).

> **CORRECCIÓN 2026-09-25:** la marca `- [ ]` vive **dentro** de la celda de la tabla de
> ítems, no al principio de la línea. Por eso el comando `grep -c "^- \[ \]"` no la cuenta
> (ver §SALIDA DE VALIDACIÓN). Los ítems siguen siendo binarios; lo que estaba mal era el
> comando con el que se contaban.

---

## QUÉ UNKNOWN DECLARÉ

| # | Descripción | Justificación |
|---|-------------|---------------|
| 1 | Fecha exacta del incidente | Solo se conoce mayo 2026, día no documentado |
| 2 | Causa raíz de corrupción EXT4 | El documento de transición no especifica causa |
| 3 | Pérdida de datos financieros | No consta si finanzas.db fue afectada |
| 4 | Alcance completo de archivos dañados | No se realizó análisis forense completo |
| 5 | Coste estimado del incidente | No se cuantificó formalmente |
| 6 | Impacto operacional no cuantificado | Sin métricas de downtime |
| 7 | Efectividad de políticas derivadas | No se ha medido aún |
| 8 | Estado de rotación de credenciales | Acción pendiente: no consta que se haya rotado |
| 9 | Cobertura actual de observabilidad | Implementación parcial, no medida |
| 10 | **Localización actual del token de Telegram** (su existencia está establecida) | No se ha inventariado dónde sigue vivo el valor (historial, respaldos, cachés) |

**Todos los UNKNOWN son legítimos:** no se infirieron por ausencia de evidencia (axioma A3: "La ausencia de evidencia no constituye evidencia").

---

## CONFIRMACIÓN DE PASO 4 (CRÍTICO)

```bash
$ cd proyectos/P3_OPS_SEC/entregables        # desde la raiz del programa
$ grep -rniE "(api[_-]?key|token|secret|password|passwd|private[_-]?key|authorization|bearer)[\"']?[[:space:]]*[:=][[:space:]]*(bearer[[:space:]]+)?(['\"][^'\"]{12,}['\"]|[A-Za-z0-9_.:/+=-]{12,}([^A-Za-z0-9_.:/+=(-]|$))|os\.environ[^)]*,[[:space:]]*['\"][^'\"]{12,}['\"]" . && echo "!!! FUGA DE CREDENCIAL !!!" || echo "OK sin credenciales"
OK sin credenciales
```

**CONFIRMADO: cero valores de credenciales en los entregables.** El comando vigente busca
un **valor**, no la mera mención de la palabra «token» o «API key», y distingue la lectura
de entorno **con** valor por defecto (alarma) de la lectura **sin** valor (no alarma). Los
dos tramos de valor exigen **12 caracteres o más**: el **entrecomillado** desde siempre y el
**sin comillas** desde la corrección H-1 del 2026-09-26 (la versión intermedia del
2026-09-26 los había subido a 16 por error).

**Verificación de los casos que definen el criterio** (ejecutada 2026-09-26, un archivo por
caso, con el comando vigente; valores inventados para la prueba, ningún valor real):

| Caso | Contenido de prueba | Resultado exigido | Resultado real |
|---|---|---|---|
| a | `API_KEY = os.environ.get("API_KEY", «valor por defecto»)` | ALARMA | ✅ ALARMA |
| b | `TOKEN = «dígitos:cadena del token»` | ALARMA | ✅ ALARMA |
| c | `PRIVATE_KEY=0x«64 hex»` | ALARMA | ✅ ALARMA |
| d | `Authorization: Bearer «jwt»` | ALARMA | ✅ ALARMA |
| e | `API_KEY = os.environ.get("API_KEY")` | SIN ALARMA | ✅ SIN ALARMA |
| f | `API_KEY = «valor largo entre comillas»` | ALARMA (regresión) | ✅ ALARMA |

**Casos del umbral** (corrección H-1, 2026-09-26; los tres primeros son los que la versión
intermedia dejó pasar sin alarma). Mismo comando, un archivo por caso:

| Caso | Contenido de prueba | Tramo / umbral | Resultado exigido | Resultado real |
|---|---|---|---|---|
| g | `TOKEN=«12 caracteres, sin comillas»` | sin comillas / 12 | ALARMA | ✅ ALARMA |
| h | `TOKEN=«15 caracteres, sin comillas»` | sin comillas / 12 | ALARMA | ✅ ALARMA |
| i | `TOKEN=«16 caracteres, sin comillas»` | sin comillas / 12 | ALARMA | ✅ ALARMA |
| j | `TOKEN = «12 caracteres, entre comillas»` | entre comillas / 12 | ALARMA | ✅ ALARMA |
| k | `API_KEY = os.environ.get("API_KEY")` | — (sin valor) | SIN ALARMA | ✅ SIN ALARMA |
| l | `API_KEY = os.environ.get("API_KEY", «16 caracteres, entre comillas»)` | entre comillas / 12 | ALARMA | ✅ ALARMA |

> El caso **e** es el que motivó el falso positivo original: el comando vigente lo
> distingue del caso **a** por la presencia del **segundo argumento** (valor por defecto).
> El caso **f** cubre la regresión **entre comillas**, tramo que el comando nunca dejó de
> ver.

> **CORRECCIÓN H-1 (2026-09-26) — aquí había una afirmación falsa.** Este apartado decía
> que el caso **f** probaba que el comando «no perdió lo que el anterior sí detectaba».
> Era **falso para el tramo sin comillas**: el caso **f** solo ejercita un valor
> **entrecomillado**, y la versión intermedia del comando exigía `{16,}` a los valores
> **sin comillas**, de modo que una credencial de 12 a 15 caracteres escrita sin comillas
> **no** disparaba la alarma. El tramo **sin comillas** se recuperó el **2026-09-26** con la
> corrección H-1; los casos **g**, **h** e **i** lo comprueban (12, 15 y 16 caracteres sin
> comillas). Lo que el comando no perdió es lo **entrecomillado** (caso **f**); lo que sí
> había perdido, hasta H-1, era el tramo **sin comillas**.

> **CORRECCIÓN 2026-09-25:** antes esta sección mostraba el comando original y concluía
> «OK sin credenciales». El comando original **no daba eso**: encontraba dos coincidencias
> en este mismo documento (una lectura `os.environ.get` con valor por defecto —el patrón
> del incidente, enmascarada arriba— y otra sin valor) y activaba el aviso de fuga. La
> conclusión era correcta, pero la comprobación no la sostenía.

**Nota sobre el alcance:** las credenciales comprometidas están en el **corpus crudo**
(inmutable), no en los entregables. La rotación debe realizarse antes de publicar y es una
acción del operador: **no consta que se haya hecho** (`UNKNOWN`).

---

## ESTADO DE LA ROTACIÓN DE CREDENCIALES

| Acción | Estado | Detalle |
|--------|--------|---------|
| Rotar la API key comprometida | ⛔ PENDIENTE / no consta | El valor hardcodeado sigue presente en el corpus crudo (ver §HALLAZGOS) |
| Rotar el token de Telegram | ⛔ PENDIENTE / no consta | Token **real y comprometido**: el registro interno el registro interno (no publicado) lo confirma y el patrón reaparece en 2 commits del historial del corpus. La **localización actual del valor** es `UNKNOWN` (ver §HALLAZGOS) |

> **CORRECCIÓN 2026-09-25:** esta sección llevaba un título interno y dos autorizaciones
> internas numeradas. Se retiran el título y los códigos porque este documento se publica
> en abierto y un lector externo no puede seguirlos. La condición técnica —no publicar
> mientras haya credenciales comprometidas sin rotar— se conserva, y sigue siendo
> bloqueante.

---

## HALLAZGOS ADICIONALES

### API key hardcodeada (verificado 2026-09-25)

`finanzas/api.py` línea 10 contiene hoy la forma remediada, sin fallback:

```python
API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY no definida en el entorno.")
```

Un valor literal hardcodeado con esa API key sigue presente en **6 archivos** del corpus
crudo:

1. `finanzas/api.py.bak` (línea 6)
2. `finanzas/api_FUNCIONANDO.py` (línea 6)
3. `finanzas/start.sh` (línea 5)
4. `filesfinanzaspersonales/start.sh` (línea 5)
5. `finanzas/__pycache__/api.py.cpython-313.pyc` (bytecode)
6. `finanzas/__pycache__/api_FUNCIONANDO.cpython-313.pyc` (bytecode)

La rotación de esa API key es **pendiente** y **no consta** que se haya hecho.

> **CORRECCIÓN 2026-09-25:** antes decía que la clave estaba hardcodeada como *fallback*
> (`os.environ.get("API_KEY", "…")`) en `finanzas/api.py`, **línea 10 del archivo
> original**, y listaba como alcance de rotación `finanzas/bot_telegram.py` y la caché
> `finanzas/__pycache__/api.cpython-313.pyc`. Verificado contra el corpus:
> - El patrón *fallback con valor por defecto* en la **línea 10** no está en
>   `finanzas/api.py`, sino en `filesfinanzaspersonales/api.py`, cuya línea 10 es
>   `API_KEY = os.environ.get("FINANZAS_API_KEY", "…")` —valor por defecto de ejemplo, no
>   una credencial real—. Es un archivo **distinto** del citado.
> - El estado «original» de `finanzas/api.py` **no está en el corpus**: no se puede
>   comprobar qué decía su línea 10 antes de la remediación → `UNKNOWN`.
> - `finanzas/bot_telegram.py` **no** contiene un valor hardcodeado: lee
>   `os.environ.get("FINANZAS_API_KEY", "")`. No entra en el alcance de rotación.
> - Las cachés que contienen el valor no son `api.cpython-313.pyc`, sino
>   `api.py.cpython-313.pyc` y `api_FUNCIONANDO.cpython-313.pyc`.
> - El valor también está en `filesfinanzaspersonales/start.sh`, que no estaba listado.

### Token de Telegram en `safefactorbot.md`: real y comprometido

**Existencia establecida; el valor no se reproduce.** El token de Telegram **era real** y
quedó comprometido. Verificado el 2026-09-26, sin exponer el valor:

- El registro interno del programa (el registro interno (no publicado), entradas del 2026-09-23) documenta que el
  token era **real** y que **seguía en todos los commits** del corpus (la rotación pendiente y la
  la rotación de credenciales **pendiente**).
- El patrón de token de Telegram `[0-9]{8,12}:[A-Za-z0-9_-]{30,}` aparece en **2 commits**
  del historial del repositorio del corpus (`f1d3841`, 2026-09-23, que lo introduce;
  `1dadccd`, 2026-09-24, que lo retira), sobre `_LAMC_EVOLUCION/textos/safefactorbot.md`.
- El archivo **actual** solo contiene los marcadores `CAMBIA_ESTE_TOKEN` y
  `CAMBIA_ESTE_CHAT_ID`, y el patrón devuelve **0** sobre el árbol de trabajo (2026-09-25).
  Eso prueba que el árbol está limpio, **no** que el token no existiera.

**`UNKNOWN`:** el **inventario actual completo de dónde sigue vivo el valor** (historial,
respaldos, cachés). El `UNKNOWN` es de **localización**, **no de existencia**. La rotación de
este token **sigue siendo obligatoria** y permanece en la rotación de credenciales **pendiente**: **no consta** que se haya
hecho.

> **CORRECCIÓN 2026-09-26:** la versión anterior daba la afirmación por «no reproducible
> contra el archivo citado» y **retiraba «token de Telegram» del alcance de rotación**. Era
> A3 al revés —«no lo encontré» → «no hace falta»— y podía llevar a **no rotar una credencial
> real**. Se corrige: existencia establecida, valor no reproducido, `UNKNOWN` reubicado en la
> localización actual y rotación restituida a la rotación de credenciales **pendiente**.

---

## CERTIFICACIÓN

Este trabajo está listo para una **revisión independiente** de su autoría.

**Este documento NO se marca a sí mismo `PASS`.** La certificación corresponde a la
revisión independiente, no a quien produjo los entregables.

> **CORRECCIÓN 2026-09-25:** la frase anterior tenía redacción rota y un término interno
> de organización. Se reescribe sin el término interno.

---

*Resumen generado por el equipo del proyecto P3 — 2026-09-21 · revisado 2026-09-25*
