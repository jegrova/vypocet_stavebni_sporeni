import csv
from datetime import datetime


def nacist_soubor():
    with open('./vlozeno.csv', newline='') as f:
        my_list = []
        for datum, val in csv.reader(f, delimiter=','):
            datetime_object = datetime.strptime(datum, '%d.%m.%Y')
            my_list.append([datetime_object, int(val)])

    return my_list


def statni_podpora(vklady_rok, urok_vklady, dan_uroky, poplatky_ucet_rok, prevedeno_minuly_rok):
    celkem_rok = vklady_rok + urok_vklady - dan_uroky - poplatky_ucet_rok + prevedeno_minuly_rok
    statni_podpora = celkem_rok * 10 / 100
    if statni_podpora > 2000:
        statni_podpora = 2000
        prebytek = celkem_rok - 20000
    else:
        prebytek = 0

    return statni_podpora, prebytek


def max_podpora(poplatky_ucet_rok, prevedeno_minuly_rok, urok, dan):
    vlozit = (20000 + poplatky_ucet_rok - prevedeno_minuly_rok) / (1 + urok - urok*dan)
    return vlozit


def vypocet_uroku_rok(vlozeno, mesicni_poplatek, urok, prvni_mesic=1):
    rocni_urok = 0
    for datum, vklad in vlozeno:
        rocni_urok += vklad * urok/12 * (12-datum.month)

    for i in range(prvni_mesic, 12):
        rocni_urok -= mesicni_poplatek * urok/12 * (12-i)

    return rocni_urok


def ziskat_roky(data):
    roky = set()
    for datum, vklad in data:
        roky.add(datum.year)

    return roky


def ziskat_vklady_rok(data, rok):
    vklady_rok = []
    for datum, vklad in data:
        if datum.year == rok:
            vklady_rok.append([datum, vklad])
    return vklady_rok


def celkem_vklady_rok(data):
    vklady_rok = 0
    for datum, vklad in data:
        vklady_rok += vklad

    return vklady_rok


def celkem_rok(data, poplatky_ucet_rok, urok_rok, dan, uroky_lonsky_zustatek=0):
    celkem = 0
    for datum, vklad in data:
        celkem += vklad

    uroky = urok_rok + uroky_lonsky_zustatek
    celkem_rok = celkem - poplatky_ucet_rok + uroky - uroky*dan

    return celkem_rok


def vlozit_zaznam_statni_podpora(data_rok, rok, roky, podpora_rok):
    if rok+1 in roky:
        data_rok[rok + 1].append([datetime(rok+1, 4, 30, 0, 0), podpora_rok])
    else:
        print(f"Následující rok bude vyplacena státní podpora: {podpora_rok}")
