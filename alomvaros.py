import csv
from datetime import datetime, timedelta
import random

#Épületek beolvasása
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
        self.allapot = random.randint(1, 5)

    def __repr__(self):
        return f"Epuletek(ep_azon={self.ep_azon}, nev='{self.nev}', tipus='{self.tipus}', epites_eve={self.epites_eve}, hasznos_terulet_m2={self.hasznos_terulet_m2}, allapot={self.allapot})"

epuletek_list = [Epuletek(*row[0].split(";")) for row in epuletek_data[1:]]

#Lakosok beolvasása
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
lakosok_szama = len(lakosok_list)

#Városfejlesztés beolvasása
with open("Varosfejlesztes.csv", "r", newline="", encoding="utf-8") as varosfejlesztes_file:
    varosfejlesztes_reader = csv.reader(varosfejlesztes_file) 
    varosfejlesztes_data = list(varosfejlesztes_reader)

class Varosfejlesztes:
    def __init__(self, projekt_azon, nev, koltseg_arany, kezdes, befejezes):
        self.projekt_azon = int(projekt_azon)
        self.nev = nev
        self.koltseg_arany = int(koltseg_arany)
        self.kezdes = datetime.strptime(kezdes.split()[0], "%Y.%m.%d").date()
        self.befejezes = datetime.strptime(befejezes.split()[0], "%Y.%m.%d").date()

varosfejlesztes_list = [Varosfejlesztes(*row[0].split(";")) for row in varosfejlesztes_data[1:]]

#Szolgáltatások beolvasása
with open("Szolgaltatasok.csv", "r", newline="", encoding="utf-8") as szolgaltatasok_file:
    szolgaltatasok_reader = csv.reader(szolgaltatasok_file) 
    szolgaltatasok_data = list(szolgaltatasok_reader)

class Szolgaltatasok:
    def __init__(self, szolg_azon, nev, tipus, ep_azon):
        self.szolg_azon = int(szolg_azon)
        self.nev = nev
        self.tipus = tipus
        self.ep_azon = int(ep_azon)
        self.havi_koltseg = random.randint(500, 3500)

    def __repr__(self):
        return f"Szolgaltatasok(szolg_azon={self.szolg_azon}, nev={self.nev}, tipus={self.tipus}, ep_azon={self.ep_azon}, havi_koltseg={self.havi_koltseg})"
szolgaltatasok_list = [Szolgaltatasok(*row[0].split(";")) for row in szolgaltatasok_data[1:]]

#Kezdeti állapot beállítása
lakosok_elegedettsege = random.randint(0, 100)  
penzkeret = random.randint(5000, 50000)  

print("\n--- Játék kezdete ---")
print(f"Lakosság száma: {lakosok_szama} fő")
print(f"Lakosok elégedettsége: {lakosok_elegedettsege}%")
print(f"Pénzkeret: {penzkeret} arany\n")

#Új épület építése
def uj_epulet_epitese():
    global penzkeret, lakosok_szama, lakosok_elegedettsege
    
    print("\n--- Új épület építése ---")
    nev = input("Add meg az épület nevét: ").strip()
    tipus = input("Add meg az épület típusát (lakóház, iroda, stb.): ").strip()
    
    try:
        hasznos_terulet_m2 = int(input("Add meg a hasznos területet (m2): ").strip())
    except ValueError:
        print("Hibás bemenet! Kérlek, számot adj meg a hasznos területhez.")
        return
    
    koltseg = random.randint(1000, 10000)  
    projekt_ido_honap = random.randint(3, 12)  

    if penzkeret < koltseg:
        print("Nincs elég pénzed az építéshez!")
        return
    
    kezdes = datetime.today()
    befejezes = kezdes + timedelta(days=30 * projekt_ido_honap)

    uj_projekt = Varosfejlesztes(len(varosfejlesztes_list) + 1, nev, koltseg, kezdes.strftime("%Y.%m.%d"), befejezes.strftime("%Y.%m.%d"))
    varosfejlesztes_list.append(uj_projekt)

    print(f"Új projekt indult: {nev}, befejezés várhatóan {befejezes.strftime('%Y.%m.%d')}.")

    havi_koltseg = koltseg // projekt_ido_honap
    for _ in range(projekt_ido_honap):
        penzkeret -= havi_koltseg
        if penzkeret < 0:
            penzkeret = 0
            print("Elfogyott a pénzkeret!")
            break

    epitesi_ev = befejezes.year
    uj_epulet = Epuletek(len(epuletek_list) + 1, nev, tipus, epitesi_ev, hasznos_terulet_m2)
    epuletek_list.append(uj_epulet)

    print(f"Az épület elkészült: {uj_epulet.nev}, {uj_epulet.hasznos_terulet_m2} m2, {uj_epulet.tipus}, építés éve: {epitesi_ev}.")
    
    if tipus.lower() == "lakóház":
        uj_lakosok = hasznos_terulet_m2 // 30
        lakosok_szama += uj_lakosok
        print(f"+{uj_lakosok} új lakos érkezett.")

    lakosok_elegedettsege = min(lakosok_elegedettsege + random.randint(1, 10), 100)
    
    print(f"Lakosok elégedettsége: {lakosok_elegedettsege}%")
    print(f"Pénzkeret: {penzkeret} arany")

# #Fő program
# while True:
#     valasztas = input("\nMit szeretnél csinálni? (1: Új épület építése, 0: Kilépés): ")
#     if valasztas == "1":
#         uj_epulet_epitese()
#     elif valasztas == "0":
#         print("Kilépés...")
#         break
#     else:
#         print("Érvénytelen választás, próbáld újra!")
