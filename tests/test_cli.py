"""Verifica el comando `total` del CLI contra los pedidos de
`datos/ejemplo.json`. Usa los pedidos 42 y 44 porque son parte del set
original del archivo.
"""

import pytest

from carrito.cli import main


def parse_summary(output: str) -> dict[str, int]:
    """Cada línea impresa es "etiqueta monto"; parsea sin depender del
    ancho exacto de las columnas alineadas.
    """
    return {
        line.split()[0]: int(line.split()[1])
        for line in output.strip().splitlines()
    }


def test_total_imprime_el_resumen_alineado(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["carrito", "total", "--pedido", "42"])

    main()

    # Pedido 42: LIBR-02 (12500) + LANA-03 (36900) = subtotal 49400, sin
    # promociones ni cupones, región metropolitana.
    summary = parse_summary(capsys.readouterr().out)
    assert summary == {"Subtotal": 49400, "IVA": 9386, "Envío": 3990, "Total": 62776}


def test_detalle_imprime_cada_linea_y_un_separador(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv", ["carrito", "total", "--pedido", "42", "--detalle"]
    )

    main()

    output = capsys.readouterr().out.splitlines()
    assert output[0] == "Cuaderno cosido x 1 12500"
    assert output[1] == "Chal de lana x 1 36900"
    assert output[2] == "-"


def test_sin_excluye_la_promocion_del_calculo(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv", ["carrito", "total", "--pedido", "44", "--sin", "volumen"]
    )

    main()

    # Pedido 44: TAZA-01 x 12 (8990 c/u) = subtotal 107880. Sin la promoción
    # "volumen" no hay línea de Promociones ni de Cupones, y el subtotal ya
    # supera el umbral de envío gratis.
    summary = parse_summary(capsys.readouterr().out)
    assert summary == {"Subtotal": 107880, "IVA": 20497, "Envío": 0, "Total": 128377}


def test_pedido_inexistente_revienta_con_keyerror(monkeypatch):
    """Documenta la deuda conocida en AGENTS.md: cli.py no captura el
    KeyError que lanza datos.pedido() para un número inexistente.
    """
    monkeypatch.setattr("sys.argv", ["carrito", "total", "--pedido", "999999"])

    with pytest.raises(KeyError):
        main()
