import csv
from datetime import datetime
#Próba az Épületekkel
with open("Epuletek.csv", "r", newline="", encoding="utf-8") as epuletek_file:
    epuletek_reader = csv.reader(epuletek_file) 
    epuletek_data = list(epuletek_reader) 

class Epuletek:
    def __init__(self, ep_azon, nev, tipus, epites_eve, hasznos_terulet_m2):
        self.ep_azon = int(ep_azon)
        self.nev = nev
        self.tipus = tipus
        self.epites_eve = int(epites_eve)
        self.hasznos_terulet_m2 = int(hasznos_terulet_m2)

    def __repr__(self):
        return f"Epuletek(ep_azon={self.ep_azon}, nev='{self.nev}', tipus='{self.tipus}', epites_eve={self.epites_eve}, hasznos_terulet_m2={self.hasznos_terulet_m2})"

epuletek_list = [Epuletek(*row[0].split(";")) for row in epuletek_data[1:]]  

for epulet in epuletek_list:
    print(epulet)

#Lakosok
with open("Lakosok.csv", "r", newline="", encoding="utf-8") as lakosok_file:
    lakosok_reader = csv.reader(lakosok_file) 
    lakosok_data = list(lakosok_reader) 

class Lakosok:
    def __init__(self, lakos_azon, nev, szuletesi_ev, foglalkozas, ep_azon):
        self.lakos_azon = int(lakos_azon)
        self.nev = nev
        self.szuletesi_ev = int(szuletesi_ev)
        self.foglalkozas = foglalkozas
        self.ep_azon = int(ep_azon)

    def __repr__(self):
        return f"Lakosok(lakos_azon={self.lakos_azon}, nev={self.nev}, szuletesi_ev={self.szuletesi_ev}, foglalkozas={self.foglalkozas}, ep_azon={self.ep_azon})"

lakosok_list = [Lakosok(*row[0].split(";")) for row in lakosok_data[1:]]  

for lakos in lakosok_list:
    print(lakos)


#Szolgáltatások
with open("Szolgaltatasok.csv", "r", newline="", encoding="utf-8") as szolgaltatasok_file:
    szolgaltatasok_reader = csv.reader(szolgaltatasok_file) 
    szolgaltatasok_data = list(szolgaltatasok_reader) 

class Szolgaltatasok:
    def __init__(self, szolg_azon, nev, tipus, ep_azon):
        self.szolg_azon = int(szolg_azon)
        self.nev = nev
        self.tipus = tipus
        self.ep_azon = int(ep_azon)

    def __repr__(self):
        return f"Szolgaltatasok(szolg_azon={self.szolg_azon}, nev={self.nev}, tipus={self.tipus} ep_azon={self.ep_azon})"

szolgaltatasok_list = [Szolgaltatasok(*row[0].split(";")) for row in szolgaltatasok_data[1:]]  

for szolgaltatas in szolgaltatasok_list:
    print(szolgaltatas)
#Varosfejlesztes
with open("Varosfejlesztes.csv", "r", newline="", encoding="utf-8") as varosfejlesztes_file:
    varosfejlesztes_reader = csv.reader(varosfejlesztes_file) 
    varosfejlesztes_data = list(varosfejlesztes_reader) 

class Varosfejlesztes:
    def __init__(self, projekt_azon, nev, koltseg_arany, kezdes, befejezes):
        self.projekt_azon = int(projekt_azon)
        self.nev = nev
        self.koltseg_arany = int(koltseg_arany)
        self.kezdes = datetime.strptime(kezdes, "%Y.%m.%d %H:%M:%S").date()
        self.befejezes = datetime.strptime(befejezes, "%Y.%m.%d %H:%M:%S").date()  

    def __repr__(self):
        return f"Varosfejlesztes(projekt_azon={self.projekt_azon}, nev={self.nev}, koltseg_arany={self.koltseg_arany}, kezdes={self.kezdes}, befejezes={self.befejezes})"

varosfejlesztes_list = [Varosfejlesztes(*row[0].split(";")) for row in varosfejlesztes_data[1:]]  

for projekt in varosfejlesztes_list:
    print(projekt)