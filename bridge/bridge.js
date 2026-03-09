const WebSocket = require("ws");
const net = require("net");

// CONFIG
const WS_PORT = 8080;      // Puerto WebSocket para Flutter
const TCP_HOST = "localhost";
const TCP_PORT = 5050;     // Tu servidor TCP

// Servidor WebSocket
const wss = new WebSocket.Server({ port: WS_PORT });

console.log(`[BRIDGE] WebSocket listening on ws://localhost:${WS_PORT}`);

wss.on("connection", (ws) => {
    console.log("[BRIDGE] WebSocket client connected");

    // Crear conexión TCP hacia tu servidor
    const tcpClient = new net.Socket();
    tcpClient.connect(TCP_PORT, TCP_HOST, () => {
        console.log("[BRIDGE] Connected to TCP server");
    });

    // Cuando Flutter envía un mensaje → reenviar al TCP
    ws.on("message", (msg) => {
        console.log("[BRIDGE] WS → TCP:", msg.toString());
        tcpClient.write(msg);
    });

    // Cuando el servidor TCP responde → reenviar al WebSocket
    tcpClient.on("data", (data) => {
        console.log("[BRIDGE] TCP → WS:", data.toString());
        ws.send(data.toString());
    });

    // Manejo de desconexión
    ws.on("close", () => {
        console.log("[BRIDGE] WebSocket client disconnected");
        tcpClient.destroy();
    });

    tcpClient.on("close", () => {
        console.log("[BRIDGE] TCP connection closed");
        ws.close();
    });
});