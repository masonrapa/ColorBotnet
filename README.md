# ColorBotnet
Simple python botnet on one-by-one orders (not looping all the devices)

botnet.py -> server for receive all the connections at once

target.py -> client that receive the orders from the master client, execute them and gives back the answer of each command

admin.py -> client with privileges for sending data to the server (you need to select at first the client you wanna send directly)

The different commands are:

list - just shows the available connections (clients recognized by the server)

connect ip:port - connect directly your orders (as admin) to the selected target

runcmd - executes a console command on the target's device (and give you back the answer if any)

script - infinite open window loop (designed for RAM killer)

fread <path_to_file> - gives you the content of some file

clear - clear the admin terminal

splash - shows up a browser window on the target's screen with the chosen URL

hlogs - gets back the login data registered locally as Link / User / Password

hlink - gets back the website history as Name / Date / Link

hdwnl - gets back the download history on the device as Path / Web / Source

discordsteal - try to catch any discord browser token registered

shutdown - powers off automatically the device

help - shows this screen (but in spanish)
