# Contexto de `app`

Esta carpeta contiene el núcleo de la aplicación Flask de Legalistas.

El diseño técnico detallado está en [docs/ARQUITECTURA_TECNICA.md](../docs/ARQUITECTURA_TECNICA.md) y el catálogo de responsabilidades está en [docs/BACKEND.md](../docs/BACKEND.md).

## Responsabilidades

- Configurar la aplicación Flask local.
- Recibir solicitudes de las pantallas.
- Validar datos de clientes, cuotas y pagos.
- Calcular pie, saldo, vencimientos, atrasos, ingresos y proyecciones.
- Coordinar la lectura y escritura de los archivos CSV.
- Entregar a las plantillas la información lista para mostrar.

## Límites

No debe contener datos de clientes reales dentro del código. No debe implementar login en el alcance inicial. La presentación visual deberá mantenerse en `templates/` y `static/`.

## Reglas de diseño

- Mantener separadas las rutas, las reglas de negocio y el acceso a CSV.
- Usar identificadores para relacionar clientes, cuotas y pagos.
- Calcular los estados relativos a la fecha actual en el momento de consultar.
- Mantener los montos como enteros en pesos chilenos internamente.
