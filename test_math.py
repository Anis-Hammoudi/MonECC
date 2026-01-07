from ecc_math import Point, G

# Test simple : 
# L'ordre de la courbe est le nombre de points total.
# Sur cette courbe spécifique (y^2 = x^3 + 35x + 3 mod 101),
# si tes calculs sont bons, multiplier G par un certain nombre doit boucler.

print("Point de base G:", G)

# Calculons 2G de deux façons
g_plus_g = G + G
two_g = G * 2

print("G + G =", g_plus_g)
print("G * 2 =", two_g)

if g_plus_g == two_g:
    print("SUCCESS: L'addition et la multiplication sont cohérentes !")
else:
    print("ERROR: Problème dans les formules.")

# Test avancé : 
# Si tu multiplies G par un très grand nombre (ex: 1000), ça ne doit pas planter.
big_point = G * 1000
print("G * 1000 =", big_point)