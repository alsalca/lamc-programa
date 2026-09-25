# ESTÁNDAR DE SEGURIDAD OPERACIONAL PARA POSICIONES DeFi

**Versión:** 1.0.0
**Fecha:** 2026-09-21
**Proyecto:** P3_OPS_SEC — LAMC Program
**Estado:** Pre-publicación (requiere HG-002)

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
| 3.1 | `- [ ]` Ningún API key, token, o secreto de producción aparece en código fuente, repositorio, o documentación pública | Búsqueda en repo: `grep -rE "api[_-]?key\|token\|secret" --include="*.py" --include="*.js" --include="*.md"` |
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

## 7. SUPERFICIE DE ATaque

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
| 9.3 | `- [ ]` Existe proceso de revocación de accesos a terceros al终止ar relación comercial | Procedimiento documentado |
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
| 10.7 | `- [ ]` No hay credenciales hardcodeadas en ningún archivo del sistema (post-remediación) | `grep -rE "(api[_-]?key\|token\|secret\|password)\s*[:=]\s*['\"][A-Za-z0-9_.:-]{12,}" . && echo "FUGA" \|\| echo "OK"` |

---

## VALIDACIÓN

### Paso 1: Formato binario
```bash
grep -c "^- \[ \]" STANDARD.md
# Resultado esperado: ≥50 (número de ítems del estándar)
```

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

---

*Estándar generado por quien construye el entregable P3 — cada ítem es binario y verificable.*
