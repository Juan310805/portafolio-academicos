// server.js — API REST con Node.js + Express + SQLite (sql.js)
// Endpoint: GET /api/tareas  →  retorna todas las tareas desde la BD
//
// Instrucciones de uso:
//   1. npm install          (instala dependencias de package.json)
//   2. node setup_db.js     (crea tareas.db con los datos del semestre)
//   3. node server.js       (inicia el servidor en http://localhost:3000)

const express = require("express");
const cors    = require("cors");
const initSqlJs = require("sql.js");
const PORT = process.env.PORT || 3000;
const fs        = require("fs");
const path    = require("path");

const app  = express();


// ── Middlewares ──────────────────────────────────────────────────────────────
app.use(cors());           // Permite peticiones desde el Frontend
app.use(express.json());
app.use(express.static(path.join(__dirname)));

// ── Cargar la base de datos SQLite ───────────────────────────────────────────
let db;

async function loadDatabase() {
  const SQL    = await initSqlJs();
  const dbPath = path.join(__dirname, "tareas.db");

  if (!fs.existsSync(dbPath)) {
    console.error("❌ No se encontró tareas.db. Ejecuta primero: node setup_db.js");
    process.exit(1);
  }

  const fileBuffer = fs.readFileSync(dbPath);
  db = new SQL.Database(fileBuffer);
  console.log("✅ Base de datos SQLite cargada correctamente.");
}

// ── Endpoint GET /api/tareas ─────────────────────────────────────────────────
app.get("/api/tareas", (req, res) => {
  try {
    const result = db.exec("SELECT id, titulo, url FROM tareas ORDER BY id LIMIT 3");

  
    if (!result || result.length === 0) {
      return res.json([]);
    }

    // Convertir formato sql.js [{columns, values}] → array de objetos
    const columns = result[0].columns;           // ["id", "titulo", "url"]
    const rows    = result[0].values;            // [[1, "Tarea 1", "http://..."], ...]

    const tareas = rows.map((row) => {
      const obj = {};
      columns.forEach((col, i) => { obj[col] = row[i]; });
      return obj;
    });

    res.json({
      ok: true,
      total: tareas.length,
      data: tareas,
    });
  } catch (err) {
    console.error("Error al consultar la BD:", err.message);
    res.status(500).json({ ok: false, error: "Error interno del servidor" });
  }
});

// ── Ruta raíz (verificación rápida) ─────────────────────────────────────────
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

// ── Iniciar servidor ─────────────────────────────────────────────────────────
loadDatabase().then(() => {
  app.listen(PORT, () => {
    console.log(` Servidor corriendo en http://portafolio_moreno_loera.onrender.com/tareas:${PORT}`);
    console.log(`   Endpoint: GET http://portafolio_moreno_loera.onrender.com/tareas:${PORT}/api/tareas`);
  });
});

