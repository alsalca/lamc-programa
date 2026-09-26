# DOMINIO — P7 SEGUNDO DOMINIO

## Entidad elegida

**Ayuntamiento de Barcelona** — organismo público (administración local, artículo 137 de la Constitución Española).

## Tipo de entidad

- **Forma jurídica:** Administración pública local (ayuntamiento)
- **Sujetos a:** Ley de Haciendas Locales (Real Decreto Legislativo 2/2004), Plan General de Contabilidad Pública
- **Obligación de publicar cuentas:** Sí — la Cuenta General se aprueba por el Pleno y se remite a la Sindicatura de Comptes de Catalunya para auditoría
- **Titularidad:** No es persona física. El ayuntamiento es una entidad de derecho público con personalidad jurídica propia

## Prueba de que es entidad (no persona)

| Criterio | Evidencia |
|----------|-----------|
| Publica sus cuentas | [Cuentas Generales e Informes Financieros](https://ajuntament.barcelona.cat/pressupostosifinances/es/resultados-e-informes-financieros/cuentas-generales-e-informes-financieros) — página oficial del ayuntamiento |
| Documentos descargables | Sí — PDFs desde 2001 hasta 2024. Cuenta General 2023: [enlace directo](https://ajuntament.barcelona.cat/pressupostosifinances/sites/default/files/COMPTE%20GENERAL%202023.pdf) (26.8 MB, 169 páginas) |
| No es persona | El ayuntamiento es una entidad de derecho público. Los datos son agregados institucionales, no individuales |

## Verificación PII (Datos Personales Identificables)

**Método:** Extracción de texto completo del PDF con `pypdf` (169 páginas), búsqueda de patrones regex y palabras clave.

| Patrón buscado | Resultado |
|----------------|-----------|
| DNI (8 dígitos + letra) | **0 resultados** |
| Emails | **0 resultados** |
| Títulos personales (Sr./Sra./D./Ilmo.) | **0 resultados** |
| Nómina | **0 ocurrencias** |
| Salario/sueldo con cifras | **0 líneas** |
| Direcciones personales | **0 resultados** |

**Conclusión:** La Cuenta General 2023 del Ayuntamiento de Barcelona contiene exclusivamente datos agregados institucionales. No hay datos personales identificables. El dominio cumple estrictamente la regla bloqueante de no-PII.

## Tipo de documentos

- **Cuenta General** — documentos oficiales con balance, cuenta de resultados, estados de cambios en patrimonio neto, estados de flujos de efectivo y liquidación presupuestaria
- **Formato:** PDF firmado digitalmente
- **Idioma original:** Catalán
- **Auditoría:** Sindicatura de Comptes de Catalunya (órgano público fiscalizador)
- **Periodicidad:** Anual (ejercicio natural: 1 enero - 31 diciembre)
- **Serie disponible:** 2001-2024 (24 ejercicios)

## Por qué este dominio tensa el contrato

1. **Contabilidad pública vs. privada:** Usa base presupuestaria + patrimonial (PGCP), distinta de las NIIF/IFRS usadas en el dominio crypto
2. **Entes consolidados:** El ayuntamiento tiene organismos autónomos, entidades públicas empresariales, sociedades municipales, consorcios, fundaciones y asociaciones — todos consolidados en la Cuenta General
3. **Fechas de corte:** El documento presenta datos al 31 de diciembre pero con devengo presupuestario y financiero que pueden dar cifras distintas
4. **Obligaciones múltiples:** Deuda financiera, provisiones, litigios, compromisos ambientales, transferencias — cada una con su propia dinámica temporal
5. **Documento largo y complejo:** 169 páginas en catalán con tablas densas — el caso difícil de extracción de datos

---

*Documento generado por P7-BCN. Fuente primaria verificada con descarga real del PDF.*
