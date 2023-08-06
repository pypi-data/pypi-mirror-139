"""Units of Measure - based on the International System of Units - 9th edition

https://www.bipm.org/en/publications/si-brochure
"""
from fractions import Fraction
from typing import Generic, TypeVar
from weakref import ref

# TODO map dimensions to quantity names
class Dimension:
    """Dimension of quantity: a product of integer powers of SI base units
    
    For each SI base unit symbol (kg, m, s, A, K, cd, mol)
    an attribute with the same name stores the exponent.
    """

    def __init__(
            self,
            kg:  int = 0,
            m:   int = 0,
            s:   int = 0,
            A:   int = 0,
            K:   int = 0,
            cd:  int = 0,
            mol: int = 0
        ) -> None:
        """The default dimension is the scalar, where all exponents are 0.

        Thus the product is 1, the identity element of dimensions.
        The order of parameters is close to the order of base units
        in the definition of the SI derived units.
        """
        self.kg  = kg
        self.m   = m
        self.s   = s
        self.A   = A
        self.K   = K
        self.cd  = cd
        self.mol = mol
    
    def __eq__(self, other) -> bool:
        """Two dimensions are equal if all exponents are equal."""
        if type(self) != type(other):
            return NotImplemented
        return (
            self.kg  == other.kg and
            self.m   == other.m  and
            self.s   == other.s  and
            self.A   == other.A  and
            self.K   == other.K  and
            self.cd  == other.cd and
            self.mol == other.mol
        )
    
    def __repr__(self) -> str:
        """Returns the equivalent constructor"""
        return (self.__class__.__name__ +
            "(kg="   + repr(self.kg)  +
            ", m="   + repr(self.m)   +
            ", s="   + repr(self.s)   +
            ", A="   + repr(self.A)   +
            ", K="   + repr(self.K)   +
            ", cd="  + repr(self.cd)  +
            ", mol=" + repr(self.mol) +
            ")")

# The identity element of dimensions
SCALAR = Dimension()

class Prefix:
    """Order of magnitude with an integer base and exponent
    
    The base is the magnitude and the exponent is the number of orders.
    Prefixes have the following attributes.
    - base: magnitude
    - exponent: number of orders
    - symbol: short string used in formulas, tables, and charts
    - name: long string used in flow text
    Prefixes with base 10 and exponents that are integer multiples of 3 in the interval [-24,24]
    or integers in the interval [-2,2] map to SI decimal prefixes.
    Prefixes with base 2 and exponents that are integer multiples of 10 up to 80 map to SI binary prefixes.
    """

    def __init__(
            self,
            base: int = 10,
            exponent: int = 0,
            symbol: str = "",
            name: str = ""
        ) -> None:
        """The default is 10 raised to 0, resulting in the value 1, the identity element of prefixes"""
        self.base = base
        self.exponent = exponent
        self.symbol = symbol
        self.name = name
    
    def __eq__(self, other) -> bool:
        """Two prefixes are equal if both the base and exponent are equal.
        
        Exponent zero with different bases is not equal,
        because the same non-zero exponent results in different values.
        """
        if type(self) != type(other):
            return NotImplemented
        return (
            self.base     == other.base and
            self.exponent == other.exponent
        )

    def __str__(self) -> str:
        """Returns the symbol"""
        return self.symbol
    
    def __repr__(self) -> str:
        """Returns the equivalent constructor"""
        return (self.__class__.__name__ +
            "(base=" + repr(self.base) +
            ", exponent=" + repr(self.exponent) +
            ", symbol=\"" + self.symbol +
            "\", name=\"" + self.name +
            "\")")

# The prefix of 1 (written as no prefix), the identity element of prefixes
PREFIX_1 = Prefix()

class Unit:
    """Product of dimension, prefix, and factor

    Units have the following attributes.
    - symbol: short string used in formulas, tables, and charts
    - name: long string used in flow text
    - dimension: product of integer powers of base units
    - prefix: order of magnitude (logarithmic scale)
    - factor: ratio as fraction of integers (linear scale)
    """

    FRACTION_1 = Fraction(1,1)

    def __init__(
            self,
            symbol: str = "",
            name: str = "",
            dimension: Dimension = SCALAR,
            prefix: Prefix = PREFIX_1,
            factor: Fraction = FRACTION_1
        ) -> None:
        """The default unit is no unit, or the value of 1."""
        self.symbol = symbol
        self.name = name
        self.dimension = dimension
        self.prefix = prefix
        self.factor = factor
    
    def __eq__(self, other: object) -> bool:
        """Units are equal if all attributes are equal."""
        if type(self) != type(other):
            return NotImplemented
        return (
            self.symbol    == other.symbol    and
            self.name      == other.name      and
            self.dimension == other.dimension and
            self.prefix    == other.prefix    and
            self.factor    == other.factor
        )
    
    def __str__(self) -> str:
        """Returns the symbol"""
        return self.symbol
    
    def __repr__(self) -> str:
        """Returns the equivalent constructor"""
        return (self.__class__.__name__ +
            "(symbol=\"" + self.symbol +
            "\", name=\"" + self.name +
            "\", dimension=" + repr(self.dimension) +
            ", prefix=" + repr(self.prefix) +
            ", factor=" + repr(self.factor) +
            ")")

# The unit of 1 (written as no unit)
UNIT_1 = Unit()

class GarbageError(Exception):
    """The object was garbage-collected."""
    pass

T = TypeVar("T")

class UnitMap(Generic[T]):
    """Map objects to units.

    The objects are not used as keys directly, because not all objects are hashable.
    Instead the integer value of id(object) is used as key,
    but two objects with non-overlapping lifetimes may have the same id() value.
    See https://docs.python.org/3/library/functions.html#id.
    
    To detect this case, a weak reference to the object is stored
    in the dictionary value together with the unit.

    The units can be objects as well and need not be of type Unit.
    """

    def __init__(self, value:T = Unit) -> None:
        """Create an empty map with the default value type Unit."""
        self.units = {} # dictionary maps id(object) to (ref(object), unit)
        self.value = value
    
    def set(self, o: object, unit: T) -> None:
        """Map the object ID to the tuple (ref(object), unit) to keep a weak reference to the object.

        Otherwise the object could be garbage-collected and its ID re-used
        for a different object without being detected.
        """
        # TODO Remove the object ID from the dictionary on finalize.
        # TODO Guard against types re-using instances, instead of relying on ref
        self.units[id(o)] = (ref(o), unit)

    def get(self, o: object) -> T:
        """Return the unit of the object.
        
        Throws GarbageError when to object was garbage-collected already.
        """

        # map the object ID to its tuple (ref, unit) and then return the unit
        (weak, unit) = self.units[id(o)]
        if (weak() is None):
            raise GarbageError
        return unit

# default unit map
unit_map = UnitMap[Unit]()

def map_to_unit(unit: object, map: UnitMap = unit_map): # -> ((o: object) -> object) requires Python 3.11
    """Decorate functions or classes with units."""
    def wrap(o: object) -> object:
        """Map object (function or class) to unit and return object."""
        map.set(o, unit)
        return o
    return wrap

def set_unit(o: object, unit: object, map: UnitMap = unit_map) -> None:
    """Set object to unit in map."""
    map.set(o, unit)

def get_unit(o: object, map: UnitMap = unit_map) -> object:
    """Get unit of object from map."""
    return map.get(o)
