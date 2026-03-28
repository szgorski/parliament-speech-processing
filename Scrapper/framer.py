# STEP 1

import os
import io

export data to a dataframe
all_speeches = io.open(f"./data_frame/all_speeches.txt", mode="w", encoding="utf-8")
for kadencja in [8, 9]:
    for posiedzenie_file in os.listdir(f"./data_transformed (unpack)/kadencja_{kadencja}"):
        for dzien_file in os.listdir(f"./data_transformed (unpack)/kadencja_{kadencja}/{posiedzenie_file}"):
            for wypowiedz_file in os.listdir(f"./data_transformed (unpack)/kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}"):
                file = io.open(f"./data_transformed (unpack)/kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
                               mode="r", encoding="utf-8")

                text = file.read()
                posel_begin = text.find("<h2 class=\"mowca\">Poseł ")
                posel_end = text.find(":</h2>")
                posel = text[(posel_begin + 24):posel_end]
                file.close()

                text = text[(posel_end + 6):]
                while len(text) > 0 and (text[0] == ' ' or text[0] == '…' or text[0] == ' ' or text[0] == '·'):
                    text = text[1:]
                while len(text) > 0 and (text[-1] == ' ' or text[-1] == '…' or text[-1] == ' ' or text[-1] == '·'):
                    text = text[:-1]

                wypowiedz_file = wypowiedz_file[:-4]
                [posiedzenie, dzien, wypowiedz] = wypowiedz_file.split()

                speech = str(kadencja) + '@@' + posiedzenie + '@@' + dzien + '@@' + wypowiedz + '@@' + posel + '@@' + text + '\n'
                all_speeches.write(speech)

all_speeches.close()

# STEP 2

import re

all_speeches = io.open(f"./data_frame/all_speeches.txt", mode="r", encoding="utf-8")
text = all_speeches.read()

chars = set()
b = 0
for char in text:
    if char not in chars:
        chars.add(char)
    b += 1
    if b % 100000 == 0:
        print(b)

print(sorted(chars))
all_speeches.close()

re.split("[!\"#%&()+,-./:;<=>?@\[\]_`§°·×–‘’”„…\n\xa0 ]", "abba")
# \n !"#%&'()+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]_`abcdefghijklmnopqrstuvwxyz\xa0§°·ÉÓ×àáâäçéëíîóôöúüýăąĆćČčďĘęěŁłńŚśşšŹźŻżŽ–‘’”„…

# STEP 3

b = 0
for kadencja in [8, 9]:
    for posiedzenie_file in os.listdir(f"./data_transformed (unpack)/kadencja_{kadencja}"):
        for dzien_file in os.listdir(f"./data_transformed (unpack)/kadencja_{kadencja}/{posiedzenie_file}"):
            for wypowiedz_file in os.listdir(f"./data_transformed (unpack)/kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}"):
                file = io.open(f"./data_transformed (unpack)/kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
                               mode="r", encoding="utf-8")

                text = file.read()
                posel_begin = text.find("<h2 class=\"mowca\">Poseł ")
                posel_end = text.find(":</h2>")
                posel = text[(posel_begin + 24):posel_end]
                file.close()

                text = text[(posel_end + 6):]
                while len(text) > 0 and (text[0] == ' ' or text[0] == '…' or text[0] == ' ' or text[0] == '·'):
                    text = text[1:]
                while len(text) > 0 and (text[-1] == ' ' or text[-1] == '…' or text[-1] == ' ' or text[-1] == '·'):
                    text = text[:-1]

                e_words = re.split("[!\"#%&()+,\-./:;<=>?@\[\]_`§°·×–‘’”„…\n\xa0 ]", text)
                words = list(filter(None, e_words))
                count = 0
                for word in words:
                    count += len(word)
                print(str(len(words)) + ': ')
                if len(words) < 30:
                    print(count)
                    print(words)
                    print(text)

                file.close()
                b += 1
                if b >= 100:
                    exit(0)
