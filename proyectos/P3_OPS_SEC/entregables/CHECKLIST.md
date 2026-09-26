# CHECKLIST DE AUDITORÍA — Estándar de Seguridad Operacional DeFi

**Propósito:** Herramienta de verificación rápida para auditar una operación DeFi contra el estándar.
**Uso:** Marcar cada ítem con ✓ (cumple) o ✗ (no cumple). Los ítems sin marcar son UNKNOWN.
**Tiempo estimado de auditoría:** 2-4 horas para una operación completa.

---

## INSTRUCCIONES

1. Para cada ítem, verificar la evidencia solicitada
2. Marcar con ✓ si se cumple, ✗ si no se cumple
3. Dejar sin marcar si no se puede verificar (UNKNOWN)
4. Al final, contar: cada ✗ es una acción correctiva, cada UNKNOWN es un riesgo desconocido
5. **Resultado:** si hay más de 3 ✗ en cualquier sección, la operación NO está lista para producción

---

## 1. CUSTODIA DE CLAVES

| # | Ítem | ✓/✗/? | Evidencia requerida |
|---|------|-------|---------------------|
| 1.1 | `- [ ]` Claves de wallets >1 ETH en hardware wallet | | Dispositivo físico presente y verificado |
| 1.2 | `- [ ]` Seed phrase en ubicación separada, material resistente | | Ubicación verificada |
| 1.3 | `- [ ]` Proceso de recuperación documentado | | Documento disponible y <90 días |
| 1.4 | `- [ ]` Sin claves en texto plano/clipboard/mensajes | | Búsqueda en filesystem |

**Resultado sección 1:** _____ /4 ✓ | _____ ✗ | _____ UNKNOWN

---

## 2. MULTISIG

| # | Ítem | ✓/✗/? | Evidencia requerida |
|---|------|-------|---------------------|
| 2.1 | `- [ ]` Wallets >10 ETH con multisig (2 de 3 mínimo) | | Configuración on-chain |
| 2.2 | `- [ ]` Firmantes en dispositivos/ubicaciones separadas | | Declaración de firmantes |
| 2.3 | `- [ ]` Verificación fuera de banda | | Procedimiento documentado |
| 2.4 | `- [ ]` Proceso de revocación de firmante comprometido | | Documento y drill <180 días |

**Resultado sección 2:** _____ /4 ✓ | _____ ✗ | _____ UNKNOWN

---

## 3. SECRETOS

| # | Ítem | ✓/✗/? | Evidencia requerida |
|---|------|-------|---------------------|
| 3.1 | `- [ ]` Sin secretos en código/repositorio/docs públicas | | `grep` en repo |
| 3.2 | `- [ ]` Secretos en gestor dedicado | | Inspección de configuración |
| 3.3 | `- [ ]` Permisos `600` en archivos de secretos | | `ls -la` |
| 3.4 | `- [ ]` Rotación ≤90 días documentada | | Registro de rotaciones |
| 3.5 | `- [ ]` Sin secretos en logs o errores | | Revisión de logs <30 días |

**Resultado sección 3:** _____ /5 ✓ | _____ ✗ | _____ UNKNOWN

---

## 4. BACKUPS

| # | Ítem | ✓/✗/? | Evidencia requerida |
|---|------|-------|---------------------|
| 4.1 | `- [ ]` Backup automático ≤24 horas | | Cron job verificable |
| 4.2 | `- [ ]` Backup en ubicación diferente | | Rutas verificadas |
| 4.3 | `- [ ]` Backup offline/air-gapped | | Verificación física |
| 4.4 | `- [ ]` Integridad verificada semanalmente | | Registro de checksums |
| 4.5 | `- [ ]` Restore probado <180 días | | Registro de drill |
| 4.6 | `- [ ]` Backups cifrados (AES-256) | | Configuración verificada |

**Resultado sección 4:** _____ /6 ✓ | _____ ✗ | _____ UNKNOWN

---

## 5. BASE DE DATOS

| # | Ítem | ✓/✗/? | Evidencia requerida |
|---|------|-------|---------------------|
| 5.1 | `- [ ]` SQLite en WAL mode | | `PRAGMA journal_mode;` |
| 5.2 | `- [ ]` Integrity check diario | | Registro de ejecución |
| 5.3 | `- [ ]` Backup antes de migraciones | | Script verificado |
| 5.4 | `- [ ]` Monitoreo de tamaño con alertas | | Configuración activa |
| 5.5 | `- [ ]` Sin acceso directo a DB desde dev | | Configuración de permisos |

**Resultado sección 5:** _____ /5 ✓ | _____ ✗ | _____ UNKNOWN

---

## 6. OBSERVABILIDAD

| # | Ítem | ✓/✗/? | Evidencia requerida |
|---|------|-------|---------------------|
| 6.1 | `- [ ]` Sistema de monitoreo operativo | | Endpoint público |
| 6.2 | `- [ ]` Alertas: caída, latencia>500ms, disco>80% | | Configuración revisable |
| 6.3 | `- [ ]` Logs retenidos ≥90 días | | Configuración verificada |
| 6.4 | `- [ ]` Dashboard de salud accesible | | Acceso verificado |
| 6.5 | `- [ ]` Monitoreo de integridad filesystem/SMART | | Configuración activa |
| 6.6 | `- [ ]` Logs separados por servicio | | Estructura verificable |

**Resultado sección 6:** _____ /6 ✓ | _____ ✗ | _____ UNKNOWN

---

## 7. SUPERFICIE DE ATAQUE

| # | Ítem | ✓/✗/? | Evidencia requerida |
|---|------|-------|---------------------|
| 7.1 | `- [ ]` Superficie de red mínima | | Escaneo o firewall |
| 7.2 | `- [ ]` Separación PROD/LAB | | Inspección física/lógica |
| 7.3 | `- [ ]` Sin experimentos en producción | | Política y auditoría |
| 7.4 | `- [ ]` Servicios dev sin exposición a internet | | Configuración de red |
| 7.5 | `- [ ]` Allowlist IPs administrativas | | Configuración firewall/VPN |

**Resultado sección 7:** _____ /5 ✓ | _____ ✗ | _____ UNKNOWN

---

## 8. RECOVERY

| # | Ítem | ✓/✗/? | Evidencia requerida |
|---|------|-------|---------------------|
| 8.1 | `- [ ]` RTO declarado por servicio | | Documento de continuidad |
| 8.2 | `- [ ]` Runbook paso a paso | | Documento actualizado |
| 8.3 | `- [ ]` Drill de recovery <180 días | | Registro con fecha |
| 8.4 | `- [ ]` Infraestructura reproducible | | Documentación/scripts |
| 8.5 | `- [ ]` Proceso de recuperación de admin comprometido | | Documento de escalamiento |

**Resultado sección 8:** _____ /5 ✓ | _____ ✗ | _____ UNKNOWN

---

## 9. TERCEROS

| # | Ítem | ✓/✗/? | Evidencia requerida |
|---|------|-------|---------------------|
| 9.1 | `- [ ]` Inventario de proveedores críticos | | Registro actualizado |
| 9.2 | `- [ ]` Proceso de soporte documentado | | Documento verificado |
| 9.3 | `- [ ]` Revocación de accesos a terceros | | Procedimiento documentado |
| 9.4 | `- [ ]` Sin dependencia single point of failure | | Análisis de dependencias |
| 9.5 | `- [ ]` Revisión trimestral de permisos | | Registro de revisiones |

**Resultado sección 9:** _____ /5 ✓ | _____ ✗ | _____ UNKNOWN

---

## 10. HIGIENE OPERACIONAL

| # | Ítem | ✓/✗/? | Evidencia requerida |
|---|------|-------|---------------------|
| 10.1 | `- [ ]` Zero-trust en desarrollo | | Proceso de code review |
| 10.2 | `- [ ]` Sin scripts de fuentes desconocidas | | Política documentada |
| 10.3 | `- [ ]` Gestión de dependencias | | Registro de auditoría |
| 10.4 | `- [ ]` Cifrado de disco en dispositivos admin | | Verificación |
| 10.5 | `- [ ]` Política de contraseñas ≥16 chars | | Configuración |
| 10.6 | `- [ ]` Review de seguridad antes de despliegue | | Registro de revisiones |
| 10.7 | `- [ ]` Sin credenciales hardcodeadas (post-remediación) | | `grep` de verificación |

**Resultado sección 10:** _____ /7 ✓ | _____ ✗ | _____ UNKNOWN

---

## RESUMEN FINAL

| Sección | ✓ (cumple) | ✗ (no cumple) | ? (UNKNOWN) |
|---------|------------|---------------|-------------|
| 1. Custodia de claves | | | |
| 2. Multisig | | | |
| 3. Secretos | | | |
| 4. Backups | | | |
| 5. Base de datos | | | |
| 6. Observabilidad | | | |
| 7. Superficie de ataque | | | |
| 8. Recovery | | | |
| 9. Terceros | | | |
| 10. Higiene operacional | | | |
| **TOTAL** | **/52** | | |

---

## DECISIÓN

- [ ] **APROBADO:** Todos los ítems marcados ✓, sin ✗ en secciones críticas (1,3,5,8)
- [ ] **CONDICIONAL:** ≤3 ✗ en total, con plan de remediación en <30 días
- [ ] **NO APROBADO:** >3 ✗ o ✗ en secciones críticas — requiere remediación antes de operar

> **NOTA 2026-09-25:** estas 3 casillas son de **decisión**, no de verificación. No cuentan
> como ítems auditables: los ítems de verificación de esta checklist son los **52** de las
> tablas (4+4+5+6+5+6+5+5+5+7), que coinciden con los 52 de `STANDARD.md`. El total de
> casillas de la checklist es 52 + 3 = **55**. El comando `grep -c "^- \[ \]" CHECKLIST.md`
> da 3 porque solo ve estas tres, que no son ítems.

**Auditor:** _________________________
**Fecha:** _________________________
**Operación auditada:** _________________________

---

## NOTA SOBRE UNKNOWN

Los ítems marcados con `?` (UNKNOWN) representan **riesgos no cuantificados**. Según el axioma A3: *"La ausencia de evidencia no constituye evidencia"*. Un UNKNOWN no es un ✓ implícito; es un hueco que debe resolverse.

**UNKNOWN en secciones críticas (1,3,5,8) = BLOCK hasta que se establezca la verificación.**

---

*Checklist generado por quien construye el entregable P3 — herramienta de auditoría binaria.*
