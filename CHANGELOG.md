# Historial de cambios

---

## Cómo leer este documento

Aquí hay **dos numeraciones distintas**, y conviene no confundirlas:

| Número | Qué numera | Dónde vive |
|---|---|---|
| **`0.2.0`** | **El contrato.** Es la versión del esquema y del formato de la ficha | `VERSION`, y el campo `schema_version` de cada ficha |
| **`v0.3.0` … `v0.7.0`** | **Las rondas de corrección del documento: cinco**, y así las cuenta `SPEC.md` §9 | En las referencias `(v0.x.0/…)` que `SPEC.md` cita junto a cada regla |
| **`r1` … `r7`** | **Los hitos del historial: siete** (las cinco pruebas ciegas y las dos limpiezas). Es una cuenta más amplia que la de rondas, no otra cifra de lo mismo | En la tabla de más abajo |

**Por qué existen las dos.** El contrato `0.2.0` no salió de un tirón: se escribió, se probó
con lectores sin contexto, y cada prueba encontró defectos reales. **Cinco rondas de corrección**
(`v0.3.0` a `v0.7.0`) repartidas en **siete hitos** (`r1` a `r7`: las cinco pruebas ciegas y las
dos limpiezas). Algunas tocaron el esquema y otras solo el manual.

> **CORRECCIÓN 2026-09-25.** Aquí decía que eran «**Siete revisiones**» y las llamaba `r1`…`r7`,
> mientras `SPEC.md` §9 dice que **van cinco** rondas. **Describían el mismo historial con dos
> cuentas sin explicarlas.** La cuenta de rondas es la del `SPEC` (cinco, las etiquetadas
> `v0.3.0`–`v0.7.0`); la de `r1`–`r7` son **hitos** —incluye la primera prueba ciega, que produjo
> `v0.2.0`, y una limpieza final—, no siete rondas de corrección.

Las referencias del tipo `(v0.4.0/C1)` que aparecen dentro de `SPEC.md` apuntan a esa historia.
**Están ahí a propósito:** cada regla del manual puede rastrearse hasta el defecto concreto
que la hizo necesaria. Un contrato sin esa trazabilidad es un contrato en el que hay que
creer; con ella, se puede auditar.

> **CORRECCIÓN 2026-09-25.** Aquí decía que las referencias de `SPEC.md` eran del tipo
> `(r4/C1)`. **El `SPEC` no usa esa forma:** usa `(v0.4.0/C1)`, como dice la tabla de arriba.
> `(r4/C1)` era una mezcla de las dos numeraciones; corregido a la forma real.

**Ninguna ronda de corrección cambió el número `0.2.0`**, porque ninguna se publicó. `0.2.0`
es, por tanto, la primera versión pública.

---

## 0.2.0 — primera publicación · 2026-09-23

El contrato, endurecido a lo largo de cinco rondas de corrección, se publica por primera vez.

### Qué es

Una ficha de **22 casillas obligatorias** para afirmar cualquier cosa sobre dinero, con dos
mecanismos centrales:

1. **El centinela `UNKNOWN` («aún no establecido»)** es un valor admitido en **16 de las 22
   casillas** —las de hecho—. **No es cero.** Cero es una medición; `UNKNOWN` es la ausencia
   de medición. Usarlo obliga a escribir el motivo.
2. **La partición.** Cada ficha declara dos listas complementarias: las casillas que quedaron
   **establecidas** y las que quedaron **sin establecer**. Juntas cubren las 22 casillas
   exactamente: sin faltar ninguna, sin repetirse. Un hueco no declarado es imposible de
   escribir sin que el verificador lo detecte.

Las **6 casillas restantes** —las de registro: `claim_id`, `known`, `unknown`, `unknown_reason`,
`producer`, `schema_version`— **nunca** admiten el centinela. Son la identidad y la estructura
de la ficha, no su contenido. Que `known` fuera `UNKNOWN` disolvería la regla que hace
funcionar todo lo demás.

### Los siete hitos (las cinco rondas de corrección)

| Rev. | Qué la motivó | Qué encontró | Qué cambió |
|---|---|---|---|
| **r1** | Primera prueba con un lector sin contexto | **Un defecto fatal:** la ficha **no tenía casilla para la cifra**. El importe solo podía ir dentro de una frase, donde ningún ordenador lo encuentra | Se añadió `quantity`, como campo propio y plano. **El número dejó de estar escondido en la prosa** |
| **r2** | Segunda prueba ciega | **Cinco contradicciones internas** —el documento decía una cosa en un sitio y la contraria en otro—, nueve ambigüedades y un hueco de diseño | Se corrigieron los cinco. Se fijó la regla **toda corrección se cita con su línea exacta, no se afirma** |
| **r3** | Tercera prueba ciega + una decisión del operador | El agente ciego **inventaba valores** para rellenar casillas que no podía conocer. Era el problema más grave de todas las rondas | **El operador dictó la regla que lo resolvió: «No lo sé es válido».** Desapareció la lista de qué casillas admitían el centinela (eran 7 de 22) y **pasó a admitirse en las 22** |
| **r4** | Cuarta prueba ciega | Aplicar el centinela a las casillas de registro **disolvía la regla de bloqueo** —`known: UNKNOWN` hacía que la ficha no pudiera exigir nada—. Y aplicarlo solo al nivel superior dejaba **seis subcampos huérfanos** | **La corrección que definió el contrato actual:** el centinela se admite en las **16 casillas de hecho** y **nunca** en las **6 de registro**. Se añadió `quantity` a la partición |
| **r5** | Quinta prueba ciega | **El agente ciego no inventó nada.** Renunció a inventar en siete sitios distintos | El problema más grave de las cinco rondas quedó cerrado |
| **r6** | Limpieza | Nueve marcas de ambigüedad que quedaban sueltas | Se resolvieron. Se corrigió la máscara de identificadores: se escribe con `X`, no con `*` |
| **r7** | Limpieza final, ya con la publicación decidida | **Dos defectos reales, y esta vez estaban en el ESQUEMA, no en el texto.** (1) La rúbrica de confianza no tenía su cuarta fila. (2) **El esquema no comprobaba la partición** —se podía declarar una casilla en las dos listas, o en ninguna, y el esquema lo aceptaba— | Se añadió a cada casilla una comprobación `oneOf` que **fuerza** la partición. Probado: rechaza una casilla en las dos listas y una casilla en ninguna |

La r7 merece un comentario, porque es la lección más incómoda del proyecto: **hasta la última
revisión, el esquema era más permisivo que el manual.** El manual decía que las dos listas
tenían que cubrir las 22 casillas sin solaparse; el esquema no lo comprobaba. **Un lector que
solo usara el esquema podía producir fichas inválidas que el verificador habría aprobado.**

### Cómo se comprobó

- **Cinco pruebas ciegas** con agentes sin ningún contexto previo. Recibieron únicamente el
  manual y el esquema, y se les pidió rellenar una ficha real. **Su informe de invenciones y
  contradicciones era la prueba.** Las cinco encontraron defectos.
- **Un verificador determinístico** sin dependencias, que mide cada ficha contra el esquema.
- **Un comprobador de coincidencia** entre lo que el manual dice y lo que el esquema obliga.
- **Una verificación independiente** escrita sin usar ninguna herramienta del proyecto.
- **Los archivos publicados están sellados con su hash SHA-256**, en `SELLOS.txt`. Cualquiera
  puede recomputarlos con `sha256sum -c SELLOS.txt` y comprobar que coinciden.

### Limitaciones conocidas

**Dos listas de cinco, y no son la misma.** El `README` declara las cinco que afectan a quien
decide adoptar el contrato; `SPEC.md` declara sus cinco bordes técnicos, numerados **LIM-1 a
LIM-5** —se renombraron desde `C1`–`C5` el 2026-09-25 para no chocar con las reglas `C` de §5—.
**No coinciden en ningún punto.** *(Corrección 2026-09-25: aquí decía «cinco, declaradas en
`SPEC.md` y resumidas en el `README`», lo que daba a entender que eran las mismas.)*
**Se publican abiertas a
propósito.** La principal: no hay análisis de si 22 casillas son las correctas, y la historia
no tranquiliza — el número ya cambió **dos veces** (`14 → 21 → 22`, contado en `SPEC.md` §9), y
la última fue porque **faltaba una casilla de verdad**.
*(Corrección 2026-09-25: aquí decía «tres veces», y el `README` y `CONTRIBUIR.md` lo repetían.
Contados en la fuente son dos cambios, no tres; los tres documentos dicen ya lo mismo.)*

### Lo que NO se hizo

- ❌ Ningún lector de datos, ningún motor de cálculo, ninguna puntuación de riesgo
- ❌ Ninguna integración con institución alguna
- ❌ Ningún cliente, ningún anuncio, ninguna promesa de seguridad
- ⚠️ **SÍ se editaron los archivos verificados antes de publicarlos, y hay que decirlo.**

  Una revisión previa a la publicación —que no existía hasta ese día— encontró que los
  artefactos aprobados llevaban **datos que permitían identificar a personas**. Estaban escritos
  para uso interno y **nadie los había mirado con ojos de «esto lo va a leer el mundo».**
  Enumerar aquí qué clase de datos eran sería volver a exponerlos: **basta con decir que había
  que limpiarlos, y que se limpiaron.**

  Se limpiaron. **Y después se repitieron las tres verificaciones**, porque un artefacto que
  cambia tiene que volver a aprobarse: el validador, el comprobador de coincidencia y la
  verificación independiente pasaron de nuevo; y el validador se atacó con 19 fichas
  malformadas para comprobar que rechaza las inválidas.

  **El paquete público se genera desde los archivos limpios y verificados**, y `SELLOS.txt`
  fija exactamente cuáles son. La lección quedó registrada: **un entregable puede estar
  correcto y no ser publicable.** Son dos preguntas distintas, y hasta ese día solo se había
  medido la primera.

---

## Segunda publicación del mismo contrato — 2026-09-25

**El contrato NO cambió.** La huella del esquema es la misma que en la primera publicación
(`fa709034…`), y `VERSION` sigue siendo `0.2.0`. **Quien haya implementado `0.2.0` no tiene
que tocar nada.** Lo que cambia es lo que rodea al contrato: los ejemplos, la herramienta que
comprueba, y algunas frases que no correspondían a su artefacto.

### Por qué hubo una segunda publicación

Una **auditoría independiente** revisó lo publicado y encontró que **los cuatro ejemplos no
pasaban su propio contrato**. El esquema declara `additionalProperties: false` —no se admiten
casillas que él no defina— y los ejemplos llevaban una casilla `_example` con sus notas
explicativas. Un validador estándar de JSON Schema los habría rechazado.

**Y la herramienta del proyecto no lo detectaba**, porque no comprobaba esa regla: decía
`APROBADO` sobre datos que violaban el contrato. **Y no era la única regla que no comprobaba:**
solo miraba cuatro listas cerradas de primer nivel (`authority`, `verification_status`,
`confidence`, `reconciliation_status`) y no recorría **las listas cerradas anidadas**
(`container.type`, `instrument.kind`, `source_type`, `freshness.status`) **ni los patrones del
esquema**, así que también aprobaba un `claim_id` que no cumplía su forma. Es el defecto clásico
de este programa —una regla escrita en la norma y no comprobada en la práctica— **vivo dentro de
la herramienta que existe para detectarlo.**

### Qué cambió

| | |
|---|---|
| **Los cuatro ejemplos** | Se retiró la casilla `_example`. Sus notas **no se perdieron**: son ahora el anexo *«Los cuatro ejemplos, explicados»* de `SPEC.md`, donde sí se pueden leer |
| **El verificador** | Ahora **comprueba `additionalProperties`** (rechaza una casilla de más, en la raíz o dentro de `subject`, `container`, `instrument` o `freshness`), **recorre todas las listas cerradas del esquema en cualquier nivel**, **aplica los patrones** (`claim_id`, `schema_version`) y **rechaza el centinela en los seis campos del registro** |
| **El mínimo de fichas y autoridades** | Se **declara por proyecto** citando la línea del charter que lo exige, en vez de estar fijado a mano con una regla atribuida a un charter que no la contenía. Un mínimo que nadie declara se informa como **«no exigido»** — nunca se aprueba en silencio |
| **Una ficha de P2** | `LAMC-P2-2026-0007` llevaba una casilla `instrument.label` que el contrato no admite (`instrument` es `{kind, symbol?, contract_address?, token_id?}`). Se retiró; su significado está en `bundle/evidence.md` |
| **Los valores de instrumento de P2** | Varias fichas de ese ejemplo usaban `instrument.kind` con valores (`TOKEN`, `OTHER`) que **el contrato no admite** —contado en `proyectos/P2_DEMO_RECONSTRUCCION/entregables/bundle/positions.json` el 2026-09-25: **5 de las 7 fichas**—. Se corrigieron al vocabulario del esquema. **El verificador los aprobaba** porque no miraba las listas cerradas anidadas |
| **El `README`** | Describe lo que la herramienta comprueba **de verdad**, incluida la comprobación de casillas de más y el alcance real del centinela |
| **La nota interna de P2** | `LEEME.md` no es un entregable y **ya no viaja en el paquete** |

### Cómo se comprobó esta vez

- **Una auditoría independiente** sobre lo publicado: **21 hallazgos**, 7 de gravedad alta,
  **ninguno bloqueante** — sin datos personales ni credenciales, ni en los archivos ni en el
  historial de git.
- **Una segunda auditoría**, esta sobre las correcciones: **8 hallazgos**, 2 de gravedad alta,
  ninguno bloqueante. **Los dos graves los había causado la propia corrección** — texto que
  seguía describiendo un campo ya retirado, y una promesa del `README` que la herramienta
  corregida ya no cumplía. Corregidos.
- **Una prueba de ataque contra el verificador**, de **19 casos**: una ficha correcta —que
  tiene que **pasar**— y dieciocho rotas, una por cada fallo conocido. **Sin el caso correcto la
  prueba no valdría nada:** un verificador que rechaza todo también acertaría las dieciocho.
  *(Nació con once casos y creció con cada defecto que se fue encontrando: 14, luego 16, hoy 19.
  Cada caso nuevo es un fallo que ya no puede volver sin que se note.)*
- **La huella del esquema, recalculada** al abrir y al cerrar: idéntica.

### Y una consecuencia que conviene decir

**Publicar no es gratis.** Que este repositorio tenga ahora dos publicaciones de la misma
versión significa que **el mismo `0.2.0` tiene dos juegos de bytes distintos**: los ejemplos
cambiaron. **Si descargaste el paquete antes del 2026-09-25, tus ejemplos no eran conformes.**
Los sellos de `SELLOS.txt` son la referencia: si un archivo no cuadra con su sello, es de la
tanda anterior.

---

## Tercera publicación — 2026-09-26

**El contrato NO cambió.** La huella del esquema sigue siendo `fa709034…` y `VERSION` sigue siendo
`0.2.0`. **Quien haya implementado `0.2.0` no tiene que tocar nada.** Lo que cambia es que
**este repositorio publica dos trabajos más** que hasta hoy estaban terminados y sin publicar:
el contrato aplicado **fuera de las criptomonedas** y la **conciliación** de dos mundos.

### Qué se añade

| Proyecto | Qué es |
|---|---|
| **`P7_SEGUNDO_DOMINIO`** | **La prueba de que el método no va de criptomonedas.** Seis fichas tomadas de la Cuenta General 2023 del **Ayuntamiento de Barcelona** —un documento público de 169 páginas—, cada una con la página y la línea de donde sale su cifra. **El contrato sirvió sin cambiarle una letra** |
| **`P8_RECONCILIACION`** | Un solo registro con **trece fichas**: las siete de la cartera ajena (P2) y las seis del ayuntamiento (P7), copiadas tal cual. **No están fusionadas**: son sujetos distintos, con monedas distintas y ninguna cifra comparable. El documento **dice qué no se pudo unir y por qué** |

**Por qué esto importa más que las cifras.** Un contrato que solo funciona con criptomonedas es un
formato para criptomonedas. Uno que sostiene la contabilidad de un ayuntamiento **sin cambiar una
coma** es un formato para evidencia financiera. Esa era la pregunta abierta desde la primera
publicación, y la respuesta está en `P7_SEGUNDO_DOMINIO/entregables/VEREDICTO.md`.

**En `P7` el lector puede ir más lejos que en ningún otro sitio de este paquete:** descargar el
documento oficial del ayuntamiento, buscar la página y la línea que la ficha cita, y **encontrar
la misma cifra**. El documento original **no viaja aquí** —pesa 26 MB y las fuentes se citan, no se
copian—: viaja el enlace oficial, que es lo que hace la comprobación posible.

### Un defecto que esta publicación destapó — y que se corrigió

La puerta de salida marca como sospechoso todo número con forma de teléfono. Al meter `P7` marcó
**`3332351497.29`**, que no es un teléfono: son **los ingresos totales del ayuntamiento**, con sus
decimales. Y a la vez **se le escapaban** los teléfonos escritos como se escriben de verdad —con el
prefijo del país y espacios entre bloques de dígitos—, porque el patrón solo los entendía escritos
de un tirón.

**El control tenía los dos defectos a la vez: inventaba uno que no existía y no veía los que sí.**
Corregido: entiende los números agrupados, no dispara con los decimales ni con los dígitos dentro
de un hash, y **no ha perdido nada de lo que cazaba** (comprobado metiendo un teléfono real en un
paquete de prueba y viendo que la puerta lo detecta).

### La comprobación, esta vez

- **La puerta de salida**, ejecutada antes de publicar: fidelidad byte a byte, sellos, cero
  credenciales, cero datos personales, cero rutas de la máquina, y el historial de git revisado.
  **Cuatro rutas absolutas y tres falsos positivos aparecieron en el camino y se corrigieron
  antes de salir**: nada de eso viaja.
- **La prueba de ataque contra el verificador**: los **57 casos** (uno correcto, 56 rotos), todos
  comportándose como deben.
- **La huella del esquema, recalculada**: idéntica.
- **Los patrones de la puerta tienen prueba propia**, y ahora vive en un archivo en vez de en un
  comentario: `publicacion/prueba_patrones_puerta.py`. Antes decía «verificado con 17 casos» y
  **esos casos no existían en ningún sitio**. Una prueba hecha una vez a mano no es una prueba.

### Y una cifra que ya no se escribe aquí

**El número de archivos publicados no se copia en este documento.** La fuente es `SELLOS.txt`, y se
comprueba con `sha256sum -c SELLOS.txt`. Una cifra en dos archivos acaba discrepando; una sola
fuente, no.

---

## Numeración futura

`0.x` mientras no haya **implementaciones independientes** del contrato. La señal para pasar a
`1.0` no es que el documento esté terminado —lo está— sino que **alguien que no sea el autor
lo haya implementado y haya dicho qué le faltó.**

Un estándar sin implementaciones independientes no es un estándar. Es una propuesta.
