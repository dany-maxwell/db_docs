"""Constantes de la aplicación"""

# Estados
ESTADO_POR_DEFECTO = "PETICIÓN PAS PENDIENTE"
ESTADO_REQUIERE_AP = "REQUIERE ACTUACION PREVIA"
ESTADO_AP = "EN ACTUACIÓN PREVIA"
ESTADO_INSTRUCCION = "EN INSTRUCCIÓN"
ESTADO_RESOLUCION = "EN RESOLUCIÓN"
ESTADO_RESUELTO = "RESUELTO"

# Estados para combo
ESTADOS_COMBO = ["", ESTADO_POR_DEFECTO, ESTADO_REQUIERE_AP, ESTADO_AP, ESTADO_INSTRUCCION, ESTADO_RESOLUCION, ESTADO_RESUELTO]

# Formato de fechas
FORMATO_FECHA = "yyyy-MM-dd"

# Índices de tablas
COLUMNAS_CONSULTAR = [
    ("tramite_id",    "N° Trámite"),
    ("proveedor",     "Proveedor"),
    ("unidad",        "Unidad"),
    ("fecha_tramite", "F. Inicio"),
    ("tipo",          "Tipo"),
    ("subtipo",       "Subtipo"),
    ("codigo",        "Código"),
    ("fecha",         "F. Doc"),
    ("origen",        "Origen"),
    ("infracciones",  "Infracciones"),
]

# Tipos de documento
TIPO_DOCUMENTO_MEMO = 1
TIPO_DOCUMENTO_AP = 4          # Actuación Previa
TIPO_DOCUMENTO_IAP = 5         # Informe AP
TIPO_DOCUMENTO_AI = 6          # Acto de Inicio
TIPO_DOCUMENTO_PR = 7          # Providencias
TIPO_DOCUMENTO_D = 8           # Dictamen
TIPO_DOCUMENTO_RPAS = 9        # Resolución
TIPO_DOCUMENTO_IJ = 11         # Informe Jurídico

# Subtipos de documento
SUBTIPO_AP = 2
SUBTIPO_IAP = 5
SUBTIPO_IJ = 11
SUBTIPO_PR_AP = 3           # Providencia en Actuación Previa
SUBTIPO_PR_INSTR = 7        # Providencia en Instrucción
SUBTIPO_PR_RES = 9          # Providencia en Resolución

# Unidad por defecto
UNIDAD_CODIGO_DEFAULT = 'CZO2'

# Mensajes
MSG_TRAMITE_INICIADO = "Trámite Iniciado"
MSG_INFRACCION_AGREGADA = "Ya agregada"
MSG_EXCEL_EXPORTADO = "Excel generado correctamente"
MSG_TITULO_RESUMEN = "RESUMEN DEL TRÁMITE"
MSG_NUMERO_TOMADO = "Número tomado"
MSG_YA_AGREGADO = "Ya agregaste esa infracción"
