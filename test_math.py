from ecc_math import Point, G, A, B, P

# --- UTILITAIRES DE TEST ---
def is_on_curve(point):
    """Vérifie si un point satisfait l'équation y^2 = x^3 + ax + b"""
    if point.is_infinity:
        return True
    
    left = (point.y ** 2) % P
    right = (point.x ** 3 + A * point.x + B) % P
    return left == right

def assert_test(condition, message):
    if condition:
        print(f"[OK] {message}")
    else:
        print(f"[ERREUR] {message}")
        exit(1) # On arrête tout si un test échoue

print("--- DÉBUT DES TESTS APPROFONDIS ---")

# Tous les points générés doivent être sur la courbe
point_test = G * 10
assert_test(is_on_curve(G), "Le point G est bien sur la courbe")
assert_test(is_on_curve(point_test), f"Le point 10*G {point_test} est bien sur la courbe")

# G + G doit être égal à G * 2
p_add = G + G
p_mul = G * 2
assert_test(p_add == p_mul, "Cohérence : (G + G) == (G * 2)")

# (A + B) + C == A + (B + C)
p1 = G
p2 = G * 2
p3 = G * 3
lhs = (p1 + p2) + p3
rhs = p1 + (p2 + p3)
assert_test(lhs == rhs, "Associativité : (P1+P2)+P3 == P1+(P2+P3)")

# A + B == B + A
assert_test(p1 + p2 == p2 + p1, "Commutativité : P1 + P2 == P2 + P1")

# P + Infini = P
infini = Point(None, None)
assert_test(G + infini == G, "P + Infini == P")
assert_test(infini + G == G, "Infini + P == P")
assert_test(infini + infini == infini, "Infini + Infini == Infini")

# Si P = (x, y), alors -P = (x, -y mod P)
inv_y = (-G.y) % P
inverse_G = Point(G.x, inv_y)
assert_test((G + inverse_G).is_infinity, "P + (-P) donne bien l'Infini")

# On va multiplier G jusqu'à retomber sur l'infini pour trouver la taille du cycle
print("\n--- Recherche de l'Ordre de la Courbe ---")
current = G
order = 1
while not current.is_infinity:
    current = current + G
    order += 1
    # Sécurité anti boucle infinie
    if order > 200: 
        print("[ERREUR] Impossible de trouver l'ordre (boucle > 200)")
        break

print(f"L'ordre du groupe généré par G est : {order}")

# 8. TEST DU GRAND NOMBRE (SCALAIRE)
p_cycle = G * (order + 1)
assert_test(p_cycle == G, f"Cyclicité : G * (Ordre + 1) revient bien au départ ({G})")

print("\n--- TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS ! ---")