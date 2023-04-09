import socket

from threading import Thread


# Crear un socket para el servidor
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Definir el puerto y la dirección del servidor
PORT = 8080
SERVER = socket.gethostbyname(socket.gethostname())

# Asociar el socket al puerto y dirección del servidor
sock.bind(("localhost", PORT))

# Escuchar conexiones entrantes
sock.listen()

# Lista para almacenar los clientes conectados
clients = {}


def descifrar(mensaje_cifrado, desplazamiento):
    mensaje_descifrado = ""
    try:
        if len(mensaje_cifrado) > 100:
            raise ValueError("El mensaje es demasiado largo. Maximo permitido: 100 caracteres.")
        for letra in mensaje_cifrado:
            if letra.isalpha():
                if letra.isupper():
                    mensaje_descifrado += chr((ord(letra) - desplazamiento - 65) % 26 + 65)
                else:
                    mensaje_descifrado += chr((ord(letra) - desplazamiento - 97) % 26 + 97)
            elif letra.isdigit():
                mensaje_descifrado += str((int(letra) - desplazamiento) % 10)
            else:
                mensaje_descifrado += letra
    except ValueError as e:
        print(f"Error: {e}")
    return mensaje_descifrado


# Función para enviar un mensaje a todos los clientes conectados
def broadcast(msg, prefix=""):
    #msg_cifrado = cifrar(msg.decode(),3)
    for client in clients:
        client.send(bytes(prefix,"utf8")+msg)

# Función para manejar a cada cliente conectado
def handle_clients(conn):
    name = conn.recv(1024).decode()
    print(name)
    welcome = f"Welcome {name}. Good to see you"
    conn.send(bytes(welcome,"utf8"))
    msg = name + " has recently joined us"
    broadcast(bytes(msg,"utf8"))
    clients[conn] = name

    while True:
        try:
            msg = conn.recv(1024).decode()
            print(msg)
         
            broadcast(bytes(f"{name} dice: {msg}","utf8"))
       
        except:
            conn.close()
            del clients[conn]
            broadcast(bytes(f"{name} has left the chat","utf8"))
            break

# Función para aceptar conexiones entrantes de los clientes
def accept_client_connection():
    while True:
        try:
            client_conn, client_address = sock.accept()
            print(client_address, " has Connected")
            client_conn.send(bytes("Welcome to the chat room, Please type your name","utf8"))
            Thread(target = handle_clients,args=(client_conn,)).start()
        except Exception:
            print('Error: usuario no puede entrar!!')


# Iniciar la función para aceptar conexiones entrantes
print("Server is listening...")
accept_thread = Thread(target=accept_client_connection)
accept_thread.start()



