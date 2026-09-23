# Documentación del proyecto Legalistas

Esta carpeta explica la lógica funcional y la arquitectura técnica de la aplicación Legalistas.

## Documentos

- `LOGICA_NEGOCIO.md`: reglas de clientes, pagos, cuotas, vencimientos, atrasos e ingresos.
- `ARQUITECTURA_PROYECTO.md`: componentes, responsabilidades y flujo de información.

## Alcance

Legalistas es una aplicación web local para un estudio jurídico. Está construida con Flask, plantillas HTML, Bootstrap y archivos CSV.

La aplicación no utiliza login, base de datos ni APIs externas.

## Inicio rápido

Desde la raíz del proyecto:

1. Instalar las dependencias de `requirements.txt`.
2. Ejecutar `python run.py`.
3. Abrir `http://127.0.0.1:5000`.

Los archivos CSV se crean automáticamente dentro de `data/`.
