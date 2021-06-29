from Crypto import PublicKey
from Crypto.PublicKey import RSA
from hashlib import sha256


keyPair = RSA.generate(bits=1024)

clepublique = [keyPair.n, keyPair.e]

cleprivee = [keyPair.n , keyPair.d ]

msg =  " Comment est votre blanquette ? faux"

hash = int.from_bytes(sha256(bytes(msg, 'utf-8')).digest(), byteorder='big')   

signature = pow(hash, cleprivee[1], cleprivee[0]) 

hashFromSignature = pow(signature, clepublique[1], clepublique[0])

hash == hashFromSignature 