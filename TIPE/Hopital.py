import os

class Hopital:


    def __init__(self, name):
        self.name = name
        self.PK = getPkFromFile(name) # Public Key

    def getPKFromFile(name):
        f = open("listeHopital.txt")
        for line in f:
            sp = line.split("|")
            if sp[0] == name:
                return sp[1]
        return "-1"