import socket
import threading
from datetime import datetime
from protocol.messages import decode_message, encode_message
import random

clients = {}   # {conn: username}

HOST = "localhost"
PORT = 5050

def handle_request(message):
    """
    Processes a decoded JSON message and returns a JSON response.
    """
    action = message.get("action")

    if action == "get_info":
        return encode_message("info_response", {
            "service": "Networking Microservice",
            "version": "1.0",
            "status": "running",
            "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
    if action == "echo":
        return encode_message("echo_response", {
            "echo": message["payload"].get("msg", "")
        })
        
    if action == "math":
        op = message["payload"].get("op")
        a = message["payload"].get("a")
        b = message["payload"].get("b")

        # Validación básica
        if a is None or b is None or op is None:
            return encode_message("error", {"msg": "Missing parameters: op, a, b are required"})

        try:
            a = float(a)
            b = float(b)
        except:
            return encode_message("error", {"msg": "Parameters a and b must be numbers"})

        # Operaciones
        if op == "add":
            result = a + b
        elif op == "subtract":
            result = a - b
        elif op == "multiply":
            result = a * b
        elif op == "divide":
            if b == 0:
                return encode_message("error", {"msg": "Division by zero is not allowed"})
            result = a / b
        else:
            return encode_message("error", {"msg": f"Unknown operation '{op}'"})

        return encode_message("math_response", {"result": result})
    
    if action == "get_time":
        return encode_message("time_response", {
            "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
    if action == "reverse_string":
        text = message["payload"].get("text", "")
        reversed_text = text[::-1]  # Reverse string using slicing
        return encode_message("reverse_response", {"reversed": reversed_text})
    
    if action == "uppercase":
        text = message["payload"].get("value") or message["payload"].get("text", "")
        upper = text.upper()
        return encode_message("uppercase_response", {"result": upper})

    if action == "read_file":
        filename = message["payload"].get("filename", "")

        try:
            with open(f"files/{filename}", "r", encoding="utf-8") as f:
                content = f.read()
            return encode_message("file_response", {"content": content})

        except FileNotFoundError:
            return encode_message("error", {"msg": f"File '{filename}' not found"})

        except Exception as e:
            return encode_message("error", {"msg": f"Error reading file: {str(e)}"})
        
    if action == "random_number":
        try:
            min_val = int(message["payload"].get("min", 0))
            max_val = int(message["payload"].get("max", 100))

            if min_val > max_val:
                return encode_message("error", {"msg": "min cannot be greater than max"})

            number = random.randint(min_val, max_val)
            return encode_message("random_response", {"number": number})

        except Exception as e:
            return encode_message("error", {"msg": f"Invalid input: {str(e)}"}) 
    
    if action == "chat_message":
        msg = message["payload"].get("msg", "")
        username = clients.get(message["conn"], "Unknown")

        # Broadcast con username
        for c in clients:
            try:
                c.send(encode_message("chat_broadcast", {
                    "msg": f"[{username}] {msg}"
                }))
            except:
                pass

        return None
    
    if action == "set_username":
        username = message["payload"].get("username", "Unknown")

        # Guardar username asociado al socket
        clients[message["conn"]] = username

        # Notificar a todos
        for c in clients:
            if c != message["conn"]:
                c.send(encode_message("chat_broadcast", {
                    "msg": f"*** {username} has joined the chat ***"
                }))

        return encode_message("username_ok", {"msg": "Username registered"})
    
    if action == "chat_command":
        cmd = message["payload"].get("cmd")

        if cmd == "users":
            # Obtener lista de usernames
            usernames = [u for u in clients.values() if u is not None]

            # Responder SOLO al cliente que lo pidió
            return encode_message("chat_broadcast", {
                "msg": "Users connected:\n- " + "\n- ".join(usernames)
            })

        return encode_message("error", {"msg": f"Unknown command '{cmd}'"})

    return encode_message("error", {"msg": "Unknown action"})


def handle_client(conn, addr):
    print(f"[THREAD STARTED] Client connected: {addr}")
    clients[conn] = None   # Registrar cliente sin username aún

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            message = decode_message(data)
            message["conn"] = conn  # Necesario para set_username y chat_message

            print(f"[RECEIVED from {addr}] {message}")

            response = handle_request(message)

            if response is not None:
                conn.send(response)

    except Exception as e:
        print(f"[ERROR with {addr}] {e}")

    finally:
        username = clients.get(conn, "Unknown")

        # Notificar a todos que el usuario salió
        for c in clients:
            if c != conn:
                try:
                    c.send(encode_message("chat_broadcast", {
                        "msg": f"*** {username} has left the chat ***"
                    }))
                except:
                    pass

        # Remover del diccionario
        if conn in clients:
            del clients[conn]

    conn.close()
    print(f"[THREAD CLOSED] Client disconnected: {addr}")

def start_server():
    """
    Starts a multithreaded TCP server that accepts multiple clients.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[SERVER RUNNING] {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()

        # Create a new thread for each client
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == "__main__":
    start_server()
   
    