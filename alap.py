#alap adatok:
############################################################################################################
epuletek = open("epuletek.csv")
lakosok = open("lakosok.csv")
services = open("szolgaltatasok")
varosfejl = open("varosfejlesztes.csv")

############################################################################################################

#egyenlőre mindent int-re írtam be, de lehet némelyiket tömbbé/listává kell alakítani

#lakosok elégedettsége 0-100 érték, akár "%" is lehet

moral = int

#kincstár, a város egyenlege

kincstar = int

#épületek állapota 1-5 skálán

bstatus = int

#szolgáltatások költségvetése

serviscost = int