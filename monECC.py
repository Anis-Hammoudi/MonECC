import argparse
import base64
import hashlib
import os
import sys
import random

from ecc_math import Point, G

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

PRIV_HEADER = "---begin monECC private key---"
PUB_HEADER  = "---begin monECC public key---"
FOOTER      = "---end monECC key---"

AES_BLOCK_SIZE = 16
ENCODING = "utf-8"

def save_private_key(filename, k: int):
    data = base64.b64encode(str(k).encode()).decode()
    with open(filename, "w") as f:
        f.write(f"{PRIV_HEADER}\n")
        f.write(f"{data}\n")
        f.write(f"{FOOTER}\n")


def save_public_key(filename, Q: Point):
    payload = f"{Q.x};{Q.y}"
    data = base64.b64encode(payload.encode()).decode()
    with open(filename, "w") as f:
        f.write(f"{PUB_HEADER}\n")
        f.write(f"{data}\n")
        f.write(f"{FOOTER}\n")


def load_private_key(filename) -> int:
    with open(filename, "r") as f:
        lines = f.read().strip().splitlines()

    if lines[0] != PRIV_HEADER:
        raise ValueError("Clé privée invalide")

    k = int(base64.b64decode(lines[1]).decode())
    return k


def load_public_key(filename) -> Point:
    with open(filename, "r") as f:
        lines = f.read().strip().splitlines()

    if lines[0] != PUB_HEADER:
        raise ValueError("Clé publique invalide")

    decoded = base64.b64decode(lines[1]).decode()
    x, y = decoded.split(";")
    return Point(int(x), int(y))

def derive_aes_material(shared_point: Point):
    secret_str = f"{shared_point.x};{shared_point.y}".encode()
    digest = hashlib.sha256(secret_str).digest()

    iv = digest[:16]
    key = digest[16:]
    return iv, key


def encrypt_message(plaintext: str, key: bytes, iv: bytes) -> bytes:
    padder = padding.PKCS7(128).padder()
    padded = padder.update(plaintext.encode(ENCODING)) + padder.finalize()

    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    return encryptor.update(padded) + encryptor.finalize()


def decrypt_message(ciphertext: bytes, key: bytes, iv: bytes) -> str:
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded) + unpadder.finalize()
    return data.decode(ENCODING)

def command_keygen(args):
    k = random.randint(1, args.size)
    Q = G * k

    priv_name = args.filename + ".priv"
    pub_name = args.filename + ".pub"

    save_private_key(priv_name, k)
    save_public_key(pub_name, Q)

    print(f"Clés générées : {priv_name}, {pub_name}")


def command_crypt(args):
    Q_target = load_public_key(args.key)

    r = random.randint(1, 1000)
    R = G * r
    S = Q_target * r

    iv, key = derive_aes_material(S)
    ciphertext = encrypt_message(args.text, key, iv)

    output = f"{R.x};{R.y}:{base64.b64encode(ciphertext).decode()}"

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
    else:
        print(output)


def command_decrypt(args):
    k = load_private_key(args.key)

    hint, data = args.text.split(":")
    rx, ry = hint.split(";")
    R = Point(int(rx), int(ry))

    ciphertext = base64.b64decode(data)

    S = R * k
    iv, key = derive_aes_material(S)

    plaintext = decrypt_message(ciphertext, key, iv)

    if args.output:
        with open(args.output, "w") as f:
            f.write(plaintext)
    else:
        print(plaintext)

def show_help():
    print("""
Script monECC par [Ton Nom]

Syntaxe :
    python monECC.py <commande> [fichier clé] [texte] [switchs]

Commandes :
    keygen          Génère une paire de clés (privée & publique)
    crypt           Chiffre un message pour la clé publique
    decrypt         Déchiffre un message avec la clé privée
    help            Affiche ce manuel

Clés :
    Fichier contenant une clé publique ("crypt") ou privée ("decrypt")

Texte :
    Phrase en clair ("crypt") ou phrase chiffrée ("decrypt")

Switchs facultatifs :
    -f <nom>       Choisir le nom des fichiers clés générés (par défaut : monECC.pub / monECC.priv)
    -s <taille>    Plage d’aléa pour la clé privée (par défaut : 1-1000)
    -i <fichier>   Lire le texte à chiffrer/déchiffrer depuis un fichier
    -o <fichier>   Écrire la sortie chiffrée/déchiffrée dans un fichier
""")


def main():
    if len(sys.argv) < 2 or sys.argv[1].lower() == "help":
        show_help()
        return

    cmd = sys.argv[1].lower()

    if cmd == "keygen":
        keygen_command()  # tu peux passer des noms de fichiers si tu veux
    elif cmd == "crypt":
        if len(sys.argv) < 4:
            print("Erreur : crypt nécessite <fichier_pub> <texte>")
            return
        pub_file = sys.argv[2]
        texte = sys.argv[3]
        ciphertext = crypt_command(pub_file, texte)
        print("Texte chiffré :", ciphertext)
    elif cmd == "decrypt":
        if len(sys.argv) < 4:
            print("Erreur : decrypt nécessite <fichier_priv> <texte_chiffré>")
            return
        priv_file = sys.argv[2]
        cipher_input = sys.argv[3]
        decrypted = decrypt_command(priv_file, cipher_input)
        print("Texte déchiffré :", decrypted)
    else:
        print(f"Commande inconnue : {cmd}")
        show_help()

if __name__ == "__main__":
    main()
