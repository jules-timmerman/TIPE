from p2pnetwork.node import Node
import time


def generateCommandId(content):
    return str(time.time()) + content["command"]

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
        # Data un dictionnaire avec id: l'id unique pour éviter les boucles et data: le contenu du message
        # globalIp: l'adresse de retour de l'initiateur / port: le port
        id = data["id"]
        if not id in self.commandSendHistory:
            self.commandSendHistory += [id]
            content = data["content"]
            historyBuffer = data["historyBuffer"]

            print (str(self.port) + " : Receiving from " + str(connected_node.port) + " : " + str(content) + "\n")

            s = None # On l'initialise pour ceux qui recevront un respond qui n'est pas le leur

            if content["command"][:7] != "respond": # Si le message recu n'est pas un retour de réponse à l'envoyeur (donc plutôt une requête de quelqu'un)
                print(str(self.port) + " : Forwarding : " + str(data)  + "\n")
                self.forwardData(data) # On le transfère
                # Comme c'est une question dans tout les cas on la traite
                s = self.callbackMessage(content) # Potentiellement la commande à renvoyer (sous forme dict contents)
            elif historyBuffer == []: # Si c'est une réponse et que le buffer est vide (donc c'est la réponse à notre question)
                s = self.callbackMessage(content) # Alors on traite la réponse (on ne veut pas la traiter si on était pas l'initiateur
            else: # Si on a une réponse mais qui n'est pas la notre
                # Il va nous falloir lui permettre de continuer son chemin comme en dessous
                s = content

            if s != None : # Si s != None alors callbackMessage a retourné et on va donc devoir renvoyer une réponse de notre part: 
                targetId = historyBuffer[-1] # La personne à qui on doit envoyer (le dernier ajouter dans l'ordre)
                for n in self.all_nodes: # Normalment on a pas de copie de node
                    if n.id == targetId:
                        print(str(self.port) + " : Responding to : " + str(n.port) + " with " + str(s)  + "\n")
                        if s == content: # C'était alors une réponse et on l'envoie au prochain mec de la chaîne de réponse
                            self.send_to_node(n, {"id": id, "historyBuffer":historyBuffer[0:-1], "content": s})
                        else:
                            self.send_to_node(n, {"id": generateCommandId(s), "historyBuffer":historyBuffer[0:-1], "content": s})
                            # On génère un nouvel id lié à la réponse
                            # On enlève la node à qui on envoie la dernière node du buffer (à savoir elle même)

        
    def node_disconnect_with_outbound_node(self, connected_node):
        print("node wants to disconnect with oher outbound node: " + connected_node.host)
        
    def node_request_to_stop(self):
        print("node is requested to stop!")


    def forwardData(self, data):
        self.send_to_nodes({"id": data["id"], "historyBuffer": data['historyBuffer'] + [self.id], "content": data["content"]})

    def sendData(self, content):
        commandId = generateCommandId(content)
        self.commandSendHistory += [commandId]     # On ajoute aussi l'ID pour que le mec de base renvoit

        print(str(self.port) + " : Sending : " + str(content) + "\n")

        self.send_to_nodes({"id": commandId, "historyBuffer": [self.id], "content":content})
            # id : unique de la commande
            # historyBuffer : les ids des nodes à qui renvoyer au fur et à mesure (le chemin parcouru)
            # Content : {"command", "params"} à envoyer tel quel à callbackMessage

