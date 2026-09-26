# INFORME — P8 RECONCILIACION

**Misión:** construir el ledger reconciliado que combina las fichas de P2 (blockchain)
y P7 (contabilidad pública) en un solo array JSON.
**Fecha de emisión:** 2026-09-25
**Estado de la validación:** `RESULTADO: APROBADO`.

---

## 1. Qué se pudo reconciliar

**Todo lo que estaba en alcance.** El ledger `bundle/ledger.json` contiene **13 fichas**:

| Dominio | Procedencia | Fichas | Estado interno |
|---|---|---|---|
| blockchain | P2_DEMO_RECONSTRUCCION / `positions.json` | `LAMC-P2-2026-0001` … `0007` | `unreconciled` |
| contabilidad_publica | P7_SEGUNDO_DOMINIO / `fichas.json` | `P7-BCN-2026-0001` … `0006` | `unreconciled` |

- Las **13 fichas se copian tal cual**: los 22 campos del contrato `evidence-envelope`
  v0.2.0 quedan **idénticos** a la fuente (verificado programáticamente).
- Cada ficha **pasa** la validación del esquema v0.2.0.
- Los **dos dominios no se fusionan**: cada ficha conserva su sujeto original y se
  distingue por `source_type`, `container.type`, `authority`, prefijo de `claim_id` y
  `producer`.

> **CORRECCIÓN 2026-09-25 (auditoría independiente, hallazgos 2 y 15).** Aquí decía que se
> añadía a cada ficha un campo `_meta` «**sin modificar** el contrato de P1». **Modificaba
> el contrato, y por eso se quitó:** una clave de más dentro de una ficha viola
> `additionalProperties: false`, que el sobre declara en la raíz. Las 13 fichas no
> validaban. Se eliminó `_meta`, su contenido está en la sección «Procedencia por ficha» de
> `bundle/reconciliacion.md`, y **el validador ahora comprueba esa regla** — antes no la
> comprobaba, y por eso decía APROBADO.

## 2. Qué NO se pudo reconciliar (y por qué)

1. **Reconciliación transversal entre dominios — no aplica.** Las fichas de blockchain
   y de contabilidad pública pertenecen a **sujetos distintos** (Aave DAO AHAB Safe vs
   Ayuntamiento de Barcelona), con divisas y naturalezas distintas. No existe ninguna
   cuenta ni magnitud en común que contrastar. Cruzarlas habría sido inventar una
   relación. Este pase concatena y clasifica las dos series; es correcto.

2. **`reconciliation_status` queda en `unreconciled` (las 13 fichas).** Es la **primera
   emisión** de este ledger. No existe todavía una segunda fuente por sujeto que
   confirme (`reconciled`) o contradiga (`disputed`) cada ficha. Marcarlas de otro modo
   sería simular una reconciliación que no se ha hecho (axioma A3).

3. **Huecos heredados — no resueltos.** Los `unknown` que traían las fuentes (p. ej.
   `quantity` en P2, `freshness` en P7) se preservan tal cual. Un hueco no
   desaparece por entrar en el ledger. Ver `bundle/unknowns.md`.

4. **Vigencia futura — no establecida.** Los datos de P7 son históricos (2023) y los de
   P2 están anclados a bloques del 2026-09-23. Nada del ledger establece hasta cuándo se
   describe el estado actual (limitación ya declarada por las fuentes).

## 3. El contrato de P1 no se tocó

El esquema `evidence-envelope.schema.json` v0.2.0 se usa **tal cual**.

> **CORRECCIÓN 2026-09-25 (auditoría, revisión 2, hallazgo 1).** Aquí decía: «La adición de
> `_meta` se hace en el ledger, no en el esquema». **Ya no hay adición ninguna.** `_meta` se
> añadía **dentro de cada ficha** —y cada ficha *es* el sobre—, así que violaba
> `additionalProperties: false`. Se retiró de las 13 fichas y su contenido está en
> `bundle/reconciliacion.md`. **El contrato no solo no se tocó: tampoco se rodeó.**

## 4. Validación

```bash
python3 herramientas/validar_evidencia.py \
    proyectos/P8_RECONCILIACION
```
→ **`RESULTADO: APROBADO`** — [1] esquema OK, [2] 13 fichas correctas,
[3] 13 fichas, [4] 2 autoridades (`PUBLIC_CHAIN`, `INSTITUTION_DOCUMENT`).

```bash
grep -o '"source_type":"[^"]*"' .../bundle/ledger.json | sort -u
# "source_type":"ONCHAIN"
# "source_type":"SIGNED_DOCUMENT"
# "source_type":"STRUCTURED_EXPORT"
```
Los tres valores presentes (`ONCHAIN` y `STRUCTURED_EXPORT` en blockchain, `SIGNED_DOCUMENT` en contabilidad pública) → los dos dominios quedan representados y distinguibles.

> **CORRECCIÓN 2026-09-26:** este bloque copiaba una salida del `grep` que ya no era la real: faltaba `STRUCTURED_EXPORT` (ficha `LAMC-P2-2026-0007`). Se reproduce la salida actual.

## 5. Entregables

| Artefacto | Ruta | Contenido |
|---|---|---|
| E-P8-02 | `bundle/ledger.json` | Ledger reconciliado (13 fichas) |
| E-P8-03 | `bundle/reconciliacion.md` | Qué está conciliado, qué no, y por qué |
| E-P8-04 | `bundle/unknowns.md` | Huecos declarados |
| E-P8-05 | `bundle/reasoning.md` | Razonamiento paso a paso |
| E-P8-06 | `INFORME.md` | Este informe |

## 6. Conclusión

Se cumple la frase falsifiable del charter: **un tercero puede leer el ledger y decir
qué parte viene de cada dominio, qué está conciliado y qué no.** Todas las fichas
conservan su dominio exacto, ninguna cifra se inventa, y los huecos quedan declarados
sin colapsar.