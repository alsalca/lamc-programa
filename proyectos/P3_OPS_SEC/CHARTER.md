# CHARTER — P3 `OPS_SEC`

**Estado:** ✅ **PUBLICADO** · **Ola:** 1 · **Coste estimado:** 4–6 días
**Autoría:** equipo del proyecto P3 · **Revisión:** independiente de la autoría · **Aprobado:** 2026-09-21

> **NOTA DE EDICIÓN 2026-09-25:** este documento se publica en un repositorio abierto.
> Se han retirado los términos internos de organización, los números de autorización
> internos y las referencias a archivos que no forman parte del paquete publicado. La
> condición técnica que esos términos describían se conserva en lenguaje verificable.
> El detalle, sección por sección, se deja anotado donde correspondía.

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
> operacional."* — Hugh Karp, fundador de Nexus Mutual (declaración recogida por
> **CoinDesk, 16-may-2026**; ver nota de procedencia)
>
> *"Esos escenarios son mucho más difíciles de asegurar porque los equipos a menudo
> carecen de prácticas de seguridad operacional estandarizadas. Sin estándares claros,
> las aseguradoras no pueden tarifar el riesgo de forma fiable."*

> **NOTA DE PROCEDENCIA 2026-09-25:** la fuente que un lector externo puede seguir es el
> documento público `publicacion/publicos/PORQUE.md`, que atribuye a Hugh Karp, fundador de
> Nexus Mutual, una declaración recogida por **CoinDesk el 16-may-2026** (artículo «Crypto
> users are choosing juicy yields over protection…»). Ese documento la registra como
> **paráfrasis del periodista, no cita textual**. Los dos bloques de arriba son la versión
> inglesa registrada internamente de la misma declaración; la de `PORQUE.md` está en
> español y no coincide palabra por palabra. Se conserva el nombre porque la cita es
> pública, atribuida y pertinente para el argumento; la fecha se afirma solo para la
> declaración recogida por CoinDesk, que es la que `PORQUE.md` fecha. No se ha localizado
> el texto inglés original en el paquete publicado: la coincidencia literal exacta con el
> artículo de CoinDesk es `UNKNOWN`.

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
| `LAMC_Master_Architecture_Document.md` | Política de secretos, `(ruta interna omitida)`, CORE+EDGE, backups | `_LAMC_EVOLUCION/textos/` |
| `LAMC_BOT_POLICY_IA_INSTRUCTIONS.md` | Las 10 reglas obligatorias de bots, ficha, separación PROD/exp | `_LAMC_EVOLUCION/textos/` |
| `LAMC_CORE_NODE_Resumen_Sesion.md` | La migración, stack implementado | `_LAMC_EVOLUCION/textos/` |
| `LAMC_MASTER_CONSTITUTION_v5.md` | P2 Recovery First, P4 Zero Trust, P8 Producción Intocable | `_LAMC_EVOLUCION/textos/` |

> **NOTA SOBRE LAS FUENTES 2026-09-25:** los cinco documentos de `_LAMC_EVOLUCION/textos/`
> son **documentos internos del operador y NO se publican** en este paquete. Se citan por su
> nombre y su ruta interna porque son la fuente real del post-mortem, pero **un verificador
> externo no puede abrirlos ni comprobarlos**: ese tramo del mapa de evidencia es `UNKNOWN`
> para un tercero. Se conservan las citas —son la trazabilidad del post-mortem— y se declara
> su límite en vez de esconderlo.

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

> **CORRECCIÓN 2026-09-25:** los pasos 1 y 4 de este bloque estaban mal escritos y no
> comprobaban lo que decían comprobar. Se corrigen aquí para que el bloque sea
> reproducible. La transcripción de la salida real, con los pasos que pasan y los que
> no, está en `entregables/RESUMEN.md`.

```bash
cd proyectos/P3_OPS_SEC/entregables

# 1. Cada ítem del estándar es verificable (formato binario)
#    Los ítems son celdas de tabla: la línea empieza por «|», no por «- [ ]».
#    Hay que contar las FILAS de la tabla de ítems, no las casillas sueltas.
grep -cE "^\| [0-9]+\.[0-9]+ \|" STANDARD.md CHECKLIST.md
#    Salida real: STANDARD.md:52  CHECKLIST.md:52
#    (El comando anterior, `grep -c "^- \[ \]"`, daba STANDARD.md:0 y CHECKLIST.md:3:
#     solo cazaba las 3 casillas de DECISIÓN de CHECKLIST.md, líneas 181-183, que no
#     son ítems de verificación.)

# 2. El post-mortem cita fuentes
grep -c "LAMC_Incident_Transitional_Policy_v4_2_2\|LAMC_CORE_NODE_Resumen_Sesion\|LAMC_Master_Architecture_Document" POSTMORTEM.md

# 3. Existe declaración explícita de UNKNOWN
grep -ci "UNKNOWN\|NO_CONSTA\|no consta" POSTMORTEM.md

# 4. CERO credenciales en los documentos (CRÍTICO, bloqueante)
#    UN SOLO comando canónico en todo P3 (idéntico en CHARTER §6, STANDARD §VALIDACIÓN
#    paso 4, RESUMEN §SALIDA y §CONFIRMACIÓN, y el prompt operativo). Cubre los cuatro
#    del incidente, alarma con valores entrecomillados de 12+ y SIN comillas de 12+, y NO
#    da falso positivo con la lectura de entorno sin valor. Historia de las correcciones
#    (2026-09-25 y 2026-09-26, incluida la que subió el umbral sin querer) en la nota de
#    abajo.
grep -rniE "(api[_-]?key|token|secret|password|passwd|private[_-]?key|authorization|bearer)[\"']?[[:space:]]*[:=][[:space:]]*(bearer[[:space:]]+)?(['\"][^'\"]{12,}['\"]|[A-Za-z0-9_.:/+=-]{12,}([^A-Za-z0-9_.:/+=(-]|$))|os\.environ[^)]*,[[:space:]]*['\"][^'\"]{12,}['\"]" . && echo "!!! FUGA DE CREDENCIAL !!!" || echo "OK sin credenciales"
#    Salida real sobre `entregables/` (2026-09-26): `OK sin credenciales`.

# 5. El mapa de evidencia cubre todas las afirmaciones
wc -l EVIDENCIA.md
```

**Criterio:** los cinco pasos pasan. **El paso 4 es bloqueante**: si hay una sola
credencial en los documentos, el proyecto es `BLOCK`.

> **CORRECCIÓN 2026-09-26 — el paso 4 había dejado de mirar (hallazgo bloqueante R3).**
> **Comando original** (2026-09-21): `grep -riE
> "(api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_.:-]{12,}" .` — daba un
> **falso positivo** con expresiones de código: `os.environ.get` es una lectura del
> entorno, no un valor.
> **Primera corrección (2026-09-25):** quitó los dos puntos (`:`) de la clase de caracteres
> y añadió `| grep -viE "os\.environ|getenv|process\.env"`, que descarta la **línea
> entera**. Apagó el falso positivo, pero dejó el comando **ciego a los cuatro patrones del
> incidente**: el valor por defecto dentro de `os.environ.get("API_KEY", …)` (el filtro tira
> la línea), el token de Telegram (`[0-9]{8,12}:[A-Za-z0-9_-]{30,}`, que lleva `:`),
> `PRIVATE_KEY=<valor>` y `Authorization: Bearer <valor>`. El paso 4 pasaba porque **dejó
> de mirar**.
> **Segunda corrección (2026-09-26, después superada):** el comando que cerró el defecto
> de ceguera no filtraba líneas y distinguía por forma, pero **subió sin querer el umbral
> de las tiras sin comillas a 16+ caracteres** (`…|[A-Za-z0-9_.:/+=-]{16,})…`). Volvía a
> mirar los cuatro patrones del incidente, pero quedaba **ciego a los valores sin comillas
> de 12 a 15 caracteres** —la mayoría de las credenciales normales escritas sin comillas—.
> El comando de esa versión se conserva **literal** como historia (es el que aparece en las
> notas del 2026-09-26 anteriores a H-1):
> `grep -rniE "(api[_-]?key|token|secret|password|passwd|private[_-]?key|authorization|bearer)[\"']?[[:space:]]*[:=][[:space:]]*(bearer[[:space:]]+)?(['\"][^'\"]{12,}['\"]|[A-Za-z0-9_.:/+=-]{16,})|os\.environ[^)]*,[[:space:]]*['\"][^'\"]{12,}['\"]" .`
> **Tercera corrección — H-1 (2026-09-26):** se restaura el umbral **`{12,}`** en el tramo
> **sin comillas** y se añade un **terminador** que impide que una llamada de código cuente
> como valor: el token debe terminar en un carácter que no sea `(`, de modo que
> `os.environ.get(` no se toma por una credencial. El tramo **entrecomillado** ya exigía
> `{12,}` y no cambia. Con el comando canónico de arriba, el paso 4 alarma con los cuatro
> patrones del incidente, con los valores entrecomillados de 12+ y con los **sin comillas de
> 12+**, y sigue sin alarmar con `os.environ.get("API_KEY")` sin valor. Verificación de los
> **6 casos del umbral** y de los casos del incidente, uno por uno, en
> `entregables/RESUMEN.md` §SALIDA DE VALIDACIÓN DETERMINÍSTICA y §CONFIRMACIÓN DE PASO 4.
> El paso 1 no pasaba con su comando original; con el comando corregido da 52 y 52.

---

## 7. FUERA DE ALCANCE

- ❌ Acusar a terceros o a proveedores por nombre
- ❌ Reproducir valores de credenciales **en ninguna forma, ni parcialmente**
- ❌ Publicar mientras sigan existiendo credenciales comprometidas sin rotar
- ❌ Prometer certificación, auditoría o cumplimiento
- ❌ Convertirlo en producto de software

---

## 8. RIESGOS

| ID | Riesgo | Mitigación |
|---|---|---|
| **R-004** | **Exponer credenciales al publicar** | **Bloqueante.** Rotación previa de las credenciales comprometidas. Paso 4 de validación. Revisión manual independiente |
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
| **M-P3-04** | Registrar el estado de la rotación de credenciales | Registro interno (no publicado en este paquete) |

**La verificación de credenciales (M-P3-03) y la rotación de las comprometidas son
precondición de cualquier publicación.**

---

## 10. CRITERIO DE TERMINADO

`PASS` cuando:
1. Cada ítem del estándar es binario y verificable.
2. Cada afirmación del post-mortem cita una fuente cruda.
3. **Cero credenciales** en los entregables (verificado con el paso 4).
4. Los `UNKNOWN` (día exacto del incidente, pérdida de datos) están declarados.

---

## 11. CONDICIÓN PREVIA A LA PUBLICACIÓN

- **Rotación de las credenciales comprometidas.** **Bloqueante** (riesgo R-004). Antes de
  publicar cualquier entregable debe haberse rotado toda credencial expuesta en el corpus.
  La comprobación mecánica es el paso 4 de §6.
- **Publicación externa.** Posterior a la rotación.

> **CORRECCIÓN 2026-09-25:** esta sección llevaba un título interno y estaba redactada
> con dos autorizaciones internas numeradas y una entrada de un registro interno que no
> forma parte de este paquete. Se retiran el título, los códigos y la referencia al
> registro interno: este documento se publica en abierto y un lector externo no puede
> abrirlos ni seguirlos. La condición técnica —rotar las credenciales antes de publicar—
> se conserva, y sigue siendo bloqueante.
