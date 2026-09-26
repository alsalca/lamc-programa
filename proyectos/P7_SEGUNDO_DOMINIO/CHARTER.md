# CHARTER — P7 `SEGUNDO_DOMINIO`

**Estado:** ✅ **COMPLETADO** · **Nivel:** **N4** · **Ola:** 2
**Autoría:** quien construye el entregable · **Verificación:** independiente (ajena a la autoría) · **Creado:** 2026-09-25
**Coste estimado:** 1–2 semanas

---

## 1. OBJETIVO

**Aplicar el contrato de P1, SIN MODIFICARLO, a un dominio financiero que no sea blockchain.**

Empezó en cadenas públicas. La tesis del programa es que **LAMC no es un sistema de crypto: es
una capacidad** — reconstruir, normalizar y gobernar evidencia financiera de fuentes
heterogéneas. **Crypto fue el primer dominio. No es la definición.**

**P7 es donde eso se demuestra o se derrumba.**

---

## 2. LA PRUEBA — Y ES DURA

> ## El mismo contrato, con las mismas 22 casillas, sin añadir ni cambiar ninguna, tiene que
> ## servir para un dominio financiero completamente distinto.

**No vale decir «se puede adaptar».** Adaptar es fallar. El contrato **ya está publicado**: si
hay que tocarlo, **N4 no se supera y la tesis general no se sostiene.**

**Frase falsifiable:**
> *Un tercero lee las fichas del segundo dominio y reconstruye la situación sin preguntar nada
> al autor — usando el manual de P1 **tal como está publicado**.*

---

## 3. POR QUÉ ESTE PROYECTO ES EL MÁS IMPORTANTE DEL PROGRAMA

Los niveles N0 a N3 están hechos: el formato, la demostración y el estándar de control.
**Los tres, en un solo dominio: cadenas públicas.**

**Y hay una objeción que mata al producto si no se responde:**

> *«Bonito. Pero solo funciona con criptomonedas.»*

**P7 no la responde con un argumento. La responde con un entregable.**

Y hay un segundo motivo, menos evidente y más importante: **hasta ahora todo lo que hemos
publicado usa datos que ya venían en formato de máquina.** Las cadenas son un caso fácil — el
dato está limpio, estructurado y es verificable por cualquiera.

**El segundo dominio tiene que ser difícil de verdad:** documentos, PDFs, informes. **Donde el
dato existe pero no está listo para usarse.** Ahí es donde el contrato demuestra si sirve.

---

## 4. ELECCIÓN DEL DOMINIO — REGLAS BLOQUEANTES

> ## ⛔ REGLA BLOQUEANTE — SIN DATOS PERSONALES
>
> **El dominio tiene que ser una ENTIDAD, no una persona.** Una empresa pública, un
> ayuntamiento, una fundación, una cooperativa, un organismo público — **alguien que publique
> sus cuentas y cuyo titular no sea un particular.**
>
> **Si el dominio elegido arrastra datos de personas, se rechaza.** Sin excepciones.
>
> **Dirección del operador, textual:** *«Debe mantener el anonimato al máximo. Debe quedar claro.»*
>
> **La lección costó cara publicando P1 y P2:** el historial de git viaja, los documentos
> citan rutas, y un dato que parece inofensivo identifica. **Aquí se elige desde el principio
> un dominio donde ese problema no exista.**

### Y además, criterios técnicos

- ✅ **Fuente real y pública** — documentos que cualquiera pueda descargar y comprobar
- ✅ **Con cifras de verdad** — importes, fechas, obligaciones
- ✅ **Documentos, no API** — es el caso difícil, y es el que interesa
- ✅ **Al menos una obligación o compromiso**, no solo activos (si no, es un caso plano)
- ✅ **Que NO sea blockchain** — si no, no demuestra nada nuevo

**Prohibido:** personas físicas, empresas privadas sin cuentas publicadas, datos con PII,
y cualquier fuente que no se pueda citar con enlace.

---

## 5. EL CONTRATO — SE USA, NO SE TOCA

```
proyectos/P1_ESQUEMA_EVIDENCIA/entregables/
    evidence-envelope.schema.json   ← la definición normativa (22 casillas)
    SPEC.md                         ← el manual
    examples/                       ← cuatro fichas de ejemplo

Publicado en: https://github.com/alsalca/lamc-programa
```

**Si el manual y el esquema difieren, manda el esquema.**
**Y si algo no encaja: NO se cambia el contrato.** Se declara como hueco con su motivo, o se
reporta como hallazgo. **Un campo nuevo aquí significa que N4 ha fallado** — y eso hay que
decirlo, no taparlo.

---

## 6. ENTREGABLES

Todos en `proyectos/P7_SEGUNDO_DOMINIO/entregables/`.

| # | Artefacto | Descripción |
|---|---|---|
| E-P7-01 | `DOMINIO.md` | El dominio elegido, por qué, y la prueba de que no tiene PII |
| E-P7-02 | `bundle/fichas.json` | Las fichas del segundo dominio, conformes al contrato de P1 |
| E-P7-03 | `bundle/evidence.md` | Cada cifra con su fuente citable |
| E-P7-04 | `bundle/unknowns.md` | **Los huecos declarados** |
| E-P7-05 | `bundle/reasoning.md` | El razonamiento, paso a paso y reconstruible |
| E-P7-06 | `INFORME.md` | Qué encajó, **qué no encajó, y qué se tuvo que forzar** |
| E-P7-07 | `VEREDICTO.md` | **¿El contrato sirvió sin modificarse? Sí o no, con la prueba** |

> **`VEREDICTO.md` es el entregable más importante.** Y **puede decir que NO.** Un `NO` con
> pruebas vale infinitamente más que un `SÍ` forzado: significaría que hemos encontrado el
> límite de la capacidad **antes** de venderla como general.

---

## 7. VALIDACIÓN DETERMINÍSTICA

```bash
python3 herramientas/validar_evidencia.py \
    proyectos/P7_SEGUNDO_DOMINIO
```

**Encuentra solo el esquema de P1.** Comprueba las 22 casillas, los valores permitidos, la
partición `known`/`unknown` sin solapes ni huecos, y que ningún `unknown` vaya sin motivo.

**Debe terminar en `RESULTADO: APROBADO`.**

**Y comprobación añadida, que es el corazón de N4:**

```bash
# El contrato NO se ha tocado: su hash es el mismo que el publicado.
sha256sum proyectos/P1_ESQUEMA_EVIDENCIA/entregables/evidence-envelope.schema.json
```

---

## 8. FUERA DE ALCANCE

- ❌ Tocar o modificar el contrato de P1
- ❌ Datos de personas físicas
- ❌ Publicar (requiere HG-001)
- ❌ Construir lector de PDFs, OCR o software de producción: el entregable es **un informe**
- ❌ Buscar un dominio que «encaje fácil»: eso vacía la prueba de sentido

---

## 9. RIESGOS

| ID | Riesgo | Mitigación |
|---|---|---|
| R-016 | **Elegir un dominio fácil que no pruebe nada** | El dominio debe tener documentos, no API |
| R-017 | **Forzar el contrato para que encaje** | §5: no se toca. Y `VEREDICTO.md` declara los forzamientos |
| R-018 | **Que el dominio arrastre PII** | Regla bloqueante de §4 |
| R-019 | **Deriva hacia construir software** | §8: el entregable es un informe |
| R-020 | **Que el `VEREDICTO` diga SÍ por complacencia** | Lo firma la verificación independiente, no quien construye |

---

## 10. MISIONES

| ID | Misión | Salida |
|---|---|---|
| **M-P7-01** | Proponer 3 dominios candidatos, comprobados | Tabla → **filtro de la verificación independiente** |
| **M-P7-02** | Emitir las fichas del dominio aprobado, contra el contrato **sin tocar** | `fichas.json` + `evidence.md` |
| **M-P7-03** | Declarar los huecos y **lo que no encajó** | `unknowns.md` |
| **M-P7-04** | Documentar el razonamiento, validar y emitir veredicto | `reasoning.md` + `VEREDICTO.md` |

**M-P7-01 requiere aprobación antes de seguir.**

---

## 11. CRITERIO DE TERMINADO

`PASS` cuando:

1. El validador dice `APROBADO` sobre las fichas del segundo dominio
2. **El hash del esquema es el mismo que el publicado** — no se ha tocado
3. Existe al menos un hueco declarado
4. `VEREDICTO.md` dice **claramente** si el contrato sirvió sin modificarse, **con la prueba**
5. Un tercero sigue `reasoning.md` y llega a lo mismo

**Si el veredicto es NO, el `PASS` también se emite** — porque un `NO` documentado es un
resultado, no un fracaso. **Lo que no se admite es un `SÍ` sin prueba.**

---

## 12. HUMAN GATES

- **HG-001** — publicación externa
- **HG-009** — aprobación del dominio elegido (filtro técnico de la verificación independiente)
