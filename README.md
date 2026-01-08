# monECC

Application de chiffrement et déchiffrement par Courbes Elliptiques (ECC) en ligne de commande.

Ce projet implémente manuellement les calculs mathématiques sur une courbe elliptique finie et utilise le standard AES-CBC pour sécuriser les messages.

## Auteurs

* **Hammoudi Anis** - Moteur Mathématique ECC (Arithmétique modulaire, Classe Point)
* **Sanaa Zouine** - Application Principale (Interface commande, Gestion de fichiers, Chiffrement AES)

## Installation

Vous avez besoin de **Python 3** et de la bibliothèque `cryptography`.

Installez la dépendance avec la commande suivante :

```bash
pip install cryptography

## Utilisation

L’application se lance depuis le terminal avec la syntaxe suivante :

```bash
python monECC.py <commande> [fichier clé] [texte] [switchs]

Commandes disponibles :
keygen:	Génère une paire de clés (privée et publique).
crypt:	Chiffre un message pour la clé publique.
decrypt:	Déchiffre un message avec la clé privée.
help:	Affiche ce manuel et la liste des commandes.