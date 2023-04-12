
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# import required libraries
import socket
from threading import Thread
import tkinter as tk
from tkinter import *
from tkinter import messagebox


import logging

logging.basicConfig(filename='actividad_chat.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%Y-%m-%d-%H:%M:%S')
# Registro de información

def cifrar(mensaje, desplazamiento):
    mensaje_cifrado = ""
    try:
        if len(mensaje) > 255:
            raise ValueError("El mensaje es demasiado largo. Maximo permitido: 255 caracteres....intentalo de nuevo")
        for letra in mensaje:
        # Verificar si la letra es un caracter ASCII imprimible
            if ord(letra) >= 32 and ord(letra) <= 126:
                letra_cifrada = chr((ord(letra) + desplazamiento - 32) % 128 + 32)
            else:
                letra_cifrada = letra
            mensaje_cifrado += letra_cifrada
    except ValueError as e:
        print(f"Error: {e}")
        logging.error(e)
        msg_list.insert(tk.END, e) 
    return mensaje_cifrado

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
        logging.error(e)
    return mensaje_descifrado

def cerrar_ventana():
    # Cierra la ventana actual
    window.destroy()
    #s.send(bytes("has left the chat", "utf8"))
    messagebox.showinfo("Ventana cerrada", f"La ventana {window} ha sido cerrada.")
    # Desconecta la sesión o realiza otras acciones necesarias
    # ...


def receive():
    while True:
        try:
            msg = s.recv(1024).decode("utf-8")
            msg_list.insert(tk.END, msg)
        except:
            s.close()
            break

def send_message(event=None):
    msg = my_msg.get()
    my_msg.set("")
    try:
        is_server_online()
        s.send(bytes(cifrar(msg,3), "utf-8"))
        
    except:
        logging.error("El servidor no esta disponible en este momento.")
        messagebox.showinfo(
            title="Error de conexion",
            message="El servidor no esta disponible en este momento.",
            icon='error',
        )
    
def on_closing(event=None):
    s.close()
    window.quit()

def is_server_online():
    host = 'localhost' # o la dirección IP del servidor
    port = 8080 # el puerto en el que el servidor está escuchando
    try:
        s.connect((host, port))
        #s.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False


window = Tk()
window.title("Ventana Chat")
window.configure(bg="sky blue")

message_frame = Frame(window,bg='white')
message_frame.pack(expand=True, fill=BOTH)


my_msg = StringVar()
my_msg.set("")

scroll_bar = Scrollbar(message_frame)
msg_list = Listbox(message_frame, bg="white", yscrollcommand=scroll_bar.set)

scroll_bar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
msg_list.pack(expand=True, fill=BOTH)

entry_field = Entry(window, textvariable=my_msg, fg="black", width=80)
entry_field.pack()


entry_field.bind("<Return>", send_message)  # Capturamos la tecla Enter
entry_field.pack()
send_button = Button(window, text="Enviar", font="Arial", fg="white", bg="blue", relief="ridge", command=send_message)
send_button.pack()

close_button = Button(window, text="Cerrar ventana",font="Arial", bg="red", fg="white", relief="ridge", command=on_closing)
close_button.pack(side="right")


host = "localhost"
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((host, port))
    print("El servidor está activo")
except:
    logging.error("El servidor no esta disponible en este momento.")
    messagebox.showinfo(
        title="Error de conexion",
        message="El servidor no esta disponible en este momento.",
        icon='error',
    )



window.protocol("WM_DELETE_WINDOW", on_closing)
receive_thread = Thread(target=receive)
receive_thread.start()

window.mainloop()



