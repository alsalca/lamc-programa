# Cómo contribuir

---

## Antes de nada: la prueba que vale

Este proyecto no acepta cambios «porque estaría bien». Acepta cambios que **resuelven un
defecto observado**.

La prueba es siempre la misma, y es la que se usó cinco veces durante su construcción:

> **Toma el manual y el esquema. No leas nada más. Intenta rellenar una ficha real de un caso
> tuyo. Anota dónde tuviste que adivinar, y dónde el documento se contradijo.**

**Ese informe es la contribución más valiosa que existe aquí.** Vale más que un parche.
Un lector nuevo ve lo que el autor ya no puede ver — eso no es un decir, es literalmente lo
que pasó las cinco veces.

---

## Qué se acepta

| Sí | No |
|---|---|
| Un caso real que el contrato no puede expresar | Una casilla nueva «por si acaso» |
| Una contradicción entre el manual y el esquema | Una preferencia de estilo |
| Una ambigüedad que te obligó a elegir | Una función nueva sin caso que la pida |
| Una regla que un ordenador puede comprobar y hoy no comprueba | Una regla que hay que interpretar |
| Traducciones | Cambios que rompan fichas existentes sin decirlo |

---

## Las tres reglas duras del proyecto

**1. El manual y el esquema son DOS SITIOS de las mismas reglas, y tienen que decir lo mismo.**

Si una regla mecánica cambia, **se actualizan los dos en el mismo acto**. No hay excepción.
*Este es el defecto que más veces ha aparecido:* el esquema comprobando menos que el manual.
En la última revisión se encontró que el esquema **no comprobaba la partición** de las dos
listas —el manual sí lo exigía— y eso permitía producir fichas inválidas que el verificador
aprobaba. **Un contrato que promete más de lo que comprueba está roto.**

**2. Nada se añade sin un caso real que lo pida.**

`quantity` se añadió porque una ficha no podía expresar una cifra. No porque fuera elegante.
**Una casilla de más es deuda para siempre.** El número ya creció tres veces; cada vez costó.

**3. Toda afirmación se cita.**

Si dices «arreglado», cita **la línea exacta** donde quedó arreglado. Sin la línea no cuenta
como arreglado. *Motivo:* en una de las rondas, un informe dio por resueltos ocho hallazgos y
**uno no lo estaba**. Si el verificador se hubiera fiado del informe, el defecto habría pasado
a la versión publicada.

---

## Cómo comprobar que no rompiste nada

El verificador no tiene dependencias. Se necesita Python 3 y nada más.

```bash
python3 herramientas/validar_evidencia.py .
```

Debe terminar en **`RESULTADO: APROBADO`**. Si tocaste el esquema o el manual, comprueba
además que los dos sigan de acuerdo:

```bash
python3 herramientas/comprobar_coincidencia.py
```

Debe decir **`SIN INDICIOS DE DESACUERDO`**.

> Es una **heurística**: da indicios, no verdades. Si dice que hay desacuerdo, míralo. Si dice
> que no, **no es una garantía** — sigue siendo un programa comparando texto.

---

## Cómo enviar un cambio

1. **Abre un informe** describiendo el caso real que falla. Si puedes, incluye la ficha que
   intentaste escribir y el punto exacto donde no supiste qué poner.
2. **Si traes un parche:** una cosa por cambio. Que el verificador pase. Que el manual y el
   esquema digan lo mismo. Y **di qué fichas existentes dejan de ser válidas**, si alguna.
3. **El autor no firma su propio trabajo.** Un cambio que rompe compatibilidad necesita que
   alguien más lo haya mirado.

---

## Dos cosas que probablemente te encuentres

**Vas a querer añadir un campo para la moneda, o para la fecha.** Ya están, pero no donde
parece: la moneda es la del instrumento, y la fecha es la de vigencia de la ficha. **No se
duplican.** Tener el mismo dato en dos sitios es cómo dos sistemas empiezan a discrepar.

**Vas a querer poner un cero donde no sabes el valor.** **No se puede.** Es el punto entero
del contrato. Si no lo sabes, `UNKNOWN` con su motivo — y el hueco queda perseguible en vez de
enterrado bajo un cero que parece un dato.

---

## Traducciones

Bienvenidas. El **español es la versión autoritativa**: si una traducción y el original
discrepan, manda el original. Al traducir, **traduce también los nombres de los campos y los
valores cerrados** — no los dejes a medias, porque entonces la ficha no valida.

---

*Apache-2.0. Puedes usar esto comercialmente sin pedir permiso y sin decir de dónde viene.
Si lo mejoras, contar cómo ayuda a todos; no contarlo no rompe ninguna regla.*
