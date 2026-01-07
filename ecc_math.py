# --- CONSTANTES DE LA COURBE ---
# Equation : y^2 = x^3 + ax + b (modulo p)
A = 35
B = 3
P = 101  

def inverse_modulaire(n):
    """
    Calcule l'inverse modulaire : (1/n) modulo P.
    Utilise pow(n, -1, P) de Python.
    """
    return pow(n, -1, P)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # Si x et y sont None, c'est le point à l'infini (Element Neutre)
        self.is_infinity = (x is None) and (y is None)

    def __eq__(self, other):
        # Permet de vérifier si point1 == point2
        if self.is_infinity and other.is_infinity:
            return True
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        """
        Additionne deux points : self + other
        """
        # CAS 1 : L'un des points est l'infini (Neutre)
        if self.is_infinity:
            return other
        if other.is_infinity:
            return self

        # CAS 2 : Points alignés verticalement (x1 == x2 mais y1 != y2)
        # La somme donne le point à l'infini
        if self.x == other.x and self.y != other.y:
            return Point(None, None)

        # CAS 3 : On additionne le point à lui-même (P + P) -> Doublage
        if self == other:
            return self.double()

        # CAS 4 : Addition classique de deux points distincts (P + Q)
        # Formule Mathématique :
        # Pente (m) = (y2 - y1) / (x2 - x1) mod P
        # x3 = m^2 - x1 - x2 mod P
        # y3 = m(x1 - x3) - y1 mod P
        
        # 1. Calcul du Delta Y et Delta X
        delta_y = other.y - self.y
        delta_x = other.x - self.x
        
        # 2. Division modulaire pour la pente (m)
        # On multiplie par l'inverse modulaire du dénominateur
        # Note : On utilise self.inverse_modulaire ou la fonction globale définie plus haut
        inv_delta_x = inverse_modulaire(delta_x)
        m = (delta_y * inv_delta_x) % P
        
        # 3. Calcul de x3
        x3 = (m**2 - self.x - other.x) % P
        
        # 4. Calcul de y3
        y3 = (m * (self.x - x3) - self.y) % P
        
        return Point(x3, y3)

    def double(self):
        """
        Double le point actuel (P + P).
        """
        # PROTECTION AJOUTÉE : Doubler l'infini donne l'infini
        if self.is_infinity:
            return self

        # CAS : Tangente verticale (y == 0), donne l'infini
        if self.y == 0:
            return Point(None, None)

        # 1. Calcul de la pente (m) de la tangente
        numerateur = (3 * self.x**2 + A)      
        denominateur = (2 * self.y)           
        
        inv_denominateur = inverse_modulaire(denominateur)
        m = (numerateur * inv_denominateur) % P

        # 2. Calcul de x3
        x3 = (m**2 - 2 * self.x) % P

        # 3. Calcul de y3
        y3 = (m * (self.x - x3) - self.y) % P
        
        return Point(x3, y3)

    def __mul__(self, scalar):
        """
        Multiplication scalaire : k * P (Algo Double & Add)
        """
        # 1. Initialisation
        # Le résultat commence à "Zéro" (l'Infini en ECC)
        result = Point(None, None) 
        
        # Le point courant commence à P (1*P)
        # À chaque tour de boucle, il deviendra 2P, 4P, 8P...
        current_point = self

        # 2. Boucle Double & Add
        while scalar > 0:
            # --- ADD ---
            # Si le bit de droite est 1 (nombre impair)
            # On ajoute la valeur courante (puissance de 2) au résultat
            if scalar % 2 == 1:
                result = result + current_point
            
            # --- DOUBLE ---
            # Qu'on ait ajouté ou pas, on double le point courant pour le prochain tour
            current_point = current_point.double()
            
            # On décale les bits vers la droite (division entière par 2)
            # Ex: 101 (5) devient 10 (2)
            scalar = scalar // 2
            
        return result

    def __str__(self):
        if self.is_infinity:
            return "(Infini)"
        return f"({self.x}, {self.y})"

# Point Générateur fourni par l'énoncé
G = Point(2, 9)