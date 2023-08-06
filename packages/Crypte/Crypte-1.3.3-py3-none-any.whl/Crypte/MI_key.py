import Crypte
import os

"""
MI Key
Based on Crypte
"""

def mi_key(path, key=None):
    if key != None:
        try:
            with open(path, "r", encoding="utf-8") as f:
                rd = f.read()
        except:
            raise Exception("Fichier inexistant ou incompatible.")

        mik = Crypte.crypte_with_key(rd, key)
        filename = os.path.basename(path)

        with open(path, "w", encoding="utf-8") as f:
            f.write(mik + "\nkey")

        os.rename(path, path.replace(filename, "code.mi"))

        return print(f"Fichier chiffré : {path.replace(filename,'code.mi')}")
    else:
        try:
            with open(path, "r", encoding="utf-8") as f:
                rd = f.read()
        except:
            raise Exception("Fichier inexistant ou incompatible.")

        mik = Crypte.crypte(rd)
        filename = os.path.basename(path)

        with open(path, "w", encoding="utf-8") as f:
            f.write(mik)

        os.rename(path, path.replace(filename, "code.mi"))

        return print(f"Fichier chiffré : {path.replace(filename,'code.mi')}")

def mi_unkey(path, key=None):
    if key != None:
        try:
            with open(path, "r", encoding="utf-8") as f:
                rd = f.read()
        except:
            raise Exception("Fichier inexistant ou incompatible.")

        if "key" in rd:
            pass
        else:
            raise Exception("Ce fichier n'est pas chiffré avec une clé privée, retirez l'argument 'key'.")

        rd = rd.replace("key", "")

        with open(path, "w", encoding="utf-8") as f:
            f.write(Crypte.decrypte_with_key(rd, key).replace("🔶", "\n"))

        filename = os.path.basename(path)
        os.rename(path, path.replace(filename, "code.txt"))

        return print(f"Fichier dechiffré : {path.replace(filename, 'code.txt')}")
    else:
        try:
            with open(path, "r", encoding="utf-8") as f:
                rd = f.read()
        except:
            raise Exception("Fichier inexistant ou incompatible.")

        if "key" not in rd:
            pass
        else:
            raise Exception("Ce fichier est chiffré avec une clé privée, ajoutez l'argument 'key'.")

        with open(path, "w", encoding="utf-8") as f:
            f.write(Crypte.decrypte(rd))

        filename = os.path.basename(path)
        os.rename(path, path.replace(filename, "code.txt"))

        return print(f"Fichier dechiffré : {path.replace(filename, 'code.txt')}")