# CHARTER — P4 `CAPA_CONTROLES`

**Estado:** ✅ **COMPLETADO** · **Nivel:** **N7** · **Ola:** 3
**Autoría:** quien construye el entregable · **Verificación:** independiente (ajena a la autoría) · **Creado:** 2026-09-25
**Coste estimado:** 2–3 meses

> **CORRECCIÓN 2026-09-25 (auditoría independiente, hallazgo 5).** Esta línea decía
> «A CREAR · **N7–N8**». Ya no era cierto por dos motivos: el proyecto está terminado, y
> **N8 no es de este proyecto**. El nivel se repartió en dos trabajos distintos y un
> nivel no puede estar en dos sitios: **P4 = N7** (benchmark de 52 controles) y
> **`N8_ORS` = N8** (modelo de puntuación). Ver el plan del programa, §3, y
> `registro/PROYECTOS.md`.

---

## 1. OBJETIVO

**Producir un benchmark de seguridad operacional basado en el estándar de P3, aplicado a una muestra real de protocolos, y sentar las bases para una puntuación de riesgo ORS.**

El estándar de P3 define **qué controles debe tener una operación DeFi**. El benchmark de P4 **mide si los tienen**.

---

## 2. LA PRUEBA

> ## Un tercero puede ejecutar el benchmark contra un protocolo y obtener una medición comparable con la de otro protocolo.

**Frase falsifiable:**
> *Dos personas distintas aplican el benchmark al mismo protocolo y obtienen el mismo resultado, ítem por ítem.*

---

## 3. ALCANCE

- ✅ Aplicar el estándar de P3 (52 ítems) a **al menos 3 protocolos**
- ✅ Medir qué controles tienen y cuáles no
- ✅ Expresar el resultado como benchmark comparable
- ✅ Declarar qué no se pudo medir

**Fuera de alcance:**
- ❌ El ORS no se construye aquí (es N8)
- ❌ No se auditan protocolos
- ❌ No se publican resultados sin HG-001

---

## 4. REGLAS BLOQUEANTES

> ⛔ **El benchmark no afirma «más seguro».** Solo dice qué controles están presentes y cuáles no. La interpretación es del lector.

> ⛔ **Solo datos observables.** Si un control no se puede comprobar desde fuentes públicas, es `UNKNOWN` con motivo.

> ⛔ **Sin datos personales.** Lo mismo que en todos los proyectos anteriores: nadie identificable.

---

## 5. ENTREGABLES

Todos en `proyectos/P4_CAPA_CONTROLES/entregables/`.

| # | Artefacto | Descripción |
|---|---|---|
| E-P4-01 | `BENCHMARK.md` | Resultados del benchmark sobre los protocolos seleccionados |
| E-P4-02 | `bundle/mediciones.json` | Mediciones conformes al esquema de P1, por protocolo |
| E-P4-03 | `bundle/evidence.md` | Cada medición con su fuente |
| E-P4-04 | `bundle/unknowns.md` | Huecos declarados |
| E-P4-05 | `bundle/reasoning.md` | Razonamiento |
| E-P4-06 | `INFORME.md` | Resultados y limitaciones |
| E-P4-07 | `PROTOCOLOS.md` | **La selección de los 3 protocolos** y el acceso público disponible para medir cada control (artefacto de **M-P4-01**) |

> **AÑADIDO 2026-09-25 (auditoría independiente, hallazgo 8).** `PROTOCOLOS.md` existía,
> estaba declarado en `ESTADO.md` y en `registro/entregables.json`, y **no figuraba en
> esta tabla**: la lista decía 6 entregables y había 7. No es un alcance nuevo —
> el artefacto es la salida de **M-P4-01**, que ya estaba en la lista de misiones (§6)—,
> es la lista la que estaba incompleta. Se añade aquí para que las dos fuentes digan lo
> mismo. Si algún día apareciera un artefacto que **no** corresponda a una misión de §6,
> eso sí sería crecimiento de alcance y exigiría **HG-004**.

---

## 6. VALIDACIÓN

```bash
python3 herramientas/validar_evidencia.py proyectos/P4_CAPA_CONTROLES
```

Debe terminar en **RESULTADO: APROBADO**.

---

## 7. MISIONES

| ID | Misión | Salida |
|---|---|---|
| M-P4-01 | Seleccionar 3 protocolos y documentar el acceso | Tabla → filtro de la verificación independiente |
| M-P4-02 | Aplicar el estándar y medir | `mediciones.json` + `BENCHMARK.md` |
| M-P4-03 | Declarar huecos | `unknowns.md` |
| M-P4-04 | Documentar y validar | `reasoning.md` + `INFORME.md` |

---

## 8. CRITERIO DE TERMINADO

`PASS` cuando:

1. El validador dice `APROBADO`
2. El benchmark cubre al menos 3 protocolos
3. Cada medición tiene fuente verificable
4. Un tercero puede repetir la medición

---

## 9. HUMAN GATES

- **HG-001** — publicación externa
- **HG-009** — aprobación de los 3 protocolos (verificación independiente)