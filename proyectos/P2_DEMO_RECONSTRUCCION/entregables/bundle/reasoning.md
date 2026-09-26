# Reasoning — Razonamiento reconstruible

## 1. Sujeto y fuente

El sujeto es `AHAB_SAFE = 0xAA2461f0f0A3dE5fEAF3273eAe16DEF861cf594e`, publicado en el libro de direcciones oficial del ecosistema Aave (`bgd-labs/aave-address-book`, `src/MiscEthereum.sol`). No se consultan ni publican firmantes, controladores ni datos personales.

## 2. Bloques ancla

| Red | Bloque decimal | Hex | Hash de bloque (`evidence_hash`, `keccak256:`) |
|:---|:---|---:|:---|
| Ethereum mainnet | 26040185 | `0x18d5779` | `keccak256:a5cb9576ce5b2cd9aba82b3c3d63c55be665c67bd2b755a46e8f6b48b7f75ff1` |
| Base mainnet | 51691143 | `0x314be87` | `keccak256:d83564d839fd5d816f8a7bb2e20de94bf4d098628fa6787817ca33ecffd71c6e` |

El hash de cada bloque se obtuvo con `eth_getBlockByNumber` contra un nodo público y es el
`evidence_hash` de las fichas ancladas a ese bloque: 0001, 0002, 0003 y 0006 usan el de
Ethereum; 0004 y 0005, el de Base. Es el caso on-chain que `SPEC.md` §4.5 admite
expresamente, con la etiqueta `keccak256:` (el algoritmo real de un bloque, no `sha256`).
La ficha documental 0007 no cita ningún bloque y conserva su `evidence_hash` en `UNKNOWN`.

Las lecturas se hacen con Tenderly público porque publicnode rechaza bloques pasados.

> **CORRECCIÓN 2026-09-26 (misión A4 — hash de bloque):** las fichas 0001–0006 declaraban
> `evidence_hash: "UNKNOWN"` con el motivo «solo se guardó el número de bloque, no su hash».
> Ese hueco era evitable: el hash del bloque es un `evidence_hash` legítimo y se puede
> pedir (véase `evidence.md`, «Nota de corrección — hash de bloque»). Se obtuvo, se
> escribió en las seis fichas —pasando `evidence_hash` de `unknown` a `known`— y se copió
> al ledger de P8 en el mismo acto. La 0007 no se tocó.

## 3. Ethereum — cuenta agregada Aave

Se llama a `getUserAccountData(address)` contra el Pool Aave V3 de Ethereum. La respuesta ABI se decodifica en seis palabras:

```
collateralBase       24.783.691,41188199 USD base (8 dec.)
debtBase              2.369.837,79237062 USD base (8 dec.)
liquidationThreshold  82,67%
LTV                   80,16%
healthFactor           8,64587503293328
```

La deuda es distinta de cero: el HF aplica.

## 4. Base — cuenta agregada Aave

Misma llamada contra el Pool Aave V3 de Base. La respuesta decodifica:

```
collateralBase       14.985,87931525 USD base
debtBase              0
healthFactor raw     2^256-1
```

**El HF no aplica.** Aave devuelve el entero máximo `2^256-1` como señal de «sin deuda». La ficha correspondiente (0005) declara `quantity = UNKNOWN` porque un número de 78 cifras no es un factor de salud financiero. El valor raw (`2^256-1`) queda documentado en `evidence.md`, no se publica como cifra.

> **CORRECCIÓN 2026-09-25:** el texto decía que el valor raw «se preserva en `unknown_detail`». Ese campo no existe en el contrato ni en la ficha; se corrige la referencia.

## 5. rETH — tenencia, no depósito

Ethereum, bloque ancla, `balanceOf` sobre el contrato `0xae78736Cd615f374D3085123A210448E74Fc6393`:

```
51,628217546317516669 rETH
```

Esto se registra como tenencia de un token. No hay un depósito independiente en Rocket Pool verificado por esta captura. El bundle no infla el número de protocolos tratando la tenencia como depósito separado.

## 6. wstETH directo — medido cero

Ethereum, bloque ancla, `balanceOf` sobre el contrato `0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0`:

```
0
```

La ficha 0006 registra cero medido. El recibo `aWstETH` del Safe pertenece a Aave y no se promueve a una posición directa de Lido. Lido no se cuenta como protocolo adicional.

## 7. Protocolos reales

| Protocolo | Tipo | Evidencia |
|:---|:---|---|
| Aave V3 | Depósito y préstamo | `getUserAccountData` en Ethereum y Base |
| Token rETH (Rocket Pool) | Tenencia | `balanceOf` en Ethereum |

> **CORRECCIÓN 2026-09-25:** se retiró una fila titulada «Aave V3 (Ethereum) — Deuda GHO». Ninguna llamada documentada en `evidence.md` establece la composición de la deuda por debt token; el propio `unknowns.md` declara ese hueco. Afirmar GHO cuando no se establece era una contradicción, no un dato.

El Safe tiene un único protocolo con depósito/préstamo: **Aave V3**. `rETH` es tenencia, no depósito. Esta distinción se mantiene explícita en todo el bundle.

## 8. Principios aplicados

- `UNKNOWN ≠ 0` — el HF de Base se declara UNKNOWN, no se inventa.
- `Container ≠ Asset` — el Safe, el recibo Aave y el activo subyacente no se mezclan.
- Llamada fallida no se convierte en dato.
- Ausencia de consulta no demuestra ausencia de posición.
- Un dato falso con forma de dato (HF de 78 cifras, wstETH contado como tercer protocolo) es peor que un hueco declarado.
- Las personas no aparecen: el sujeto es la entidad y la dirección publicada. Nada más.