from urllib.request import urlopen
import time
import os
import io
import re

posiedzenie = 1
dzien = 1
wypowiedz = 1

# url = f"https://www.sejm.gov.pl/Sejm9.nsf/wypowiedz.xsp?posiedzenie={posiedzenie}&dzien={dzien}&wyp={wypowiedz}"
# page = urlopen(url)
# html_bytes = page.read()
# html = html_bytes.decode("utf-8")
# end_index = html.find("</html>")
#
# h2_index = html.find("<h2 class=\"mowca\"")
# html_cut = html[h2_index:end_index]
# finish_index = html_cut.find("</div>")
# html_finish = html_cut[0:finish_index]
#
# path = f'./wypowiedzi/{posiedzenie}'
# doesExist = os.path.exists(path)
# if not doesExist:
#     os.makedirs(path)
#
# path = f'./wypowiedzi/{posiedzenie}/{dzien}'
# doesExist = os.path.exists(path)
# if not doesExist:
#     os.makedirs(path)
#
# file = io.open(f"./wypowiedzi/{posiedzenie}/{dzien}/{posiedzenie} {dzien} {wypowiedz}.txt",
#                mode="w", encoding="utf-8")
# file.write(html_finish)
#
# for posiedzenie_file in os.listdir(f"./wypowiedzi"):
#     for dzien_file in os.listdir(f"./wypowiedzi/{posiedzenie_file}"):
#         for wypowiedz_file in os.listdir(f"./wypowiedzi/{posiedzenie_file}/{dzien_file}"):
#             file = io.open(f"./wypowiedzi/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
#                            mode="+", encoding="utf-8")
#             # TODO usuń nawiasy

# STEP 0.1 - delete speeches not of 'poseł'
# for wypowiedz_file in os.listdir(f"./wypowiedzi/kadencja_9/1/1"):
#     file = io.open(f"./wypowiedzi/kadencja_9/1/1/{wypowiedz_file}",
#                            mode="r+", encoding="utf-8")
#     text = file.read()
#     posel_index = text.find("<h2 class=\"mowca\">Poseł ")
#     if posel_index == -1:
#         file.close()
#         os.remove(f"./wypowiedzi/kadencja_9/1/1/{wypowiedz_file}")
#         print("DELETED " + wypowiedz_file)
#     else:
#         posel_end = text.find(":</h2>")
#         posel = text[(posel_index + 24):posel_end]
#         print(posel)
#         file.close()

# STEP 0.2 - delete 'tekst niewygłoszony' from names of 'poseł'
# for wypowiedz_file in os.listdir(f"./wypowiedzi/kadencja_9/1/1"):
#     file = io.open(f"./wypowiedzi/kadencja_9/1/1/{wypowiedz_file}",
#                    mode="r", encoding="utf-8")
#     text = file.read()
#     text_index = text.find(" (tekst niewygłoszony):</h2>")
#     if text_index != -1:
#         text = text[:text_index] + text[(text_index + 22):]
#         file.close()
#         file = io.open(f"./wypowiedzi/kadencja_9/1/1/{wypowiedz_file}",
#                        mode="w", encoding="utf-8")
#         file.write(text)
#     file.close()

# STEP 1 - find opening exclamations
for wypowiedz_file in os.listdir(f"./wypowiedzi/kadencja_9/1/1"):
    file = io.open(f"./wypowiedzi/kadencja_9/1/1/{wypowiedz_file}",
                   mode="r", encoding="utf-8")
    text = file.read()
    for exclamation in re.finditer('  [A-ZĄĆĘŁŃÓŚŹŻ][^]*?!', text)
        print(exclamation)
