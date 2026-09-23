# Contexto de `app/templates`

Esta carpeta contiene las vistas HTML de Flask.

## Vistas

- Inicio con resumen mensual.
- Listado y búsqueda de clientes.
- Formulario de ingreso de cliente.
- Ficha individual del cliente.
- Edición y eliminación de ficha individual.
- Formulario de registro de pagos.
- Informe general del mes.

## Criterios de interfaz

- Usar Bootstrap para grillas, formularios, tablas, alertas y estados visuales.
- Mostrar estados pagados en verde y atrasos en rojo, acompañando el color con texto para accesibilidad.
- Mantener visibles el monto programado, el monto pagado y el saldo pendiente.
- Incluir mensajes claros cuando una validación impida guardar información.
- La interfaz debe funcionar en una pantalla local de escritorio y conservar legibilidad en pantallas pequeñas.

No se debe colocar aquí lógica de cálculo de cuotas o lectura directa de CSV.
