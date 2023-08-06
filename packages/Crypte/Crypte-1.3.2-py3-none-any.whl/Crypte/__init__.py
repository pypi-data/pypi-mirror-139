import random
Keys = ["\n", "a", "z", "e", "r", "t", "y", "u", "i", "o", "p", "q", "s", "²",  "d", "f", "g", "h", "j", "k", "l", "m", "w", "x", "c", "v", "b", "n", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "é", "à", "è", " ", "A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P", "Q", "S", "D", "F", "G", "H", "J", "K", "L", "M", "W", "X", "C", "V", "B", "N", "?", ",", ";", ".", ":", "/", "!", ")", "(", "^", "'", "+", "-", "=", "[", "]", "{", "}", "ê", "¨", "@", "-", ",", "/", "'", "<", ">", "_", "-", "~", "#", "|", "ç", "*", "&", "°"]
CK = Keys


def init_keys(keys):
    for k in keys:
        Keys.append(k)
    CK = Keys
    return print(f"\33[37mClés {keys} ajoutée(s) !")


def decrypte_with_key(msg, key):
    Keys = []

    for k in key:
        Keys.append(k)

    New_Message = ""

    msg = msg.split(".")

    for Number in msg:
        try:
            index = Keys[int(Number)]
            New_Message = str(New_Message) + str(index)
        except:
            New_Message = str(New_Message) + "🔶"

    return New_Message


def crypte_with_key(msg, key):
    Keys = []

    for k in key:
        Keys.append(k)

    New_Message = ""

    for Number in msg:
        try:
            index = Keys.index(Number)
            New_Message = str(New_Message) + "." + str(index)
        except Exception as e:
            New_Message = str(New_Message) + "🔶"

    return New_Message


def create_key():
    Keys = CK

    Final_key = ""
    
    for loop in range(int(len(Keys))):
        rdm = random.choice(Keys)
        Keys.remove(rdm)
        Final_key = Final_key + rdm
    
    return "\33[37mClé \33[33m" + Final_key + "\33[37m crée."


def decrypte(msg):
    New_Message = ""

    m = msg.split(".")
    for Number in m:
        try:
            index = Keys[int(Number)]
            New_Message = str(New_Message) + str(index)
        except:
            pass

    return New_Message


def crypte_with_file(file):
    try:
        with open(file, "r", encoding='utf-8') as f:
            rd = f.read()
        pass
    except:
        raise f"Fichier {file} introuvable !"
        return

    New_Message = ""
    for Letter in rd:
        if Letter in Keys:
            index = Keys.index(Letter)
            New_Message = str(New_Message) + "." + str(index)
    return New_Message


def decrypte_with_file(file):
    try:
        with open(file, "r", encoding='utf-8') as f:
            rd = f.read()
        pass
    except:
        raise f"Fichier {file} introuvable !"
        return

    New_Message = ""
    m = rd.split(".")
    for Number in m:
        try:
            index = Keys[int(Number)]
            New_Message = str(New_Message) + str(index)
        except:
            pass

    return New_Message


def crypte(msg):
    New_Message = ""
    for Letter in msg:
        if Letter in Keys:
            index = Keys.index(Letter)
            New_Message = str(New_Message) + "." + str(index)

    return New_Message