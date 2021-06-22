class Client:

    def __init__(self):
        self.blockchain = Blockchain()
        self.listPerson = []            # Liste de Person
        # cf Miner pour le Thread etc...

    def receivedData(data):
        # Pour les data, on peut prendre une STR de la forme "command|parametre1/param2/param3..."
        # Les demandes en respond sont potentiellement différentes voir comment gérer les réponses avec une bibliothèque
        t = data.split("|")
        command = t[0]
        params = t[1].split("/")

        if command == "getAllBlocks":   # Envoie l'entièreté de la blockchain au param1 
            sendAllBlock(params[0])  
        elif command == "respondAllBlocks":   # C'est la commande reçu après avoir fait getAllBlocks
            pass
        elif command == "getHospitals":
            pass
        elif command == "respondHospitals":
            pass
        elif command == "newBlock":
            pass


        



    def getAllChain(): # Ask peers for all the chain and compare using alternateFollowingChains
        # Il va falloir choisir la meilleure blockchain parmi toutes celles reçu
        pass # cf P2P

    def getInfoAboutPerson(personId): # Renvoie un objet Person
        # Ca demande des infos au reste du réseau à propos de la personne
        pass


    def parseBlock(self, block):
        listTrans = block.transactions # Liste des transactions du blocs
        for trans in listTrans:
            persFound = False
            for pers in listPerson:
                if trans.personId == pers.personId:
                    persFound = True
                    malFound = False
                    for mal in pers.medicalHistory:
                        if mal.malId == trans.malId:
                            mal.addDate(trans.newDate)
                            malFound = True
                    if not malFound:
                        mal = Maladie(trans.malId)
                        mal.addDates(trans.newDate)
                        pers.medicalHistory += [mal]
            
                        
            if not persFound:
                pers = getInfoAboutPerson(trans.personId) # On récupère les infos de la personne du reste du réseau
               
                malFound = False               
                for mal in pers.medicalHistory:
                    if mal.malId == trans.malId:
                        malFound = True
                        if trans.newDate not in mal.dates:
                            mal.addDate(trans.newDate)
                if not malFound:
                   mal = Maladie(trans.malId)
                   mal.addDates(trans.newDate)
                   pers.medicalHistory += [mal]

                listPerson += [pers]