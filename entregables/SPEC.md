# SPEC — LAMC Evidence Envelope v0.2.0

**Contrato común de evidencia financiera de LAMC.**
**Nivel:** N0 · **Estado:** contrato v0.2.0 terminado, verificado y publicado

> **Qué es esto, en una frase:** una ficha de tamaño fijo que obliga a toda afirmación
> económica a declarar **quién la afirma, cuándo se vio, cuándo rige, cuánto vale, con qué
> autoridad, con qué respaldo crudo y qué queda aún no establecido** — antes de que esa
> afirmación pueda mezclarse con cualquier otra.
>
> **Lo que impide:** que fuentes epistemológicamente distintas (una cadena pública, un
> extracto bancario, una frase de una persona) se sumen como si fueran equivalentes.

**Archivos del contrato:**

| Archivo | Qué es |
|---|---|
| `evidence-envelope.schema.json` | El esquema. Es la definición normativa. Si esta spec y el esquema difieren, **manda el esquema**. |
| `SPEC.md` | Este documento. Explica la semántica que el esquema no puede expresar. |
| `examples/01-public-chain.json` | `authority = PUBLIC_CHAIN` — saldo nativo leído en vivo, anclado a un bloque |
| `examples/02-institution-document.json` | `authority = INSTITUTION_DOCUMENT` — extracto bancario; **la cifra es `UNKNOWN`** |
| `examples/03-derived.json` | `authority = DERIVED` — cifra calculada, con contradicción declarada |
| `examples/04-institution-api.json` | `authority = INSTITUTION` — API de un explorador, con cifra real |
| `VERSION` · `LICENSE` | `0.2.0` · Apache-2.0 |

---

## 1. ALCANCE

**Dentro:** la forma, la semántica y las reglas de una afirmación de evidencia financiera.

**Fuera:** cómo se obtienen los datos, qué motores los normalizan, qué se hace con ellos,
cómo se valoran, cómo se puntúa el riesgo. Este contrato **transporta** evidencia; no la
produce, no la pondera y no la juzga.

**Una afirmación, un sujeto, un contenedor, un instrumento.** Si necesitas dos, son dos
fichas.

> ### Quién manda en las reglas
>
> **El esquema es la fuente autoritativa de las reglas mecánicas:** qué campos son obligatorios,
> qué valores admite cada uno, qué patrones rigen y qué nodos admiten el centinela.
> **Este documento explica QUÉ SIGNIFICA cada campo y POR QUÉ.**
> **Las tablas y listas de aquí son resúmenes legibles de las reglas del esquema: si alguna vez
> difieren, MANDA EL ESQUEMA y la diferencia es un DEFECTO que hay que corregir.**

*(Eso es lo que un agente ciego tuvo que adivinar en la quinta prueba, y no debería tener que
adivinar: aquí está dicho.)*

### (v0.4.0/C1) El origen de una obligación es OTRA afirmación, y por tanto OTRA ficha

**No hay campo para «desde cuándo existe la deuda», y no hace falta.** El sobre registra
**una** afirmación con **una** fecha de efecto. Si necesitas dos hechos —«la deuda es de
4.750.000 USD al 31 de agosto» y «la deuda se originó el 12 de marzo»—, son **dos fichas**,
cada una con su `effective_at`, su `raw_reference` y su autoridad. La segunda puede no
existir: entonces el origen es simplemente **un hecho que no hemos afirmado**, que es
distinto de un hueco de esta ficha.

> **Esto aclara la regla de §4.3, y era el origen de la confusión:** la fecha de corte
> describe **el saldo**, no el nacimiento de la obligación. Un saldo al 31-08 tiene
> `effective_at` el 31-08 **aunque la obligación sea de marzo**. Y si lo que quieres
> registrar es marzo, **eso no es un campo que falte: es una ficha que no has emitido**.

**El esquema no se toca por esto.** El principio ya estaba en el contrato; lo que faltaba era
decirlo aquí.

---

## 2. LOS CINCO AXIOMAS

El contrato está construido para que estos cinco sean **comprobables**, no aspiracionales.

| # | Axioma | Dónde se materializa |
|---|---|---|
| **A1** | `UNKNOWN ≠ 0` | `unknown` es una lista explícita de campos no establecidos. Un campo no establecido se declara; nunca se rellena con cero, `null` ni cadena vacía. |
| **A2** | `EVIDENCE COMPLETENESS ≠ RISK` | El sobre no tiene campo de riesgo, ni puntuación, ni ponderación. A propósito: no se puede confundir tener más fichas con tener menos riesgo. |
| **A3** | La ausencia de evidencia no constituye evidencia | `unknown` con `unknown_reason` obligatorio. Y el sobre **no tiene forma de expresar "X no existe"**: como máximo expresa "no lo hemos establecido". Se aplica al importe: una cifra no establecida es el centinela `UNKNOWN`, nunca `0`. |
| **A4** | `Container ≠ Asset` | `container` (dónde) e `instrument` (qué) son objetos **separados y obligatorios**, con vocabularios distintos. `banco` ≠ `moneda`. Binance ≠ BTC. Wallet ≠ ETH. |
| **A5** | `source_type ≠ calidad` | `source_type` es taxonomía, no nota. La calidad se expresa aparte, en `authority` + `verification_status` + `freshness` + `reconciliation_status`. |

---

## 3. NOTACIÓN Y TIPOS

| Notación | Significado |
|---|---|
| `date-time` | RFC 3339 con zona horaria explícita. Ejemplo: `2026-01-15T09:30:00Z`. |
| **`UNKNOWN`** | **Centinela.** Cadena literal, en mayúsculas. Significa «aún no establecido» (axioma A1). En qué campos se admite lo declara **el esquema**, campo por campo: es **16 del hecho sí y 6 del registro nunca** (§3). **NO vale en los 22.** |
| `UNKNOWN` (lista) | Cuando el campo `unknown` contiene el nombre de un campo, ese campo **no quedó establecido**. |
| Obligatorio | Los **22 campos** son obligatorios en toda ficha. No hay campos opcionales **entre los 22** (`unknown_detail` no es uno de los 22: es el cuerpo del motivo, apéndice **opcional** de `unknown_reason`, ver §4.6). |

> **Por qué `UNKNOWN` es una cadena y no `null`:**
> `null` es ambiguo — puede significar «no aplica», «no lo medimos», «se perdió» o «es cero».
> La cadena literal obliga a decidir y a escribir el motivo. Y obliga a que la lista `unknown`
> y el valor del campo **concuerden** (§5, regla C8).

### LA REGLA DEL CENTINELA — «no lo sé es válido»

> **Decisión del operador (HG-011), textual: «No lo sé es válido».**

**Qué significa.** «Aún no establecido» es un **estado de primera clase** (axioma A1), así que
tiene que poder decirse **sin inventar un valor con forma de dato**. Ése fue el defecto que
costó tres rondas: una lista de siete campos «que admitían el centinela» obligaba a rellenar
los demás con algo — y ese algo era una invención.

> **la regla mecánica vive en el esquema y sólo ahí**: la partición
> completa está en la `description` de la raíz, y cada campo declara en su propio nodo si admite
> el centinela. **Esta spec no la repite.**

**Lo que hay que entender, y no es una regla:**

- **Los 22 campos se parten en dos grupos.** **16 son CAMPOS DEL HECHO** —describen el mundo— y
  admiten el centinela. **6 son CAMPOS DEL REGISTRO** —`claim_id`, `known`, `unknown`,
  `unknown_reason`, `producer`, `schema_version`— y **nunca** lo admiten: no describen el mundo,
  describen **la propia ficha**, y *una contabilidad que dice «no sé» de sí misma no es una
  contabilidad*. Sin esa separación, `unknown: "UNKNOWN"` **anulaba la regla bloqueante entera**.
- **«No aplica» y «no lo sé» son cosas distintas, y viven en dos niveles** (§3, más abajo).
- **La salvaguarda:** una ficha cuyo **hecho** es todo «no lo sé» no afirma nada y **se
  rechaza**. El validador del programa lo comprueba.

**Lo que la regla cerró** — ya no hay que arreglarlo, porque ya no existe:

| Callejón sin salida | Estado |
|---|---|
| `evidence_hash` obligatorio con patrón, sin centinela | **Disuelto** — admite `"UNKNOWN"` |
| `source_reference` / `raw_reference` obligatorias no vacías | **Disuelto** |
| `freshness.policy` sin centinela declarado | **Disuelto** |
| `observed_at` — el contrato asumía que siempre se conoce | **Disuelto** |
| **L-5** — `container` agregado como hueco de primer nivel | **Disuelto** (§10) |

> **Los seis del registro no son una excepción arbitraria: son la frontera entre describir el
> mundo y describir la ficha.** Y hay **dos limitaciones declaradas** en vez de contradicciones
> escondidas — los **enums obligatorios** (`subject.type`, `container.type`, `instrument.kind`)
> no admiten el centinela, y las **cifras aproximadas** no tienen representación propia (§10).

### Dos cosas que NO son lo que parecen

**(v0.3.0/B3) Una ilustración no es un valor por defecto.**
Los ejemplos de esta spec y del esquema (`"4750000"`, `"saldo on-chain: 60 minutos"`,
`"extracto bancario: cierre de mes"`) son **ilustraciones del formato**, nunca valores que se
puedan copiar a una ficha. Copiar uno cuando **la fuente no lo declara** es **inferencia**, y
está prohibido por A1/A3. Si no tienes el valor, va el centinela o se omite, y el hueco se
declara.

**(v0.3.0/B6 y v0.5.0/S5) «No aplica» NO es «no establecido» — y vive en DOS niveles.**
La versión anterior decía que un campo que no aplica **se omite**. Eso **confundía dos niveles
y era imposible de cumplir**: los 22 campos son obligatorios, así que **ninguno se puede
omitir**. La frontera correcta:

| Nivel | Qué se hace |
|---|---|
| **Los 22 campos** | **Nunca se omiten.** «No aplica» **se expresa con el centinela `"UNKNOWN"`**, y el hueco se declara con su motivo. |
| **Subcampos opcionales** (`chain`, `token_id`, `label`, `policy`…) | **Sí se omiten** cuando no aplican — y entonces **no** se declaran hueco. |
| **Un subcampo aplica y no lo establecimos** | Vale el centinela, si su nodo lo admite; si el hueco es interno, el detalle va a `unknown_detail` con su ruta. |

> los niveles y qué admite cada nodo están en el esquema.

---

## 4. LOS 22 CAMPOS

El sobre se llamó «de 14 campos» en documentos anteriores (HG-004). **La fuente original
—`documento interno de propuesta` §5— enumera 21.**

**A esos 21 se añade uno: `quantity`, en v0.2.0.** La fuente describía la procedencia de un
importe **sin tener dónde poner el importe**. Lo detectó la prueba ciega de N0 y lo autorizó
HG-010/D-014. **Total: 22.** Ver §10, hallazgos F-1 y F-5.

### 4.1 Identidad

**`claim_id`** — `string`, patrón `^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-[0-9]{4}-[0-9]{4}$`

Identificador único y estable. **Nunca se reutiliza** para otra afirmación, aunque la
primera se corrija o se retracte: una corrección es una ficha nueva que sustituye, no una
edición de la anterior. Es lo que permite reconstruir la historia sin sobrescribirla.

### Convención obligatoria (B1: la unicidad)

```
claim_id  =  <APARATO>-<AAAA>-<NNNN>

APARATO   slug del emisor, EN MAYÚSCULAS (A–Z, 0–9, guiones).
          DEBE coincidir con el primer segmento de 'producer'
          (lo que va antes de '/' o de '@').
AAAA      año de emisión.
NNNN      secuencia monotónica de 4 dígitos POR APARATO Y AÑO, desde 0001.

LONGITUD  11 a 40 caracteres en total, y el APARATO entre 1 y 30.
          El mínimo lo fija el propio patrón: 1 + 1 + 4 + 1 + 4 = 11, así que
          "A-2026-0001" es válido y el esquema no lo rechaza (v0.4.0/T3).

Ejemplo:  claim_id = "LAMC-P1-2026-0001"
          producer = "LAMC-P1/eth-rpc"
```

**Y la forma práctica de sostener la unicidad** —que es lo que B1 del contrato exige y nada
comprueba por sí solo:

1. **El `APARATO` es del emisor y no se comparte.** Dos emisores distintos **nunca** usan el
   mismo. Un tercero elige el suyo y no reutiliza uno que ya haya visto.
2. **La secuencia es monotónica** dentro de cada aparato y año, y **no se rellena huecos**.
3. **Un `claim_id` no se edita jamás.** Corregir una ficha es emitir **otra** con **otro** id.
4. **El emisor mantiene un registro append-only** `claim_id → producer`. Ese registro —no el
   esquema— es lo que sostiene la unicidad, y es lo que un tercero debe poder inspeccionar.

> **El prefijo va en el id, y no por gusto:** con un espacio de nombres único y global, dos
> emisores independientes colisionarían sin conocerse. **N0 exige que un tercero pueda emitir
> fichas sin hablar con nosotros** — así que el id tiene que llevar quién lo emite.

**`subject`** — objeto `{type, subject_id, label?}` — **exactamente uno**
El *Economic Subject*: la entidad cuyos derechos y obligaciones económicas se representan.

| `type` | Significa |
|---|---|
| `NATURAL_PERSON` | Una persona |
| `LEGAL_ENTITY` | Una sociedad, fundación o trust |
| `GROUP` | Un conjunto de sujetos agregados (familia, grupo empresarial) |

Un portafolio familiar son **N fichas**, no una. Esto es lo que permite multi-entidad sin
colapsar identidades.

### Las formas de un identificador (v0.3.0/B1 y v0.4.0/T4) — no se inventa

```
subject_id = <IDENTIFICADOR>            <- (1) lo aporta una fuente, tal cual
subject_id = "LOCAL:<ETIQUETA>"        <- (2) lo asignamos NOSOTROS
subject_id = "BANCO-XXXX-XXXX-1234"    <- (3) forma enmascarada o truncada
subject_id = "UNKNOWN"                 <- (4) no lo sabemos
```

**Las cuatro son legítimas, y la (4) lo es desde la regla central.** Valen igual para
`container.container_id`: son las mismas cuatro formas.

> ### Un identificador local NO es un dato sobre el mundo: es una ETIQUETA.
> Y tiene que **verse como lo que es**. El resultado **no puede ser un valor inventado
> indistinguible de un dato real.**

Por eso el prefijo `LOCAL:` es **obligatorio** cuando el identificador lo ponemos nosotros:

1. **`LOCAL:` está reservado al emisor.** Nunca identifica a un sujeto ante un tercero: es
   una etiqueta interna para poder hablar del sujeto dentro de nuestra propia evidencia.
2. **Un identificador aportado por una fuente NO lleva el prefijo.** Si un banco, un
   registro o una cadena dan un identificador, se escribe tal cual.
3. **Una forma enmascarada o truncada también es legítima** — `"BANCO-XXXX-XXXX-1234"` —,
   porque es **visiblemente parcial**: no se puede confundir con el identificador completo.
   Es lo que permite cumplir R-008 (no publicar un dato personal) sin inventar nada.
   **La máscara se escribe con `X`, NO con `*`** (v0.5.0/X1, corregido en v0.6.0/B4): en
   **`subject_id`** el patrón admite letras y dígitos pero **no asteriscos**, así que
   `BANCO-****-****-1234` **era rechazado por el propio esquema** — la prosa y el esquema se
   contradecían. En **`container_id` no hay patrón**, así que ahí la `X` es **convención por
   coherencia, no obligación** del esquema.
4. **Con `LOCAL:` o con una forma enmascarada, el identificador real queda sin establecer.**
   Eso es un hueco anidado, así que **se declara en `unknown_detail`** con la clave
   `subject.subject_id`. La etiqueta dice *que* no lo tenemos; el detalle dice *por qué*.
5. **`known` no significa «dato real del mundo»**, significa «la ficha establece este valor».
   Una etiqueta local se establece (existe, es estable, es nuestra) y por eso va en `known`
   — pero **lleva la marca que impide leerla como un identificador de verdad**.

```
subject_id = "LOCAL:SUBJ-0001"     <- (2) etiqueta nuestra; el id real está sin establecer
subject_id = "900123456-7"         <- (1) identificador real, aportado por una fuente
subject_id = "BANCO-XXXX-XXXX-1234" <- (3) enmascarado: parcial a la vista, no confundible
subject_id = "UNKNOWN"             <- (4) no lo sabemos. ES VÁLIDO (regla central)
```

**`producer`** — `string`, convención `<APARATO>[/<componente>][@<versión>]`

Qué emitió la ficha: sistema, lector, script, persona o agente. **`APARATO` es un slug estable
en mayúsculas** y es el **mismo para todas las fichas de ese aparato** — si no lo fuera, no se
podrían agrupar dos fichas por autor, que es justo para lo que sirve este campo.

```
producer = "LAMC-P1/eth-rpc"        claim_id = "LAMC-P1-2026-0001"
producer = "OBSERVATORIO-EJEMPLO/uniswap"   claim_id = "OBS-EJEMPLO-2026-0117"
```

**No es prosa por ficha.** «el constructor de P1 — consulta JSON-RPC hecha el martes» no vale: describe
el método (eso es `capture_method`) y cambia en cada ficha, con lo que deja de poder agrupar.

**`schema_version`** — `string`, patrón `^[0-9]+\.[0-9]+\.[0-9]+$`
Versión del sobre que la ficha declara cumplir. Debe coincidir **exactamente** con el
contenido del archivo `VERSION`.

### 4.2 Qué se observa

**`container`** — objeto — **dónde**
El lugar donde se observa el derecho u obligación.

| `container.type` | Qué es |
|---|---|
| `BLOCKCHAIN_WALLET` | Una dirección en una cadena |
| `BANK_ACCOUNT` | Una cuenta bancaria |
| `BROKERAGE_ACCOUNT` | Una cuenta de intermediación |
| `CENTRALIZED_EXCHANGE` | Una cuenta en un exchange centralizado |
| `CUSTODY_ACCOUNT` | Una cuenta de custodia |
| `PENSION_ACCOUNT` | Una cuenta de pensión |
| `CREDIT_ACCOUNT` | Una cuenta de crédito |
| `DOCUMENTARY_ASSET` | Un activo documental |
| `OTHER` | Otro, o un agregado |

Opcionales: `container_id` (dirección, cuenta enmascarada, contrato), `operator` (quién
administra: **custodio** en una cuenta de activo, **acreedor** en un `CREDIT_ACCOUNT`),
`chain` y `chain_id` (solo si `type = BLOCKCHAIN_WALLET`).

**Estos opcionales siguen la regla de v0.5.0/S5, que tiene dos niveles:** un **subcampo
opcional** que **no aplica** —`chain` en una cuenta bancaria— **se omite y no se declara como
hueco**. Si **aplica pero no lo establecimos**, vale el **centinela `"UNKNOWN"`** y el hueco se
declara con su motivo. Si el hueco está **dentro** del objeto —el caso del agregado—, el detalle
va a `unknown_detail` con su ruta (`container.chain`). **Lo que nunca se omite son los 22
campos**, que son obligatorios: en ellos «no aplica» se expresa con el centinela.

> **`chain_id` es el número, `chain` es la etiqueta.** `"ethereum-mainnet"` es prosa;
> `1` es un hecho. Se pide el número para eliminar la ambigüedad de nombres entre redes
> homónimas.

**`instrument`** — objeto `{kind, symbol?, contract_address?, token_id?}` — **qué**
Lo que existe económicamente **dentro** del contenedor. Vocabulario de `kind`:
`NATIVE` · `ERC20` · `SPL` · `JETTON` · `BEP20` · `ERC721` · `ERC1155` · `LP_POSITION` ·
`LENDING_POSITION` · `CASH` · `FIAT_BALANCE` · `DEBT` · `NONE`.

> ### A4 aplicado
> ```
> container = {type: BANK_ACCOUNT,  operator: BANCO-EJEMPLO}  instrument = {kind: FIAT_BALANCE, symbol: USD}
> container = {type: BLOCKCHAIN_WALLET, chain: ethereum}      instrument = {kind: NATIVE, symbol: ETH}
> ```
> No se puede escribir una ficha donde el contenedor *sea* el instrumento. El esquema los
> obliga a ser dos objetos separados.
>
> **Si la afirmación es sobre el contenedor mismo** (por ejemplo, «esta cuenta existe»),
> se declara `instrument.kind = NONE`. No se deja vacío: `NONE` dice «no hay instrumento
> separado», mientras que vacío no dice nada.

**`source_type`** — enumeración de 11 valores
Cómo se obtuvo. **No implica calidad (A5).**

```
ONCHAIN · PUBLIC_API
REGULATED_API · INSTITUTION_API · OPEN_FINANCE_API
SIGNED_DOCUMENT · BANK_STATEMENT · BROKER_STATEMENT · STRUCTURED_EXPORT
MANUAL_DOCUMENT · MANUAL_ASSERTION
```

> **v0.3.0/B2 · Dónde va cada extracto.** `BANK_STATEMENT` cubre el extracto de **cuenta** y el de
> **tarjeta** — un estado de tarjeta es un extracto bancario y no hace falta un valor nuevo.
> `BROKER_STATEMENT` cubre el estado de cuenta de intermediación. Si aparece un documento
> bancario que no encaje en ninguno, **se usa el más cercano y se dice por qué en
> `capture_method`**; no se inventa una taxonomía nueva desde un caso.
>
> **`MANUAL_DOCUMENT` — definido (cierra un hueco del catálogo).** Es un documento que **no
> emite una institución**: apuntes nuestros, una captura de pantalla, un PDF que hicimos
> nosotros. **No aporta autoridad institucional**: con él, `authority` es `HUMAN` o `DERIVED`,
> nunca `INSTITUTION_DOCUMENT`. **`MANUAL_ASSERTION`** es distinto: es una afirmación **sin
> documento detrás** — lo que alguien dice. La frontera es si hay un documento o no.

**`source_reference`** — `string` no vacío
Referencia a la fuente: endpoint, documento, identificador de consulta. Debe permitir
**volver** a la fuente.

**`capture_method`** — `string` no vacío
**El camino de acceso**: cómo obtuvimos el dato. Lectura de contrato, consulta a endpoint,
transcripción del documento por nosotros, tecleo de lo que alguien dijo, cálculo. Si es una
derivación, aquí se describe la derivación.

> **v0.6.0/B3 · No se le exige reproducibilidad.** Antes la prosa pedía que `capture_method`
> fuera «reproducible por un tercero», **y a la vez** la rúbrica declaraba que **una transcripción
> manual no es reproducible por definición**: el contrato exigía y presuponía a la vez lo mismo
> imposible. **`capture_method` DESCRIBE el método** con precisión suficiente para que un tercero
> pueda **intentarlo**; **la reproducibilidad se gradúa con `confidence` (K1)**, no se exige aquí.
>

> ### `source_type` vs `capture_method` — dos preguntas distintas
> ```
> source_type      ¿QUÉ ES la fuente?        (su naturaleza)
> capture_method   ¿CÓMO la leímos?          (nuestro camino de acceso)
> ```
> **Son ortogonales, y por eso no se puede deducir uno del otro.** Dos trampas frecuentes:
>
> | Falso razonamiento | Por qué está mal |
> |---|---|
> | «Lo leí por una API, entonces la fuente es institucional» | La API es el camino. La fuente sigue siendo la que es: si esa API publica lo que dijo un tercero, la fuente es ese tercero. |
> | «Es un PDF, entonces la fuente es documental» | El PDF es un soporte. Un PDF autogenerado por nosotros no es un documento institucional. |
>
> **`capture_method` es donde se declara la debilidad del camino.** Si transcribimos a mano,
> se dice aquí — y esa debilidad se refleja en `verification_status`, no en `source_type`.

**`quantity`** — `string` decimal, o el centinela `"UNKNOWN"` · **cuánto**

La cantidad de `instrument.symbol` que la afirmación sostiene.

```
"quantity": "4750000"                  ← 4.750.000 USD
"quantity": "0.123456789012345678"     ← ETH, con 18 decimales exactos
"quantity": "UNKNOWN"                  ← no se estableció, y hay motivo abajo
```

**Tres decisiones que van juntas:**

1. **Es una cadena, no un número.** Un `float` en JSON no puede representar
   `0.123456789012345678` sin perder dígitos, y redondearía a cero los saldos pequeños
   —justo los que más importan en una posición cripto. La cadena conserva la cifra exacta.
   Formato: dígitos con punto decimal, sin separadores de miles, sin símbolo de moneda.
2. **No lleva la moneda.** La unidad ya está en `instrument.symbol` (`USD`, `ETH`, `EUR`).
   Duplicarla permitiría que las dos se contradijeran.
3. **No lleva la fecha.** Para un saldo a una fecha de corte, la fecha de corte **es**
   `effective_at` (§4.3): un saldo al 31-08 rige desde el 31-08, no desde que lo leímos.

**Nunca es negativa.** Un pasivo se escribe con su valor absoluto y `instrument.kind = DEBT`.
Un `-4750000` no diría si el sujeto debe o le deben.

> **El importe no va en prosa — CUANDO LA CIFRA SE CONOCE.** Escribirla dentro de
> `capture_method` —como hizo la prueba ciega de N0 con la v0.1.0, que no tenía este campo— la deja
> fuera de todo campo: un lector no puede saber que existió ese parche.
>
> **La excepción, y es la que manda cuando la cifra es aproximada (v0.6.0/B1):** si la fuente dice
> «como dos millones», **no hay cifra exacta que poner en `quantity`**. Entonces
> `quantity = "UNKNOWN"` **y la aproximación se escribe en el motivo del hueco** (L-8). Las dos
> reglas no se anulan: **§4.2 prohíbe el importe en prosa cuando se conoce; L-8 lo ordena cuando es
> aproximado y el valor es el centinela.**

### 4.3 Cuándo

**`observed_at`** — `date-time` · **cuándo lo vimos**

**`effective_at`** — `date-time` o el centinela `"UNKNOWN"` · **cuándo rige económicamente**

> ### No son lo mismo, y deben poder diferir
> Un extracto bancario observado hoy puede regir desde el mes pasado. Una posición
> on-chain observada ahora rige desde que se abrió. Un contrato firmado hoy puede
> regir desde el 1 de enero.
>
> **Copiar `observed_at` en `effective_at` está prohibido cuando no se conoce la fecha de
> efecto.** Se escribe `"UNKNOWN"` y se declara el motivo. Un registro de fecha de captura
> no es prueba de fecha de efecto (la regla del programa: *no inferir verdad presente de
> registros históricos*).

> **El caso del saldo a una fecha de corte.** Si el extracto dice «saldo al 31 de agosto»,
> entonces `effective_at = "2026-01-31"` y `observed_at` es el día que lo leímos.
> La cifra **rige** desde el corte. Para un saldo puntual de cadena, `effective_at` es el
> instante del bloque. Y si no se conoce la fecha de corte, `effective_at = "UNKNOWN"` con
> su motivo: **no se copia `observed_at` para rellenar.**

> **Esta regla es sobre el SALDO, no sobre el origen de la obligación.** `effective_at` dice
> **desde cuándo rige la cifra que esta ficha afirma**. Desde cuándo existe la obligación es
> **otro hecho** y por tanto **otra ficha** (v0.4.0/C1, §8).

### (v0.3.0/B9 y v0.5.0/I1) La precisión y la zona las pone la FUENTE

> **Regla (v0.5.0/I1): NO SE AÑADE PRECISIÓN QUE LA FUENTE NO DIO.**

El defecto que esto corrige era grave y silencioso: la fuente daba **sólo una fecha de corte**
(`2026-01-31`), el esquema exigía un instante con hora y zona, y el emisor **fabricaba** las dos
—`23:59:59` por convención y un **desplazamiento horario inferido de la moneda del instrumento**—. **Inventó
precisión horaria y una zona que nadie le había dado**, que es exactamente lo que el centinela
existe para no tener que hacer.

**Una fecha sin hora es un valor válido y honesto** cuando la fuente sólo da la fecha. Y si se
escribe hora, **la zona es obligatoria** — nunca una hora local suelta.

```
instante de sistema o de cadena   ->  UTC           2026-01-15T09:30:00Z
corte de una fuente con zona      ->  zona DE LA FUENTE
                                      banco: 2026-01-31T23:59:59+02:00
fecha sola, que es lo que la fuente dio ->  2026-01-31   (SIN hora y SIN zona)
```

**No se convierte en silencio.** El corte de un banco se escribe en el desplazamiento que ese banco usa, que
es como lo dice el banco; pasarlo a `Z` cambia el día para quien lo lea. Si por alguna razón
se normaliza, **la convención se declara en `capture_method`** — lo que nunca vale es dejar
una fecha sin offset y que cada lector suponga una zona distinta.

**`freshness`** — objeto `{status, valid_until?, policy?}`

| `freshness.status` | Significa |
|---|---|
| `fresh` | Vigente |
| `stale` | Envejecida: usable con reserva declarada |
| `expired` | **Vencida: no puede sostener una conclusión** |
| `UNKNOWN` | No se estableció la política de vigencia |

`valid_until` (`date-time` o `"UNKNOWN"`) es el instante de vencimiento. **`policy` es
`OPCIONAL`** — el esquema solo exige `status`, y **manda el esquema** (v0.4.0/T2). Si la fuente no
declara política de vigencia, `status` vale `"UNKNOWN"`, el hueco se declara, y `policy` **se
omite**: no se rellena con un ejemplo.

> **v0.3.0/B3 · «saldo on-chain: 60 minutos» y «extracto bancario: cierre de mes» son ILUSTRACIONES
> del formato, no valores por defecto.** Copiarlas a una ficha cuando la fuente no las declara
> es **inferencia**, prohibida por A1/A3. Si no tienes la política, `freshness.status` es
> `"UNKNOWN"` y el hueco se declara — no se rellena con el ejemplo de la spec (B3, §3).

> **La consecuencia de `expired` es dura:** el dato no se borra, pero **no puede sostener
> una conclusión**. Ver `examples/03-derived.json`: una cifra de junio de 2026 conserva su
> valor y su fecha, y aun así queda marcada `expired` en septiembre de 2026.

### 4.4 Con qué fuerza

**`authority`** — **quién lo afirma**

| Valor | Significa |
|---|---|
| `PUBLIC_CHAIN` | Estado de una blockchain, verificable determinísticamente |
| `INSTITUTION` | API de una institución regulada |
| `INSTITUTION_DOCUMENT` | Extracto, certificado, estado financiero |
| `HUMAN` | Afirmación manual de una persona |
| `DERIVED` | Calculado por nosotros a partir de otras evidencias |

### La regla de la transcripción manual

Si alguien **transcribe a mano** un documento institucional, ¿la ficha es
`INSTITUTION_DOCUMENT` o `HUMAN`? **Se decide por el origen, no por el camino.**

```
Transcribo a mano un extracto bancario
   -> authority = INSTITUTION_DOCUMENT      (quien responde por la cifra es el banco)
   -> source_type = BANK_STATEMENT          (la fuente sigue siendo el extracto)
   -> capture_method = "transcripcion manual del PDF, hecha por el operador"
   -> verification_status = documentary     (verificable contra el documento)

Alguien me dice de memoria cuanto tiene en el banco
   -> authority = HUMAN                     (quien responde es la persona)
   -> source_type = MANUAL_ASSERTION
   -> verification_status = unverified

Transcribo mi propia hoja de calculo
   -> authority = HUMAN o DERIVED           (no hay institucion detras)
   -> source_type = STRUCTURED_EXPORT
```

**Por qué se decide así:** `authority` responde a *«¿quién responde si esto es falso?»*. Si
transcribí mal el extracto, **el banco no es el culpable — pero el documento original sigue
existiendo y sigue siendo la autoridad a la que apelar**. Lo que cambió no es quién responde:
es **cuánto hay que confiar en mí para llegar a él**. Eso se declara en `capture_method`, y
se paga en `verification_status` y en `confidence`.

**Regla dura:** transcribir **nunca** sube la autoridad y **nunca** deja la ficha en
`deterministic`. Como máximo conserva la autoridad del origen y baja la verificabilidad.

**`verification_status`** — **cómo se verificó**

| Valor | Significa |
|---|---|
| `deterministic` | Reproducible por cualquiera, sin confiar en nadie |
| `authenticated` | Verificable contra la institución emisora |
| `documentary` | Verificable contra el documento |
| `unverified` | Afirmado, no verificado |

**`confidence`** — `high` · `medium` · `low`

> **Esto no es una ponderación ni un score** (eso sería N8 y está prohibido aquí). Es una
> **rúbrica contable**: se cuentan criterios, no se suman pesos.

Se evalúan **cuatro criterios**, y cada uno es SÍ o NO — **el esquema los contiene.**

| # | Criterio | Es SÍ cuando… |
|---|---|---|
| **K1** | **Reproducible** | El camino de `capture_method` lo puede repetir un tercero y llegar **al mismo resultado** |
| **K2** | **Sin huecos materiales** | `unknown` está vacío, o lo que falta no cambia la conclusión que se saca de la cifra. **`raw_reference` en el centinela es SIEMPRE material** (v0.6.0/B5): sin respaldo citable la cifra no se puede usar como evidencia |
| **K3** | **Sin contradicción abierta** | `reconciliation_status` no es `disputed` |
| **K4** | **Vigente** | `freshness.status` es `fresh` |

**Veredicto:**

| Situación | `confidence` |
|---|---|
| Los cuatro en SÍ | **`high`** |
| **Un** criterio en NO | **`medium`** |
| **Dos o más** en NO | **`low`** |
| Hueco **material** en la cifra o su unidad (`quantity` / `instrument.symbol` en `unknown`) | **`low`**, aunque lo demás esté bien |

> **«Hueco no material»** = lo que falta **no impide usar la cifra para lo que la ficha
> pretende**. Que la política de vigencia sea nuestra y no de la fuente es no material.
> Que falte el tipo de cambio con que se convirtió la cifra **sí** es material.
> El juicio de materialidad es del que emite, y **se declara por escrito en el motivo
> correspondiente**: en **`unknown_reason`** si el campo entero no está establecido, y en
> **`unknown_detail`** si lo que falta es un detalle **dentro** de un campo que sí lo está
> (por ejemplo `instrument.symbol`, que es material: sin la unidad, la cifra no se puede usar).
> Antes esto era una contradicción —`unknown_reason` solo admite campos de `unknown`, y
> `unknown` solo de primer nivel—, así que un hueco anidado **no tenía dónde declarar su
> materialidad**. Ahora sí.

### (v0.3.0/B4) K1 y la transcripción manual

**Decisión: una transcripción manual hace K1 = NO, y por tanto techa la ficha en `medium`.**

El motivo, en una frase: **un tercero puede releer el documento, pero no puede repetir mi
transcripción.** El paso que hay que reproducir incluye mi mano, y mi mano no está en el
artefacto. Así que el camino «transcribir» no es reproducible por definición.

```
K1 = SÍ   el tercero repite el camino y llega al mismo número
          (leer un contrato, repetir una consulta, releer un archivo)
K1 = NO   el camino incluye un paso que no puede repetir:
          transcripción manual, tecleo, testimonio, cálculo no documentado
```

**Consecuencia que importa:** una ficha `INSTITUTION_DOCUMENT` transcrita a mano conserva su
autoridad —el banco sigue respondiendo por la cifra— pero **nunca alcanza `confidence: high`**,
porque `high` exige los cuatro criterios. Y si además el documento no es accesible para un
tercero, K1 sigue en NO y K2 probablemente también: `low`.

**Verificación de la rúbrica sobre los cuatro ejemplos** (un tercero puede repetir esta tabla):

| Ficha | K1 | K2 | K3 | K4 | Resultado |
|---|---|---|---|---|---|
| `01-public-chain` | SÍ | SÍ (sin huecos) | SÍ | SÍ | **`high`** |
| `02-institution-document` | NO (PDF cifrado) | NO (falta la cifra: **material**) | SÍ | NO (`freshness.status = UNKNOWN`) | **`low`** |
| `03-derived` | SÍ | NO (contenedor agregado) | NO (`disputed`) | NO (`expired`) | **`low`** |
| `04-institution-api` | SÍ | NO (hueco **no material**) | SÍ | SÍ | **`medium`** |

**La ficha 04 se bajó de `high` a `medium` al aplicar esta rúbrica**, porque declara un hueco
interno. Es la rúbrica actuando, no una opinión.

> `authority`, `verification_status` y `confidence` son **tres ejes independientes**.
> No se deduce uno de otro, y el contrato no impone ninguna combinación: un extracto
> bancario tiene autoridad institucional alta y verificabilidad pública nula (A5).
> Declarar `confidence: high` sobre `verification_status: unverified` es legítimo
> —significa que le creemos a quien lo afirmó— siempre que se declare así.

### 4.5 Respaldo crudo

**`raw_reference`** — `string` no vacío
Referencia **citable y reproducible** al artefacto crudo. **Sin esto no hay evidencia.**

> **v0.6.0/B5 · El caso en que localizar es IMPOSIBLE.** Si el artefacto **se conoce pero no se
> puede localizar** —se sabe cómo se llama y se tiene su hash, pero no su ubicación—, exigir una
> referencia que localice **obliga a inventar una referencia falsa**. **`raw_reference` vale el
> centinela `"UNKNOWN"`** y el motivo explica que el artefacto existe, cómo se llama y por qué no
> se puede localizar. **La conducta honesta pasa a estar permitida.**
>
> **Y su consecuencia, que hay que asumir:** una ficha así **es conforme al sobre** pero **su
> respaldo no es citable**. Eso es un **hueco material**, así que **`confidence` no puede ser
> `high`**. *«Válida» significa «conforme al sobre». **No significa «usable como evidencia».***
>

### (v0.3.0/B8) La forma depende del TIPO DE ARTEFACTO

**No toda la evidencia es un archivo.** Exigir una ruta a un estado de cadena o a una
respuesta de API es pedir un imposible — y una regla que no cabe en la realidad se incumple.
La regla es **referencia reproducible según el tipo**:

| Tipo de artefacto | Referencia válida |
|---|---|
| **Archivo** | ruta **absoluta** o URI |
| **Estado de cadena** | cadena + **número de bloque** (+ dirección/contrato) |
| **Respuesta de API** | **endpoint completo + la consulta** |
| **Documento con dueño** | ruta **y hash** |
| **Testimonio oral** | **quién lo declara + fecha + dónde o cómo se recibió** |

```
archivo      /ruta/al/informe.md  +  sha256 d9ee4197…
cadena       Ethereum mainnet, bloque 26037286 (hash 0x18cb…), eth_getBalance(0xb1e1…)
API          https://eth.blockscout.com/api/v2/addresses/0x5c78…/token-balances
documento    adjuntos/02-extracto-ejemplo.pdf.enc  +  sha256 1b2ae02e…
```

**La prueba de que la referencia sirve:** un tercero que no estuvo presente **puede volver al
artefacto y obtener lo mismo**. Si tu referencia no permite eso, no es una referencia: es una
descripción. Las formas de arriba la permiten; `extracto.txt` **no**.

> **v0.5.0/X5 · El testimonio oral tiene referencia, y por eso `MANUAL_ASSERTION` ya se puede
> cumplir.** El contrato define `MANUAL_ASSERTION` como «una afirmación sin documento detrás» y
> **luego exigía una referencia al artefacto** — insatisfacible por construcción. Un testimonio
> **sí tiene** referencia: **quién lo dijo, cuándo, y dónde o cómo se recibió**. Con esa fila, el
> tipo de fuente deja de ser un callejón sin salida.

Si el artefacto no es publicable (contiene datos personales), se indica su ubicación y su
hash, y se declara en `unknown` lo que no se publica.

**`evidence_hash`** — `string`, `<algoritmo>:<hex>`
Hash del artefacto crudo. Detecta alteración posterior: si el archivo cambia, el hash deja
de coincidir y la ficha queda cuestionada sin necesidad de volver a leerla.

> **v0.5.0/X7 · El algoritmo se declara, no se disfraza.** El contrato afirmaba que *«en la
> cadena, el hash del bloque **es** un sha256»* **para que encajara en el patrón**. **Es falso:
> el de Ethereum es Keccak-256.** El contrato estaba **etiquetando mal un dato real para que
> cupiera en la casilla** — el mismo pecado que combate. Ahora **algoritmo y valor van
> separados** (`sha256:…` para archivos, `keccak256:…` para bloques) con una lista declarada de
> algoritmos en el esquema.

> **`evidence_hash` no sustituye a `raw_reference`.** El hash prueba integridad; la
> referencia prueba procedencia. Hacen falta las dos.
>
> **El caso on-chain está declarado como excepción legítima.** Cuando el artefacto crudo
> **es la propia cadena**, no hay archivo que hashear: lo que se cita es el **hash del
> bloque** y su número, que cumplen la misma función —atar la afirmación a un estado
> concreto e inalterable— y se pueden reverificar sin nosotros. En
> `examples/01-public-chain.json` el hash es el del bloque, no de un fichero nuestro — y va
> etiquetado **`keccak256:`**, que es su algoritmo de verdad.

### 4.6 Contraste y huecos

**`reconciliation_status`** — `unreconciled` · `reconciled` · `disputed`

| Valor | Significa |
|---|---|
| `unreconciled` | Aún no contrastada contra otras evidencias |
| `reconciled` | Contrastada y coincide |
| `disputed` | **Contrastada y NO coincide** |

> **`disputed` no resuelve nada: registra.** La contradicción se preserva (regla dura 2:
> no reconciliar por inferencia). El contrato no permite expresar «se resolvió a favor de
> la fuente A» sin una ficha nueva que lo justifique.

**`known`** — lista, mínimo 1 elemento, sin repetidos
Los campos **de esta ficha** que quedaron establecidos. Cada elemento es el nombre de un
campo de este mismo sobre.

**`unknown`** — lista, sin repetidos
Los campos **de esta ficha** que permanecen **aún no establecidos**. Cada elemento es el
nombre de un campo de este mismo sobre, **de primer nivel**. **Puede estar vacía** — y una
ficha sin huecos es tan válida como una con huecos.

> ### Las dos listas son una contabilidad, no una impresión
> ```
> known ∪ unknown  =  los 22 campos del sobre, exactamente
> known ∩ unknown  =  vacío
> ```
>
> ### La regla que decide en qué lista va cada campo (C8)
> ```
> Un campo va a 'unknown'  ⟺  su valor es el centinela "UNKNOWN"
> Todo lo demás va a 'known'.
> ```
> **Y nada más.** La versión anterior añadía «o la ficha no lo identifica (no aplica, o
> falta)», y esa coletilla **contradecía a C11**: un campo que **no aplica se omite y no se
> declara hueco**, así que no puede ir a `unknown`. Con la regla central, la equivalencia es
> **exacta y no necesita excepciones**: el valor es el centinela, o el campo está establecido.
> **Esto resuelve el caso que la prueba ciega señaló:** ¿`freshness` con
> `status: "UNKNOWN"` va a `known` o a `unknown`? **A `known`.** El campo **está
> establecido**: lo que se estableció es precisamente que no hay política de vigencia.
> Y su hueco interno se declara en `unknown_detail` con su motivo.
> `unknown` se reserva para el centinela **en el campo mismo** (`"effective_at": "UNKNOWN"`,
> `"quantity": "UNKNOWN"`) o para el campo que la ficha no llega a identificar.
>
> **Sin esta regla la partición era autorreferente**: `known` y `unknown` se cuentan a sí
> mismos, y «¿dónde va `unknown_reason`?» no tenía respuesta. Con C8: `known` y `unknown`
> son campos establecidos por construcción (los escribe el emisor y no valen centinela), así
> que **van a `known`** — junto con `unknown_reason`. Los tres. Siempre.
> **`unknown_detail` NO entra en ninguna de las dos listas** (C7/C9): no es uno de los 22
> campos, es el cuerpo del motivo.
> **Cada uno de los 22 campos está en una lista y solo en una.** Esto es lo que hace que el
> sobre sea verificable de verdad: un lector recorre los 22 nombres y comprueba que ninguno
> falta y ninguno sobra. Un campo que no aparece en ninguna lista es un hueco escondido —
> precisamente lo que este contrato existe para impedir.
>
> **Consecuencia práctica:** no basta con declarar `unknown`. Hay que declarar también
> `known`, porque la afirmación de que *todo lo demás está establecido* es una afirmación
> que también se firma.

**`unknown_reason`** — objeto `{nombre_de_campo: motivo}`, no vacío cuando `unknown` no está vacío

> **v0.3.0/B5 · Cuando `unknown` está vacío, `unknown_reason` es `{}` — y sigue estando.**
> La revisión independiente recomendó **omitirlo** en ese caso. **No se puede, y conviene decir por qué:**
> `unknown_reason` es **uno de los 22 campos**, y los 22 son obligatorios. Omitirlo dejaría
> la ficha con 21, o convertiría el número de campos en condicional — y entonces el conteo
> deja de poder comprobarse, que es justo lo que sostiene C7. **El `{}` no es ruido: es la
> declaración de que no hay nada sin establecer, y se puede comprobar de un vistazo.**

> ### LA REGLA BLOQUEANTE
> ```
> Si unknown no está vacío  →  unknown_reason es OBLIGATORIO y no puede estar vacío.
> ```
> **Un `UNKNOWN` sin motivo es casi tan inútil como un dato inventado.** El motivo dice
> *por qué* no se sabe, y esa diferencia es la que separa «no lo medimos» de «no existe» —
> que es exactamente lo que A3 prohíbe confundir.
>
> **Está en el esquema, no solo aquí.** `allOf[0]` del esquema lo impone con `if/then`:
> si `unknown` tiene al menos un elemento, `unknown_reason` pasa a ser obligatorio y a
> exigir al menos una propiedad. Un validador de JSON Schema lo detecta sin leer prosa.

**`unknown_detail`** — objeto, **OPCIONAL** (no vacío si aparece)

Amplía un motivo hacia **dentro** de un campo compuesto, con notación de punto
(`container.chain_id`, `freshness.valid_until`, `subject.subject_id`).

> **v0.3.0/A4 · No es obligatorio, y la prosa anterior decía lo contrario.**
> v0.2.0 lo llamaba «obligatorio» aquí y el esquema lo dejaba como la única propiedad **no**
> requerida. Las dos cosas no pueden ser verdad: **manda el esquema**, y la prosa se corrige.
>
> **Lo que `unknown_detail` es:** el **cuerpo del motivo**, no una casilla del sobre.
> - **No es uno de los 22 campos** y **no entra** en `known` ni en `unknown` (C7/C9).
> - **Existe cuando hay huecos anidados** —un campo establecido, algo dentro sin establecer—.
> - **Cuando no hay huecos anidados, se omite.** Si aparece, no puede estar vacío.

> **La distinción que resuelve:**
> - **`unknown`** = *el campo no quedó establecido en absoluto.*
> - **`unknown_detail`** = *el campo quedó establecido, pero algo dentro de él no.*
>
> Ejemplo de `examples/03-derived.json`: `container` está en `unknown` porque el agregado no
> tiene un contenedor único; y `container.chain` va a `unknown_detail` porque, además, no se
> sabe qué cadenas entraron en el total.
>
> **Un campo en `unknown` no puede estar también en `known`.** Si el valor se conoce y lo
> que falta es un detalle interno, el campo va a `known` y el detalle a `unknown_detail`.

---

## 5. REGLAS DE VALIDACIÓN

### R. Estructurales (las impone el esquema)

> **v0.4.0/T1 · Estas reglas se llaman `R1`–`R10`, no `A1`–`A10`.** Antes chocaban con los **axiomas
> `A1`–`A5`** de §2: el mismo nombre para dos cosas distintas dentro del mismo documento, de
> modo que una cita a «A3» no se sabía de cuál hablaba. **Los axiomas conservan la letra A**
> porque están citados así en `esquema interno`; **las reglas pasan a R.**
> *(R2 vive en la tabla de coherencia, como B7: se reclasificó al comprobar que el esquema no
> la imponía.)*
>
> **Convención de citas:** las reglas **del contrato** son `R`, `B` y `C` (estas tablas). Las
> **correcciones de las rondas** se citan con su ronda —`v0.3.0/B1`, `v0.4.0/T3`—, para que no
> se confundan con las reglas. Antes no había distinción y el documento **se citaba a sí mismo
> sin saberse de cuál hablaba** (v0.4.0/T1).
>

| # | Regla |
|---|---|
| R1 | Los 22 campos están presentes. |
| R3 | `authority`, `verification_status`, `confidence`, `reconciliation_status`, `source_type`, `subject.type`, `container.type`, `instrument.kind` y `freshness.status` toman valores de su lista cerrada. |
| R4 | `subject` referencia exactamente **un** sujeto. |
| R5 | `container` e `instrument` son objetos distintos y ambos obligatorios (axioma A4). |
| R6 | **El centinela se admite en los 16 campos del HECHO y NUNCA en los 6 del REGISTRO.** Cuáles son unos y otros, y qué nodo lo admite, **lo declara el esquema**. |
| R7 | **Bloqueante:** `unknown` no vacío exige `unknown_reason` no vacío. |
| R8 | `subject_id` admite **las cuatro formas** de §4.1 y su patrón está en el esquema: el identificador de la fuente, una etiqueta `LOCAL:` nuestra, una forma **enmascarada** —con `X`, no con `*` (v0.5.0/X1)— o el centinela. Si el identificador real no queda establecido, se declara en `unknown_detail` con la clave `subject.subject_id`. |
| R9 | `quantity`, cuando tiene valor, es una cadena decimal no negativa (`^(0\|[1-9][0-9]*)(\.[0-9]+)?$`) o el centinela `"UNKNOWN"`. **Nunca un número negativo**: el pasivo va con `instrument.kind = DEBT` y valor absoluto. |
| R10 | **Disuelta la asimetría:** `subject_id` y `container.operator` admiten el centinela **en las mismas condiciones** — las que declara el esquema. En los **22 campos**, «no aplica» se expresa con el centinela; en los **subcampos opcionales**, se omite (v0.5.0/S5). |

### B. De coherencia (las comprueba un tercero al leer)

| # | Regla | Por qué |
|---|---|---|
| B1 | `claim_id` no se repite entre fichas. | Sin esto no hay reconstrucción posible. |
| B2 | `raw_reference` permite localizar el artefacto y `evidence_hash` coincide con él — **salvo el caso declarado en que el artefacto se conoce y no es localizable**: entonces vale el centinela con su motivo, y `confidence` baja (v0.6.0/B5). | Sin esto no hay evidencia, solo afirmación. |
| B3 | `freshness.status = expired` ⇒ la ficha **no** se usa para sostener una conclusión presente. | El dato no se borra; se le quita la fuerza. |
| B4 | `reconciliation_status = disputed` ⇒ la contradicción se registra y se escala; **no** se promedia ni se elige por conveniencia. | Regla dura 2. |
| B5 | `source_type` no se usa como sustituto de calidad (A5). | Un extracto bancario no es «peor» que una cadena; es distinto. |
| B6 | `schema_version` coincide con `VERSION`. | Sin esto la ficha es de una versión indeterminada. |
| B7 | **R2 (reclasificada desde el grupo R).** Ningún campo es nulo ni vacío, salvo los centinelas `"UNKNOWN"` donde se admiten, y salvo el objeto `unknown_reason`, que es `{}` cuando `unknown` está vacío (v0.3.0/B5). | **El esquema no impone «no vacío» de forma global**: lo impone campo a campo donde tiene sentido. Decir que era estructural era falso. |

### C. De la lista `unknown`

| # | Regla |
|---|---|
| C1 | **`unknown` no vacío ⇒ `unknown_reason` obligatorio** (bloqueante). |
| C2 | Cada clave de `unknown_reason` es un campo declarado en `unknown`. **Y al revés: si un campo sale de `unknown`, su motivo se retira de `unknown_reason`.** |
| C3 | Cada motivo es texto no vacío que explica **por qué** no se sabe, no que no se sabe. |
| C4 | **Generalizada a campos compuestos.** Ningún valor —de primer nivel **ni hoja de un campo compuesto**— puede ser cero, `null`, cadena vacía ni un relleno plausible. Lo no establecido vale el **centinela `"UNKNOWN"` cuando el nodo lo admite** — 16 campos del hecho y los subcampos opcionales; **nunca** en los 6 del registro ni en los enums obligatorios. Si el hueco es **interno** —el campo tiene valor pero algo dentro no—, el campo va a `known` y el detalle a `unknown_detail` con su ruta. |
| C5 | `known` y `unknown` no comparten elementos. |
| C6 | `unknown` solo contiene nombres de **primer nivel**. El detalle de un hueco anidado va en `unknown_detail`. |
| C7 | **`known` ∪ `unknown` = los 22 campos, exactamente.** Sin faltantes ni sobrantes. `unknown_detail` no entra: no es uno de los 22. |
> **C8 NO se enuncia aquí** (v0.6.0/A2). Su versión antigua decía «…**o la ficha no lo identifica**», y
> esa coletilla **contradice a C11** —un campo que no aplica no va a `unknown`— y **contradice a §4.6**,
> que ya la había retirado. **La regla vigente está en §4.6**, y es exacta: a `unknown` **si y solo si**
> el valor es el centinela. Se deja constancia del hueco para que una cita antigua a C8 se sepa muerta.
| C9 | `known`, `unknown` y `unknown_reason` **van a `known`** — son establecidos por construcción: los escribe el emisor y **no valen el centinela**. Si algún día valen `"UNKNOWN"` (la regla central lo permite), **van a `unknown` como cualquier otro campo**, y entonces la partición no se puede evaluar: el emisor habrá renunciado a su propia contabilidad. **`unknown_detail` NO va a ninguna de las dos listas**: no es uno de los 22 campos, es el cuerpo del motivo (axioma A1/C7). |
| C11 | **«No aplica» vive en dos niveles (v0.5.0/S5).** En **los 22 campos**, «no aplica» se expresa **con el centinela** — ninguno se omite. En los **subcampos opcionales**, se **omiten** y no se declaran hueco. Es la frontera frente al **axioma A3** (§3). |

> **C10 YA NO EXISTE** (v0.4.0/S2). Era la lista de «qué campos admiten el centinela», y era **la
> causa raíz de tres rondas de fallos**. Con la regla central (§3) **no hay tal lista**: el
> centinela vale en los 22. Se deja constancia del hueco en la numeración para que una cita
> antigua a C10 se sepa muerta, en vez de apuntar a otra regla.

---

## 6. CÓMO EMITIR UNA FICHA — RECETA PARA UN TERCERO

> **La receta repite reglas que ya están en el esquema** —el formato de `claim_id`, la
> partición `known`/`unknown`, qué admite el centinela—. **Es la mayor deuda de este
> documento** y se marca, no se limpia en esta ronda (L-13).

Esta sección existe para cumplir el test de N0: **emitir una ficha compatible leyendo solo
esta spec y el esquema, sin hablar con el autor.**

```
1. claim_id
   Formato obligatorio: <APARATO>-<AAAA>-<NNNN>   p. ej. "LAMC-P1-2026-0001"
   APARATO en mayúsculas, igual que el primer segmento de tu 'producer'.
   NNNN es tu secuencia, monótona, por aparato y año. No lo reutilices jamás,
   ni siquiera para corregir. Para corregir, emite una ficha nueva.

2. subject
   Escribe UN tipo (NATURAL_PERSON | LEGAL_ENTITY | GROUP) y un subject_id.
   Si tu afirmación abarca varios sujetos, PARA: son varias fichas.
   ¿El identificador lo pones tú? Entonces DEBE empezar por "LOCAL:" — es una
   etiqueta, no un dato sobre el mundo — y declaras en unknown_detail que el
   identificador real no está establecido (clave "subject.subject_id").
   ¿Lo aporta una fuente? Se escribe tal cual, sin prefijo.

3. container ≠ instrument   ← el error más frecuente
   container = DÓNDE se observa      (BANK_ACCOUNT, BLOCKCHAIN_WALLET, ...)
   instrument = QUÉ existe ahí       (FIAT_BALANCE/USD, NATIVE/ETH, ...)
   Si no hay instrumento separado, escribe instrument.kind = "NONE".
   Comprueba: ¿tu contenedor es una institución y tu instrumento una moneda?
   Entonces está bien. ¿Son lo mismo? Entonces has violado A4.

4. quantity   ← el campo que faltaba
   CUÁNTO. Cadena decimal, sin moneda y sin fecha:
      "quantity": "4750000"
   La UNIDAD la pone instrument.symbol (USD, ETH...). La FECHA la pone effective_at.
   Nunca negativa: un pasivo va con instrument.kind = "DEBT" y valor absoluto.
   Si no la sabes, escribe "UNKNOWN" y da el motivo abajo. NUNCA un cero, y NUNCA
   el importe metido en prosa dentro de otro campo.

5. source_type / source_reference / capture_method
   source_type = QUE ES la fuente. capture_method = COMO la leíste. De dónde
   exactamente, y un método que otro pueda repetir. Si transcribiste a mano, dilo aquí.

6. observed_at / effective_at
   ¿Cuándo lo viste? ¿Desde cuándo rige? Para un saldo al corte, effective_at ES la
   fecha de corte. Si no sabes lo segundo, "UNKNOWN" y decláralo abajo. NO copies
   observed_at para rellenar.

7. freshness
   status + policy. Si no tienes política de vigencia, status = "UNKNOWN" y el
   hueco se declara. NO copies las políticas que salen como ejemplo en esta spec:
   son ilustraciones del formato, no valores por defecto (v0.3.0/B3).

8. authority / verification_status / confidence
   Tres ejes. No los deduzcas uno del otro.
   authority: si transcribiste un documento, sigue siendo INSTITUTION_DOCUMENT.
   confidence: aplica la rúbrica de 4 criterios (§4.4) y cuenta, no pondera.

9. raw_reference / evidence_hash
   La referencia al crudo, según SU TIPO DE ARTEFACTO (v0.3.0/B8):
      archivo           -> ruta absoluta o URI
      estado de cadena  -> cadena + número de bloque (+ dirección/contrato)
      respuesta de API  -> endpoint completo + la consulta
      documento         -> ruta Y hash
   Y su sha256. Si el crudo es la cadena, el hash es el del bloque.

10. reconciliation_status
    Si no lo has contrastado con nada, es "unreconciled". Es un valor honesto.

11. known / unknown / unknown_reason / unknown_detail
    Recorre los 22 campos. Aplica C8, que ahora es EXACTO: va a `unknown` el campo
    que valga el centinela "UNKNOWN", y todo lo demás a `known` (incluidos `known`,
    `unknown` y `unknown_reason`). Ya no hay que decidir nada más.
    Si `unknown` está vacío, `unknown_reason` es {} — sigue estando, porque es uno
    de los 22 (v0.3.0/B5).
    Y comprueba la SALVAGUARDA (regla 6, §3): al menos UN campo del hecho debe estar
    establecido. Una ficha en la que todo es "no lo sé" no afirma nada y se rechaza.
    `unknown_detail` NO va en ninguna de las dos listas: no es un campo del sobre,
    es el cuerpo del motivo. Va aparte, y solo si hay huecos ANIDADOS (A1/A4).
    Lo que no aplica se omite y no se declara (C11).
    Si `unknown` no está vacío y falta el motivo, tu ficha NO ES VÁLIDA — y es lo
    primero que va a comprobar cualquiera.

12. producer / schema_version
    Formato: <APARATO>[/<componente>][@<versión>]  p. ej. "LAMC-P1/eth-rpc".
    El mismo aparato escribe SIEMPRE el mismo APARATO: no es prosa por ficha.
    Y contra qué versión del sobre. schema_version = "0.2.0".
```

**Comprobación final, en una línea:** si un tercero te pregunta «¿y esto cómo lo sabes?»,
la respuesta debe estar dentro de la ficha. Si tienes que contestar por fuera, la ficha
está incompleta.

---

## 7. DIFERENCIAS QUE EL SOBRE HACE VISIBLES

Estas cuatro filas describen **el mismo hecho económico** visto por cuatro fuentes. En un
esquema ingenuo se sumarían. Aquí no pueden confundirse:

| Fuente | `authority` | `verification_status` | Lo que la ficha admite |
|---|---|---|---|
| Estado de Ethereum | `PUBLIC_CHAIN` | `deterministic` | Cualquiera lo reproduce sin confiar en nadie |
| API del banco | `INSTITUTION` | `authenticated` | Hay que confiar en la institución, y se puede |
| Extracto en PDF | `INSTITUTION_DOCUMENT` | `documentary` | Hay que confiar en el documento, y se puede |
| Frase de una persona | `HUMAN` | `unverified` | Afirmado, sin verificar |

**Ninguna es «mejor» que otra en abstracto (A5).** Pero **no son intercambiables**, y el
sobre obliga a decir cuál es cuál.

---

## 8. QUÉ NO HACE ESTE CONTRATO

- **No valora.** No convierte activos a moneda ni fija tipos de cambio.
- **No puntúa.** No hay riesgo, ni índice, ni ponderación — eso es N8 y está prohibido aquí.
- **No reconcilia.** Registra el estado de contraste; no lo decide.
- **No verifica por ti.** Declara con qué autoridad y cómo se verificó; la verificación es tuya.
- **No expresa ausencia.** No existe la forma «X no existe»: como máximo, «no lo hemos establecido» (A3).
- **No transporta datos personales.** Publica hashes, rutas y referencias; los datos personales se quedan en el artefacto crudo (R-008).

---

## 9. COMPATIBILIDAD Y VERSIONADO

**v0.1.0 fue la primera versión.** Cubría solo lo ya implementado más lo definido en el
charter de P1 (R-007: límite duro contra el sobrediseño).

**v0.2.0 añade un campo obligatorio: `quantity`.** La v0.1.0 describía **la procedencia de
un importe sin tener dónde poner el importe**: podía decir «hay una deuda en USD
documentada por este extracto» y no «la deuda es de 4.750.000 USD». Lo detectó la prueba
ciega de N0, no nosotros. Por la regla 2 de abajo, añadir un campo obligatorio **rompe
compatibilidad**, y por eso sube la versión menor.

**v0.2.0 también cierra 8 hallazgos semánticos** de esa prueba: autoridad de una
transcripción manual, `source_type` vs `capture_method`, rúbrica de `confidence`, `DEBT` y
`operator` en cuentas de crédito, `subject_id` sin centinela, C4 generalizada,
`unknown_detail` como **cuerpo del motivo**, y **OPCIONAL** —es la única propiedad no requerida del esquema— (ver v0.3.0/A4 en §4.6), y en qué
lista va `freshness` con `status = UNKNOWN`.

**Las rondas v0.4.0 y v0.5.0 no cambian la FORMA del sobre: cambian las REGLAS.** El centinela
pasó a admitirse en los campos del hecho, se cerró la partición y se corrigieron las fechas, el
hash y la máscara de los identificadores. **`VERSION` se queda en `0.2.0`, y hay que
justificarlo** en vez de subirlo por inercia:

1. **No se añade ni se quita ningún campo.** Siguen 22. La regla 2 de abajo reserva la subida de
   versión para **añadir un campo obligatorio**, y eso no ocurre.
2. **Casi todo AMPLÍA lo que es válido:** fecha sin hora, máscara con `X`, `keccak256`, y el
   testimonio oral con forma de referencia. **Formas que antes se rechazaban, ahora se aceptan.**
3. **Lo único que se estrecha es una forma que nunca fue legítima.** `unknown: "UNKNOWN"` se
   admitió por error en la ronda v0.4.0 y **anulaba la contabilidad entera**; quitarlo no es
   romper compatibilidad, es **corregir un error** que duró una ronda.
4. **Subir `VERSION` obligaría a tocar los 4 ejemplos** —su `schema_version` debe coincidir con
   `VERSION`—, y **estas órdenes congelan los 4 salvo lo que las Partes 1 y 2 obliguen**. Un
   rótulo no vale romper esa restricción.

> **Si el rótulo nuevo hace falta, son cinco líneas.** No lo decide quien construyó esto.

### (v0.5.0/Q13) «v0.4.0» en este texto NO es la versión del sobre

Son **dos cosas distintas con nombres parecidos**, y confundirlas hace pensar que hay una
contradicción que no existe:

| Nombre | Qué es | Hoy |
|---|---|---|
| `schema_version` (y el archivo `VERSION`) | La versión **del sobre** — del contrato | **`0.2.0`** |
| `vX.Y.0/T1`, `v0.4.0/S2`… | La **ronda de corrección de este documento** | van **cinco** |

**El sobre va por la 0.2.0 y este documento por la quinta ronda de revisión.** No se corrigen
entre sí.

> ### (v0.7.0) La obligación de mantenimiento
>
> **Cuando una regla mecánica cambie, hay que actualizar LOS DOS SITIOS — el esquema y su resumen
> en la prosa — en el mismo acto.**
> **Un cambio en uno solo es un DEFECTO, no una mejora.**
> **El verificador del programa comprueba que coincidan.**
>
> *(El defecto que produjo cinco rondas no se arregla con una limpieza: se arregla con esta regla.)*

**Reglas de evolución:**

1. **La versión es la del sobre, no la del emisor.** `schema_version` en la ficha debe
   coincidir con `VERSION`.
2. **Añadir un campo obligatorio rompe compatibilidad.** Va a `v0.2.0`, con justificación
   escrita, y los emisores anteriores quedan marcados incompatibles.
3. **`14 → 21 → 22` ya ocurrió.** Primero por un rótulo mal contado (F-1), después por un
   campo que **faltaba de verdad** (F-5). `ESTABILIDAD_DEL_SOBRE = UNKNOWN`: no hay análisis
   de si 22 campos son los correctos. **Cada campo nuevo exige justificación escrita**, y
   `quantity` la tiene: sin él el sobre no puede expresar una cifra.
4. **Nada se elimina dentro de la misma versión mayor.** Una ficha emitida contra `v0.1.0`
   sigue siendo legible.

---

## 10. LÍMITES Y HALLAZGOS DECLARADOS

Nada de esto se resuelve por inferencia. Se declara.

### Hallazgos

**F-1 · El sobre se llama «de 14 campos» y tiene 21.**
La fuente original (`documento interno de propuesta` §5,
líneas 162–197) enumera **21** campos. La cifra «14» viajó a siete documentos y a la
herramienta de verificación sin contrastarse con la fuente (caso que motivó la regla
9.quater de `esquema interno`). **La v0.2.0 implementa 22**, y el esquema marca los 22 como
`required`: los 21 de la fuente más `quantity` (F-5).
**Estado:** la revisión independiente corrigió la herramienta y los rótulos el 2026-09-21 (F-3). La
versión inicial de `validar_evidencia.py` solo exigía 14 campos y **no comprobaba 7**
(`evidence_hash`, `reconciliation_status`, `known`, `unknown`, `unknown_reason`, `producer`,
`schema_version`), de modo que habría emitido un `APROBADO` falso. Era un hueco de la
herramienta, no del contrato.
**Residuo:** quedan **dos** referencias obsoletas — la contradicción interna de
una página de síntesis interna (dice 14 en la línea 256 y 21 en las
líneas 37, 53 y 238) y una entrada histórica de `registro interno`, que **no se edita** porque el
log es append-only.

**F-5 · El sobre no tenía campo para el IMPORTE — defecto arquitectónico.**
La **prueba ciega de N0** (agente sin contexto, con solo esta spec y el esquema) lo
encontró: podía describirse la procedencia de un importe, pero no el importe. El agente
tuvo que **meter la cifra y la fecha de corte en prosa dentro de `capture_method`** — fuera
de todo campo.
**Corregido en v0.2.0** con un solo campo plano, `quantity`, y aclarando en la spec que la
unidad es `instrument.symbol` y que la fecha de corte es `effective_at`. **No se añadió ni
la moneda ni la fecha como campos**, precisamente porque ya existían.
**Origen:** el defecto venía de la arquitectura aprobada en HG-004 (21 campos), no de P1,
que implementó fielmente lo que se le dio. **HG-010 autorizó la corrección.**

**F-6 · Ocho hallazgos semánticos de la misma prueba ciega.** Resueltos en v0.2.0 y
documentados arriba: autoridad de la transcripción manual (§4.4), `source_type` vs
`capture_method` (§4.2), rúbrica de `confidence` (§4.4), `DEBT` y `operator` en cuentas de
crédito (§4.2), `subject_id` sin centinela (v0.3.0/A8), C4 generalizada a campos compuestos,
`unknown_detail` como cuerpo del motivo (§4.6) y la regla C8 para `freshness.status = UNKNOWN`.

**F-8 · Segunda prueba ciega: 15 correcciones (5 contradicciones, 9 ambigüedades, 1 hueco).**
La segunda ronda de correcciones (`orden de corrección interna v0.3.0`) encontró **cinco contradicciones
internas** —el documento diciendo dos cosas a la vez—, **nueve ambigüedades** que obligaban a
inventar o a juzgar sin regla, y **un hueco de diseño** que se resolvió **sin añadir campo**
(C1). La lección de método: **el contrato crecía en campos mientras seguía contradiciéndose
por dentro**, y fue un agente sin contexto quien lo vio. Tabla de resoluciones y líneas
exactas: `estado interno`, sección «Tabla L-10».

**F-7 · Tres defectos propios, encontrados por la comprobación independiente al pasar a v0.2.0.**
(1) La ficha `02` tenía `freshness` en `unknown`, cuando su valor **no** es el centinela sino un
objeto establecido: por la regla C8 que la propia v0.2.0 define, iba a `known`. (2) Al moverlo,
quedó un **motivo huérfano** en `unknown_reason` —violando C2— que la herramienta del programa
**no detecta** y sí detectó la comprobación independiente. (3) El apartado 6 de esa misma
comprobación usaba una ficha con `unknown` vacío, de modo que **la regla bloqueante no se
disparaba y el test se autoanulaba**: un test que no puede fallar no prueba nada.
**Los tres corregidos.** El (2) y el (3) son la misma lección que C5/C6/C7 en v0.1.0: **una
comprobación permisiva da confianza falsa.**

**F-9 · Tres rondas peleando contra una lista que no debía existir (v0.4.0).**
La causa raíz de las tres rondas anteriores era **la lista de «qué campos admiten el
centinela»**: siete elegidos a mano. Cada caso real encontraba el octavo, y la salida era
**inventar un valor con forma de dato** — exactamente lo que el programa existe para impedir.
**El operador lo cortó de raíz (HG-011): «No lo sé es válido». El centinela vale en los 22, y
la lista desaparece.** Eso **disuelve de golpe** cinco callejones sin salida
(`evidence_hash`, `source_reference`/`raw_reference`, `freshness.policy`, `observed_at` y
**L-5**) que se llevaban tres rondas intentando arreglar uno a uno.
**La lección:** cuando la misma clase de defecto vuelve tres veces, el defecto no está en los
casos — está en **la regla que los obliga a existir**.

**F-12 · La regla del centinela se aplicó a medias, y las tres formas del error (v0.5.0).**
En la ronda v0.4.0 se dijo **«el centinela vale en cualquiera de los 22 campos»** — y era falso
**en tres sentidos a la vez**: **me pasé** (incluir `known`, `unknown` y `claim_id` **anulaba la
contabilidad entera**: `unknown: "UNKNOWN"` **evadía la regla bloqueante**), **me quedé corto**
(seis subcampos que la prosa decía que lo admitían **no lo admitían**), y **no lo cerré** (los
enums obligatorios no lo admiten y la prosa no lo aclaraba, así que parecía una contradicción
en vez de un borde).
**La lección —y es la tercera vez que aparece la misma forma—:** una regla **enunciada en prosa**
y **aplicada a mano campo por campo** se desalinea siempre. **De ahí L-13:** la regla vive en el
esquema, y la prosa explica y remite.
**Y una segunda lección:** un **borde** declarado (no puedo decir «sé que es una cuenta pero no
de qué clase») **no es una contradicción** — es una limitación, y se escribe (L-7).

**F-2 · El `contrato interno del proyecto` §8 se contradice.** Dice «Comprueba: 1…2…3…4» y a continuación
«los **6** pasos» y «los 6 comandos de validación», cuando el comando real es **uno**.
Se reporta; no se corrige sin autorización, porque es texto de gobernanza.

**F-3 · La herramienta de verificación cambió durante la sesión.**
Cuando este chat empezó a trabajar, `herramientas/validar_evidencia.py` exigía 14 campos y
terminaba su salida con «los 3 bloques pasan» pese a tener 4. A mitad de sesión fue
sustituida: ahora exige los **21**, cuenta **fichas** (no archivos), admite varias fichas
dentro de un archivo y añade un bloque 4. **Este entregable se validó contra la versión
corregida.** El archivo concreto que validó queda identificado por su hash en `estado interno`,
no por su fecha ni su tamaño: una fecha de modificación no dice nada sobre lo que el programa
hace.
**Consecuencia declarada:** el resultado `APROBADO` de esta sesión pertenece a esa versión
concreta de la herramienta. Si la herramienta vuelve a cambiar, la validación debe repetirse.
Por eso este chat ejecutó además una **comprobación independiente** que no usa la herramienta
del programa: lee el esquema, extrae su condicional `if/then` y lo evalúa por su cuenta
(§12).

**F-4 · Dos defectos propios, encontrados y corregidos antes de reportar.**
(1) `examples/03-derived.json` listaba `instrument` en `known` **y** en `unknown` a la vez:
una contradicción interna que la herramienta del programa **no** detectaba. (2) El mismo
ejemplo usaba notación de punto (`container.container_id`) dentro de `unknown_reason`, donde
la regla C2 solo admite nombres de primer nivel. Ambos se corrigieron, y de ahí nacieron las
reglas C6 y C7.

### Limitaciones declaradas

> **L-7, L-8 y L-9 se consolidaron** en la sección siguiente como **C4, C2 y C5** (v0.6.0): eran las mismas limitaciones dichas en dos sitios.

**L-1 · CORREGIDA: la red a RPC público no está bloqueada.** (v0.2.0)
En v0.1.0 se declaró que la red saliente a RPC público respondía **HTTP 403**. **La
declaración era incorrecta y se retira.** La revisión independiente lo verificó y quien construyó el entregable lo confirmó
después: probando **endpoints distintos**, seis responden con normalidad.
El error fue de método: se probaron tres endpoints concretos, los tres caídos, y se
generalizó a «la red está bloqueada» — que es exactamente **afirmar por muestra insuficiente**.
**Lo que ha cambiado en v0.2.0:** el ejemplo 01 ya **no** dice «no se pudo verificar». Se
leyó en vivo por RPC, con bloque y hash citados, y **cualquiera puede repetir la consulta**.
**Regla que produce:** una comprobación fallida en N puntos **no autoriza** la conclusión
«no se puede». Se escribe `UNKNOWN` acotado: «con estos endpoints y en este momento, no
respondió», y se declara la muestra.

**L-2 · `unknown` solo admite nombres de campo de primer nivel.**
No se puede escribir `unknown: ["container.chain_id"]`. Por eso existe `unknown_detail`,
que recoge el hueco anidado sin debilitar la regla bloqueante, que sigue anclada a
`unknown_reason`.

**L-6 · `quantity` no dice si la cifra es un saldo o un flujo.** (NUEVA en v0.2.0)
El campo expresa una cantidad **a una fecha** (un saldo, un valor), no un movimiento entre
dos fechas. Para un flujo harían falta dos fechas. No se añade: el charter de P1 es N0 y
la prueba ciega no lo pidió. **Marcar para cuando aparezca un caso real.**

**L-3 · `known` y `unknown` no los valida la herramienta del programa.**
`validar_evidencia.py` comprueba que los 22 campos existan y que `unknown` no vaya sin
motivo, pero **no** comprueba C2 (que todo motivo corresponda a un campo de `unknown`),
C5 (sin elementos compartidos), C6 (sin rutas anidadas en `unknown`) ni C7 (partición exacta
de los 22 campos). En esta sesión esas **cuatro** reglas las
verificó la **comprobación independiente** descrita en §12, que no forma parte de la
herramienta oficial. **Es el candidato natural a incorporarse a la herramienta**, y mientras
no se incorpore, C5/C6/C7 dependen de esa comprobación auxiliar.

**L-4 · Los cuatro ejemplos son fichas individuales, no un conjunto reconciliado.**
El contrato se demuestra sobre fichas sueltas. La reconstrucción de un portafolio es N1–N2
(P2), no N0.

**L-5 · RESUELTA — `container` agregado (v0.4.0).**
En `examples/03-derived.json`, `container` figuraba en `unknown` **y a la vez llevaba un valor
completo**: una contradicción real que el validador anterior no podía ver y **el nuevo sí**
(`'container' tiene valor pero no figura en 'known'`). La destapó **la regla nueva** al hacer
la equivalencia exacta: **si el campo tiene valor, está establecido, y va a `known`.**
**Arreglado:** `container` pasa a `known`; lo que **no** está establecido —**qué cadenas**
entran en el agregado— vive en `unknown_detail` con su ruta (`container.chain`); y su
`container_id` es una etiqueta nuestra, marcada **`LOCAL:`**. **Ya no es una limitación
abierta: es un caso resuelto y cubierto por un ejemplo.**

### (v0.5.0/L-13) UNA SOLA FUENTE DE VERDAD — las reglas viven en el esquema

**El esquema manda y la prosa explica y resume** (§1). Lo que esta sección añade es **por qué**.

**Por qué.** Cinco rondas fallaron por lo mismo: **la regla vivía en dos sitios y se
desalineaban**. Cada vez que se arreglaba uno, el otro se quedaba atrás.

**Y una corrección de criterio (v0.7.0).** En la ronda anterior se dijo que **repetir una regla
en la prosa era un DEFECTO**, y se marcaron **21 sitios** para borrarlos. **Era un error:** la
mayoría de esas reglas son **las tablas que hacen legible el documento** —los 22 campos, las
autoridades, la rúbrica, la partición de las dos listas—, y borrarlas obligaría a **abrir el
esquema para todo**. **Lo que falló nunca fue que la prosa repita reglas: fue que la prosa y el
esquema se CONTRADIJERAN.** Así que la limpieza correcta no es borrar: es **verificar que
coincidan** — y eso está hecho, punto por punto, para los 21. **La obligación de mantenerlos
alineados está escrita en §9.**

---

### Limitaciones conocidas de v0.2.0

**Estas NO son errores: son bordes conocidos.** Van escritas para que **nadie las descubra por
sorpresa**. *(Las que ya estaban declaradas como L-7, L-8 y L-9 se consolidaron aquí como C4,
C2 y C5: eran las mismas, dichas dos veces.)*

**C1 · «Válida» significa «conforme al sobre». NO significa «usable como evidencia».**
Una ficha puede ser **conforme al sobre** y tener un respaldo **incitable** —el caso en que el
artefacto se conoce pero no se puede localizar, con `raw_reference` en el centinela (v0.6.0/B5)—.
**`confidence` debe reflejarlo** y no puede ser `high`. **El contrato garantiza la FORMA de la
evidencia, no su FUERZA.**

**C2 · Las cifras aproximadas no tienen campo propio.**
Si la fuente dice «como dos millones», **no hay forma de escribir la cifra sin afirmar una
exactitud que la fuente no dio**. **La aproximación va en el motivo del hueco, no en el valor:**
`quantity = "UNKNOWN"` + *«la fuente dijo aproximadamente 2.000.000 USD»*. **No se añade campo**:
si algún día un caso real lo exige, se añade entonces.

**C3 · No hay campo para la CONTRAPARTE de una deuda sin contenedor.**
En una deuda oral, **el acreedor no tiene dónde ir**: su único alojamiento posible era
`container.operator`, y **no hay contenedor**. Se declara en vez de forzar un contenedor falso.

**C4 · Conocimiento parcial DENTRO de un objeto compuesto.**
Si no sabes **de qué tipo** es el contenedor, **el objeto entero vale `"UNKNOWN"`** — no un
objeto con el tipo sin establecer. **No se puede declarar «sé el número pero no el tipo».**
*(`freshness.status` es un caso declarado y distinto: su `"UNKNOWN"` significa «no se estableció
la política de vigencia», que es una afirmación útil, no conocimiento parcial del tipo.)*

**C5 · `schema_version` no lo puede verificar un tercero ciego.**
La prueba prohíbe leer `VERSION`, así que el emisor lo toma de la prosa. **Es un límite de la
PRUEBA, no del contrato.** Se anota para que no se confunda con un defecto del documento.

---

### Incertidumbres heredadas

```
ESTABILIDAD_DEL_SOBRE_DE_22_CAMPOS   = UNKNOWN
FRESHNESS_ENFORCEMENT                = OPEN
RECONCILIATION_RULES                 = OPEN   (el contrato registra el estado, no lo decide)
```

---

## 11. PROCEDENCIA DE CADA CAMPO

> **Nota para el lector de fuera.** Varias fuentes de esta tabla —`plan interno`,
> `contrato interno del proyecto`, `esquema interno`, `encargo interno`, la *el documento interno de propuesta*— son documentos
> internos del programa LAMC y **no se publican**. Se citan igualmente porque cada regla de
> este contrato puede rastrearse hasta el documento y la línea que la originaron: **la
> trazabilidad es lo que permite auditar el contrato en vez de tener que creer en él.**
> Que una fuente no sea pública no la vuelve invisible: la vuelve **no comprobable por el
> lector**, y eso se declara aquí en vez de disimularse.

Tabla de trazabilidad (misión M-P1-01: campo → fuente).

| Campo | Fuente autoritativa |
|---|---|
| Los **21** campos y su orden | `documento interno de propuesta` §5, líneas 162–197 |
| El **22.º**, `quantity` | **No viene de la fuente: se añadió en v0.2.0.** Propuesta de la revisión independiente en HG-010, simplificada por el operador (D-014) a un campo plano; defecto detectado por la prueba ciega de N0 (F-5) |
| Las 22 como `required` | `plan interno` §2.1 · `contrato interno del proyecto` §3 · `encargo interno` (bloque del sobre), con `quantity` añadido en v0.2.0 |
| `authority` (5 valores) | el documento interno de propuesta §5 (líneas 201–219) · `contrato interno del proyecto` §5 |
| `verification_status` (4 valores) | el documento interno de propuesta §5 · `contrato interno del proyecto` §5 |
| `source_type` (11 valores) | el documento interno de propuesta §6 (líneas 223–255) · `contrato interno del proyecto` §5 |
| `subject` (3 tipos) | `plan interno` §2.2 · `contrato interno del proyecto` §4 |
| `container` (9 subtipos) | el documento interno de propuesta §4, líneas 127–156 |
| `container ≠ instrument` (A4) | `plan interno` §1 · el documento interno de propuesta §4, línea 147 |
| `observed_at ≠ effective_at` | `contrato interno del proyecto` §3 · `encargo interno` |
| `freshness` vencida no sostiene conclusión | `contrato interno del proyecto` §3 · `encargo interno` |
| `reconciliation_status` (3 valores) | `encargo interno` |
| `unknown_reason` obligatorio | `plan interno` §2.1 · `contrato interno del proyecto` §6 · A1/A3 de `esquema interno` §1.bis |
| Axiomas A1–A5 | `esquema interno` §1.bis · `plan interno` §1 |
| Datos de los ejemplos 01 y 03 | Informe interno de observabilidad del programa LAMC (§D, §H.1, §C, §E, §G) — **documento privado, no publicado** |
| Documento crudo del ejemplo 02 | Extracto bancario privado — **no publicado**; el ejemplo lo referencia por su hash |

**Huecos de procedencia declarados:** `known` / `unknown` / `unknown_reason` como **listas
de nombres de campo** aparecen en `plan interno` §2.1 y en el charter como campos del
sobre, pero **ningún documento del programa define su estructura interna**. La estructura
adoptada aquí (listas de nombres de campo + objeto de motivos) es una **decisión de
implementación**, no una transcripción. Queda marcada para que el checker la revise.

---

## 12. COMPROBACIÓN INDEPENDIENTE

La validación determinística oficial es una sola:

```
python3 herramientas/validar_evidencia.py .        # desde la raíz del repositorio
```

**Esa comprobación tiene un límite conocido** (L-3): no verifica C5, C6 ni C7, y no
comprueba que la regla bloqueante esté realmente **expresada en el esquema** — se conforma
con comprobar los datos.

Por eso este entregable se sometió además a una **comprobación independiente**, que **no usa
la herramienta del programa**. Hace **nueve** cosas:

| # | Comprueba |
|---|---|
| 1 | `required` ⊆ `properties`, 22 campos obligatorios, y `unknown_detail` como único no-obligatorio (A4) |
| 2 | Que las enumeraciones del esquema coinciden con las del charter (authority, verification_status, confidence, reconciliation_status, subject.type) |
| 3 | Que el condicional `if/then` **existe en el esquema** y exige `unknown_reason` no vacío |
| 4 | Que ese condicional **se dispara** sobre las cuatro fichas reales, evaluándolo sin usar el validador |
| 5 | Que el esquema **rechaza** una ficha con `unknown` y sin motivo, y otra con motivo vacío |
| 6 | Centinelas, `schema_version` = `VERSION`, C5, C6 y C7 sobre cada ficha |
| 7 | **La partición del centinela, derivada recorriendo el esquema**: los **16 campos del hecho lo admiten** y los **6 del registro NO** (v0.5.0/S1 y S2), derivado del propio esquema y no de una lista escrita a mano |
| 8 | **Los 6 subcampos opcionales lo admiten** (`chain`, `chain_id`, `contract_address`, `token_id`, `label`, `policy`) y **los 3 enums obligatorios NO** (v0.5.0/S3 y S4) |
| 9 | **Que `known`/`unknown` del esquema son exactamente los 22 campos** y que `unknown_detail` no está en ninguno. Y las convenciones: `LOCAL:` declarado, prefijo de `claim_id` = aparato de `producer`, máscara con `X` (no `*`), y las fechas con la precisión que la fuente dio (v0.5.0/X1 e I1) |

**Resultado: `APROBADO — contrato coherente`.**

> **Esta comprobación no sustituye al checker independiente.** La hizo el propio Maker: es
> una *autocomprobación*, y por definición no puede contar como verificación por pares. Vale
> como evidencia de que las reglas están donde se dice que están — no como `PASS`.

**Y un efecto secundario que importa:** la comprobación encontró **dos defectos reales** en
el ejemplo 03 que la herramienta oficial **no detectaba** (F-4). Eso mide, mejor que ninguna
afirmación, para qué sirve tener dos comprobaciones distintas.
