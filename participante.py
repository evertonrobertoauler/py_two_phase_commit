import socket
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostname(), 4000))

client.send(bytes("teste", "UTF-8"))
time.sleep(150)

client.close()
