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
   cupones porcentuales, después los vales de monto fijo. El orden importa
   cuando hay más de uno.
4. **IVA** — 19% sobre el monto ya descontado.
5. **Envío** — según la región, gratis sobre los $50.000 o gratis para
   clientes en su primera compra (`cliente_nuevo`).

## Problemas conocidos

- **Un pedido a un número inexistente revienta con traceback.**
  `carrito.datos.pedido()` documenta que lanza `KeyError` si el número no
  existe, pero `cli.py` no lo captura — no hay un mensaje de error legible
  para el usuario del CLI.
- **Cobertura de tests parcial.** `tests/` solo cubre `descuentos.py` e
  `impuestos.py` (corrieron en CI el orden de cupones y el redondeo del
  IVA). `precios.py`, `envio.py`, `resumen.py`, `cli.py` y `datos.py` no
  tienen tests.
- **Nombres en inglés dentro de un código en español.**
  `descuentos.volume_discount(order, amount)` y
  `envio.free_shipping_for_new_customer(order)` rompen la convención de
  nombres en español (`pedido`, `monto`) del resto del proyecto.
- **`datos.cargar()` relee y reparsea `ejemplo.json` en cada llamada**, sin
  caché. No es un problema hoy, pero conviene resolverlo antes de que el CLI
  se use con más frecuencia.
