import utils
from datetime import date

# Cílová částka = vklady účastníka + úroky z vkladů - daň z úroků +
#   + státní podpora + úroky ze státní podpory (následující roky) - poplatky účtu


urok_procento = 1.2
urok = urok_procento/100

dan_procento = 15
dan = dan_procento/100

poplatek_mesic = 27
poplatky_ucet_rok = poplatek_mesic * 12


data = utils.nacist_soubor()
roky = utils.ziskat_roky(data)
data_rok = {}
celkem_stavebni_sporeni = 0
zaklad_statni_podpora = 0
celkem_vklady = 0

for i in roky:
    data_rok[i] = utils.ziskat_vklady_rok(data, i)

for rok in roky:
    print("==============================================================================================")
    print(f"Rok {rok}")
    if data_rok[rok][0][0].month != 1:
        urok_vklady = utils.vypocet_uroku_rok(data_rok[rok], poplatek_mesic, urok, prvni_mesic=data_rok[rok][0][0].month)
        poplatky_ucet_rok = (12 - data_rok[rok][0][0].month + 1) * poplatek_mesic
        celkem_stavebni_sporeni += utils.celkem_rok(data_rok[rok], poplatky_ucet_rok, urok_vklady, dan)
    else:
        urok_rok = utils.vypocet_uroku_rok(data_rok[rok], poplatek_mesic, urok)
        celkem_stavebni_sporeni += utils.celkem_rok(data_rok[rok], poplatky_ucet_rok, urok_rok, dan, celkem_stavebni_sporeni*urok)

        datum = data_rok[rok][len(data_rok[rok]) - 1][0]
        if datum.date() == date.fromisoformat(f"{datum.year}-04-30"):
            data_rok[rok].pop(len(data_rok[rok]) - 1)

        urok_vklady = utils.vypocet_uroku_rok(data_rok[rok], poplatek_mesic, urok)

    vklady_maximalni_podpora = utils.max_podpora(poplatky_ucet_rok, zaklad_statni_podpora, urok, dan)
    print(f"Nutno vložit v tomto roce pro získání maximální možné státní podpory: {vklady_maximalni_podpora:.2f}")
    vklady_rok = utils.celkem_vklady_rok(data_rok[rok])
    celkem_vklady += vklady_rok
    print(f"Vklady: {vklady_rok}")
    print(f"Naspořeno: {celkem_stavebni_sporeni:.2f}")
    podpora_rok, zaklad_statni_podpora = utils.statni_podpora(vklady_rok, urok_vklady, urok_vklady*dan, poplatky_ucet_rok, zaklad_statni_podpora)
    print(f"Získaná státní podpora: {podpora_rok}")
    print(f"Převedný základ pro státní podporu v dalším roce: {zaklad_statni_podpora:.2f}")
    utils.vlozit_zaznam_statni_podpora(data_rok, rok, roky, podpora_rok)

print("==============================================================================================")
print(f"Celkem vloženo: {celkem_vklady}")
print(f"Celkem uloženo na stavebním spoření: {celkem_stavebni_sporeni + podpora_rok}")