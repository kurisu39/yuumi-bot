from voicelines import sortedVoiceLines
import math
import string

n = 1
for i in sortedVoiceLines:
    filename = "File0" + str("0" * (2 - math.floor(math.log(n, 10)))) + str(n) + ".ogg"
    something = i.lower().translate(str.maketrans("", "", string.punctuation))
    print(f'"{filename}" : "{something}",')
    n += 1
