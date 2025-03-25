import csv
import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

#kiinduló paraméterek
penzkeret = int(input("💰 Add meg az induló pénzkeretet (100000+ ajánlott): "))
lakosok_elegedettsege = int(input("😊 Add meg a lakosok induló elégedettségét (1-99): "))
min_elegedettseg = int(input(f"📉 Add meg az elvárt minimális elégedettséget (1-{lakosok_elegedettsege-1}): "))

kezdo_datum = input("📅 Add meg a szimuláció kezdő dátumát (YYYY-MM-DD): ")
kezdo_datum = datetime.strptime(kezdo_datum, "%Y-%m-%d")

fordulok_szama = int(input("🔄 Add meg a szimuláció hosszát (hónapokban): "))

print("\n--- Szimulációs beállítások ---")
print(f"💰 Pénzkeret: {penzkeret} arany")
print(f"😊 Lakosok elégedettsége: {lakosok_elegedettsege}%")
print(f"📉 Minimális elégedettség: {min_elegedettseg}%")
print(f"📅 Kezdő dátum: {kezdo_datum.strftime('%Y-%m-%d')}")
print(f"🔄 Fordulók száma: {fordulok_szama}")

#osztályok, adatbeolvasás

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


class Lakosok:
    def __init__(self, lakos_azon, nev, szuletesi_ev, foglalkozas, ep_azon):
        self.lakos_azon = int(lakos_azon)
        self.nev = nev
        self.szuletesi_ev = int(szuletesi_ev)
        self.foglalkozas = foglalkozas
        self.ep_azon = int(ep_azon)

    def __repr__(self):
        return f"Lakosok(lakos_azon={self.lakos_azon}, nev={self.nev}, szuletesi_ev={self.szuletesi_ev}, foglalkozas={self.foglalkozas}, ep_azon={self.ep_azon})"


class Varosfejlesztes:
    def __init__(self, projekt_azon, nev, koltseg_arany, kezdes, befejezes):
        self.projekt_azon = int(projekt_azon)
        self.nev = nev
        self.koltseg_arany = int(koltseg_arany)
        self.kezdes = datetime.strptime(kezdes.split()[0], "%Y.%m.%d").date()
        self.befejezes = datetime.strptime(befejezes.split()[0], "%Y.%m.%d").date()


class Szolgaltatasok:
    def __init__(self, szolg_azon, nev, tipus, ep_azon):
        self.szolg_azon = int(szolg_azon)
        self.nev = nev
        self.tipus = tipus
        self.ep_azon = int(ep_azon)
        self.havi_koltseg = random.randint(500, 3500)

    def __repr__(self):
        return f"Szolgaltatasok(szolg_azon={self.szolg_azon}, nev={self.nev}, tipus={self.tipus}, ep_azon={self.ep_azon}, havi_koltseg={self.havi_koltseg})"


#Opciónális funkció, jobban betölti az adatokat

def load_data(filename, cls):
    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        data = list(reader)
    return [cls(*row[0].split(";")) for row in data[1:]]

epuletek_list = load_data("Epuletek.csv", Epuletek)
lakosok_list = load_data("Lakosok.csv", Lakosok)
varosfejlesztes_list = load_data("Varosfejlesztes.csv", Varosfejlesztes)
szolgaltatasok_list = load_data("Szolgaltatasok.csv", Szolgaltatasok)

lakosok_szama = len(lakosok_list)

###Új Épület építése

construction_projects = []

def uj_epulet_epitese():
    global penzkeret
    
    print("\n--- Új épület építése ---")
    nev = input("🏗️ Épület neve: ").strip()
    tipus = input("🏢 Épület típusa (lakóház, iroda, stb.): ").strip()
    
    try:
        hasznos_terulet_m2 = int(input("📏 Hasznos terület (m²): ").strip())
    except ValueError:
        print("❌ Hibás bemenet! Kérlek, számot adj meg.")
        return
    
    koltseg = int(input("💰 Projekt költsége: ").strip())  
    projekt_ido_honap = random.randint(3, 12)

    if penzkeret < koltseg:
        print("❌ Nincs elég pénzed az építéshez!")
        return
    
    kezdes = kezdo_datum
    befejezes = kezdes + relativedelta(months=projekt_ido_honap)

    havi_koltseg = koltseg // projekt_ido_honap

    construction_projects.append({
        "nev": nev,
        "tipus": tipus,
        "epitesi_ev": befejezes.year,
        "hasznos_terulet_m2": hasznos_terulet_m2,
        "befejezes": befejezes,
        "havi_koltseg": havi_koltseg,
        "hatralevo_honap": projekt_ido_honap 
    })

    print(f"🏗️ Építkezés elkezdődött: {nev}, várható befejezés: {befejezes.strftime('%Y.%m.%d')}.")
    print(f"📉 Havonta levonásra kerül: {havi_koltseg} arany.")


###Futatható szimuláció

for honap in range(fordulok_szama):
    print(f"\n=== {kezdo_datum.strftime('%Y-%m')} hónap kezdete ===")

    for project in construction_projects:
        if project["hatralevo_honap"] > 0:
            penzkeret -= project["havi_koltseg"]
            project["hatralevo_honap"] -= 1

    havi_koltseg = sum(szolg.havi_koltseg for szolg in szolgaltatasok_list)
    penzkeret -= havi_koltseg

    print(f"Havi fenntartási költségek: {havi_koltseg} arany")
    print(f"🏗️ Építkezési költségek ebben a hónapban: {sum(p['havi_koltseg'] for p in construction_projects if p['hatralevo_honap'] > 0)} arany")
    print(f"💰 Maradék pénzkeret: {penzkeret} arany")

    valtozas = int(input("🔄 0: Kihagy | 1: Építés: "))
    if valtozas == 1:
        uj_epulet_epitese()

    completed_projects = [p for p in construction_projects if p["befejezes"] <= kezdo_datum]

    for project in completed_projects:
        uj_epulet = Epuletek(len(epuletek_list) + 1, project["nev"], project["tipus"], project["epitesi_ev"], project["hasznos_terulet_m2"])
        epuletek_list.append(uj_epulet)

        lakosok_elegedettsege = min(lakosok_elegedettsege + random.randint(1, 10), 100)

        print(f"✅ Elkészült épület: {uj_epulet.nev}, {uj_epulet.hasznos_terulet_m2} m², {uj_epulet.tipus}.")

    
        if project["tipus"].lower() == "lakóház":
            uj_lakosok = project["hasznos_terulet_m2"] // 30
            lakosok_szama += uj_lakosok
            print(f"🏠 +{uj_lakosok} új lakos érkezett!")


    construction_projects = [p for p in construction_projects if p["befejezes"] > kezdo_datum]

    kezdo_datum += relativedelta(months=1)

print("\n🏁 A szimuláció véget ért!")

