"""Verifica la política de orden de cupones documentada en el docstring de
`carrito.descuentos`: los cupones porcentuales se aplican primero, y sobre
el monto que queda, los vales de monto fijo.
"""

from carrito.descuentos import total_con_descuentos
from carrito.modelo import Cupon, Linea, Pedido, Producto


def test_cupon_porcentual_se_aplica_antes_que_vale_de_monto_fijo():
    producto = Producto(sku="DEMO-01", nombre="Producto demo", precio=1000)
    pedido = Pedido(
        numero=1,
        lineas=[Linea(producto, 10)],
        cupones=[
            Cupon(codigo="DESC10", tipo="porcentaje", valor=10),
            Cupon(codigo="VALE2000", tipo="monto", valor=2000),
        ],
    )

    # Subtotal: 1000 * 10 = 10000 (sin promociones).
    # Política documentada: primero el porcentual, después el fijo.
    #   10000 - 10% de 10000 (1000) = 9000
    #   9000 - 2000 (vale fijo)     = 7000
    assert total_con_descuentos(pedido) == 7000


def test_total_con_descuentos_encadena_promocion_y_cupones_en_orden():
    producto = Producto(sku="DEMO-02", nombre="Producto demo 2", precio=1000)
    pedido = Pedido(
        numero=2,
        lineas=[Linea(producto, 10)],
        promociones=["volumen"],
        cupones=[
            Cupon(codigo="VALE300", tipo="monto", valor=300),
            Cupon(codigo="DESC20", tipo="porcentaje", valor=20),
        ],
    )

    # Subtotal: 1000 * 10 = 10000.
    # Promoción "volumen" (10 o más unidades): 5% del subtotal = 500,
    # se resta del subtotal -> 10000 - 500 = 9500.
    # Cupones sobre ese monto, porcentual primero y fijo después:
    #   9500 - 20% de 9500 (1900) = 7600
    #   7600 - 300 (vale fijo)    = 7300
    assert total_con_descuentos(pedido) == 7300
