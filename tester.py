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

    def __repr__(self):
            return f"Lakosok(projekt_azon={self.projekt_azon}, nev={self.nev}, koltseg(arany)={self.koltseg_arany}, kezdes={self.kezdes}, befejezes={self.befejezes})"
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

leendo_epuletek = []

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

    leendo_epuletek.append({
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





javitando_epuletek = []
def karbantartas():
    global penzkeret, lakosok_elegedettsege
    print("\n--- Karbantartás meglévő épületeken ---")
    # Ha nincs épület, nincs mit karbantartani
    if not epuletek_list:
        print("Nincsenek karbantartásra szoruló épületek!")
        return
    # Meglévő épületek listázása
    print("Válassz egy épületet karbantartásra:")
    for i, epulet in enumerate(epuletek_list, start=1):
        print(f"{i}. {epulet.nev} ({epulet.tipus}) - {epulet.hasznos_terulet_m2} m²: {epulet.allapot}")
    # Felhasználói választás
    try:
        valasztott_index = int(input("Írd be az épület számát: ")) - 1
        if valasztott_index < 0 or valasztott_index >= len(epuletek_list):
            print("Érvénytelen választás.")
            return
    except ValueError:
        print("Hibás bemenet, számot adj meg!")
        return
    epulet = epuletek_list[valasztott_index]
    koltseg = int(input("💰 Projekt költsége: "))
    projekt_ido_honap = random.randint(1, 6)
    if penzkeret < koltseg:
        print("Nincs elég pénzed a karbantartásra!")
        return
    kezdes = kezdo_datum

    befejezes = kezdes + relativedelta(months=projekt_ido_honap)

    havi_koltseg = koltseg // projekt_ido_honap

    nev = epulet.nev

    tipus = epulet.tipus

    hasznos_terulet_m2 = epulet.hasznos_terulet_m2

    javitando_epuletek.append({
        "nev": nev,
        "tipus": tipus,
        "epitesi_ev": befejezes.year,
        "hasznos_terulet_m2": hasznos_terulet_m2,
        "befejezes": befejezes,
        "havi_koltseg": havi_koltseg,
        "hatralevo_honap": projekt_ido_honap
    })
    print(f"Karbantartási projekt indult: {epulet.nev}, befejezés várhatóan {befejezes.strftime('%Y.%m.%d')}.")
    print(f"📉 Havonta levonásra kerül: {havi_koltseg} arany.")
    

def mentes_fajlba():
    fajlnev = "varos_naplo.txt"
     # Az aktuális dátum és idő beszúrása a naplóba
    idobelyeg = datetime.strftime(kezdo_datum, "%Y-%m-%d")
    with open(fajlnev, "a", encoding="utf-8") as fajl:
        fajl.write(f"\n=== {idobelyeg} - Forduló vége ===\n")
        # Események kiírása, ha van
        # if esemenyek:
        #     fajl.write("\nEsemények:\n")
        #     for esemeny in esemenyek:
        #         fajl.write(f"- {esemeny}\n")
        # else:
        #     fajl.write("\nNincs új esemény ebben a fordulóban.\n")

        # Város állapota
        fajl.write("\nVáros aktuális állapota:\n")
        fajl.write(f"- Lakosság elégedettsége: {lakosok_elegedettsege}%\n")
        fajl.write(f"- Rendelkezésre álló pénzkeret: {penzkeret} arany\n")

        # Épületek állapotának listázása
        fajl.write("\nÉpületek állapota:\n")
        for epulet in epuletek_list:
            fajl.write(f"- {epulet.nev} (Típus: {epulet.tipus}, Állapot: {epulet.allapot})\n")

        fajl.write("\n" + "="*40 + "\n")

    print(f"A jelenlegi forduló adatai elmentve: {fajlnev}")


epuletek_allapota = []
for ep in epuletek_list:
    epuletek_allapota.append(ep.allapot)

    

###Futatható szimuláció

for honap in range(fordulok_szama):
    havi_koltseg = sum(szolg.havi_koltseg for szolg in szolgaltatasok_list)
    penzkeret -= havi_koltseg
    print(f"\n=== {kezdo_datum.strftime('%Y-%m')} hónap kezdete ===")
    if penzkeret <= 0:
        print("\n A város csődbe ment! Nincs több pénz fejlesztésre.")
        break
    
    if lakosok_elegedettsege < min_elegedettseg:
        print("\n A lakosok túl elégedetlenek! A városvezetést leváltották.")
        break

    for project in leendo_epuletek:
        if project["hatralevo_honap"] > 0:
            penzkeret -= project["havi_koltseg"]
            project["hatralevo_honap"] -= 1
    
    for project in javitando_epuletek:
        if project["hatralevo_honap"] > 0:
            penzkeret -= project["havi_koltseg"]
            project["hatralevo_honap"] -= 1

    elkeszult_projektek = [p for p in leendo_epuletek if p["befejezes"] <= kezdo_datum]

    for project in elkeszult_projektek:
        uj_epulet = Epuletek(len(epuletek_list) + 1, project["nev"], project["tipus"], project["epitesi_ev"], project["hasznos_terulet_m2"])
        epuletek_list.append(uj_epulet)

        lakosok_elegedettsege = min(lakosok_elegedettsege + random.randint(1, 10), 100)

        print(f"✅ Elkészült épület: {uj_epulet.nev}, {uj_epulet.hasznos_terulet_m2} m², {uj_epulet.tipus}.")

    
        if project["tipus"].lower() == "lakóház":
            uj_lakosok = project["hasznos_terulet_m2"] // 30
            lakosok_szama += uj_lakosok
            print(f"🏠 +{uj_lakosok} új lakos érkezett!")


    javitando_epuletek = [k for k in javitando_epuletek if k["befejezes"] > kezdo_datum]

    for project in javitando_epuletek:
        for epulet in epuletek_list:
            if epulet.nev == project["nev"]:
                epulet.allapot = min(epulet.allapot + random.randint(1, 5), 5) 
                print(f"✅ Karbantartás befejezve: {epulet.nev}, új állapot: {epulet.allapot}")
                break
        lakosok_elegedettsege = min(lakosok_elegedettsege + random.randint(1, 10), 100)

    javitando_epuletek = [k for k in javitando_epuletek if k["befejezes"] > kezdo_datum]

    
    print(f"Havi fenntartási költségek: {havi_koltseg} arany")
    print(f"🏗️ Építkezési költségek ebben a hónapban: {sum(p['havi_koltseg'] for p in leendo_epuletek if p['hatralevo_honap'] > 0)} arany")
    print(f"🏗️ Karbantartási költségek ebben a hónapban: {sum(k['havi_koltseg'] for k in javitando_epuletek if k['hatralevo_honap'] > 0)} arany")
    print(f"💰 Maradék pénzkeret: {penzkeret} arany")
    valtozas = int(input("🔄 0: Kihagy | 1: Építés | 2: Karbantarás: "))
    if valtozas == 0:
        continue
    elif valtozas == 1:
        uj_epulet_epitese()
    elif valtozas == 2: 
        karbantartas()
    kezdo_datum += relativedelta(months=1)
    mentes_fajlba()

print("\n🏁 A szimuláció véget ért!")
