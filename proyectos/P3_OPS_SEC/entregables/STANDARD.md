# ESTÁNDAR DE SEGURIDAD OPERACIONAL PARA POSICIONES DeFi

**Versión:** 1.0.0
**Fecha:** 2026-09-21
**Proyecto:** P3_OPS_SEC — estándar de seguridad operacional
**Estado:** Pre-publicación (pendiente de rotación de las credenciales comprometidas)

> **NOTA DE EDICIÓN 2026-09-25:** se han retirado de este documento los términos internos
> de organización, los números de autorización internos y las referencias a archivos que no
> forman parte del paquete publicado. Se conserva la condición técnica que describían.

---

## PROPÓSITO

Este estándar define **requisitos binarios** (se cumplen o no se cumplen) para la operación segura de posiciones DeFi. Cada ítem es verificable por un tercero independiente. No hay espacio para interpretaciones: o se cumple, o no se cumple.

**Inspiración directa:** Las 10 reglas de `LAMC_BOT_POLICY_IA_INSTRUCTIONS.md` y las políticas SS20 del `LAMC_Incident_Transitional_Policy_v4_2_2.md`, generalizadas de una operación personal a un estándar aplicable a cualquier posición DeFi.

---

## 1. CUSTODIA DE CLAVES

| # | Requisito | Verificación |
|---|-----------|--------------|
| 1.1 | `- [ ]` Las claves privadas de wallets con fondos significativos >1 ETH viven en hardware wallet, no en software | Inspección física del dispositivo |
| 1.2 | `- [ ]` La clave de recuperación (seed phrase) está almacenada en ubicación física separada del hardware wallet, en formato resistente a fuego/agua | Verificación de ubicación y material |
| 1.3 | `- [ ]` Existe documentación escrita del proceso de recuperación ante pérdida/robo del hardware wallet | Documento disponible y revisado en últimos 90 días |
| 1.4 | `- [ ]` Ninguna clave privada de wallets con fondos >0.1 ETH aparece en archivo de texto plano, clipboard, o mensaje de mensajería | Búsqueda en filesystem y logs |

---

## 2. MULTISIG

| # | Requisito | Verificación |
|---|-----------|--------------|
| 2.1 | `- [ ]` Cualquier wallet con fondos >10 ETH opera bajo esquema multisig (mínimo 2 de 3 firmantes) | Inspección de configuración on-chain o del contrato |
| 2.2 | `- [ ]` Los firmantes del multisig están en dispositivos/ubicaciones físicas separadas | Declaración firmada de cada firmante |
| 2.3 | `- [ ]` La verificación de transacciones se realiza fuera de banda (no en el mismo dispositivo que firma) | Procedimiento documentado |
| 2.4 | `- [ ]` Existe un proceso documentado para revocar un firmante comprometido sin bloquear fondos | Documento disponible y probado en últimos 180 días |

---

## 3. SECRETOS

| # | Requisito | Verificación |
|---|-----------|--------------|
| 3.1 | `- [ ]` Ningún API key, token, o secreto de producción aparece en código fuente, repositorio, o documentación pública | Búsqueda de **valores** en el repo (comando canónico en §VALIDACIÓN, paso 4) |
| 3.2 | `- [ ]` Todos los secretos viven en un gestor dedicado (ej: `el gestor de secretos/`, gestor de secretos, o vault) | Inspección de configuración |
| 3.3 | `- [ ]` Los secretos en disco tienen permisos `600` (solo propietario) | `ls -la` del directorio de secretos |
| 3.4 | `- [ ]` Existe un proceso documentado de rotación de secretos con frecuencia máxima de 90 días | Registro de rotaciones de los últimos 12 meses |
| 3.5 | `- [ ]` Ningún secreto de producción aparece en logs, mensajes de error, o dumps de stack | Revisión de logs de últimos 30 días |

---

## 4. BACKUPS

| # | Requisito | Verificación |
|---|-----------|--------------|
| 4.1 | `- [ ]` Existe backup automático de la base de datos de posiciones con frecuencia máxima de 24 horas | Cron job o script verificable |
| 4.2 | `- [ ]` Los backups se almacenan en ubicación física diferente a la base de datos original | Inspección de rutas de destino |
| 4.3 | `- [ ]` Existe al menos un backup offline/air-gapped (no accesible por red) | Verificación física del medio |
| 4.4 | `- [ ]` Se realiza verificación de integridad de backups (checksum) al menos semanalmente | Registro de verificaciones |
| 4.5 | `- [ ]` Existe proceso documentado de restauración y se ha probado en últimos 180 días | Registro de pruebas de restauración |
| 4.6 | `- [ ]` Los backups están cifrados con algoritmo AES-256 o equivalente | Verificación de configuración de cifrado |

---

## 5. BASE DE DATOS

| # | Requisito | Verificación |
|---|-----------|--------------|
| 5.1 | `- [ ]` SQLite opera en WAL (Write-Ahead Logging) mode | `PRAGMA journal_mode;` retorna "wal" |
| 5.2 | `- [ ]` Se ejecuta `integrity_check` programado al menos diariamente | Cron job o script con registro de ejecución |
| 5.3 | `- [ ]` La base de datos tiene backups automáticos antes de cada migración esquemática | Script de migración incluye paso de backup |
| 5.4 | `- [ ]` Existe monitoreo de tamaño de base de datos y alerta si supera umbral esperado | Configuración de alerta verificable |
| 5.5 | `- [ ]` No se permite acceso directo a la base de datos desde herramientas de desarrollo sin pass-through por API | Configuración de permisos o documentation de acceso |

---

## 6. OBSERVABILIDAD

| # | Requisito | Verificación |
|---|-----------|--------------|
| 6.1 | `- [ ]` El sistema de monitoreo (ej: Uptime Kuma) está operativo y verificable externamente | Endpoint de health check público |
| 6.2 | `- [ ]` Existen alertas configuradas para: caída de servicios, latencia >500ms, uso de disco >80% | Configuración de alertas revisable |
| 6.3 | `- [ ]` Los logs de seguridad se retienen por mínimo 90 días | Configuración de retención de logs |
| 6.4 | `- [ ]` Existe dashboard de salud del sistema visible para el operador en todo momento | Acceso al dashboard verificado |
| 6.5 | `- [ ]` Se monitorea la integridad del filesystem (warnings de EXT4, SMART en discos) | Configuración de monitoreo activa |
| 6.6 | `- [ ]` Cada servicio productivo tiene su propio archivo de logs, no mezclado con otros servicios | Estructura de logs verificable |

---

## 7. SUPERFICIE DE ATAQUE

| # | Requisito | Verificación |
|---|-----------|--------------|
| 7.1 | `- [ ]` La superficie de red expuesta es mínima: solo puertos necesarios están abiertos o tunelados | Escaneo de puertos o configuración de firewall |
| 7.2 | `- [ ]` Existe separación física o lógica entre entorno de producción y entorno de laboratorio/experimentación | Inspección de infraestructura |
| 7.3 | `- [ ]` Ningún experimento se ejecuta en el servidor de producción | Política documentada y registro de auditoría |
| 7.4 | `- [ ]` Los servicios de desarrollo no están expuestos a internet | Configuración de red verificable |
| 7.5 | `- [ ]` Existe allowlist de IPs para acceso administrativo (SSH, paneles de control) | Configuración de firewall o VPN |

---

## 8. RECOVERY

| # | Requisito | Verificación |
|---|-----------|--------------|
| 8.1 | `- [ ]` Existe un Recovery Time Objective (RTO) declarado y documentado para cada servicio crítico | Documento de continuidad operacional |
| 8.2 | `- [ ]` El procedimiento de recovery está documentado paso a paso (runbook) | Runbook disponible y actualizado |
| 8.3 | `- [ ]` Se ha realizado al menos un drill de recovery en los últimos 180 días | Registro del drill con fecha y resultado |
| 8.4 | `- [ ]` La infraestructura es reproducible mediante scripts/documentación (no depende de memoria humana) | Intento de recreación desde cero documentado |
| 8.5 | `- [ ]` Existe procedimiento para recuperar acceso ante compromiso de dispositivo de administración | Documento de escalamiento |

---

## 9. TERCEROS

| # | Requisito | Verificación |
|---|-----------|--------------|
| 9.1 | `- [ ]` Existe inventario de todos los proveedores de servicios críticos (RPC, custody, oracle) con fechas de revisión | Registro actualizado |
| 9.2 | `- [ ]` Cada proveedor tiene documentado su proceso de soporte y escalamiento | Documento de acuerdos o contacto verificado |
| 9.3 | `- [ ]` Existe proceso de revocación de accesos a terceros al terminar relación comercial | Procedimiento documentado |
| 9.4 | `- [ ]` No hay dependencia de un único proveedor para servicios críticos (single point of failure) | Análisis de dependencias |
| 9.5 | `- [ ]` Los permisos otorgados a terceros se revisan trimestralmente | Registro de revisiones |

---

## 10. HIGIENE OPERACIONAL

| # | Requisito | Verificación |
|---|-----------|--------------|
| 10.1 | `- [ ]` Se aplica Zero-Trust en el entorno de desarrollo: no se confía en scripts, dependencias, o código no revisado | Proceso de code review documentado |
| 10.2 | `- [ ]` No se ejecutan scripts de fuentes desconocidas sin análisis previo | Política documentada |
| 10.3 | `- [ ]` Existe proceso de gestión de dependencias (actualización, renovación, eliminación de obsoletas) | Registro de auditoría de dependencias |
| 10.4 | `- [ ]` Los dispositivos de administración tienen cifrado de disco activado | Verificación en dispositivos |
| 10.5 | `- [ ]` Existe política de contraseñas: mínimo 16 caracteres, no reutilizadas entre servicios | Configuración de políticas |
| 10.6 | `- [ ]` Se realiza revisión de seguridad de código antes de cada despliegue a producción | Registro de revisiones |
| 10.7 | `- [ ]` No hay credenciales hardcodeadas en ningún archivo del sistema (post-remediación) | `grep` de valores hardcodeados (comando canónico en §VALIDACIÓN, paso 4) |

---

## VALIDACIÓN

### Paso 1: Formato binario
```bash
# Los ítems son filas de tabla; la marca `- [ ]` va dentro de la celda.
grep -cE "^\| [0-9]+\.[0-9]+ \|" STANDARD.md
# Resultado real: 52 (número de ítems del estándar)
```
> **CORRECCIÓN 2026-09-25:** aquí decía `grep -c "^- \[ \]" STANDARD.md` con «resultado
> esperado ≥50». Ese comando da **0** en este archivo, porque la línea de cada ítem empieza
> por `|` y no por `- [ ]`. Se sustituye por el conteo de filas de la tabla, que es lo que
> se pretendía medir.

### Paso 2: Ausencia de lenguaje aspiracional
```bash
grep -iE "considerar|evaluar|tender a|podría|debería" STANDARD.md
# Resultado esperado: 0 coincidencias
```

### Paso 3: Cobertura de áreas mínimas
Las 10 áreas del charter están representadas:
- [x] Custodia de claves (§1)
- [x] Multisig (§2)
- [x] Secretos (§3)
- [x] Backups (§4)
- [x] Base de datos (§5)
- [x] Observabilidad (§6)
- [x] Superficie de ataque (§7)
- [x] Recovery (§8)
- [x] Terceros (§9)
- [x] Higiene operacional (§10)

### Paso 4: Cero credenciales hardcodeadas (bloqueante)
```bash
grep -rniE "(api[_-]?key|token|secret|password|passwd|private[_-]?key|authorization|bearer)[\"']?[[:space:]]*[:=][[:space:]]*(bearer[[:space:]]+)?(['\"][^'\"]{12,}['\"]|[A-Za-z0-9_.:/+=-]{12,}([^A-Za-z0-9_.:/+=(-]|$))|os\.environ[^)]*,[[:space:]]*['\"][^'\"]{12,}['\"]" . && echo "!!! FUGA DE CREDENCIAL !!!" || echo "OK sin credenciales"
# Resultado real (2026-09-26): «OK sin credenciales» (0 valores hardcodeados).
# Busca un VALOR, no una mención. Este es el comando canónico del proyecto (idéntico al
# de CHARTER.md §6 y RESUMEN.md §SALIDA y §CONFIRMACIÓN, y del prompt operativo).
```
> **MAQUETACIÓN:** el comando vive en un bloque de código y **no** dentro de una celda de
> tabla: contiene `|` literales, y un `|` sin escapar dentro de una celda rompería la tabla
> de Markdown (era el defecto de los ítems 3.1 y 10.7, que ahora lo referencian en vez de
> copiarlo).

> **CORRECCIÓN 2026-09-25:** el comando anterior era `grep -rE
> "api[_-]?key\|token\|secret" ...`. En expresiones regulares extendidas `\|` no es
> alternancia: busca el carácter `|` literal, así que no comprobaba lo que decía. Se
> sustituyó por un comando con `|` sin escapar y buscando un valor entrecomillado.

> **CORRECCIÓN 2026-09-26 — el comando unificado del 2026-09-25 era ciego (hallazgo
> bloqueante R3).** **Comando original** (2026-09-21): `grep -riE
> "(api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_.:-]{12,}" .`
> **Por qué se cambió:** daba un falso positivo con expresiones de código;
> `os.environ.get` es una lectura del entorno, no un valor. **Qué se rompió al cambiarlo:**
> la corrección quitó los `:` de la clase de caracteres y añadió `| grep -viE
> "os\.environ|getenv|process\.env"`, que descarta la **línea entera**; el paso 4 pasó a dar
> «OK sin credenciales» porque quedó **ciego a los cuatro patrones del incidente** —el
> valor por defecto de `os.environ.get("API_KEY", …)`, el token de Telegram (lleva `:`),
> `PRIVATE_KEY=<valor>` y `Authorization: Bearer <valor>`—. **Cómo se cierra el falso
> positivo:** con un comando que no filtra líneas y distingue por forma. La primera versión
> de ese cierre (2026-09-26, después superada) alzó el umbral de las tiras **sin comillas**
> a `{16,}` y quedó **ciega a los valores de 12 a 15 caracteres sin comillas**; su texto se
> conserva **literal** como historia (véase `CHARTER.md` §6 y `RESUMEN.md`). **Cierre H-1
> (2026-09-26):** el comando canónico de arriba restaura `{12,}` en el tramo **sin
> comillas** y exige que el token termine en un carácter distinto de `(`, para que
> `os.environ.get(` no cuente como valor; el tramo **entrecomillado** ya exigía `{12,}` y no
> cambia. Alarma con los cuatro patrones del incidente y con los **6 casos del umbral**
> (12/15/16 sin comillas, 12 entrecomillado, `os.environ` sin valor y `os.environ` con
> valor), ejecutados en `RESUMEN.md` §CONFIRMACIÓN DE PASO 4. `entregables/` sigue dando
> «OK sin credenciales».

---

## USO

1. **Auditoría:** un tercero puede tomar este estándar y verificar cada ítem contra la operación real, uno por uno.
2. **Mejora continua:** cada ítem no cumplido se convierte en acción correctiva con fecha objetivo.
3. **Seguro:** las aseguradoras pueden usar este estándar para tarifar el riesgo operacional de una posición DeFi.

---

## REFERENCIAS

- `LAMC_BOT_POLICY_IA_INSTRUCTIONS.md` — Las 10 reglas que inspiraron este estándar
- `LAMC_Incident_Transitional_Policy_v4_2_2.md` — Políticas SS20 derivadas del incidente
- `LAMC_Master_Architecture_Document.md` — Política de secretos y arquitectura

> **NOTA SOBRE LAS FUENTES 2026-09-25:** estos tres documentos son **documentos internos
> del operador y NO se publican** en este paquete. Se citan porque son la fuente real del
> estándar y del incidente, pero **un verificador externo no puede abrirlos ni
> comprobarlos**: ese tramo de la trazabilidad es `UNKNOWN` para un tercero. Se conservan
> las citas y se declara su límite en vez de esconderlo.

---

## ERRATA 2026-09-25

Cambios de forma de esta revisión, todos verificables con `grep`:

1. **Carácter corrupto corregido.** El ítem 9.3 tenía dos ideogramas chinos (U+7EC8 y
   U+6B62) incrustados dentro de la palabra «terminar», en la frase «al terminar relación
   comercial». Se han eliminado. Barrido completo de P3: era el único carácter no latino
   ajeno al español.
2. **Capitalización corregida.** El título de la sección 7 decía `SUPERFICIE DE ATaque`;
   ahora dice `SUPERFICIE DE ATAQUE`.
3. **Comando de credenciales unificado.** Los ítems 3.1 y 10.7 usaban
   `grep -rE "...\|token\|..."`: en expresiones regulares extendidas `\|` NO es alternancia,
   sino el carácter `|` literal, así que el comando no comprobaba lo que decía. Ahora hay
   **un solo** comando canónico, con `|` sin escapar y buscando un **valor** entrecomillado,
   en §VALIDACIÓN paso 4 (idéntico al de `CHARTER.md` §6 y `RESUMEN.md`). Las celdas de
   3.1 y 10.7 apuntan a él en vez de repetirlo: un `|` sin escapar dentro de una celda
   rompería la tabla de Markdown.

---

*Estándar generado por el equipo del proyecto P3 — cada ítem es binario y verificable —
revisado 2026-09-25.*
