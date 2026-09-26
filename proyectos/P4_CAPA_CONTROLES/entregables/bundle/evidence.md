# MAPA DE EVIDENCIA — Bench P4_CAPA_CONTROLES

**Fecha de medición:** 2026-09-25
**Estándar aplicado:** `proyectos/P3_OPS_SEC/entregables/STANDARD.md` (52 ítems)
**Muestra:** Aave · Uniswap · Liquity (V1)
**Regla:** cada control marcado `✓`/`✗` en `BENCHMARK.md` se sostiene con **una o más fuentes públicas** citadas abajo, verificables por un tercero. Lo no publicamente observable es `UNKNOWN` (ver `unknowns.md`).

---

## Convención aplicada a §3.1 y §10.7 (reproducible)

El estándar §3.1 habla de "**secreto de producción**" y §10.7 de "credenciales hardcodeadas (post-remediación)". Para una medición reproducible se fija esta definición:

- **Control `✓` (presente)** = en HEAD de los repositorios inspeccionados **no hay una clave de producción / alto valor** (private key, token de servidor, API key no-`NEXT_PUBLIC_`, password).
- **Claves cliente-públicas (`NEXT_PUBLIC_*`), IDs públicos de proyecto (WalletConnect) y claves de licencia commiteadas por diseño** NO se consideran "secreto de producción". Se documentan como **hallazgo de transparencia** en `unknowns.md`, pero no marcan el control ausente.

Esta misma regla se aplica a los tres protocolos por igual. Cualquier revisor que desee una tolerancia distinta (p. ej. "que un escáner automático no dispare NINGÚN patrón") debe anotarla y obtendría un veredicto distinto; se declara explícitamente para que el benchmark sea repetible.

---

## EVIDENCIA POR PROTOCOLO Y CONTROLES QUE LA USAN

### AVAA / AAVE DAO

| Control | Veredicto | Fuente(s) pública(s) |
|---|---|---|
| §2.1 | ✅ presente | ARFC governance forum "June - Update Signers and SAFE Configuration" (2026-06-02, TokenLogic) documenta 7 SAFEs de tesorería 2-of-3 y SAFEs operacionales 2-of-5/3-of-5: https://governance.aave.com/t/arfc-june-update-signers-and-safe-configuration/25023 · Página de seguridad: "Community Guardian: 5-of-9 community multisig": https://aave.com/security · Safe on-chain "Aave: Team Gnosis Safe": https://etherscan.io/address/0x4a75f0ae51a5d616ada4db52be140d89302aaf78 · Índice de permisos: https://github.com/aave-dao/aave-permissions-book |
| §3.1 | ✅ presente (sin secreto de producción) | Grep sobre `.env`/`.env.example` a HEAD: aave-ui/.env → https://raw.githubusercontent.com/aave/aave-ui/master/.env · aave-v4/.env.example → https://raw.githubusercontent.com/aave/aave-v4/main/.env.example · aave-dao/seatbelt-gov-v3/.env.example → https://raw.githubusercontent.com/aave-dao/seatbelt-gov-v3/main/.env.example · aave/protocol-subgraphs/.env.test. **Hallazgo de transparencia:** `aave/interface/.env.example` (HEAD) contiene dos `NEXT_PUBLIC_*` client-keys con formato real (Transak, Amplitude) — ver https://raw.githubusercontent.com/aave/interface/main/.env.example y `unknowns.md`. |
| §6.1 | ✅ presente | Subgraphs públicos en The Graph + API pública aave-api-v2: repo https://github.com/aave/protocol-subgraphs (README lista endpoints, p. ej. https://thegraph.com/explorer/subgraphs/Cd2gEDVeqnjBn1hSeqFMitw8Q1iiyV9FYUZkLNRcL87g) · API https://aave-api-v2.aave.com/data/rates-history |
| §9.4 | ❌ ausente (proveedor único) | AaveOracle usa Chainlink como fuente primaria: https://raw.githubusercontent.com/aave/aave-v3-core/master/contracts/misc/AaveOracle.sol ("Use of Chainlink Aggregators as first source of price") · Docs https://aave.com/docs/ecosystem/oracle · Fallback oracle desactivado (address(0)): propuesta #351 https://governance-v2.aave.com/governance/proposal/351/ y hilo BGD "Operational Oracles update" https://governance.aave.com/t/bgd-operational-oracles-update/13213 |
| §10.3 | ✅ presente | Dependabot: https://raw.githubusercontent.com/aave/aave-ui/master/.github/dependabot.yml (npm weekly) · https://raw.githubusercontent.com/aave-dao/seatbelt-gov-v3/main/.github/dependabot.yml · Dependency Review en CI: https://raw.githubusercontent.com/aave/aave-v4/main/.github/workflows/dependency-review.yml |
| §10.7 | ✅ presente (sin secretos de producción a HEAD) | Mismo grep que §3.1. **Hallazgo de transparencia:** mismas dos claves `NEXT_PUBLIC_*` client-keys de `interface/.env.example` (ver §3.1 y `unknowns.md`). |

---

### UNISWAP / UNISWAP DAO

| Control | Veredicto | Fuente(s) pública(s) |
|---|---|---|
| §2.1 | ? UNKNOWN | La tesorería (~US$2.57B "Token Holdings") está bajo un **timelock gobernado por la DAO** (voto on-chain con quórum), NO bajo un multisig 2-de-3 clásico. No hay evidencia pública de un multisig con firmantes concreto. Referencias técnicas públicas: https://developers.uniswap.org/docs/ecosystem/governance/technical-reference · Timelock on-chain: https://etherscan.io/address/0x1a9C8182C09F50C8318d769245beA52c32BE35BC · GovernorBravo 0x408ED6354d4973f66138C91495F2f2FCbd8724C3. Al no verificarse el **esquema multisig 2-de-3 que exige el estándar**, se declara UNKNOWN (esquema distinto), no presente. |
| §3.1 | ✅ presente (sin secreto de producción) | No hay `.env` con secretos reales a HEAD en v3-core/v3-periphery/v4-core/docs/interface. v4-core `.env` commiteado contiene solo `FOUNDRY_FUZZ_SEED=0x4444` (semilla de test, no credencial). Configs usan `${{ secrets.* }}` / `process.env.*`. **Hallazgo de transparencia:** `interface/.nx/key/key.ini` (clave de licencia Nx Cloud, commiteda por diseño) y `walletConnectProjectId` público. Limitación: barrido en repos/fichas inspeccionados (docs 213MB, interface 410MB con rate-limit del listado total). |
| §6.1 | ✅ presente | Status page pública: https://status.uniswap.org → https://statuspage.incident.io/uniswap-status ("fully operational"; componentes Developer Portal, API, UniswapX, Unichain) · API docs https://developers.uniswap.org/docs/get-started/quickstart · Subgraphs públicos The Graph v1/v2/v3/v4: https://developers.uniswap.org/docs/ecosystem/subgraphs/overview |
| §9.4 | ✅ presente (múltiples proveedores documentados) | Oracles v3 TWAP built-in; v4 sin oracle built-in; Unichain documenta oráculos Api3, Pyth, RedStone y Chainlink Data Feeds: https://developers.uniswap.org/docs/unichain/tools/oracles y https://developers.uniswap.org/docs/unichain/tools/data-feeds · RPC Unichain: Alchemy, Blockdaemon, Chainstack, dRPC, Dwellir, Infura, QuickNode, OnFinality: https://developers.uniswap.org/docs/unichain/tools/node-providers · Indexing: The Graph, Goldsky, Allium, GhostGraph |
| §10.3 | **? UNKNOWN** (no observable desde el repositorio público) | No hay `.github/dependabot.yml` ni `renovate.json` commiteados a HEAD en v3-core / v3-periphery / v4-core / interface / docs (sondas raw → 404 a HEAD), ni workflow de dependency-review visible. **Pero hay evidencia indirecta de que el proceso SÍ existe**: Dependabot aparece activo por ajustes de la organización (dependabot.ecosyste.ms). **No se puede observar la configuración desde el repositorio público, y eso no es lo mismo que no tenerla** (axioma A3). Antes decía `❌ ausente`: era una afirmación que nuestra propia evidencia desmentía. |
| §10.7 | ✅ presente (sin credenciales de producción a HEAD) | Mismo escaneo que §3.1. **Hallazgo de transparencia:** `interface/.nx/key/key.ini` — clave RSA de licencia Nx Cloud que el `.gitignore` re-incluye a propósito (no es credencial/API). Sin `pk_live_/sk_live_`, private keys ni API keys reales. |

---

### LIQUITY (V1)

| Control | Veredicto | Fuente(s) pública(s) |
|---|---|---|
| §1.1–1.4 | ➖ no aplica | Protocolo inmutable y governance-free, sin llaves de administración: https://www.liquity.org/features/governance-free ("no admin key… completely immutable") · Blog oficial: https://www.liquity.org/blog/price-oracles-in-liquity ("immutable and governance-free… set in stone") · Mecanismo on-chain `_renounceOwnership()` en setAddresses de contratos Ownable: https://github.com/liquity/dev/blob/main/packages/contracts/contracts/TroveManager.sol (mismo patrón en StabilityPool, PriceFeed) · Contratos desplegados no-proxy y verificados en Etherscan: TroveManager 0xA39739EF8b0231DbFA0DcdA07d7e29faAbCf4bb2 (https://etherscan.io/address/0xA39739EF8b0231DbFA0DcdA07d7e29faAbCf4bb2) · Audit independiente público (Trail of Bits). |
| §2.1–2.4 | ➖ no aplica | Mismo fundamento que §1: no hay claves de propietario ni esquema multisig de DAO que custodiar (contratos no-upgradeable y sin owner tras renounceOwnership). |
| §3.1 | ✅ presente (sin secreto de producción) | Repos de la org github.com/liquity (V1 monorepo `liquity/dev`) a HEAD: solo placeholders — packages/contracts/secrets.js.template (valores `undefined`), packages/lib-ethers/.env.sample. **Hallazgo de transparencia:** `walletConnectProjectId` público (client ID) en dev-frontend config — ver https://github.com/liquity/dev/blob/main/packages/dev-frontend/src/config/index.ts y `unknowns.md`. |
| §6.1 | ✅ presente | Subgraph público `liquity/liquity` en The Graph: https://github.com/liquity/dev/blob/main/packages/subgraph/package.json · herramienta CR monitor pública: https://github.com/liquity/cr-monitor · estado on-chain sin autenticación (TCR, base rate, price feed en contratos públicos). Nota: endpoint hosteado del subgraph migró de api.thegraph.com; la URL live actual se declara UNKNOWN. |
| §9.4 | ✅ presente (estructura observable) | Chainlink ETH/USD como oráculo primario: https://www.liquity.org/blog/liquity-integrates-leading-oracle-network-chainlink · Tellor como oráculo secundario/fallback: https://www.liquity.org/blog/price-oracles-in-liquity · Código PriceFeed.sol con lógica Chainlink+Tellor: https://github.com/liquity/dev/blob/main/packages/contracts/contracts/PriceFeed.sol |
| §10.3 | ✅ presente (Dependabot) | Dependabot config npm daily: https://raw.githubusercontent.com/liquity/dev/main/.github/dependabot.yml. No se halló informe de auditoría de dependencias publicado por separado. |
| §10.7 | ✅ presente (sin credenciales reales a HEAD) | Ver §3.1. **Hallazgo de transparencia:** el único literal credential-shaped es `walletConnectProjectId` público (client ID de WalletConnect), no un secreto. |

---

## NOTA METODOLÓGICA SOBRE ALCANCE DEL GREP DE SECRETOS

- Aave: se inspeccionaron a profundidad los repos nucleares (.env y .env.example de aave-ui, aave-v4, seatbelt-gov-v3, protocol-subgraphs, interface) y 34 de 153 repos públicos de la org. ~119 repos no se barrieron (limitación de code-search). Una credencial podría existir en un repo no inspeccionado → es **UNKNOWN no cubierto**, declarado en `unknowns.md`.
- Uniswap: barrido directo de archivos de alto valor en v3-core/v3-periphery/v4-core/docs/interface; rate-limit del listado total de docs e interface. El veredicto "sin credenciales" aplica a los repos/fichas inspeccionados.
- Liquity: barrido del monorepo `liquity/dev` a HEAD.

**Estas limitaciones NO se ocultan:** se reportan como alcance del grep en esta medición (A1/A3).

---

*Mapa de evidencia generado por quien construye el entregable — 2026-09-25. Cada `✓`/`✗` es reproducible desde las URLs citadas.*

---

## Procedencia por ficha

> Estas notas estaban dentro del JSON, en una clave `_meta` que viajaba
> **dentro de cada ficha**. El contrato no la admite (`additionalProperties: false`),
> así que las fichas no validaban contra su propio esquema. El contenido es el mismo,
> y aquí —al lado de la evidencia— se lee mejor.

### `P4-CTRL-2026-0001`

- **protocolo** — Aave
- **fecha_medicion** — 2026-09-25
- **metodo** — Aplicación del estándar P3 (52 ítems, proyectos/P3_OPS_SEC/entregables/STANDARD.md) desde acceso público únicamente. Cada ítem marcado presente/ausente/unknown/no_aplica según evidencia pública citada en bundle/evidence.md. Benchmark binario: solo dice qué controles están presentes/ausentes/sin-observar; no afirma que un protocolo sea con controles verificables que otro.
- **controles** — {"presente": 5, "ausente": 1, "unknown": 46, "no_aplica": 0, "total": 52}

### `P4-CTRL-2026-0002`

- **protocolo** — Uniswap
- **fecha_medicion** — 2026-09-25
- **metodo** — Aplicación del estándar P3 (52 ítems, proyectos/P3_OPS_SEC/entregables/STANDARD.md) desde acceso público únicamente. Cada ítem marcado presente/ausente/unknown/no_aplica según evidencia pública citada en bundle/evidence.md. Benchmark binario: solo dice qué controles están presentes/ausentes/sin-observar; no afirma que un protocolo sea con controles verificables que otro.
- **controles** — {"presente": 4, "ausente": 0, "unknown": 48, "no_aplica": 0, "total": 52}

### `P4-CTRL-2026-0003`

- **protocolo** — Liquity
- **fecha_medicion** — 2026-09-25
- **metodo** — Aplicación del estándar P3 (52 ítems, proyectos/P3_OPS_SEC/entregables/STANDARD.md) desde acceso público únicamente. Cada ítem marcado presente/ausente/unknown/no_aplica según evidencia pública citada en bundle/evidence.md. Benchmark binario: solo dice qué controles están presentes/ausentes/sin-observar; no afirma que un protocolo sea con controles verificables que otro.
- **controles** — {"presente": 5, "ausente": 0, "unknown": 39, "no_aplica": 8, "total": 52}
