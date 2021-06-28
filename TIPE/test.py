from Client import Client
import socket

c1 = Client(8010)
c2 = Client(8011, [socket.gethostbyname(socket.gethostname())], [8010])

c2.sendData("getAllBlocks", ["OUI"])
