# Flujo formulario → Flask → CSV → resultado

## Crear cliente y plan de pago

1. El usuario abre el formulario de nuevo cliente.
2. Ingresa nombre, monto total, modalidad, cantidad de cuotas, fecha inicial y materia.
3. Flask recibe el formulario y valida campos obligatorios, tipos y rangos.
4. El servicio calcula el pago inicial: 30% si existe un plan en cuotas, o 100% si es pago único.
5. Si corresponde, calcula el saldo del 70% y lo distribuye entre la cantidad de cuotas seleccionada.
6. El servicio genera las cuotas con sus fechas de vencimiento el día 30 de cada mes.
7. El repositorio agrega una fila a `clientes.csv` y las cuotas correspondientes a `cuotas.csv`.
8. El resultado redirige a la ficha del cliente y muestra un mensaje de creación exitosa.

## Registrar un pago

1. El usuario abre la ficha del cliente.
2. Selecciona una cuota pendiente o parcialmente pagada.
3. Ingresa fecha, monto, estado de boleta y observación opcional.
4. Flask valida que cliente y cuota existan.
5. El servicio valida que el monto sea positivo y calcula el saldo resultante.
6. El repositorio agrega el movimiento a `pagos.csv`; no se sobrescriben pagos anteriores.
7. La ficha se vuelve a consultar para mostrar estado actualizado y saldo pendiente.

## Consultar clientes

1. El usuario escribe un nombre y/o selecciona una materia.
2. Flask normaliza los filtros.
3. El servicio solicita los clientes al repositorio y aplica los filtros.
4. La respuesta renderiza la tabla con enlaces a las fichas.

## Generar informe mensual

1. El usuario abre el informe y selecciona un mes anterior, actual o futuro.
2. El servicio obtiene clientes, cuotas y pagos.
3. Agrupa pagos por cuota y mes de pago.
4. Compara la fecha actual con el vencimiento del día 30.
5. Clasifica cada cuota como pagada, pendiente, parcialmente pagada, vencida o no aplicable.
6. Calcula saldo atrasado y prepara filas para la tabla.
7. La plantilla muestra pagos completos en verde y atrasos en rojo, además de texto explícito.
8. El usuario puede imprimir el período consultado mediante la función de impresión del navegador.

## Calcular resumen de inicio

1. El servicio toma el primer y último día del mes actual.
2. Suma pagos cuya fecha de pago pertenece a ese mes.
3. Calcula el faltante frente a la meta de $4.000.000.
4. Suma las cuotas programadas del mes para obtener la proyección.
5. La plantilla muestra ingresos reales, meta, faltante, proyección y conteos de estado.
