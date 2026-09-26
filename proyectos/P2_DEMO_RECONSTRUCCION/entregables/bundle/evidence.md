# Evidence log

## Common capture rules

- Subject: Aave DAO AHAB Safe, `0xAA2461f0f0A3dE5fEAF3273eAe16DEF861cf594e`.
- Historical RPC provider: `https://gateway.tenderly.co/public/<chain>`.
- All calls use a fixed block tag, never `latest`.
- Selector: `getUserAccountData(address)` = `0xbf92857c`.
- Selector: `balanceOf(address)` = `0x70a08231`.
- Raw artifact: public-chain state. Every figure below is reproducible from the chain, the
  pinned block and the full `eth_call` given in its own section, against the public endpoint
  shown there. No local file is part of this bundle.
- Block hashes used as `evidence_hash` (`SPEC.md` §4.5, on-chain case; the real algorithm of
  an Ethereum/Base block is Keccak-256, hence the `keccak256:` label), obtained with
  `eth_getBlockByNumber`:
  - Ethereum mainnet block `26040185` (`0x18d5779`):
    `keccak256:a5cb9576ce5b2cd9aba82b3c3d63c55be665c67bd2b755a46e8f6b48b7f75ff1`
    (node hash `0xa5cb9576ce5b2cd9aba82b3c3d63c55be665c67bd2b755a46e8f6b48b7f75ff1`).
  - Base mainnet block `51691143` (`0x314be87`):
    `keccak256:d83564d839fd5d816f8a7bb2e20de94bf4d098628fa6787817ca33ecffd71c6e`
    (node hash `0xd83564d839fd5d816f8a7bb2e20de94bf4d098628fa6787817ca33ecffd71c6e`).
  - Ficha `LAMC-P2-2026-0007` is documentary and cites no block: its `evidence_hash` remains
    `UNKNOWN` with reason.

### Aave aggregate return (6 words, ABI-encoded)

1. `totalCollateralBase` (8 decimals)
2. `totalDebtBase` (8 decimals)
3. `availableBorrowsBase` (8 decimals)
4. `currentLiquidationThreshold` (bps)
5. `ltv` (bps)
6. `healthFactor` (1e18 scale); sentinel `2^256-1` when debt is zero.

---

## Ethereum — Aave account data

- Chain ID: `1` · Block: `26040185` (`0x18d5779`)
- Block hash (`evidence_hash`): `keccak256:a5cb9576ce5b2cd9aba82b3c3d63c55be665c67bd2b755a46e8f6b48b7f75ff1`
- Pool: `0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2`

```bash
curl -sL --max-time 30 -X POST \
  -H 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","id":1,"method":"eth_call","params":[{"to":"0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2","data":"0xbf92857c000000000000000000000000aa2461f0f0a3de5feaf3273eae16def861cf594e"},"0x18d5779"]}' \
  https://gateway.tenderly.co/public/mainnet
```

- collateral: `2478369141188199 / 1e8 = 24783691.41188199`
- debt: `236983779237062 / 1e8 = 2369837.79237062`
- liquidation threshold: `8267 / 100 = 82.67%`
- LTV: `8016 / 100 = 80.16%`
- HF: `8645875032933278749 / 1e18 = 8.64587503293328`

HF applies: debt is non-zero at this block.

---

## Base — Aave account data

- Chain ID: `8453` · Block: `51691143` (`0x314be87`)
- Block hash (`evidence_hash`): `keccak256:d83564d839fd5d816f8a7bb2e20de94bf4d098628fa6787817ca33ecffd71c6e`
- Pool: `0xA238Dd80C259a72e81d7e4664a9801593F98d1c5`

```bash
curl -sL --max-time 30 -X POST \
  -H 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","id":1,"method":"eth_call","params":[{"to":"0xA238Dd80C259a72e81d7e4664a9801593F98d1c5","data":"0xbf92857c000000000000000000000000aa2461f0f0a3de5feaf3273eae16def861cf594e"},"0x314be87"]}' \
  https://gateway.tenderly.co/public/base
```

- collateral: `1498587931525 / 1e8 = 14985.87931525`
- debt: `0`
- raw HF: `2^256 - 1`

**HF does not apply.** Debt is zero; Aave returns the uint256 maximum sentinel. The raw integer is not published as a financial HF. The record declares `quantity = UNKNOWN` with reason.

---

## Ethereum — rETH holding

- Target: `0xae78736Cd615f374D3085123A210448E74Fc6393`
- Block: `26040185` (`0x18d5779`)
- Block hash (`evidence_hash`): `keccak256:a5cb9576ce5b2cd9aba82b3c3d63c55be665c67bd2b755a46e8f6b48b7f75ff1`

```bash
curl -sL --max-time 30 -X POST \
  -H 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","id":1,"method":"eth_call","params":[{"to":"0xae78736Cd615f374D3085123A210448E74Fc6393","data":"0x70a08231000000000000000000000000aa2461f0f0a3de5feaf3273eae16def861cf594e"},"0x18d5779"]}' \
  https://gateway.tenderly.co/public/mainnet
```

Decoded (18 decimals): `51628217546317516669 / 1e18 = 51.628217546317516669` rETH. Recorded as a token holding; no Rocket Pool deposit is asserted.

---

## Ethereum — wstETH direct check

- Target: `0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0`
- Block: `26040185` (`0x18d5779`)
- Block hash (`evidence_hash`): `keccak256:a5cb9576ce5b2cd9aba82b3c3d63c55be665c67bd2b755a46e8f6b48b7f75ff1`

Same `balanceOf` call pattern. Result: measured zero. No direct Lido position is asserted.

---

## Institutional publication record

- Source: https://github.com/bgd-labs/aave-address-book/blob/dd8bd67401e9c656061c0ac4dff777da25bca884/src/MiscEthereum.sol (commit `dd8bd67401e9c656061c0ac4dff777da25bca884`)
- Constant: `AHAB_SAFE = 0xAA2461f0f0A3dE5fEAF3273eAe16DEF861cf594e`

That record establishes the public entity/address relationship. It does not establish a balance; its `quantity` is therefore `UNKNOWN`.

> **CORRECCIÓN 2026-09-26:** esta sección citaba la rama `blob/main`, que se mueve. La ficha `LAMC-P2-2026-0007` ya fija la referencia al commit `dd8bd67401e9c656061c0ac4dff777da25bca884`; esta sección se alinea con la ficha.

---

## Nota de conformidad — `instrument.label`

La ficha `LAMC-P2-2026-0007` llevaba `instrument.label: "PUBLICATION_OF_ENTITY_ADDRESS"`, un texto libre dentro del objeto
`instrument`. **El contrato no lo admite**: `instrument` declara `additionalProperties: false` y no tiene campo de texto libre, a propósito
(si no se sabe el tipo, el objeto entero vale `UNKNOWN`; no se anota al lado).

El significado no se pierde: la ficha ya lo dice en sus propios campos — `instrument.kind: NONE` (no hay un instrumento separado del contenedor), `source_type: STRUCTURED_EXPORT` y `capture_method` («lectura documental del libro de direcciones publicado por
la organización») —, y el `unknown_reason` de `quantity` explica que el documento establece la relación entidad-dirección, no un saldo.

> **CORRECCIÓN 2026-09-25:** esta ficha llevaba `instrument.kind: OTHER`, un valor que el contrato no admite. Se corrigió a `NONE`: la afirmación es sobre la relación entidad-dirección publicada, no sobre un instrumento separado del contenedor.

> **CORRECCIÓN 2026-09-26:** este párrafo describía la ficha `LAMC-P2-2026-0007` con `source_type: SIGNED_DOCUMENT`, el valor viejo. La ficha ya usa `STRUCTURED_EXPORT` (la fuente es un archivo de código sin firmar y el contrato no tiene un valor dedicado a documento público). Se alinea el texto con la ficha.

---

## Nota de corrección — hash de bloque como `evidence_hash` (misión A4)

Las fichas 0001–0006 declaraban `evidence_hash: "UNKNOWN"` porque solo se había guardado
el número de bloque. **El hash del bloque se puede pedir y el contrato lo admite**
(`SPEC.md` §4.5: en el caso on-chain el hash del bloque **es** un `evidence_hash`
legítimo, etiquetado `keccak256:` porque es su algoritmo real). Dejar `UNKNOWN` un dato
establecible convertía un hueco evitable en una limitación declarada.

Se pidió el hash a un nodo público con `eth_getBlockByNumber` (llamada y respuesta
reproducibles en la tabla de abajo) y se escribió en cada ficha:

| Fichas | Cadena | Bloque | Hash del nodo | `evidence_hash` en la ficha |
|:---|:---|:---|:---|:---|
| 0001, 0002, 0003, 0006 | Ethereum mainnet | `26040185` (`0x18d5779`) | `0xa5cb9576ce5b2cd9aba82b3c3d63c55be665c67bd2b755a46e8f6b48b7f75ff1` | `keccak256:a5cb9576ce5b2cd9aba82b3c3d63c55be665c67bd2b755a46e8f6b48b7f75ff1` |
| 0004, 0005 | Base mainnet | `51691143` (`0x314be87`) | `0xd83564d839fd5d816f8a7bb2e20de94bf4d098628fa6787817ca33ecffd71c6e` | `keccak256:d83564d839fd5d816f8a7bb2e20de94bf4d098628fa6787817ca33ecffd71c6e` |

Llamadas exactas:

```bash
# Ethereum mainnet — bloque 26040185 (0x18d5779)
curl -s --max-time 30 -X POST -H 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["0x18d5779",false],"id":1}' \
  https://ethereum-rpc.publicnode.com
# -> "number":"0x18d5779", "hash":"0xa5cb9576ce5b2cd9aba82b3c3d63c55be665c67bd2b755a46e8f6b48b7f75ff1"

# Base mainnet — bloque 51691143 (0x314be87)
curl -s --max-time 30 -X POST -H 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["0x314be87",false],"id":1}' \
  https://base-rpc.publicnode.com
# -> "number":"0x314be87", "hash":"0xd83564d839fd5d816f8a7bb2e20de94bf4d098628fa6787817ca33ecffd71c6e"
```

El mismo hash de Ethereum se obtuvo también en `https://gateway.tenderly.co/public/mainnet`
y `https://eth.drpc.org`, y el de Base en `https://gateway.tenderly.co/public/base`
(consenso, no una respuesta aislada de un proveedor).

En esas seis fichas `evidence_hash` pasó de `unknown` a `known` y su motivo se retiró de
`unknown_reason`. La ficha **0007** no se toca: es documental, no cita ningún bloque y su
hueco de hash sigue siendo legítimo. El cambio se copió idéntico al ledger de P8 en el
mismo acto.
