# HUECOS DECLARADOS — P4_CAPA_CONTROLES

**Fecha:** 2026-09-25
**Proyecto:** P4_CAPA_CONTROLES · **Misión M-P4-03**
**Regla:** la ausencia de evidencia NO constituye evidencia (axioma A3). Un `UNKNOWN` es "aún no establecido", no un `✓` implícito ni un fallo.

---

## 1. HUECOS ESTRUCTURALES POR LIMITACIÓN DE ACCESO (los 52 ítems internos)

La mayoría de los controles del estándar de P3 miden **operación interna de la entidad** que
opera el protocolo (custodia física de claves, backups, base de datos, logs, RTO, drills).
Un tercero sin acceso interno **no puede verificarlos desde fuentes públicas**. Por eso valen
`UNKNOWN` en esta medición para los tres protocolos:

| Área (ítems) | Por qué es `UNKNOWN` |
|---|---|
| §1.1–1.3 | Custodia física de claves (hardware wallet, seed phrase, proceso de recuperación): no observable públicamente |
| §2.2–2.4 | Ubicación de firmantes, verificación fuera de banda, drill de revocación: declaraciones internas |
| §3.2–3.4 | Gestor de secretos, permisos `600`, rotación: configuración interna |
| §3.5 | Logs / errores: no públicos |
| §4.1–4.6 | Backups, ubicaciones, air-gap, checksum, restore, cifrado: operación interna |
| §5.1–5.5 | Base de datos (WAL, integrity_check, monitoreo): la DB del operador no es pública |
| §6.2–6.6 | Alertas, retención de logs, dashboard, filesystem/SMART, logs por servicio: configuración interna |
| §7.1–7.5 | Superficie de red interna, separación PROD/LAB, allowlist: infraestructura privada (no se escanea sin autorización) |
| §8.1–8.5 | RTO, runbook, drill, reproducibilidad, escalamiento: procedimientos internos |
| §9.1–9.3, 9.5 | Inventario de proveedores, soporte, revocación, revisión trimestral: registros internos |
| §10.1–10.2, 10.4–10.6 | Zero-trust, scripts, cifrado de disco, contraseñas, review de despliegue: políticas internas |

**Esto NO significa que esos controles falten.** Es el límite honesto del benchmark público.
Un auditor con acceso interno los resolvería; un `UNKNOWN` en secciones críticas es un hueco
que, en el estándar P3, **bloquea** hasta establecerse (CHECKLIST.md §NOTA).

---

## 2. CASOS PARTICULARES DECLARADOS ítem a ítem

| # | Protocolo | Ítem | Estado | Motivo |
|---|---|---|---|---|
| 1 | Uniswap | §2.1 | `UNKNOWN` | La tesorería (~US$2.57B) está bajo **timelock gobernado por voto on-chain de la DAO**, no bajo un multisig 2-de-3 con firmantes concretos. No hay evidencia pública de multisig clásico. El esquema observado difiere del que exige el estándar → no se marca presente ni ausente. |
| 2 | Aave | §9.4 | `AUSENTE` (hallazgo) | Evidencia pública de **proveedor único** de precio (Chainlink) con fallback desactivado (address(0)). El control "sin SPOF" no se cumple según la evidencia pública. Nota: también sería defendible `NO_APLICA` si se exigiera múltiples proveedores; se fijó ausente por el criterio de la escala. |
| 3 | Uniswap | §10.3 | `AUSENTE` (hallazgo) | Sin config de gestión de dependencias commiteda a HEAD (ni dependabot.yml ni renovate.json ni workflow de dependency-review). Se declara ausente en esta medición; Dependabot podría activarse vía ajustes de org (no públicamente verificable). |
| 4 | Liquity | §1, §2 | `NO_APLICA` | Confirmado inmutable y governance-free (sin claves, `renounceOwnership` on-chain, contratos no-proxy). Custodia y multisig no aplican estructuralmente. |
| 5 | Liquity | §6.1 | `PRESENTE` con hueco | El endpoint hosteado del subgraph migró; la URL live actual se declara `UNKNOWN` aunque la superficie pública (subgraph desplegable + estado on-chain) exista. |

---

## 3. HALLAZGOS DE TRANSPARENCIA (grep de secretos — no marcan control ausente)

Bajo la convención fijada en `evidence.md` (§3.1/§10.7 = "sin **secretos de producción**"), estos
literales **NO** se clasifican como credencial de producción; se documentan para que el revisor
aplique su propia tolerancia:

| Protocolo | Literal hallado | Naturaleza | Fuente |
|---|---|---|---|
| Aave | `NEXT_PUBLIC_TRANSAK_API_KEY=799087ea-…` · `NEXT_PUBLIC_AMPLITUDE_API_KEY=6b28cb73…` | claves **cliente-públicas** (`NEXT_PUBLIC_` se expone en el bundle del frontend, por diseño) en `.env.example`; liveness sin confirmar | https://raw.githubusercontent.com/aave/interface/main/.env.example |
| Uniswap | `interface/.nx/key/key.ini` (clave RSA de licencia Nx Cloud) | commiteada **por diseño** (el `.gitignore` la re-incluye con comentario); no es credencial/API | https://raw.githubusercontent.com/Uniswap/interface/main/.nx/key/key.ini |
| Uniswap | `walletConnectProjectId` | ID público de cliente WalletConnect | repos de Uniswap interface |
| Liquity | `walletConnectProjectId: "b16efb4f…"` | ID público de cliente WalletConnect, no secreto | https://github.com/liquity/dev/blob/main/packages/dev-frontend/src/config/index.ts |

**Consecuencia si cambia la tolerancia:** si el criterio del revisor es "que NINGÚN patrón de
escáner dispare", Aave §3.1/§10.7 pasaría a `UNKNOWN` (o `AUSENTE`), y lo mismo valdría revisar
para Uniswap/Liquity. El impacto se limita a §3.1/§10.7 de los tres protocolos.

---

## 4. LIMITACIÓN DEL GREP (declarada, no ocultada)

| Protocolo | Alcance del grep | No cubierto |
|---|---|---|
| Aave | Repos nucleares (aave-ui, aave-v4, seatbelt-gov-v3, protocol-subgraphs, interface) + 34/153 repos de la org | ~119 repos no inspeccionados (code-search GitHub requirió login) |
| Uniswap | Archivos de alto valor de v3-core/v3-periphery/v4-core/docs/interface | Barrido byte-a-byte total de docs (213MB) e interface (410MB) con rate-limit |
| Liquity | Monorepo `liquity/dev` a HEAD | No hay barrido exhaustivo de todos los repos de la org |

Una credencial podría vivir en un repositorio no inspeccionado → es **`UNKNOWN` no cubierto**,
no un resultado oculto.

---

## 5. RESUMEN DE HUECOS POR PROTOCOLO (conteo sobre 52)

| Protocolo | ✅ presente | ❌ ausente | ? UNKNOWN | ➖ no aplica |
|---|---:|---:|---:|---:|
| Aave | 5 | 1 | 46 | 0 |
| Uniswap | 4 | 1 | 47 | 0 |
| Liquity | 5 | 0 | 39 | 8 |

Todos los `UNKNOWN` tienen su motivo asociado (los $46/$47/$39 ítems internos, sección 1).
Ninguno se promovió a `✓` por ausencia de evidencia (A1/A3).

---

*Huecos declarados por quien construye el entregable — 2026-09-25.*