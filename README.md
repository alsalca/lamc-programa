# Evidence Envelope

### La ficha común de evidencia financiera

**Versión 0.2.0** · Licencia Apache-2.0

> **Este repositorio es el programa LAMC.**
> LAMC no es un sistema de criptomonedas: es un **método** para reconstruir, normalizar y
> conciliar evidencia financiera de fuentes heterogéneas. **Lo primero que publica es esto**
> — el formato que hace posibles los pasos siguientes. Qué viene después, al final, en
> *El programa y lo que falta*.

---

## El problema, en tres frases

Dos documentos oficiales pueden decir el mismo día que una cuenta tiene **24.817 dólares** y
**0 dólares**, y los dos pueden estar "bien". Un sistema puede marcar la misma operación como
**APROBADA** y **FALLIDA** el mismo día. Y una auditoría puede citar respaldos **que no
existen**, sin que nada la detenga.

Nada de eso es fraude. Es un problema de **formato**: hoy no hay manera de escribir, de forma
que un ordenador lo entienda, la diferencia entre *lo verifiqué* y *me lo contaron*, entre
*no hay nada* y *no lo he mirado*, entre *es de hoy* y *es de hace ocho meses*.

**Evidence Envelope es ese formato.** Una ficha de 22 casillas que obliga a declarar qué se
sabe, qué no, y con qué respaldo se afirma.

---

## La idea que lo hace distinto

Casi todos los formatos de datos obligan a rellenar. Como no se puede rellenar lo que no se
sabe, la gente escribe un **cero**, o una suposición razonable, y **ese dato falso viaja para
siempre** por el resto del sistema.

Este contrato hace lo contrario: **el hueco es un valor legal.**

```
En cualquiera de las 16 casillas de hecho se puede escribir  UNKNOWN
                                                  («aún no establecido»)
Con una condición: hay que escribir POR QUÉ.
Sin el motivo, la ficha es inválida.
```

`UNKNOWN` **no es cero**. Cero es una medición: *miré y no había nada*. `UNKNOWN` es la
ausencia de medición. Confundirlos es el error más caro de todo el registro financiero, y
este contrato lo hace imposible de escribir.

Y hay una segunda lista que se firma junto a la primera —las casillas que **sí** quedaron
establecidas—. Las dos juntas tienen que cubrir las 22 casillas **exactamente**: sin faltar
ninguna, sin repetirse. Si una casilla no aparece en ninguna de las dos, la ficha está mal
formada y **cualquier verificador lo detecta**. No hay huecos escondidos.

---

## Un ejemplo

Un lunar. Dos médicos lo miran:

- Uno **lo ve a simple vista**: «parece benigno».
- Otro **hace una biopsia**: «es benigno, con estas tinciones, en este laboratorio».

Las dos frases dicen lo mismo. **No valen lo mismo.** Un sistema que las guarde juntas sin
distinguirlas es un sistema que va a fallar.

Con dinero pasa igual:

| Quién afirma | Cómo se comprueba | Cuánto puedes confiar |
|---|---|---|
| **La cadena de Ethereum** | Cualquiera, solo, sin confiar en nadie | Es verificable por cualquiera |
| **Un banco** | Hay que confiar en el banco, pero el banco responde | Es responsable de su dato |
| **Un PDF de extracto** | Hay que confiar en el papel | El papel se puede adulterar |
| **Una persona, de memoria** | — | Puede ser cierto. No está verificado |

Los cuatro son fichas válidas. **Dicen cosas distintas, y la ficha obliga a escribirlo.**

---

## Úsalo en 30 segundos

No hay nada que instalar. Se necesita Python 3, y nada más — ni una dependencia.

```bash
git clone <este-repositorio>
cd evidence-envelope
python3 herramientas/validar_evidencia.py .
```

Debe terminar en `RESULTADO: APROBADO`. Los cuatro archivos de `entregables/examples/` pasan la comprobación; el verificador los mide
contra el esquema, campo por campo.

**Las cuatro fichas están anonimizadas y ninguna describe a nadie.** Dos son lecturas reales
de la cadena sobre direcciones **vacías, generadas al azar** —no pertenecen a ninguna persona—;
una describe un extracto **sintético** que se publica cifrado; y la cuarta es un caso con las
cifras, la fecha y los activos **sustituidos**. La declaración de anonimización de cada ficha
vive en el **anexo final de `entregables/SPEC.md`** («Anexo — Los cuatro ejemplos, explicados»),
**no en un campo de la ficha**: el esquema no tiene ningún campo `anonymization` y una clave
así sería rechazada.

> **CORRECCIÓN 2026-09-25:** aquí decía «Cada ficha lo declara en su propio campo
> `anonymization`». **Era falso:** `grep -c anonymization` sobre los cuatro ejemplos da **0** en
> los cuatro. La nota de anonimización se movió al anexo del `SPEC.md` cuando los ejemplos
> dejaron de llevar casillas que el esquema no admite.

**Para escribir tu propia ficha:** lee `entregables/SPEC.md` y copia la ficha de `entregables/examples/` que más se
parezca a tu caso. El verificador te dirá qué falta.

### Lo que la herramienta comprueba

- Que estén las **22 casillas**, todas, sin vacíos —salvo `unknown` y `unknown_reason`, que **sí
  pueden ir vacíos a propósito** cuando no hay nada sin establecer
- Que `UNKNOWN` se use donde está permitido —y **solo** donde está permitido—: la herramienta
  lo rechaza de forma expresa en los **seis campos del registro** (`claim_id`, `known`,
  `unknown`, `unknown_reason`, `producer`, `schema_version`), y comprueba **todas las listas
  cerradas del esquema, en cualquier nivel**, **los patrones** (`claim_id`, `schema_version`) y
  las claves que el contrato no admite. **El esquema, por sí solo, no impide el centinela en
  `producer`** (es una cadena libre): ese hueco está declarado en `SPEC.md` (§5) y lo cubre la
  herramienta
- Que cada valor de la lista "establecido" sea realmente un valor, y cada hueco tenga motivo
- Que las dos listas cubran las 22 casillas sin solaparse y sin dejar ninguna fuera
- Que los valores cerrados (autoridad, estado de verificación, confianza) sean de la lista
- Que **no haya ninguna casilla de más**: el contrato declara `additionalProperties: false`,
  así que una clave que el esquema no define —en la raíz o dentro de `subject`, `container`,
  `instrument` o `freshness`— hace fallar la comprobación

> **CORRECCIÓN 2026-09-25 · dos matices del alcance.** (1) Aquí decía «las 22 casillas, todas, y
> **ninguna vacía**»; **la herramienta exime a `unknown` y `unknown_reason`**, que pueden ir
> vacíos a propósito. (2) Decía «`UNKNOWN` … y **solo** donde está permitido» sin precisar el
> alcance; ahora se dice el real: la herramienta lo rechaza en los seis campos del registro,
> comprueba las listas cerradas y los patrones, pero **no es un validador JSON Schema completo**
> — el hueco del esquema en `producer` lo cubre ella, no el esquema (ver `SPEC.md` §5).

> **CORRECCIÓN 2026-09-25 (auditoría, revisión 2, hallazgo 2).** Aquí decía, como algo que la
> herramienta comprueba, «que haya al menos **tres fichas y dos autoridades distintas**».
> **Era verdad con la versión anterior y dejó de serlo con la corregida**, que declara esos
> mínimos por proyecto en un registro interno que **este paquete no lleva**. La línea se
> sustituye por la comprobación que sí hace —y que antes **no** hacía: la de las casillas de
> más, que es la que faltaba y la que motivó la corrección.
>
> **Los mínimos, tal como salen hoy en este paquete:** la herramienta los informa como
> **«no exigido»** y dice cuántos hay. Es deliberado: prefiere decir **«no se le pedía»** a
> aprobar en silencio. **Lo que este paquete SÍ trae, y puedes contar tú mismo:** 4 ejemplos
> y 4 autoridades distintas (`PUBLIC_CHAIN`, `INSTITUTION_DOCUMENT`, `INSTITUTION`, `DERIVED`).

---

## Lo que este contrato garantiza — y lo que no

Esto importa más que todo lo anterior, y conviene decirlo sin adornos.

> **La ficha garantiza la FORMA de la evidencia, no su FUERZA.**

Que una ficha sea **válida** significa que **cumple el formato**. No significa que lo que dice
sea cierto, ni que su respaldo sea bueno. Se puede escribir una ficha perfectamente válida
apoyada en un documento que nadie debería aceptar — y la ficha lo dirá, si está bien hecha,
en su propia casilla de confianza.

El contrato obliga a **declarar**. No obliga a **tener razón**. Un formato no puede sustituir
al juicio; solo puede impedir que el juicio se haga sobre datos falseados.

Esto es deliberado. Un estándar que prometiera más que eso sería mentira.

---

## Estado: esto es el primer peldaño

**Versión 0.2.0.** El contrato está terminado, probado y verificado. **No hay nada construido
encima.** No hay lector de datos, ni motor de cálculo, ni comparación entre instituciones, ni
puntuación de riesgo. Nada de eso se construye hasta que este peldaño pase su prueba.

Y la prueba es esta:

> **¿Un tercero que nunca habló con el autor puede rellenar una ficha compatible leyendo
> solo el manual y el esquema?**

Se ha probado cinco veces con agentes sin ningún contexto previo. Las cinco veces encontraron
defectos reales. La quinta, **ningún valor inventado**.

**No hay todavía ninguna institución usándolo.** Si estás leyendo esto y te interesa, esa es
exactamente la conversación que falta.

### Limitaciones conocidas, declaradas

Se declaran aquí en vez de esconderlas. **Estas cinco son las que afectan a quien decide
adoptarlo.** La especificación declara además **sus propios bordes técnicos** —la sección
*Limitaciones conocidas de v0.2.0* de `SPEC.md`, numerados **LIM-1 a LIM-5**; se renombraron
desde `C1`–`C5` el 2026-09-25 para no chocar con las reglas `C` de §5—, que son otros cinco y
distintos: los de aquí son de uso, los de allí son del contrato.

> *(Corrección 2026-09-25. Aquí decía «Están **en detalle** en `SPEC.md`, sección Limitaciones
> conocidas de v0.2.0», dando a entender que eran **las mismas cinco, con más detalle**. No lo
> son: son **dos listas distintas y sin un solo punto en común.** Una referencia que promete
> equivalencia y entrega otra cosa es peor que no referenciar — quien la sigue cree haber
> leído lo que no leyó.)*

- **El sobre puede necesitar más casillas, o menos.** Un formulario de **22 casillas** es
  riesgo de que se vuelva inmanejable. Y la historia no tranquiliza: el número ya cambió
  **dos veces** (`14 → 21 → 22`, contado en `SPEC.md` §9), y la última fue porque **faltaba
  una casilla de verdad**.

  > **CORRECCIÓN 2026-09-25.** Aquí decía «**22 casillas por 12 dominios**». **Nada en el
  > documento define ni cuenta 12 dominios**: el `SPEC.md` agrupa los 22 campos en **6 bloques**
  > (§4). La cifra era un número que nadie podía comprobar y se retira. Y decía «el número ya
  > cambió **tres veces**»; contados en la fuente son **dos** cambios (`14 → 21 → 22`), no tres.
- **El contrato declara la vigencia; que el sistema la respete es otra cosa.** Eso no está
  construido.
- **Una ficha expresa una cantidad a una fecha — no distingue un saldo de un movimiento.**
  Un flujo entre dos fechas necesitaría dos fechas, y eso no está. No se añade hasta que un
  caso real lo pida.
- **Los ejemplos de saldo en cadena caducan por diseño.** Pasada su vigencia siguen siendo
  ciertos *para aquel bloque*, pero ya no describen el presente.
- **Las fichas son sueltas**, no un portafolio reconstruido. Ese es el peldaño siguiente.

---

## Contenido

| Archivo | Qué es |
|---|---|
| `entregables/SPEC.md` | **El manual técnico.** Qué significa cada una de las 22 casillas y cómo rellenarla |
| `entregables/evidence-envelope.schema.json` | El contrato, en formato que un ordenador comprueba |
| `PORQUE.md` | El problema de mercado que lo motiva, con las cifras y sus fuentes |
| `entregables/examples/01-public-chain.json` | Ficha de un saldo en la cadena de Ethereum |
| `entregables/examples/02-institution-document.json` | Ficha de un extracto bancario — **con la cifra en «aún no establecido»** |
| `entregables/examples/03-derived.json` | Ficha de un total calculado por nosotros |
| `entregables/examples/04-institution-api.json` | Ficha de un dato que responde por nosotros una institución |
| `entregables/adjuntos/02-extracto-ejemplo.pdf.enc` | El documento **sintético y cifrado** que cita el ejemplo 02. Se publica para que su hash sea comprobable; la contraseña no |
| `entregables/adjuntos/03-informe-ejemplo.txt` | El documento **sintético** que cita el ejemplo 03. Se publica **entero** para que su hash y su contenido sean comprobables |
| `herramientas/validar_evidencia.py` | El verificador. Sin dependencias |
| `herramientas/comprobar_coincidencia.py` | Comprueba que el manual y el esquema no se contradigan. Es una **heurística**, no una garantía |
| `proyectos/` | Los dos proyectos de ejemplo publicados (P2 y P3), cada uno con su `CHARTER.md`: el contrato aplicado fuera de P1 |
| `README.en.md` | Resumen en inglés de este `README.md`; ante cualquier diferencia, **manda el español** |
| `SELLOS.txt` | El SHA-256 de cada archivo publicado. Se comprueba con `sha256sum -c SELLOS.txt` |
| `CHANGELOG.md` | Qué cambió en cada versión y por qué |
| `CONTRIBUIR.md` | Cómo proponer un cambio |
| `entregables/VERSION` · `entregables/LICENSE` | `0.2.0` · Apache-2.0 |

**Los cuatro ejemplos son de autoridades distintas a propósito:** uno de cadena pública, uno
de documento de institución, uno calculado por nosotros y uno de una institución que responde
por el dato. Cuatro fichas de la misma autoridad no demostrarían nada.

**El ejemplo 02 es el más útil de los cuatro.** El extracto está **cifrado**: no se puede abrir
sin contraseña, así que la cifra no se pudo leer. La ficha **declara el hueco con su motivo** en
vez de rellenarlo con un cero. Enseña qué hace el contrato cuando todavía no sabe cuánto — que
es el caso normal, no la excepción.

**Y el contenedor se publica.** Puedes comprobar que su SHA-256 es el que la ficha dice, y
comprobar tú mismo que sin la contraseña no se abre. **No hay ningún dato de nadie dentro:** es
un documento fabricado para el ejemplo.

**Ninguna de las cuatro fichas describe a una persona.** Dos son lecturas reales de la cadena
sobre direcciones vacías generadas al azar; una describe el documento sintético de arriba; y la
cuarta lleva las cifras, la fecha y los activos sustituidos. La declaración de anonimización de
cada una está en el **anexo final de `entregables/SPEC.md`**, no en un campo de la ficha.

> **CORRECCIÓN 2026-09-25:** aquí decía «Cada una lo declara en su propio campo
> `anonymization`». **Era falso**, por lo mismo que arriba: los cuatro ejemplos no tienen ese
> campo (el esquema no lo admite). La nota vive en el anexo del `SPEC.md`.

---

## Las cuatro confusiones que este contrato impide

**1. Que lo que no se sabe se convierta en cero.**
Un hueco declarado se puede ir a tapar. Un cero falso, no.

**2. Que se confunda el dónde con el qué.**
El banco no es el peso. La wallet no es el ether. Son dos casillas distintas y las dos son
obligatorias. Parece una tontería hasta que alguien suma «lo que tengo en el banco» con
«lo que tengo en la moneda» y cuenta el dinero dos veces.

**3. Que se confunda cuándo lo vimos con cuándo rige.**
Un extracto que miro hoy puede hablar del mes pasado. Un contrato firmado hoy puede regir
desde enero. Copiar la primera fecha en la segunda es inventar.

**4. Que un dato vencido siga decidiendo.**
Una medición de junio no describe septiembre. El número no se borra —es historia— pero se le
quita la fuerza: **un dato vencido no puede sostener una conclusión.**

Y una quinta, que es una regla de una sola línea y evita un problema enorme:

> **Nunca se escribe «esto no existe».** El contrato no tiene forma de decirlo. Como mucho
> admite «no lo hemos establecido». No encontrar una cosa **no es prueba** de que no exista, y
> confundir las dos ha costado muy caro en medicina y en dinero.

---

## Por qué esto importa ahora

Al preparar esta publicación se fueron a verificar, **una por una**, las cifras que todo el
mundo repite sobre hackeos y seguros en DeFi. **Nueve. Casi ninguna aguantó.**

No porque alguien mienta, sino porque **casi nadie declara con qué filtro contó**:

- **Dos firmas serias** midieron el mismo semestre de 2026 y publicaron resultados distintos:
  **972 M** frente a **más de 1.000 M**.
- **La misma fuente pública** —DeFiLlama, la que todos citan— produce **cuatro totales
  distintos** del mismo conjunto de datos, según qué se incluya. Todos defendibles. El filtro,
  casi nunca declarado.
- **El mismo hackeo** se reporta con **tres importes diferentes**, aunque hay comunicado
  oficial de quien lo sufrió.
- **La estadística más repetida del sector** —«menos del 2% está asegurado»— **no tiene
  metodología publicada**, y quien la dice es el fundador del mayor asegurador: es su
  estimación sobre el tamaño de su propio mercado. Lo cual no la invalida, pero el lector
  necesita saberlo para pesarla.

**Ninguna de esas cuatro cosas es un problema de datos. Las cuatro son un problema de
declaración.** Que es exactamente el problema que este contrato resuelve.

> **Una aseguradora no puede tarifar un riesgo que no puede medir.** Nexus Mutual, el mayor
> asegurador del sector, ha pagado algo más de **18,5 M** en reclamaciones acumuladas frente a
> más de **7.000 M** en cobertura suscrita. La brecha no es falta de capital: es falta de
> estándar.

Está todo en **`PORQUE.md`** — cifra por cifra, con su fuente, su filtro **y lo que no se pudo
establecer**. Ese documento se somete a las reglas del contrato que publica.

---

## El programa y lo que falta

**LAMC** nació de un problema concreto: una persona con patrimonio repartido entre bancos,
cadenas públicas y documentos, que necesitaba saber **qué sabía de verdad y qué estaba
suponiendo**. El método salió de ahí. Se publica porque el problema no es de una persona.

> **El activo no es el portafolio. Es el método.**

### Publicado hoy

**El contrato 0.2.0** — este repositorio. El formato.

Es el peldaño que hace posibles los demás: **sin una ficha común no hay nada que agregar, ni
que comparar, ni que auditar.** Por eso va primero, aunque no sea lo más vistoso.

### Lo que viene después, y en qué orden

Se construye **de lo simple a lo complejo**. Cada peldaño tiene **una prueba que un tercero
puede fallar**, y no se sube al siguiente sin pasarla.

| # | Peldaño | Prueba para subir |
|---|---|---|
| **1** | **El contrato** ✅ — este repositorio | ¿Un tercero sin contexto rellena una ficha válida? **Probado cinco veces** |
| **2** | **Reconstruir** — leer datos reales y emitir fichas de un portafolio entero | ¿Reproduce un total conocido **sin inventar ningún valor**? |
| **3** | **Controles operativos** — el estándar de lo que pasa **fuera de la cadena**, que es donde están los golpes | ¿Un tercero puede comprobar el estado de un control **sin preguntarle al autor**? |
| **4** | **Los datos de control** — qué control tiene cada protocolo, y cuál no | ¿Se pueden comparar dos instituciones entre sí? |

**La razón del orden.** Hoy no hay nada que agregar porque **no existe el formato de lo que se
quiere agregar**. Construir el motor antes que la unidad de medida es exactamente cómo se
acaba con dos sistemas que no se pueden comparar — que es el problema que cuenta `PORQUE.md`.

### Lo que NO se va a construir

- Un panel de inversión, señales, o recomendaciones de compra
- Custodia de claves, ni firma de transacciones
- Puntuaciones de riesgo **antes** de que exista el dato que las sostenga
- Nada que aconseje: **el sistema declara. No recomienda.**

---

*Apache-2.0. Úsalo, cópialo, modifícalo, véndelo. Si lo mejoras, cuenta cómo.*
