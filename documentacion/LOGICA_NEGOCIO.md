# Lógica de negocio

## 1. Cliente y ficha

Cada ficha contiene:

- Nombre completo.
- Materia: familia, laboral, asesoría, mediación u otro.
- Monto total del servicio.
- Fecha de ingreso de la causa.
- Modalidad de pago: pago único o plan en cuotas.
- Cantidad de cuotas posteriores al pie.
- Fecha de la primera cuota, solo cuando existe un plan en cuotas.
- Estado de boleta del pago inicial.

La ficha puede editarse y eliminarse. Al eliminarla, también se eliminan sus cuotas y pagos relacionados.

## 2. Pago inicial

### Cliente con cuotas

- El pie inicial corresponde al 30% del monto total.
- El pie se registra automáticamente como pagado.
- La fecha del pie coincide con la fecha de ingreso de la causa.
- El 70% restante se distribuye entre las cuotas posteriores.
- La boleta del pie se registra como `si` o `no`.

### Cliente sin cuotas

- El pago inicial corresponde al 100% del monto total.
- Se registra como pago único, no como pie ni como cuota mensual.
- La fecha del pago coincide con la fecha de ingreso de la causa.
- La boleta se registra como `si` o `no`.
- El monto se suma a los ingresos del mes correspondiente a la fecha de ingreso.
- No participa en proyección ni en contadores de cuotas.

## 3. Cuotas mensuales

- Cada cuota posterior al pie recibe un número desde `1`.
- Las cuotas vencen el día `30` de su mes.
- Para febrero se utiliza el último día disponible del mes.
- Los montos se guardan como enteros en pesos chilenos.
- Si el saldo no se divide exactamente, los pesos restantes se distribuyen entre las primeras cuotas.
- Actualmente no existe un monto mínimo de cuota.

## 4. Estados

El estado se calcula al consultar los datos:

- **Pagada**: pagos acumulados iguales o superiores al monto programado.
- **Abono parcial**: existe un pago, pero todavía queda saldo y la cuota no está vencida.
- **Pendiente**: no existen pagos y la fecha de vencimiento aún no pasa.
- **Atrasada**: queda saldo pendiente y la fecha actual supera el vencimiento.

Los estados no se guardan como una verdad permanente en los CSV, porque dependen de la fecha actual.

## 5. Ingresos del resumen principal

El ingreso del mes suma todos los pagos cuya `fecha_pago` pertenece al mes consultado:

- Pagos únicos.
- Pies pagados durante ese mes.
- Pagos de cuotas realizados durante ese mes.

Un pago de un mes anterior no se vuelve a sumar en meses posteriores.

## 6. Proyección y contadores

La proyección solo considera cuotas mensuales posteriores al pie que correspondan al mes actual.

El pie inicial no cuenta como cuota. Los pagos únicos tampoco cuentan como cuotas.

Los contadores del resumen son:

- Pagadas: cuotas mensuales del período completamente pagadas.
- Pendientes: cuotas mensuales del período sin pago o con abono parcial que aún no vencen.
- Atrasadas: cuotas mensuales vencidas, incluyendo saldos pendientes de períodos anteriores.

## 7. Morosidad acumulada

Una cuota mensual impaga de un mes anterior se arrastra al resumen actual como atraso.

Para cada cliente moroso se acumula:

- Cantidad de cuotas mensuales vencidas.
- Saldo pendiente total.
- Nombre y materia.

Los pies y pagos únicos se excluyen de la morosidad acumulada.

## 8. Informes

El informe permite seleccionar un mes anterior, actual o futuro.

- El período seleccionado determina qué cuotas programadas se muestran.
- La fecha actual determina si una cuota está vencida.
- Los pagos mostrados corresponden al período seleccionado.
- El informe se puede imprimir con la función de impresión del navegador.
