from P2P import P2P
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

class P2P (Node):
    
    def __init__(self, host, port, node_connues) :

        self.host = host
        self.port = port
        self.historique_commandes = []

    def initialisation(self, contenu) :
        id = {"port": str(self.port) ,"host" : str(self.host) , "time" : str(time.time())}
        message = { "id" : id , "contenu" : contenu }
        
        for nodes in self.nodes_outbound :
            self.send_to_node(nodes, message)

    
    def transmettre_commandes(self, message, sender) :
        if not message["id"] in self.historique_commandes :
            self.historique_commandes += message["id"] 
        for nodes in self.nodes_outbound :
            if nodes.host != sender.host and nodes.port != sender.host :
                self.send_to_node(nodes, message)

    def traiter_commande(self, ):
        pass


    def return_to_sender(self, data):
        pass



    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super(MyOwnPeer2PeerNode, self).__init__(host, port, id, callback, max_connections)

    def outbound_node_connected(self, connected_node):
        print("outbound_node_connected: " + connected_node.id)
        
    def inbound_node_connected(self, connected_node):
        print("inbound_node_connected: " + connected_node.id)

    def inbound_node_disconnected(self, connected_node):
        print("inbound_node_disconnected: " + connected_node.id)

    def outbound_node_disconnected(self, connected_node):
        print("outbound_node_disconnected: " + connected_node.id)

    def node_message(self, connected_node, data):
        print("node_message from " + connected_node.id + ": " + str(data))
        
    def node_disconnect_with_outbound_node(self, connected_node):
        print("node wants to disconnect with oher outbound node: " + connected_node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop!")

    # OPTIONAL
    # If you need to override the NodeConection as well, you need to
    # override this method! In this method, you can initiate
    # you own NodeConnection class.
    def create_new_connection(self, connection, id, host, port):
        return MyOwnNodeConnection(self, connection, id, host, port) 


    
   