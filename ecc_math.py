import secrets
import random
A = 35
B = 3
P = 101

def inverse_modulaire(n):
    return pow(n, -1, P)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_infinity = (x is None) and (y is None)

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        if self.is_infinity and other.is_infinity:
            return True
        if self.is_infinity or other.is_infinity:
            return False
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        if self.is_infinity:
            return other
        if other.is_infinity:
            return self

        if self.x == other.x and self.y != other.y:
            return Point(None, None)

        if self == other:
            return self.double()

        delta_y = other.y - self.y
        delta_x = other.x - self.x
        
        m = (delta_y * inverse_modulaire(delta_x)) % P
        
        x3 = (m**2 - self.x - other.x) % P
        y3 = (m * (self.x - x3) - self.y) % P
        
        return Point(x3, y3)

    def double(self):
        if self.is_infinity:
            return self

        if self.y == 0:
            return Point(None, None)

        numerateur = (3 * self.x**2 + A)      
        denominateur = (2 * self.y)           
        
        m = (numerateur * inverse_modulaire(denominateur)) % P

        x3 = (m**2 - 2 * self.x) % P
        y3 = (m * (self.x - x3) - self.y) % P
        
        return Point(x3, y3)

    def __mul__(self, scalar):
        result = Point(None, None)
        current_point = self

        while scalar > 0:
            if scalar % 2 == 1:
                result = result + current_point
            
            current_point = current_point.double()
            scalar = scalar // 2
            
        return result

    def __str__(self):
        if self.is_infinity:
            return "(Infini)"
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()

G = Point(2, 9)
def generate_private_key():
    """
    Génère une clé privée aléatoire entre 1 et 1000.
    Garantit que la clé est valide (pas un multiple de l'ordre 4).
    """
    while True:
        k = random.randint(1, 1000)
        public_key = G * k
        
        if public_key.is_infinity:
            continue
            
        return k