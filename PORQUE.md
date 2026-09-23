# Por qué existe esto

### El problema no es que se pierda dinero. Es que nadie coincide en cuánto.

---

## El hallazgo, antes del argumento

Al preparar esta publicación se fueron a verificar, una por una, las cifras que todo el mundo
repite sobre hackeos en DeFi y sobre el seguro en DeFi. **Nueve de ellas.**

El resultado no fue el que se esperaba. **La mayoría no aguantó**, y las que aguantaron
aguantaron **solo si se dice con qué filtro se contaron.**

Lo que sigue no es un alegato. Es **el registro de esa verificación**, con cada cifra, su
fuente y su estado real —incluidas las que quedaron en duda—. Está escrito aplicando **las
mismas reglas del contrato que este repositorio publica**: nada se afirma sin decir quién lo
dice, cuándo, y cuánto se puede confiar en ello.

**El documento se somete a su propio estándar.** Es la única forma honesta de presentarlo.

---

## Exhibit A · Dos empresas, el mismo semestre, dos resultados

Sobre el **primer semestre de 2026**, dos firmas de análisis publicaron su recuento de
pérdidas por hackeos:

| Firma | Pérdidas H1 2026 |
|---|---|
| **Immunefi** | **972 millones de dólares** (207 incidentes) |
| **Blockaid** | **más de 1.000 millones de dólares** |

Mismo periodo. Mismo fenómeno. **Resultados que no coinciden.** No es que una esté mintiendo:
es que **no existe un formato común** que obligue a declarar qué se contó, con qué método, y
qué quedó fuera. Sin eso, dos mediciones honestas del mismo hecho **no se pueden comparar**.

---

## Exhibit B · La misma fuente pública, dos totales distintos

Esto es más grave, porque aquí **la fuente es la misma**.

El panel público de DeFiLlama es **la referencia que todo el mundo cita**. Al consultarlo
directamente:

| Cómo se cuenta | Resultado |
|---|---|
| Lo que **la prensa cita**: «$17.000M en 518 incidentes en 10 años» | **$17.000M / 518 incidentes** |
| **Cómputo directo del mismo dataset**, todos los registros | **$20.700M / 1.281 registros** |
| **Cómputo directo**, solo protocolos DeFi, 2020 → sep-2026 | **$9.016M / 802 incidentes** |
| El mismo, excluyendo retiradas de liquidez y fondos devueltos | **$7.796M** |

**La misma fuente primaria produce cuatro cifras distintas**, y todas son defendibles,
porque **dependen de qué se incluye**. Y el filtro casi nunca se declara.

Una cifra sin su filtro no es un dato: **es un número que parece un dato.** Es exactamente el
defecto que este contrato existe para hacer imposible de escribir.

---

## Exhibit C · El mismo hackeo, tres importes

El exploit de **Kelp DAO**, del **18 de abril de 2026**, se reporta así según quién lo cuente:

| Fuente | Importe |
|---|---|
| **LayerZero** (el protocolo afectado) | **~290 M** |
| **CoinDesk** | **292 M** |
| **Global Ledger** · DeFiLlama | **293 M** |

Tres cifras para **un solo hecho, del que se conoce la fecha exacta y el activo exacto**
(~116.500 rsETH). La diferencia es pequeña y no cambia la conclusión — **pero demuestra que no
existe una taxonomía común ni para el caso más simple.** Si el importe de un hackeo del que
hay comunicado oficial no coincide entre quien lo sufrió y quien lo cuenta, **¿qué se puede
esperar de una cifra agregada?**

Y con **Drift** pasa lo mismo en el mismo mes: **285 M** o **295 M**, según la fuente.

---

## Exhibit D · La estadística que todo el mundo repite y nadie puede comprobar

> **«Menos del 2% del valor depositado en DeFi está asegurado.»**

Se repite en todas partes. **La frase es real y está bien atribuida a Hugh Karp**, fundador de
Nexus Mutual, el mayor asegurador del sector.

**Pero no tiene metodología publicada.** No hay medición independiente de qué cuenta como
«valor asegurado». Es la estimación **del fundador del mayor asegurador** sobre **el tamaño de
su propio mercado potencial** — lo cual no la invalida, pero **es información que el lector
necesita para pesarla, y que casi nunca se le da.**

Lo mismo con el otro número célebre, el **0,14%** — que sí es comprobable, y de hecho
comprobamos:

| Fecha | Nexus Mutual | Todo el sector seguros (31 protocolos) | TVL de DeFi |
|---|---|---|---|
| 16-may-2026 | ~123,5 M (**0,149%**) | — | 83.050 M |
| 23-sep-2026 | 116,94 M (**0,121%**) | 132,5 M (**0,137%**) | 96.404 M |

El dato era correcto **en mayo**. Hoy es **0,12%**. **Una cifra cierta deja de ser cierta sola**,
porque el mundo se mueve debajo de ella — y nada en el número avisa de que caducó.

---

## Exhibit E · Por qué el seguro no cierra la brecha

Aquí está el nudo del argumento, y conviene decirlo sin adornos:

> **Nexus Mutual ha pagado algo más de 18,5 millones de dólares en reclamaciones acumuladas.
> Ha suscrito más de 7.000 millones en cobertura acumulada.**

La brecha entre lo que se pierde y lo que se cubre **no es un problema de capital disponible**.
Es que **la mayor parte del riesgo no es asegurable todavía**, y no por falta de apetito:

> *«Estos riesgos son más difíciles de asegurar, pero **sin estándares claros sobre cómo los
> equipos gestionan su infraestructura y su seguridad**, las aseguradoras se enfrentan a un
> problema enorme para poner precio a las pólizas. **Las primas necesarias se vuelven
> prohibitivamente caras.**»*
> — Hugh Karp, fundador de Nexus Mutual *(16-may-2026)*

**Una aseguradora no puede tarifar un riesgo que no puede medir.** Y no puede medirlo porque
**no hay un formato estándar** que le diga, de cada protocolo, qué está verificado, qué no, con
qué respaldo, y desde cuándo.

Y hay un matiz que casi nunca se cuenta y que **cambia el diseño del problema**: buena parte de
los golpes más grandes **no vienen del código**.

> *«Muchos de los mayores hackeos se han originado **fuera de la cadena**, por fallos de
> seguridad operacional.»* — Hugh Karp

Es decir: el fallo no está en el contrato inteligente, **está en el procedimiento**. Y el
procedimiento **es exactamente lo que un formato de evidencia puede registrar y un auditor
puede comprobar.**

---

## Las tres cifras que sí aguantan

| Afirmación | Cifra | Fuente | Estado |
|---|---|---|---|
| Pérdidas en **abril de 2026** | **641,67 M** — el peor mes del año. Kelp DAO (293 M) + Drift (285 M) ≈ 88% | **Global Ledger**, 6-may-2026 *(primaria)* | ✅ **Confirmada** |
| Pérdidas acumuladas en **protocolos DeFi**, 2020 → sep-2026 | **9.016 M** en 802 incidentes | **DeFiLlama**, cómputo directo *(primaria)* | ✅ **Confirmada, con el filtro declarado** |
| Compromiso de **clave privada** como vector | **8.500 M** — «casi la mitad de todos los hackeos de los últimos 10 años» | **DL News** citando DeFiLlama, 22-abr-2026 | ⚠️ **Parcial** — es *todo cripto*, no solo DeFi |

**Nota sobre la tercera.** Se repite que la clave privada es el vector número uno y el phishing
a multisigs el número dos. **El segundo no se sostiene** al clasificar solo protocolos DeFi: por
importe lidera el compromiso de clave privada, pero **por número de incidentes lidera el control
de accesos**. La ingeniería social, que es de lo que se habla cuando se dice «phishing»,
aparece muy por debajo. **La afirmación popular es imprecisa, y se corrige aquí.**

---

## Lo que esto significa

Fíjate en lo que tienen en común los cuatro primeros exhibits. **No es que falten datos.**
DeFiLlama es público, gratuitamente consultable, y tiene un registro por incidente.

Lo que falta es **una forma de decir qué se contó**. Cuatro cosas, concretamente:

1. **Qué se midió y qué no.** «Protocolos DeFi» y «todo cripto» no son el mismo universo.
2. **Cuándo se midió.** El 0,14% era cierto en mayo y no en septiembre.
3. **Con qué respaldo.** Una estimación del fundador de una aseguradora no pesa igual que un
   registro con hash.
4. **Qué quedó sin establecer.** El filtro que no se declara es un hueco que nadie puede ir a
   tapar, porque **nadie sabe que existe**.

**Eso son exactamente las cuatro cosas que este contrato obliga a escribir.**

---

## Lo que este contrato hace — y lo que no

**Lo que hace:** convierte «aquí hay un número» en «aquí hay un número, de esta fuente, medido
así, en esta fecha, con esto verificado y esto no, y esto es lo que se puede confiar en él».

**Lo que no hace, y hay que decirlo claro:**

> **No reduce el riesgo. No audita protocolos. No dice si un protocolo es seguro. No reemplaza
> al juicio de una aseguradora.**

Es **el formato**. Es la pieza que hoy no existe y que hace que las demás sean posibles: sin
una ficha estándar no hay nada que agregar, nada que comparar, nada que tarifar y nada que
asegurar a escala.

Publicar unas cifras que se contradicen entre sí **y no decirlo** sería repetir el defecto que
este contrato denuncia. Por eso este documento declara lo que no pudo establecer.

---

## Procedencia de cada cifra

Todas las afirmaciones de este documento, con su estado. **Ninguna se da por buena sin fuente.**

| # | Afirmación | Fuente | Tipo | Estado |
|---|---|---|---|---|
| 1 | ~7.700 M perdidos en exploits DeFi desde 2020 | CoinDesk citando DeFiLlama, 16-may-2026 | secundaria | ⚠️ **Parcial** — no reproducible exactamente; desactualizada |
| 2 | >600 M perdidos solo en abril de 2026 | Global Ledger, 6-may-2026 | **primaria** | ✅ **Confirmada** |
| 3 | <2% del TVL de DeFi asegurado | Declaración de Hugh Karp a CoinDesk, 16-may-2026 | secundaria | ⚠️ **Parcial** — sin metodología publicada; conflicto de interés declarado |
| 4 | Nexus Mutual ≈ 0,14% del ecosistema | CoinDesk citando DeFiLlama, 16-may-2026 | secundaria | ✅ **Confirmada a mayo-2026**; hoy 0,12% |
| 5 | Clave privada = vector nº1 | Cointelegraph y DL News citando DeFiLlama, abr-2026 | secundaria | ⚠️ **Parcial** — cierto por importe; **falso por número de incidentes** |
| 6 | Kelp DAO, 18-abr-2026, ~293 M | LayerZero (comunicado oficial), 19-abr-2026 | **primaria** | ✅ **Confirmada** — el importe varía 290/292/293 M según la fuente |
| 7 | ~15.000 M retirados de Aave en 4 días | XWIN Research / CryptoQuant vía NewsBTC | secundaria | ❌ **No confirmada** — DeFiLlama da **−10.763 M en 4 días**; los 15.000 M son **a 3 días** y con otra fuente de TVL |
| 8 | Cita de Karp sobre los estándares | CoinDesk, 16-may-2026 | secundaria | ⚠️ **Paráfrasis del periodista**, no cita textual — aquí se reproduce lo que sí dijo |
| 9 | Brecha asegurado / en riesgo | Nexus Mutual (primaria) + DeFiLlama (primaria) | **primaria** | ✅ **Confirmada** — sin métrica estándar de «TVL asegurado» |

### Fuentes

- **DeFiLlama — Hacks:** https://defillama.com/hacks · API: https://api.llama.fi/hacks
- **DeFiLlama — Protocolos:** https://api.llama.fi/protocols
- **Global Ledger** — «Hackers Steal $642M in April, Set 2026 Record», 6-may-2026
- **CoinDesk** — «Crypto users are choosing juicy yields over protection…», 16-may-2026
- **LayerZero** — «KelpDAO Incident Statement», 19-abr-2026
- **DL News** — «How crypto can avoid private key compromises», 22-abr-2026
- **Cointelegraph** — «Private key compromises led crypto hack losses…», 21-abr-2026
- **Immunefi** — informe H1 2026, vía The Block, 9-jul-2026
- **Blockaid** — informe H1 2026
- **Nexus Mutual** — cobertura suscrita y historial de reclamaciones

### Advertencia sobre fuentes

Varias cifras de este documento —las que más circulan— **provienen todas de un único artículo
de CoinDesk del 16 de mayo de 2026**, cuyos datos base son el panel de DeFiLlama y **una sola
entrevista por correo con Hugh Karp.**

**Los artículos de KuCoin, BingX y MEXC que repiten esas cifras no son fuentes independientes:**
son resúmenes generados automáticamente de ese mismo artículo. **Se citan aquí las fuentes
originales, no sus copias.** Es la regla L-01 de este programa: *se verifica contra la fuente,
nunca contra la copia.*

---

## Una última cosa, incómoda

**Este documento es un ejemplo de su propio problema.**

Las cifras que contiene las contamos nosotros, con nuestros filtros, el 23 de septiembre de
2026. **Si alguien las vuelve a contar mañana, saldrán distintas** — y ninguna de las dos
estará mal.

La diferencia es que aquí **está escrito cómo se contaron, cuándo, con qué fuente, y qué no se
pudo establecer.** Esa es toda la aportación. No es magia: es **escribir las cosas de forma que
se puedan auditar.**

> **El activo no es el dato. Es saber de dónde salió.**

---

*Apache-2.0.*
