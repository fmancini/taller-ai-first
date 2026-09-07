# language: es
# Decisiones de negocio para esta regla (no se discuten en la revisión):
#   1. El umbral de $50.000 se evalúa sobre el monto ya con promociones y
#      cupones aplicados (después del descuento).
#   2. El IVA cuenta para el umbral: se compara el monto descontado más IVA.
#   3. Las promociones descuentan del monto igual que los cupones.
#   4. Con $50.000 justos (monto + IVA) el envío es gratis (umbral inclusivo,
#      >=).
#   Además, un cliente nuevo no paga envío en su primera compra sin importar
#   el monto: esa regla no depende del umbral.

Característica: Envío gratis
  Como cliente que arma un pedido
  Quiero saber cuándo el envío sale gratis
  Para no llevarme una sorpresa en el total

  Antecedentes:
    Dado un pedido en la región "metropolitana"

  Esquema del escenario: El umbral de envío gratis se evalúa sobre el monto con IVA incluido
    Dado una línea con un producto de $<precio_unitario>, cantidad 1
    Cuando se calcula el resumen del pedido
    Entonces el monto que se compara con el umbral es $<monto_umbral>
    Y el envío <resultado>

    Ejemplos:
      | precio_unitario | monto_umbral | resultado           |
      | 10000           | 11900        | cuesta $3.990       |
      | 42016           | 49999        | cuesta $3.990       |
      | 42017           | 50000        | es gratis           |
      | 42018           | 50001        | es gratis           |

  Escenario: Un cupón que reduce el monto por debajo del umbral hace que el envío deje de ser gratis
    # Sin el cupón, $60.000 + IVA ($71.400) ya calificaría para envío gratis.
    Dado una línea con un producto de $60.000, cantidad 1
    Y un cupón de tipo "monto" por $20.000
    Cuando se calcula el resumen del pedido
    Entonces el monto que se compara con el umbral es $47.600
    Y el envío cuesta $3.990

  Escenario: Una promoción que reduce el monto por debajo del umbral hace que el envío deje de ser gratis
    # Sin la promoción, $60.000 + IVA ($71.400) ya calificaría para envío gratis.
    Dado una línea con un producto de $30.000, cantidad 2
    Y la promoción "2x1" aplicada
    Cuando se calcula el resumen del pedido
    Entonces el monto que se compara con el umbral es $35.700
    Y el envío cuesta $3.990

  Escenario: Un cliente nuevo no paga envío aunque el monto esté muy por debajo del umbral
    Dado un cliente nuevo
    Y una línea con un producto de $5.000, cantidad 1
    Cuando se calcula el resumen del pedido
    Entonces el monto que se compara con el umbral es $5.950
    Y el envío es gratis
