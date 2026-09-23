# Legalistas

Aplicación web local para administrar clientes, cuotas, pagos, boletas e informes mensuales de un estudio jurídico.

La explicación central de lógica y arquitectura está en [documentacion/README.md](documentacion/README.md).

## Ejecución local

1. Instalar Python 3.10 o superior.
2. Crear un entorno virtual.
3. Instalar las dependencias de `requirements.txt`.
4. Ejecutar `python run.py`.
5. Abrir `http://127.0.0.1:5000`.

La aplicación crea `data/clientes.csv`, `data/cuotas.csv` y `data/pagos.csv` automáticamente. No requiere login, base de datos ni servicios externos para guardar la información.

## Funcionalidades implementadas

- Alta de clientes con pago inicial del 30% en cuotas o del 100% sin cuotas.
- Distribución del saldo en cuotas, sin monto mínimo.
- Registro de pagos y estado de boleta.
- Registro de boleta para el pie inicial o pago único al crear un cliente.
- Edición y eliminación de fichas con protección del historial de pagos.
- Búsqueda por nombre y materia.
- Estados de cuotas según fecha actual y vencimiento del día 30.
- Arrastre de saldos pendientes de cuotas anteriores como atrasos del mes actual.
- Listado de clientes morosos con cantidad de cuotas y total atrasado.
- Informe mensual y resumen de ingresos frente a la meta de $4.000.000.
- Consulta e impresión de informes de meses anteriores, actuales y futuros.