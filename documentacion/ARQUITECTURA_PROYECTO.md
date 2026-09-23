# Arquitectura del proyecto

## 1. Vista general

```text
Navegador
   |
   v
Plantillas HTML + Bootstrap
   |
   v
Rutas Flask
   |
   v
Servicios de negocio
   |
   v
Repositorio CSV
   |
   v
clientes.csv, cuotas.csv, pagos.csv
```

La aplicación es local y monousuario. No tiene login, API externa ni base de datos.

## 2. Capas

### Presentación

Ubicación: `app/templates/` y `app/static/`.

- `base.html`: navegación, Bootstrap y mensajes.
- `inicio.html`: resumen financiero y clientes morosos.
- `clientes.html`: búsqueda y listado.
- `cliente_form.html`: alta de clientes.
- `cliente_editar.html`: modificación de fichas.
- `cliente_detalle.html`: cuotas, pagos, edición y eliminación.
- `informe_mensual.html`: informe seleccionable e imprimible.
- `app.css`: colores, layout, estados y estilos de impresión.

Las plantillas presentan datos; no deben leer CSV ni calcular cuotas.

### Rutas Flask

Ubicación: `app/routes.py`.

Responsabilidades:

- Recibir formularios.
- Convertir fechas y montos.
- Llamar a los servicios.
- Mostrar mensajes de éxito o error.
- Renderizar plantillas o redirigir.

Rutas principales:

- `GET /`: resumen principal.
- `GET /clientes`: listado y filtros.
- `GET|POST /clientes/nuevo`: alta.
- `GET /clientes/<id>`: ficha.
- `GET|POST /clientes/<id>/editar`: edición.
- `POST /clientes/<id>/eliminar`: eliminación.
- `POST /clientes/<id>/pagos`: registro de pagos.
- `GET /informe?month=YYYY-MM`: informe por período.

### Servicios de negocio

Ubicación: `app/services.py`.

Responsabilidades:

- Calcular pago único o pie.
- Generar cuotas.
- Calcular vencimientos.
- Determinar estados.
- Registrar pagos.
- Editar y eliminar clientes.
- Construir informes.
- Calcular ingresos, proyección, atrasos y morosidad.

La lógica se prueba con `tests/test_services.py` sin necesidad de levantar el servidor.

### Repositorio CSV

Ubicación: `app/repositories.py`.

Responsabilidades:

- Crear archivos y encabezados.
- Leer filas.
- Agregar registros.
- Reemplazar archivos mediante un temporal.
- Mantener la estructura de cada CSV.

No decide si una cuota está vencida y no calcula la meta mensual.

## 3. Persistencia

### `data/clientes.csv`

Contiene la ficha del cliente y su fecha de ingreso.

### `data/cuotas.csv`

Contiene el pago único, pie y cuotas mensuales programadas.

- `number=0`: pago inicial o pie.
- `number>0`: cuota mensual.
- `kind=unico`: pago completo sin cuotas.
- `kind=pie`: pago inicial del plan.
- `kind=mensual`: cuota posterior.

### `data/pagos.csv`

Contiene cada pago real, fecha de pago, monto, boleta y observación.

## 4. Flujo de alta

1. El usuario abre el formulario.
2. Selecciona modalidad y boleta del pago inicial.
3. La fecha de primera cuota se exige solo con modalidad en cuotas.
4. Flask valida y normaliza los datos.
5. El servicio calcula pago inicial y cuotas.
6. El repositorio guarda cliente, cuotas y pago inicial.
7. Flask redirige a la ficha.

## 5. Flujo de resumen

1. Se leen clientes, cuotas y pagos.
2. Se suman pagos por fecha de pago para ingresos del mes.
3. Se identifican cuotas mensuales del período actual.
4. Se buscan cuotas mensuales vencidas de períodos anteriores.
5. Se agrupan atrasos por cliente.
6. La plantilla presenta métricas y tabla de morosos.

## 6. Flujo de informe

1. El usuario selecciona `YYYY-MM`.
2. Flask convierte el mes en una fecha de referencia.
3. El servicio carga cuotas cuyo mes de referencia coincide.
4. Los pagos se filtran por fecha de pago del período.
5. La fecha actual se usa para determinar estados.
6. Bootstrap presenta colores de pagado, pendiente y atrasado.
7. `window.print()` permite imprimir el informe.

## 7. Pruebas

Las pruebas cubren:

- Pago inicial del 30%.
- Pago único del 100%.
- Fechas históricas del pie.
- Cuotas sin monto mínimo.
- Pagos y boletas.
- Edición y eliminación.
- Informes pasados y futuros.
- Arrastre de morosidad.
- Listado agrupado de clientes morosos.
