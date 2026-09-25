# UNKNOWNs — Huecos declarados

Cada entrada corresponde a un campo de una ficha que el bundle declara como `UNKNOWN`. La lista sigue el orden de las fichas en `positions.json`.

| Ficha | Campo | Motivo |
|:---|:---|:---|
| 0001–0004, 0006 | `evidence_hash` | No se generó un hash criptográfico de la respuesta raw; la llamada exacta, endpoint, bloque, calldata y respuesta están preservados en `evidence.md` y `capture.json`. |
| 0001–0004, 0006 | `unknown_detail` | No hay estructura adicional que documentar para estas afirmaciones. Los detalles semánticos van en el campo `unknown_detail`. |
| 0005 | `quantity` | Base Aave devuelve deuda cero y el factor de salud `2^256-1`. No existe un HF financiero aplicable; la cantidad se declara `UNKNOWN` con motivo. El valor raw se preserva en `unknown_detail`, no se publica como cifra financiera. |
| 0005 | `evidence_hash` | No se generó hash. |
| 0005 | `unknown_detail` | No hay estructura adicional que documentar. |
| 0007 | `quantity` | La ficha documental establece la relación entidad/dirección, no un saldo. La cantidad no está establecida. |
| 0007 | `effective_at` | La fecha de publicación del libro de direcciones no se ha establecido en esta captura. |
| 0007 | `evidence_hash` | No se generó hash. |
| 0007 | `unknown_detail` | No hay estructura adicional fuera del alcance de esta ficha documental. |

## Huecos generales (sin ficha asociada)

1. **Valoración de mercado**: ninguna cantidad en `positions.json` incluye un precio externo. Las cifras en USD de las fichas Aave son unidades contables internas del protocolo, no valoraciones de mercado.
2. **Composición de la deuda**: `getUserAccountData` informa deuda agregada; la composición por debt token no se establece aquí.
3. **Posiciones en otros protocolos**: no se consultaron Morpho, Compound, Pendle, Curve, Balancer, Fluid ni otros protocolos. Ausencia de consulta no es ausencia de posición.
4. **Cobertura de cadenas**: el bundle cubre Ethereum mainnet y Base mainnet. No se establece el estado del Safe en otras cadenas.
5. **Identidad de firmantes y controladores**: no se consultó ni publica ningún dato personal. El sujeto es exclusivamente la entidad pública y la dirección publicada.
6. **Reconciliación**: todas las fichas están en `unreconciled`. No se contrastan contra libros contables, snapshots ni fuentes institucionales.
7. **Validez futura**: las afirmaciones están ancladas a bloques históricos. No se establece hasta cuándo describen el estado actual.