# db_docs — Sistema de Gestión de Trámites PAS

> Aplicación de escritorio para la gestión, numeración y seguimiento de documentos dentro de **Procedimientos Administrativos Sancionadores (PAS)**.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![PySide6](https://img.shields.io/badge/PySide6-Qt6-green?logo=qt)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13%2B-blue?logo=postgresql)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## Tabla de Contenidos

- [Descripción](#descripción)
- [Arquitectura](#arquitectura)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Módulos Principales](#módulos-principales)
- [Base de Datos](#base-de-datos)
- [Migración de Datos](#migración-de-datos)
- [Uso](#uso)
- [Decisiones Técnicas](#decisiones-técnicas)
- [Problemas Conocidos](#problemas-conocidos)
- [Contribuir](#contribuir)

---

## Descripción

`db_docs` es una aplicación de escritorio desarrollada con **Python + PySide6** y base de datos **PostgreSQL**. Gestiona el ciclo de vida completo de trámites administrativos sancionadores, desde la creación del expediente hasta la resolución final, incluyendo:

- Creación y seguimiento de trámites con sus proveedores/responsables.
- Generación automática de numeración oficial para cada tipo de documento.
- Registro de la trazabilidad cronológica de documentos por trámite.
- Búsqueda avanzada con exportación a Excel.
- Gestión de impugnaciones.
- Actualización en tiempo real vía PostgreSQL `LISTEN/NOTIFY`.

El flujo principal sigue el proceso sancionador:

```
Memorando PAS → [Actuación Previa] → Acto de Inicio → Instrucción → Resolución
```

---

## Arquitectura

```
┌──────────────────────────────────────────────────┐
│                  UI (PySide6 / Qt)                │
│  Crear Trámite │ Tomar Número │ Consultar │ Impu. │
└────────────────────────┬─────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────┐
│              Capa de Servicios (Python)            │
│  catalogo_service │ busqueda_service │ auditoria   │
└────────────────────────┬─────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────┐
│               Base de Datos (PostgreSQL)           │
│  Tablas │ Vistas │ Funciones PL/pgSQL │ Triggers   │
└──────────────────────────────────────────────────┘
```

**Principios aplicados:**
- La UI **nunca** ejecuta SQL directamente.
- La lógica de negocio vive en funciones PL/pgSQL (DB) o en `services/`.
- Los servicios devuelven estructuras simples (listas/tuplas), sin objetos UI.

---

## Requisitos Previos

| Herramienta   | Versión mínima |
|---------------|---------------|
| Python        | 3.10+         |
| PostgreSQL    | 13+           |
| pip           | 22+           |

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/dany-maxwell/db_docs.git
cd db_docs

# 2. Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt
```

**`requirements.txt` (mínimo requerido):**
```
PySide6>=6.5.0
psycopg2-binary>=2.9.0
python-dotenv>=1.0.0
openpyxl>=3.1.0
```

---

## Configuración

Crea un archivo `.env` en la raíz del proyecto basado en el siguiente ejemplo:

```env
# .env.example
DB_NAME=db_docs
DB_USER=user_app
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

> **⚠️ Importante:** Nunca subas el archivo `.env` al repositorio. Está incluido en `.gitignore`.

**Inicializar la base de datos:**

```bash
psql -U postgres -c "CREATE DATABASE db_docs;"
psql -U postgres -d db_docs -f query-database.sql
```

---

## Estructura del Proyecto

```
db_docs/
├── main.py                          # Punto de entrada
├── constants.py                     # Constantes globales (tipos, estados, mensajes)
├── .env                             # Variables de entorno (no versionado)
├── .env.example                     # Plantilla de configuración
├── requirements.txt                 # Dependencias Python
├── query-database.sql               # Schema completo de la base de datos
├── insert_excel_to_db.ipynb         # Notebook de migración de datos históricos
│
├── db/
│   ├── connection.py                # Pool de conexiones (psycopg2)
│   └── pg_listener.py               # Listener LISTEN/NOTIFY en hilo separado
│
├── services/
│   ├── db_helper.py                 # Ejecutor genérico de queries
│   ├── catalogo_service.py          # Consultas de catálogos (proveedores, tipos, etc.)
│   ├── busqueda_service.py          # Búsquedas por memo, código, avanzada
│   └── auditoria_service.py         # Operaciones de escritura (crear trámite, documento)
│
└── ui/
    ├── main_window.py               # Ventana principal con QTabWidget
    ├── widgets/
    │   └── widgets.py               # Widgets reutilizables (ComboBoxes, formularios)
    └── pages/
        ├── crear_tramite/
        │   ├── ui_crear_tramite.py          # Formulario nuevo trámite
        │   └── widget_nuevo_proveedor.py    # Subventana nuevo proveedor
        ├── tomar_numero/
        │   ├── base_tab.py                  # Clase base para tabs de numeración
        │   ├── ui_tomar_numero.py           # Contenedor de tabs
        │   ├── tab_ap.py                    # Actuación Previa
        │   ├── tab_iap.py                   # Informe de Actuación Previa
        │   ├── tab_ai.py                    # Acto de Inicio PAS
        │   ├── tab_rpas.py                  # Resolución PAS
        │   └── tab_de.py                    # Documentos extra (oficios, memorandos)
        ├── consultar/
        │   └── ui_consultar.py              # Búsqueda avanzada + exportación Excel
        └── impugnacion/
            └── ui_impugnacion.py            # Registro de impugnaciones
```

---

## Módulos Principales

### `Crear Trámite`
Registra un nuevo expediente con proveedor, unidad, servicio y asunto. Admite hasta tres documentos iniciales (Memorando, Petición Razonada, Informe Técnico). Permite crear nuevos proveedores desde la misma pantalla.

### `Tomar Número`
Genera la numeración oficial para cada etapa del proceso sancionador. Cada subtab corresponde a un tipo de documento:

| Tab | Documento | Constante |
|-----|-----------|-----------|
| AP | Actuación Previa | `TIPO_DOCUMENTO_AP = 4` |
| IAP | Informe de Actuación Previa | `TIPO_DOCUMENTO_IAP = 5` |
| AI | Acto de Inicio | `TIPO_DOCUMENTO_AI = 6` |
| RPAS | Resolución PAS | `TIPO_DOCUMENTO_RPAS = 9` |
| DE | Documentos Extra (Oficios, Memorandos) | tipos 12, 13, 14 |

La numeración es generada por la función `crear_documento()` en PostgreSQL, garantizando secuencias sin huecos.

### `Consultar`
Búsqueda avanzada usando `v_busqueda_avanzada` con filtros por memo, proveedor, unidad, tipo, subtipo, estado, código y rango de fechas. Permite exportar a Excel con hoja resumen y hoja de documentos.

### `Impugnación`
Registra un recurso de apelación asociando el código del documento de impugnación a un trámite existente.

---

## Base de Datos

### Tablas Principales

| Tabla | Descripción |
|-------|-------------|
| `tramite` | Expediente principal (proveedor, unidad, servicio, estado) |
| `documento` | Documentos vinculados a un trámite con código y tipo |
| `proveedor` | Prestador de servicios / presunto responsable |
| `tipo_documento` | Catálogo de tipos de documento |
| `subtipo_documento` | Subclasificación por tipo |
| `infraccion` | Catálogo de infracciones imputables |
| `documento_infraccion` | Relación N:M documento ↔ infracción |
| `trazabilidad_tramite` | Línea de tiempo de documentos por trámite |
| `secuencia_documento` | Control de numeración por tipo y año |
| `plantilla_codigo` | Formato de código por tipo (ej: `PAS-{ANIO}-{SEQ}`) |
| `feriados` | Tabla de días no laborables para calcular plazos |

### Vistas Clave

| Vista | Propósito |
|-------|-----------|
| `v_busqueda_avanzada` | Búsqueda combinada para el módulo Consultar |
| `v_documentos_tramite` | Lista de documentos de un trámite |
| `v_info_tramite_por_memo` | Datos del trámite dado un memo |
| `v_reporte_tramites` | Reporte pivot de hitos del proceso |
| `vista_seguimiento_final` | Matriz completa de seguimiento para exportación |

### Funciones PL/pgSQL

| Función | Descripción |
|---------|-------------|
| `crear_tramite(...)` | Crea el trámite y sus documentos iniciales en una transacción |
| `crear_documento(...)` | Genera un documento con código automático o manual |
| `generar_codigo_documento(...)` | Aplica plantilla + secuencia para obtener el código oficial |
| `actualizar_estado_tramite(...)` | Transiciona el estado del trámite |
| `sumar_dias_laborables(...)` | Calcula fecha término descontando feriados |
| `agregar_infraccion_a_documento(...)` | Asocia una infracción a un documento |
| `aplicar_impugnacion(...)` | Registra un recurso de apelación |

### Triggers

| Trigger | Tabla | Acción |
|---------|-------|--------|
| `trg_nuevo_documento` | `documento` | `NOTIFY canal_documentos` al insertar |
| `trg_post_insert_documento` | `documento` | Registra en `trazabilidad_tramite` |
| `trg_nuevo_proveedor` | `proveedor` | `NOTIFY canal_proveedores` al insertar |

---

## Migración de Datos

El archivo `insert_excel_to_db.ipynb` contiene el proceso ETL para cargar datos históricos desde un archivo Excel (`eda_prueba.xlsx`):

1. Normalización de texto (tildes, mayúsculas, espacios).
2. Corrección de typos en fechas (`amyo → mayo`, `octubte → octubre`).
3. Mapeo de proveedores, unidades y servicios a IDs de la BD.
4. Carga secuencial: proveedores → trámites → documentos (memo, petición, informes, etc.).

> **Nota:** Este notebook es de uso único para migración inicial. Las credenciales deben configurarse via variables de entorno antes de ejecutar.

---

## Uso

```bash
# Activar entorno virtual y ejecutar
source .venv/bin/activate
python main.py
```

---

## Decisiones Técnicas

- **Pool de conexiones** (`psycopg2.pool.SimpleConnectionPool`, min=1, max=5) para evitar conexiones por cada query.
- **LISTEN/NOTIFY** en hilo daemon para refrescar combos en tiempo real sin polling.
- **Vistas SQL** para mantener consultas complejas fuera del código Python.
- **`lru_cache`** en catálogos estáticos (`tipos`, `subtipos`, `infracciones`) para reducir round-trips a la BD.
- **Debounce de 400ms** (`QTimer.setSingleShot`) en la búsqueda por código para no disparar queries en cada tecla.
- **Índices GIN trigram** en `documento.codigo_final` para búsquedas `ILIKE` eficientes.

---

## Problemas Conocidos

Ver sección de [issues](https://github.com/dany-maxwell/db_docs/issues) para el estado actualizado. Los más relevantes identificados durante la revisión del código:

1. **Bug crítico — firma de `crear_tramite`**: La función Python pasa `servicio_id` como 3er argumento, pero la función PL/pgSQL no lo acepta ni lo inserta en `tramite`, a pesar de que `tramite.servicio_id` es `NOT NULL`. Esto genera un error en tiempo de ejecución.

2. **Manejo de transacciones**: `get_connection()` no hace rollback en excepciones, lo que puede dejar transacciones abiertas en el pool.

3. **Acceso por índice numérico**: Los resultados de BD se acceden como `fila[5]`, `fila[2]`, etc., lo que es frágil ante cambios en las vistas/queries.

4. **Import duplicado** en `ui_impugnacion.py`: `busqueda_por_memo` se importa dos veces.

5. **`lru_cache` no se invalida**: Si cambian los catálogos en BD durante la sesión, la UI no reflejará los cambios hasta reiniciar.

6. **Sin `requirements.txt` ni `.env.example`** en el repositorio.

---

## Contribuir

1. Haz un fork del repositorio.
2. Crea una rama descriptiva: `git checkout -b fix/crear-tramite-servicio-id`.
3. Realiza tus cambios con commits atómicos y mensajes en español o inglés.
4. Abre un Pull Request describiendo el problema y la solución.

---

*Desarrollado como parte de las prácticas preprofesionales — 2024.*
