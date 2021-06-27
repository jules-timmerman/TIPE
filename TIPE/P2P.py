from p2pnetwork.node import Node
import time
from requests import get


class P2P (Node):
    def __init__(self, host, port, callbackMessage):
        super(P2P, self).__init__(host, port, None)

        self.callbackMessage = callbackMessage
        self.commandSendHistory = [] # Liste avec des ids de commandes pour éviter les boucles

    def outbound_node_connected(self, connected_node):
        print("outbound_node_connected: " + connected_node.host)
        
    def inbound_node_connected(self, connected_node):
        print("inbound_node_connected: " + connected_node.host)

    def inbound_node_disconnected(self, connected_node):
        print("inbound_node_disconnected: " + connected_node.host)

    def outbound_node_disconnected(self, connected_node):
        print("outbound_node_disconnected: " + connected_node.host)

    def node_message(self, connected_node, data):
        print("node_message from " + connected_node.host + ": " + str(data))

        # Data un dictionnaire avec id: l'id unique pour éviter les boucles et data: le contenu du message
        # globalIp: l'adresse de retour de l'initiateur / port: le port
        id = data["id"]
        if not id in self.commandSendHistory:
            self.commandSendHistory += [id]
            content = data["content"]
            s = self.callbackMessage(content) # Potentiellement la commande à renvoyer
            if not s == "":
                self.connect_with_node(data["globalIP"], data["port"])
                for n in self.nodes_outbound: 
                    if n.host == host and n.port == port:
                        self.send_to_node() # Il faut savoir à qui renvoyer
            self.forwardData(data)
        
        
    def node_disconnect_with_outbound_node(self, connected_node):
        print("node wants to disconnect with oher outbound node: " + connected_node.host)
        
    def node_request_to_stop(self):
        print("node is requested to stop!")


    def forwardData(self, data):
        self.send_to_nodes(data)

    def sendData(self, contents):
        t = time.time()

        unique = contents["command"]
        for p in contents["params"]:
            unique += str(p)
        id = str(t) + unique
        self.commandSendHistory += [id] # On ajoute aussi l'ID pour que le mec de base renvoit


        self.commandSendHistory += id
        globalIP = get('https://api.ipify.org').text # l'IP global de l'initiateur pour lui répondre
        # On supposera ici que tout les ports sont ouverts et que ce sont les mêmes en extérieur et intérieur
        port = self.port

        self.send_to_nodes({"id": id, "globalIP":globalIP, "port": port, "content":contents})


    def discovery():
        pass


