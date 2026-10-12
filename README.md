![Desarrollo asistido por agentes. Máster Big Data y Data Engineering](docs/images/banner-readme.png)

# Kivora · pipeline de ventas

> **Práctica final del módulo Desarrollo asistido por agentes.** El enunciado
> está en [`assignment.md`](assignment.md): léelo antes de empezar.

**Kivora** es una tienda online de moda y complementos con clientes en
España y en el resto de Europa, Reino Unido y Estados Unidos. Cada día, la
tienda deja en `data/inbox/` una carpeta con los pedidos, clientes y pagos
del día.

El **equipo de datos** transforma esas carpetas en tablas de negocio. Hoy
genera dos:

- `daily_sales`: ventas por día y país, para el cuadro de mando de
  Dirección Comercial. Su contrato está en
  [`docs/data-contracts/daily_sales.md`](docs/data-contracts/daily_sales.md).
- `top_customers`: los diez clientes que más han comprado.

El equipo trabaja con agentes de código. La herramienta principal es
**Claude Code**.

## Estado actual

El pipeline funciona con los datos que hay en `data/inbox/` (del 1 al 3 de
septiembre de 2026). Los tickets abiertos están en `docs/tickets/`:

- [KIV-100](docs/tickets/KIV-100.md): incorporación al pipeline.

La tienda envía nuevas entregas de datos con su ticket. Para simularlo:

```bash
uv run python tasks.py deliver 1   # días 4 a 7 y el ticket KIV-101
uv run python tasks.py deliver 2   # días 8 a 10 y el ticket KIV-102
```

Cada entrega se recibe una sola vez y en orden. Los ficheros nuevos de
`data/inbox/` y `docs/tickets/` se incorporan al repositorio con un commit.

## Preparar el entorno

Se necesitan [uv](https://docs.astral.sh/uv/), Git y Claude Code. `uv`
descarga Python 3.12 si no está instalado.

```bash
uv sync
uv run python tasks.py setup
uv run python tasks.py run
uv run python tasks.py test
```

En Windows, macOS y Linux las órdenes son las mismas. Si prefieres activar
el entorno virtual (`.venv\Scripts\Activate.ps1` en PowerShell,
`source .venv/bin/activate` en macOS y Linux), puedes omitir `uv run`.

## Tareas

| Orden | Qué hace |
| --- | --- |
| `python tasks.py setup` | Comprueba la versión de Python y las dependencias |
| `python tasks.py run` | Ejecuta el pipeline sobre `data/inbox/` y escribe `output/` |
| `python tasks.py test` | Ejecuta los tests |
| `python tasks.py check` | Comprobaciones básicas sobre `output/` |
| `python tasks.py deliver N` | Recibe la entrega `N` de la tienda |
| `python tasks.py reset` | Borra `output/` |

## Interfaz de ejecución

El equipo de Plataforma lanza el pipeline así, y esta interfaz **no se
puede cambiar**:

```bash
uv run python -m kivora --inbox data/inbox --reference data/reference --out output
```

Las tres opciones tienen esos valores por defecto.

## Estructura

```text
kivora-pipeline/
├── kivora/                 código del pipeline
│   ├── __main__.py         punto de entrada (python -m kivora)
│   ├── ingest.py           carga las fuentes en SQLite sin limpiarlas
│   ├── pipeline.py         orquesta la carga, el SQL y la exportación
│   └── check.py            comprobaciones básicas de output/
├── sql/                    transformaciones en SQL (SQLite)
├── tests/                  tests (pytest)
├── data/
│   ├── inbox/              entregas de la tienda: no se modifican nunca
│   └── reference/          tablas de referencia (tipos de cambio)
├── deliveries/             entregas futuras, para python tasks.py deliver
├── docs/
│   ├── sources.md          formato de cada fuente
│   ├── data-contracts/     qué garantiza cada tabla de salida
│   └── tickets/            peticiones de negocio
├── assignment.md           enunciado de la práctica
└── tasks.py                lanzador de tareas
```

Solo se usa la biblioteca estándar de Python (SQLite incluido), más
`tzdata` para las zonas horarias en Windows y `pytest` para los tests.
