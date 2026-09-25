# Dónde va cada cosa

Hay **dos** carpetas llamadas `entregables` y es fácil confundirlas. Esta es la
de SALIDA de P2: aquí escribes tú.

| Ruta | Qué es | ¿Escribes? |
|---|---|---|
| `proyectos/P1_ESQUEMA_EVIDENCIA/entregables/` | **El contrato publicado**: el esquema, el manual y los ejemplos de P1 | ❌ NO — es de solo lectura |
| `proyectos/P2_DEMO_RECONSTRUCCION/entregables/` | **Tu salida**: el bundle y el informe | ✅ Sí |

## El contrato que tienes que cumplir

```
proyectos/P1_ESQUEMA_EVIDENCIA/entregables/
    evidence-envelope.schema.json   ← la definición normativa (22 casillas)
    SPEC.md                         ← el manual: cómo rellenar cada una
    examples/                       ← cuatro fichas de ejemplo ya conformes
```

**Si el manual y el esquema difieren, manda el esquema.**

Copia la forma de `examples/` para tu primera ficha: es lo más rápido y lo más
seguro. La ficha `01-public-chain.json` es la que más se parece a lo que vas a
hacer.

## Tu salida

```
entregables/
    WALLET.md               la wallet elegida y por qué
    bundle/positions.json   las fichas (una lista con varias dentro)
    bundle/evidence.md      cada dato con su llamada exacta
    bundle/unknowns.md      LOS HUECOS, declarados
    bundle/reasoning.md     el razonamiento paso a paso
    INFORME.md              qué se pudo y qué no
```

## La validación

```bash
python3 herramientas/validar_evidencia.py \
    proyectos/P2_DEMO_RECONSTRUCCION
```

**Encuentra el esquema de P1 sola**: no copies el esquema aquí, ni le indiques
dónde está. Si dijera «no encontré ningún archivo *.schema.json», es un fallo de
la herramienta y hay que reportarlo — no algo que rodear copiando el esquema.
