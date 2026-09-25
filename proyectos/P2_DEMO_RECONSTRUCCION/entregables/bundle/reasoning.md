# Reasoning — Razonamiento reconstruible

## 1. Sujeto y fuente

El sujeto es `AHAB_SAFE = 0xAA2461f0f0A3dE5fEAF3273eAe16DEF861cf594e`, publicado en el libro de direcciones oficial del ecosistema Aave (`bgd-labs/aave-address-book`, `src/MiscEthereum.sol`). No se consultan ni publican firmantes, controladores ni datos personales.

## 2. Bloques ancla

| Red | Bloque decimal | Hex |
|:---|:---|---:|
| Ethereum mainnet | 26040185 | `0x18d5779` |
| Base mainnet | 51691143 | `0x314be87` |

Las lecturas se hacen con Tenderly público porque publicnode rechaza bloques pasados.

## 3. Ethereum — cuenta agregada Aave

Se llama a `getUserAccountData(address)` contra el Pool Aave V3 de Ethereum. La respuesta ABI se decodifica en seis palabras:

```
collateralBase       24.783.691,41188819 USD base (8 dec.)
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

**El HF no aplica.** Aave devuelve el entero máximo `2^256-1` como señal de «sin deuda». La ficha correspondiente (0005) declara `quantity = UNKNOWN` porque un número de 78 cifras no es un factor de salud financiero. El valor raw se preserva en `unknown_detail`, no se publica como cifra.

## 5. rETH — tenencia, no depósito

Ethereum, bloque ancla, `balanceOf` sobre el contrato `0xae78736Cd615f374D3085123A210448E74Fc6393`:

```
51,6282 rETH
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
| Aave V3 (Ethereum) | Deuda GHO | Captura agregada; composición no detallada |
| Token rETH (Rocket Pool) | Tenencia | `balanceOf` en Ethereum |

El Safe tiene un único protocolo con depósito/préstamo: **Aave V3**. `rETH` es tenencia, no depósito. Esta distinción se mantiene explícita en todo el bundle.

## 8. Principios aplicados

- `UNKNOWN ≠ 0` — el HF de Base se declara UNKNOWN, no se inventa.
- `Container ≠ Asset` — el Safe, el recibo Aave y el activo subyacente no se mezclan.
- Llamada fallida no se convierte en dato.
- Ausencia de consulta no demuestra ausencia de posición.
- Un dato falso con forma de dato (HF de 78 cifras, wstETH contado como tercer protocolo) es peor que un hueco declarado.
- Las personas no aparecen: el sujeto es la entidad y la dirección publicada. Nada más.