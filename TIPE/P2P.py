import socket
from Blockchain import Blockchain
from Crypto.PublicKey import RSA
from hashlib import sha256
from Person import Person
import time
from Block import Block
from Transaction import Transaction
from Maladie import Maladie


from p2pnetwork.node import Node

N = 60
def delete_pos(l,i) : 
        res = []
        for k in range(0,len(l)) :
            if i != k :
                res += [l[k]]
        return res


class P2P (Node):
    
    def __init__(self, host, port, node_connues) :
        super(P2P, self).__init__(host, port, None)
        self.host = host
        self.port = port
        self.historique_commandes = [] # liste de dictionnaires du type { "id" : id du message , "dernier_commanditaire" : dernier mec qui a demandé la commande, ???????????? "contenudemande" : réponses qu'il a reçu pour l'instant, liste de dictionnaires}
        self.stockage_reponses = [] # liste de réponses du type { "réponse" : réponse , "client" : client }
    
    def transmettre_commandes(self, message, sender) :
        booleen = False
        id_message = message["id"]
        for histo in self.historique_commandes :
            if id_message == histo["id"] :
                booleen = True
        if not booleen : #on ne transmet que s'il n'est pas dans l'historique. Si il l'était, il aurait déjà été transmit
                self.historique_commandes += { "id" : message["id"], "dernier_commanditaire" : sender.id}
                self.traiter_commande(message)
        for nodes in self.nodes_outbound :
            if nodes.id != sender.id :
                self.send_to_node(nodes, message)
            ok = { "id" : str(self.id) + str(time.time()) , "contenu" : "" , "contenudemande" : [] , "parametre" : "ok" }
            self.send_to_node(sender,ok)
        booleen = False
    

    def return_to_sender(self, data, sender):
        pass
    def recevoir_commande(self,message) :
        pass    

    def sendData(self,contents) : 
        data_id = str(self.id) + str(time.time())       
        data = { "id" : data_id , "contenu" : contents , "contenudemande": [], "parametre" : None}
        for node in self.nodes_outbound :
            self.send_to_node(node,data)



    def node_message(self, connected_node, data):
            data_id = data["id"]
            parametre = data["parametre"]
            data_contenu = data["contenu"]
            data_contenudemande = data["contenudemande"]
            if parametre == None :
                self.transmettre_commande(data,connected_node)
            
            # compteur = N//2
            # if parametre == "ok" :
            #     while compteur != 0 :
            #         time.sleep(1) 
            #         compteur = compteur - 1
            #         booleen = False
            #     for histo in self.historique_commandes :
            #             if histo["id"] == data_id :
            #                 booleen = True
            #             if booleen :
            #                 data = { "id" : data_id , "contenu" : data_contenu, "contenudemande" : self.callbackMessage(data_contenu), "parametre" : "retour" }
            #                 self.send_to_node(self,data)
            #     booleen = False


            compteur = N//2

            if parametre == "retour" :             
                for (i,histo) in enumerate(self.historique_commandes) :
                    if histo["id"] == data_id :    
                        if histo["dernier_commanditaire"].id == self.id :
                            for reponse in data["contenudemande"] :
                                self.callbackMessage(reponse)
                        else :
                            retour = { "id" : data_id , "contenu" : data_contenu, "contenudemande" : data_contenudemande + self.callbackMessage(data_contenu), "parametre" : "retour" }
                    
                            self.send_to_node(histo["dernier_commanditaire"],retour)
                    
                            time.sleep(N)
                            self.historique_commandes = delete_pos(self.historique_commandes,i)

    def outbound_node_connected(self, connected_node):
        print("outbound_node_connected: " + connected_node.id)
        
    def inbound_node_connected(self, connected_node):
        print("inbound_node_connected: " + connected_node.id)

    def inbound_node_disconnected(self, connected_node):
        print("inbound_node_disconnected: " + connected_node.id)

    def outbound_node_disconnected(self, connected_node):
        print("outbound_node_disconnected: " + connected_node.id)

    
        #print("node_message from " + connected_node.id + ": " + str(data))
        
    def node_disconnect_with_outbound_node(self, connected_node):
        print("node wants to disconnect with oher outbound node: " + connected_node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop!")



    
   