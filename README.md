# db_docs — Sistema de Gestión de Trámites PAS

> Aplicación de escritorio para la gestión, numeración y seguimiento de documentos dentro de **Procedimientos
Administrativos Sancionadores (PAS)**.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![PySide6](https://img.shields.io/badge/PySide6-Qt6-green?logo=qt)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13%2B-blue?logo=postgresql)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## Tabla de Contenidos

- [Descripción](#descripción)
- [Arquitectura](#arquitectura)
- [Flujo del Proceso Sancionador](#flujo-del-proceso-sancionador)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Módulos de la Aplicación](#módulos-de-la-aplicación)
- [Base de Datos](#base-de-datos)
- [Migración de Datos Históricos](#migración-de-datos-históricos)
- [Uso](#uso)
- [Decisiones Técnicas](#decisiones-técnicas)
- [Contribuir](#contribuir)

---

## Descripción

`db_docs` es una aplicación de escritorio desarrollada con **Python + PySide6** y base de datos **PostgreSQL**. Gestiona
el ciclo de vida completo de los Procedimientos Administrativos Sancionadores (PAS) de una entidad regulatoria, desde la
recepción del memorando de solicitud hasta la resolución final y los recursos de impugnación.

Sus funciones principales son:

- Registrar trámites y gestionar la información de proveedores/presuntos responsables.
- Generar y asignar la numeración oficial de cada tipo de documento del proceso.
- Mantener la trazabilidad cronológica completa de documentos por trámite.
- Calcular plazos descontando días no laborables y feriados.
- Buscar y filtrar expedientes con exportación a Excel.
- Registrar impugnaciones y archivar los documentos correspondientes.
- Refrescar los datos en tiempo real mediante notificaciones de PostgreSQL.

---

## Arquitectura

El sistema está dividido en tres capas con responsabilidades bien delimitadas:

```
┌──────────────────────────────────────────────────────────┐
│                    UI  (PySide6 / Qt)                     │
│  Crear Trámite │ Tomar Número │ Consultar │ Impugnación   │
└───────────────────────────┬──────────────────────────────┘
                            │  solo llama servicios, sin SQL
┌───────────────────────────▼──────────────────────────────┐
│              Capa de Servicios  (Python)                  │
│   catalogo_service  │  busqueda_service  │  auditoria     │
└───────────────────────────┬──────────────────────────────┘
                            │  RealDictCursor + pool
┌───────────────────────────▼──────────────────────────────┐
│              Base de Datos  (PostgreSQL)                  │
│   Tablas │ Vistas │ Funciones PL/pgSQL │ Triggers         │
└──────────────────────────────────────────────────────────┘
```

**Principios de diseño:**

- La UI nunca ejecuta SQL directamente; solo consume servicios.
- Toda la lógica de negocio compleja reside en funciones PL/pgSQL.
- Los servicios retornan `dict` (via `RealDictCursor`), accesibles por nombre de columna.
- Un pool de conexiones (`SimpleConnectionPool`, min=1, max=5) gestiona la concurrencia.
- Las notificaciones en tiempo real se reciben en un hilo daemon independiente.

---

## Flujo del Proceso Sancionador

El sistema modela el siguiente ciclo de vida de un trámite PAS:

```
[1] PETICIÓN PAS PENDIENTE
        │
        ├──► [2] REQUIERE ACTUACIÓN PREVIA
        │           │
        │           └──► [3] EN ACTUACIÓN PREVIA
        │                       │
        │                 (¿Prosigue a PAS?)
        │                    Sí ──► continúa
        │                    No ──► RESUELTO (sin sanción)
        │
        └──► [4] EN INSTRUCCIÓN
                    │
                    └──► [5] EN RESOLUCIÓN
                                │
                                └──► [6] RESUELTO
                                           │
                                     (¿Impugnación?)
                                        Sí ──► nuevo ciclo
```

Cada transición queda registrada en `trazabilidad_tramite` con su línea de proceso, permitiendo reconstruir el historial
completo del expediente.

---

## Requisitos Previos

| Herramienta | Versión mínima | Notas                                       |
|-------------|:--------------:|---------------------------------------------|
| Python      |     3.10+      | Requiere f-strings con expresiones          |
| PostgreSQL  |      13+       | La extensión `pg_trgm` debe estar instalada |
| pip         |      22+       |                                             |

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/dany-maxwell/db_docs.git
cd db_docs

# 2. Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt
```

**`requirements.txt`:**

```
PySide6>=6.5.0
psycopg2-binary>=2.9.0
python-dotenv>=1.0.0
openpyxl>=3.1.0
```

---

## Configuración

### Variables de entorno

Crea un archivo `.env` en la raíz del proyecto usando `.env.example` como plantilla:

```bash
cp .env.example .env
```

Edita `.env` con los valores de tu entorno:

```env
DB_NAME=db_docs
DB_USER=user_app
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
```

### Inicialización de la base de datos

```bash
# Crear la base de datos
psql -U postgres -c "CREATE DATABASE db_docs;"

# Crear el usuario de aplicación
psql -U postgres -c "CREATE USER user_app WITH PASSWORD 'tu_contraseña';"

# Aplicar el schema completo (tablas, vistas, funciones, triggers, permisos)
psql -U postgres -d db_docs -f query-database.sql
```

---

## Estructura del Proyecto

```
db_docs/
├── main.py                          # Punto de entrada de la aplicación
├── constants.py                     # Constantes globales (tipos, estados, columnas UI)
├── .env.example                     # Plantilla de variables de entorno
├── requirements.txt                 # Dependencias Python
├── query-database.sql               # Schema completo de PostgreSQL
├── insert_excel_to_db.ipynb         # ETL de migración de datos históricos
│
├── db/
│   ├── connection.py                # Pool de conexiones con rollback automático
│   └── pg_listener.py               # Receptor LISTEN/NOTIFY en hilo daemon
│
├── services/
│   ├── db_helper.py                 # Ejecutor genérico de queries (RealDictCursor)
│   ├── catalogo_service.py          # Consultas de catálogos (proveedores, tipos, docs)
│   ├── busqueda_service.py          # Búsquedas por memo, código y búsqueda avanzada
│   └── auditoria_service.py         # Operaciones de escritura (crear, numerar, archivar)
│
└── ui/
    ├── main_window.py               # Ventana principal con QTabWidget y listeners
    ├── widgets/
    │   └── widgets.py               # Widgets reutilizables (ComboBoxes, formularios)
    └── pages/
        ├── crear_tramite/
        │   ├── ui_crear_tramite.py          # Formulario de nuevo trámite
        │   └── widget_nuevo_proveedor.py    # Subventana para registrar proveedores
        ├── tomar_numero/
        │   ├── base_tab.py                  # Clase base con lógica compartida de numeración
        │   ├── ui_tomar_numero.py           # Contenedor de tabs de numeración
        │   ├── tab_mem.py                   # Aceptar / devolver memorando
        │   ├── tab_ap.py                    # Actuación Previa
        │   ├── tab_iap.py                   # Informe de Actuación Previa
        │   ├── tab_pr.py                    # Providencias (AP / Instrucción / Resolución)
        │   ├── tab_ai.py                    # Acto de Inicio PAS
        │   ├── tab_ij.py                    # Informe Jurídico
        │   ├── tab_d.py                     # Dictamen
        │   ├── tab_rpas.py                  # Resolución PAS
        │   └── tab_de.py                    # Oficios, Memorandos y Respuestas
        ├── consultar/
        │   └── ui_consultar.py              # Búsqueda avanzada y exportación a Excel
        └── impugnacion/
            └── ui_impugnacion.py            # Registro de impugnaciones / apelaciones
```

---

## Módulos de la Aplicación

### Crear Trámite

Registra un nuevo expediente PAS. Permite seleccionar o crear un proveedor (presunto responsable), elegir la unidad
requirente y el servicio controlado, ingresar el asunto, y cargar hasta tres documentos de inicio:

| Documento                 | `tipo_documento_id` | Obligatorio |
|---------------------------|:-------------------:|:-----------:|
| Memorando de Petición PAS |          1          |     Sí      |
| Petición Razonada         |          2          |     No      |
| Informe Técnico           |         15          |     No      |

Al guardar, el sistema invoca `crear_tramite()` en PostgreSQL, que crea el trámite y sus documentos en una única
transacción atómica.

### Tomar Número

Genera la numeración oficial para cada etapa del proceso. Organizado en nueve tabs:

| Tab                  | Documento                                     | `tipo_documento_id` |
|----------------------|-----------------------------------------------|:-------------------:|
| Aceptar Memo         | Procesar / Devolver el memorando              |          —          |
| Actuación Previa     | Número de Actuación Previa                    |          4          |
| Informe AP           | Informe Inicial o Final de Actuación Previa   |          5          |
| Providencias         | Providencia de AP / Instrucción / Resolución  |          7          |
| Acto de Inicio       | Acto de Inicio PAS con infracciones asociadas |          6          |
| Informe Jurídico     | Informe Jurídico PAS                          |         11          |
| Dictamen             | Dictamen                                      |          8          |
| Resolución           | Resolución PAS                                |          9          |
| Oficios / Memorandos | Documentos de notificación y respuesta        |     12, 13, 14      |

Cada tab filtra automáticamente los documentos origen disponibles según el trámite seleccionado. El código se genera en
PostgreSQL mediante `crear_documento()`, garantizando secuencias sin huecos incluso ante cancelaciones.

### Consultar

Búsqueda avanzada sobre la vista `v_busqueda_avanzada` con los siguientes filtros simultáneos:

- Memorando, proveedor, unidad
- Código de documento (búsqueda parcial con `ILIKE`)
- Tipo y subtipo de documento
- Estado del trámite
- Rango de fechas
- Estado de archivado

Los resultados se exportan a Excel en dos formatos:

- **Tabla actual:** exporta exactamente los registros visibles en pantalla, con hoja resumen del trámite si hay un memo
  seleccionado.
- **Reporte completo:** exporta `vista_seguimiento_final` con todos los hitos del proceso, coloreando filas según el
  estado (amarillo = AP, celeste = Instrucción, rojo = Resolución, gris = Resuelto).

### Impugnación

Registra un recurso de apelación contra una resolución. Muestra todos los documentos del trámite seleccionado y permite
elegir el punto de impugnación. Al confirmar, `aplicar_impugnacion()` archiva todos los documentos desde el seleccionado
en adelante e inserta el documento de impugnación (tipo 10) en el trámite.

---

## Base de Datos

### Tablas principales

| Tabla                  | Descripción                                                              |
|------------------------|--------------------------------------------------------------------------|
| `tramite`              | Expediente principal: proveedor, unidad, servicio, estado, asunto        |
| `documento`            | Documentos del trámite con código, tipo, fecha, plazo y fecha de término |
| `proveedor`            | Prestadores de servicios / presuntos responsables                        |
| `tipo_documento`       | Catálogo de tipos de documento                                           |
| `subtipo_documento`    | Subclasificación por tipo                                                |
| `infraccion`           | Catálogo de infracciones imputables                                      |
| `documento_infraccion` | Relación N:M documento ↔ infracción                                      |
| `trazabilidad_tramite` | Línea de tiempo de documentos por trámite y línea de proceso             |
| `plantilla_codigo`     | Formato de código por tipo (tokens reemplazables)                        |
| `secuencia_documento`  | Contador anual por plantilla, con bloqueo `FOR UPDATE`                   |
| `feriados`             | Días no laborables para el cálculo de plazos                             |

### Vistas clave

| Vista                     | Propósito                                                     |
|---------------------------|---------------------------------------------------------------|
| `v_busqueda_avanzada`     | Búsqueda combinada para el módulo Consultar                   |
| `v_info_tramite_por_memo` | Datos del trámite dado el ID de un memorando                  |
| `v_documentos_tramite`    | Lista de documentos de un trámite con estado                  |
| `v_consulta_documentos`   | Documentos con tipo, subtipo e infracciones                   |
| `v_reporte_tramites`      | Pivot de hitos principales del proceso                        |
| `vista_seguimiento_final` | Matriz completa con todos los documentos y fechas por trámite |
| `vista_seguimiento_tipos` | Historial recursivo de documentos por línea de proceso        |

### Funciones PL/pgSQL

| Función                               | Descripción                                                        |
|---------------------------------------|--------------------------------------------------------------------|
| `crear_tramite(...)`                  | Crea el trámite y sus documentos iniciales en una transacción      |
| `crear_documento(...)`                | Genera un documento con código automático o manual                 |
| `generar_codigo_documento(...)`       | Aplica plantilla + secuencia anual para el código oficial          |
| `actualizar_estado_tramite(...)`      | Transiciona el estado del trámite                                  |
| `prosigue_tramite(...)`               | Marca si el trámite procede o no a la fase PAS                     |
| `sumar_dias_laborables(...)`          | Calcula la fecha de término descontando feriados y fines de semana |
| `agregar_infraccion_a_documento(...)` | Asocia una infracción a un documento (idempotente)                 |
| `aplicar_impugnacion(...)`            | Archiva documentos desde un punto e inserta el de impugnación      |
| `nuevo_proveedor(...)`                | Crea un proveedor; el trigger emite `NOTIFY canal_proveedores`     |

### Triggers

| Trigger                     | Tabla       | Evento                                                                             |
|-----------------------------|-------------|------------------------------------------------------------------------------------|
| `trg_nuevo_documento`       | `documento` | `AFTER INSERT` → emite `NOTIFY canal_documentos`                                   |
| `trg_post_insert_documento` | `documento` | `AFTER INSERT` → registra en `trazabilidad_tramite` con lógica de línea de proceso |
| `trg_nuevo_proveedor`       | `proveedor` | `AFTER INSERT` → emite `NOTIFY canal_proveedores`                                  |

La función `fn_registrar_trazabilidad()` asigna la línea de proceso siguiendo esta lógica: si no hay documento padre,
asigna línea 1; si existe un hermano archivado del mismo padre (reintento de corrección), incrementa la línea global del
trámite; de lo contrario, hereda la línea del padre.

### Permisos

El usuario `user_app` tiene permisos de `INSERT`, `SELECT` y `UPDATE` sobre todas las tablas y vistas de negocio, y
`USAGE`/`SELECT` sobre las secuencias. No tiene permisos de `DELETE` ni acceso a funciones administrativas.

---

## Migración de Datos Históricos

El archivo `insert_excel_to_db.ipynb` contiene un ETL de uso único para cargar expedientes históricos desde un archivo
Excel (`eda_prueba.xlsx`). El proceso sigue estos pasos:

1. **Normalización:** elimina tildes, convierte a mayúsculas y colapsa espacios múltiples.
2. **Corrección de typos:** mapea errores tipográficos de fechas presentes en el Excel de origen (p. ej. `amyo → mayo`,
   `octubte → octubre`).
3. **Resolución de claves foráneas:** hace merge de proveedores, unidades y servicios contra la BD para obtener sus IDs.
4. **Carga secuencial:** proveedores → trámites → memorandos → peticiones razonadas → informes técnicos → actuaciones
   previas → actos de inicio → resoluciones → documentos de notificación.

> **Nota:** Configura las credenciales de conexión mediante variables de entorno en el archivo `.env` antes de ejecutar
> el notebook.

---

## Uso

```bash
# 1. Activar el entorno virtual
source .venv/bin/activate      # Linux / macOS
.venv\Scripts\activate         # Windows

# 2. Iniciar la aplicación
python main.py
```

La ventana principal carga las cuatro pestañas. Los combos se actualizan automáticamente cuando otro usuario registra un
nuevo proveedor o documento en la misma base de datos, gracias al mecanismo `LISTEN/NOTIFY`.

---

## Decisiones Técnicas

**Pool de conexiones con rollback automático**
`SimpleConnectionPool` (min=1, max=5) reutiliza conexiones entre queries. El context manager `get_connection()` ejecuta
`rollback()` automáticamente ante cualquier excepción antes de devolver la conexión al pool, previniendo transacciones
sucias.

**Acceso a resultados por nombre de columna**
`db_helper.py` usa `psycopg2.extras.RealDictCursor`, de modo que todos los resultados son `dict`. El acceso es siempre
por clave (`row['codigo_final']`), nunca por índice numérico, lo que hace el código robusto ante cambios de orden en
columnas de vistas o queries.

**Numeración controlada por la base de datos**
`generar_codigo_documento()` aplica `FOR UPDATE` sobre `secuencia_documento` antes de incrementar el contador. Esto
garantiza que dos sesiones concurrentes no generen el mismo número sin necesidad de bloqueos a nivel de aplicación.

**Lógica de negocio en PL/pgSQL**
Las operaciones complejas (`crear_tramite`, `crear_documento`, `aplicar_impugnacion`, `fn_registrar_trazabilidad`)
residen en el motor de base de datos para asegurar atomicidad, consistencia y un único punto de verdad independiente del
cliente.

**Actualizaciones en tiempo real mediante LISTEN/NOTIFY**
`PgNotifyListener` mantiene una conexión dedicada en un hilo daemon que escucha `canal_documentos` y
`canal_proveedores`. Cuando se inserta un registro, PostgreSQL emite la notificación y la UI refresca los combos
automáticamente en todos los tabs, sin polling.

**Debounce de 400 ms en búsqueda por texto**
El módulo Consultar usa `QTimer.setSingleShot(True)` con 400 ms de espera antes de ejecutar la query. Esto evita
disparar una consulta por cada tecla pulsada, reduciendo la carga sobre la base de datos.

**Índices GIN con trigrama**
`documento.codigo_final` tiene un índice `gin_trgm_ops` que permite búsquedas `ILIKE '%texto%'` eficientes sobre grandes
volúmenes de documentos sin necesidad de full-text search.

**Cálculo de plazos con días laborables**
`sumar_dias_laborables(fecha, dias)` genera una serie de fechas excluyendo fines de semana y entradas de la tabla
`feriados`, retornando la fecha límite real. El resultado se almacena en `documento.fecha_termino` para consulta futura.

---

## Contribuir

1. Haz un fork del repositorio.
2. Crea una rama con un nombre descriptivo:
   ```bash
   git checkout -b feat/nombre-de-la-funcionalidad
   git checkout -b fix/descripcion-del-bug
   ```
3. Realiza tus cambios con commits atómicos siguiendo el formato:
   ```
   tipo(alcance): descripción breve en imperativo

   Cuerpo opcional con más detalle.
   ```
   Tipos válidos: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`.

4. Verifica que la aplicación levanta sin errores antes de hacer push:
   ```bash
   python main.py
   ```
5. Abre un Pull Request describiendo el problema que resuelve y los cambios realizados.

---

*Desarrollado como parte de las prácticas preprofesionales en la Coordinación Zonal 2 de ARCOTEL — 2026.*