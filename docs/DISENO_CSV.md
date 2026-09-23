# Diseño de archivos CSV

Todos los archivos usarán UTF-8, encabezados fijos y fechas `YYYY-MM-DD`. Los montos se guardarán como enteros en pesos chilenos.

## `data/clientes.csv`

| Campo | Tipo conceptual | Descripción |
|---|---|---|
| `cliente_id` | texto | Identificador único estable. |
| `nombre_completo` | texto | Nombre del cliente. |
| `materia` | texto | `familia`, `laboral`, `asesoria`, `mediacion` u `otro`. |
| `monto_total` | entero | Precio total del servicio. |
| `paga_en_cuotas` | booleano | `si` o `no`. |
| `cantidad_cuotas` | entero | Cantidad de cuotas posteriores al pie. |
| `fecha_primera_cuota` | fecha | Fecha base para comenzar el plan. |
| `fecha_creacion` | fecha | Fecha de creación de la ficha. |
| `estado` | texto | `activo`, `finalizado` o `anulado`. |

## `data/cuotas.csv`

| Campo | Tipo conceptual | Descripción |
|---|---|---|
| `cuota_id` | texto | Identificador único de la cuota. |
| `cliente_id` | texto | Relación con `clientes.csv`. |
| `numero_cuota` | entero | `0` para pie; desde `1` para cuotas posteriores. |
| `tipo` | texto | `pie` o `mensual`. |
| `monto_programado` | entero | Valor esperado de la cuota. |
| `fecha_vencimiento` | fecha | Día 30 del mes correspondiente. |
| `mes_referencia` | texto | Mes `YYYY-MM` al que pertenece. |

El estado no se guarda como dato definitivo: se calcula usando pagos existentes y la fecha actual.

## `data/pagos.csv`

| Campo | Tipo conceptual | Descripción |
|---|---|---|
| `pago_id` | texto | Identificador único del movimiento. |
| `cliente_id` | texto | Relación con el cliente. |
| `cuota_id` | texto | Relación con la cuota pagada. |
| `fecha_pago` | fecha | Día en que se recibió el dinero. |
| `monto_pagado` | entero | Monto recibido. |
| `boleta_generada` | booleano | `si` o `no`. |
| `observacion` | texto | Nota opcional. |

## Reglas de integridad

- No reutilizar identificadores.
- No eliminar pagos históricos para corregir una operación; registrar una corrección documentada si fuese necesario.
- Verificar que `cliente_id` y `cuota_id` existan antes de guardar un pago.
- Crear archivos y encabezados si no existen.
- Escribir mediante archivo temporal y reemplazo controlado cuando se reescriba un CSV.
- Realizar copias de respaldo de la carpeta `data`.
