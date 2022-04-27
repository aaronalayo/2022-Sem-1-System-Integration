
# f1 = open("GSM1.c9yUHM", encoding="utf8")
# print(f'{f1}')

# from base64 import decode
# import base64



# with open("GSM1.mZJzJQ", 'r', encoding="unicode-escape") as f2:
#     data = f2.readlines()
#     line = data[-1].encode('latin_1')
#     # smiley = ((line))
   
#     print(line.decode('utf-8'))
    
#     f2.close()

import pandas as pd
data = pd.read_csv("items - Sheet1 (1).tsv", sep="\t")

for note in data["note"]:
    print(note)