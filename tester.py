import csv
import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

while True:
    penzkeret = int(input("💰 Add meg az induló pénzkeretet (100000+ arany ajánlott): "))
    if penzkeret <= 0:
        print("Egy 0-nál nagyobb egész számot adj meg.")
        continue

    try:
        lakosok_elegedettsege = int(input("😊 Add meg a lakosok induló elégedettségét (1-99): "))
        if lakosok_elegedettsege <= 0 or lakosok_elegedettsege > 99:
            print("Egy 0 és 100 közötti egész számot adj meg.")
            continue
    except ValueError:
        print("Egy 0 és 100 közötti egész számot adj meg.")
        continue

    try:
        min_elegedettseg = int(input(f"📉 Add meg az elvárt minimális elégedettséget (1-{lakosok_elegedettsege-1}): "))
        if min_elegedettseg <= 0 or min_elegedettseg >= lakosok_elegedettsege:
            print("Egy 0-nál nagyobb számot adj meg, ami kisebb, mint a lakosok induló elégedettsége.")
            continue
    except ValueError:
        print("Egy 0-nál nagyobb számot adj meg, ami kisebb, mint a lakosok induló elégedettsége.")
        continue

    while True:
        kezdo_datum = input("📅 Add meg a szimuláció kezdő dátumát (YYYY-MM-DD): ")
        try:
            kezdo_datum = datetime.strptime(kezdo_datum, "%Y-%m-%d")
            break
        except ValueError:
            print("Érvénytelen dátum formátum. Használj YYYY-MM-DD formátumot.")

    try:
        fordulok_szama = int(input("🔄 Add meg a szimuláció hosszát (hónapokban): "))
        if fordulok_szama <= 0:
            print("Adja meg a szimuláció hosszát egy pozitív egész számként.")
            continue
    except ValueError:
        print("Egy 0-nál nagyobb egész számot adj meg.")
        continue

    break

print("\n--- Szimulációs beállítások ---")
print(f"💰 Pénzkeret: {penzkeret} arany")
print(f"😊 Lakosok elégedettsége: {lakosok_elegedettsege}%")
print(f"📉 Minimális elégedettség: {min_elegedettseg}%")
print(f"📅 Kezdő dátum: {kezdo_datum.strftime('%Y-%m-%d')}")
print(f"🔄 Fordulók száma: {fordulok_szama}")

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
        return f"Varosfejlesztes(projekt_azon={self.projekt_azon}, nev={self.nev}, koltseg(arany)={self.koltseg_arany}, kezdes={self.kezdes}, befejezes={self.befejezes})"

class Szolgaltatasok:
    def __init__(self, szolg_azon, nev, tipus, ep_azon):
        self.szolg_azon = int(szolg_azon)
        self.nev = nev
        self.tipus = tipus
        self.ep_azon = int(ep_azon)
        self.havi_koltseg = random.randint(500, 3500)



    def __repr__(self):
        return f"Szolgaltatasok(szolg_azon={self.szolg_azon}, nev={self.nev}, tipus={self.tipus}, ep_azon={self.ep_azon}, havi_koltseg={self.havi_koltseg})"

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



def ep_azon_generálása():
    letezo_idk = {epulet.ep_azon for epulet in epuletek_list}

    while True:
        uj_id = random.randint(100, 999)
        if uj_id not in letezo_idk:
            return uj_id

leendo_epuletek = []

def uj_epulet_epitese():
    global penzkeret

    print("\n--- Új épület építése ---")
    while True:
        ep_azon = ep_azon_generálása()
        nev = input("🏗️ Épület neve: ").strip().capitalize()
        if not nev:
            print("❌ Hibás bemenet! Kérlek, adj meg egy érvényes nevet az épületnek.")
            continue
        tipus = input("🏢 Épület típusa (lakóház, iroda, stb.): ").strip().capitalize()
        if not tipus:
            print("❌ Hibás bemenet! Kérlek, adj meg egy érvényes épülettípust.")
            continue
        try:
            hasznos_terulet_m2 = int(input("📏 Hasznos terület (m²): ").strip())
            if hasznos_terulet_m2 <= 0:
                print("❌ Hibás bemenet! Kérlek, adj meg egy pozitív egész számot.")
                continue
        except ValueError:
            print("❌ Hibás bemenet! Kérlek, számot adj meg.")
            continue
        try:
            koltseg = int(input("💰 Projekt költsége: ").strip())
            if koltseg <= 0:
                print("❌ Hibás bemenet! A költségnek 0-nál nagyobbnak kell lennie.")
                continue
        except ValueError:
            print("❌ Hibás bemenet! Kérlek, számot adj meg.")
            continue
        projekt_ido_honap = random.randint(3, 12)

        if penzkeret < koltseg:
            print("❌ Nincs elég pénzed az építéshez!")
            continue

        kezdes = kezdo_datum
        befejezes = kezdes + relativedelta(months=projekt_ido_honap)
        havi_koltseg = koltseg // projekt_ido_honap

        leendo_epuletek.append({
            "ep_azon": ep_azon,
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
        break




javitando_epuletek = []
def karbantartas():
    global penzkeret, lakosok_elegedettsege

    print("\n--- Karbantartás meglévő épületeken ---")
    while True:
        if not epuletek_list:
            print("❌ Nincsenek karbantartásra szoruló épületek!")
            continue
        print("🔧 Válassz egy épületet karbantartásra:")
        for i, epulet in enumerate(epuletek_list, start=1):
            print(f"{i}. {epulet.nev} ({epulet.tipus}) - {epulet.hasznos_terulet_m2} m² | Állapot: {epulet.allapot}/5")

        try:
            valasztott_index = int(input("🏗️ Írd be az épület számát: ")) - 1
            if valasztott_index < 0 or valasztott_index >= len(epuletek_list):
                print("❌ Érvénytelen választás.")
                continue
        except ValueError:
            print("❌ Hibás bemenet! Számot adj meg.")
            continue

        epulet = epuletek_list[valasztott_index]
        try:
            koltseg = int(input("💰 Projekt költsége: "))
            if koltseg <= 0:
                print("Egy 0-nál nagyobb egész számot adj meg.")
                continue
        except ValueError:
            print("Egy 0-nál nagyobb egész számot adj meg.")
        projekt_ido_honap = random.randint(1, 6)

        if penzkeret < koltseg:
            print("❌ Nincs elég pénzed a karbantartásra!")
            continue

        kezdes = kezdo_datum
        befejezes = kezdes + relativedelta(months=projekt_ido_honap)

        havi_koltseg = koltseg // projekt_ido_honap

        javitando_epuletek.append({
            "nev": epulet.nev,
            "tipus": epulet.tipus,
            "epitesi_ev": epulet.epites_eve,
            "hasznos_terulet_m2": epulet.hasznos_terulet_m2,
            "befejezes": befejezes,
            "havi_koltseg": havi_koltseg,
            "hatralevo_honap": projekt_ido_honap
        })

        print(f"🔧 Karbantartási projekt indult: {epulet.nev}, befejezés várhatóan {befejezes.strftime('%Y.%m.%d')}.")
        print(f"📉 Havonta levonásra kerül: {havi_koltseg} arany.")
        break

def szolgaltatas_bevezetese():
    global penzkeret, szolgaltatasok_list, lakosok_elegedettsege
    epuletek_azonositoi = []
    print("\n--- Új szolgáltatás létrehozása ---")
    while True:
        for i, epulet in enumerate(epuletek_list, start=1):
            epuletek_azonositoi.append(i)
            print(f"{i}. {epulet.nev} ({epulet.tipus}) - ID: {epulet.ep_azon}")

        try:
            uzemelteto_epulet = int(input("Adja meg a szolgáltatás üzemeltető épületét (ID): ").strip())
            if uzemelteto_epulet not in epuletek_azonositoi:
                print("❌ Hibás bemenet! Kérlek, egy létező számot adj meg.")
                continue
        except ValueError:
            print("❌ Hibás bemenet! Kérlek, egy létező számot adj meg.")
            continue
        nev = input("🏗️ Szolgáltatás neve: ").strip().capitalize()
        if not nev:
            print("❌ Hibás bemenet! Kérlek, egy nevet adj meg az épületnek.")
            continue
        tipus = input("🏢 Szolgáltatás típusa (egészségügy, oktatás, stb.): ").strip().capitalize()
        if not tipus:
                print("❌ Hibás bemenet! Kérlek, adj meg egy érvényes szolgáltatástípust.")
                continue
        try:
            havi_koltseg = int(input("💰 Szolgáltatás havi költsége: ").strip())
        except ValueError:
            print("❌ Hibás bemenet! Kérlek, számot adj meg.")
            continue

        uj_szolg_id = max((szolg.szolg_azon for szolg in szolgaltatasok_list), default=0) + 1

        uj_szolgaltatas = Szolgaltatasok(uj_szolg_id, nev, tipus, uzemelteto_epulet)
        uj_szolgaltatas.havi_koltseg = havi_koltseg

        szolgaltatasok_list.append(uj_szolgaltatas)

        lakosok_elegedettsege = min(lakosok_elegedettsege + random.randint(1, 10), 100)

        print(f"✅ Új szolgáltatás létrehozva: {nev} ({tipus}), üzemeltető épület ID: {uzemelteto_epulet}")
        print(f"📉 Havonta levonásra kerül: {havi_koltseg} arany.")
        break


def szolgaltatas_torlese():
    global szolgaltatasok_list, lakosok_elegedettsege
    while True:
        if not szolgaltatasok_list:
            print("❌ Nincs elérhető szolgáltatás a törléshez!")
            continue
        print("\n--- Szolgáltatás törlése ---")
        for i, szolg in enumerate(szolgaltatasok_list, start=1):
            print(f"{i}. {szolg.nev} ({szolg.tipus}) - Havi költség: {szolg.havi_koltseg} arany")
        try:
            valasztott_index = int(input("Válassz egy szolgáltatást törlésre (szám): ")) - 1
            if valasztott_index < 0 or valasztott_index >= len(szolgaltatasok_list):
                print("❌ Érvénytelen választás!")
                continue
        except ValueError:
            print("❌ Hibás bemenet! Számot adj meg.")
            continue
        torolt_szolgaltatas = szolgaltatasok_list.pop(valasztott_index)
        print(f"🗑️ A(z) {torolt_szolgaltatas.nev} szolgáltatás törölve lett.")
        csokkenes = random.randint(5, 15)
        lakosok_elegedettsege = max(lakosok_elegedettsege - csokkenes, 0)
        print(f"📉 Lakosok elégedettsége csökkent: -{csokkenes}% (Új érték: {lakosok_elegedettsege}%)")
        aktualis_havi_koltseg = sum(szolg.havi_koltseg for szolg in szolgaltatasok_list)
        print(f"📊 Új havi fenntartási költség: {aktualis_havi_koltseg} arany")
        break

import random

esemenyek = [
    {"nev": "Nem történt semmi", "valoszinuseg": 0.4, "penz_valtozas": 0, "elegedettseg_valtozas": 0, "epulet_kar": None, "leiras": "Nincs változás."},
    {"nev": "Fellázadás", "valoszinuseg": 0.08, "penz_valtozas": -10000, "elegedettseg_valtozas": -20, "epulet_kar": None, "leiras": "A lakosság fellázad, ami pénzügyi és elégedettségi csökkenést okoz."},
    {"nev": "Tornádó", "valoszinuseg": 0.05, "penz_valtozas": -15000, "elegedettseg_valtozas": -30, "epulet_kar": "random", "leiras": "Tornádó pusztítást végez, és károkat okozhat az épületekben."},
    {"nev": "Csatorna törés", "valoszinuseg": 0.15, "penz_valtozas": -5000, "elegedettseg_valtozas": -10, "epulet_kar": None, "leiras": "A csatornarendszer törése problémákat okoz, és pénzügyi kárt."},
    {"nev": "Erdőtűz", "valoszinuseg": 0.1, "penz_valtozas": -8000, "elegedettseg_valtozas": -15, "epulet_kar": "random", "leiras": "Erdőtűz keletkezik, ami pénzügyi veszteséget és elégedettségcsökkenést okoz."},
    {"nev": "Arany eső", "valoszinuseg": 0.12, "penz_valtozas": +15000, "elegedettseg_valtozas": +5, "epulet_kar": None, "leiras": "Arany eső hull, ami gazdasági növekedést és enyhe elégedettség növekedést eredményez."},
    {"nev": "Földrengés", "valoszinuseg": 0.05, "penz_valtozas": -20000, "elegedettseg_valtozas": -40, "epulet_kar": "random", "leiras": "Földrengés következik be, mely súlyos károkat és magas pénzügyi veszteséget okoz."},
    {"nev": "Anti-Krisztus", "valoszinuseg": 0.02, "penz_valtozas": 0, "elegedettseg_valtozas": -100, "epulet_kar": None, "leiras": "Az Anti-Krisztus megjelenése mély szellemi válságot és elégedettségvesztést okoz."},
    {"nev": "Idegen invázió", "valoszinuseg": 0.03, "penz_valtozas": "random", "elegedettseg_valtozas": -10, "epulet_kar": "random", "leiras": "Idegenek inváziója következik, amely károkat okozhat mind anyagi, mind szellemi szinten."}
]


osszes_valoszinuseg = sum(e["valoszinuseg"] for e in esemenyek)
if abs(osszes_valoszinuseg - 1.0) > 0.0001:
    raise ValueError("Az események valószínűségeinek összege nem 1! Jelenlegi érték: " + str(osszes_valoszinuseg))

import random

def varatlan_esemeny():
    global penzkeret, lakosok_elegedettsege, epuletek_list

    esemeny = random.choices(esemenyek, weights=[e["valoszinuseg"] for e in esemenyek])[0]

    if esemeny["nev"] == "Nem történt semmi":
        print("\n✅ Ebben a hónapban nem történt semmi.")
        return

    print(f"\n🌟 *** {esemeny['nev']} történt! ***")
    print(esemeny["leiras"])

    penz_valtozas = esemeny.get("penz_valtozas", 0)
    if penz_valtozas == "random":
        penz_valtozas = random.randint(-20000, 20000)
    penzkeret += penz_valtozas

    lakosok_elegedettsege += esemeny.get("elegedettseg_valtozas", 0)
    lakosok_elegedettsege = max(0, min(100, lakosok_elegedettsege))

    if "epulet_kar" in esemeny and esemeny["epulet_kar"] and epuletek_list:
        if esemeny["epulet_kar"] == "egy":
            serult_epuletek = [random.choice(epuletek_list)]
        elif esemeny["epulet_kar"] == "tobb":
            serult_epuletek = random.sample(epuletek_list, min(len(epuletek_list), random.randint(1, 3)))
        else:
            serult_epuletek = []

        for epulet in serult_epuletek:
            serult_mertek = random.randint(1, 3)
            epulet.allapot = max(1, epulet.allapot - serult_mertek)

            print(f"🏚️ A(z) {epulet.nev} állapota {serult_mertek} ponttal romlott! Új állapot: {epulet.allapot}/5")

            if epulet.allapot == 1:
                epuletek_list.remove(epulet)
                print(f"💥 A(z) {epulet.nev} teljesen megsemmisült és eltűnt a városból!")

    if esemeny["nev"] == "Anti-Krisztus":
        print("💀 A világ elpusztult! A játék véget ért!")
        exit()

    print(f"💰 Pénzkeret: {penzkeret} arany")
    print(f"😊 Lakosok elégedettsége: {lakosok_elegedettsege}%")

    return esemeny


def mentes_fajlba():
    fajlnev = "varos_naplo.txt"
    idobelyeg = datetime.strftime(kezdo_datum, "%Y-%m-%d")
    with open(fajlnev, "a", encoding="utf-8") as fajl:
        fajl.write(f"\n=== {idobelyeg} - Forduló vége ===\n")
        if esemenyek:
            fajl.write("\nEsemény:\n")
            fajl.write(f"- {utolso_esemeny}\n")
        else:
            fajl.write("\nNincs új esemény ebben a fordulóban.\n")

        fajl.write("\nVáros aktuális állapota:\n")
        fajl.write(f"- Lakosság elégedettsége: {lakosok_elegedettsege}%\n")
        fajl.write(f"- Rendelkezésre álló pénzkeret: {penzkeret} arany\n")

        fajl.write("\nÉpületek állapota:\n")
        for epulet in epuletek_list:
            fajl.write(f"- {epulet.nev} (Típus: {epulet.tipus}, Állapot: {epulet.allapot})\n")

        fajl.write("\n" + "="*40 + "\n")

    print(f"A jelenlegi forduló adatai elmentve: {fajlnev}")


epuletek_allapota = []
for ep in epuletek_list:
    epuletek_allapota.append(ep.allapot)



if penzkeret > 0 and lakosok_elegedettsege > min_elegedettseg and lakosok_elegedettsege < 100:
    for honap in range(fordulok_szama):
        havi_koltseg = sum(szolg.havi_koltseg for szolg in szolgaltatasok_list)
        penzkeret -= havi_koltseg

        print(f"\n=== {kezdo_datum.strftime('%Y-%m')} hónap kezdete ===")
        utolso_esemeny = varatlan_esemeny()

        for project in leendo_epuletek + javitando_epuletek:
            if project["hatralevo_honap"] > 0:
                penzkeret -= project["havi_koltseg"]
                project["hatralevo_honap"] -= 1

        elkeszult_projektek = [p for p in leendo_epuletek if p["befejezes"] <= kezdo_datum]
        for project in elkeszult_projektek:
            uj_epulet = Epuletek(project["ep_azon"], project["nev"], project["tipus"], project["epitesi_ev"], project["hasznos_terulet_m2"])
            epuletek_list.append(uj_epulet)
            lakosok_elegedettsege = min(lakosok_elegedettsege + random.randint(1, 10), 100)
            print(f"✅ Elkészült épület: {uj_epulet.nev}, {uj_epulet.hasznos_terulet_m2} m², {uj_epulet.tipus}.")

            if project["tipus"].lower() == "lakóház":
                uj_lakosok = project["hasznos_terulet_m2"] // 30
                lakosok_szama += uj_lakosok
                print(f"🏠 +{uj_lakosok} új lakos érkezett!")

        completed_repairs = [p for p in javitando_epuletek if p["befejezes"] <= kezdo_datum]
        for project in completed_repairs:
            for epulet in epuletek_list:
                if epulet.nev == project["nev"]:
                    epulet.allapot = min(epulet.allapot + random.randint(1, 5), 5)
                    print(f"✅ Karbantartás befejezve: {epulet.nev}, új állapot: {epulet.allapot}/5")
                    break
            lakosok_elegedettsege = min(lakosok_elegedettsege + random.randint(1, 10), 100)
        javitando_epuletek = [k for k in javitando_epuletek if k["befejezes"] > kezdo_datum]

        epitesi_koltseg = sum(p['havi_koltseg'] for p in leendo_epuletek if p['hatralevo_honap'] > 0)
        karbantartasi_koltseg = sum(k['havi_koltseg'] for k in javitando_epuletek if k['hatralevo_honap'] > 0)
        penzkeret -= epitesi_koltseg + karbantartasi_koltseg
        if penzkeret <= 0:
            print("\n💥 A város csődbe ment!")
            break
        if lakosok_elegedettsege <= min_elegedettseg:
            print("\n😡 A lakosok elégedetlensége miatt zavargások törtek ki! A városvezetés megbukott.")
            break
        if lakosok_elegedettsege >= 100:
            print("\n🎉A lakosok elégedettsége elérte a 100%-ot! A polgárok örömmel ünnepelnek, és mindenki bizakodva tekint a jövőbe. Gratulálunk! 🎊")
            break
        print(f"Havi fenntartási költségek: {havi_koltseg} arany")
        print(f"🏗️ Építkezési költségek ebben a hónapban: {epitesi_koltseg} arany")
        print(f"🔧 Karbantartási költségek ebben a hónapban: {karbantartasi_koltseg} arany")
        print(f"Lakosok elégedettsége: {lakosok_elegedettsege}%")
        print(f" A város lakossága: {lakosok_szama} fő")
        print(f"💰 Maradék pénzkeret: {penzkeret} arany")


        kezdo_datum += relativedelta(months=1).normalized()
        mentes_fajlba()

        while True:
            try:
                valtozas = int(input("🔄 0: Kihagy | 1: Építés | 2: Karbantartás | 3: Szolgáltatás bevezetése | 4: Szolgáltatás törlése | 5: Kilépés: "))
                
                if valtozas == 0:
                    break
                elif valtozas == 1:
                    uj_epulet_epitese()
                elif valtozas == 2:
                    karbantartas()
                elif valtozas == 3:
                    szolgaltatas_bevezetese()
                elif valtozas == 4:
                    szolgaltatas_torlese()
                elif valtozas == 5:
                    print("🚪 Kilépés a szimulációból.")
                    exit()
                else:
                    print("❌ Érvénytelen választás!")
            except ValueError:
                print("❌ Érvénytelen választás!")
        
else:
    print("\n A város csődbe ment!")


print("\n🏁 A szimuláció véget ért!")