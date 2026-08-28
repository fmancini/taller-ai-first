"""Verifica que el IVA redondee igual que el resto del sistema.

`carrito.dinero` documenta una política de redondeo centralizada
(`redondear()`, usada por `porcentaje()`): el medio peso va hacia arriba.
`carrito.impuestos.iva()` calcula con `int(monto * IVA / 100)`, que trunca
en vez de redondear.
"""

from carrito.dinero import porcentaje
from carrito.impuestos import IVA, iva
from carrito.modelo import Linea, Pedido, Producto


def test_iva_redondea_el_medio_peso_hacia_arriba():
    producto = Producto(sku="DEMO-03", nombre="Producto demo 3", precio=550)
    pedido = Pedido(numero=3, lineas=[Linea(producto, 1)])

    monto = 550  # Sin promociones ni cupones: el monto gravado es el subtotal.
    # Política de redondeo centralizada (carrito.dinero.porcentaje/redondear):
    # 19% de 550 = 104.5, y el medio peso va hacia arriba -> 105.
    esperado = porcentaje(monto, IVA)
    assert esperado == 105

    assert iva(monto) == esperado
    assert pedido.lineas[0].producto.precio * pedido.lineas[0].cantidad == monto
