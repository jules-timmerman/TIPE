from Miner import Miner
import sys
import time


m = Miner (int(sys.argv[1]), ["127.0.0.1"], [8000])

time.sleep(60)

m.blockchain.printBlockchainAndAll()