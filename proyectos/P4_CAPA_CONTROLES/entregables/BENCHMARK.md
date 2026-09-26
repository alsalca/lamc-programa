# BENCHMARK DE CONTROLES — P4_CAPA_CONTROLES

**Fecha de medición:** 2026-09-25
**Estándar aplicado:** `proyectos/P3_OPS_SEC/entregables/STANDARD.md` (52 ítems)
**Muestra:** Aave · Uniswap · Liquity (V1) — ver `PROTOCOLOS.md`

> **Este benchmark NO afirma que un protocolo sea «con controles verificables» que otro.**
> Comunica, ítem a ítem contra el estándar de P3, qué controles tienen **evidencia
> pública de estar presentes (`✓`)** o **ausentes (`✗`)** en la medición, y cuáles **no se
> pudieron observar desde fuentes públicas (`?` = UNKNOWN)** porque son operaciones
> internas. Un `?` NO es un `✓` oculto (axioma A3).
>
> **Y no es una auditoría ni una certificación.** No mide seguridad, no opina sobre la
> calidad de ningún protocolo y **no acusa a nadie**: un `✗` solo se marca cuando hay
> **evidencia pública de que el control NO se cumple**, nunca cuando simplemente no se
> pudo ver. Cada marca se puede comprobar en los enlaces citados en `bundle/evidence.md`, y
> **si alguien encuentra un error, se corrige y se dice** — así se corrigió el `✗` de
> Uniswap §10.3 el 2026-09-26, que nuestra propia evidencia desmentía.

## Leyenda

| Marca | Significado |
|---|---|
| ✅ | Hay evidencia pública de que el control **se cumple** |
| ❌ | Hay evidencia pública de que el control **no se cumple** |
| ? | **UNKNOWN** — no observable desde fuentes públicas en esta medición |
| ➖ | **No aplica** — el control no aplica a la estructura del protocolo |

## Resumen

| Protocolo | ✅ presente | ❌ ausente | ? UNKNOWN | ➖ no aplica | Total |
|---|---:|---:|---:|---:|---:|
| Aave | 5 | 1 | 46 | 0 | 52 |
| Uniswap | 4 | 0 | 48 | 0 | 52 |
| Liquity | 5 | 0 | 39 | 8 | 52 |

## Detalle ítem a ítem

### §1 — Custodia de claves

| # | Control (estándar P3) | Aave | Uniswap | Liquity |
|---|---|---:|---:|---:|
| 1.1 | Claves de wallets >1 ETH en hardware wallet | ? | ? | ➖ |
| 1.2 | Seed phrase en ubicación separada y material resistente | ? | ? | ➖ |
| 1.3 | Proceso de recuperación documentado | ? | ? | ➖ |
| 1.4 | Sin claves en texto plano/clipboard/mensajería | ? | ? | ➖ |
| | Subtotal | ✅0 ❌0 ?4 ➖0 | ✅0 ❌0 ?4 ➖0 | ✅0 ❌0 ?0 ➖4 |

### §2 — Multisig

| # | Control (estándar P3) | Aave | Uniswap | Liquity |
|---|---|---:|---:|---:|
| 2.1 | Fondos >10 ETH en multisig mínimo 2-de-3 | ✅ | ? | ➖ |
| 2.2 | Firmantes en dispositivos/ubicaciones separadas | ? | ? | ➖ |
| 2.3 | Verificación fuera de banda | ? | ? | ➖ |
| 2.4 | Proceso de revocación de firmante <180 días | ? | ? | ➖ |
| | Subtotal | ✅1 ❌0 ?3 ➖0 | ✅0 ❌0 ?4 ➖0 | ✅0 ❌0 ?0 ➖4 |

### §3 — Secretos

| # | Control (estándar P3) | Aave | Uniswap | Liquity |
|---|---|---:|---:|---:|
| 3.1 | Sin API key/token/secreto en código o docs públicas | ✅ | ✅ | ✅ |
| 3.2 | Secretos en gestor dedicado | ? | ? | ? |
| 3.3 | Permisos 600 en archivos de secretos | ? | ? | ? |
| 3.4 | Rotación de secretos documentada ≤90 días | ? | ? | ? |
| 3.5 | Sin secretos en logs/errores | ? | ? | ? |
| | Subtotal | ✅1 ❌0 ?4 ➖0 | ✅1 ❌0 ?4 ➖0 | ✅1 ❌0 ?4 ➖0 |

### §4 — Backups

| # | Control (estándar P3) | Aave | Uniswap | Liquity |
|---|---|---:|---:|---:|
| 4.1 | Backup automático ≤24h | ? | ? | ? |
| 4.2 | Backup en ubicación física diferente | ? | ? | ? |
| 4.3 | Backup offline/air-gapped | ? | ? | ? |
| 4.4 | Verificación de integridad semanal | ? | ? | ? |
| 4.5 | Restore probado <180 días | ? | ? | ? |
| 4.6 | Backups cifrados AES-256 | ? | ? | ? |
| | Subtotal | ✅0 ❌0 ?6 ➖0 | ✅0 ❌0 ?6 ➖0 | ✅0 ❌0 ?6 ➖0 |

### §5 — Base de datos

| # | Control (estándar P3) | Aave | Uniswap | Liquity |
|---|---|---:|---:|---:|
| 5.1 | SQLite en WAL mode | ? | ? | ? |
| 5.2 | Integrity check diario | ? | ? | ? |
| 5.3 | Backup antes de migraciones | ? | ? | ? |
| 5.4 | Monitoreo de tamaño con alertas | ? | ? | ? |
| 5.5 | Sin acceso directo a DB desde dev | ? | ? | ? |
| | Subtotal | ✅0 ❌0 ?5 ➖0 | ✅0 ❌0 ?5 ➖0 | ✅0 ❌0 ?5 ➖0 |

### §6 — Observabilidad

| # | Control (estándar P3) | Aave | Uniswap | Liquity |
|---|---|---:|---:|---:|
| 6.1 | Sistema de monitoreo operativo y verificable externamente | ✅ | ✅ | ✅ |
| 6.2 | Alertas: caída, latencia>500ms, disco>80% | ? | ? | ? |
| 6.3 | Logs de seguridad retenidos ≥90 días | ? | ? | ? |
| 6.4 | Dashboard de salud visible | ? | ? | ? |
| 6.5 | Monitoreo de integridad filesystem/SMART | ? | ? | ? |
| 6.6 | Logs separados por servicio | ? | ? | ? |
| | Subtotal | ✅1 ❌0 ?5 ➖0 | ✅1 ❌0 ?5 ➖0 | ✅1 ❌0 ?5 ➖0 |

### §7 — Superficie de ataque

| # | Control (estándar P3) | Aave | Uniswap | Liquity |
|---|---|---:|---:|---:|
| 7.1 | Superficie de red expuesta mínima | ? | ? | ? |
| 7.2 | Separación PROD/LAB | ? | ? | ? |
| 7.3 | Sin experimentos en producción | ? | ? | ? |
| 7.4 | Servicios dev sin exposición a internet | ? | ? | ? |
| 7.5 | Allowlist IPs administrativas | ? | ? | ? |
| | Subtotal | ✅0 ❌0 ?5 ➖0 | ✅0 ❌0 ?5 ➖0 | ✅0 ❌0 ?5 ➖0 |

### §8 — Recovery

| # | Control (estándar P3) | Aave | Uniswap | Liquity |
|---|---|---:|---:|---:|
| 8.1 | RTO declarado por servicio | ? | ? | ? |
| 8.2 | Runbook paso a paso | ? | ? | ? |
| 8.3 | Drill de recovery <180 días | ? | ? | ? |
| 8.4 | Infraestructura reproducible | ? | ? | ? |
| 8.5 | Proceso de recuperación de admin comprometido | ? | ? | ? |
| | Subtotal | ✅0 ❌0 ?5 ➖0 | ✅0 ❌0 ?5 ➖0 | ✅0 ❌0 ?5 ➖0 |

### §9 — Terceros

| # | Control (estándar P3) | Aave | Uniswap | Liquity |
|---|---|---:|---:|---:|
| 9.1 | Inventario de proveedores críticos | ? | ? | ? |
| 9.2 | Proceso de soporte documentado | ? | ? | ? |
| 9.3 | Revocación de accesos a terceros | ? | ? | ? |
| 9.4 | Sin dependencia de un único proveedor (SPOF) | ❌ | ✅ | ✅ |
| 9.5 | Revisión trimestral de permisos | ? | ? | ? |
| | Subtotal | ✅0 ❌1 ?4 ➖0 | ✅1 ❌0 ?4 ➖0 | ✅1 ❌0 ?4 ➖0 |

### §10 — Higiene operacional

| # | Control (estándar P3) | Aave | Uniswap | Liquity |
|---|---|---:|---:|---:|
| 10.1 | Zero-trust en desarrollo | ? | ? | ? |
| 10.2 | Sin scripts de fuentes desconocidas | ? | ? | ? |
| 10.3 | Gestión de dependencias | ✅ | ? | ✅ |
| 10.4 | Cifrado de disco en dispositivos admin | ? | ? | ? |
| 10.5 | Política de contraseñas ≥16 caracteres | ? | ? | ? |
| 10.6 | Review de seguridad antes de despliegue | ? | ? | ? |
| 10.7 | Sin credenciales hardcodeadas (post-remediación) | ✅ | ✅ | ✅ |
| | Subtotal | ✅2 ❌0 ?5 ➖0 | ✅1 ❌0 ?6 ➖0 | ✅2 ❌0 ?5 ➖0 |

## Interpretación

- La mayoría de los ítems de las secciones §4 (Backups), §5 (Base de datos), §6.2-6.6,
  §7, §8 y partes de §1/§2/§3/§9/§10 miden **operación interna** (custodia física de
  claves, backups, WAL de la base de datos, retención de logs, RTO, drill). Un tercero sin
  acceso interno no puede verificarlos desde fuentes públicas, por eso valen `? (UNKNOWN)`.
- Eso **no** significa que el control falte: es el límite honesto del acceso público (A1/A3).
- Los controles verificables públicamente (secretos en repositorios, superficie de
  monitorización pública, esquema de gobernanza/multisig on-chain, gestión de dependencias,
  dependencia de proveedores) son los que admiten `✓`/`✗` en esta medición.

*Benchmark generado por quien construye el entregable — 2026-09-25. La interpretación de estos resultados es del lector.*