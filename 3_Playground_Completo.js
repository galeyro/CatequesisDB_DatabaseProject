/* global use, db */
// MongoDB Playground
// To disable this template go to Settings | MongoDB | Use Default Template For Playground.
// Make sure you are connected to enable completions and to be able to run a playground.
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.
// The result of the last command run in a playground is shown on the results panel.
// By default the first 20 documents will be returned with a cursor.
// Use 'console.log()' to print to the debug output.
// For more documentation on playgrounds please refer to
// https://www.mongodb.com/docs/mongodb-vscode/playgrounds/

// 1. CONFIGURACIÓN E INICIALIZACIÓN
use("CatequesisDB");

// Limpiamos colecciones previas para asegurar pruebas limpias
db.catequistas.drop();
db.alumnos.drop();
db.grupos.drop();

// =============================================================
// 2. INSERCIÓN DE DATOS (CREATE)
// =============================================================

// --- A. Insertar CATEQUISTAS ---
// Guardamos en variables para reusar sus IDs automáticamente
var cat1 = db.catequistas.insertOne({
    username: "soraya.m",
    passwordHash: "sha256_hashed_pwd_123",
    esActivo: true,
    rol: "Catequista",
    datosPersonales: {
        nombre: "Soraya",
        apellido: "Martinez",
        telefono: "0991234567",
        email: "soraya@mail.com",
        esJovenApoyo: false,
    },
});

var cat2 = db.catequistas.insertOne({
    username: "juan.joven",
    passwordHash: "sha256_hashed_pwd_456",
    esActivo: true,
    rol: "Apoyo",
    datosPersonales: {
        nombre: "Juan",
        apellido: "Lopez",
        esJovenApoyo: true,
    },
});

// --- B. Insertar ALUMNOS ---
var alum1 = db.alumnos.insertOne({
    idSql: 101,
    esInscripcionActiva: true,
    datosPersonales: {
        nombre: "Carlitos",
        apellido: "Perez",
        fechaNacimiento: new Date("2015-05-20T00:00:00Z"),
        lugarNacimiento: "Quito",
        direccion: "Av. Amazonas 123",
        telefono: "022222222",
        infoEscolar: "Escuela Sucre",
        infoSalud: "Alergia al maní",
    },
    representantes: [
        {
            id: 50,
            nombre: "Maria",
            apellido: "Gomez",
            telefono: "099999999",
            email: "maria@mail.com",
            ocupacion: "Ingeniera",
        },
    ],
    historialSacramentos: [
        {
            nombreSacramento: "Bautismo",
            fechaRealizacion: new Date("2016-01-15T00:00:00Z"),
            lugar: "Parroquia La Dolorosa",
            comentarios: "Todo correcto",
            documentos: {
                id: 101,
                nombreAlumno: "Carlitos Perez",
                fecha: new Date("2016-02-01T00:00:00Z"),
                emitidoPor: "P. Juan",
            },
        },
    ],
});

var alum2 = db.alumnos.insertOne({
    idSql: 102,
    esInscripcionActiva: true,
    datosPersonales: {
        nombre: "Anita",
        apellido: "Sosa",
        fechaNacimiento: new Date("2015-08-10T00:00:00Z"),
        infoSalud: "Ninguna",
    },
    representantes: [],
    historialSacramentos: [],
});

// --- C. Insertar GRUPOS ---
db.grupos.insertOne({
    datosGenerales: {
        nombreGrupo: "Primera Comunión - Sábados",
        periodo: {
            anio: "2025-2026",
            fechaInicio: new Date("2025-09-01T00:00:00Z"),
            fechaFin: new Date("2026-06-30T00:00:00Z"),
        },
        nivel: {
            nombre: "Nivel 1",
            orden: 1,
            sacramentoObjetivo: "Eucaristía",
        },
        parroquia: {
            nombre: "San Francisco",
            direccion: "Centro Histórico",
            telefono: "022555555",
        },
    },
    catequistas: [
        {
            idCatequista: cat1.insertedId, // Vinculación automática
            nombreCompleto: "Soraya Martinez",
        },
        {
            idCatequista: cat2.insertedId,
            nombreCompleto: "Juan Lopez",
        },
    ],
    alumnosInscritos: [
        {
            idAlumno: alum1.insertedId, // Vinculación automática
            nombreCompleto: "Carlitos Perez",
            estadoInscripcion: "Confirmado",
            padrino: {
                nombre: "Pedro",
                apellido: "Ramirez",
                telefono: "091111111",
            },
        },
        {
            idAlumno: alum2.insertedId,
            nombreCompleto: "Anita Sosa",
            estadoInscripcion: "Pendiente",
        },
    ],
    asistencias: [
        {
            fecha: new Date("2026-03-01T00:00:00Z"),
            tema: "La Creación",
            detalle: [
                { idAlumno: alum1.insertedId, esPresente: true },
                { idAlumno: alum2.insertedId, esPresente: false },
            ],
        },
    ],
});

print(">>> Datos Insertados Correctamente (Create) <<<");

// =============================================================
// 3. OPERACIONES CRUD Y BÚSQUEDAS
// =============================================================

// --- READ (Find Simple) ---
// Regla de Negocio: Buscar alumnos con alertas de salud
print("\n--- Resultado: Alumnos con Alergias ---");
var alumnosAlergia = db.alumnos.find({
    "datosPersonales.infoSalud": { $ne: "Ninguna" },
});
printjson(alumnosAlergia.toArray());

// --- UPDATE ---
// Escenario: Actualizar el teléfono de la catequista Soraya
db.catequistas.updateOne(
    { username: "soraya.m" },
    { $set: { "datosPersonales.telefono": "0990000000" } }
);
print("\n>>> Update Realizado (Teléfono Soraya Actualizado) <<<");

// --- DELETE ---
// Escenario: Eliminar un registro de prueba (borramos a Anita)
db.alumnos.deleteOne({ "datosPersonales.nombre": "Anita" });
print("\n>>> Delete Ejecutado (Anita eliminada) <<<");

// --- BÚSQUEDA AVANZADA (LOOKUP / AGGREGATION) ---
// Regla: Obtener el email del catequista cruzando la colección Grupos con Catequistas
print("\n--- Resultado: Emails de Catequistas por Grupo (Lookup) ---");
var reporteCatequistas = db.grupos.aggregate([
    {
        $lookup: {
            from: "catequistas",
            localField: "catequistas.idCatequista", // Campo en Grupos
            foreignField: "_id", // Campo en Catequistas
            as: "info_detallada_catequistas",
        },
    },
    {
        $project: {
            "datosGenerales.nombreGrupo": 1,
            "info_detallada_catequistas.datosPersonales.email": 1,
        },
    },
]);
printjson(reporteCatequistas.toArray());

// --- ÍNDICES ---
// Optimización: Crear índice para buscar rápido por Apellido
db.alumnos.createIndex({ "datosPersonales.apellido": 1 });
print("\n>>> Índice creado en Apellido <<<");
