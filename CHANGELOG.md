# Historial de cambios

---

## Cómo leer este documento

Aquí hay **dos numeraciones distintas**, y conviene no confundirlas:

| Número | Qué numera | Dónde vive |
|---|---|---|
| **`0.2.0`** | **El contrato.** Es la versión del esquema y del formato de la ficha | `VERSION`, y el campo `schema_version` de cada ficha |
| **`r1` … `r7`** | **Las revisiones del documento.** Cada una corrigió defectos que encontró un lector nuevo | En las referencias `(v0.x.0/…)` que `SPEC.md` cita junto a cada regla |

**Por qué existen las dos.** El contrato `0.2.0` no salió de un tirón: se escribió, se probó
con lectores sin contexto, y cada prueba encontró defectos reales. **Siete revisiones antes de
la primera publicación.** Algunas tocaron el esquema y otras solo el manual.

Las referencias del tipo `(r4/C1)` que aparecen dentro de `SPEC.md` apuntan a esa historia.
**Están ahí a propósito:** cada regla del manual puede rastrearse hasta el defecto concreto
que la hizo necesaria. Un contrato sin esa trazabilidad es un contrato en el que hay que
creer; con ella, se puede auditar.

**Ninguna revisión cambió el número `0.2.0`**, porque ninguna se publicó. `0.2.0` es, por
tanto, la primera versión pública.

---

## 0.2.0 — primera publicación · 2026-09-23

El contrato, endurecido a lo largo de siete revisiones, se publica por primera vez.

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

### Las siete revisiones

| Rev. | Qué la motivó | Qué encontró | Qué cambió |
|---|---|---|---|
| **r1** | Primera prueba con un lector sin contexto | **Un defecto fatal:** la ficha **no tenía casilla para la cifra**. El importe solo podía ir dentro de una frase, donde ningún ordenador lo encuentra | Se añadió `quantity`, como campo propio y plano. **El número dejó de estar escondido en la prosa** |
| **r2** | Segunda prueba ciega | **Cinco contradicciones internas** —el documento decía una cosa en un sitio y la contraria en otro—, nueve ambigüedades y un hueco de diseño | Se corrigieron los cinco. Se fijó la regla **L-10: toda corrección se cita con su línea exacta, no se afirma** |
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

Cinco, declaradas en `SPEC.md` y resumidas en el `README`. **Se publican abiertas a
propósito.** La principal: no hay análisis de si 22 casillas son las correctas, y la historia
no tranquiliza — el número ya cambió tres veces, y la última fue porque **faltaba una casilla
de verdad**.

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

## Numeración futura

`0.x` mientras no haya **implementaciones independientes** del contrato. La señal para pasar a
`1.0` no es que el documento esté terminado —lo está— sino que **alguien que no sea el autor
lo haya implementado y haya dicho qué le faltó.**

Un estándar sin implementaciones independientes no es un estándar. Es una propuesta.
