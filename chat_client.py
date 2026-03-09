import socket
import threading
from protocol.messages import encode_message, decode_message

HOST = "localhost"
PORT = 5050

def listen_for_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break

            msg = decode_message(data)
            print(f"\n[CHAT] {msg['payload']['msg']}")
        except:
            break

def run_chat_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    # Hilo que escucha mensajes del servidor
    threading.Thread(target=listen_for_messages, args=(sock,), daemon=True).start()

    print("Connected to chat. Type messages and press Enter.")

    while True:
        msg = input()
        sock.send(encode_message("chat_message", {"msg": msg}))

if __name__ == "__main__":
    run_chat_client()