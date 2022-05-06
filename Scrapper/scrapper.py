from urllib.request import urlopen
import time
import os
import io
# import re

# 34, 1-2
# 51, 2, 5
posiedzenie = 51
dzien = 2
wypowiedz = 5

while posiedzenie <= 86:
    try:
        url = f"https://www.sejm.gov.pl/Sejm8.nsf/wypowiedz.xsp?posiedzenie={posiedzenie}&dzien={dzien}&wyp={wypowiedz}"
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
    except:
        time.sleep(60)
        url = f"https://www.sejm.gov.pl/Sejm8.nsf/wypowiedz.xsp?posiedzenie={posiedzenie}&dzien={dzien}&wyp={wypowiedz}"
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")

    h2_index = html.find("<h2 class=\"mowca\"")
    print(h2_index)
    if h2_index == -1:
        if wypowiedz > 1:
            wypowiedz = 1
            dzien += 1
        else:
            if dzien > 1:
                wypowiedz = 1
                dzien = 1
                posiedzenie += 1

    else:
        end_index = html.find("</html>")
        html_cut = html[h2_index:end_index]
        finish_index = html_cut.find("</div>")
        html_finish = html_cut[0:finish_index]

        path = f'./kadencja8/{posiedzenie}'
        doesExist = os.path.exists(path)
        if not doesExist:
            os.makedirs(path)

        path = f'./kadencja8/{posiedzenie}/{dzien}'
        doesExist = os.path.exists(path)
        if not doesExist:
            os.makedirs(path)

        file = io.open(f"./kadencja8/{posiedzenie}/{dzien}/{posiedzenie} {dzien} {wypowiedz}.txt",
                       mode="w", encoding="utf-8")
        file.write(html_finish)
        # file.close()
        print(f"{posiedzenie}, {dzien}, {wypowiedz}")

        wypowiedz += 1
