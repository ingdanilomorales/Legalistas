# Plan de implementación de Legalistas

## 1. Objetivo

Diseñar una aplicación web local para el estudio jurídico **Legalistas**, sin autenticación, que permita administrar fichas de clientes, planes de cuotas, pagos y boletas, además de entregar información mensual de cobranza e ingresos.

Este documento funciona como referencia del diseño y de la implementación inicial. Las funciones principales ya están desarrolladas y quedan pendientes las mejoras indicadas en las decisiones técnicas.

## 2. Alcance funcional

### 2.1 Ficha de cliente

Cada cliente deberá registrar:

- Nombre completo.
- Materia o tipo de causa:
  - Familia.
  - Laboral.
  - Asesoría.
  - Mediación.
  - Otro.
- Monto total del servicio.
- Si pagará en cuotas: sí o no.
- Cantidad de cuotas, cuando corresponda.
- Fecha de ingreso del cliente.
- Fecha de la primera cuota.
- Si se generó boleta por el pago inicial, pie o pago único.
- Estado general de la ficha.

La ficha debe conservar la información necesaria para reconstruir el plan de pago y consultar la situación del cliente.

Desde la ficha se podrá editar la información del cliente y eliminar la ficha. La eliminación será en cascada para sus cuotas y pagos relacionados. Los cambios financieros se bloquearán cuando existan pagos manuales, para proteger el historial.

### 2.2 Reglas de cobro

- En un plan con cuotas, el pie inicial se considera pagado en el momento de crear el plan y corresponde al 30% del monto total.
- En modalidad sin cuotas, el pago inicial corresponde al 100% del monto total y se registra como ingreso del mes.
- Al crear la ficha se debe indicar si se generó boleta por ese pago inicial.
- En un plan con cuotas, el saldo restante corresponde al 70% del monto total.
- Si existen cuotas, el saldo restante se distribuirá según la cantidad de cuotas seleccionada.
- La fecha de la primera cuota debe quedar registrada.
- Las cuotas vencen el día 30 de su mes correspondiente.
- Para meses que no tengan día 30, se deberá definir en la implementación si se utiliza el último día del mes o si se mantiene la fecha de vencimiento como regla administrativa. Esta decisión debe quedar documentada antes de programar.

### 2.3 Registro de pagos

Desde la ficha del cliente se deberá poder registrar cada pago con:

- Cliente relacionado.
- Cuota relacionada.
- Fecha del pago.
- Monto pagado.
- Si se generó boleta: sí o no.
- Observación opcional.

El registro deberá permitir distinguir entre cuotas pagadas, pendientes, parcialmente pagadas y vencidas.

### 2.4 Búsqueda

La interfaz deberá permitir buscar y filtrar clientes por:

- Nombre del cliente.
- Tipo de causa o materia.

Los filtros deben poder usarse juntos y mostrar resultados que permitan abrir la ficha correspondiente.

### 2.5 Informe mensual

El informe general deberá permitir seleccionar un mes anterior, actual o futuro y mostrar todos los clientes con:

- Nombre.
- Materia.
- Monto total del servicio.
- Cuota esperada del mes.
- Monto pagado durante el mes.
- Estado de la cuota del mes.
- Fecha de pago, cuando exista.
- Estado de boleta, cuando exista registro de pago.
- Monto atrasado o pendiente.

Criterio visual:

- Verde: cuota pagada completamente.
- Rojo: cuota vencida o monto pendiente atrasado.
- Estado neutral: cuota aún no vencida o cliente sin cuota programada para el mes.

El informe debe incluir una fecha de corte basada en la fecha actual del computador.

### 2.6 Resumen de la pantalla principal

La pantalla principal deberá mostrar:

- Ingresos efectivamente pagados en el mes en curso.
- Meta mensual fija de $4.000.000.
- Monto faltante para alcanzar la meta, sin mostrar valores negativos como deuda de meta.
- Monto proyectado del mes, considerando las cuotas que deberían pagarse.
- Diferencia entre lo proyectado y la meta.
- Cantidad de cuotas pagadas, pendientes y vencidas del mes.

Se deberá distinguir claramente entre dinero cobrado y dinero proyectado. Un pago registrado debe sumarse a los ingresos del mes según su fecha de pago, no según la fecha de vencimiento de la cuota.

Los clientes con modalidad de pago único se contabilizan directamente como ingresos del mes. No deben aumentar la proyección ni los contadores de cuotas pagadas, pendientes o vencidas del resumen principal.

En clientes con plan de cuotas, el pie inicial también se suma a los ingresos reales del mes, pero no se considera una cuota mensual. La proyección y los contadores del resumen solo deben incluir las cuotas posteriores al pie.

El pago del pie debe registrarse con la fecha de ingreso de la causa. Por lo tanto, un cliente ingresado en un mes anterior no aporta su pie al ingreso del mes actual; solo se consideran los pagos efectivamente registrados durante el mes en curso y la cuota mensual que corresponda a ese período.

Las cuotas mensuales vencidas de períodos anteriores que mantengan saldo pendiente se arrastran al resumen del mes actual como cuotas atrasadas. Se acumula su saldo pendiente y no se vuelven a sumar como proyección del mes actual ni como una cuota nueva.

Debajo del estado general se mostrará un listado de clientes morosos, agrupado por cliente, con su materia, cantidad de cuotas vencidas y total atrasado. Los pies y pagos únicos quedan fuera de este listado.

## 3. Propuesta de almacenamiento CSV

Los CSV serán la fuente de persistencia local. Se recomienda usar archivos separados para no mezclar entidades con movimientos históricos.

### 3.1 Clientes

Archivo previsto: `data/clientes.csv`

Campos conceptuales:

- Identificador único del cliente.
- Nombre completo.
- Materia.
- Monto total.
- Modalidad de pago.
- Cantidad de cuotas.
- Fecha de primera cuota.
- Fecha de creación.
- Estado de la ficha.

### 3.2 Cuotas

Archivo previsto: `data/cuotas.csv`

Campos conceptuales:

- Identificador único de cuota.
- Identificador de cliente.
- Número de cuota.
- Tipo de cuota: pie o cuota mensual.
- Monto programado.
- Fecha de vencimiento.
- Mes de referencia.
- Estado calculado o registrado.

La información derivada de la fecha actual debe calcularse al consultar, para evitar estados obsoletos guardados en CSV.

### 3.3 Pagos

Archivo previsto: `data/pagos.csv`

Campos conceptuales:

- Identificador único del pago.
- Identificador de cliente.
- Identificador de cuota.
- Fecha de pago.
- Monto pagado.
- Boleta generada.
- Observación.

### 3.4 Reglas del almacenamiento

- Usar codificación UTF-8.
- Mantener una fila de encabezados estable.
- No borrar pagos históricos al modificar una ficha.
- Usar identificadores únicos, no el nombre del cliente, para relacionar archivos.
- Validar montos y fechas antes de guardar.
- Crear automáticamente los CSV faltantes con sus encabezados al iniciar la aplicación.
- Documentar el formato monetario: guardar montos como números enteros en pesos chilenos, sin separadores ni símbolo `$`.
- Considerar escritura segura para evitar perder el archivo completo durante una actualización.

## 4. Pantallas previstas

1. **Inicio / resumen**: indicadores del mes, meta, ingresos, proyección y alertas.
2. **Clientes**: listado, buscador por nombre y filtro por materia.
3. **Nuevo cliente**: formulario de ficha y configuración de pago.
4. **Ficha del cliente**: datos del servicio, edición, eliminación, calendario de cuotas, pagos y acción para registrar un pago.
5. **Informe mensual**: selector de período, tabla del mes seleccionado con estados y colores, e impresión del resultado.

## 5. Validaciones principales

- Nombre completo obligatorio.
- Materia obligatoria y limitada a las opciones definidas.
- Monto total mayor que cero.
- Fecha de ingreso obligatoria y válida.
- Fecha de primera cuota obligatoria y válida solo cuando el cliente paga en cuotas.
- En planes con cuotas, el pie debe calcularse como 30% del total; sin cuotas, el pago debe ser el 100% del total.
- La cantidad de cuotas debe ser un entero positivo.
- La fecha de primera cuota debe ser válida.
- Un pago no debe asociarse a una cuota inexistente.
- Un pago no debería superar el saldo pendiente sin advertencia explícita.
- El monto pagado debe ser mayor que cero.
- La opción de boleta debe ser obligatoria: sí o no.

## 6. Orden recomendado de desarrollo

1. Definir y documentar reglas de negocio pendientes, especialmente meses sin día 30 y redondeo de porcentajes.
2. Crear la estructura de datos CSV y la capa de lectura/escritura.
3. Implementar validaciones de clientes y generación del plan de cuotas.
4. Implementar el alta y listado de clientes.
5. Implementar la ficha individual y registro de pagos.
6. Implementar estados de vencimiento usando la fecha actual.
7. Implementar buscador y filtro por materia.
8. Implementar informe mensual.
9. Implementar resumen de ingresos y proyección.
10. Aplicar estilos Bootstrap, mensajes de validación y diseño adaptable.
11. Ejecutar pruebas funcionales y probar persistencia al reiniciar la aplicación.
12. Documentar cómo iniciar la aplicación localmente y cómo respaldar los CSV.

## 7. Criterios de aceptación

- La aplicación puede iniciarse localmente sin login ni servicios externos obligatorios.
- Un usuario puede crear una ficha completa y verla después de reiniciar la aplicación.
- El pago inicial se calcula automáticamente: 30% para planes en cuotas y 100% para modalidad sin cuotas.
- Las cuotas se generan distribuyendo el saldo restante entre la cantidad seleccionada por el usuario.
- Un pago puede registrarse con su estado de boleta.
- Una ficha puede editarse desde su vista de detalle.
- Una ficha puede eliminarse junto con sus cuotas y pagos relacionados, mediante confirmación.
- El pago inicial puede registrarse con boleta generada o no generada, tanto en planes con cuotas como en pagos únicos.
- Las cuotas mensuales impagas de meses anteriores aparecen acumuladas en el indicador de cuotas atrasadas del resumen.
- El usuario puede consultar e imprimir informes de meses anteriores, actuales y futuros.
- El estado de vencimiento cambia correctamente al avanzar la fecha del sistema.
- El buscador funciona por nombre y materia.
- El informe del mes distingue visualmente pagos completos y atrasos.
- El resumen separa ingresos reales, monto faltante y proyección.
- Los datos permanecen en archivos CSV legibles y respaldables.

## 8. Fuera de alcance inicial

- Login, usuarios y permisos.
- Integración con sistemas tributarios o emisión electrónica real de boletas.
- Envío automático de correos o mensajes.
- Base de datos SQL.
- Hospedaje en internet.
- Gestión contable completa.

## 9. Arquitectura técnica

La aplicación seguirá una arquitectura simple por capas para mantener separadas la interfaz, las reglas de negocio y la persistencia.

### 9.1 Capas

1. **Presentación**: plantillas HTML renderizadas por Flask y componentes Bootstrap.
2. **Rutas Flask**: reciben solicitudes, validan la entrada básica, llaman a los servicios y seleccionan la respuesta.
3. **Servicios de negocio**: calculan pie, cuotas, pagos, vencimientos, informe y resumen mensual.
4. **Repositorios CSV**: leen y escriben los archivos locales sin decidir reglas de negocio.
5. **Datos**: archivos CSV de clientes, cuotas y pagos.

Las plantillas no deben leer CSV ni realizar cálculos de cuotas. Las rutas no deben contener la lógica completa de negocio.

### 9.2 Estructura técnica prevista

```text
solemne 2 final/
├── PLAN_IMPLEMENTACION.md
├── ESTRUCTURA_CARPETAS.md
├── requirements.txt
├── run.py
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── services.py
│   ├── repositories.py
│   ├── domain.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── inicio.html
│   │   ├── clientes.html
│   │   ├── cliente_form.html
│   │   ├── cliente_detalle.html
│   │   └── informe_mensual.html
│   └── static/
│       ├── css/
│       └── js/
├── data/
├── docs/
└── tests/
```

### 9.3 Responsabilidad de cada archivo previsto

- `run.py`: punto de entrada para iniciar la aplicación local.
- `app/__init__.py`: crea y configura Flask, registra rutas y prepara los CSV.
- `app/routes.py`: define inicio, clientes, ficha, pagos e informe mensual.
- `app/services.py`: concentra validaciones, cálculos y estados de negocio.
- `app/repositories.py`: encapsula lectura, creación y escritura segura de CSV.
- `app/domain.py`: representa internamente clientes, cuotas, pagos y resúmenes.
- `app/templates/base.html`: estructura común de navegación y Bootstrap.
- `app/templates/inicio.html`: resumen de ingresos, meta y proyección.
- `app/templates/clientes.html`: listado, buscador y filtro por materia.
- `app/templates/cliente_form.html`: formulario de alta de cliente.
- `app/templates/cliente_detalle.html`: ficha, cuotas y registro de pagos.
- `app/templates/informe_mensual.html`: informe del mes con estados y colores.
- `app/static/`: estilos o comportamiento visual complementario.
- `data/`: persistencia local mediante CSV.
- `docs/`: reglas, decisiones y manual técnico.
- `tests/`: pruebas de reglas, persistencia y flujos principales.

## 10. Flujo formulario → Flask → CSV → resultado

### 10.1 Alta de cliente

1. El usuario completa nombre, monto, modalidad de pago, cantidad de cuotas, fecha inicial y materia.
2. Flask recibe y valida campos obligatorios, tipos, fechas y montos.
3. El servicio calcula el pago inicial: 30% y saldo restante para planes en cuotas; 100% para modalidad sin cuotas.
4. Si corresponde, distribuye el saldo según la cantidad de cuotas seleccionada.
5. El servicio genera las fechas de vencimiento del día 30.
6. El repositorio agrega el cliente a `clientes.csv` y las cuotas a `cuotas.csv`.
7. Flask redirige a la ficha creada mostrando un mensaje de resultado.

### 10.2 Registro de pago

1. El usuario selecciona una cuota desde la ficha del cliente.
2. Ingresa fecha, monto, boleta generada sí/no y observación opcional.
3. Flask valida que cliente y cuota existan.
4. El servicio valida el monto y calcula el saldo posterior.
5. El repositorio agrega el movimiento a `pagos.csv`, conservando el historial.
6. La ficha se vuelve a consultar y muestra el estado actualizado.

### 10.3 Informe y resumen

1. El servicio lee clientes, cuotas y pagos.
2. Agrupa pagos por cuota y por mes de pago.
3. Compara la fecha actual con el vencimiento de cada cuota.
4. Clasifica las cuotas y calcula saldos atrasados.
5. Suma los pagos del mes para obtener ingresos reales.
6. Suma las cuotas esperadas del mes para obtener la proyección.
7. La plantilla muestra resultados en verde para pagos completos y rojo para atrasos.

## 11. Funciones generales necesarias del backend

### Servicios de negocio

- Validar y normalizar la ficha de cliente.
- Calcular el pago inicial según modalidad: 30% más saldo restante en cuotas, o 100% sin cuotas.
- Generar el calendario de cuotas.
- Resolver el vencimiento del día 30.
- Calcular pagos acumulados por cuota.
- Determinar si una cuota está pagada, parcial, pendiente, vencida o no aplica.
- Registrar y validar pagos.
- Filtrar clientes por nombre y materia.
- Construir el informe del mes en curso.
- Calcular ingresos reales, monto faltante y monto proyectado.

### Repositorios CSV

- Crear archivos faltantes con encabezados.
- Leer clientes, cuotas y pagos.
- Agregar clientes, cuotas y pagos.
- Validar relaciones entre identificadores.
- Preservar historial y realizar escrituras controladas.

## 12. Reglas técnicas y decisiones pendientes

- Usar UTF-8 y fechas en formato `YYYY-MM-DD`.
- Guardar montos como enteros en pesos chilenos, sin símbolo ni separadores.
- Usar identificadores únicos para relacionar archivos.
- Calcular estados de vencimiento en cada consulta, no como estados permanentes guardados en CSV.
- Para febrero, se recomienda usar el último día del mes como vencimiento efectivo, ya que no existe día 30.
- Si el 30% produce decimales, se recomienda redondear al peso más cercano y ajustar el saldo para que el total cierre.
- El pago se suma a ingresos según su fecha de pago, no según la fecha de vencimiento.
- La meta mensual es $4.000.000 y el faltante no debe mostrarse como valor negativo.

La aplicación permanecerá sin login, sin base de datos, sin APIs externas y sin módulos ajenos al control de clientes, cuotas, pagos, boletas e informes del estudio jurídico.
