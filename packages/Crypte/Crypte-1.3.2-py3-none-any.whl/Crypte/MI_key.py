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
            raise "Fichier inexistant ou incompatible."

        mik = Crypte.crypte_with_key(rd, key)
        filename = os.path.basename(path)

        with open(path, "w", encoding="utf-8") as f:
            f.write(mik)

        os.rename(path, path.replace(filename, "code.mi"))

        return f"Fichier chiffré : {path.replace(filename,'code.mi')}"
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

        return Exception(f"Fichier chiffré : {path.replace(filename,'code.mi')}")