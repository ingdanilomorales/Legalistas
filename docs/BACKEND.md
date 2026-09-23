# Diseño del backend

## Archivos previstos y responsabilidades

### `run.py`

Punto de entrada local. Iniciará la aplicación Flask configurada para ejecutarse en el computador del estudio.

### `app/__init__.py`

Construirá la aplicación, definirá configuración básica, registrará rutas y verificará que los CSV necesarios estén disponibles.

### `app/routes.py`

Contendrá las rutas HTTP y el flujo de formularios:

- Inicio y resumen mensual.
- Listado y búsqueda de clientes.
- Creación de clientes.
- Detalle de cliente.
- Registro de pagos.
- Informe mensual.

Solo coordinará entrada, servicio y respuesta.

### `app/domain.py`

Definirá las estructuras internas para cliente, cuota, pago y resumen mensual. No debe abrir archivos ni conocer detalles de HTML.

### `app/services.py`

Funciones generales previstas:

- Validar y normalizar ficha de cliente.
- Calcular el pago inicial según modalidad: 30% con cuotas o 100% sin cuotas.
- Validar cantidad de cuotas y distribuir el saldo restante.
- Generar calendario de cuotas.
- Resolver vencimiento del día 30.
- Calcular pagos acumulados por cuota.
- Determinar estado de cuota.
- Registrar y validar pagos.
- Filtrar clientes por nombre y materia.
- Construir informe del mes.
- Calcular ingresos reales, faltante y proyección.

### `app/repositories.py`

Funciones generales previstas:

- Leer filas de clientes.
- Leer filas de cuotas.
- Leer filas de pagos.
- Agregar cliente.
- Agregar cuotas.
- Agregar pago.
- Crear CSV y encabezados iniciales.
- Validar relaciones entre archivos.

Este archivo no debe decidir si una cuota está vencida ni calcular la meta.

## Estados calculados

- `pagada`: pagos acumulados iguales o superiores al monto programado.
- `parcial`: existe pago, pero queda saldo.
- `pendiente`: no existe pago y aún no vence.
- `vencida`: no está completamente pagada y la fecha actual supera el vencimiento.
- `no_aplicable`: el cliente no tiene cuota para el período consultado.

## Criterio monetario

Los cálculos internos deben operar con enteros en pesos para evitar errores de redondeo. El formato con `$`, puntos y separadores se aplica únicamente al presentar valores en HTML.
