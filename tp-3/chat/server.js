const WebSocket = require('ws');
const crypto = require('crypto');
const express = require('express');
const http = require('http');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

// Clave de cifrado simétrica (clave compartida)
const secret = 'my_secret_key_12345';

// Funciones para cifrar y descifrar mensajes
function encryptMessage(message) {
    const cipher = crypto.createCipher('aes256', secret);
    let encrypted = cipher.update(message, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    return encrypted;
}

function decryptMessage(encryptedMessage) {
    const decipher = crypto.createDecipher('aes256', secret);
    let decrypted = decipher.update(encryptedMessage, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    return decrypted;
}

// Manejar conexiones WebSocket
wss.on('connection', (ws) => {
    console.log('Nuevo cliente conectado');

    ws.on('message', (message) => {
        console.log('Mensaje recibido (cifrado):', message);
        const decryptedMessage = decryptMessage(message);
        console.log('Mensaje descifrado:', decryptedMessage);

        // Enviar el mensaje cifrado a todos los clientes
        const encryptedResponse = encryptMessage(decryptedMessage);
        wss.clients.forEach((client) => {
            if (client !== ws && client.readyState === WebSocket.OPEN) {
                client.send(encryptedResponse);
            }
        });
    });

    ws.send(encryptMessage('¡Bienvenido al chat seguro!'));
});

// Frontend estático
app.use(express.static('public'));

server.listen(3000, () => {
    console.log('Servidor en ejecución en http://localhost:8080');
});
