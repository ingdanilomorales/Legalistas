# Decisiones y puntos pendientes

## Decisiones adoptadas

- La aplicación será local y no tendrá login.
- La persistencia será exclusivamente mediante CSV.
- No se usarán APIs externas ni base de datos.
- La meta mensual será de $4.000.000.
- En planes con cuotas, el pie inicial será el 30% y se considerará pagado al crear el plan. En modalidad sin cuotas, se registrará el 100% del servicio como pago inicial.
- Las cuotas posteriores se distribuirán según la cantidad seleccionada, sin monto mínimo.
- Los vencimientos se calcularán para el día 30 de cada mes.

## Puntos que deben cerrarse antes de programar

### Meses sin día 30

Febrero no tiene día 30. Se recomienda usar el último día del mes como vencimiento efectivo para evitar fechas imposibles. La decisión debe confirmarse antes de implementar.

### Redondeo del pie

Como los montos son pesos enteros, se debe definir cómo redondear el 30% cuando el resultado no sea entero. Recomendación: redondear al peso más cercano y asignar el saldo como diferencia para que el total cierre exactamente. Esta regla solo aplica a planes en cuotas.

### Número de cuotas

La cantidad debe ser un entero positivo. El saldo restante se distribuirá entre las cuotas seleccionadas, permitiendo valores inferiores cuando corresponda.

### Pagos superiores al saldo

Se recomienda bloquear pagos que superen el saldo pendiente, salvo que el usuario confirme una corrección explícita. No se debe ocultar el exceso.

### Alcance contradictorio

La solicitud describe una aplicación para un estudio jurídico, pero también indica no ampliar el alcance más allá de “pasajes, alojamiento, comida y entradas”. Esas categorías no corresponden al dominio Legalistas. Este diseño prioriza el alcance jurídico detallado y no agrega módulos de viajes, alojamiento, alimentación ni entradas. La frase debe aclararse antes de implementar si pretendía referirse a otro proyecto.
