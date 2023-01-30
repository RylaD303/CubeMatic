
from typing import Union
from math import atan2, sqrt, cos, sin

number_types = Union[int, float, complex]

class Vector2D:
    """A two-dimensional vector with Cartesian coordinates."""
    def __init__(self, x_axis: number_types, y_axis: number_types) -> "None":
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
        if type(other) in [int, float, complex]:
            return Vector2D(self.x + other, self.y + other)
        return Vector2D(self.x + other.x, self.y+other.y)

    def __mul__(self, other : Union[number_types, "Vector2D"]) -> Union[number_types,"Vector2D"]:
        """Multiplication of scalar or vectors"""
        if type(other) in [int, float, complex]:
            return Vector2D(self.x*other, self.y*other)
        return self.x*other.x + self.y*other.y

    def __sub__(self, other : Union[number_types, "Vector2D"]) -> "Vector2D":
        """Vector subtraction."""
        if type(other) in [int, float, complex]:
            return Vector2D(self.x - other, self.y - other)
        return Vector2D(self.x - other.x, self.y - other.y)

    def __truediv__(self, other : number_types) -> "Vector2D":
        """Vector division."""
        return Vector2D(self.x/other, self.y/other)

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
        """Self multiplication of scalar or vectors"""
        self = self.__mul__(other)
        return self

    def __rsub__(self, other : Union[number_types, "Vector2D"]) -> "Vector2D":
        """Right vector subtraction."""
        return self.__sub__(other)

    def __isub__(self, other : Union[number_types, "Vector2D"]) -> "Vector2D":
        """Self vector subtraction."""
        self = self.__sub__(other)
        return self

    def __itruediv__(self, other : number_types) -> "Vector2D":
        """Self vector division."""
        self = self.__truediv__(other)
        return self

    def __neg__(self) -> "Vector2D":
        """Negation of the vector."""
        return Vector2D(-self.x, -self.y)

    def __abs__(self) -> number_types:
        """Absolute value (length) of the vector."""
        return sqrt(self.x**2 + self.y**2)

    def __eq__(self, other : Union["Vector2D", tuple[number_types, number_types]]) -> bool:
        """Compares 2 vectors or vector and tuple of (number , number),
        returns: bool -
        true if they have equal coorinates false otherwise"""
        if type(other) is tuple:
            return (self.x, self.y) == other
        return (self.x, self.y) == (other.x, other.y)

    def __neq__(self, other : Union["Vector2D", tuple[number_types, number_types]]) -> bool:
        """Compares 2 vectors or vector and tuple of (number , number),
        returns: bool -
        true if they don't have equal coorinates false otherwise"""
        return not self==other

    def __iter__(self):
        """Returns an iterable of the Vector2D"""
        yield self.x
        yield self.y


    def distance_to(self, other : "Vector2D") -> number_types:
        """The distance between vectors self and other."""
        return abs(self - other)

    def to_polar(self) -> tuple[number_types, number_types]:
        """Return the vector's components in polar coordinates."""
        return self.__abs__(), atan2(self.y, self.x)

    def blend(self, other : "Vector2D", scale : number_types) -> None:
        """Blends two vectors into self.
        scale = 0 : stays self, scale = 1 : becomes other"""
        self = (1-scale)*self + scale*other

    def angle_rotated(self , angle) -> "Vector2D":
        """Returns new vector rotated by with the given angle. Angle should be in pi value."""
        copy = Vector2D(
            self.x*cos(angle) - self.y*sin(angle),
            self.x*sin(angle) + self.y*cos(angle))
        return copy

    def angle_rotate(self , angle) -> "Vector2D":
        """Rotates the vector by the given angle. Angle should be in pi value."""
        self.x, self.y =\
            self.x*cos(angle) - self.y*sin(angle),\
            self.x*sin(angle) + self.y*cos(angle)
