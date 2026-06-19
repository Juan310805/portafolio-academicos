// setup_db.js — Crea la base de datos SQLite con las tareas del semestre
const initSqlJs = require("sql.js");
const fs = require("fs");
const path = require("path");

async function createDatabase() {
  const SQL = await initSqlJs();
  const db = new SQL.Database();

  // Crear tabla tareas
  db.run(`
    CREATE TABLE IF NOT EXISTS tareas (
      id      INTEGER PRIMARY KEY AUTOINCREMENT,
      titulo  TEXT NOT NULL,
      url     TEXT NOT NULL
    )
  `);

  // Insertar tareas del semestre
  const tareas = [
    {
      titulo: "Tarea 1 — Página HTML de presentación personal (CV Web v.1)",
      url: "https://juan-moreno.github.io/tareas/Tarea%201/index.html",
    },
    {
      titulo: "Tarea 2 — Servidor Node.js/Express: endpoints HTTP y conectividad BD",
      url: "https://juan-moreno.github.io/tareas/tarea2/index.html",
    },
    {
      titulo: "Tarea 3 — Simulación de dados: distribución aleatoria con HTML/JS",
      url: "https://juan-moreno.github.io/tareas/tarea3/index.html",
    },
    
  ];

  const stmt = db.prepare("INSERT INTO tareas (titulo, url) VALUES (?, ?)");
  for (const t of tareas) {
    stmt.run([t.titulo, t.url]);
  }
  stmt.free();

  // Guardar el archivo .db
  const dbBuffer = Buffer.from(db.export());
  const dbPath = path.join(__dirname, "tareas.db");
  fs.writeFileSync(dbPath, dbBuffer);
  db.close();

  console.log(`✅ Base de datos creada en: ${dbPath}`);
  console.log(`   Registros insertados: ${tareas.length}`);
}

createDatabase().catch(console.error);
