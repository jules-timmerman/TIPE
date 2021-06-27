from Client import Client

c1 = Client(8010)
c2 = Client(8011, ["127.0.0.1"], [8010])

c2.sendData("getAllBlocks", ["OUI"])
