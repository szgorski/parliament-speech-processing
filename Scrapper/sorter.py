from urllib.request import urlopen
import time
import os
import io
import re

# posiedzenie = 1
# dzien = 1
# wypowiedz = 1
# for posiedzenie_file in os.listdir(f"./wypowiedzi"):
#     for dzien_file in os.listdir(f"./wypowiedzi/{posiedzenie_file}"):
#         for wypowiedz_file in os.listdir(f"./wypowiedzi/{posiedzenie_file}/{dzien_file}"):
#             file = io.open(f"./wypowiedzi/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
#                            mode="+", encoding="utf-8")

# download also 0's ('marszałek')
# STEP ? - map all names
#          (delete 'tekst niewygłoszony')

# STEP ? - delete speeches not of 'poseł'
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

# STEP ? - delete 'tekst niewygłoszony' from names of 'poseł'
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

#

# STEP ? - (count occurrences of names, if more than one),
#          delete other 'poseł' names' and their texts

# STEP ? - calculate appearances of names, if more than one,
#          manually check speeches with more than one name

# STEP ? - find opening exclamations
# for wypowiedz_file in os.listdir(f"./wypowiedzi/kadencja_9/1/1"):
file = io.open(f"./wypowiedzi/kadencja_9/1/1/1 1 27.txt",
                   mode="r", encoding="utf-8")
text = file.read()
for exclamation in re.finditer('  [A-ZĄĆĘŁŃÓŚŹŻ][^(?!\.\?)]*\!|\! [A-ZĄĆĘŁŃÓŚŹŻ][^(?!\.\?)]*\!', text):
    print(exclamation[0][2:])

# STEP ? - delete all explanations from files
# STEP ? - delete parenthesis statements
# STEP ? - replace ... occurrences

# STEP ? - delete HTML formatting
# STEP ? - delete white chars
# STEP ? - delete all ... ... occurrences

# STEP ? - move speeches to 'posel' files
