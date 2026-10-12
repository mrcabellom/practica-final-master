# Fuentes de datos

La tienda online de Kivora deja cada día una carpeta en `data/inbox/` con el
nombre del día (`data/inbox/2026-09-01/`). Cada carpeta trae los registros
nuevos o modificados de ese día, no una foto completa.

Todas las marcas de tiempo vienen en **UTC**, en formato ISO 8601 con `Z`
(`2026-09-01T22:10:00Z`). Los importes usan punto decimal.

`data/inbox/` es lo que envía la tienda y **no se modifica nunca**: los
problemas del origen se resuelven en el pipeline.

## `orders.csv`

| Campo | Descripción |
| --- | --- |
| `order_id` | Identificador del pedido |
| `customer_id` | Cliente |
| `created_at` | Momento en que se hizo el pedido (UTC) |
| `updated_at` | Momento de la última modificación del pedido (UTC) |
| `status` | `confirmed` o `cancelled` |
| `currency` | Moneda del pedido (ISO 4217) |
| `total_amount` | Importe total, en la moneda del pedido |

Cuando un pedido cambia, la tienda lo vuelve a enviar el día del cambio, con
el mismo `order_id` y un `updated_at` posterior.

## `customers.csv`

| Campo | Descripción |
| --- | --- |
| `customer_id` | Identificador del cliente |
| `name` | Nombre |
| `country` | País (ISO 3166-1 alfa-2). Puede venir vacío |
| `signup_date` | Fecha de alta |

Trae las altas y las modificaciones del día.

## `payments.csv`

| Campo | Descripción |
| --- | --- |
| `payment_id` | Identificador del pago |
| `order_id` | Pedido al que corresponde |
| `paid_at` | Momento del intento de pago (UTC) |
| `method` | `card`, `paypal` o `bizum` |
| `status` | `captured` (cobrado) o `failed` |
| `amount` | Importe del pago, en la moneda del pedido |

Un pedido puede tener más de un pago.

## `data/reference/fx_rates.csv`

Tabla fija de tipos de cambio a euros.

| Campo | Descripción |
| --- | --- |
| `currency` | Moneda (ISO 4217) |
| `rate_to_eur` | Euros por unidad de la moneda: `importe_eur = importe × rate_to_eur` |
