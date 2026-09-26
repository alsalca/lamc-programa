# UNKNOWNs — Huecos declarados

Cada entrada corresponde a un campo de una ficha que el bundle declara como `UNKNOWN`. La lista sigue el orden de las fichas en `positions.json`.

| Ficha | Campo | Motivo |
|:---|:---|:---|
| 0005 | `quantity` | Base Aave devuelve deuda cero y el factor de salud `2^256-1`. No existe un HF financiero aplicable; la cantidad se declara `UNKNOWN` con motivo. El valor raw (`2^256-1`) queda documentado en `evidence.md`, no se publica como cifra financiera. |
| 0007 | `quantity` | La ficha documental establece la relación entidad/dirección, no un saldo. La cantidad no está establecida. |
| 0007 | `effective_at` | La fecha de publicación del libro de direcciones no se ha establecido en esta captura. |
| 0007 | `evidence_hash` | No hay artefacto local que hashear: la fuente es un archivo de código en un repositorio público, no un archivo del bundle. La `source_reference` está fijada al commit `dd8bd67401e9c656061c0ac4dff777da25bca884` en vez de a la rama `blob/main`, así que un tercero puede volver a obtener el contenido exacto. Materialidad: la ficha documenta la relación entidad-dirección publicada, no un saldo, así que el hueco no puede alterar ninguna cifra; solo retira el ancla de integridad independiente frente a una edición posterior del archivo. |

> **CORRECCIÓN 2026-09-25:** esta tabla listaba filas de `unknown_detail` que no existen. `unknown_detail` no es uno de los 22 campos del contrato (es un apéndice opcional de `unknown_reason`) y ninguna ficha lo declara; además, una de aquellas frases se contradecía. Se sustituyen por los huecos que las fichas declaran de verdad en su lista `unknown`: `evidence_hash` (0001–0006), `quantity` (0005 y 0007) y `effective_at` (0007).

> **CORRECCIÓN 2026-09-26:** las filas de `evidence_hash` de 0005 y 0007 todavía decían «No se generó hash.» —el qué, sin el porqué ni la materialidad—, mientras que las fichas ya explican ambas cosas. Se sustituyen por el motivo real de cada ficha. Además, la ficha 0007 conservaba en su `evidence_hash` el literal viejo «No cryptographic hash generated.»; se corrigió en `positions.json` y, en el mismo acto, en el ledger de P8, para que el ledger siga idéntico a su fuente (M-R3-5).

> **CORRECCIÓN 2026-09-26 (misión A4 — hash de bloque).** Las fichas 0001–0006 declaraban
> `evidence_hash: "UNKNOWN"` con el motivo «solo se guardó el número de bloque, no su hash».
> El contrato admite expresamente el hash del bloque como `evidence_hash` on-chain
> (`SPEC.md` §4.5, etiqueta `keccak256:`), así que el dato **se podía establecer y se ha
> establecido**: se pidió `eth_getBlockByNumber` a un nodo público y se escribió el hash
> del bloque que cada ficha cita.
>
> - 0001, 0002, 0003 y 0006 → Ethereum mainnet, bloque `26040185` (`0x18d5779`),
>   `keccak256:a5cb9576ce5b2cd9aba82b3c3d63c55be665c67bd2b755a46e8f6b48b7f75ff1`.
> - 0004 y 0005 → Base mainnet, bloque `51691143` (`0x314be87`),
>   `keccak256:d83564d839fd5d816f8a7bb2e20de94bf4d098628fa6787817ca33ecffd71c6e`.
>
> En esas seis fichas `evidence_hash` pasó de `unknown` a `known` y su motivo se retiró de
> `unknown_reason`; la partición sigue cubriendo las 22 casillas **sin solapes ni huecos**.
> La ficha **0007 se queda como estaba**: es documental, su artefacto no es un bloque y su
> hueco de hash es legítimo. El cambio se copió idéntico al ledger de P8 **en el mismo acto**.

## Huecos generales (sin ficha asociada)

1. **Valoración de mercado**: ninguna cantidad en `positions.json` incluye un precio externo. Las cifras en USD de las fichas Aave son unidades contables internas del protocolo, no valoraciones de mercado.
2. **Composición de la deuda**: `getUserAccountData` informa deuda agregada; la composición por debt token no se establece aquí.
3. **Posiciones en otros protocolos**: no se consultaron Morpho, Compound, Pendle, Curve, Balancer, Fluid ni otros protocolos. Ausencia de consulta no es ausencia de posición.
4. **Cobertura de cadenas**: el bundle cubre Ethereum mainnet y Base mainnet. No se establece el estado del Safe en otras cadenas.
5. **Identidad de firmantes y controladores**: no se consultó ni publica ningún dato personal. El sujeto es exclusivamente la entidad pública y la dirección publicada.
6. **Reconciliación**: todas las fichas están en `unreconciled`. No se contrastan contra libros contables, snapshots ni fuentes institucionales.
7. **Validez futura**: las afirmaciones están ancladas a bloques históricos. No se establece hasta cuándo describen el estado actual.