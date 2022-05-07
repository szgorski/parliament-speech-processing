from urllib.request import urlopen
import time
import os
import io

kadencja = 9
no_of_posiedzenie = 45  # should be inserted manually (additional verification)
posiedzenie = 1
dzien = 1

# downloads all 'Marszałek (przebieg posiedzenia)', not for analysis
while posiedzenie <= no_of_posiedzenie:
    try:
        url = f"https://www.sejm.gov.pl/Sejm{kadencja}.nsf/wypowiedz.xsp?posiedzenie={posiedzenie}&dzien={dzien}&wyp=0"
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
    except:
        time.sleep(60)
        url = f"https://www.sejm.gov.pl/Sejm{kadencja}.nsf/wypowiedz.xsp?posiedzenie={posiedzenie}&dzien={dzien}&wyp=0"
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")

    h2_index = html.find("<p class=\"marsz\">")
    print(h2_index)
    if h2_index == -1:
        dzien = 1
        posiedzenie += 1
    else:
        end_index = html.find("</html>")
        html_cut = html[h2_index:end_index]
        finish_index = html_cut.find("</div><p class=\"przebieg\"></p></div>")
        html_finish = html_cut[0:finish_index]

        path = f'./kadencja_{kadencja}/{posiedzenie}'
        doesExist = os.path.exists(path)
        if not doesExist:
            os.makedirs(path)

        path = f'./kadencja_{kadencja}/{posiedzenie}/{dzien}'
        doesExist = os.path.exists(path)
        if not doesExist:
            os.makedirs(path)

        file = io.open(f"./kadencja_{kadencja}/{posiedzenie}/{dzien}/{posiedzenie} {dzien} 0.txt",
                       mode="w", encoding="utf-8")
        file.write(html_finish)
        file.close()
        print(f"{posiedzenie}, {dzien}, 0")

        dzien += 1

# downloads all speeches
while posiedzenie <= no_of_posiedzenie:
    try:
        url = f"https://www.sejm.gov.pl/Sejm{kadencja}.nsf/wypowiedz.xsp?posiedzenie={posiedzenie}&dzien={dzien}&wyp={wypowiedz}"
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
    except:
        time.sleep(60)
        url = f"https://www.sejm.gov.pl/Sejm{kadencja}.nsf/wypowiedz.xsp?posiedzenie={posiedzenie}&dzien={dzien}&wyp={wypowiedz}"
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")

    h2_index = html.find("<h2 class=\"mowca\"")
    print(h2_index)
    if h2_index == -1:
        if wypowiedz > 0:
            wypowiedz = 0
            dzien += 1
        else:
            if dzien > 1:
                wypowiedz = 0
                dzien = 1
                posiedzenie += 1

    else:
        end_index = html.find("</html>")
        html_cut = html[h2_index:end_index]
        finish_index = html_cut.find("</div>")
        html_finish = html_cut[0:finish_index]

        path = f'./kadencja_{kadencja}/{posiedzenie}'
        doesExist = os.path.exists(path)
        if not doesExist:
            os.makedirs(path)

        path = f'./kadencja_{kadencja}/{posiedzenie}/{dzien}'
        doesExist = os.path.exists(path)
        if not doesExist:
            os.makedirs(path)

        file = io.open(f"./kadencja_{kadencja}/{posiedzenie}/{dzien}/{posiedzenie} {dzien} {wypowiedz}.txt",
                       mode="w", encoding="utf-8")
        file.write(html_finish)
        file.close()
        print(f"{posiedzenie}, {dzien}, {wypowiedz}")

        wypowiedz += 1
