# CHARTER — N8 `ORS`

**Estado:** ✅ **COMPLETADO** · **Nivel:** **N8** · **Ola:** 3
**Autoría:** quien construye el entregable · **Verificación:** independiente (ajena a la autoría) · **Creado:** 2026-09-25
**Coste estimado:** 3–4 semanas

---

## 1. OBJETIVO

**Diseñar un modelo de puntuación de riesgo operacional (ORS) basado en el benchmark de P4, que permita comparar protocolos por su exposición operacional sin afirmar que ninguno es «seguro».**

El benchmark de P4 dice **qué controles tiene cada protocolo**. El ORS dice **cómo se traduce eso en una puntuación comparable**.

---

## 2. LA PRUEBA

> ## Un tercero aplica el mismo modelo ORS a dos protocolos distintos y obtiene dos puntuaciones que reflejan diferencias reales en controles, no ruido del modelo.

---

## 3. REGLAS BLOQUEANTES

> ⛔ El ORS **no es una nota de seguridad**. No dice si un protocolo es "seguro". Solo dice qué parte de los controles observables están presentes.

> ⛔ Las puntuaciones se basan **exclusivamente** en los datos de P4. No se añaden criterios nuevos.

> ⛔ Sin datos personales.

---

## 4. ENTREGABLES

| # | Artefacto | Descripción |
|---|---|---|
| E-N8-01 | `MODELO.md` | Definición del modelo ORS y su fórmula |
| E-N8-02 | `bundle/puntuaciones.json` | Puntuaciones de los 3 protocolos de P4 |
| E-N8-03 | `bundle/evidence.md` | Fuentes de cada puntuación |
| E-N8-04 | `INFORME.md` | Resultados y limitaciones |

---

## 5. VALIDACIÓN

```bash
python3 herramientas/validar_evidencia.py proyectos/N8_ORS
```

---

## 6. MISIONES

| ID | Misión | Salida |
|---|---|---|
| M-N8-01 | Diseñar el modelo ORS | `MODELO.md` → filtro de la verificación independiente |
| M-N8-02 | Aplicar el modelo a los 3 protocolos | `puntuaciones.json` |
| M-N8-03 | Documentar y validar | `INFORME.md` |

Todo en `proyectos/N8_ORS/entregables/`.

---

## 7. CRITERIO DE TERMINADO

`PASS` cuando:
1. El modelo está documentado y es reproducible
2. Las puntuaciones se basan en datos de P4
3. El informe declara explícitamente lo que el ORS **no** mide