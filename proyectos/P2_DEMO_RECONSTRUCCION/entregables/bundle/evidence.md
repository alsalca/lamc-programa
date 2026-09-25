# Evidence log

## Common capture rules

- Subject: Aave DAO AHAB Safe, `0xAA2461f0f0A3dE5fEAF3273eAe16DEF861cf594e`.
- Historical RPC provider: `https://gateway.tenderly.co/public/<chain>`.
- All calls use a fixed block tag, never `latest`.
- Selector: `getUserAccountData(address)` = `0xbf92857c`.
- Selector: `balanceOf(address)` = `0x70a08231`.
- Raw capture: `/tmp/p2_capture.json`.

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
- Pool: `0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2`

```bash
curl -sL --max-time 30 -X POST \
  -H 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","id":1,"method":"eth_call","params":[{"to":"0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2","data":"0xbf92857c000000000000000000000000aa2461f0f0a3de5feaf3273eae16def861cf594e"},"0x18d5779"]}' \
  https://gateway.tenderly.co/public/mainnet
```

- collateral: `2478369141188199 / 1e8 = 24783691.41188819`
- debt: `236983779237062 / 1e8 = 2369837.79237062`
- liquidation threshold: `8267 / 100 = 82.67%`
- LTV: `8016 / 100 = 80.16%`
- HF: `8645875032933278749 / 1e18 = 8.64587503293328`

HF applies: debt is non-zero at this block.

---

## Base — Aave account data

- Chain ID: `8453` · Block: `51691143` (`0x314be87`)
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

```bash
curl -sL --max-time 30 -X POST \
  -H 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","id":1,"method":"eth_call","params":[{"to":"0xae78736Cd615f374D3085123A210448E74Fc6393","data":"0x70a08231000000000000000000000000aa2461f0f0a3de5feaf3273eae16def861cf594e"},"0x18d5779"]}' \
  https://gateway.tenderly.co/public/mainnet
```

Decoded (18 decimals): `51.6282` rETH. Recorded as a token holding; no Rocket Pool deposit is asserted.

---

## Ethereum — wstETH direct check

- Target: `0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0`
- Block: `26040185` (`0x18d5779`)

Same `balanceOf` call pattern. Result: measured zero. No direct Lido position is asserted.

---

## Institutional publication record

- Source: https://github.com/bgd-labs/aave-address-book/blob/main/src/MiscEthereum.sol
- Constant: `AHAB_SAFE = 0xAA2461f0f0A3dE5fEAF3273eAe16DEF861cf594e`

That record establishes the public entity/address relationship. It does not establish a balance; its `quantity` is therefore `UNKNOWN`.