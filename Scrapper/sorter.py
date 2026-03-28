import os
import io
import re
import regex
import pickle

# one may perform one step at the time

# STEP 1.1 - map all 'Marszałek' names
name_set = {"Marszałek"}

for kadencja in [8, 9]:
    posiedzenie = 1
    dzien = 1
    for posiedzenie_file in os.listdir(f"./kadencja_{kadencja}"):
        for dzien_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}"):
            file = io.open(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{posiedzenie_file} {dzien_file} 0.txt",
                           mode="r", encoding="utf-8")
            text = file.read()
            for name in re.findall('<p class="marsz">.+?:</p>', text):
                name_set.add(name[17:-5])
            file.close()


# STEP 1.2 - map all 'Poseł' names
for kadencja in [8, 9]:
    posiedzenie = 1
    dzien = 1
    wypowiedz = 1
    for posiedzenie_file in os.listdir(f"./kadencja_{kadencja}"):
        for dzien_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}"):
            for wypowiedz_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}"):
                file = io.open(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
                               mode="r", encoding="utf-8")
                text = file.read()
                text_niewygloszony = text.find(" (tekst niewygłoszony):</h2>")
                if text_niewygloszony != -1:
                    text = text[:text_niewygloszony] + text[(text_niewygloszony + 22):]
                for name in re.findall('<h2 class="mowca">.+?:</h2>', text):
                    name_set.add(name[18:-6])
                file.close()

file_set = io.open("./name_set.txt", mode="wb")
pickle.dump(name_set, file_set)
file_set.close()


# STEP 2.1 - delete speeches not of 'Poseł'
# set_good = set()
# set_bad = set()
deleted = 0
saved = 0

for kadencja in [8, 9]:
    posiedzenie = 1
    dzien = 1
    wypowiedz = 1
    for posiedzenie_file in os.listdir(f"./kadencja_{kadencja}"):
        for dzien_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}"):
            for wypowiedz_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}"):
                file = io.open(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
                               mode="r", encoding="utf-8")
                text = file.read()
                posel = re.search("<h2 class=\"mowca\">Poseł (?!Sprawozdawca)", text)
                if posel is None:
                    # if text.find("<h2 class=\"mowca\">") != -1:
                    #     mowca_begin = text.find("<h2 class=\"mowca\">")
                    #     mowca_end = text.find(":</h2>")
                    #     set_bad.add(text[(mowca_begin + 18):mowca_end])
                    # else:
                    #     mowca_begin = text.find("<p class=\"marsz\">")
                    #     mowca_end = text.find(":</p>")
                    #     set_bad.add(text[(mowca_begin + 17):mowca_end])
                    file.close()
                    os.remove(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}")
                    deleted += 1
                else:
                    # header = text.find("</h2>")
                    # set_good.add(text[18:(header - 1)])
                    file.close()
                    saved += 1
print(f"DELETED {deleted} FILES")   # DELETED 9686 FILES
print(f"SAVED {saved} FILES")       # SAVED 53156 FILES

# for name in sorted(set_good):
#     print(name)
# print()
# for name in sorted(set_bad):
#     print(name)


# STEP 2.2 - delete 'tekst niewygłoszony' from names of 'Poseł'
modified = 0
for kadencja in [8, 9]:
    posiedzenie = 1
    dzien = 1
    wypowiedz = 1
    for posiedzenie_file in os.listdir(f"./kadencja_{kadencja}"):
        for dzien_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}"):
            for wypowiedz_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}"):
                file = io.open(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
                               mode="r", encoding="utf-8")
                text = file.read()
                text_index = text.find(" (tekst niewygłoszony):</h2>")
                if text_index != -1:
                    text = text[:text_index] + text[(text_index + 22):]
                    file.close()
                    file = io.open(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
                                   mode="w", encoding="utf-8")
                    file.write(text)
                    modified += 1
                file.close()
print(f"MODIFIED {modified} FILES")   # MODIFIED 2109 FILES


# STEP 3 - replace ' <ENTER><ENTER>' and '<ENTER><ENTER>' with ' '
modified = 0
for kadencja in [8, 9]:
    posiedzenie = 1
    dzien = 1
    wypowiedz = 1
    for posiedzenie_file in os.listdir(f"./kadencja_{kadencja}"):
        for dzien_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}"):
            for wypowiedz_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}"):
                file = io.open(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
                               mode="r", encoding="utf-8")
                text = file.read()
                text_index = text.find(" \n\n")
                while text_index != -1:
                    text = text[:text_index + 1] + text[(text_index + 3):]
                    text_index = text.find(" \n\n")

                text_index = text.find("\n\n")
                while text_index != -1:
                    text = text[:text_index] + " " + text[(text_index + 2):]
                    text_index = text.find("\n\n")

                file.close()
                file = io.open(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
                               mode="w", encoding="utf-8")
                file.write(text)
                file.close()
                modified += 1
print(f"MODIFIED {modified} FILES")   # MODIFIED 53156 FILES


# STEP 4.1 - delete other 'Poseł' names' and their texts
file_set = io.open("./name_set.txt", mode="rb")
name_set = pickle.load(file_set)
file_set.close()
name_regex = ""
for name in name_set:
    name_regex = name_regex + f"|<p>    {name}:</p>"
name_regex = name_regex[1:]

deleted = 0
for kadencja in [8, 9]:
    posiedzenie = 1
    dzien = 1
    wypowiedz = 1
    for posiedzenie_file in os.listdir(f"./kadencja_{kadencja}"):
        for dzien_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}"):
            for wypowiedz_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}"):
                file = io.open(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
                               mode="r", encoding="utf-8")
                text = file.read()
                posel = ""
                for name in re.findall('<h2 class="mowca">.+?:</h2>', text):
                    posel = f"<p>    {name[18:-6]}:</p>"

                occurrence = False
                for name in re.findall(name_regex, text):
                    if name != posel:
                        occurrence = True
                        del_begin = text.find(name)
                        del_end = text.find(posel) + len(posel)
                        text = text[:del_begin] + text[del_end:]
                        deleted += 1

                if occurrence == True:
                    file.close()
                    file = io.open(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
                                   mode="w", encoding="utf-8")
                    file.write(text)
                file.close()
print(f"DELETED {deleted} OCCURRENCES")  # DELETED 10495 OCCURRENCES


# STEP 4.2 - manually verify speeches with other 'Poseł' names [CHECK BELOW]
deleted = 0
for kadencja in [8, 9]:
    posiedzenie = 1
    dzien = 1
    wypowiedz = 1
    for posiedzenie_file in os.listdir(f"./kadencja_{kadencja}"):
        for dzien_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}"):
            for wypowiedz_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}"):
                file = io.open(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
                               mode="r", encoding="utf-8")
                text = file.read()
                occurrence = False
                for name in re.findall(name_regex, text):
                    # print(f"{kadencja}: {wypowiedz_file}")
                    occurrence = True
                file.close()
                if occurrence == True:
                    os.remove(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}")
                    deleted += 1
print(f"DELETED {deleted} FILES")     # DELETED 38 FILES


# STEP 5.1 - find opening exclamations
exclamation_raw_set = set()
for kadencja in [8, 9]:
    posiedzenie = 1
    dzien = 1
    wypowiedz = 1
    for posiedzenie_file in os.listdir(f"./kadencja_{kadencja}"):
        for dzien_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}"):
            for wypowiedz_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}"):
                file = io.open(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
                               mode="r", encoding="utf-8")
                text = file.read()
                for exclamation in regex.findall('  [A-ZĄĆĘŁŃÓŚŹŻ][^(?!\.\?)]*\!|\! [A-ZĄĆĘŁŃÓŚŹŻ][^(?!\.\?)]*\!',
                                                 text, overlapped=True):
                    exclamation_raw_set.add(exclamation[1:])
                file.close()
file_set = io.open("exclamation_raw_set.txt", mode="wb")
pickle.dump(exclamation_raw_set, file_set)
file_set.close()

# STEP 5.2 - verify exclamations manually (saved to exclamation_selected.txt)
# file_set = io.open("exclamation_raw_set.txt", mode="rb")
# exclamation_raw_set = pickle.load(file_set)
# file_set.close()
# for exclamation in sorted(exclamation_raw_set):
#     print(exclamation)

exclamation_set = set()
file = io.open("exclamation_selected.txt", mode="r", encoding="utf-8")
work = True
while work:
    line = file.readline()[:-1]
    if len(line) > 1:
        exclamation_set.add(line)
    else:
        work = False

file.close()
file_set = io.open("exclamation_set.txt", mode="wb")
pickle.dump(exclamation_set, file_set)
file_set.close()

# STEP 5.3 - delete all explanations from files (not only those from the beginning)
exclamation_regex = ""
for exclamation in exclamation_set:
    exclamation_regex += f"|[  \.\?\!]{exclamation}"
exclamation_regex = exclamation_regex[1:]

deleted = 0
for kadencja in [8, 9]:
    posiedzenie = 1
    dzien = 1
    wypowiedz = 1
    for posiedzenie_file in os.listdir(f"./kadencja_{kadencja}"):
        for dzien_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}"):
            for wypowiedz_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}"):
                file = io.open(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
                               mode="r", encoding="utf-8")
                text = file.read()
                for exclamation in regex.findall(exclamation_regex, text, overlapped=True):
                    exclamation = exclamation[1:]
                    position = text.find(exclamation)
                    text = text[:position] + text[(position + len(exclamation)):]
                    deleted += 1

                file.close()
                file = io.open(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
                               mode="w", encoding="utf-8")
                file.write(text)
                file.close()
print(f"DELETED {deleted} EXCLAMATIONS")  # DELETED 132329 EXCLAMATIONS


# STEP 6.1 - delete parenthesis statements
deleted = 0
for kadencja in [8, 9]:
    posiedzenie = 1
    dzien = 1
    wypowiedz = 1
    for posiedzenie_file in os.listdir(f"./kadencja_{kadencja}"):
        for dzien_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}"):
            for wypowiedz_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}"):
                file = io.open(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
                               mode="r", encoding="utf-8")
                text = file.read()
                for parenthesis in re.findall("\(.*?\)", text):
                    position = text.find(parenthesis)
                    text = text[:position] + text[(position + len(parenthesis)):]
                    deleted += 1

                file.close()
                file = io.open(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
                               mode="w", encoding="utf-8")
                file.write(text)
                file.close()
print(f"DELETED {deleted} PARENTHESIS")  # DELETED 124248 PARENTHESIS

# STEP 6.2 - replace ... with … punctuation mark
replaced = 0
for kadencja in [8, 9]:
    posiedzenie = 1
    dzien = 1
    wypowiedz = 1
    for posiedzenie_file in os.listdir(f"./kadencja_{kadencja}"):
        for dzien_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}"):
            for wypowiedz_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}"):
                file = io.open(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
                               mode="r", encoding="utf-8")
                text = file.read()
                for parenthesis in re.findall("\.\.\.", text):
                    position = text.find(parenthesis)
                    text = text[:position] + "…" + text[(position + 3):]
                    replaced += 1

                file.close()
                file = io.open(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
                               mode="w", encoding="utf-8")
                file.write(text)
                file.close()
print(f"REPLACED {replaced} ELLIPSIS")  # REPLACED 39669 ELLIPSIS


# STEP 6.3 - delete HTML formatting
modified = 0
for kadencja in [8, 9]:
    posiedzenie = 1
    dzien = 1
    wypowiedz = 1
    for posiedzenie_file in os.listdir(f"./kadencja_{kadencja}"):
        for dzien_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}"):
            for wypowiedz_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}"):
                file = io.open(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
                               mode="r", encoding="utf-8")
                text = file.read()
                for p in re.findall("<p>", text):
                    position = text.find(p)
                    text = text[:position] + " " + text[(position + 3):]
                for p in re.findall("</p>", text):
                    position = text.find(p)
                    text = text[:position] + " " + text[(position + 4):]

                file.close()
                file = io.open(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
                               mode="w", encoding="utf-8")
                file.write(text)
                file.close()
                modified += 1
print(f"MODIFIED {modified} FILES")   # MODIFIED 53118 FILES


# STEP 6.4 - delete white chars and quotation marks
modified = 0
for kadencja in [8, 9]:
    posiedzenie = 1
    dzien = 1
    wypowiedz = 1
    for posiedzenie_file in os.listdir(f"./kadencja_{kadencja}"):
        for dzien_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}"):
            for wypowiedz_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}"):
                file = io.open(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
                               mode="r", encoding="utf-8")
                text = file.read()
                i = 0
                while i in range(len(text) - 1):
                    if text[i] == ' ' or text[i] == ' ':
                        if text[i + 1] == ' ' or text[i + 1] == ' ':
                            text = text[:i] + text[(i + 1):]
                        else:
                            i += 1
                    else:
                        i += 1
                i = 0
                while i in range(len(text)):
                    if text[i] == '˝':
                        text = text[:i] + text[(i + 1):]
                    else:
                        i += 1
                file.close()

                file = io.open(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
                               mode="w", encoding="utf-8")
                file.write(text)
                file.close()
                modified += 1
print(f"MODIFIED {modified} FILES")   # MODIFIED 53118 FILES


# STEP 6.5 - delete all '… …' occurrences
deleted = 0
for kadencja in [8, 9]:
    posiedzenie = 1
    dzien = 1
    wypowiedz = 1
    for posiedzenie_file in os.listdir(f"./kadencja_{kadencja}"):
        for dzien_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}"):
            for wypowiedz_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}"):
                file = io.open(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
                               mode="r", encoding="utf-8")
                text = file.read()
                i = 0
                while i in range(len(text) - 2):
                    if text[i] == '…' and text[i + 1] == ' ' and text[i + 2] == '…':
                        text = text[:i] + ' ' + text[(i + 3):]
                        deleted += 1
                    else:
                        i += 1
                file.close()

                file = io.open(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
                               mode="w", encoding="utf-8")
                file.write(text)
                file.close()
print(f"DELETED {deleted} ELLIPSIS")  # DELETED 13217 ELLIPSIS


# STEP 7 - move speeches to 'Poseł' files [CHECK BELOW]
for kadencja in [8, 9]:
    posiedzenie = 1
    dzien = 1
    wypowiedz = 1
    for posiedzenie_file in os.listdir(f"./kadencja_{kadencja}"):
        for dzien_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}"):
            for wypowiedz_file in os.listdir(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}"):
                file = io.open(f"./kadencja_{kadencja}/{posiedzenie_file}/{dzien_file}/{wypowiedz_file}",
                               mode="r", encoding="utf-8")
                text = file.read()
                posel_begin = text.find("<h2 class=\"mowca\">Poseł ")
                posel_end = text.find(":</h2>")
                posel = text[(posel_begin + 24):posel_end]
                text = text[(posel_end + 6):]
                while len(text) > 0 and (text[0] == ' ' or text[0] == '…' or text[0] == ' ' or text[0] == '·'):
                    text = text[1:]
                while len(text) > 0 and (text[-1] == ' ' or text[-1] == '…' or text[-1] == ' ' or text[-1] == '·'):
                    text = text[:-1]

                if len(text) > 0:
                    sort = io.open(f"./data_sorted/{posel}.txt", mode="a", encoding="utf-8")
                    sort.write(text + '\n')
                    sort.close()
                else:
                    print(f"EMPTY SPEECH - {kadencja}: {wypowiedz_file}")
                file.close()

count = 0
for name in os.listdir("data_sorted"):
    file = io.open(f"./data_sorted/{name}", mode="r", encoding="utf-8")
    text = file.read()
    while len(text) > 0 and text[-1] == '\n':
        text = text[:-1]
    file.close()
    file = io.open(f"./data_sorted/{name}", mode="w", encoding="utf-8")
    file.write(text)
    file.close()
    count += 1
print(f"CREATED {count} FILES")       # CREATED 666 FILES

# [NOTES]

# [STEP 4.2] Verification issues:
# 8: 10 2 276.txt
# 8: 15 3 58.txt
# 8: 20 1 270.txt
# 8: 22 2 267.txt
# 8: 28 2 164.txt
# 8: 3 1 36.txt
# 8: 33 1 53.txt
# 8: 33 1 66.txt
# 8: 42 2 84.txt
# 8: 43 2 21.txt
# 8: 43 2 21.txt
# 8: 43 2 21.txt
# 8: 51 2 301.txt
# 8: 54 3 118.txt
# 8: 54 3 118.txt
# 8: 54 3 142.txt
# 8: 61 1 183.txt
# 8: 67 3 276.txt
# 8: 72 2 150.txt
# 8: 72 2 150.txt
# 8: 72 2 150.txt
# 8: 74 2 19.txt
# 8: 76 1 75.txt
# 8: 79 1 192.txt
# 8: 8 1 82.txt
# 8: 80 4 17.txt
# 8: 80 4 17.txt
# 8: 80 4 17.txt
# 8: 80 4 17.txt
# 8: 80 4 17.txt
# 8: 80 4 17.txt
# 8: 80 4 17.txt
# 8: 84 3 182.txt
# 8: 84 3 182.txt
# 8: 84 3 204.txt
# 8: 85 1 21.txt
# 9: 11 1 102.txt
# 9: 12 2 206.txt
# 9: 12 3 26.txt
# 9: 12 3 26.txt
# 9: 13 1 39.txt
# 9: 15 1 188.txt
# 9: 17 1 176.txt
# 9: 21 2 86.txt
# 9: 30 3 38.txt
# 9: 31 1 99.txt
# 9: 31 1 99.txt
# 9: 31 1 99.txt
# 9: 34 2 158.txt
# 9: 38 2 125.txt
# 9: 38 2 19.txt
# 9: 4 2 204.txt
# 9: 9 3 54.txt

# [STEP 7] Verification issues:
# EMPTY SPEECH - 8: 38 2 91.txt
# EMPTY SPEECH - 9: 2 3 129.txt