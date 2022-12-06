
from typing import Union
import math

number_types = Union[int, float, complex]

class Vector2D:
    """A two-dimensional vector with Cartesian coordinates."""
    def __init__(self, x : number_types, y : number_types) -> "Vector2D":
        """Initialisation of a Vector2D."""
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        """returns: Unambiguous string representation of the vector."""
        return f"Vector2D({self.x, self.y})"

    def __str__(self) -> str:
        """returns: string representation of the vector."""
        return  f"{self.x, self.y}"

    def __add__(self, other : Union[number_types, "Vector2D"]) -> "Vector2D":
        """Vector addition."""
        if other is int or other is float or other is complex:
            return Vector2D(self.x + other, self.y + other)
        return Vector2D(self.x + other.x, self.y+other.y)

    def __mul__(self, other : Union[number_types, "Vector2D"]) -> Union[number_types,"Vector2D"]:
        """Multiplication of scalar or vectors"""
        if other is int or other is float or other is complex:
            return Vector2D(self.x*other, self.y*other)
        return self.x*other.x + self.y*other.y



    def __radd__(self, other : Union[number_types, "Vector2D"]) -> "Vector2D":
        """Right vector addition."""
        return self.__add__(other)

    def __iadd__(self, other : "Vector2D") -> "Vector2D":
        """Addittion to self."""
        self = self.__add__(other)
        return self

    def __rmul__(self, other : Union[number_types, "Vector2D"]) -> Union[number_types,"Vector2D"]:
        """Right multiplication of scalar or vectors"""
        return self.__mul__(other)

    def __imul__(self, other : Union[number_types, "Vector2D"]) -> Union[number_types,"Vector2D"]:
        """Right multiplication of scalar or vectors"""
        self = self.__mul__(other)
        return self

    def __neg__(self) -> "Vector2D":
        """Negation of the vector."""
        return Vector2D(-self.x, -self.y)

    def __abs__(self) -> number_types:
        """Absolute value (length) of the vector."""
        return math.sqrt(self.x**2 + self.y**2)

    def __eq__(self, other : "Vector2D") -> bool:
        """Compares 2 vectors,
        returns: bool -
        true if they have equal coorinates false otherwise"""
        return self.x, self.y == other.x, other.y

    def distance_to(self, other : "Vector2D") -> number_types:
        """The distance between vectors self and other."""
        return abs(self - other)

    def to_polar(self) -> tuple[number_types, number_types]:
        """Return the vector's components in polar coordinates."""
        return self.__abs__(), math.atan2(self.y, self.x)