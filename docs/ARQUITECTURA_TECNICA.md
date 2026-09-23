# Arquitectura técnica de Legalistas

## Alcance

Diseño para una aplicación web local, monousuario y sin login, construida con Flask, HTML, Bootstrap y archivos CSV. En esta etapa se documentan decisiones y contratos; no se implementa el código completo.

## Capas

### Presentación

- Plantillas HTML renderizadas por Flask.
- Bootstrap para formularios, tablas, alertas, colores de estado y diseño adaptable.
- Formularios HTML con validación básica de navegador, siempre respaldada por validación del servidor.

### Rutas Flask

Reciben solicitudes HTTP, extraen parámetros, llaman a los servicios y seleccionan la plantilla o redirección correspondiente. No deben calcular cuotas ni leer CSV directamente.

### Servicios de negocio

Centralizan las reglas de clientes, pie, cuotas, pagos, vencimientos, informe mensual y resumen de ingresos. Esta capa debe poder probarse sin depender de una petición HTTP.

### Persistencia CSV

Los repositorios leen y escriben `clientes.csv`, `cuotas.csv` y `pagos.csv`. La persistencia usa identificadores estables y conserva el historial de pagos.

## Flujo general

```text
Navegador
   |
   v
Plantilla HTML + formulario Bootstrap
   |
   v
Ruta Flask
   |
   v
Servicio de negocio
   |
   v
Repositorio CSV
   |
   v
Resultado calculado
   |
   v
Plantilla HTML con mensaje o informe
```

## Decisiones técnicas

- Aplicación local iniciada desde un punto de entrada único.
- Sin base de datos, APIs externas, login ni integración tributaria.
- Fechas almacenadas en formato ISO `YYYY-MM-DD`.
- Montos almacenados como enteros en pesos chilenos, sin `$` ni separadores.
- Estados de vencimiento calculados con la fecha actual al consultar, no almacenados como una verdad permanente.
- El nombre del cliente sirve para buscar, pero las relaciones internas usan identificadores.

## Seguridad y consistencia mínima

Aunque no exista login, se deben validar todos los datos recibidos del formulario, escapar los valores mostrados en HTML y evitar que el usuario pueda elegir identificadores inexistentes. Las escrituras CSV deben preservar encabezados y datos existentes.
