# Autor: Gustav Freitag
# Datum: 25.02.2024
# Zweck: Klasse Sekretaer, Schnittstelle zu Kanaele

from time import * #!! test
from Kanaele import *

class Sekretaer:
    def __init__(self,pcnummer:int)->"Sekretaer":
        self.__gegnerIP = "192.168.1." + str(pcnummer)
        #self.__gegnerIP = "10.16.102." + str(pcnummer)
        self.__port = 55555
        self.__k = Kanaele(self.__gegnerIP,self.__port)
        self.__erster = self.__k.erster()
        #self.__erster = True #!! test

    def gibErster(self)->bool:
        return self.__erster

    def sendeSchiffe(self,schiffe:[(int, int)]):
        stringS = ""
        for schiff in schiffe:
            for coord in schiff:
                stringS += str(coord[0]) + " " + str(coord[1]) + ","
            stringS = stringS[:-1]
            stringS += "]"
        stringS = stringS[:-1]
        self.__k.senden(stringS)
    
    def empfangeSchiffe(self)->[(int, int)]:
        stringS=self.__k.empfangen()
        #stringS = '7 5,7 6,7 7,7 8]9 4,9 5,9 6,9 7'#!! test
        stringS = stringS.split(']')
        schiffe = []
        for schiff in stringS:
            schiff = schiff.split(',')
            print(schiff)
            s=[]
            for cord in schiff:
                x,y = cord.split()
                s.append((int(x),int(y)))
            schiffe.append(s)
        return schiffe
                
    def kommuniziereSchiffe(self,schiffe:[(int, int)])->[(int, int)]:
        if self.__erster:
            self.sendeSchiffe(schiffe)
            return self.empfangeSchiffe()
        else:
            gegnerSchiffe = self.empfangeSchiffe()
            self.sendeSchiffe(schiffe)
            return gegnerSchiffe

    def sendeZug(self,zug:(int,int)):
        stringZ= str(zug[0]) + " " + str(zug[1])
        self.__k.senden(stringZ)

        
    
    def empfangeZug(self)->(int,int):
        stringZ = self.__k.empfangen()
        x,y = stringZ.split()
        return (int(x),int(y))

        #!! test:
        #sleep(2)
        #global zuege
        #global z
        #z += 1
        #print(zuege[z])
        #return zuege[z]

#zuege= []
#for i in range(5):
#    for j in range(5):
#        zuege.append((i,j))
#z = -1
#schiffe = [[(1,0),(2,0),(3,0)],[(4,4),(4,5),(4,6)]]
#print(empfangeSchiffe(sendeSchiffe(schiffe)))
