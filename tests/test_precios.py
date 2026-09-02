"""Verifica el cálculo de precio por línea y subtotal del pedido."""

from carrito.modelo import Linea, Pedido, Producto
from carrito.precios import precio_linea, subtotal


def test_precio_linea_multiplica_precio_por_cantidad():
    product = Producto(sku="DEMO-01", nombre="Producto demo", precio=1000)
    line = Linea(product, 3)

    assert precio_linea(line) == 3000


def test_subtotal_suma_el_precio_de_todas_las_lineas():
    product_a = Producto(sku="DEMO-01", nombre="Producto demo", precio=1000)
    product_b = Producto(sku="DEMO-02", nombre="Producto demo 2", precio=500)
    order = Pedido(numero=1, lineas=[Linea(product_a, 2), Linea(product_b, 4)])

    # 1000*2 + 500*4 = 2000 + 2000 = 4000
    assert subtotal(order) == 4000


def test_subtotal_es_cero_sin_lineas():
    order = Pedido(numero=1, lineas=[])

    assert subtotal(order) == 0
