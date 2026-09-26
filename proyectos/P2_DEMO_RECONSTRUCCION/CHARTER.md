# CHARTER — P2 `DEMO_RECONSTRUCCION`

**Estado:** ✅ **PUBLICADO** · **Nivel:** **N1–N2**
**Ola:** 1 · **Coste estimado:** 3–4 días
**Autoría:** quien construye el entregable P2 · **Verificación:** independiente (ajena a la autoría) · **Aprobado:** 2026-09-21
**Abierto:** 2026-09-23, al cerrarse y publicarse P1

---

## 1. OBJETIVO

Producir un **bundle de evidencia reconstruible** de una wallet pública **que no sea del
operador**, aplicando el método de LAMC de punta a punta.

**Frase falsifiable:** *un tercero lee el bundle y reconstruye la posición sin hacer
ninguna pregunta al autor.*

---

## 2. POR QUÉ ESTE PROYECTO

Ataca de frente la objeción que mata a LAMC como producto:

> *"Esto solo funciona para el portafolio de una persona."*

Una demostración sobre un tercero lo desmiente **sin tocar los libros propios** — que es
exactamente lo que este programa necesita dado que la reconciliación corre por otro carril.

Además es el mejor artefacto de venta posible: no dice *"puedo hacer esto"*; **muestra el
resultado**. Y es lo que hará que P5 (la calculadora) tenga a dónde atraer tráfico.

---

## 3. RESTRICCIÓN DE ENTORNO — LEER ANTES DE EMPEZAR

**Verificado:** el repositorio interno de observabilidad **no existe en este entorno**.
El directorio de trabajo del operador no está disponible. Solo está el corpus documental en (ruta interna omitida).

Esto obliga a elegir un camino. **La elección corresponde al verificador independiente, no a quien construye:**

| Camino | Descripción | Coste | Requiere |
|---|---|---|---|
| **A — Reconstrucción desde fuentes públicas** | Quien construye consulta RPC/exploradores públicos (curl) y arma el bundle a mano, aplicando el esquema de P1 | 3–4 días | Nada. Autocontenido |
| **B — Pipeline real** | Se ejecuta en la infraestructura interna, donde vive el repositorio | Depende de acceso | Acceso a la infraestructura interna + autorización humana expresa |

**Camino por defecto: A.** Es autocontenido, no depende de infraestructura y demuestra
mejor el método (porque el esfuerzo de procedencia queda a la vista).
Cambiar a B requiere **autorización humana expresa**.

---

## 4. ENTREGABLE

Todos los entregables van en `proyectos/P2_DEMO_RECONSTRUCCION/entregables/`.

| # | Artefacto | Descripción |
|---|---|---|
| E-P2-01 | `WALLET.md` | La wallet elegida, por qué, y su justificación |
| E-P2-02 | `bundle/positions.json` | Posiciones observadas, conformes al esquema de P1 |
| E-P2-03 | `bundle/evidence.md` | Cada dato con su `raw_reference` citable |
| E-P2-04 | `bundle/unknowns.md` | **Los huecos, declarados explícitamente como UNKNOWN** |
| E-P2-05 | `bundle/reasoning.md` | El razonamiento reconstruible paso a paso |
| E-P2-06 | `INFORME.md` | Qué se pudo y qué no se pudo determinar, y por qué |

**El artefacto E-P2-04 es el más importante del proyecto.** Un bundle sin huecos
declarados demuestra lo contrario de lo que se pretende: que el autor no distingue
lo que sabe de lo que supone.

---

## 5. SELECCIÓN DE LA WALLET — CRITERIO

> ## ⛔ REGLA BLOQUEANTE — SE LEE ANTES QUE NADA
>
> ### La wallet tiene que ser una **ENTIDAD PÚBLICA DOCUMENTADA**.
>
> Una tesorería de DAO, un multisig de protocolo, una fundación, una organización
> **que haya publicado esa dirección como suya**.
>
> ### Si es una **dirección pseudónima que puede ser de un particular, SE RECHAZA.** Sin excepciones.
>
> **Que un explorador no le ponga nombre NO significa que no sea atribuible.** Solo
> significa que nadie la ha etiquetado *todavía*. Una dirección con historial se puede
> atribuir a una persona con análisis de cadena — es literalmente el trabajo de una
> industria entera.
>
> **Y el estándar ya está fijado.** Al publicar el contrato de P1 se sustituyó la cartera
> del propio operador —suya, y con su permiso— por **direcciones vacías generadas al azar**.
> Si el listón para quien **consintió** fue «ni una dirección real», el listón para quien
> **no ha consentido nada** no puede ser más bajo.
>
> **Dirección del operador, textual:** *«Debe mantener el anonimato al máximo. Debe quedar
> claro.»*
>
> **Cómo se comprueba:** la candidata aparece publicada **por la propia organización** como
> su dirección (documentación, gobernanza, blog, libro de direcciones oficial). Si la única
> fuente es un explorador que no le pone nombre, **no cumple**.

### Y además, los cinco criterios técnicos

- ✅ Actividad en **≥2 cadenas** (demuestra el multi-cadena)
- ✅ Posiciones en **≥2 protocolos** distintos (Aave, Morpho, Kamino, Orca, Pendle…)
- ✅ Al menos una posición **con apalancamiento** (demuestra el cálculo de HF/LTV)
- ✅ Datos públicamente accesibles por RPC o explorador
- ✅ **Entidad, no persona** — ya cubierto por la regla bloqueante de arriba

**Prohibido:** wallets del operador, wallets de personas conocidas identificables,
wallets señaladas en investigaciones por delitos, y **cualquier dirección pseudónima
que no esté publicada como propia por una organización.**

**Candidatas a evaluar:** tesorerías de DAO, multisigs de protocolos, fundaciones, y
direcciones de ejemplo citadas en documentación pública **como de una entidad**.

> **Lo que NO sirve como justificación:** «no tiene etiqueta pública», «no la he
> atribuido», «casi seguro que es un fondo». **Ninguna de las tres es una comprobación**
> de que no sea una persona. La comprobación es que **una organización la publique
> como suya.**

---

## 6. VALIDACIÓN DETERMINÍSTICA

```bash
python3 herramientas/validar_evidencia.py \
    proyectos/P2_DEMO_RECONSTRUCCION
```

La herramienta **encuentra sola el esquema de P1**: no hay que copiarlo aquí ni
indicarle dónde está. Comprueba que cada posición tiene las **22 casillas**
completas, que los valores están en las listas permitidas, que ninguna ficha lleva
claves que el contrato no admite, que la partición `known`/`unknown` cubre las 22
sin solaparse y sin dejar ninguna fuera, y que **ningún `unknown` va sin su
`unknown_reason`** (regla bloqueante).

**Criterio:** los cuatro bloques del validador pasan, y el informe declara al menos **un** hueco `UNKNOWN`
(una reconstrucción sin huecos es sospechosa, no perfecta).

---

## 7. FUERA DE ALCANCE

- ❌ Tocar wallets propias o del operador
- ❌ Exponer información atribuible a personas identificables
- ❌ Publicar (requiere autorización humana expresa)
- ❌ Construir infraestructura de observabilidad permanente
- ❌ Ejecutar cualquier transacción
- ❌ Interactuar con contratos (solo lectura)

---

## 8. RIESGOS

| ID | Riesgo | Mitigación |
|---|---|---|
| R-009 | Wallet trivial que no demuestre nada | Criterio de selección obligatorio (§5); el verificador independiente aprueba la elección |
| R-010 | La reconstrucción parece perfecta ⇒ parece inventada | Obligatorio declarar huecos; sin `unknowns.md` no hay `PASS` |
| R-011 | Exposición de privacidad de terceros | Criterio §5 + verificación independiente |
| R-012 | Deriva hacia construir un producto | Prohibido en §7; el entregable es un informe, no software |
| R-013 | **Publicar sin querer un dato de una persona** | Aprendido al publicar P1: el bundle no lleva rutas, correos, nombres de sistemas ni nada atribuible. **Y si algún día se publica, el historial de git también viaja: limpiar los archivos no basta** |

---

## 9. MISIONES

| ID | Misión | Salida |
|---|---|---|
| **M-P2-01** | Proponer 3 wallets candidatas con justificación | Tabla de candidatas → **filtro del verificador independiente** + **autorización del operador** si la candidata no es una entidad pública documentada |
| **M-P2-02** | Reconstruir las posiciones desde fuentes públicas | `positions.json` + `evidence.md` |
| **M-P2-03** | Declarar los huecos | `unknowns.md` |
| **M-P2-04** | Documentar el razonamiento y correr validación | `reasoning.md` + salida del comando de validación |

**M-P2-01 requiere aprobación antes de continuar.** No empezar la reconstrucción sin
la wallet aprobada.

---

## 10. CRITERIO DE TERMINADO

`PASS` cuando:
1. El comando de validación pasa (los cuatro bloques del validador).
2. Existe al menos un hueco declarado como `UNKNOWN`.
3. Un tercero puede seguir `reasoning.md` y llegar a las mismas conclusiones.

---

## 11. AUTORIZACIONES REQUERIDAS

- **Publicación externa** — requiere autorización humana expresa.
- **Camino B (pipeline real en la infraestructura interna)** — requiere autorización humana expresa.
- **Aprobación de la wallet elegida.** **Tiene DOS partes, y conviene no
  confundirlas** (corregido el 2026-09-23: el charter decía «delegado a la verificación
  independiente» y a quien construye se le dijo «lo aprueba el operador» — una regla en dos
  sitios que no decían lo mismo):
  - **La idoneidad técnica** —que la wallet demuestre lo que hay que demostrar— **la juzga el
    verificador independiente.** Está delegada.
  - **La privacidad de un tercero** —si se reconstruyen y publican las finanzas de alguien que
    no ha dado permiso— **la autoriza el operador.** No es delegable: es material e
    irreversible, y es exactamente el tipo de decisión que el programa reserva al humano.
  - **Regla práctica:** si la candidata es una **entidad pública documentada** (una tesorería de
    DAO, un multisig de protocolo, una fundación), decide el verificador independiente. Si es una **dirección
    pseudónima que puede ser de un particular**, autoriza el operador.
