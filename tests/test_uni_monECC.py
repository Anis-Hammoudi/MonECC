import sys
import os
sys.path.append(os.path.abspath(".."))
from ecc_math import G, Point

def test_point_operations():
    P = G
    Q = G + G
    assert isinstance(Q, Point)
    assert Q != P

    k = 5
    R1 = G * k
    R2 = G + G + G + G + G
    assert R1 == R2

    inf = Point(None, None)
    assert G + inf == G
    assert inf + G == G

    print("Tests ECC OK!")

test_point_operations()
