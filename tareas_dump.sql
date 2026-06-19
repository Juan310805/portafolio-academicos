-- ============================================================
--  tareas_dump.sql  —  Exportación de la base de datos SQLite
--  Proyecto: Portafolio Académico — Ingeniería de Software
--  Alumno:   Juan Francisco Moreno Loera  |  Matrícula: 24040318
--  Grupo:    J-305
-- ============================================================

-- Crear tabla
CREATE TABLE IF NOT EXISTS tareas (
  id      INTEGER PRIMARY KEY AUTOINCREMENT,
  titulo  TEXT NOT NULL,
  url     TEXT NOT NULL
);

-- Insertar registros del semestre
INSERT INTO tareas (id, titulo, url) VALUES
  (1, 'Tarea 1 — Página HTML de presentación personal (CV Web v.1)',
      'https://juan-moreno.github.io/tareas/tarea1/index.html'),

  (2, 'Tarea 2 — Servidor Node.js/Express: endpoints HTTP y conectividad BD',
      'https://juan-moreno.github.io/tareas/tarea2/index.html'),

  (3, 'Tarea 3 — Simulación de dados: distribución aleatoria con HTML/JS',
      'https://juan-moreno.github.io/tareas/tarea3/index.html'),

  (4, 'Tarea 4 — Indicadores de calidad de software (CRUD + SVG + PDF)',
      'https://juan-moreno.github.io/tareas/tarea4/index.html'),

  (5, 'Tarea 5 — Modelos de colas y simulación (M/M/1, M/M/c, DES)',
      'https://juan-moreno.github.io/tareas/tarea5/index.html');

-- Verificar
SELECT id, titulo, url FROM tareas;
