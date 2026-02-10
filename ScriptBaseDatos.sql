----------------------------------------------------
-- 1. tablas base
----------------------------------------------------

create table unidad (
    id serial primary key,
    codigo varchar(20) not null,
    nombre varchar(150) not null
);

create table proveedor (
    id serial primary key,
    nombre varchar(200) not null,
    ruc varchar(20)
);

create table tramite (
    id serial primary key,
    proveedor_id int not null,
    unidad_id int not null,
    estado varchar(30) not null,
    fecha_creacion date not null default current_date,

    foreign key (proveedor_id) references proveedor(id),
    foreign key (unidad_id) references unidad(id)
);

----------------------------------------------------
-- 2. catalogos de documentos
----------------------------------------------------

create table tipo_documento (
    id serial primary key,
    nombre varchar(100) not null,
    se_numera_en_unidad boolean not null default false,
    requiere_infraccion boolean not null default false
);

create table subtipo_documento (
    id serial primary key,
    tipo_documento_id int not null,
    nombre varchar(120) not null,

    foreign key (tipo_documento_id) 
        references tipo_documento(id)
);

----------------------------------------------------
-- 3. documento (tabla central)
----------------------------------------------------

create table documento (
    id serial primary key,

    tramite_id int not null,
    tipo_documento_id int not null,
    subtipo_documento_id int,

    documento_origen_id int,

    codigo_final varchar(60) not null,
    es_manual boolean not null default false,

    fecha_documento date not null default current_date,

    foreign key (tramite_id) 
        references tramite(id),

    foreign key (tipo_documento_id) 
        references tipo_documento(id),

    foreign key (subtipo_documento_id) 
        references subtipo_documento(id),

    foreign key (documento_origen_id) 
        references documento(id),

    constraint uq_codigo_documento 
        unique (codigo_final)
);

alter table documento
alter column fecha_documento type timestamp(0);

alter table documento
alter column fecha_documento set default now();

----------------------------------------------------
-- 4. infracciones
----------------------------------------------------

create table infraccion (
    id serial primary key,
    codigo_infraccion varchar(30) not null,
    descripcion varchar(250)
);

create table documento_infraccion (
    documento_id int not null,
    infraccion_id int not null,

    primary key (documento_id, infraccion_id),

    foreign key (documento_id) 
        references documento(id),

    foreign key (infraccion_id) 
        references infraccion(id)
);

----------------------------------------------------
-- 5. numeracion
----------------------------------------------------

create table plantilla_codigo (
    id serial primary key,
    tipo_documento_id int not null,
    formato varchar(100) not null,
    reinicio varchar(20) not null,

    foreign key (tipo_documento_id) 
        references tipo_documento(id)
);

create table secuencia_documento (
    id serial primary key,
    plantilla_id int not null,
    anio int not null,
    ultimo_numero int not null default 0,

    foreign key (plantilla_id) 
        references plantilla_codigo(id)
);

----------------------------------------------------
-- Insercion de Datos
----------------------------------------------------

insert into tipo_documento (nombre, se_numera_en_unidad, requiere_infraccion) values
('MEMORANDO INICIO PAS', false, false),
('PETICION RAZONADA', false, false),
('INFORME TÉCNICO', false, false),
('ACTUACIÓN PREVIA', true, false),
('INFORME DE ACTUACÍON PREVIA', true, false),
('ACTO DE INICIO', true, true),
('PROVIDENCIA', true, false),
('DICATAMEN', true, false),
('RESOLUCION', true, false),
('IMPUTACION', true, false),
('INFORME JURIDICO', true, false);

insert into subtipo_documento (tipo_documento_id, nombre) values
(5, 'CONCLUSIÓN'), -- informe de actuacion previa
(5, 'FINAL'),
(7, 'DE ACTUACIÓN PREVIA'), -- providencia
(7, 'APERTURA'),
(7, 'NOTIFICACIÓN ACTUADO'),
(7, 'CIERRE'),
(7, 'REMITE INFORMES'),
(7, 'OTROS'),
(7, 'EN RESOLUCIÓN'),
(11, 'EN INSTRUCCIÓN'), -- informe juridico
(11, 'PATROCINIO'),
(11, 'OTROS');

insert into plantilla_codigo (tipo_documento_id, formato, reinicio) values
(4, 'AP-{unidad}-{anio}-{sec}', 'anual'),
(5, 'IAP-{unidad}-{anio}-{sec}','anual'),
(6, 'ARCOTEL-{unidad}-AI-{anio}-{sec}', 'anual'),
(7, 'ARCOTEL-{unidad}-PR-{anio}-{sec}', 'anual'),
(8, 'FI-{unidad}-D-{anio}-{sec}', 'anual'),
(9, 'ARCOTEL-{unidad}-RPAS-{anio}-{sec}', 'anual'),
(11, 'IJ-{unidad}-{anio}-{sec}', 'anual');

insert into infraccion (codigo_infraccion) values
	('117, a), 1'), ('117, a), 2'), ('117, a), 3'), ('117, b), 1'), ('117, b), 2'), ('117, b), 3'), ('117, b), 4'),
	('117, b), 5'), ('117, b), 6'), ('117, b), 7'), ('117, b), 8'), ('117, b), 9'), ('117, b), 10'), ('117, b), 11'),
	('117, b), 12'), ('117, b), 13'), ('117, b), 14'), ('117, b), 15'), ('117, b), 16'), ('118, a), 1'), ('118, a), 2'),
	('118, a), 3'), ('118, a), 4'), ('118, a), 5'), ('118, b), 1'), ('118, b), 2'), ('118, b), 3'), ('118, b), 4'),
	('118, b), 5'), ('118, b), 6'), ('118, b), 7'), ('118, b), 8'), ('118, b), 9'), ('118, b), 10'), ('118, b), 11'),
	('118, b), 12'), ('118, b), 13'), ('118, b), 14'), ('118, b), 15'), ('118, b), 16'), ('118, b), 17'), ('118, b), 18'),
	('118, b), 19'), ('118, b), 20'), ('118, b), 21'), ('118, b), 22'), ('118, b), 23'), ('118, b), 24'), ('118, b), 25'),
	('118, b), 26'), ('118, b), 27'), ('118, b), 28'), ('118, b), 29'), ('119, a), 1'), ('119, a), 2'), ('119, a), 3'),
	('119, a), 4'), ('119, b), 1'), ('119, b), 2'), ('119,b), 3'), ('119, b), 4'), ('119, b), 5'), ('120, 1)'),
	('120, 2)'), ('120, 3)'), ('120, 4)'), ('120, 5)'), ('120, 6)'), ('120, 7)');

----------------------------------------------------
-- funcion: generar_codigo_documento
----------------------------------------------------

create or replace function generar_codigo_documento(
    p_tipo_documento int,
    p_unidad_codigo varchar,
    p_anio int
)
returns varchar
language plpgsql
as $$
declare
    v_formato varchar;
    v_plantilla_id int;
    v_secuencia int;
    v_codigo varchar;
begin

    select id, formato
    into v_plantilla_id, v_formato
    from plantilla_codigo
    where tipo_documento_id = p_tipo_documento;

    if v_plantilla_id is null then
        raise exception 'no existe plantilla para este tipo de documento';
    end if;

    select ultimo_numero
    into v_secuencia
    from secuencia_documento
    where plantilla_id = v_plantilla_id
      and anio = p_anio
    for update;

    if v_secuencia is null then

        insert into secuencia_documento
        (plantilla_id, anio, ultimo_numero)
        values
        (v_plantilla_id, p_anio, 1);

        v_secuencia := 1;

    else
        v_secuencia := v_secuencia + 1;

        update secuencia_documento
        set ultimo_numero = v_secuencia
        where plantilla_id = v_plantilla_id
          and anio = p_anio;
    end if;

    v_codigo := v_formato;

    v_codigo := replace(v_codigo, '{unidad}', p_unidad_codigo);
    v_codigo := replace(v_codigo, '{anio}', p_anio::varchar);
    v_codigo := replace(v_codigo, '{sec}', 
                    lpad(v_secuencia::varchar, 4, '0'));

    return v_codigo;

end;
$$;

----------------------------------------------------
-- funcion: crear_documento
----------------------------------------------------

create or replace function crear_documento(
    p_tramite int,
    p_tipo int,
    p_subtipo int,
    p_origen int,
    p_codigo_manual varchar,
    p_unidad varchar
)
returns int
language plpgsql
as $$
declare
    v_codigo varchar;
    v_es_manual boolean;
    v_anio int := extract(year from current_date);
    v_id int;
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

    insert into documento(
        tramite_id,
        tipo_documento_id,
        subtipo_documento_id,
        documento_origen_id,
        codigo_final,
        es_manual
    )
    values (
        p_tramite,
        p_tipo,
        p_subtipo,
        p_origen,
        v_codigo,
        v_es_manual
    )
    returning id into v_id;

    return v_id;

end;
$$;

----------------------------------------------------
-- funcion: agregar_infraccion_a_documento
----------------------------------------------------

create or replace function agregar_infraccion_a_documento(
    p_documento int,
    p_infraccion int
)
returns void
language plpgsql
as $$
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
$$;

----------------------------------------------------
-- view: info de tramites por memo
----------------------------------------------------

drop view v_info_tramite_por_memo;
create view v_info_tramite_por_memo as
select
    p.nombre        as proveedor,
    u.codigo        as unidad,
    t.id 			as tramite,
    t.estado,
    t.fecha_creacion,
    d.id			
from documento d
join tramite t   on d.tramite_id = t.id
join proveedor p on p.id = t.proveedor_id
join unidad u    on u.id = t.unidad_id
where d.tipo_documento_id = 1;

----------------------------------------------------
-- view: listar documentos por tramite
----------------------------------------------------
drop view v_documentos_tramite;
create or replace view v_documentos_tramite as
select
    d.tramite_id,
    td.nombre as tipo,
    st.nombre as subtipo,
    d.codigo_final,
    d.fecha_documento,
    dor.codigo_final as origen,

    (
        select string_agg(i.codigo_infraccion, ', ')
        from documento_infraccion di
        join infraccion i on i.id = di.infraccion_id
        where di.documento_id = d.id
    ) as infracciones,
	td.id as tipo_id,
	st.id as subtipo_id
from documento d
join tipo_documento td on td.id = d.tipo_documento_id
left join subtipo_documento st on st.id = d.subtipo_documento_id
left join documento dor on dor.id = d.documento_origen_id;

----------------------------------------------------
-- view: ver los documento con codigo similar al escrito
----------------------------------------------------

drop view v_busqueda_por_codigo;

create or replace view v_busqueda_por_codigo as
select
    d.id                     as documento_id,
    d.codigo_final,
    d.tramite_id,
	d.tipo_documento_id,
    td.nombre                as tipo,
    st.nombre                as subtipo,
    d.fecha_documento,
    dor.codigo_final		 as origen ,
    (
    	select string_agg(i.codigo_infraccion, ', ')
        from documento_infraccion di
        join infraccion i on i.id = di.infraccion_id
        where di.documento_id = d.id
    ) as infracciones,
    td.id as tipo_id,
	st.id as subtipo_id,

    (
        select m.codigo_final
        from documento m
        where m.tramite_id = d.tramite_id
        and m.tipo_documento_id = 1
        limit 1
    ) as memo_inicio_p

from documento d
join tipo_documento td on td.id = d.tipo_documento_id
left join subtipo_documento st on st.id = d.subtipo_documento_id
left join documento dor on dor.id = d.documento_origen_id;

----------------------------------------------------
-- view: consulta completa
----------------------------------------------------
drop view v_consulta_documentos; 
create or replace view v_consulta_documentos as
select
    d.id,
    d.tramite_id,
    t.id as id_tramite,
    p.nombre as proveedor,
    u.codigo as unidad,

    td.id as tipo_id,
    td.nombre as tipo,

    st.id as subtipo_id,
    st.nombre as subtipo,

    d.codigo_final,
    d.fecha_documento,

    dor.codigo_final as codigo_origen,

    string_agg(i.codigo_infraccion, ', ') as infracciones

from documento d
join tramite t on t.id = d.tramite_id
join proveedor p on p.id = t.proveedor_id
join unidad u on u.id = t.unidad_id

join tipo_documento td on td.id = d.tipo_documento_id
left join subtipo_documento st on st.id = d.subtipo_documento_id

left join documento dor on dor.id = d.documento_origen_id

left join documento_infraccion di on di.documento_id = d.id
left join infraccion i on i.id = di.infraccion_id

group by
    d.id, t.id, p.nombre, u.codigo,
    td.id, td.nombre,
    st.id, st.nombre,
    d.codigo_final, d.fecha_documento,
    dor.codigo_final;

----------------------------------------------------
-- funcion para la consulta
----------------------------------------------------

create or replace  function f_buscar_documentos(
    p_memo int default null,
    p_codigo text default null,
    p_tipo int default null,
    p_subtipo int default null
)
returns table (
    tipo text,
    subtipo text,
    codigo text,
    fecha date,
    origen text,
    infracciones text,
    id int
)
language sql
as $$

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

$$;

----------------------------------------------------
-- view: consultar tramites
----------------------------------------------------

create or replace view v_consulta_tramite as
select
    -- DATOS DEL TRÁMITE
    t.id                as tramite_id,
    p.nombre            as proveedor,
    u.codigo            as unidad,
    t.estado,
    t.fecha_creacion    as fecha_tramite,

    -- MEMO DEL TRÁMITE
    (
        select m.codigo_final
        from documento m
        where m.tramite_id = t.id
        and m.tipo_documento_id = 1
        limit 1
    ) as memo,

    -- DOCUMENTOS
    d.id                as documento_id,
    td.nombre           as tipo,
    st.nombre           as subtipo,
    d.codigo_final,
    d.fecha_documento,
    dor.codigo_final    as codigo_origen,

    string_agg(i.codigo_infraccion, ', ') as infracciones

from tramite t
join proveedor p on p.id = t.proveedor_id
join unidad u    on u.id = t.unidad_id

left join documento d on d.tramite_id = t.id
left join tipo_documento td on td.id = d.tipo_documento_id
left join subtipo_documento st on st.id = d.subtipo_documento_id
left join documento dor on dor.id = d.documento_origen_id

left join documento_infraccion di on di.documento_id = d.id
left join infraccion i on i.id = di.infraccion_id

group by
    t.id, p.nombre, u.codigo, t.estado, t.fecha_creacion,
    d.id, td.nombre, st.nombre,
    d.codigo_final, d.fecha_documento,
    dor.codigo_final;

----------------------------------------------------
-- view: permite la busqueda completa en Consultas
----------------------------------------------------

drop view v_busqueda_avanzada ;
create or replace view v_busqueda_avanzada as
select
    t.id                    as tramite_id,
    p.id                    as proveedor_id,
    p.nombre                as proveedor,
    u.id                    as unidad_id,
    u.codigo                as unidad,

    mem.id                  as memo_id,
    mem.codigo_final        as memo,

    t.fecha_creacion        as fecha_tramite,
    t.estado,

    d.id                    as documento_id,
    td.nombre               as tipo,
    td.id                   as tipo_id,
    sd.nombre               as subtipo,
    sd.id                   as subtipo_id,
    d.codigo_final          as codigo,
    d.fecha_documento       as fecha,

    orig.codigo_final       as origen,

    (
        select string_agg(i.codigo_infraccion, ', ')
        from documento_infraccion di
        join infraccion i on i.id = di.infraccion_id
        where di.documento_id = d.id
    ) as infracciones

from tramite t
join proveedor p on p.id = t.proveedor_id
join unidad u on u.id = t.unidad_id

join documento mem 
     on mem.tramite_id = t.id
    and mem.tipo_documento_id = 1

join documento d 
     on d.tramite_id = t.id

join tipo_documento td 
     on td.id = d.tipo_documento_id

left join subtipo_documento sd 
     on sd.id = d.subtipo_documento_id

left join documento orig 
     on orig.id = d.documento_origen_id

----------------------------------------------------
-- funcion: buscar tramites
----------------------------------------------------

create or replace function f_buscar_tramites(
    p_proveedor text default null,
    p_unidad text default null,

    p_estado text default null,

    p_fecha_desde date default null,
    p_fecha_hasta date default null,

    p_anio int default null,
    p_mes int default null
)
returns table (
    proveedor text,
    unidad text,
    memo text,
    fecha_tramite date,

    tipo text,
    subtipo text,
    codigo text,
    fecha_doc date,
    origen text,
    infracciones text
)
language sql
as $$

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

    (p_proveedor is null or proveedor ilike '%'||p_proveedor||'%')

    and (p_unidad is null or unidad = p_unidad)

    and (p_estado is null or estado = p_estado)

    and (p_fecha_desde is null or fecha_tramite >= p_fecha_desde)
    and (p_fecha_hasta is null or fecha_tramite <= p_fecha_hasta)

    and (p_anio is null or extract(year from fecha_tramite) = p_anio)
    and (p_mes is null or extract(month from fecha_tramite) = p_mes)

order by fecha_tramite desc, fecha_documento;

$$;

----------------------------------------------------
-- index importantes
----------------------------------------------------

create index idx_documento_tramite
on documento(tramite_id);

create index idx_documento_tipo
on documento(tipo_documento_id);

create index idx_documento_subtipo
on documento(subtipo_documento_id);

create index idx_documento_codigo
on documento(codigo_final);

create extension if not exists pg_trgm;

create index idx_documento_codigo_trgm
on documento using gin (codigo_final gin_trgm_ops);

create index idx_tramite_id
on tramite(id);

create index idx_tramite_proveedor
on tramite(proveedor_id);

create index idx_tramite_unidad
on tramite(unidad_id);

----------------------------------------------------
-- Nota: Algunas views y funciones quedaron obsoletas 
--	o remplazadas por otro, pendiente la limieza de la base de datos
----------------------------------------------------

