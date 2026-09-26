# CHARTER — P8 `RECONCILIACION`

**Estado:** ✅ **COMPLETADO** · **Nivel:** **N5–N6** · **Ola:** 2
**Autoría:** quien construye el entregable · **Verificación:** independiente (ajena a la autoría) · **Creado:** 2026-09-25
**Coste estimado:** 3–4 semanas

---

## 1. OBJETIVO

**Reconciliar dos dominios financieros distintos —blockchain y contabilidad pública— en un
mismo ledger, sin colapsar la cuenta ni inventar ningún dato.**

N0 a N4 demostraron que el contrato de 22 casillas sirve para **un dominio cualquiera**. P8 es
donde se demuestra que sirve para **dos dominios a la vez** — y que se pueden reconciliar sin
fundirlos.

---

## 2. LA PRUEBA

> ## Un tercero toma las fichas de P7 y las de P2/P3, las mete en el mismo ledger, y el
> ## resultado es un balance único que distingue claramente activos de pasivos y procedencias
> ## **sin que ningún dato se haya inventado ni ninguna cuenta se haya colapsado.**

**Frase falsifiable:**
> *Un tercero puede leer el ledger y decir qué parte viene de cada dominio, qué está
> conciliado y qué no, y cuándo caduca cada afirmación.*

---

## 3. QUÉ SE RECONCILIA (y qué no)

| Dominio | Proyecto origen | Qué aporta |
|---|---|---|
| **Blockchain** | P2 (AHAB Safe) + P3 (estándar ops) | Posiciones en Aave, rETH, colateral, deuda, controles |
| **Contabilidad pública** | P7 (Ayuntamiento de Barcelona) | Ingresos, patrimonio, deuda, provisiones, compromisos ambientales |

**No se reconcilia:**
- ❌ El portafolio personal del operador (fuera de alcance)
- ❌ Datos que no tengan procedencia verificable
- ❌ Cifras estimadas o proyectadas (solo datos observados)

---

## 4. REGLAS BLOQUEANTES

> ⛔ **No se inventa ningún dato.** Si un número no se puede leer del mismo documento donde
> se leyó originalmente, se declara `UNKNOWN` con su motivo. Un dato que no está no se
> completa — ni por inferencia, ni por «es obvio», ni por «tiene que sumar».

> ⛔ **Los dominios no se fusionan.** El ledger debe distinguir —en cada línea— de qué
> dominio viene cada afirmación. Si al final no se puede separar lo que es blockchain de lo
> que son cuentas públicas, el proyecto no ha cumplido.

> ⛔ **El contrato no se toca.** 22 casillas, las mismas que en P1. Si algo no encaja, se
> declara como hueco y se reporta como hallazgo de N4+.

> ⛔ **Sin datos personales.** Se aplican las mismas reglas que en P2, P3 y P7: ni una
> persona identificable.

---

## 5. ENTREGABLES

Todos en `proyectos/P8_RECONCILIACION/entregables/`.

| # | Artefacto | Descripción |
|---|---|---|
| E-P8-01 | `DOMINIOS.md` | Los dos dominios que se reconcilian, con su origen y prueba |
| E-P8-02 | `bundle/ledger.json` | **El ledger reconciliado** — una lista de fichas de ambos dominios |
| E-P8-03 | `bundle/reconciliacion.md` | Qué está conciliado, qué no, y por qué |
| E-P8-04 | `bundle/unknowns.md` | **Huecos declarados** — sin colapsar |
| E-P8-05 | `bundle/reasoning.md` | Razonamiento paso a paso |
| E-P8-06 | `INFORME.md` | Qué se pudo reconciliar y qué no, y por qué |

---

## 6. VALIDACIÓN DETERMINÍSTICA

```bash
python3 herramientas/validar_evidencia.py \
    proyectos/P8_RECONCILIACION
```

Debe terminar en **`RESULTADO: APROBADO`**. Encuentra el esquema de P1 solo.

**Y una validación adicional, específica de P8:**

```bash
# Cada ficha debe llevar el dominio de origen (blockchain / contabilidad pública)
# en su campo `source_type`. Se comprueba:
grep -c '"source_type"' bundle/ledger.json
grep -o '"source_type":"[^"]*"' bundle/ledger.json | sort -u
```

Deben aparecer al menos los dos valores: `ONCHAIN` y `PUBLIC_API` (o el que corresponda a cada dominio).

---

## 7. FUERA DE ALCANCE

- ❌ Datos del portafolio personal del operador
- ❌ Cifras estimadas o proyectadas
- ❌ Modificar el contrato de P1
- ❌ Publicar (requiere HG-001)
- ❌ Escribir software de producción; el entregable es un informe y un ledger

---

## 8. MISIONES

| ID | Misión | Salida |
|---|---|---|
| **M-P8-01** | Diseñar el ledger: qué fichas de cada dominio entran | `DOMINIOS.md` → **filtro de la verificación independiente** |
| **M-P8-02** | Reconciliar: emitir el ledger con todas las fichas | `ledger.json` + `reconciliacion.md` |
| **M-P8-03** | Declarar los huecos | `unknowns.md` |
| **M-P8-04** | Documentar y validar | `reasoning.md` + `INFORME.md` |

**M-P8-01 requiere aprobación antes de seguir.**

---

## 9. CRITERIO DE TERMINADO

`PASS` cuando:

1. El validador dice `APROBADO` sobre el ledger
2. Cada ficha del ledger tiene su dominio de origen claramente identificado
3. Los dos dominios se distinguen sin colapsar
4. Existe al menos un hueco declarado
5. Un tercero sigue `reasoning.md` y llega a la misma conclusión

---

## 10. HUMAN GATES

- **HG-001** — publicación externa
- **HG-009** — aprobación del diseño de ledger (verificación independiente)