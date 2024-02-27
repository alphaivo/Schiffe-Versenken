# Autor: St. Schmidt
# Datum: 10.09.2009; letzte Änderung: 23.08.2011
# Zweck: Eine Klasse Kanaele für die Kommunkation zwischen
#        zwei Rechnern im Netzwerk über TCP/IP
#
# ACHTUNG: FRISCH ANGEPASST AN PYTHON 3
#          WEITERE AENDERUNGEN FOLGEN GEWISS !!
#
# TODO:    Beschränkung auf 1023 Byte sollte noch entfallen!
#
"""
Klasse Kanaele:

Initialisierung:
<Kanalname> = Kanaele (ipadresse, portnummer)
Vor.: ipadresse beinhaltet als String die IP-Adresse des Kommunikations-
      partners. portnummer ist die (zukünftige) Portnummer des zu öffnenden
      Kanals für den Datenausstausch, wenn der aufrufende Prozess Klient der
      TCP/IP-Verbindung ist. Andernfalls ist es der Port des Verbindungssockets
      des Servers.
Eff.: Der Kanal <Kanalname> ist zwischen dem aufrufenden Rechner und dem
      Kommunikationspartner etabliert und geöffnet und steht zum Datenaustausch
      zur Verfügung.
      Der aufrufende Prozess war solange blockiert, bis der Kommunikations-
      partner ebenfalls durch eine Initialisierung versucht hat, den Kanal
      (mit gleicher Portnummer) zu öffnen.
      Laufen beide Kommunikationsprogramme auf demselben Rechner, so ist eine
      Datei "ServerFuerPort<portnummer>" im aktuellen Verzeichnis angelegt.

Verschicken von Daten:
<Kanalname>.senden(textstring)
Vor.: Der Kanal ist von beiden Kommunikationspartnern aus gesehen geöffnet.
      textstring ist vom Typ String und maximal 1023 Byte lang.
Eff.: textstring liegt im Kanal zum Empfang bereit. Der sendende
      Prozess so lange blockiert, bis der Kommunikationspartner die Daten
      durch Empfang entgegengenommen hat.

Empfangen von Daten:
<Nachrichtvariable> = <Kanalname>.empfangen()
Vor.: Der Kanal ist von beiden Kommunikationspartnern aus gesehen geöffnet.
Eff.: In <Nachrichtvariable> ist der Kanalinhalt vom Typ String
      (maximale Länge: 1023 Byte) enthalten.
      Der aufrufende Prozess war solange blockiert, bis wirklich Daten aus dem
      Kanal empfangen werden konnten.

Beenden der Verbindung / Schliessen des Kanals:
<Kanalname>.schliessen()
Vor.: keine
Eff.: Der Kanal ist vom aufrufenden Prozess aus gesehen geschlossen. Die zu-
      gehörige Kommunikations-Portadresse ist wieder freigegeben.
      Liefen beide Kommunikationsprozesse auf einem Rechner und wurde schliessen
      vom erstgestarteten Kommunikationsprozess aufgerufen, so ist die
      Datei "ServerFuerPort<portnummer>" wieder gelöscht.

nützliche Hilfsfunktion:
<Kanalname>.erster()
Vor.: keine
Eff.: True ist geliefert, gdw. der aufrufende Prozess auf der Maschine mit der
      kleineren IP-Adresse läuft.
      Laufen beide Prozesse auf derselben Maschine, so ist True geliefert, gdw. der
      aufrufende Prozess nicht der erstgestartete Prozess ist.
"""

from socket import *
from os import remove

class Kanaele:
  def __init__(self, zielIP, zielport):
    self.__rechnername = gethostname()
    self.__quellIP     = gethostbyname(self.__rechnername)
    self.__quellport   = zielport
    self.__zielIP      = zielIP
    self.__zielport    = zielport
    if self.__zielIP > self.__quellIP:  # Die Quelle ist der Server!
      self.__server  = self.__quellIP
      self.__erster = False
      self.__verbindungssocket = socket(AF_INET,SOCK_STREAM)
      self.__verbindungssocket.bind((self.__rechnername,self.__quellport))
      self.__verbindungssocket.listen(1)
      # print (self.__rechnername, "wartet auf Kontaktaufname ...")
      self.__kommunikationssocket, self.__addr = self.__verbindungssocket.accept()
      # print ("Verbindung zu", self.__zielIP, "hergestellt!")
    elif self.__zielIP < self.__quellIP:   # Das Ziel ist der Server!     
      self.__server = self.__zielIP
      self.__erster = True
      # print ("Es wird versucht, eine Verbindung aufzubauen ...")
      self.__kommunikationssocket = socket (AF_INET, SOCK_STREAM)
      while True: #Warte, bis der Server da ist und die Verbindung zulässt!
        try:
          self.__kommunikationssocket.connect((self.__zielIP, self.__zielport))
          break
        except error:
          pass
      # print ("Verbindung hergestellt zu:", self.__kommunikationssocket.getpeername())
    else:
      # print ("Quellrechner ist mit Zielrechner identisch!")
      # Quellrechner = Zielrechner!
      # Zur Entscheidung wird eine existierende/nichtexistierende Datei
      # herangezogen!
      self.__dateiname = "ServerFuerPort" + str (self.__zielport)
      # print (self.__dateiname)
      try:  
        self.__datei = open(self.__dateiname,"r")
        self.__datei.close()
        #gelungen: Dieses Programm ist der Klient!
        self.__erster = True
        self.__Dateizugriff = True
        self.__server = self.__zielIP
        # print "Es wird versucht, eine Verbindung aufzubauen ..."
        self.__kommunikationssocket = socket (AF_INET, SOCK_STREAM)
        self.__kommunikationssocket.connect((self.__zielIP, self.__zielport))
        # print ("Verbindung hergestellt zu:", self.__kommunikationssocket.getpeername())
      except IOError:
        #Dieses Programm ist der Server!
        # print ("Bin der Server!!")
        self.__erster = False
        self.__Dateizugriff = False
        self.__datei = open(self.__dateiname,"w")
        self.__datei.write("Server läuft!" + "\n")
        self.__datei.close()
        self.__server  = self.__quellIP
        self.__verbindungssocket = socket(AF_INET,SOCK_STREAM)
        self.__verbindungssocket.bind((self.__rechnername,self.__quellport))
        self.__verbindungssocket.listen(1)
        # print (self.__rechnername, "wartet auf Kontaktaufname ...")
        self.__kommunikationssocket, self.__addr = self.__verbindungssocket.accept()
        # print ("Verbindung zu", self.__zielIP, "hergestellt!")

  def erster(self):
    return self.__erster
        
  def empfangen(self):
    nachricht = self.__kommunikationssocket.recv(1024)[1:]
    self.__kommunikationssocket.send(b">")
    return str (nachricht,encoding='utf8')
  
  def senden(self,datenstring):
    if len (datenstring) > 1023:
      raise ValueError("Es duerfen maximal 1023 Byte gesendet werden!")
    self.__kommunikationssocket.send(bytes(">" + datenstring,encoding='utf8'))
    self.__kommunikationssocket.recv(1024)
    
  def schliessen(self):
    # print ("Verbindung wird geschlossen ...")
    self.__kommunikationssocket.close()
    if self.__zielIP != self.__quellIP:
      if self.__server == self.__quellIP:
        # print ("Server fährt runter ...")
        self.__verbindungssocket.close()
    else:
      if not self.__Dateizugriff:
        # print ("Server fährt runter ...")
        self.__verbindungssocket.close()
        remove(self.__dateiname)
        # print ("Lock-Datei wurde gelöscht!") 
