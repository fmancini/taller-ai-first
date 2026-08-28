"""El resumen del pedido, desglosado."""

from carrito.descuentos import PROMOCIONES, monto_tras_cupones, monto_tras_promociones
from carrito.envio import costo_envio
from carrito.impuestos import iva
from carrito.precios import subtotal


ETIQUETAS = {
    "2x1": "Promoción 2x1",
    "volumen": "Descuento por volumen",
    "primera-compra": "Primera compra",
}


def resumen(pedido) -> dict[str, int]:
    """El desglose del pedido, en el mismo orden que 'Cómo se arma el
    total' en el README: subtotal, promociones, cupones, IVA y envío.
    """
    base = subtotal(pedido)
    tras_promociones = monto_tras_promociones(pedido)
    tras_cupones = monto_tras_cupones(pedido, tras_promociones)
    impuesto = iva(tras_cupones)
    envio = costo_envio(pedido, tras_cupones)

    lineas = {"Subtotal": base}
    if tras_promociones != base:
        lineas["Promociones"] = tras_promociones - base
    if tras_cupones != tras_promociones:
        lineas["Cupones"] = tras_cupones - tras_promociones
    lineas["IVA"] = impuesto
    lineas["Envío"] = envio
    lineas["Total"] = tras_cupones + impuesto + envio
    return lineas
