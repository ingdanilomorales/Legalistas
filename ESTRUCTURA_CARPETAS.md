# Estructura de carpetas

La siguiente estructura corresponde a la aplicación Flask local de Legalistas. Los archivos de aplicación y las plantillas principales ya están implementados; los CSV se crean automáticamente al iniciar.

```text
solemne 2 final/
├── PLAN_IMPLEMENTACION.md
├── ESTRUCTURA_CARPETAS.md
├── documentacion/
│   ├── README.md
│   ├── LOGICA_NEGOCIO.md
│   └── ARQUITECTURA_PROYECTO.md
├── requirements.txt                 # Dependencias previstas, sin código de negocio
├── run.py                            # Punto de entrada local previsto
├── app/
│   ├── README.md
│   ├── __init__.py                   # Fábrica/configuración de Flask
│   ├── routes.py                     # Rutas y recepción de formularios
│   ├── services.py                   # Reglas de negocio y cálculos
│   ├── repositories.py               # Lectura y escritura de CSV
│   ├── domain.py                     # Entidades y estructuras internas
│   ├── templates/
│   │   ├── README.md
│   │   ├── base.html
│   │   ├── inicio.html
│   │   ├── clientes.html
│   │   ├── cliente_form.html
│   │   ├── cliente_detalle.html
│   │   └── informe_mensual.html
│   └── static/
│       ├── README.md
│       ├── css/
│       └── js/
├── data/
│   └── README.md
├── docs/
│   ├── README.md
│   ├── ARQUITECTURA_TECNICA.md
│   ├── FLUJO_FORMULARIO_CSV.md
│   ├── DISENO_CSV.md
│   ├── BACKEND.md
│   └── DECISIONES.md
└── tests/
    └── README.md
```

## Responsabilidad de cada carpeta

- `app/`: núcleo de la aplicación Flask y lógica de negocio.
- `app/routes.py`: endpoints HTML y procesamiento inicial de formularios.
- `app/services.py`: reglas de pie, cuotas, vencimientos, informes y resumen.
- `app/repositories.py`: persistencia CSV, sin cálculos de presentación.
- `app/domain.py`: entidades y valores internos de clientes, cuotas y pagos.
- `app/templates/`: futuras vistas HTML renderizadas por Flask y componentes Bootstrap.
- `app/static/`: futuros recursos de presentación, como hojas de estilo, JavaScript e imágenes.
- `data/`: archivos CSV locales con clientes, cuotas y pagos.
- `docs/`: decisiones de negocio, reglas de cálculo, manual de uso y respaldo.
- `tests/`: pruebas de validaciones, cuotas, pagos, vencimientos, informes y resumen mensual.

## Principio de separación

La lógica de cálculo y persistencia debe permanecer fuera de las plantillas HTML. Las plantillas solo deberían presentar la información preparada por la aplicación. Los CSV deben tratarse como datos, no como archivos de configuración ni como plantillas de interfaz.
