# Práctica final · Desarrollo y evolución de un pipeline de datos con agentes de código

**Módulo:** Desarrollo asistido por agentes
**Profesor:** Manuel Rodrigo Cabello Malagón
**Tiempo estimado:** 10 horas para el núcleo (las ampliaciones opcionales, aparte)
**Entrega:** [fecha], 23:59

---

## 1. Contexto

Kivora es una tienda online de moda. Su equipo de datos mantiene un pipeline
en Python y SQL que procesa cada día los pedidos, clientes y pagos de la
tienda y genera tablas de negocio.

Acabas de incorporarte al equipo. Durante la práctica recibirás tres tickets,
en orden: entender el pipeline (KIV-100), incorporar las devoluciones y una
nueva tabla de métricas para Finanzas (KIV-101) y adaptarte a un cambio en
el formato de las devoluciones (KIV-102). Los datos llegan en entregas
sucesivas, como en un proyecto real.

El trabajo se hace con un agente de código, preferentemente **Claude Code**.
No se evalúa solo si el pipeline funciona, sino **cómo has trabajado con el
agente**: qué contexto le diste, qué decidiste tú y qué delegaste, cómo
comprobaste lo que hacía y cómo dejaste el proyecto preparado para el
siguiente que llegue.

## 2. Material de partida

El punto de partida es el repositorio plantilla
[`mrcabellom/practica-final-master`](https://github.com/mrcabellom/practica-final-master).
Tu copia se llamará `kivora-pipeline` (apartado 7) y contiene:

- datos de ejemplo de los tres primeros días en `data/inbox/`
- un pipeline básico en Python y SQLite (`kivora/`, `sql/`)
- tests parciales (`tests/`)
- documentación de las fuentes, un contrato de datos y el primer ticket
  (`docs/`)
- un `CLAUDE.md` heredado
- las entregas futuras de la tienda en `deliveries/`, que se reciben con
  `uv run python tasks.py deliver N`.

El `README.md` del repositorio explica cómo preparar el entorno. Funciona
igual en Windows, macOS y Linux: todas las órdenes se lanzan con `uv run`, que
usa el Python del proyecto. No des nada por supuesto: ni la documentación ni
los tests están necesariamente bien.

## 3. Reglas del juego

Estas reglas no son negociables. Incumplirlas impide evaluar parte de la
práctica o penaliza.

1. **La interfaz de ejecución no cambia.** El pipeline se lanza con
   `uv run python -m kivora --inbox <dir> --reference <dir> --out <dir>` y
   deja en `--out` los ficheros que pide el ticket KIV-101
   (`daily_customer_metrics.csv`, `rejected.csv` y `quality_report.json`).
   Puedes reorganizar todo lo demás.
2. **Tu pipeline se ejecutará con datos que no conoces.** Tienen el mismo
   formato y el mismo tipo de problemas que los del repositorio, pero otros
   valores y otras fechas. Un pipeline ajustado a los datos de ejemplo
   fallará.
3. **`data/inbox/` y `deliveries/` no se modifican nunca.** Los problemas de
   los datos se resuelven en el pipeline. Las entregas se reciben con
   `uv run python tasks.py deliver N` y se guardan en un commit propio.
4. **El historial de Git es parte de la entrega.** Haz commits reales y
   frecuentes. Los que haga el agente conservan su línea
   `Co-Authored-By`. No reescribas la historia.
5. **Un tag por fase.** Al cerrar cada fase, crea el tag `phase-N` sobre el
   último commit de esa fase. Los tags marcan qué había en cada momento y se
   comprueban.
6. **Los tickets son deliberadamente incompletos.** Detectar lo que no dicen
   y decidirlo con criterio es parte de la práctica. Las decisiones ambiguas
   no tienen una única respuesta válida: se evalúa que estén detectadas,
   justificadas, documentadas y que el código haga lo que dice la
   documentación.
7. **Rutas fijas.** Los entregables van en las rutas indicadas en cada fase:
   la corrección los busca ahí.

## 4. Desarrollo: seis fases

Las fases van en orden y cada una se apoya en la anterior. Para cada una se
indica la situación, qué tienes que hacer, qué entregas y cuándo está
cerrada.

> **Ampliación con OpenSpec.** Las fases 1, 2, 4 y 5 se pueden hacer con
> OpenSpec en lugar de con documentos Markdown. Es opcional y sube nota
> (apartado 5). Cada fase indica, en un recuadro como este, qué cambia si
> eliges esa ruta.

### Fase 1 · Entender antes de tocar (KIV-100)

**Situación.** Es tu primer día. El ticket `docs/tickets/KIV-100.md` te pide
entender el pipeline antes de que llegue el trabajo nuevo.

**Qué hacer.**

- Usa el agente para analizar el repositorio completo: README, fuentes,
  contrato, código, SQL y tests. Trabaja en modo plan: en esta fase no se
  modifica código.
- Responde a las preguntas del ticket con **hechos comprobados**: cada
  afirmación, con su archivo y línea, o con el comando que la demuestra y su
  resultado. No aceptes lo que diga el agente sin verificarlo.
- Crea o completa las instrucciones del proyecto (`CLAUDE.md` o
  equivalente): qué es el proyecto, cómo se ejecuta y se prueba de verdad,
  qué no se puede tocar y cuándo un trabajo está terminado. Corto,
  verificado y útil para una sesión nueva.

**Entregables.**

- `docs/analysis.md`: análisis del pipeline, con evidencias.
- `CLAUDE.md`: instrucciones del proyecto.
- Respuesta en la sección **Respuesta** de `docs/tickets/KIV-100.md`.

> **Con OpenSpec:** ejecuta `openspec init --tools claude --language es`,
> completa `openspec/config.yaml` con el contexto del proyecto y documenta
> en una spec base (`openspec/specs/daily-sales/spec.md`) cómo funciona
> **hoy** `daily_sales`, defectos incluidos.

**Cierre.** Sin cambios en `kivora/`, `sql/` ni `tests/`. Tag `phase-1`.

### Fase 2 · Especificar y planificar (KIV-101)

**Situación.** Ejecuta `uv run python tasks.py deliver 1`: llegan cuatro
días nuevos con devoluciones y el ticket KIV-101 de Finanzas. Haz un commit
solo con lo recibido.

**Qué hacer.**

- **Especificación.** Con ayuda del agente, escribe qué hay que construir
  antes de decidir cómo. Incluye:
  - objetivo y fuera de alcance
  - requisitos numerados
  - escenarios de aceptación con **datos y cifras reales** de `data/inbox/`
    (este pedido, este cliente, este día, este importe)
  - una sección **Aclaraciones**: cada ambigüedad que hayas detectado en
    el ticket y en los datos, las opciones, la decisión y el motivo. Pide al
    agente que te ayude a encontrarlas, pero las decisiones son tuyas.
- **Plan.** Pide al agente un plan de implementación a partir de la
  especificación, en tareas que digan cómo se verifica cada una. Haz commit
  del borrador **tal como te lo dio**. Después revísalo críticamente,
  corrígelo y haz commit de la versión revisada con una sección
  **Revisión del plan**: qué cambiaste y por qué.

**Entregables.**

- `docs/specs/KIV-101/spec.md`
- `docs/specs/KIV-101/plan.md` (al menos dos commits: borrador y revisión)

> **Con OpenSpec:** `/opsx:propose add-customer-metrics` sustituye a
> `docs/specs/KIV-101/`. Las aclaraciones van en `design.md`, los
> escenarios en los deltas de `specs/` y el plan en `tasks.md`. Haz commit
> del change tal como lo generó el agente y, tras revisarlo (con
> `/opsx:update` o a mano), de la versión revisada. Debe pasar
> `openspec validate add-customer-metrics --strict`. La tabla de lo que
> cambiaste en la revisión va en la memoria.

**Cierre.** Sin cambios en `kivora/`, `sql/` ni `tests/`. Tag `phase-2`.

### Fase 3 · Preparar al agente

**Situación.** Antes de implementar, prepara el entorno de trabajo del
agente para este proyecto concreto. Lo que has visto en las fases 1 y 2
(riesgos, tareas repetitivas, comprobaciones que se olvidan) es lo que tiene
que guiar la configuración.

**Qué hacer.**

- **Permisos** en `.claude/settings.json` (compartido con el equipo): qué
  puede hacer el agente sin preguntar, qué tiene que preguntar y qué tiene
  prohibido.
- **Al menos un mecanismo de extensión** (skill, hook, subagente, servidor
  MCP o comando), elegido para una necesidad concreta de este proyecto. Se
  ejecuta y se prueba en la corrección: un hook que no funciona no cuenta.
  Los skills y comandos que instala OpenSpec no cuentan como propios.
- En la memoria (`docs/report.md`), una sección **Configuración del agente**
  con:
  - una **tabla de protecciones**: riesgo, mecanismo que lo cubre, tipo
    (instrucción, permiso, hook o aislamiento) y por qué ese tipo y no otro
  - para cada mecanismo de extensión: qué problema resuelve, por qué ese
    mecanismo y qué aporta frente a pedirle lo mismo directamente al agente.

**Entregables.** `.claude/` (y `.mcp.json` si usas MCP) y la sección de la
memoria.

**Cierre.** Tag `phase-3`.

### Fase 4 · Implementar con un bucle de feedback (KIV-101)

**Situación.** Toca construir lo especificado, con el agente, siguiendo el
plan revisado.

**Qué hacer.**

- **Oráculo propio.** Añade a `tasks.py` una tarea `acceptance` que ejecute
  el pipeline sobre `data/inbox/` y compruebe los escenarios de tu
  especificación, con código de salida 0 solo si todos pasan. Úsala como
  señal de parada del agente (por ejemplo, como condición de `/goal`, en un
  hook `Stop` o en un skill de validación).
- **Implementación** de `daily_customer_metrics`, `rejected.csv` y
  `quality_report.json` según el ticket y tu especificación.
- **Tests** que comprueben, como mínimo:
  1. la eliminación correcta de duplicados
  2. el tratamiento de valores nulos
  3. las devoluciones parciales
  4. varias devoluciones sobre un mismo pedido
  5. las devoluciones sin pedido asociado
  6. el cálculo del importe neto
  7. la ausencia de duplicidades después de los joins.

  Un test que pasaría con el código roto no cuenta. Si un test existente
  contradice el contrato, no lo adaptes en silencio: decide y justifícalo.
- **Controles de calidad** (al menos dos) en `quality_report.json`, por
  ejemplo `net_amount = gross_amount - refunded_amount` y que lo devuelto no
  supere lo comprado. El pipeline informa de los registros que los
  incumplen.
- **Registra cada vuelta del ciclo** con el agente en la memoria: qué
  feedback le diste, qué cambió y qué criterio usaste para decidir que
  estaba terminado.
- **Responde a Finanzas** en `docs/tickets/KIV-101.md`, en lenguaje de
  negocio.

> **Con OpenSpec:** implementa con `/opsx:apply`, con commits que citen las
> tareas, y archiva el change con `/opsx:archive` antes del tag.

**Cierre.** `tests` y `acceptance` en verde. Tag `phase-4`.

### Fase 5 · Gestionar un cambio (KIV-102)

**Situación.** Ejecuta `uv run python tasks.py deliver 2` y haz commit de lo
recibido. Plataforma avisa de que `refunds.json` ha cambiado de formato.

**Qué hacer.**

- **Primero el impacto, después el código.** Con el agente, y antes de
  modificar nada, analiza qué partes del pipeline, de los tests y de la
  documentación se ven afectadas y qué pasa hoy con los datos nuevos. Haz
  commit del análisis antes del primer commit de código: se comprueba en el
  historial.
- Especificación del cambio (solo lo que cambia) y plan.
- Tests que fallen con el código anterior y pasen con el nuevo.
- Implementación sin regresiones: todo lo de la fase 4 sigue en verde.
- Responde al ticket en `docs/tickets/KIV-102.md`.

**Entregables.** `docs/specs/KIV-102/impact.md`, `spec.md` y `plan.md`.

> **Con OpenSpec:** `/opsx:propose support-refunds-v2`, con el análisis de
> impacto en la sección `Impact` de `proposal.md` y en su propio commit
> antes del código. Después, `/opsx:apply` y `/opsx:archive` antes del tag.

**Cierre.** Tag `phase-5`.

### Fase 6 · Revisar y cerrar

**Qué hacer.**

- **Revisión** del trabajo completo con, al menos, un revisor distinto de la
  sesión que escribió el código (un subagente, `/code-review`, otra
  herramienta). En `docs/review.md`, una tabla con cada hallazgo, quién lo
  encontró, su gravedad, tu decisión (aceptado o rechazado) y el motivo.
  Aplica los cambios que aceptes.
- **README actualizado**: qué produce el pipeline, cómo se ejecuta, cómo se
  prueba y cómo se trabaja en el proyecto con el agente.
- **Memoria completa** (apartado 6).
- **Sesiones**: al menos tres sesiones exportadas con `/export`, sin editar,
  en `docs/sessions/`, de las fases 2, 4 y 5. Revisa antes que no contengan
  secretos ni datos personales.

> **Con OpenSpec:** al terminar, `openspec validate --all --strict` pasa y
> no queda ningún change sin archivar.

**Cierre.** Tag `phase-6`: es la entrega.

## 5. Ampliaciones opcionales

Suman hasta 1 punto sobre 10 (sin superar la nota máxima):

| Ampliación | Puntos |
| --- | ---: |
| Especificación con **OpenSpec** en las fases 1, 2, 4 y 5: ciclo `propose → apply → archive` completo y validado | hasta 0,4 |
| Un segundo mecanismo de extensión distinto, con su propia justificación | 0,2 |
| Sesiones en paralelo con worktrees en alguna fase, integradas sin conflictos | 0,2 |
| Integración continua en GitHub Actions que ejecute tests y aceptación | 0,2 |
| Un servidor MCP propio útil para el proyecto | 0,2 |
| `AGENTS.md` para trabajar también con otras herramientas | 0,1 |
| Un fichero de estado que permita retomar el trabajo tras `/clear` | 0,1 |

Cada ampliación tiene que estar justificada en la memoria.

## 6. Memoria (`docs/report.md`)

Documento en Markdown con, al menos, estas secciones:

1. **Decisiones con el agente.** Las principales: quién propuso qué y por
   qué se decidió así.
2. **Configuración del agente.** La tabla de protecciones y la
   justificación de cada mecanismo (fase 3).
3. **Ciclo de iteración.** Cómo estructuraste el trabajo con el agente: qué
   feedback le pasaste en cada vuelta (salida de tests, del oráculo,
   revisiones…), cuántas vueltas hubo y qué criterio usaste para decidir que
   la solución estaba lista.
4. **Trazabilidad.** Una tabla que relacione cada requisito con sus
   escenarios y con el test o criterio de aceptación que lo comprueba.
5. **Cambio de esquema.** Cómo analizaste el impacto y qué aprendiste.
6. **Revisión.** Resumen de `docs/review.md`.
7. **Qué harías distinto.**

## 7. Entrega

**Con cuenta de GitHub (recomendado):**

1. Crea tu repositorio a partir de la plantilla con **Use this template**,
   como **privado** y con el nombre `kivora-pipeline`. Después, clónalo en
   tu equipo.
2. Añade al profesor como colaborador (*Settings → Collaborators*):
   [usuario de GitHub].
3. Sube la rama `main` y los tags: `git push origin main --tags`.
4. Comunica la URL del repositorio por [canal].

**Sin cuenta de GitHub:** clona la plantilla en una carpeta llamada
`kivora-pipeline`:

```bash
git clone https://github.com/mrcabellom/practica-final-master.git kivora-pipeline
```

Trabaja igual en local, con Git, y entrega un zip de la carpeta del
repositorio **con la carpeta oculta `.git`**: ahí están el historial, los
commits del agente y los tags. Sin ella no se puede corregir.
Excluye `.venv` y `output`, que se regeneran.

En Windows (PowerShell), desde la carpeta que contiene el repositorio:

```powershell
tar -a -c -f apellido-nombre.zip --exclude=.venv --exclude=output kivora-pipeline
```

En macOS y Linux:

```bash
zip -r apellido-nombre.zip kivora-pipeline -x "*/.venv/*" "*/output/*"
```

Si tu Linux no tiene `zip`, instálalo con el gestor de paquetes (por
ejemplo, `sudo apt install zip`).

Antes de enviarlo, compruébalo: descomprímelo en otra carpeta y ejecuta
`git log --oneline` y `git tag` dentro. Tienen que aparecer tus commits y
los seis tags. Envía el zip por [canal].

Estructura mínima esperada al final:

```text
CLAUDE.md
README.md
tasks.py                          con la tarea acceptance
.claude/settings.json             y tus mecanismos de extensión
docs/analysis.md
docs/specs/KIV-101/spec.md        (u openspec/, si eliges esa ruta)
docs/specs/KIV-101/plan.md
docs/specs/KIV-102/impact.md
docs/specs/KIV-102/spec.md
docs/specs/KIV-102/plan.md
docs/review.md
docs/report.md
docs/sessions/                    tres sesiones exportadas como mínimo
docs/tickets/KIV-10{0,1,2}.md     con su respuesta
```

## 8. Evaluación

La nota es sobre 10 y tiene dos partes de 5 puntos cada una:

**Parte 1 · Automática (5 puntos).** Un script ejecuta tu pipeline y revisa el
repositorio. Responde a dos preguntas: si tu pipeline resuelve el problema y si hay
evidencias de que lo has hecho como se pide.

| Qué se comprueba | Puntos |
| --- | ---: |
| Resultado del pipeline, con los datos del repositorio y con datos que no conoces | 3 |
| Los tests y `tasks.py acceptance` pasan | 0,5 |
| La especificación y el plan de KIV-101 y KIV-102 están donde se piden | 0,5 |
| El historial lo demuestra: tags en orden, nada de código antes de especificar, plan revisado antes de implementar, impacto antes del código, commits del agente y sesiones exportadas | 0,6 |
| La configuración del agente funciona: permisos válidos y mecanismos que se ejecutan sin errores | 0,4 |

**Parte 2 · Profesor (5 puntos).** El profesor lee tus documentos y sesiones.
Responde a una pregunta: si has usado bien los artefactos.

| Qué se valora | Puntos |
| --- | ---: |
| Análisis del pipeline y `CLAUDE.md` | 0,6 |
| Especificación y plan: aclaraciones, escenarios con datos reales, tareas verificables, revisión del plan y cambio de KIV-102 | 1,6 |
| Mecanismos de extensión justificados y tabla de protecciones | 1 |
| Calidad de los tests: cada caso del enunciado con un test que fallaría con el código roto | 0,8 |
| Memoria: decisiones, ciclo de iteración, trazabilidad, revisión y sesiones | 1 |

**Ampliaciones:** hasta +1 (apartado 5). **Penalizaciones:** modificar los
datos de entrada (−1) o subir secretos al repositorio (−0,5). Cambiar la
interfaz de ejecución impide evaluar el resultado del pipeline.

## 9. Preguntas frecuentes

**¿Puedo usar GitHub Copilot, Cursor u OpenCode?**
Sí, si lo documentas en la memoria y las instrucciones del proyecto sirven
también para esa herramienta. Los mecanismos de extensión se evalúan igual.

**¿Tengo que usar OpenSpec?**
No. Es una ampliación. Si lo usas, sustituye a los documentos de
`docs/specs/` en las fases 2 y 5. El resto de la práctica es igual.

**¿Puedo cambiar la estructura del código o pasar de SQL a Python?**
Sí. Solo son fijas la interfaz de ejecución, los ficheros de salida y las
rutas de los entregables.

**¿Puedo añadir dependencias?**
Sí, con `uv add`. El pipeline tiene que funcionar con `uv sync` seguido de
`uv run python -m kivora`.

**¿Qué hago si el ticket no dice algo?**
Lo que haría un buen profesional: detectarlo, decidir con criterio,
documentarlo en la sección de aclaraciones y probarlo.

**Me he equivocado de tag.**
Puedes moverlo con `git tag -f phase-N` (y, si usas GitHub,
`git push -f origin phase-N`) antes de la entrega. Lo que no se reescribe
son los commits.

**Una fase me ha salido mal.**
Sigue adelante y cuéntalo en la memoria. Un problema bien diagnosticado y
explicado vale más que uno escondido.
