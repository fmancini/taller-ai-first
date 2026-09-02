# AGENTS.md

Este archivo le da contexto a Claude Code (claude.ai/code) para trabajar en este repositorio.

## Comandos

```sh
uv sync                                      # instalar dependencias
uv run python -m carrito total --pedido 42   # correr el CLI (el único comando es "total")
uv run pytest                                # correr toda la suite de tests
uv run pytest tests/test_impuestos.py        # correr un archivo de tests
uv run pytest tests/test_impuestos.py::test_iva_redondea_el_medio_peso_hacia_arriba  # correr un test puntual
```

Opciones del CLI para `total`: `--pedido <n>` (obligatorio), `--detalle`
(imprime cada línea del pedido), `--sin <promoción>` (repetible; excluye una
promoción por su clave en `carrito.descuentos.PROMOCIONES`: `2x1`, `volumen`,
`primera-compra`).

CI (`.github/workflows/tests.yml`) corre `uv sync --locked` y después
`uv run pytest` en cada push/PR.

## Arquitectura

Es una calculadora de totales de pedido chica. Todo se lee desde
`datos/ejemplo.json` (productos y pedidos de ejemplo) vía
`carrito.datos.cargar()` — todavía no hay base de datos, y tampoco hay
caché, así que cada llamada a `pedido(numero)` reparsea el archivo JSON
completo.

El total se arma como un pipeline fijo, y cada etapa vive en su propio
módulo:

1. **Subtotal** (`precios.py`) — suma de `precio * cantidad` por línea.
2. **Promociones** (`descuentos.py`) — 2x1, descuento por volumen (10 o más
   unidades) y descuento de primera compra, aplicadas según lo que traiga
   `pedido.promociones` y busque el diccionario `PROMOCIONES`. Se calculan
   sobre el subtotal y se suman entre sí (no se encadenan).
3. **Cupones** (`descuentos.py`) — se aplican sobre el monto que queda tras
   las promociones. **El orden importa y es una política deliberada**: los
   cupones porcentuales siempre se aplican antes que los de monto fijo, sin
   importar el orden en que aparezcan en `pedido.cupones`
   (`monto_tras_cupones` los particiona y reordena). Esto fue un bug antes;
   `tests/test_descuentos.py` lo protege.
4. **IVA** (`impuestos.py`) — 19% sobre el monto ya descontado.
5. **Envío** (`envio.py`) — tarifa plana según la región (`TRAMOS`), gratis
   sobre `UMBRAL_ENVIO_GRATIS` ($50.000) o para `cliente_nuevo` en su primera
   compra.

`resumen.py` vuelve a correr este pipeline (no usa
`descuentos.total_con_descuentos`, que solo usan los tests) para armar el
diccionario de desglose que se imprime, en el mismo orden documentado
arriba. `cli.py` solo formatea ese diccionario como columnas alineadas.

**El redondeo está centralizado**: cualquier cálculo que produzca una
fracción de peso (porcentajes, descuentos, IVA) debe pasar por
`dinero.porcentaje()` / `dinero.redondear()`, que redondean el medio peso
hacia arriba. No reimplementes el redondeo a mano en un módulo nuevo — es
exactamente el bug que protege `tests/test_impuestos.py`.

**Convención de nombres**: el código actual mezcla español (`pedido`,
`monto`, `cantidad`, la mayoría de los identificadores) con excepciones en
inglés (`descuentos.volume_discount(order, amount)`,
`envio.free_shipping_for_new_customer(order)`). No sigas ese patrón mixto:
de ahora en adelante, todo identificador nuevo (funciones, variables,
parámetros, clases) va en inglés. No renombres lo existente solo por esto;
aplica la regla al código que agregues o toques de ahora en más.

## Documentación vs. código

Si la documentación (README, docstrings, este archivo) contradice lo que
hace el código, seguí lo que dice la documentación — pero avisale al
usuario de la contradicción antes de actuar, en vez de resolverla en
silencio.
