# Resumen de la problemática

## Problemática

El estudio jurídico necesita una forma simple y centralizada de registrar clientes, organizar sus planes de pago y consultar el estado de cuotas y pagos. Sin una herramienta dedicada, esta información puede quedar dispersa, dificultando el seguimiento de saldos pendientes, pagos atrasados, boletas e ingresos mensuales.

## Solución propuesta

`Legalistas` es una aplicación web local desarrollada con Python y Flask. Permite crear y administrar fichas de clientes, generar pagos únicos o planes de cuotas, registrar abonos, consultar saldos y estados, y obtener informes mensuales.

La información se conserva en archivos CSV (`clientes.csv`, `cuotas.csv` y `pagos.csv`), por lo que el proyecto no requiere una base de datos ni servicios externos. La aplicación está pensada para ejecutarse localmente mediante `python run.py`.

## Alcance

- Registro, búsqueda, edición y eliminación de clientes.
- Programación de pagos únicos o en cuotas.
- Registro de pagos, boletas y observaciones.
- Visualización de saldos, cuotas atrasadas e ingresos.
- Consulta e impresión de informes mensuales.
- Documentación funcional, técnica y de ciberseguridad mínima.

## Ejecución

1. Instalar Python 3.10 o superior.
2. Instalar dependencias con `pip install -r requirements.txt`.
3. Ejecutar `python run.py`.
4. Abrir `http://127.0.0.1:5000` en el navegador.
