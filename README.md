# carrito

Cálculo del total de un pedido: precios, descuentos, impuesto y envío.

```sh
uv sync
uv run python -m carrito total --pedido 42
```

Opciones del comando `total`:

- `--pedido` (obligatorio): número del pedido a consultar.
- `--detalle`: además del resumen, imprime cada línea con producto, cantidad
  y precio.
- `--sin <promoción>`: excluye una promoción puntual del cálculo (repetible).
  Los valores válidos son las claves de `carrito.descuentos.PROMOCIONES`
  (`2x1`, `volumen`, `primera-compra`).

## Cómo se arma el total

1. **Subtotal** — la suma de las líneas.
2. **Promociones** — 2x1, descuento por volumen (10 unidades o más) y primera
   compra, si el pedido las trae (`pedido.promociones`). Se calculan sobre el
   subtotal y se suman entre sí.
3. **Cupones** — sobre el monto que queda tras las promociones: primero los
   vales de monto fijo, después los cupones porcentuales. El orden importa
   cuando hay más de uno.
4. **IVA** — 19% sobre el monto ya descontado.
5. **Envío** — según la región, gratis sobre los $50.000 o gratis para
   clientes en su primera compra (`cliente_nuevo`).

## Reportes

Para sacar el resumen en CSV se usa `carrito.exportar.a_csv()`, que es lo que
consume el sistema de reportes.

## Próximos pasos

- Los pedidos se van a mover de `datos/ejemplo.json` a **Postgres**; el módulo
  `carrito.datos` va a hablar con la base a través de SQLAlchemy.
- La **API REST** reemplaza al CLI. El CLI queda como herramienta de depuración.
- El catálogo de productos pasa a un servicio aparte y se consulta por HTTP.
