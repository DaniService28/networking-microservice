import socket
from protocol.messages import encode_message, decode_message

"""Simple client for interacting with the networking microservice."""

HOST = "localhost"
PORT = 5050

def send_request(action, payload=None):
    """
    Sends a JSON request to the server and returns the decoded response.
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    message = encode_message(action, payload)
    client.send(message)

    data = client.recv(1024)
    response = decode_message(data)

    client.close()
    return response

def enter_chat_mode():
    import threading
    import socket
    from protocol.messages import encode_message, decode_message

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    print("\n=== CHAT MODE ===")
    print("Type messages and press Enter.")
    print("Type '/exit' to return to the main menu.\n")

    # Pedir username
    username = input("Choose a username: ")
    sock.send(encode_message("set_username", {"username": username}))

    # Hilo que escucha mensajes del servidor
    def listen():
        while True:
            try:
                data = sock.recv(1024)
                if not data:
                    break
                msg = decode_message(data)
                print(f"\n{msg['payload']['msg']}")
            except:
                break

    threading.Thread(target=listen, daemon=True).start()

    # Loop principal del chat
    while True:
        msg = input()
        if msg.strip() == "/users":
            sock.send(encode_message("chat_command", {"cmd": "users"}))
            continue

        if msg.strip() == "/exit":
            print("Leaving chat mode...\n")
            sock.close()
            break

        sock.send(encode_message("chat_message", {"msg": msg}))

def show_menu():
    """
    Displays the interactive menu for the user.
    """
    print("\n=== NETWORKING MICROSERVICE CLIENT ===")
    print("1. Get server info")
    print("2. Echo a message")
    print("3. Math operations")
    print("4. Get server time")
    print("5. Reverse a string")
    print("6. Uppercase text")
    print("7. Read a file")
    print("8. Generate random number")
    print("9. Enter chat mode")
    print("10. Exit")




def run_client():
    """
    Main loop for the interactive client.
    """
    while True:
        show_menu()
        choice = input("Select an option: ")

        if choice == "1":
            response = send_request("get_info")
            print("\nServer response:", response)

        elif choice == "2":
            msg = input("Enter a message to echo: ")
            response = send_request("echo", {"msg": msg})
            print("\nServer response:", response)

        elif choice == "3":
            print("\nAvailable operations: add, subtract, multiply, divide")
            op = input("Enter operation: ").strip()

            a = input("Enter value for a: ")
            b = input("Enter value for b: ")

            response = send_request("math", {"op": op, "a": a, "b": b})
            print("\nMath result:", response)
            
        elif choice == "4":
            response = send_request("get_time")
            print("\nServer time:", response)
            
        elif choice == "5":
            text = input("Enter text to reverse: ")
            response = send_request("reverse_string", {"text": text})
            print("\nReversed text:", response)
            
        elif choice == "6":
            text = input("Enter text to convert to uppercase: ")
            response = send_request("uppercase", {"text": text})
            print("\nUppercase result:", response)
            
        elif choice == "7":
            filename = input("Enter filename to read: ")
            response = send_request("read_file", {"filename": filename})
            print("\nServer response:", response)
        
        elif choice == "8":
            min_val = int(input("Enter minimum value: "))
            max_val = int(input("Enter maximum value: "))
            response = send_request("random_number", {"min": min_val, "max": max_val})
            print("\nRandom number:", response)
            
        elif choice == "9":
            enter_chat_mode()
            
        elif choice == "10":
            print("Goodbye!")
            break



if __name__ == "__main__":
    run_client()