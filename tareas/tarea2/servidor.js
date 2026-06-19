// servidor.js
// Servidor web con Express que expone dos endpoints:
//   GET /         → responde con texto plano
//   GET /info     → responde con un objeto JSON

const express = require('express');
const app = express();
const PORT = 3000;

// Endpoint 1: texto plano
app.get('/', (req, res) => {
  res.send('¡Hola! Este es el servidor de Juan. Bienvenido a la API.');
});

// Endpoint 2: estructura JSON
app.get('/info', (req, res) => {
  res.json({
    servidor: 'API de ejemplo',
    version: '1.0.0',
    autor: 'Juan',
    descripcion: 'Servidor construido con Node.js y Express',
    endpoints: [
      { ruta: '/',      metodo: 'GET', respuesta: 'texto plano' },
      { ruta: '/info',  metodo: 'GET', respuesta: 'JSON'        }
    ]
  });
});

// Iniciar el servidor
app.listen(PORT, () => {
  console.log(`Servidor corriendo en http://localhost:${PORT}`);
  console.log(`  Texto plano → http://localhost:${PORT}/`);
  console.log(`  JSON        → http://localhost:${PORT}/info`);
});
