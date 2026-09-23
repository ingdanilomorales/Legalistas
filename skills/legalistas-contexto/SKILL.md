---
name: legalistas-contexto
description: Carga y aplica el contexto funcional de la aplicación Legalistas al desarrollar, revisar o documentar este proyecto.
---

# Legalistas Contexto

Usa esta skill cuando una tarea se relacione con la aplicación web local del estudio jurídico: su backend Flask, interfaz HTML/Bootstrap, clientes, cuotas, pagos, informes o persistencia en CSV.

## Fuente de verdad

Antes de planificar o ejecutar una tarea del proyecto, lee completamente [documentacion/spec.md](../../documentacion/spec.md). Trata ese archivo como la especificación funcional vigente.

## Contexto que debes respetar

- Mantén Flask como backend, HTML/Bootstrap como frontend y CSV como mecanismo de persistencia.
- Conserva la ejecución local mediante `python run.py`.
- No introduzcas login, base de datos, servicios externos ni funcionalidades fuera del alcance de la especificación.
- Respeta las acciones, datos, validaciones, reglas de cuotas y pagos, e informes descritos en `documentacion/spec.md`.
- Si una solicitud contradice la especificación o requiere una funcionalidad nueva, señálalo antes de ampliar el alcance.
- Cuando la tarea sea solo documental, no modifiques código ni archivos de datos.

## Uso de la referencia

Consulta nuevamente `documentacion/spec.md` si la tarea requiere verificar criterios de cumplimiento, reglas de negocio, nombres de archivos CSV o límites funcionales. No dupliques su contenido en esta skill: el documento es la referencia mantenida del proyecto.
