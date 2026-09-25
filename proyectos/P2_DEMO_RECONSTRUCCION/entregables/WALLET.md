# Wallet elegida — AHAB_SAFE

## Entidad

- **Entidad pública documentada:** Aave DAO / AHAB Safe.
- **Dirección pública:** `0xAA2461f0f0A3dE5fEAF3273eAe16DEF861cf594e`
- **Fuente de publicación de la dirección:** libro de direcciones del ecosistema Aave, `src/MiscEthereum.sol`, donde aparece como `AHAB_SAFE`. Fuente pública: https://github.com/bgd-labs/aave-address-book/blob/main/src/MiscEthereum.sol
- **Fuente de contexto de gobernanza:** repositorio público de propuestas del DAO de Aave: https://github.com/aave-dao/aave-proposals-v3

No se incluyen nombres, direcciones ni datos de las personas que puedan firmar o administrar el Safe. El sujeto de este bundle es el Safe y la entidad pública que publicó la dirección.

## Alcance de esta reconstrucción

Se reconstruyen lecturas de solo lectura en:

- Ethereum mainnet, bloque `26040185` (`0x18d5779`), chain ID `1`.
- Base mainnet, bloque `51691143` (`0x314be87`), chain ID `8453`.

Las lecturas históricas se hacen mediante Tenderly público porque el nodo publicnode rechaza llamadas históricas sin acceso de archivo.

## Resultado resumido

| Red | Colateral Aave, base USD | Deuda Aave, base USD | HF | Interpretación |
|---|---:|---:|---:|---|
| Ethereum | 24.783.691,41 | 2.369.837,79 | 8,6458750329 | HF aplicable: existe deuda |
| Base | 14.985,88 | 0,00 | No aplica | Aave devuelve `2^256-1`; se interpreta como sin deuda, no como un HF financiero |

El Safe mantiene además `rETH` directamente en Ethereum. Esto se registra como **tenencia de un token asociado a Rocket Pool**, no como un depósito separado en Rocket Pool. El `wstETH` directo es cero; por tanto no se presenta una posición directa en Lido.

## Decisión de modelado

Aave es el único protocolo con depósito/préstamo observado en las llamadas de esta misión. `rETH` se registra como tenencia de activo, no como depósito de Rocket Pool. Esta distinción se mantiene explícita para no inflar el número de protocolos.
