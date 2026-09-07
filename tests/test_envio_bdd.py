"""Steps de pytest-bdd para tests/features/envio.feature.

No toca carrito/*: algunos escenarios documentan una decisión de negocio (el
IVA cuenta para el umbral de envío gratis) que envio.py todavía no
implementa, así que se espera que fallen hasta que se actualice el código.
"""

from pytest_bdd import given, parsers, scenarios, then, when

from carrito.modelo import Cupon, Linea, Pedido, Producto
from carrito.resumen import resumen

scenarios("features/envio.feature")


def _convertir_monto(texto: str) -> int:
    return int(texto.replace(".", ""))


_convertir_monto.pattern = r"[\d.]+"

EXTRA_TYPES = {"Monto": _convertir_monto}


@given(parsers.parse('un pedido en la región "{region}"'), target_fixture="pedido")
def pedido_en_region(region):
    return Pedido(numero=1, region=region)


@given("un cliente nuevo")
def marcar_cliente_nuevo(pedido):
    pedido.cliente_nuevo = True


@given(
    parsers.parse(
        "una línea con un producto de ${precio:Monto}, cantidad {cantidad:d}",
        extra_types=EXTRA_TYPES,
    )
)
def agregar_linea(pedido, precio, cantidad):
    producto = Producto(sku=f"SKU-{precio}", nombre="Producto de prueba", precio=precio)
    pedido.lineas.append(Linea(producto=producto, cantidad=cantidad))


@given(
    parsers.parse(
        'un cupón de tipo "{tipo}" por ${valor:Monto}', extra_types=EXTRA_TYPES
    )
)
def agregar_cupon(pedido, tipo, valor):
    pedido.cupones.append(Cupon(codigo=f"CUPON-{valor}", tipo=tipo, valor=valor))


@given(parsers.parse('la promoción "{nombre}" aplicada'))
def agregar_promocion(pedido, nombre):
    pedido.promociones.append(nombre)


@when("se calcula el resumen del pedido", target_fixture="resultado")
def calcular_resumen(pedido):
    return resumen(pedido)


@then(
    parsers.parse(
        "el monto que se compara con el umbral es ${monto_esperado:Monto}",
        extra_types=EXTRA_TYPES,
    )
)
def verificar_monto_umbral(resultado, monto_esperado):
    monto_umbral = resultado["Total"] - resultado["Envío"]
    assert monto_umbral == monto_esperado


@then("el envío es gratis")
def verificar_envio_gratis(resultado):
    assert resultado["Envío"] == 0


@then(parsers.parse("el envío cuesta ${monto:Monto}", extra_types=EXTRA_TYPES))
def verificar_envio_cuesta(resultado, monto):
    assert resultado["Envío"] == monto
