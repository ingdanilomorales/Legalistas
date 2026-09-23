# Especificación de la aplicación

## 1. Propósito

Aplicación web local para registrar clientes de un estudio jurídico y consultar el resumen de sus pagos. El backend se ejecuta con Python y Flask; la interfaz utiliza HTML y Bootstrap. No requiere login, base de datos ni servicios externos.

## 2. Acciones del usuario

El usuario puede:

- Crear una ficha de cliente con nombre, materia, fecha de ingreso, monto total y modalidad de pago.
- Definir un pago único o un plan con pago inicial y cuotas posteriores.
- Consultar el listado de clientes y buscar por nombre o materia.
- Abrir el detalle de un cliente y revisar cuotas, pagos, saldos y estados.
- Registrar pagos asociados a una cuota, indicando fecha, monto, boleta y observación.
- Editar datos de una ficha y eliminarla junto con sus cuotas y pagos.
- Consultar un informe mensual, incluyendo meses anteriores, actuales o futuros, e imprimirlo.
- Revisar el resumen de ingresos y cuotas atrasadas desde la pantalla inicial.

## 3. Datos administrados

El sistema maneja:

- **Clientes:** identificador, nombre completo, materia, monto total, modalidad de pago, cantidad y fecha de cuotas, fecha de ingreso y estado.
- **Cuotas:** identificador, cliente asociado, número, tipo, monto programado, vencimiento y mes de referencia.
- **Pagos:** identificador, cliente y cuota asociados, fecha, monto, emisión de boleta y observación.

## 4. Persistencia en CSV

La información se guarda en la carpeta `data/` mediante tres archivos CSV:

- `clientes.csv`: datos de las fichas de clientes.
- `cuotas.csv`: planes y vencimientos de pago.
- `pagos.csv`: pagos realizados y sus comprobantes u observaciones.

Al crear o modificar información, el sistema escribe las filas correspondientes en los CSV. Al mostrar listados, fichas o informes, lee los CSV y relaciona los registros mediante sus identificadores. No se utiliza una base de datos.

## 5. Reglas básicas

- El nombre del cliente, la materia, la fecha de ingreso y el monto total son obligatorios.
- El monto total debe ser mayor que cero.
- Un pago único genera una cuota por el total.
- Un plan en cuotas requiere al menos una cuota posterior y su fecha inicial; el pago inicial corresponde al 30% del total.
- El saldo restante se distribuye entre las cuotas programadas.
- Un pago debe ser mayor que cero y no puede superar el saldo pendiente de la cuota.
- Una cuota puede quedar pendiente, con abono parcial, pagada o atrasada según sus pagos y vencimiento.
- Si existen pagos manuales, la edición no debe alterar el plan financiero ni su historial.
- La eliminación de un cliente elimina también sus cuotas y pagos asociados.
- La aplicación funciona localmente mediante `python run.py`.

## 6. Criterios mínimos de cumplimiento

La aplicación cumple la especificación cuando:

1. Se inicia localmente con Flask y permite acceder a la interfaz desde el navegador.
2. Permite crear, consultar, editar y eliminar fichas de clientes.
3. Permite registrar pagos y visualizar cuotas, saldos y estados.
4. Permite consultar el resumen de pagos y un informe mensual.
5. Los datos permanecen disponibles después de reiniciar la aplicación porque se guardan en los tres archivos CSV.
6. Se respetan las validaciones de montos, fechas, cuotas y pagos.
7. No requiere login, base de datos ni servicios externos.

## 7. Normas mínimas de ciberseguridad

Por tratarse de una aplicación local que maneja datos de clientes y pagos, se deben cumplir como mínimo las siguientes normas:

- La aplicación debe escuchar únicamente en `127.0.0.1`; no debe exponerse directamente a Internet ni a redes externas.
- El modo debug de Flask solo debe utilizarse durante el desarrollo local. No debe usarse para una instalación de uso real.
- Los archivos CSV deben permanecer dentro de la carpeta `data/`. Las rutas y nombres de archivo no deben provenir directamente de datos ingresados por el usuario.
- Los formularios deben validar campos obligatorios, fechas, números, montos positivos, identificadores y relaciones entre clientes, cuotas y pagos antes de guardar información.
- Los datos mostrados en HTML deben escaparse correctamente para evitar inyección de código, especialmente en nombres, observaciones y materias.
- Las operaciones que modifican o eliminan datos deben aceptar únicamente métodos HTTP apropiados y validar el registro objetivo antes de ejecutarse.
- Los errores no deben mostrar rutas internas, trazas, secretos ni información técnica innecesaria al usuario.
- Los archivos CSV contienen información sensible: deben limitarse al usuario local autorizado y no deben publicarse, subirse a repositorios ni incluirse en registros de depuración.
- Deben realizarse copias de respaldo periódicas de `data/` y comprobar que puedan restaurarse.
- Las dependencias de Python deben mantenerse identificadas en `requirements.txt` y actualizarse ante vulnerabilidades conocidas.
- No deben almacenarse contraseñas, claves, tokens ni secretos en el código fuente ni en los archivos CSV.

### Criterios mínimos de seguridad

La aplicación cumple el mínimo de seguridad cuando:

1. Solo es accesible localmente y no expone el servidor de desarrollo a una red externa.
2. Valida entradas y relaciones antes de leer o modificar los CSV.
3. Escapa contenido dinámico al renderizar las páginas.
4. Protege los CSV y cuenta con respaldos recuperables.
5. No revela información sensible mediante errores, código fuente o archivos de configuración.
