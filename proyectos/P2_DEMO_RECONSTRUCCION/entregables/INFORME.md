# INFORME — P2 Demo Reconstrucción

## Resultado

Se reconstruyó una muestra reproducible del AHAB Safe publicado por Aave DAO:

`0xAA2461f0f0A3dE5fEAF3273eAe16DEF861cf594e`

La reconstrucción cubre dos lecturas históricas y sus controles asociados:

- Ethereum mainnet, bloque `26040185` (`0x18d5779`).
- Base mainnet, bloque `51691143` (`0x314be87`).

## Hallazgos establecidos

### Ethereum

La llamada Aave V3 `getUserAccountData` devuelve:

- colateral base: **24.783.691,41 USD**;
- deuda base: **2.369.837,79 USD**;
- umbral de liquidación: **82,67 %**;
- LTV máximo: **80,16 %**;
- HF: **8,6458750329**.

La deuda es distinta de cero, por lo que el HF es aplicable a esta lectura.

El Safe también tiene **51,6282 rETH** medidos por `balanceOf`. El bundle lo trata como tenencia de token, no como un depósito independiente en Rocket Pool.

El saldo directo de wstETH es **0** en el bloque anclado. No se afirma una posición directa en Lido. El `aWstETH` observado es un recibo de Aave y se mantiene separado del activo subyacente.

### Base

La llamada Aave V3 devuelve:

- colateral base: **14.985,88 USD**;
- deuda base: **0 USD**;
- umbral de liquidación: **83,00 %**;
- LTV máximo: **80,00 %**;
- HF técnico: `2^256-1`.

El entero máximo no se publica como factor de salud financiero. Con deuda cero, el HF **no aplica**. La ficha lo expresa como `UNKNOWN` con motivo explícito.

## Qué no se pudo establecer

Está documentado en `bundle/unknowns.md`. Los huecos principales son:

- valoración de mercado independiente de tokens;
- composición individual de la deuda agregada;
- validez futura de saldos históricos;
- hash criptográfico de respuestas raw;
- posiciones en otros protocolos o cadenas no consultados;
- depósito interno de Rocket Pool;
- identidad de firmantes o controladores.

## Límites de interpretación

Este bundle no es un balance contable, una auditoría de solvencia ni una afirmación de patrimonio neto. Es evidencia on-chain anclada a bloques concretos. `reconciliation_status` queda `unreconciled`.

La entidad pública y el Safe son el único sujeto. No se incluyeron datos personales de firmantes o administradores.

## Archivos

- `WALLET.md`
- `bundle/positions.json`
- `bundle/evidence.md`
- `bundle/unknowns.md`
- `bundle/reasoning.md`
