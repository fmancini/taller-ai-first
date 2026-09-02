"""Verifica el costo de envío por región y las condiciones de envío gratis
documentadas en el docstring de `carrito.envio`.
"""

from carrito.envio import TRAMOS, UMBRAL_ENVIO_GRATIS, costo_envio
from carrito.modelo import Pedido


def test_costo_envio_segun_la_region():
    order = Pedido(numero=1, region="extremo")

    assert costo_envio(order, monto=1000) == TRAMOS["extremo"]


def test_region_desconocida_usa_la_tarifa_de_regiones():
    order = Pedido(numero=1, region="patagonia")

    assert costo_envio(order, monto=1000) == TRAMOS["regiones"]


def test_envio_gratis_sobre_el_umbral():
    order = Pedido(numero=1, region="metropolitana")

    assert costo_envio(order, monto=UMBRAL_ENVIO_GRATIS) == 0
    assert costo_envio(order, monto=UMBRAL_ENVIO_GRATIS - 1) == TRAMOS["metropolitana"]


def test_envio_gratis_para_cliente_nuevo_aunque_no_llegue_al_umbral():
    order = Pedido(numero=1, region="extremo", cliente_nuevo=True)

    assert costo_envio(order, monto=1000) == 0
