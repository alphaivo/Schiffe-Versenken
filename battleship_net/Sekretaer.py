# Autor: Gustav Freitag
# Datum: 28.02.2024
# Zweck: Klasse Sekretaer, Schnittstelle zu Kanaele

from Kanaele import *
from random import *


class Sekretaer:
    """
    Vor.: -heimspiel- ist ein Boolean und False wenn in der Schule gespielt werden soll, sonst True. -pcnummer- ist die PC-Nummer des Gegners im Raum A124 bzw.
    die IP-Adresse des gegnerischen PCs. Die Module Random und Kanaele sind importiert.
    Eff.: Eine Kanal mit dem Gegner ist nun aufgebaut. Die gegnerische IP und der Port des Kanals ist gespeichert. Außerdem ist festgelegt, ob der Spieler anfängt.
    Erg.: Eine Instanz der Klasse Sekretär ist geliefert.
    """
    def __init__(self, pcnummer:int, heimspiel:bool)->"Sekretaer":
        if heimspiel:
            self.__gegnerIP = str(pcnummer)# normale IP-Adressen#
        else:
            self.__gegnerIP = "10.16.102." + str(pcnummer)
        self.__port = 55555
        self.__k = Kanaele(self.__gegnerIP,self.__port)

        self.__erster = self.__k.erster()
        if self.__k.erster():#
            self.__erster = randint(0,1) == 1
            self.__k.senden(str(not self.__erster))
        else:#
            self.__erster = self.__k.empfangen() == 'True'
        

    def gibErster(self)->bool:
        """Vor.: -
        Eff.: -
        Erg.: Es ist geliefert, ob der Spieler beginnt."""
        return self.__erster

    def sendeSchiffe(self,schiffe:[(int, int)]):
        """Vor.: -schiffe- ist eine Liste von Listen von Tupeln (x,y) mit Koordinaten vom Typ int.
        Eff.: -schiffe- ist an den Gegner übermittelt, wenn dieser empfangeSchiffe aufruft.
        Erg.: -"""
        stringS = ""
        for schiff in schiffe:
            for coord in schiff:
                stringS += str(coord[0]) + " " + str(coord[1]) + ","
            stringS = stringS[:-1]
            stringS += "]"
        stringS = stringS[:-1]
        self.__k.senden(stringS)
    
    def empfangeSchiffe(self)->[(int, int)]:
        """Vor.: -
        Eff.: Das Programm wird pausiert, bis der Gegner sendeSchiffe aufruft.
        Erg.: Eine Liste der gegnerischen Schiffen mit jeweils mehreren Koordinaten ist geliefert."""
        stringS=self.__k.empfangen()
        stringS = stringS.split(']')
        schiffe = []
        for schiff in stringS:
            schiff = schiff.split(',')
            s=[]
            for cord in schiff:
                x,y = cord.split()
                s.append((int(x),int(y)))
            schiffe.append(s)
        return schiffe
                
    def kommuniziereSchiffe(self,schiffe:[(int, int)])->[(int, int)]:
        """Vor.: -schiffe- ist eine Liste von Listen von Tupeln (x,y) mit Koordinaten von jedem Schiff der eigenen Flotte.
        Eff.: -schiffe- ist an den Gegner übermittelt, das Programm wird pausiert, bis der Gegner ebenfalls kommuniziereSchiffe aufruft.
        Erg.: Eine Liste der gegnerischen Schiffen mit jeweiligen mehreren Koordinaten ist geliefert."""
        if self.__erster:
            self.sendeSchiffe(schiffe)
            return self.empfangeSchiffe()
        else:
            gegnerSchiffe = self.empfangeSchiffe()
            self.sendeSchiffe(schiffe)
            return gegnerSchiffe

    def sendeZug(self,zug:(int,int)):
        """Vor.: -zug- ist ein Tuple bestehend aus x- und y-Koordinate. x und y sind vom Typ int.
        Eff.: Der Zug ist an den Gegner übermittelt, falls dieser ihn mit empfangeZug empfängt.
        Erg.: - """
        stringZ= str(zug[0]) + " " + str(zug[1])
        self.__k.senden(stringZ)

        
    
    def empfangeZug(self)->(int,int):
        """Vor.: -
        Eff.: Das Programm wird pausiert, bis der Gegner sendeZug aufruft.
        Erg.: Der Zug des Gegners ist geliefert."""
        stringZ = self.__k.empfangen()
        x,y = stringZ.split()
        return (int(x),int(y))

    def quit(self):
        """Vor.: -
        Eff.: Der Kanal zum Gegner ist geschlossen.
        Erg.: -"""
        self.__k.schliessen()



