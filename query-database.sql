-- DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION pg_database_owner;

COMMENT ON SCHEMA public IS 'standard public schema';

-- DROP TYPE public.gtrgm;

CREATE TYPE public.gtrgm (
	INPUT = gtrgm_in,
	OUTPUT = gtrgm_out,
	ALIGNMENT = 4,
	STORAGE = plain,
	CATEGORY = U,
	DELIMITER = ',');

-- DROP SEQUENCE public.documento_id_seq;

CREATE SEQUENCE public.documento_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE public.documento_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE public.documento_id_seq TO postgres;
GRANT USAGE, SELECT ON SEQUENCE public.documento_id_seq TO user_app;

-- DROP SEQUENCE public.infraccion_id_seq;

CREATE SEQUENCE public.infraccion_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE public.infraccion_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE public.infraccion_id_seq TO postgres;
GRANT USAGE, SELECT ON SEQUENCE public.infraccion_id_seq TO user_app;

-- DROP SEQUENCE public.plantilla_codigo_id_seq;

CREATE SEQUENCE public.plantilla_codigo_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE public.plantilla_codigo_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE public.plantilla_codigo_id_seq TO postgres;
GRANT USAGE, SELECT ON SEQUENCE public.plantilla_codigo_id_seq TO user_app;

-- DROP SEQUENCE public.proveedor_id_seq;

CREATE SEQUENCE public.proveedor_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE public.proveedor_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE public.proveedor_id_seq TO postgres;
GRANT USAGE, SELECT ON SEQUENCE public.proveedor_id_seq TO user_app;

-- DROP SEQUENCE public.secuencia_documento_id_seq;

CREATE SEQUENCE public.secuencia_documento_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE public.secuencia_documento_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE public.secuencia_documento_id_seq TO postgres;
GRANT USAGE, SELECT ON SEQUENCE public.secuencia_documento_id_seq TO user_app;

-- DROP SEQUENCE public.servicio_id_seq;

CREATE SEQUENCE public.servicio_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE public.servicio_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE public.servicio_id_seq TO postgres;
GRANT USAGE, SELECT ON SEQUENCE public.servicio_id_seq TO user_app;

-- DROP SEQUENCE public.subtipo_documento_id_seq;

CREATE SEQUENCE public.subtipo_documento_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE public.subtipo_documento_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE public.subtipo_documento_id_seq TO postgres;
GRANT USAGE, SELECT ON SEQUENCE public.subtipo_documento_id_seq TO user_app;

-- DROP SEQUENCE public.tipo_documento_id_seq;

CREATE SEQUENCE public.tipo_documento_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE public.tipo_documento_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE public.tipo_documento_id_seq TO postgres;
GRANT USAGE, SELECT ON SEQUENCE public.tipo_documento_id_seq TO user_app;

-- DROP SEQUENCE public.tramite_id_seq;

CREATE SEQUENCE public.tramite_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE public.tramite_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE public.tramite_id_seq TO postgres;
GRANT USAGE, SELECT ON SEQUENCE public.tramite_id_seq TO user_app;

-- DROP SEQUENCE public.trazabilidad_tramite_id_seq;

CREATE SEQUENCE public.trazabilidad_tramite_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE public.trazabilidad_tramite_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE public.trazabilidad_tramite_id_seq TO postgres;
GRANT USAGE, SELECT ON SEQUENCE public.trazabilidad_tramite_id_seq TO user_app;

-- DROP SEQUENCE public.unidad_id_seq;

CREATE SEQUENCE public.unidad_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE public.unidad_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE public.unidad_id_seq TO postgres;
GRANT USAGE, SELECT ON SEQUENCE public.unidad_id_seq TO user_app;
-- public.feriados definition

-- Drop table

-- DROP TABLE public.feriados;

CREATE TABLE public.feriados (
	fecha date NOT NULL,
	descripcion text NULL,
	CONSTRAINT feriados_pkey PRIMARY KEY (fecha)
);

-- Permissions

ALTER TABLE public.feriados OWNER TO postgres;
GRANT ALL ON TABLE public.feriados TO postgres;
GRANT INSERT, UPDATE, SELECT ON TABLE public.feriados TO user_app;


-- public.infraccion definition

-- Drop table

-- DROP TABLE public.infraccion;

CREATE TABLE public.infraccion (
	id serial4 NOT NULL,
	codigo_infraccion varchar(30) NOT NULL,
	descripcion varchar(250) NULL,
	CONSTRAINT infraccion_pkey PRIMARY KEY (id)
);

-- Permissions

ALTER TABLE public.infraccion OWNER TO postgres;
GRANT ALL ON TABLE public.infraccion TO postgres;
GRANT INSERT, UPDATE, SELECT ON TABLE public.infraccion TO user_app;


-- public.proveedor definition

-- Drop table

-- DROP TABLE public.proveedor;

CREATE TABLE public.proveedor (
	id serial4 NOT NULL,
	nombre varchar(200) NOT NULL,
	cedula_ruc varchar(50) NULL,
	canton varchar(50) NULL,
	ciudad varchar(50) NULL,
	provincia varchar(50) NULL,
	CONSTRAINT proveedor_pkey PRIMARY KEY (id)
);

-- Table Triggers

create trigger trg_nuevo_proveedor after
insert
    on
    public.proveedor for each row execute function notify_nuevo_proveedor();

-- Permissions

ALTER TABLE public.proveedor OWNER TO postgres;
GRANT ALL ON TABLE public.proveedor TO postgres;
GRANT INSERT, UPDATE, SELECT ON TABLE public.proveedor TO user_app;


-- public.servicio definition

-- Drop table

-- DROP TABLE public.servicio;

CREATE TABLE public.servicio (
	id serial4 NOT NULL,
	servicio varchar(200) NOT NULL,
	CONSTRAINT servicio_pkey PRIMARY KEY (id)
);

-- Permissions

ALTER TABLE public.servicio OWNER TO postgres;
GRANT ALL ON TABLE public.servicio TO postgres;
GRANT INSERT, UPDATE, SELECT ON TABLE public.servicio TO user_app;


-- public.tipo_documento definition

-- Drop table

-- DROP TABLE public.tipo_documento;

CREATE TABLE public.tipo_documento (
	id serial4 NOT NULL,
	nombre varchar(100) NOT NULL,
	se_numera_en_unidad bool DEFAULT false NOT NULL,
	requiere_infraccion bool DEFAULT false NOT NULL,
	CONSTRAINT tipo_documento_pkey PRIMARY KEY (id)
);

-- Permissions

ALTER TABLE public.tipo_documento OWNER TO postgres;
GRANT ALL ON TABLE public.tipo_documento TO postgres;
GRANT INSERT, UPDATE, SELECT ON TABLE public.tipo_documento TO user_app;


-- public.trazabilidad_tramite definition

-- Drop table

-- DROP TABLE public.trazabilidad_tramite;

CREATE TABLE public.trazabilidad_tramite (
	id serial4 NOT NULL,
	tramite_id int4 NOT NULL,
	documento_id int4 NOT NULL,
	linea_proceso int4 DEFAULT 1 NOT NULL,
	CONSTRAINT trazabilidad_tramite_pkey PRIMARY KEY (id),
	CONSTRAINT trazabilidad_tramite_tramite_id_documento_id_key UNIQUE (tramite_id, documento_id)
);
CREATE INDEX idx_trazabilidad_documento ON public.trazabilidad_tramite USING btree (documento_id);
CREATE INDEX idx_trazabilidad_id ON public.trazabilidad_tramite USING btree (id);
CREATE INDEX idx_trazabilidad_tramite ON public.trazabilidad_tramite USING btree (tramite_id);

-- Permissions

ALTER TABLE public.trazabilidad_tramite OWNER TO postgres;
GRANT ALL ON TABLE public.trazabilidad_tramite TO postgres;
GRANT INSERT, UPDATE, SELECT ON TABLE public.trazabilidad_tramite TO user_app;


-- public.unidad definition

-- Drop table

-- DROP TABLE public.unidad;

CREATE TABLE public.unidad (
	id serial4 NOT NULL,
	codigo varchar(35) NOT NULL,
	nombre varchar(150) NULL,
	CONSTRAINT unidad_pkey PRIMARY KEY (id)
);

-- Permissions

ALTER TABLE public.unidad OWNER TO postgres;
GRANT ALL ON TABLE public.unidad TO postgres;
GRANT INSERT, UPDATE, SELECT ON TABLE public.unidad TO user_app;


-- public.plantilla_codigo definition

-- Drop table

-- DROP TABLE public.plantilla_codigo;

CREATE TABLE public.plantilla_codigo (
	id serial4 NOT NULL,
	tipo_documento_id int4 NOT NULL,
	formato varchar(100) NOT NULL,
	reinicio varchar(20) NOT NULL,
	CONSTRAINT plantilla_codigo_pkey PRIMARY KEY (id),
	CONSTRAINT plantilla_codigo_tipo_documento_id_fkey FOREIGN KEY (tipo_documento_id) REFERENCES public.tipo_documento(id)
);

-- Permissions

ALTER TABLE public.plantilla_codigo OWNER TO postgres;
GRANT ALL ON TABLE public.plantilla_codigo TO postgres;
GRANT INSERT, UPDATE, SELECT ON TABLE public.plantilla_codigo TO user_app;


-- public.secuencia_documento definition

-- Drop table

-- DROP TABLE public.secuencia_documento;

CREATE TABLE public.secuencia_documento (
	id serial4 NOT NULL,
	plantilla_id int4 NOT NULL,
	anio int4 NOT NULL,
	ultimo_numero int4 DEFAULT 0 NOT NULL,
	CONSTRAINT secuencia_documento_pkey PRIMARY KEY (id),
	CONSTRAINT secuencia_documento_plantilla_id_fkey FOREIGN KEY (plantilla_id) REFERENCES public.plantilla_codigo(id)
);

-- Permissions

ALTER TABLE public.secuencia_documento OWNER TO postgres;
GRANT ALL ON TABLE public.secuencia_documento TO postgres;
GRANT INSERT, UPDATE, SELECT ON TABLE public.secuencia_documento TO user_app;


-- public.subtipo_documento definition

-- Drop table

-- DROP TABLE public.subtipo_documento;

CREATE TABLE public.subtipo_documento (
	id serial4 NOT NULL,
	tipo_documento_id int4 NOT NULL,
	nombre varchar(120) NOT NULL,
	CONSTRAINT subtipo_documento_pkey PRIMARY KEY (id),
	CONSTRAINT subtipo_documento_tipo_documento_id_fkey FOREIGN KEY (tipo_documento_id) REFERENCES public.tipo_documento(id)
);

-- Permissions

ALTER TABLE public.subtipo_documento OWNER TO postgres;
GRANT ALL ON TABLE public.subtipo_documento TO postgres;
GRANT INSERT, UPDATE, SELECT ON TABLE public.subtipo_documento TO user_app;


-- public.tramite definition

-- Drop table

-- DROP TABLE public.tramite;

CREATE TABLE public.tramite (
	id serial4 NOT NULL,
	proveedor_id int4 NOT NULL,
	unidad_id int4 NOT NULL,
	estado varchar(30) DEFAULT 'PETICION PAS PENDIENTE'::character varying NOT NULL,
	fecha_insercion date DEFAULT CURRENT_DATE NOT NULL,
	asunto text NULL,
	prosigue bool DEFAULT true NOT NULL,
	servicio_id int4 NOT NULL,
	observacion text NULL,
	CONSTRAINT tramite_pkey PRIMARY KEY (id),
	CONSTRAINT tramite_proveedor_id_fkey FOREIGN KEY (proveedor_id) REFERENCES public.proveedor(id),
	CONSTRAINT tramite_servicio_id_fkey FOREIGN KEY (servicio_id) REFERENCES public.servicio(id),
	CONSTRAINT tramite_unidad_id_fkey FOREIGN KEY (unidad_id) REFERENCES public.unidad(id)
);
CREATE INDEX idx_tramite_id ON public.tramite USING btree (id);
CREATE INDEX idx_tramite_proveedor ON public.tramite USING btree (proveedor_id);
CREATE INDEX idx_tramite_unidad ON public.tramite USING btree (unidad_id);

-- Permissions

ALTER TABLE public.tramite OWNER TO postgres;
GRANT ALL ON TABLE public.tramite TO postgres;
GRANT INSERT, UPDATE, SELECT ON TABLE public.tramite TO user_app;


-- public.documento definition

-- Drop table

-- DROP TABLE public.documento;

CREATE TABLE public.documento (
	id serial4 NOT NULL,
	tramite_id int4 NOT NULL,
	tipo_documento_id int4 NOT NULL,
	subtipo_documento_id int4 NULL,
	documento_origen_id int4 NULL,
	codigo_final text NOT NULL,
	es_manual bool DEFAULT false NOT NULL,
	fecha_documento timestamp(0) DEFAULT now() NULL,
	archivado bool DEFAULT false NOT NULL,
	asunto text NULL,
	plazo int4 NULL,
	fecha_termino date NULL,
	CONSTRAINT documento_pkey PRIMARY KEY (id),
	CONSTRAINT documento_documento_origen_id_fkey FOREIGN KEY (documento_origen_id) REFERENCES public.documento(id),
	CONSTRAINT documento_subtipo_documento_id_fkey FOREIGN KEY (subtipo_documento_id) REFERENCES public.subtipo_documento(id),
	CONSTRAINT documento_tipo_documento_id_fkey FOREIGN KEY (tipo_documento_id) REFERENCES public.tipo_documento(id),
	CONSTRAINT documento_tramite_id_fkey FOREIGN KEY (tramite_id) REFERENCES public.tramite(id) ON DELETE CASCADE
);
CREATE INDEX idx_documento_codigo ON public.documento USING btree (codigo_final);
CREATE INDEX idx_documento_codigo_trgm ON public.documento USING gin (codigo_final gin_trgm_ops);
CREATE INDEX idx_documento_id ON public.documento USING btree (id);
CREATE INDEX idx_documento_origen ON public.documento USING btree (documento_origen_id);
CREATE INDEX idx_documento_subtipo ON public.documento USING btree (subtipo_documento_id);
CREATE INDEX idx_documento_tipo ON public.documento USING btree (tipo_documento_id);
CREATE INDEX idx_documento_tramite ON public.documento USING btree (tramite_id);

-- Table Triggers

create trigger trg_nuevo_documento after
insert
    on
    public.documento for each row execute function notify_nuevo_documento();
create trigger trg_post_insert_documento after
insert
    on
    public.documento for each row execute function fn_registrar_trazabilidad();

-- Permissions

ALTER TABLE public.documento OWNER TO postgres;
GRANT ALL ON TABLE public.documento TO postgres;
GRANT INSERT, UPDATE, SELECT ON TABLE public.documento TO user_app;


-- public.documento_infraccion definition

-- Drop table

-- DROP TABLE public.documento_infraccion;

CREATE TABLE public.documento_infraccion (
	documento_id int4 NOT NULL,
	infraccion_id int4 NOT NULL,
	CONSTRAINT documento_infraccion_pkey PRIMARY KEY (documento_id, infraccion_id),
	CONSTRAINT documento_infraccion_documento_id_fkey FOREIGN KEY (documento_id) REFERENCES public.documento(id) ON DELETE CASCADE,
	CONSTRAINT documento_infraccion_infraccion_id_fkey FOREIGN KEY (infraccion_id) REFERENCES public.infraccion(id)
);

-- Permissions

ALTER TABLE public.documento_infraccion OWNER TO postgres;
GRANT ALL ON TABLE public.documento_infraccion TO postgres;
GRANT INSERT, UPDATE, SELECT ON TABLE public.documento_infraccion TO user_app;


-- public.v_busqueda_avanzada source

CREATE OR REPLACE VIEW public.v_busqueda_avanzada
AS SELECT t.id AS tramite_id,
    p.id AS proveedor_id,
    p.nombre AS proveedor,
    u.id AS unidad_id,
    u.codigo AS unidad,
    mem.id AS memo_id,
    mem.codigo_final AS memo,
    t.fecha_insercion AS fecha_tramite,
    t.estado,
    d.id AS documento_id,
    td.nombre AS tipo,
    td.id AS tipo_id,
    sd.nombre AS subtipo,
    sd.id AS subtipo_id,
    d.codigo_final AS codigo,
    d.fecha_documento AS fecha,
    orig.codigo_final AS origen,
    ( SELECT string_agg(i.codigo_infraccion::text, ', '::text) AS string_agg
           FROM documento_infraccion di
             JOIN infraccion i ON i.id = di.infraccion_id
          WHERE di.documento_id = d.id) AS infracciones,
    d.archivado
   FROM tramite t
     JOIN proveedor p ON p.id = t.proveedor_id
     JOIN unidad u ON u.id = t.unidad_id
     JOIN documento mem ON mem.tramite_id = t.id AND mem.tipo_documento_id = 1
     JOIN documento d ON d.tramite_id = t.id
     JOIN tipo_documento td ON td.id = d.tipo_documento_id
     LEFT JOIN subtipo_documento sd ON sd.id = d.subtipo_documento_id
     LEFT JOIN documento orig ON orig.id = d.documento_origen_id;

-- Permissions

ALTER TABLE public.v_busqueda_avanzada OWNER TO postgres;
GRANT ALL ON TABLE public.v_busqueda_avanzada TO postgres;
GRANT INSERT, UPDATE, SELECT ON TABLE public.v_busqueda_avanzada TO user_app;


-- public.v_consulta_documentos source

CREATE OR REPLACE VIEW public.v_consulta_documentos
AS SELECT d.id,
    d.tramite_id,
    t.id AS id_tramite,
    p.nombre AS proveedor,
    u.codigo AS unidad,
    td.id AS tipo_id,
    td.nombre AS tipo,
    st.id AS subtipo_id,
    st.nombre AS subtipo,
    d.codigo_final,
    d.fecha_documento,
    dor.codigo_final AS codigo_origen,
    string_agg(i.codigo_infraccion::text, ', '::text) AS infracciones
   FROM documento d
     JOIN tramite t ON t.id = d.tramite_id
     JOIN proveedor p ON p.id = t.proveedor_id
     JOIN unidad u ON u.id = t.unidad_id
     JOIN tipo_documento td ON td.id = d.tipo_documento_id
     LEFT JOIN subtipo_documento st ON st.id = d.subtipo_documento_id
     LEFT JOIN documento dor ON dor.id = d.documento_origen_id
     LEFT JOIN documento_infraccion di ON di.documento_id = d.id
     LEFT JOIN infraccion i ON i.id = di.infraccion_id
  GROUP BY d.id, t.id, p.nombre, u.codigo, td.id, td.nombre, st.id, st.nombre, d.codigo_final, d.fecha_documento, dor.codigo_final;

-- Permissions

ALTER TABLE public.v_consulta_documentos OWNER TO postgres;
GRANT ALL ON TABLE public.v_consulta_documentos TO postgres;
GRANT INSERT, UPDATE, SELECT ON TABLE public.v_consulta_documentos TO user_app;


-- public.v_documentos_tramite source

CREATE OR REPLACE VIEW public.v_documentos_tramite
AS SELECT d.tramite_id,
    td.nombre AS tipo,
    st.nombre AS subtipo,
    d.codigo_final,
    d.fecha_documento,
    dor.codigo_final AS origen,
    ( SELECT string_agg(i.codigo_infraccion::text, ', '::text) AS string_agg
           FROM documento_infraccion di
             JOIN infraccion i ON i.id = di.infraccion_id
          WHERE di.documento_id = d.id) AS infracciones,
    td.id AS tipo_id,
    st.id AS subtipo_id,
    d.id AS documento_id,
    t.estado
   FROM documento d
     JOIN tipo_documento td ON td.id = d.tipo_documento_id
     LEFT JOIN subtipo_documento st ON st.id = d.subtipo_documento_id
     LEFT JOIN documento dor ON dor.id = d.documento_origen_id
     JOIN tramite t ON d.tramite_id = t.id;

-- Permissions

ALTER TABLE public.v_documentos_tramite OWNER TO postgres;
GRANT ALL ON TABLE public.v_documentos_tramite TO postgres;
GRANT INSERT, UPDATE, SELECT ON TABLE public.v_documentos_tramite TO user_app;


-- public.v_info_tramite_por_memo source

CREATE OR REPLACE VIEW public.v_info_tramite_por_memo
AS SELECT d.id,
    d.codigo_final,
    p.nombre AS proveedor,
    p.cedula_ruc,
    u.codigo AS unidad,
    t.id AS tramite,
    t.estado,
    t.fecha_insercion
   FROM documento d
     JOIN tramite t ON d.tramite_id = t.id
     JOIN proveedor p ON p.id = t.proveedor_id
     JOIN unidad u ON u.id = t.unidad_id
  WHERE d.tipo_documento_id = 1;

-- Permissions

ALTER TABLE public.v_info_tramite_por_memo OWNER TO postgres;
GRANT ALL ON TABLE public.v_info_tramite_por_memo TO postgres;
GRANT INSERT, UPDATE, SELECT ON TABLE public.v_info_tramite_por_memo TO user_app;


-- public.v_jp source

CREATE OR REPLACE VIEW public.v_jp
AS SELECT p.nombre AS proveedor_id,
    u.codigo AS unidad_id,
    s.servicio AS servicio_id,
    t.id AS tramite_id,
    t.asunto
   FROM tramite t
     JOIN proveedor p ON t.proveedor_id = p.id
     JOIN unidad u ON t.unidad_id = u.id
     JOIN servicio s ON t.servicio_id = s.id;

-- Permissions

ALTER TABLE public.v_jp OWNER TO postgres;
GRANT ALL ON TABLE public.v_jp TO postgres;
GRANT INSERT, UPDATE, SELECT ON TABLE public.v_jp TO user_app;


-- public.v_reporte_tramites source

CREATE OR REPLACE VIEW public.v_reporte_tramites
AS SELECT t.id AS tramite,
    p.nombre AS proveedor,
    p.cedula_ruc,
    u.codigo AS unidad,
    memo.codigo_final AS memo,
    memo.fecha_documento AS fecha_memo,
    ptr.codigo_final AS ptr,
    ptr.fecha_documento AS fecha_ptr,
    it.codigo_final AS it,
    it.fecha_documento AS fecha_it,
    t.asunto,
    ap.codigo_final AS ap,
    ap.fecha_documento AS fecha_ap,
    iap1.codigo_final AS iap1,
    iap1.fecha_documento AS fecha_iap1,
    iapf.codigo_final AS iapf,
    iapf.fecha_documento AS fecha_iapf,
    t.prosigue,
    ai.codigo_final AS ai,
    ai.fecha_documento AS fecha_ai,
    infr.infracciones AS posible_infraccion,
    d.codigo_final AS d,
    d.fecha_documento AS fecha_d,
    rpas.codigo_final AS rpas,
    rpas.fecha_documento AS fecha_rpas,
    t.estado
   FROM tramite t
     LEFT JOIN proveedor p ON p.id = t.proveedor_id
     LEFT JOIN unidad u ON u.id = t.unidad_id
     LEFT JOIN ( SELECT documento.id,
            documento.tramite_id,
            documento.tipo_documento_id,
            documento.subtipo_documento_id,
            documento.documento_origen_id,
            documento.codigo_final,
            documento.es_manual,
            documento.fecha_documento,
            documento.archivado,
            documento.asunto
           FROM documento
          WHERE documento.tipo_documento_id = 1
          ORDER BY documento.tramite_id, documento.id DESC) memo ON memo.tramite_id = t.id
     LEFT JOIN ( SELECT documento.id,
            documento.tramite_id,
            documento.tipo_documento_id,
            documento.subtipo_documento_id,
            documento.documento_origen_id,
            documento.codigo_final,
            documento.es_manual,
            documento.fecha_documento,
            documento.archivado,
            documento.asunto
           FROM documento
          WHERE documento.tipo_documento_id = 2
          ORDER BY documento.tramite_id, documento.id DESC) ptr ON ptr.tramite_id = t.id
     LEFT JOIN ( SELECT documento.id,
            documento.tramite_id,
            documento.tipo_documento_id,
            documento.subtipo_documento_id,
            documento.documento_origen_id,
            documento.codigo_final,
            documento.es_manual,
            documento.fecha_documento,
            documento.archivado,
            documento.asunto
           FROM documento
          WHERE documento.tipo_documento_id = 3
          ORDER BY documento.tramite_id, documento.id DESC) it ON it.tramite_id = t.id
     LEFT JOIN ( SELECT documento.id,
            documento.tramite_id,
            documento.tipo_documento_id,
            documento.subtipo_documento_id,
            documento.documento_origen_id,
            documento.codigo_final,
            documento.es_manual,
            documento.fecha_documento,
            documento.archivado,
            documento.asunto
           FROM documento
          WHERE documento.tipo_documento_id = 4
          ORDER BY documento.tramite_id, documento.id DESC) ap ON ap.tramite_id = t.id
     LEFT JOIN ( SELECT documento.id,
            documento.tramite_id,
            documento.tipo_documento_id,
            documento.subtipo_documento_id,
            documento.documento_origen_id,
            documento.codigo_final,
            documento.es_manual,
            documento.fecha_documento,
            documento.archivado,
            documento.asunto
           FROM documento
          WHERE documento.tipo_documento_id = 5 AND documento.subtipo_documento_id = 1
          ORDER BY documento.tramite_id, documento.id DESC) iap1 ON iap1.tramite_id = t.id
     LEFT JOIN ( SELECT documento.id,
            documento.tramite_id,
            documento.tipo_documento_id,
            documento.subtipo_documento_id,
            documento.documento_origen_id,
            documento.codigo_final,
            documento.es_manual,
            documento.fecha_documento,
            documento.archivado,
            documento.asunto
           FROM documento
          WHERE documento.tipo_documento_id = 5 AND documento.subtipo_documento_id = 2
          ORDER BY documento.tramite_id, documento.id DESC) iapf ON iapf.tramite_id = t.id
     LEFT JOIN ( SELECT documento.id,
            documento.tramite_id,
            documento.tipo_documento_id,
            documento.subtipo_documento_id,
            documento.documento_origen_id,
            documento.codigo_final,
            documento.es_manual,
            documento.fecha_documento,
            documento.archivado,
            documento.asunto
           FROM documento
          WHERE documento.tipo_documento_id = 6
          ORDER BY documento.tramite_id, documento.id DESC) ai ON ai.tramite_id = t.id
     LEFT JOIN ( SELECT idoc.documento_id,
            string_agg(i.codigo_infraccion::text, ' | '::text ORDER BY (i.codigo_infraccion::text)) AS infracciones
           FROM documento_infraccion idoc
             JOIN infraccion i ON i.id = idoc.infraccion_id
          GROUP BY idoc.documento_id) infr ON infr.documento_id = ai.id
     LEFT JOIN ( SELECT documento.id,
            documento.tramite_id,
            documento.tipo_documento_id,
            documento.subtipo_documento_id,
            documento.documento_origen_id,
            documento.codigo_final,
            documento.es_manual,
            documento.fecha_documento,
            documento.archivado,
            documento.asunto
           FROM documento
          WHERE documento.tipo_documento_id = 8
          ORDER BY documento.tramite_id, documento.id DESC) d ON d.tramite_id = t.id
     LEFT JOIN ( SELECT documento.id,
            documento.tramite_id,
            documento.tipo_documento_id,
            documento.subtipo_documento_id,
            documento.documento_origen_id,
            documento.codigo_final,
            documento.es_manual,
            documento.fecha_documento,
            documento.archivado,
            documento.asunto
           FROM documento
          WHERE documento.tipo_documento_id = 9
          ORDER BY documento.tramite_id, documento.id DESC) rpas ON rpas.tramite_id = t.id;

-- Permissions

ALTER TABLE public.v_reporte_tramites OWNER TO postgres;
GRANT ALL ON TABLE public.v_reporte_tramites TO postgres;
GRANT INSERT, UPDATE, SELECT ON TABLE public.v_reporte_tramites TO user_app;


-- public.vista_seguimiento_final source

CREATE OR REPLACE VIEW public.vista_seguimiento_final
AS WITH datos_agrupados AS (
         SELECT tr.tramite_id,
            tr.linea_proceso,
            d.tipo_documento_id,
            d.subtipo_documento_id,
            o.tipo_documento_id AS tipo_origen,
            o.subtipo_documento_id AS subtipo_origen,
            d.codigo_final,
            d.fecha_documento,
            d.plazo,
            d.fecha_termino,
            d.asunto
           FROM trazabilidad_tramite tr
             JOIN documento d ON tr.documento_id = d.id
             LEFT JOIN documento o ON o.id = d.documento_origen_id
        ), matriz_completa AS (
         SELECT datos_agrupados.tramite_id,
            datos_agrupados.linea_proceso,
            datos_agrupados.tipo_documento_id,
            datos_agrupados.subtipo_documento_id,
            datos_agrupados.tipo_origen,
            datos_agrupados.subtipo_origen,
            datos_agrupados.fecha_documento,
            datos_agrupados.plazo,
            datos_agrupados.fecha_termino,
            datos_agrupados.asunto,
            first_value(datos_agrupados.codigo_final) OVER (PARTITION BY datos_agrupados.tramite_id, datos_agrupados.tipo_documento_id, datos_agrupados.subtipo_documento_id, datos_agrupados.tipo_origen, datos_agrupados.subtipo_origen ORDER BY datos_agrupados.linea_proceso DESC RANGE BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING) AS nombre_documento
           FROM datos_agrupados
        )
 SELECT m.tramite_id AS "N Tramite",
    m.linea_proceso AS "Linea de Tiempo",
    p.nombre AS "PRESUNTO RESPONSABLE",
    p.cedula_ruc AS "CÉDULA - RUC",
    p.canton AS "Cantón",
    p.ciudad AS "Ciudad",
    p.provincia AS "Provincia",
    u.codigo AS "UNIDAD REQUIRIENTE",
    s.servicio AS "SERVICIO CONTROLADO",
    max(
        CASE
            WHEN m.tipo_documento_id = 1 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "MEMORANDO PETICION INICIO PAS",
    max(
        CASE
            WHEN m.tipo_documento_id = 1 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA MEMORANDO PETICION INICIO PAS",
    max(
        CASE
            WHEN m.tipo_documento_id = 2 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "PETICIÓN RAZONADA",
    max(
        CASE
            WHEN m.tipo_documento_id = 2 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA PETICIÓN RAZONADA",
    max(
        CASE
            WHEN m.tipo_documento_id = 15 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "INFORME TÉCNICO",
    max(
        CASE
            WHEN m.tipo_documento_id = 15 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA INFORME TÉCNICO",
    t.asunto AS "ASUNTO / EXTRACTO HECHO DETECTADO",
    max(
        CASE
            WHEN m.tipo_documento_id = 4 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "No. ACTUACIÓN PREVIA",
    max(
        CASE
            WHEN m.tipo_documento_id = 4 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA No. ACTUACIÓN PREVIA",
    max(
        CASE
            WHEN m.tipo_documento_id = 12 AND m.subtipo_documento_id = 13 AND m.tipo_origen = 4 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "OFICIO NOTIFICACIÓN ACTUACIÓN PREVIA",
    max(
        CASE
            WHEN m.tipo_documento_id = 12 AND m.subtipo_documento_id = 13 AND m.tipo_origen = 4 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA OFICIO NOTIFICACIÓN ACTUACIÓN PREVIA",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 14 AND m.tipo_origen = 4 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "MEMORANDO NOTIFICACION ACTUACIÓN PREVIA",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 14 AND m.tipo_origen = 4 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA MEMORANDO NOTIFICACION ACTUACIÓN PREVIA",
    max(
        CASE
            WHEN m.tipo_documento_id = 7 AND m.subtipo_documento_id = 3 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "PROVIDENCIAS ACTUACIONES PREVIAS",
    max(
        CASE
            WHEN m.tipo_documento_id = 7 AND m.subtipo_documento_id = 3 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA PROVIDENCIAS ACTUACIONES PREVIAS",
    max(
        CASE
            WHEN m.tipo_documento_id = 12 AND m.subtipo_documento_id = 13 AND m.tipo_origen = 7 AND m.subtipo_origen = 3 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "OFICIO ENVIO PROVIDENCIAS ACTUACIONES PREVIAS",
    max(
        CASE
            WHEN m.tipo_documento_id = 12 AND m.subtipo_documento_id = 13 AND m.tipo_origen = 7 AND m.subtipo_origen = 3 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA OFICIO ENVIO PROVIDENCIAS ACTUACIONES PREVIAS",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 15 AND m.tipo_origen = 7 AND m.subtipo_origen = 3 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "MEMORANDO PRUEBA DE NOTIFICACIÓN PROVIDENCIAS ACTUACIONES PREV",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 15 AND m.tipo_origen = 7 AND m.subtipo_origen = 3 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA MEMORANDO PRUEBA DE NOTIFICACIÓN PROVIDENCIAS ACTUACIONE",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 23 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "MEMORANDOS - OFICIOS - ACTUACIÓN PREVIA",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 23 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA MEMORANDOS - OFICIOS - ACTUACIÓN PREVIA",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 24 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "MEMORANDO RESPUESTA MEMORANDOS - OFICIOS -  ACTUACIÓN PREVIA",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 24 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA MEMORANDO RESPUESTA MEMORANDOS - OFICIOS -  ACTUACIÓN PR",
    max(
        CASE
            WHEN m.tipo_documento_id = 5 AND m.subtipo_documento_id = 1 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "INFORME DE ACTUACIÓN PREVIA",
    max(
        CASE
            WHEN m.tipo_documento_id = 5 AND m.subtipo_documento_id = 1 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA INFORME DE ACTUACIÓN PREVIA",
    max(
        CASE
            WHEN m.tipo_documento_id = 12 AND m.subtipo_documento_id = 13 AND m.tipo_origen = 5 AND m.subtipo_origen = 1 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "OFICIO NOTIFICACIÓN INFORME DE ACTUACÓN PREVIA",
    max(
        CASE
            WHEN m.tipo_documento_id = 12 AND m.subtipo_documento_id = 13 AND m.tipo_origen = 5 AND m.subtipo_origen = 1 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA OFICIO NOTIFICACIÓN INFORME DE ACTUACÓN PREVIA",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 15 AND m.tipo_origen = 5 AND m.subtipo_origen = 1 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "MEMORANDO PRUEBA DE NOTIFICACIÓN DE INFORME DE ACTUACIÓN PREV",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 15 AND m.tipo_origen = 5 AND m.subtipo_origen = 1 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA MEMORANDO PRUEBA DE NOTIFICACIÓN DE INFORME DE ACTUACIÓ",
    max(
        CASE
            WHEN m.tipo_documento_id = 14 AND m.subtipo_documento_id = 28 AND m.tipo_origen = 5 AND m.subtipo_origen = 1 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "RESPUESTA DE INFORME DE ACTUACIÓN PREVIA",
    max(
        CASE
            WHEN m.tipo_documento_id = 14 AND m.subtipo_documento_id = 28 AND m.tipo_origen = 5 AND m.subtipo_origen = 1 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA RESPUESTA DE INFORME DE ACTUACIÓN PREVIA",
    max(
        CASE
            WHEN m.tipo_documento_id = 5 AND m.subtipo_documento_id = 2 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "INFORME FINAL ACTUACIÓN PREVIA",
    max(
        CASE
            WHEN m.tipo_documento_id = 5 AND m.subtipo_documento_id = 2 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA INFORME FINAL ACTUACIÓN PREVIA",
    max(
        CASE
            WHEN m.tipo_documento_id = 12 AND m.subtipo_documento_id = 13 AND m.tipo_origen = 5 AND m.subtipo_origen = 2 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "OFICIO DE NOTIFICACIÓN INFORME FINAL ACTUACIÓN PREVIA",
    max(
        CASE
            WHEN m.tipo_documento_id = 12 AND m.subtipo_documento_id = 13 AND m.tipo_origen = 5 AND m.subtipo_origen = 2 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA OFICIO DE NOTIFICACIÓN INFORME FINAL ACTUACIÓN PREVIA",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 14 AND m.tipo_origen = 5 AND m.subtipo_origen = 2 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "MEMORANDO DE NOTIFICACIÓN DE INFORME FINAL DE ACTUACIÓN PREVI",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 14 AND m.tipo_origen = 5 AND m.subtipo_origen = 2 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA MEMORANDO DE NOTIFICACIÓN DE INFORME FINAL DE ACTUACIÓN",
    t.prosigue AS "PROCEDE INICIO DE PAS",
    max(
        CASE
            WHEN m.tipo_documento_id = 11 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "INFORME JURIDICO PAS",
    max(
        CASE
            WHEN m.tipo_documento_id = 11 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA INFORME JURIDICO PAS",
    max(
        CASE
            WHEN m.tipo_documento_id = 6 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "ACTO DE INICIO PAS",
    max(
        CASE
            WHEN m.tipo_documento_id = 6 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA ACTO DE INICIO PAS",
    max(
        CASE
            WHEN m.tipo_documento_id = 12 AND m.subtipo_documento_id = 13 AND m.tipo_origen = 6 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "OFICIO NOTIFICACIÓN",
    max(
        CASE
            WHEN m.tipo_documento_id = 12 AND m.subtipo_documento_id = 13 AND m.tipo_origen = 6 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA OFICIO NOTIFICACIÓN",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 15 AND m.tipo_origen = 6 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "MEMORANDO PRUEBA DE NOTIFICACIÓN",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 15 AND m.tipo_origen = 6 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA MEMORANDO PRUEBA DE NOTIFICACIÓN",
    max(
        CASE
            WHEN m.tipo_documento_id = 14 AND m.subtipo_documento_id = 21 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "RESPUESTA PRESTADOR",
    max(
        CASE
            WHEN m.tipo_documento_id = 14 AND m.subtipo_documento_id = 21 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA RESPUESTA PRESTADOR",
    max(
        CASE
            WHEN m.tipo_documento_id = 7 AND m.subtipo_documento_id = 8 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "PROVIDENCIA EVACUACIÓN PRUEBAS",
    max(
        CASE
            WHEN m.tipo_documento_id = 7 AND m.subtipo_documento_id = 8 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA PROVIDENCIA EVACUACIÓN PRUEBAS",
    max(
        CASE
            WHEN m.tipo_documento_id = 12 AND m.subtipo_documento_id = 13 AND m.tipo_origen = 7 AND m.subtipo_origen = 8 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "OFICIO NOTIFICACION PROVIDENCIA",
    max(
        CASE
            WHEN m.tipo_documento_id = 12 AND m.subtipo_documento_id = 13 AND m.tipo_origen = 7 AND m.subtipo_origen = 8 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA OFICIO NOTIFICACION PROVIDENCIA",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 15 AND m.tipo_origen = 7 AND m.subtipo_origen = 8 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "MEMORANDO PRUEBA DE NOTIFICACIÓN PROVIDENCIA",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 15 AND m.tipo_origen = 7 AND m.subtipo_origen = 8 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA MEMORANDO PRUEBA DE NOTIFICACIÓN PROVIDENCIA",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 16 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "MEMORANDO A UNIDAD DE DOCUMENTACIÓN Y ARCHIVO",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 16 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA MEMORANDO A UNIDAD DE DOCUMENTACIÓN Y ARCHIVO",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 25 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "MEMORANDO RESPUESTA DE  DOCUMENTACIÓN Y ARCHIVO",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 25 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA MEMORANDO RESPUESTA DE  DOCUMENTACIÓN Y ARCHIVO",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 17 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "OTROS MEMORANDOS A DEDA Y A OTRAS UNIDADES",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 17 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA OTROS MEMORANDOS A DEDA Y A OTRAS UNIDADES",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 26 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "MEMORANDO RESPUESTA A OTROS MEMORANDOS A DEDA Y A OTRAS UNIDADE",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 26 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA MEMORANDO RESPUESTA A OTROS MEMORANDOS A DEDA Y A OTRAS U",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 18 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "MEMORANDO A GESTIÓN ECONÓMICA",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 18 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA MEMORANDO A GESTIÓN ECONÓMICA",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 27 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "RESPUESTA DE GESTIÓN ECONÓMICA",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 27 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA RESPUESTA DE GESTIÓN ECONÓMICA",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 20 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "MEMORANDO A SERVIDOR TÉCNICO",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 20 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA MEMORANDO A SERVIDOR TÉCNICO",
    max(
        CASE
            WHEN m.tipo_documento_id = 3 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "No. INFORME TÉCNICO",
    max(
        CASE
            WHEN m.tipo_documento_id = 3 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA No. INFORME TÉCNICO",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 19 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "MEMORANDO A SERVIDOR JURÍDICO",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 19 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA MEMORANDO A SERVIDOR JURÍDICO",
    max(
        CASE
            WHEN m.tipo_documento_id = 11 AND m.subtipo_documento_id = 10 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "No. INFORME JURÍDICO - INSTRUCCIÓN",
    max(
        CASE
            WHEN m.tipo_documento_id = 11 AND m.subtipo_documento_id = 10 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA No. INFORME JURÍDICO - INSTRUCCIÓN",
    max(
        CASE
            WHEN m.tipo_documento_id = 7 AND m.subtipo_documento_id = 5 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "PROVIDENCIA NOTIFICANDO LO ACTUADO",
    max(
        CASE
            WHEN m.tipo_documento_id = 7 AND m.subtipo_documento_id = 5 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA PROVIDENCIA NOTIFICANDO LO ACTUADO",
    max(
        CASE
            WHEN m.tipo_documento_id = 7 AND m.subtipo_documento_id = 6 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "PROVIDENCIA CIERRE DE TÉRMINO DE PRUEBA",
    max(
        CASE
            WHEN m.tipo_documento_id = 7 AND m.subtipo_documento_id = 6 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA PROVIDENCIA CIERRE DE TÉRMINO DE PRUEBA",
    max(
        CASE
            WHEN m.tipo_documento_id = 12 AND m.subtipo_documento_id = 13 AND m.tipo_origen = 7 AND m.subtipo_origen = 6 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "OFICIO DE PROVIDENCIA DE CIERRE DE PRUEBA",
    max(
        CASE
            WHEN m.tipo_documento_id = 12 AND m.subtipo_documento_id = 13 AND m.tipo_origen = 7 AND m.subtipo_origen = 6 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA OFICIO DE PROVIDENCIA DE CIERRE DE PRUEBA",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 14 AND m.tipo_origen = 7 AND m.subtipo_origen = 6 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "MEMORANDO DE NOTIFICACIÓN DE CIERRE DE PRUEBA",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 14 AND m.tipo_origen = 7 AND m.subtipo_origen = 6 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA MEMORANDO DE NOTIFICACIÓN DE CIERRE DE PRUEBA",
    max(
        CASE
            WHEN m.tipo_documento_id = 7 AND m.subtipo_documento_id = 7 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "PROVIDENCIA REMITE INFORMES IJ e IT",
    max(
        CASE
            WHEN m.tipo_documento_id = 7 AND m.subtipo_documento_id = 7 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA PROVIDENCIA REMITE INFORMES IJ e IT",
    max(
        CASE
            WHEN m.tipo_documento_id = 8 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "No. DICTAMEN",
    max(
        CASE
            WHEN m.tipo_documento_id = 8 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA No. DICTAMEN",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 29 AND m.tipo_origen = 8 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "MEMORANDO DICTAMEN A CZO2 / PRESUNTO RESPONSABLE",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 29 AND m.tipo_origen = 8 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA MEMORANDO DICTAMEN A CZO2 / PRESUNTO RESPONSABLE",
    max(
        CASE
            WHEN m.tipo_documento_id = 7 AND m.subtipo_documento_id = 9 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "PROVIDENCIA EXTENSIÓN PLAZO",
    max(
        CASE
            WHEN m.tipo_documento_id = 7 AND m.subtipo_documento_id = 9 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA PROVIDENCIA EXTENSIÓN PLAZO",
    max(
        CASE
            WHEN m.tipo_documento_id = 7 AND m.subtipo_documento_id = 9 THEN m.plazo
            ELSE NULL::integer
        END) AS "PLAZO (meses)",
    max(
        CASE
            WHEN m.tipo_documento_id = 7 AND m.subtipo_documento_id = 3 THEN m.fecha_termino
            ELSE NULL::date
        END) AS "PLAZO A PARTIR DE …",
    max(
        CASE
            WHEN m.tipo_documento_id = 9 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "No. RESOLUCIÓN",
    max(
        CASE
            WHEN m.tipo_documento_id = 9 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA No. RESOLUCIÓN",
    max(
        CASE
            WHEN m.tipo_documento_id = 9 THEN m.asunto
            ELSE NULL::text
        END) AS "SANCIÓN",
    max(
        CASE
            WHEN m.tipo_documento_id = 12 AND m.subtipo_documento_id = 13 AND m.tipo_origen = 9 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "OFICIO NOTIFICACIÓN RESOLUCIÓN",
    max(
        CASE
            WHEN m.tipo_documento_id = 12 AND m.subtipo_documento_id = 13 AND m.tipo_origen = 9 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA OFICIO NOTIFICACIÓN RESOLUCIÓN",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 15 AND m.tipo_origen = 9 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "MEMORANDO PRUEBA DE NOTIFICACIÓN RESOLUCIÓN",
    max(
        CASE
            WHEN m.tipo_documento_id = 13 AND m.subtipo_documento_id = 15 AND m.tipo_origen = 9 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA MEMORANDO PRUEBA DE NOTIFICACIÓN RESOLUCIÓN",
    max(
        CASE
            WHEN m.tipo_documento_id = 10 THEN m.nombre_documento
            ELSE NULL::text
        END) AS "APELACIÓN / RESOLUCIÓN",
    max(
        CASE
            WHEN m.tipo_documento_id = 10 THEN m.fecha_documento
            ELSE NULL::timestamp without time zone
        END) AS "FECHA APELACIÓN / RESOLUCIÓN",
    max(
        CASE
            WHEN m.tipo_documento_id = 10 THEN m.asunto
            ELSE NULL::text
        END) AS "DECISIÓN RECURSO DE APELACIÓN",
    t.estado AS "ESTADO"
   FROM matriz_completa m
     JOIN tramite t ON m.tramite_id = t.id
     JOIN proveedor p ON t.proveedor_id = p.id
     JOIN unidad u ON t.unidad_id = u.id
     JOIN servicio s ON t.servicio_id = s.id
  GROUP BY m.tramite_id, m.linea_proceso, p.nombre, p.cedula_ruc, p.canton, p.ciudad, p.provincia, u.codigo, s.servicio, t.asunto, t.prosigue, t.estado
  ORDER BY m.tramite_id, m.linea_proceso;

-- Permissions

ALTER TABLE public.vista_seguimiento_final OWNER TO postgres;
GRANT ALL ON TABLE public.vista_seguimiento_final TO postgres;
GRANT INSERT, UPDATE, SELECT ON TABLE public.vista_seguimiento_final TO user_app;


-- public.vista_seguimiento_tipos source

CREATE OR REPLACE VIEW public.vista_seguimiento_tipos
AS WITH RECURSIVE historial_completo AS (
         SELECT tr.tramite_id,
            tr.linea_proceso,
            d.id AS documento_id,
            d.tipo_documento_id,
            d.codigo_final
           FROM trazabilidad_tramite tr
             JOIN documento d ON d.id = tr.documento_id
        )
 SELECT tramite_id,
    linea_proceso AS linea_tiempo,
    max(
        CASE
            WHEN tipo_documento_id = 1 THEN nombre
            ELSE NULL::text
        END) AS memorando,
    max(
        CASE
            WHEN tipo_documento_id = 4 THEN nombre
            ELSE NULL::text
        END) AS actuacion,
    max(
        CASE
            WHEN tipo_documento_id = 6 THEN nombre
            ELSE NULL::text
        END) AS acto_inicio,
    max(
        CASE
            WHEN tipo_documento_id = 3 THEN nombre
            ELSE NULL::text
        END) AS informe
   FROM ( SELECT hc.tramite_id,
            hc.linea_proceso,
            hc.tipo_documento_id,
            first_value(hc.codigo_final) OVER (PARTITION BY hc.tramite_id, hc.tipo_documento_id ORDER BY hc.linea_proceso DESC ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING) AS nombre
           FROM ( SELECT v.tramite_id,
                    v.linea_proceso,
                    t.tipo_documento_id
                   FROM ( SELECT DISTINCT trazabilidad_tramite.tramite_id,
                            trazabilidad_tramite.linea_proceso
                           FROM trazabilidad_tramite) v
                     CROSS JOIN ( SELECT DISTINCT documento.tipo_documento_id
                           FROM documento) t) base
             LEFT JOIN historial_completo hc ON base.tramite_id = hc.tramite_id AND base.linea_proceso = hc.linea_proceso AND base.tipo_documento_id = hc.tipo_documento_id) final
  GROUP BY tramite_id, linea_proceso
  ORDER BY tramite_id, linea_proceso;

-- Permissions

ALTER TABLE public.vista_seguimiento_tipos OWNER TO postgres;
GRANT ALL ON TABLE public.vista_seguimiento_tipos TO postgres;
GRANT INSERT, UPDATE, SELECT ON TABLE public.vista_seguimiento_tipos TO user_app;



-- DROP FUNCTION public.actualizar_estado_tramite(varchar, int4);

CREATE OR REPLACE FUNCTION public.actualizar_estado_tramite(p_estado character varying, p_tramite_id integer)
 RETURNS integer
 LANGUAGE plpgsql
AS $function$

begin
	update tramite set estado = p_estado where id = p_tramite_id;
	return p_tramite_id;
end;
$function$
;

-- Permissions

ALTER FUNCTION public.actualizar_estado_tramite(varchar, int4) OWNER TO postgres;
GRANT ALL ON FUNCTION public.actualizar_estado_tramite(varchar, int4) TO postgres;

-- DROP FUNCTION public.agregar_infraccion_a_documento(int4, int4);

CREATE OR REPLACE FUNCTION public.agregar_infraccion_a_documento(p_documento integer, p_infraccion integer)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
begin

    if exists (
        select 1
        from documento_infraccion
        where documento_id = p_documento
          and infraccion_id = p_infraccion
    ) then
        return;
    end if;

    insert into documento_infraccion(
        documento_id,
        infraccion_id
    )
    values (
        p_documento,
        p_infraccion
    );

end;
$function$
;

-- Permissions

ALTER FUNCTION public.agregar_infraccion_a_documento(int4, int4) OWNER TO postgres;
GRANT ALL ON FUNCTION public.agregar_infraccion_a_documento(int4, int4) TO postgres;

-- DROP FUNCTION public.aplicar_impugnacion(varchar, date, int4, int4);

CREATE OR REPLACE FUNCTION public.aplicar_impugnacion(p_codigo_imp character varying, p_fecha_imp date, p_tramite_id integer, p_documento_id integer)
 RETURNS integer
 LANGUAGE plpgsql
AS $function$
declare
	v_rows_updated int;

begin
	update documento set archivado = true
	where tramite_id = p_tramite_id
	and id >= p_documento_id;
	
	insert into documento (tramite_id, tipo_documento_id, codigo_final, es_manual, fecha_documento)
	values
	(p_tramite_id, 10, p_codigo_imp, True, p_fecha_imp);

	get diagnostics v_rows_updated = row_count;

	return v_rows_updated;
end;
$function$
;

-- Permissions

ALTER FUNCTION public.aplicar_impugnacion(varchar, date, int4, int4) OWNER TO postgres;
GRANT ALL ON FUNCTION public.aplicar_impugnacion(varchar, date, int4, int4) TO postgres;

-- DROP FUNCTION public.crear_documento(int4, int4, int4, int4, varchar, varchar, date, text, int4, date);

CREATE OR REPLACE FUNCTION public.crear_documento(p_tramite integer, p_tipo integer, p_subtipo integer, p_origen integer, p_codigo_manual character varying, p_unidad character varying, p_fecha_documento date DEFAULT NULL::date, p_asunto text DEFAULT NULL::text, p_plazo integer DEFAULT NULL::integer, p_fecha_termino date DEFAULT NULL::date)
 RETURNS integer
 LANGUAGE plpgsql
AS $function$
declare
    v_codigo varchar;
    v_es_manual boolean;
    v_anio int := extract(year from current_date);
    v_id int;
	v_fecha timestamp;
begin

    if p_codigo_manual is not null then
        v_codigo := p_codigo_manual;
        v_es_manual := true;
    else
        v_codigo := generar_codigo_documento(
                        p_tipo,
                        p_unidad,
                        v_anio);
        v_es_manual := false;
    end if;

	if p_fecha_documento is not null then
		v_fecha := p_fecha_documento;
	else
		v_fecha := now();
	end if;

    insert into documento(
        tramite_id,
        tipo_documento_id,
        subtipo_documento_id,
        documento_origen_id,
        codigo_final,
		fecha_documento,
        es_manual,
		asunto,
		plazo,
		fecha_termino
    )
    values (
        p_tramite,
        p_tipo,
        p_subtipo,
        p_origen,
        v_codigo,
		v_fecha,
        v_es_manual,
		p_asunto,
		p_plazo,
		p_fecha_termino
    )
    returning id into v_id;
    return v_id;
end;
$function$
;

-- Permissions

ALTER FUNCTION public.crear_documento(int4, int4, int4, int4, varchar, varchar, date, text, int4, date) OWNER TO postgres;
GRANT ALL ON FUNCTION public.crear_documento(int4, int4, int4, int4, varchar, varchar, date, text, int4, date) TO postgres;

-- DROP FUNCTION public.crear_tramite(int4, int4, int4, varchar, date, text, varchar, date, varchar, date, varchar, date);

CREATE OR REPLACE FUNCTION public.crear_tramite(p_proveedor_id integer, p_unidad_id integer, p_servicio_id integer, p_estado character varying, p_fecha_tramite date, p_asunto text, p_codigo_memo character varying, p_fecha_memo date, p_codigo_peticion character varying DEFAULT NULL::character varying, p_fecha_peticion date DEFAULT NULL::date, p_codigo_informe character varying DEFAULT NULL::character varying, p_fecha_informe date DEFAULT NULL::date)
 RETURNS integer
 LANGUAGE plpgsql
AS $function$
declare
	v_tramite_id int;
begin
	insert into tramite (proveedor_id, unidad_id, servicio_id, estado, fecha_insercion, asunto) values
		(p_proveedor_id, p_unidad_id, p_servicio_id, p_estado, p_fecha_tramite, p_asunto) returning id into v_tramite_id;

	insert into documento (tramite_id, tipo_documento_id, codigo_final, es_manual, fecha_documento) values
		(v_tramite_id, 1, p_codigo_memo, True, p_fecha_memo);

	if p_codigo_peticion is not null then
		insert into documento (tramite_id, tipo_documento_id, codigo_final, es_manual, fecha_documento) values
			(v_tramite_id, 2, p_codigo_peticion, True, p_fecha_peticion);
	end if;
	
	if p_codigo_informe is not null then
		insert into documento (tramite_id, tipo_documento_id, codigo_final, es_manual, fecha_documento) values
			(v_tramite_id, 15, p_codigo_informe, True, p_fecha_informe);
	end if;
	return v_tramite_id;
end 
$function$
;

-- Permissions

ALTER FUNCTION public.crear_tramite(int4, int4, int4, varchar, date, text, varchar, date, varchar, date, varchar, date) OWNER TO postgres;
GRANT ALL ON FUNCTION public.crear_tramite(int4, int4, int4, varchar, date, text, varchar, date, varchar, date, varchar, date) TO postgres;

-- DROP FUNCTION public.f_buscar_documentos(int4, text, int4, int4);

CREATE OR REPLACE FUNCTION public.f_buscar_documentos(p_memo integer DEFAULT NULL::integer, p_codigo text DEFAULT NULL::text, p_tipo integer DEFAULT NULL::integer, p_subtipo integer DEFAULT NULL::integer)
 RETURNS TABLE(tipo text, subtipo text, codigo text, fecha date, origen text, infracciones text, id integer)
 LANGUAGE sql
AS $function$

select
    tipo,
    subtipo,
    codigo_final,
    fecha_documento,
    codigo_origen,
    infracciones,
	id

from v_consulta_documentos
where

(
    (
        p_memo is not null
        and tramite_id = (
            select tramite_id
            from documento
            where id = p_memo
        )
    )

    or (
        p_memo is null
        and p_codigo is not null
        and codigo_final ilike '%' || p_codigo || '%'
    )

    or (
        p_memo is null
        and p_codigo is null
    )
)

and (
    p_codigo is null
    or codigo_final ilike '%' || p_codigo || '%'
)

and (p_tipo is null or tipo_id = p_tipo)

and (p_subtipo is null or subtipo_id = p_subtipo)

order by id desc;

$function$
;

-- Permissions

ALTER FUNCTION public.f_buscar_documentos(int4, text, int4, int4) OWNER TO postgres;
GRANT ALL ON FUNCTION public.f_buscar_documentos(int4, text, int4, int4) TO postgres;

-- DROP FUNCTION public.f_buscar_tramites(text, text, text, date, date, int4, int4);

CREATE OR REPLACE FUNCTION public.f_buscar_tramites(p_proveedor text DEFAULT NULL::text, p_unidad text DEFAULT NULL::text, p_estado text DEFAULT NULL::text, p_fecha_desde date DEFAULT NULL::date, p_fecha_hasta date DEFAULT NULL::date, p_anio integer DEFAULT NULL::integer, p_mes integer DEFAULT NULL::integer)
 RETURNS TABLE(proveedor text, unidad text, memo text, fecha_tramite date, tipo text, subtipo text, codigo text, fecha_doc date, origen text, infracciones text)
 LANGUAGE sql
AS $function$

select
    proveedor,
    unidad,
    memo,
    fecha_tramite,

    tipo,
    subtipo,
    codigo_final,
    fecha_documento,
    codigo_origen,
    infracciones

from v_consulta_tramite
where

    -- proveedor
    (p_proveedor is null or proveedor ilike '%'||p_proveedor||'%')

    -- unidad
    and (p_unidad is null or unidad = p_unidad)

    -- estado
    and (p_estado is null or estado = p_estado)

    -- rango fechas
    and (p_fecha_desde is null or fecha_tramite >= p_fecha_desde)
    and (p_fecha_hasta is null or fecha_tramite <= p_fecha_hasta)

    -- año / mes
    and (p_anio is null or extract(year from fecha_tramite) = p_anio)
    and (p_mes is null or extract(month from fecha_tramite) = p_mes)

order by fecha_tramite desc, fecha_documento;

$function$
;

-- Permissions

ALTER FUNCTION public.f_buscar_tramites(text, text, text, date, date, int4, int4) OWNER TO postgres;
GRANT ALL ON FUNCTION public.f_buscar_tramites(text, text, text, date, date, int4, int4) TO postgres;

-- DROP FUNCTION public.fn_registrar_trazabilidad();

CREATE OR REPLACE FUNCTION public.fn_registrar_trazabilidad()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
DECLARE
    v_linea_padre INT;
    v_nueva_linea INT;
    v_existe_reintento BOOLEAN;
BEGIN
    -- 1. Buscamos la línea de tiempo donde está el padre (doc4)
    SELECT linea_proceso INTO v_linea_padre
    FROM trazabilidad_tramite
    WHERE documento_id = NEW.documento_origen_id;

    -- 2. ¿Existe ya algún otro documento que nació del doc4 y fue archivado?
    -- Esto nos confirma que el nuevo documento es una "corrección" o reintento.
    SELECT EXISTS (
        SELECT 1 FROM documento 
        WHERE documento_origen_id = NEW.documento_origen_id 
        AND archivado = True
        AND id != NEW.id
    ) INTO v_existe_reintento;

    -- 3. Decidimos la línea de proceso
    IF v_linea_padre IS NULL THEN
        -- Es el primer documento del trámite (el PAS)
        INSERT INTO trazabilidad_tramite (tramite_id, documento_id, linea_proceso)
        VALUES (NEW.tramite_id, NEW.id, 1);

    ELSIF v_existe_reintento THEN
        -- Si hay un hijo archivado, saltamos a la siguiente línea global del trámite
        SELECT COALESCE(MAX(linea_proceso), 0) + 1 INTO v_nueva_linea 
        FROM trazabilidad_tramite 
        WHERE tramite_id = NEW.tramite_id;

        INSERT INTO trazabilidad_tramite (tramite_id, documento_id, linea_proceso)
        VALUES (NEW.tramite_id, NEW.id, v_nueva_linea);

    ELSE
        -- Flujo normal: misma línea que el padre
        INSERT INTO trazabilidad_tramite (tramite_id, documento_id, linea_proceso)
        VALUES (NEW.tramite_id, NEW.id, v_linea_padre);
    END IF;

    RETURN NEW;
END;
$function$
;

-- Permissions

ALTER FUNCTION public.fn_registrar_trazabilidad() OWNER TO postgres;
GRANT ALL ON FUNCTION public.fn_registrar_trazabilidad() TO postgres;

-- DROP FUNCTION public.generar_codigo_documento(int4, varchar, int4);

CREATE OR REPLACE FUNCTION public.generar_codigo_documento(p_tipo_documento integer, p_unidad_codigo character varying, p_anio integer)
 RETURNS character varying
 LANGUAGE plpgsql
AS $function$
declare
    v_formato varchar;
    v_plantilla_id int;
    v_secuencia int;
    v_codigo varchar;
begin

    -- 1. obtener plantilla del tipo
    select id, formato
    into v_plantilla_id, v_formato
    from plantilla_codigo
    where tipo_documento_id = p_tipo_documento;

    if v_plantilla_id is null then
        raise exception 'no existe plantilla para este tipo de documento';
    end if;

    -- 2. buscar secuencia del año
    select ultimo_numero
    into v_secuencia
    from secuencia_documento
    where plantilla_id = v_plantilla_id
      and anio = p_anio
    for update;

    -- 3. si no existe secuencia, crearla
    if v_secuencia is null then

        insert into secuencia_documento
        (plantilla_id, anio, ultimo_numero)
        values
        (v_plantilla_id, p_anio, 1);

        v_secuencia := 1;

    else
        -- 4. incrementar
        v_secuencia := v_secuencia + 1;

        update secuencia_documento
        set ultimo_numero = v_secuencia
        where plantilla_id = v_plantilla_id
          and anio = p_anio;
    end if;

    -- 5. construir codigo
    v_codigo := v_formato;

    v_codigo := replace(v_codigo, '{unidad}', p_unidad_codigo);
    v_codigo := replace(v_codigo, '{anio}', p_anio::varchar);
    v_codigo := replace(v_codigo, '{sec}', 
                    lpad(v_secuencia::varchar, 4, '0'));

    return v_codigo;

end;
$function$
;

-- Permissions

ALTER FUNCTION public.generar_codigo_documento(int4, varchar, int4) OWNER TO postgres;
GRANT ALL ON FUNCTION public.generar_codigo_documento(int4, varchar, int4) TO postgres;

-- DROP FUNCTION public.gin_extract_query_trgm(text, internal, int2, internal, internal, internal, internal);

CREATE OR REPLACE FUNCTION public.gin_extract_query_trgm(text, internal, smallint, internal, internal, internal, internal)
 RETURNS internal
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$gin_extract_query_trgm$function$
;

-- Permissions

ALTER FUNCTION public.gin_extract_query_trgm(text, internal, int2, internal, internal, internal, internal) OWNER TO postgres;
GRANT ALL ON FUNCTION public.gin_extract_query_trgm(text, internal, int2, internal, internal, internal, internal) TO postgres;

-- DROP FUNCTION public.gin_extract_value_trgm(text, internal);

CREATE OR REPLACE FUNCTION public.gin_extract_value_trgm(text, internal)
 RETURNS internal
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$gin_extract_value_trgm$function$
;

-- Permissions

ALTER FUNCTION public.gin_extract_value_trgm(text, internal) OWNER TO postgres;
GRANT ALL ON FUNCTION public.gin_extract_value_trgm(text, internal) TO postgres;

-- DROP FUNCTION public.gin_trgm_consistent(internal, int2, text, int4, internal, internal, internal, internal);

CREATE OR REPLACE FUNCTION public.gin_trgm_consistent(internal, smallint, text, integer, internal, internal, internal, internal)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$gin_trgm_consistent$function$
;

-- Permissions

ALTER FUNCTION public.gin_trgm_consistent(internal, int2, text, int4, internal, internal, internal, internal) OWNER TO postgres;
GRANT ALL ON FUNCTION public.gin_trgm_consistent(internal, int2, text, int4, internal, internal, internal, internal) TO postgres;

-- DROP FUNCTION public.gin_trgm_triconsistent(internal, int2, text, int4, internal, internal, internal);

CREATE OR REPLACE FUNCTION public.gin_trgm_triconsistent(internal, smallint, text, integer, internal, internal, internal)
 RETURNS "char"
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$gin_trgm_triconsistent$function$
;

-- Permissions

ALTER FUNCTION public.gin_trgm_triconsistent(internal, int2, text, int4, internal, internal, internal) OWNER TO postgres;
GRANT ALL ON FUNCTION public.gin_trgm_triconsistent(internal, int2, text, int4, internal, internal, internal) TO postgres;

-- DROP FUNCTION public.gtrgm_compress(internal);

CREATE OR REPLACE FUNCTION public.gtrgm_compress(internal)
 RETURNS internal
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$gtrgm_compress$function$
;

-- Permissions

ALTER FUNCTION public.gtrgm_compress(internal) OWNER TO postgres;
GRANT ALL ON FUNCTION public.gtrgm_compress(internal) TO postgres;

-- DROP FUNCTION public.gtrgm_consistent(internal, text, int2, oid, internal);

CREATE OR REPLACE FUNCTION public.gtrgm_consistent(internal, text, smallint, oid, internal)
 RETURNS boolean
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$gtrgm_consistent$function$
;

-- Permissions

ALTER FUNCTION public.gtrgm_consistent(internal, text, int2, oid, internal) OWNER TO postgres;
GRANT ALL ON FUNCTION public.gtrgm_consistent(internal, text, int2, oid, internal) TO postgres;

-- DROP FUNCTION public.gtrgm_decompress(internal);

CREATE OR REPLACE FUNCTION public.gtrgm_decompress(internal)
 RETURNS internal
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$gtrgm_decompress$function$
;

-- Permissions

ALTER FUNCTION public.gtrgm_decompress(internal) OWNER TO postgres;
GRANT ALL ON FUNCTION public.gtrgm_decompress(internal) TO postgres;

-- DROP FUNCTION public.gtrgm_distance(internal, text, int2, oid, internal);

CREATE OR REPLACE FUNCTION public.gtrgm_distance(internal, text, smallint, oid, internal)
 RETURNS double precision
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$gtrgm_distance$function$
;

-- Permissions

ALTER FUNCTION public.gtrgm_distance(internal, text, int2, oid, internal) OWNER TO postgres;
GRANT ALL ON FUNCTION public.gtrgm_distance(internal, text, int2, oid, internal) TO postgres;

-- DROP FUNCTION public.gtrgm_in(cstring);

CREATE OR REPLACE FUNCTION public.gtrgm_in(cstring)
 RETURNS gtrgm
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$gtrgm_in$function$
;

-- Permissions

ALTER FUNCTION public.gtrgm_in(cstring) OWNER TO postgres;
GRANT ALL ON FUNCTION public.gtrgm_in(cstring) TO postgres;

-- DROP FUNCTION public.gtrgm_options(internal);

CREATE OR REPLACE FUNCTION public.gtrgm_options(internal)
 RETURNS void
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE
AS '$libdir/pg_trgm', $function$gtrgm_options$function$
;

-- Permissions

ALTER FUNCTION public.gtrgm_options(internal) OWNER TO postgres;
GRANT ALL ON FUNCTION public.gtrgm_options(internal) TO postgres;

-- DROP FUNCTION public.gtrgm_out(gtrgm);

CREATE OR REPLACE FUNCTION public.gtrgm_out(gtrgm)
 RETURNS cstring
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$gtrgm_out$function$
;

-- Permissions

ALTER FUNCTION public.gtrgm_out(gtrgm) OWNER TO postgres;
GRANT ALL ON FUNCTION public.gtrgm_out(gtrgm) TO postgres;

-- DROP FUNCTION public.gtrgm_penalty(internal, internal, internal);

CREATE OR REPLACE FUNCTION public.gtrgm_penalty(internal, internal, internal)
 RETURNS internal
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$gtrgm_penalty$function$
;

-- Permissions

ALTER FUNCTION public.gtrgm_penalty(internal, internal, internal) OWNER TO postgres;
GRANT ALL ON FUNCTION public.gtrgm_penalty(internal, internal, internal) TO postgres;

-- DROP FUNCTION public.gtrgm_picksplit(internal, internal);

CREATE OR REPLACE FUNCTION public.gtrgm_picksplit(internal, internal)
 RETURNS internal
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$gtrgm_picksplit$function$
;

-- Permissions

ALTER FUNCTION public.gtrgm_picksplit(internal, internal) OWNER TO postgres;
GRANT ALL ON FUNCTION public.gtrgm_picksplit(internal, internal) TO postgres;

-- DROP FUNCTION public.gtrgm_same(gtrgm, gtrgm, internal);

CREATE OR REPLACE FUNCTION public.gtrgm_same(gtrgm, gtrgm, internal)
 RETURNS internal
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$gtrgm_same$function$
;

-- Permissions

ALTER FUNCTION public.gtrgm_same(gtrgm, gtrgm, internal) OWNER TO postgres;
GRANT ALL ON FUNCTION public.gtrgm_same(gtrgm, gtrgm, internal) TO postgres;

-- DROP FUNCTION public.gtrgm_union(internal, internal);

CREATE OR REPLACE FUNCTION public.gtrgm_union(internal, internal)
 RETURNS gtrgm
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$gtrgm_union$function$
;

-- Permissions

ALTER FUNCTION public.gtrgm_union(internal, internal) OWNER TO postgres;
GRANT ALL ON FUNCTION public.gtrgm_union(internal, internal) TO postgres;

-- DROP FUNCTION public.notify_nuevo_documento();

CREATE OR REPLACE FUNCTION public.notify_nuevo_documento()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
begin
	perform pg_notify('canal_documentos', new.codigo_final);
	return new;
end
$function$
;

-- Permissions

ALTER FUNCTION public.notify_nuevo_documento() OWNER TO postgres;
GRANT ALL ON FUNCTION public.notify_nuevo_documento() TO postgres;

-- DROP FUNCTION public.notify_nuevo_proveedor();

CREATE OR REPLACE FUNCTION public.notify_nuevo_proveedor()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
begin
	perform pg_notify('canal_proveedores', new.id::text);
	return new;
end
$function$
;

-- Permissions

ALTER FUNCTION public.notify_nuevo_proveedor() OWNER TO postgres;
GRANT ALL ON FUNCTION public.notify_nuevo_proveedor() TO postgres;

-- DROP PROCEDURE public.nuevo_documento(int4, varchar, date, int4, int4, int4);

CREATE OR REPLACE PROCEDURE public.nuevo_documento(IN p_tramite_id integer, IN p_documento_codigo character varying, IN p_fecha_documento date, IN p_tipo_id integer, IN p_subtipo_id integer, IN p_origen_id integer)
 LANGUAGE plpgsql
AS $procedure$
begin
	insert into documento (tramite_id, codigo_final, fecha_documento, tipo_documento_id, subtipo_documento_id, documento_origen_id, es_manual)
	values
	(p_tramite_id, p_documento_codigo, p_fecha_documento, p_tipo_id, p_subtipo_id, p_origen_id, true);
end;
$procedure$
;

-- Permissions

ALTER PROCEDURE public.nuevo_documento(int4, varchar, date, int4, int4, int4) OWNER TO postgres;
GRANT ALL ON PROCEDURE public.nuevo_documento(int4, varchar, date, int4, int4, int4) TO postgres;

-- DROP FUNCTION public.nuevo_proveedor(varchar, varchar, varchar, varchar, varchar);

CREATE OR REPLACE FUNCTION public.nuevo_proveedor(p_nombre character varying, p_cedula_ruc character varying, p_canton character varying, p_ciudad character varying, p_provincia character varying)
 RETURNS integer
 LANGUAGE plpgsql
AS $function$
declare
	v_proveedor_id int;
begin
	insert into proveedor (nombre, cedula_ruc, canton, ciudad, provincia) values
	(p_nombre, p_cedula_ruc, p_canton, p_ciudad, p_provincia) 
	returning id into v_proveedor_id;
	return v_proveedor_id;
end;
$function$
;

-- Permissions

ALTER FUNCTION public.nuevo_proveedor(varchar, varchar, varchar, varchar, varchar) OWNER TO postgres;
GRANT ALL ON FUNCTION public.nuevo_proveedor(varchar, varchar, varchar, varchar, varchar) TO postgres;

-- DROP FUNCTION public.prosigue_documento(bool, int4);

CREATE OR REPLACE FUNCTION public.prosigue_documento(p_prosigue boolean, p_tramite_id integer)
 RETURNS integer
 LANGUAGE plpgsql
AS $function$

begin
	update tramite set prosigue = p_prosigue where id = p_tramite_id;
	return p_tramite_id;
end;
$function$
;

-- Permissions

ALTER FUNCTION public.prosigue_documento(bool, int4) OWNER TO postgres;
GRANT ALL ON FUNCTION public.prosigue_documento(bool, int4) TO postgres;

-- DROP FUNCTION public.prosigue_tramite(bool, int4);

CREATE OR REPLACE FUNCTION public.prosigue_tramite(p_prosigue boolean, p_tramite_id integer)
 RETURNS integer
 LANGUAGE plpgsql
AS $function$

begin
	update tramite set prosigue = p_prosigue where id = p_tramite_id;
	return p_tramite_id;
end;
$function$
;

-- Permissions

ALTER FUNCTION public.prosigue_tramite(bool, int4) OWNER TO postgres;
GRANT ALL ON FUNCTION public.prosigue_tramite(bool, int4) TO postgres;

-- DROP FUNCTION public.set_limit(float4);

CREATE OR REPLACE FUNCTION public.set_limit(real)
 RETURNS real
 LANGUAGE c
 STRICT
AS '$libdir/pg_trgm', $function$set_limit$function$
;

-- Permissions

ALTER FUNCTION public.set_limit(float4) OWNER TO postgres;
GRANT ALL ON FUNCTION public.set_limit(float4) TO postgres;

-- DROP FUNCTION public.show_limit();

CREATE OR REPLACE FUNCTION public.show_limit()
 RETURNS real
 LANGUAGE c
 STABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$show_limit$function$
;

-- Permissions

ALTER FUNCTION public.show_limit() OWNER TO postgres;
GRANT ALL ON FUNCTION public.show_limit() TO postgres;

-- DROP FUNCTION public.show_trgm(text);

CREATE OR REPLACE FUNCTION public.show_trgm(text)
 RETURNS text[]
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$show_trgm$function$
;

-- Permissions

ALTER FUNCTION public.show_trgm(text) OWNER TO postgres;
GRANT ALL ON FUNCTION public.show_trgm(text) TO postgres;

-- DROP FUNCTION public.similarity(text, text);

CREATE OR REPLACE FUNCTION public.similarity(text, text)
 RETURNS real
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$similarity$function$
;

-- Permissions

ALTER FUNCTION public.similarity(text, text) OWNER TO postgres;
GRANT ALL ON FUNCTION public.similarity(text, text) TO postgres;

-- DROP FUNCTION public.similarity_dist(text, text);

CREATE OR REPLACE FUNCTION public.similarity_dist(text, text)
 RETURNS real
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$similarity_dist$function$
;

-- Permissions

ALTER FUNCTION public.similarity_dist(text, text) OWNER TO postgres;
GRANT ALL ON FUNCTION public.similarity_dist(text, text) TO postgres;

-- DROP FUNCTION public.similarity_op(text, text);

CREATE OR REPLACE FUNCTION public.similarity_op(text, text)
 RETURNS boolean
 LANGUAGE c
 STABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$similarity_op$function$
;

-- Permissions

ALTER FUNCTION public.similarity_op(text, text) OWNER TO postgres;
GRANT ALL ON FUNCTION public.similarity_op(text, text) TO postgres;

-- DROP FUNCTION public.strict_word_similarity(text, text);

CREATE OR REPLACE FUNCTION public.strict_word_similarity(text, text)
 RETURNS real
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$strict_word_similarity$function$
;

-- Permissions

ALTER FUNCTION public.strict_word_similarity(text, text) OWNER TO postgres;
GRANT ALL ON FUNCTION public.strict_word_similarity(text, text) TO postgres;

-- DROP FUNCTION public.strict_word_similarity_commutator_op(text, text);

CREATE OR REPLACE FUNCTION public.strict_word_similarity_commutator_op(text, text)
 RETURNS boolean
 LANGUAGE c
 STABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$strict_word_similarity_commutator_op$function$
;

-- Permissions

ALTER FUNCTION public.strict_word_similarity_commutator_op(text, text) OWNER TO postgres;
GRANT ALL ON FUNCTION public.strict_word_similarity_commutator_op(text, text) TO postgres;

-- DROP FUNCTION public.strict_word_similarity_dist_commutator_op(text, text);

CREATE OR REPLACE FUNCTION public.strict_word_similarity_dist_commutator_op(text, text)
 RETURNS real
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$strict_word_similarity_dist_commutator_op$function$
;

-- Permissions

ALTER FUNCTION public.strict_word_similarity_dist_commutator_op(text, text) OWNER TO postgres;
GRANT ALL ON FUNCTION public.strict_word_similarity_dist_commutator_op(text, text) TO postgres;

-- DROP FUNCTION public.strict_word_similarity_dist_op(text, text);

CREATE OR REPLACE FUNCTION public.strict_word_similarity_dist_op(text, text)
 RETURNS real
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$strict_word_similarity_dist_op$function$
;

-- Permissions

ALTER FUNCTION public.strict_word_similarity_dist_op(text, text) OWNER TO postgres;
GRANT ALL ON FUNCTION public.strict_word_similarity_dist_op(text, text) TO postgres;

-- DROP FUNCTION public.strict_word_similarity_op(text, text);

CREATE OR REPLACE FUNCTION public.strict_word_similarity_op(text, text)
 RETURNS boolean
 LANGUAGE c
 STABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$strict_word_similarity_op$function$
;

-- Permissions

ALTER FUNCTION public.strict_word_similarity_op(text, text) OWNER TO postgres;
GRANT ALL ON FUNCTION public.strict_word_similarity_op(text, text) TO postgres;

-- DROP FUNCTION public.sumar_dias_laborables(date, int4);

CREATE OR REPLACE FUNCTION public.sumar_dias_laborables(fecha_inicio date, dias integer)
 RETURNS date
 LANGUAGE sql
AS $function$
SELECT fecha
FROM (
    SELECT g::date AS fecha
    FROM generate_series(
        fecha_inicio + INTERVAL '1 day',
        fecha_inicio + INTERVAL '365 days',
        INTERVAL '1 day'
    ) g
    WHERE EXTRACT(DOW FROM g) NOT IN (0,6)
      AND NOT EXISTS (
          SELECT 1
          FROM feriados f
          WHERE f.fecha = g::date
      )
    ORDER BY g
    LIMIT dias
) sub
ORDER BY fecha DESC
LIMIT 1;
$function$
;

-- Permissions

ALTER FUNCTION public.sumar_dias_laborables(date, int4) OWNER TO postgres;
GRANT ALL ON FUNCTION public.sumar_dias_laborables(date, int4) TO postgres;

-- DROP FUNCTION public.word_similarity(text, text);

CREATE OR REPLACE FUNCTION public.word_similarity(text, text)
 RETURNS real
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$word_similarity$function$
;

-- Permissions

ALTER FUNCTION public.word_similarity(text, text) OWNER TO postgres;
GRANT ALL ON FUNCTION public.word_similarity(text, text) TO postgres;

-- DROP FUNCTION public.word_similarity_commutator_op(text, text);

CREATE OR REPLACE FUNCTION public.word_similarity_commutator_op(text, text)
 RETURNS boolean
 LANGUAGE c
 STABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$word_similarity_commutator_op$function$
;

-- Permissions

ALTER FUNCTION public.word_similarity_commutator_op(text, text) OWNER TO postgres;
GRANT ALL ON FUNCTION public.word_similarity_commutator_op(text, text) TO postgres;

-- DROP FUNCTION public.word_similarity_dist_commutator_op(text, text);

CREATE OR REPLACE FUNCTION public.word_similarity_dist_commutator_op(text, text)
 RETURNS real
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$word_similarity_dist_commutator_op$function$
;

-- Permissions

ALTER FUNCTION public.word_similarity_dist_commutator_op(text, text) OWNER TO postgres;
GRANT ALL ON FUNCTION public.word_similarity_dist_commutator_op(text, text) TO postgres;

-- DROP FUNCTION public.word_similarity_dist_op(text, text);

CREATE OR REPLACE FUNCTION public.word_similarity_dist_op(text, text)
 RETURNS real
 LANGUAGE c
 IMMUTABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$word_similarity_dist_op$function$
;

-- Permissions

ALTER FUNCTION public.word_similarity_dist_op(text, text) OWNER TO postgres;
GRANT ALL ON FUNCTION public.word_similarity_dist_op(text, text) TO postgres;

-- DROP FUNCTION public.word_similarity_op(text, text);

CREATE OR REPLACE FUNCTION public.word_similarity_op(text, text)
 RETURNS boolean
 LANGUAGE c
 STABLE PARALLEL SAFE STRICT
AS '$libdir/pg_trgm', $function$word_similarity_op$function$
;

-- Permissions

ALTER FUNCTION public.word_similarity_op(text, text) OWNER TO postgres;
GRANT ALL ON FUNCTION public.word_similarity_op(text, text) TO postgres;


-- Permissions

GRANT ALL ON SCHEMA public TO pg_database_owner;
GRANT USAGE ON SCHEMA public TO public;
GRANT USAGE ON SCHEMA public TO user_app;