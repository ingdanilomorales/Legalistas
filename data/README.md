# Contexto de `data`

Esta carpeta almacenará los datos persistentes de la aplicación mediante archivos CSV.

## Archivos previstos

- `clientes.csv`: fichas de clientes.
- `cuotas.csv`: plan de cuotas generado para cada cliente.
- `pagos.csv`: historial de pagos y estado de boleta.

## Reglas de operación

- Usar UTF-8 y encabezados definidos.
- Guardar los montos en pesos chilenos como números enteros, sin símbolo ni separadores.
- Relacionar registros por identificadores únicos.
- Conservar el historial de pagos.
- Respaldar esta carpeta antes de realizar cambios importantes.
- No subir datos reales a un repositorio público.

Los estados de vencimiento no deben depender de una copia fija guardada en CSV; deben derivarse comparando la fecha actual con el vencimiento de cada cuota.
