import socket
import logging
from threading import Thread

logging.basicConfig(filename='registro_session.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%Y-%m-%d-%H:%M:%S')



# Función para descifrar un mensaje
def descifrar(mensaje_cifrado, desplazamiento):
    mensaje_descifrado = ""
    try:
        if len(mensaje_cifrado) > 255:
            raise ValueError("El mensaje es demasiado largo. Maximo permitido: 255 caracteres.")
        for letra in mensaje_cifrado:
        # Verificar si la letra es un caracter ASCII imprimible
            if ord(letra) >= 32 and ord(letra) <= 126:
                letra_descifrada = chr((ord(letra) - desplazamiento - 32) % 128 + 32)
            else:
                letra_descifrada = letra
            mensaje_descifrado += letra_descifrada
    except ValueError as e:
        print(f"Error: {e}")
        logging.error("El mensaje es demasiado largo. Maximo permitido: 255 caracteres.")
    return mensaje_descifrado


# Función para enviar un mensaje a todos los clientes conectados
def broadcast(msg, prefix=""):
    #msg_cifrado = cifrar(msg.decode(),3)
    for client in clients:
        client.send(bytes(prefix,"utf8")+msg)

# Función para manejar a cada cliente conectado
def handle_clients(conn):
    try:
        name = descifrar(conn.recv(1024).decode(),3)
    except ConnectionResetError as e:
        print("Se ha producido un error de conexión: ", e)
        logging.error(f"Se ha producido un error de conexión: ")
        return
    #name = descifrar(conn.recv(1024).decode(),3)
    print(name)
    welcome = f"Bienvenido {name}. Un gusto verte"
    conn.send(bytes(welcome,"utf8"))
    msg = name + " ha entrado al chat"
    logging.info(f"{name} ha entrado al chat")
    broadcast(bytes(msg,"utf8"))
    clients[conn] = name

    while True:
        try:
            msg = conn.recv(1024).decode()
            print(msg)
            msg_descifrado = descifrar(msg,3)
            broadcast(bytes(f"{name} dice: {msg_descifrado}","utf8"))
            logging.info(name+ ' envio un mensaje')
        except:
            conn.close()
            del clients[conn]
            broadcast(bytes(f"{name} ha dejado el chat","utf8"))
            logging.info(f"{name} ha dejado el chat")
            break

# Función para aceptar conexiones entrantes de los clientes
def accept_client_connection():
    while True:
        client_conn, client_address = sock.accept()
        print(client_address, " se conecto")
        client_conn.send(bytes("Bienvenido a la sala de chat, por favor ingresa tu nombre:","utf8"))
        Thread(target = handle_clients,args=(client_conn,)).start()





# Crear un socket para el servidor





# Definir el puerto y la dirección del servidor
clients = {}
PORT = 8080
#SERVER = socket.gethostbyname(socket.gethostname())

try:
# Asociar el socket al puerto y dirección del servidor
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", PORT))
    sock.listen()
    print("Servidor escuchando en el puerto: ", PORT)
    logging.info("---------------NUEVO INICIO DE SESION---------------")
    accept_thread = Thread(target=accept_client_connection)
    accept_thread.start()

except Exception:
    logging.error("NO SE ENCUENTRA SERVIDOR")
# Lista para almacenar los clientes conectados



# Iniciar la función para aceptar conexiones entrantes




