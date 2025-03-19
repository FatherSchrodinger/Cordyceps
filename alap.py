#alap adatok beolvasása:
############################################################################################################
epuletek = open("epuletek.csv","r",encoding="utf8")
lakosok = open("lakosok.csv","r",encoding="utf8")
services = open("szolgaltatasok.csv","r",encoding="utf8")
varosfejl = open("varosfejlesztes.csv","r",encoding="utf8")
##############################
temp = epuletek.readline()
temp1 = temp.split(";")
#print (temp.split(";"))
for i in epuletek:
    temp = epuletek.readline()
    temp1 = temp.split(";")
    for i in temp1:
        print ("i= ",i)
##############################
temp = lakosok.readline()
temp1 = temp.split(";")
print (temp.split(";"))
##############################
temp = services.readline()
temp1 = temp.split(";")
print (temp.split(";"))
##############################
temp = varosfejl.readline()
temp1 = temp.split(";")
print (temp.split(";"))
############################################################################################################

#egyenlőre mindent int-re írtam be, de lehet némelyiket tömbbé/listává kell alakítani

#lakosok elégedettsége 0-100 érték, akár "%" is lehet

moral = 1
if moral > 100:
    print ("az elégedettség nem lehet ilyen értékű")
if moral < 1:
    print ("paraszt lázadás")

#kincstár, a város egyenlege

kincstar = int

#épületek állapota 1-5 skálán

bstatus = 1
if bstatus > 5:
    print ("az épület nem lehet ilyen értékű")
if  bstatus < 1:
    print ("OSHA violation")

#szolgáltatások költségvetése

serviscost = int