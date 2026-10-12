# Contrato de datos: `daily_sales`

- **Consumidor:** cuadro de mando de Dirección Comercial.
- **Responsable:** equipo de datos.
- **Fichero:** `output/daily_sales.csv`.

## Grano

Una fila por día y país.

## Columnas

| Columna | Tipo | Descripción |
| --- | --- | --- |
| `sales_date` | fecha `AAAA-MM-DD` | Día natural de la venta en hora peninsular española (`Europe/Madrid`), a partir de `created_at` |
| `country` | texto | País del cliente (ISO 3166-1 alfa-2). Si el cliente no lo tiene informado, `UNKNOWN` |
| `orders_count` | entero | Número de ventas |
| `gross_amount` | decimal | Importe de las ventas en EUR, con dos decimales |

## Qué es una venta

Un pedido es una venta si, en su **última versión**:

1. no está cancelado (`status` distinto de `cancelled`), y
2. tiene al menos un pago con `status = captured`.

Cada venta cuenta **una sola vez**, tenga los pagos que tenga.

## Importes

- Todos los importes se expresan en EUR. La conversión usa la tabla fija
  `data/reference/fx_rates.csv`: `importe_eur = importe × rate_to_eur`,
  redondeado a dos decimales.
- Un registro en una moneda que no esté en la tabla no se puede convertir:
  no se usa y se informa de él.

## Garantías

- La suma de `gross_amount` de todas las filas coincide con la suma de las
  ventas en EUR.
- Dos ejecuciones sobre los mismos datos dan el mismo fichero.
