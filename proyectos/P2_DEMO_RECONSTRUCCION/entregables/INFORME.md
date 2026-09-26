# INFORME — P2 Demo Reconstrucción

## Resultado

Se reconstruyó una muestra reproducible del AHAB Safe publicado por Aave DAO:

`0xAA2461f0f0A3dE5fEAF3273eAe16DEF861cf594e`

La reconstrucción cubre dos lecturas históricas y sus controles asociados:

- Ethereum mainnet, bloque `26040185` (`0x18d5779`), hash de bloque
  `keccak256:a5cb9576ce5b2cd9aba82b3c3d63c55be665c67bd2b755a46e8f6b48b7f75ff1`.
- Base mainnet, bloque `51691143` (`0x314be87`), hash de bloque
  `keccak256:d83564d839fd5d816f8a7bb2e20de94bf4d098628fa6787817ca33ecffd71c6e`.

Ese hash es el `evidence_hash` de las seis fichas ancladas a bloque (0001–0006): el caso
on-chain que el contrato admite (`SPEC.md` §4.5), con la etiqueta `keccak256:` que es su
algoritmo real. La ficha documental 0007 no cita bloque y mantiene su `evidence_hash` en
`UNKNOWN`.

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

El saldo directo de wstETH es **0** en el bloque anclado. No se afirma una posición directa en Lido. El `aWstETH` es un recibo de Aave y se mantiene separado del activo subyacente.

> **CORRECCIÓN 2026-09-25:** el texto decía «el `aWstETH` observado». Ninguna llamada de `evidence.md` ni ninguna ficha observa un saldo de `aWstETH`; se retira la palabra «observado» en vez de afirmar una observación que no está documentada.

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
- posiciones en otros protocolos o cadenas no consultados;
- depósito interno de Rocket Pool;
- identidad de firmantes o controladores.

> **CORRECCIÓN 2026-09-26 (misión A4 — hash de bloque).** Esta lista incluía «hash
> criptográfico de respuestas raw». Las fichas 0001–0006 declaraban `evidence_hash:
> "UNKNOWN"` por eso, pero el hueco era evitable: el hash del bloque citado se puede pedir
> y el contrato lo admite como `evidence_hash` on-chain (`SPEC.md` §4.5, etiqueta
> `keccak256:`). Se obtuvo por `eth_getBlockByNumber`, se escribió en las seis fichas
> —pasando `evidence_hash` de `unknown` a `known`, sin dejar motivo en `unknown_reason`— y
> se copió idéntico al ledger de P8 en el mismo acto. Por eso el hueco desaparece de esta
> lista. La ficha 0007 (documental) conserva su `evidence_hash` en `UNKNOWN` con motivo:
> su artefacto no es un bloque.

## Límites de interpretación

Este bundle no es un balance contable, una auditoría de solvencia ni una afirmación de patrimonio neto. Es evidencia on-chain anclada a bloques concretos. `reconciliation_status` queda `unreconciled`.

La entidad pública y el Safe son el único sujeto. No se incluyeron datos personales de firmantes o administradores.

## Archivos

- `WALLET.md`
- `bundle/positions.json`
- `bundle/evidence.md`
- `bundle/unknowns.md`
- `bundle/reasoning.md`
