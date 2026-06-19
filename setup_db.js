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
  // Asegúrate de que las URLs ahora apunten a la carpeta 'tareas'
  const tareas = [
  {
    titulo: "Tarea 1 — Simulación de juego de dados",
    url: "https://github.com/Juan310805/portafolio-academicos/blob/main/tareas/tarea1/Juegos%20de%20Dados%20(1).html",
  },
  {
    titulo: "Tarea 2 — Servidor Node.js/Express",
    url: "https://github.com/Juan310805/portafolio-academicos/blob/main/tareas/tarea2/servidor.js",
  },
  {
    titulo: "Tarea 3 — Software Engineering Visualization Tool",
    url: "https://github.com/Juan310805/portafolio-academicos/blob/main/tareas/tarea3/main_SoftEngViz.py",
  }
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
