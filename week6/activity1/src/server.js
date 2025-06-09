const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const morgan = require('morgan');


const app = express();
const PORT = 3000;
const EXTERNAL_API_URL = 'https://callback-iot.onrender.com/data';

app.use(bodyParser.json());
app.use(morgan('tiny'))

let visualizationData = [];

app.get('/data', async (req, res) => {
    try {
        const response = await axios.get(EXTERNAL_API_URL);
        const data = response.data;
      
        const lastTwo = data.slice(-2);
        
        res.json(lastTwo);
    } catch (error) {
        console.error('Error al obtener datos:', error);
        res.status(500).json({ error: 'Error al obtener datos del endpoint externo' });
    }
});

app.post('/visualize', (req, res) => {
    const newData = req.body;
    
    if (!newData) {
        return res.status(400).json({ error: 'Datos no proporcionados' });
    }
    
    visualizationData.push(newData);
    
    if (visualizationData.length > 10) {
        visualizationData = visualizationData.slice(-10);
    }
    
    res.json({ message: 'Datos recibidos para visualización', data: newData });
});

app.get('/visualize-data', (req, res) => {
    const lastTwo = visualizationData.slice(-2);  
    res.json(lastTwo);
});

app.listen(PORT, () => {
    console.log(`API corriendo en http://localhost:${PORT}`);
});