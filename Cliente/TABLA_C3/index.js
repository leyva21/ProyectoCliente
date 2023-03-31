const express = require('express');
const mysql = require('mysql2');
const ejs = require('ejs');

const app = express();
const port = 3000;

// Configurar la conexión a la base de datos
const db = mysql.createConnection({
    user: 'root',
    password: 'pepedrako123',
    host: 'localhost',
    database: 'cliente'
});

// Conectar a la base de datos
db.connect((err) => {
    if (err) {
        console.error('Error al conectar a la base de datos:', err);
        return;
    }

    console.log('Conexión exitosa a la base de datos.');
});

// Configurar la plantilla EJS como motor de vistas
app.set('view engine', 'ejs');

// Definir la ruta para mostrar la tabla de datos
app.get('/', (req, res) => {

    //let ip = req.connection.remoteAddress;

    // Si la dirección IP es una dirección IPv6 con notación "::ffff:"
    /*if (ip.substr(0, 7) === '::ffff:') {
      ip = ip.substr(7); // Extraer la parte de la dirección IPv4
    }
  
    const sql = `INSERT INTO cliente.ip_addresses (ip) VALUES ('${ip}')`;
  
    db.query(sql, (err, result) => {
      if (err) throw err;
      console.log(`Dirección IP ${ip} guardada en la base de datos`);
    });*/
  
    
    // Obtener los datos de la tabla traffic_data
    db.promise().query('SELECT * FROM traffic_data')
        .then(([rows, fields]) => {
            res.render('index', { trafficData: rows });
        })
        .catch((err) => {
            console.log(err);
            res.render('index', { trafficData: [] });
        });
});

// Iniciar el servidor
app.listen(port, () => {
    console.log(`Servidor iniciado en el puerto ${port}.`);
});
