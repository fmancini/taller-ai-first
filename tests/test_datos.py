"""Verifica la carga de pedidos desde `datos/ejemplo.json`. Usa los pedidos
41, 42 y 46 porque son parte del set original del archivo (no dependen de
líneas agregadas después).
"""

import pytest

from carrito.datos import cargar, pedido
from carrito.modelo import Pedido


def test_cargar_devuelve_pedidos_indexados_por_numero():
    orders = cargar()

    assert 41 in orders
    assert isinstance(orders[41], Pedido)
    assert orders[41].numero == 41


def test_pedido_arma_las_lineas_con_su_producto():
    order = pedido(41)

    assert len(order.lineas) == 1
    line = order.lineas[0]
    assert line.producto.sku == "TAZA-01"
    assert line.cantidad == 2


def test_pedido_usa_los_valores_por_defecto_cuando_faltan_en_el_json():
    order = pedido(41)

    assert order.region == "metropolitana"
    assert order.cupones == []
    assert order.promociones == []
    assert order.cliente_nuevo is False


def test_pedido_toma_region_y_cliente_nuevo_del_json():
    order = pedido(46)

    assert order.region == "extremo"
    assert order.cliente_nuevo is True
    assert order.promociones == ["primera-compra"]


def test_pedido_lanza_keyerror_si_el_numero_no_existe():
    with pytest.raises(KeyError):
        pedido(999999)
