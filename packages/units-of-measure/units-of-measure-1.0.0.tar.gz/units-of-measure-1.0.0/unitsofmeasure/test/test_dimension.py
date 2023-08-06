"""Test Dimension"""
import pytest
from unitsofmeasure import Dimension, SCALAR

@pytest.mark.parametrize(
    "dimension        , kg , m , s , A , K , cd , mol , representation",[
    (Dimension()      ,  0 , 0 , 0 , 0 , 0 ,  0 ,   0 , "Dimension(kg=0, m=0, s=0, A=0, K=0, cd=0, mol=0)"), # scalar
    (Dimension(kg=1)  ,  1 , 0 , 0 , 0 , 0 ,  0 ,   0 , "Dimension(kg=1, m=0, s=0, A=0, K=0, cd=0, mol=0)"), # SI base units
    (Dimension(m=1)   ,  0 , 1 , 0 , 0 , 0 ,  0 ,   0 , "Dimension(kg=0, m=1, s=0, A=0, K=0, cd=0, mol=0)"),
    (Dimension(s=1)   ,  0 , 0 , 1 , 0 , 0 ,  0 ,   0 , "Dimension(kg=0, m=0, s=1, A=0, K=0, cd=0, mol=0)"),
    (Dimension(A=1)   ,  0 , 0 , 0 , 1 , 0 ,  0 ,   0 , "Dimension(kg=0, m=0, s=0, A=1, K=0, cd=0, mol=0)"),
    (Dimension(K=1)   ,  0 , 0 , 0 , 0 , 1 ,  0 ,   0 , "Dimension(kg=0, m=0, s=0, A=0, K=1, cd=0, mol=0)"),
    (Dimension(cd=1)  ,  0 , 0 , 0 , 0 , 0 ,  1 ,   0 , "Dimension(kg=0, m=0, s=0, A=0, K=0, cd=1, mol=0)"),
    (Dimension(mol=1) ,  0 , 0 , 0 , 0 , 0 ,  0 ,   1 , "Dimension(kg=0, m=0, s=0, A=0, K=0, cd=0, mol=1)")
])
def test(dimension: Dimension, kg: int, m: int, s: int, A: int, K: int, cd: int, mol: int, representation: str) -> None:
    assert dimension.kg  == kg
    assert dimension.m   == m
    assert dimension.s   == s
    assert dimension.A   == A
    assert dimension.K   == K
    assert dimension.cd  == cd
    assert dimension.mol == mol

    # test equality
    other = Dimension(kg, m, s, A, K, cd, mol)
    assert id(dimension) != id(other)
    assert dimension == other

    # test representation
    assert repr(dimension) == representation

def test_scalar() -> None:
    assert SCALAR.kg  == 0
    assert SCALAR.m   == 0
    assert SCALAR.s   == 0
    assert SCALAR.A   == 0
    assert SCALAR.K   == 0
    assert SCALAR.cd  == 0
    assert SCALAR.mol == 0
