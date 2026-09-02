"""Verifica el desglose de `carrito.resumen.resumen()`: las líneas opcionales
(Promociones, Cupones) solo aparecen cuando cambian el monto, y el orden
coincide con "Cómo se arma el total" en el README.
"""

from carrito.modelo import Cupon, Linea, Pedido, Producto
from carrito.resumen import resumen


def test_resumen_sin_promociones_ni_cupones_omite_esas_lineas():
    product = Producto(sku="DEMO-03", nombre="Producto demo 3", precio=550)
    order = Pedido(numero=3, lineas=[Linea(product, 1)])

    breakdown = resumen(order)

    # Subtotal 550, sin descuentos: IVA 105 (ver test_impuestos.py), envío
    # 3990 (metropolitana, bajo el umbral de envío gratis).
    assert list(breakdown.keys()) == ["Subtotal", "IVA", "Envío", "Total"]
    assert breakdown["Subtotal"] == 550
    assert breakdown["IVA"] == 105
    assert breakdown["Envío"] == 3990
    assert breakdown["Total"] == 550 + 105 + 3990


def test_resumen_con_promociones_y_cupones_desglosa_cada_etapa():
    product = Producto(sku="DEMO-02", nombre="Producto demo 2", precio=1000)
    order = Pedido(
        numero=2,
        lineas=[Linea(product, 10)],
        promociones=["volumen"],
        cupones=[
            Cupon(codigo="VALE300", tipo="monto", valor=300),
            Cupon(codigo="DESC20", tipo="porcentaje", valor=20),
        ],
    )

    breakdown = resumen(order)

    # Mismos montos que test_total_con_descuentos_encadena_promocion_y_cupones_en_orden
    # en test_descuentos.py: subtotal 10000, tras promoción "volumen" 9500,
    # tras cupones (porcentual antes que fijo) 7300.
    assert list(breakdown.keys()) == [
        "Subtotal",
        "Promociones",
        "Cupones",
        "IVA",
        "Envío",
        "Total",
    ]
    assert breakdown["Subtotal"] == 10000
    assert breakdown["Promociones"] == -500
    assert breakdown["Cupones"] == -2200
    assert breakdown["IVA"] == 1387
    assert breakdown["Envío"] == 3990
    assert breakdown["Total"] == 7300 + 1387 + 3990
