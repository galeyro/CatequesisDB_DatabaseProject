/* ENTREGABLE 1: Script de Extracción y Transformación (ETL)
   OBJETIVO: Generar JSONs formateados desde SQL Server compatibles con el esquema NoSQL diseñado.
   AUTOR: [Tu Nombre]
*/

USE [CatequesisDB]
GO

-- =================================================================================
-- 1. EXTRACCIÓN DE CATEQUISTAS (Fusión de Login + Perfil)
-- =================================================================================
SELECT 
    -- Datos de Cuenta (Tabla Usuario)
    u.username,
    u.password_hash AS [passwordHash],
    u.esta_activo AS [esActivo],
    u.rol AS [rol],
    
    -- Datos Personales Embebidos (Tabla Catequista)
    c.nombre,
    c.apellido,
    c.telefono,
    c.email,
    c.es_joven_apoyo AS [esJovenApoyo]

FROM [dbo].[Usuario] u
INNER JOIN [dbo].[Catequista] c ON c.Usuario_id_user = u.id_user
FOR JSON PATH, ROOT('catequistas');
GO


-- =================================================================================
-- 2. EXTRACCIÓN DE ALUMNOS (Con Historial de Sacramentos Embebido)
-- =================================================================================
SELECT 
    -- Datos Raíz
    a.id_alumno AS [idSql],
    a.inscripcion_activa AS [esInscripcionActiva],

    -- Objeto Datos Personales
    JSON_QUERY((
        SELECT 
            a.nombre,
            a.apellido,
            a.fecha_nacimiento AS [fechaNacimiento],
            a.lugar_nacimiento AS [lugarNacimiento],
            a.direccion,
            a.telefono,
            a.info_escolar AS [infoEscolar],
            a.info_salud AS [infoSalud]
        FOR JSON PATH, WITHOUT_ARRAY_WRAPPER
    )) AS [datosPersonales],

    -- Array de Representantes
    (
        SELECT 
            r.nombre,
            r.apellido,
            r.telefono,
            r.email,
            r.ocupacion
        FROM [dbo].[Representante] r
        INNER JOIN [dbo].[Alumno_Representante] ar ON r.id_rep = ar.id_rep
        WHERE ar.id_alumno = a.id_alumno
        FOR JSON PATH
    ) AS [representantes],

    -- Array Historial Sacramentos
    (
        SELECT 
            s.nombre_sacramento AS [nombreSacramento], -- Guardamos el nombre directo (Desnormalizado)
            sr.fecha_realizacion AS [fechaRealizacion],
            sr.lugar,
            
            -- Certificado anidado
            JSON_QUERY((
                SELECT 
                    doc.codigo_unico AS [id],
                    doc.emitido_por AS [emitidoPor],
                    doc.fecha_emision AS [fecha]
                FROM [dbo].[Documento] doc
                WHERE doc.id_sacramento_realizado = sr.id
                FOR JSON PATH, WITHOUT_ARRAY_WRAPPER
            )) AS [documentos]

        FROM [dbo].[Sacramento_Realizado] sr
        INNER JOIN [dbo].[Sacramento] s ON sr.id_sacramento = s.id_sacramento
        WHERE sr.id_alumno = a.id_alumno
        FOR JSON PATH
    ) AS [historialSacramentos]

FROM [dbo].[Alumno] a
FOR JSON PATH, ROOT('alumnos');
GO


-- =================================================================================
-- 3. EXTRACCIÓN DE GRUPOS (Con Catequistas, Alumnos y Asistencia anidados)
-- =================================================================================
SELECT 
    g.id_grupo AS [idSql],

    -- Objeto Datos Generales (Absorbiendo Catálogos de Nivel, Periodo y Parroquia)
    JSON_QUERY((
        SELECT 
            g.nombre_grupo AS [nombreGrupo],
            p.nombre_periodo AS [nombrePeriodo],
            n.nombre_nivel AS [nombreNivel],
            pq.nombre_parroquia AS [nombreParroquia],
            pq.direccion AS [direccionParroquia]
        FROM [dbo].[Periodo] p, [dbo].[Nivel] n, [dbo].[Parroquia] pq
        WHERE g.id_periodo = p.id_periodo 
          AND g.id_nivel = n.id_nivel 
          AND g.id_parroquia = pq.id_parroquia
        FOR JSON PATH, WITHOUT_ARRAY_WRAPPER
    )) AS [datosGenerales],

    -- Array de Catequistas
    (
        SELECT 
            c.id_catequista AS [idCatequista], -- Referencia para futura relación
            (c.nombre + ' ' + c.apellido) AS [nombreCompleto]
        FROM [dbo].[Grupo_Catequista] gc
        INNER JOIN [dbo].[Catequista] c ON gc.id_catequista = c.id_catequista
        WHERE gc.id_grupo = g.id_grupo
        FOR JSON PATH
    ) AS [catequistas],

    -- Array de Alumnos Inscritos (Snapshot)
    (
        SELECT 
            al.id_alumno AS [idAlumno],
            (al.nombre + ' ' + al.apellido) AS [nombreCompleto],
            i.estado AS [estadoInscripcion],
            
            -- Padrino anidado
            JSON_QUERY((
                SELECT pad.nombre, pad.apellido, pad.telefono
                FROM [dbo].[Padrino] pad
                WHERE pad.id_inscripcion = i.id_inscripcion
                FOR JSON PATH, WITHOUT_ARRAY_WRAPPER
            )) AS [padrino]

        FROM [dbo].[Inscripcion] i
        INNER JOIN [dbo].[Alumno] al ON i.id_alumno = al.id_alumno
        WHERE i.id_grupo = g.id_grupo
        FOR JSON PATH
    ) AS [alumnosInscritos],

    -- Array de Asistencias (Agrupado por Fecha - Lógica Compleja)
    (
        SELECT 
            asis_group.fecha AS [fecha],
            asis_group.tema AS [tema],
            (
                SELECT 
                    detalle.id_alumno AS [idAlumno],
                    detalle.es_presente AS [esPresente]
                FROM [dbo].[Asistencia] detalle
                WHERE detalle.id_grupo = g.id_grupo 
                  AND detalle.fecha = asis_group.fecha
                FOR JSON PATH
            ) AS [detalle]
        FROM (
            SELECT DISTINCT fecha, tema 
            FROM [dbo].[Asistencia] 
            WHERE id_grupo = g.id_grupo
        ) asis_group
        FOR JSON PATH
    ) AS [asistencias]

FROM [dbo].[Grupo] g
FOR JSON PATH, ROOT('grupos');
GO