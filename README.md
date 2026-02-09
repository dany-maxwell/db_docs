# Sistema de Gestión de Trámites

Este proyecto es una aplicación de escritorio desarrollada en **Python (PySide6 / Qt)** con base de datos **PostgreSQL**, orientada a la gestión y numeración de documentos dentro de trámites administrativos.

El sistema permite:
- Crear y administrar trámites.
- Tomar numeración oficial de distintos tipos de documentos.
- Consultar información por memo, código, proveedor, unidad y fechas.
- Exportar resultados a Excel.

---

## 1. Arquitectura General

El proyecto está dividido en tres capas principales:

### a) Base de Datos
Contiene la lógica central del negocio:
- Tablas de trámites, documentos, proveedores y unidades.
- Catálogos de tipos y subtipos de documentos.
- Control de secuencias para generación de códigos.
- Vistas para simplificar consultas desde la aplicación.

Se prioriza que los filtros complejos se ejecuten en PostgreSQL mediante vistas y funciones, dejando a Python únicamente la presentación.

### b) Capa de Servicios (Python)
Módulos encargados de:
- Conectarse a la base de datos.
- Ejecutar consultas y devolver datos limpios.
- Encapsular toda sentencia SQL para evitar lógica dispersa en la UI.

Principios utilizados:
- Un servicio = una responsabilidad.
- Retorno de datos en estructuras simples (listas/tuplas).
- Cero lógica de interfaz dentro de services.

### c) Interfaz Gráfica
Construida con PySide6:

Módulos principales:
- **Tomar Número**: generación de documentos oficiales
- **Consultas**: búsqueda y visualización de información

La UI solo consume servicios, sin SQL directo.

---

## 2. Flujo de Numeración

1. Un trámite se origina a partir de un memo.
2. Los documentos se registran inicialmente sin código oficial.
3. Al aprobarse, el sistema genera el código usando la secuencia.
4. Si el documento es rechazado antes de numerarse, puede eliminarse sin afectar la secuencia.

Esto garantiza:
- Secuencias limpias y reales.
- No existen huecos por documentos descartados.

---

## 3. Consultas

El módulo de consultas permite:
- Búsqueda por memo o por código.
- Filtros por tipo y subtipo.
- Búsqueda avanzada por:
  - Proveedor
  - Unidad
  - Estado
  - Rango de fechas

Resultados exportables a Excel con:
- Hoja resumen del trámite
- Listado de documentos relacionados

---

## 4. Decisiones Técnicas

- Uso de vistas SQL para:
  - Mantener consultas complejas fuera de la UI.
  - Facilitar cambios sin modificar Python.
- Índices en:
  - documento.tipo_documento_id
  - documento.tramite_id
  - documento.codigo_final
  - etc
- Retardos (debounce) en búsqueda por código para optimizar rendimiento.
- Arquitectura orientada a mantenimiento (microservicios).

---

## 5. Requisitos

- Python 3.10+
- PySide6
- psycopg2
- openpyxl
- PostgreSQL 13+

---

## 6. Estructura del Proyecto

- services/        → Acceso a datos
- ui/              → Interfaces Qt
- ui/consultar/    → Módulo de consultas
- ui/tomar_numero/ → Numeración
- database/        → Scripts SQL

---

## 7. Consideraciones

- El sistema actual es de gestión de información, no de almacenamiento de archivos.
- Toda numeración es controlada por la base de datos.
- La aplicación puede integrarse con sistemas externos mediante servicios.

---
