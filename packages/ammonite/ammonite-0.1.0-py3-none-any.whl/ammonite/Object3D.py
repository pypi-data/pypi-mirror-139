import math
from ammonite import ureg
from ammonite import pint


class Box:
    """Class representing a box"""

    @ureg.check(None, "[length]", "[length]", "[length]")
    def __init__(
        self, width: pint.Quantity, depth: pint.Quantity, height: pint.Quantity
    ):
        """Construct Box from its width :math:`w`, depth :math:`d`, height :math:`h`
        and compute its volume :math:`V` and area :math:`A`

        :param width: width of the box. Is expected to be a `length` unit.
        :param depth: depth of the box. Is expected to be a `length` unit.
        :param height: height of the box. Is expected to be a `length` unit.
        """
        self.width = width
        """Box's width"""
        self.depth = depth
        """Box's depth"""
        self.height = height
        """Box's height"""
        self.volume = self.width * self.depth * self.height
        """Box's volume :math:`V = w \\cdot d \\cdot h`"""
        self.area = 2 * (
            self.width * self.depth
            + self.depth * self.height
            + self.height * self.width
        )
        """Box's area :math:`A = 2(w \\cdot d + d \\cdot h + h \\cdot w)`"""


class Cube:
    """Class representing a cube"""

    @ureg.check(None, "[length]")
    def __init__(self, side: pint.Quantity):
        """Construct a Cube from its side :math:`w` and compute its volume :math:`V`
        and area :math:`A`

        :param side: side of the cube. Is expected to be a `length` unit.
        """
        self.side = side
        """Cube's side"""
        self.volume = self.side**3
        """Cube's volume :math:`V = w^3`"""
        self.area = 6 * (self.side**2)
        """Cube's area :math:`A = 6 \\cdot w^2`"""

    @classmethod
    def from_volume(cls, volume: pint.Quantity):
        """Construct Cube from its volume, deducting its side :math:`w` from its
        volume :math:`V`

        :math:`w = \\root{3}\\of{V}`

        :param volume: volume of the cube. Is expected to be a `length³` unit.
        """
        side = volume ** (1 / 3)
        return cls(side)

    @classmethod
    def from_area(cls, area: pint.Quantity):
        """Construct Cube from its area, deducting its side :math:`w` from its area
        :math:`A`

        :math:`w = \\sqrt{\\frac{A}{6}}`

        :param area: area of the cube. Is expected to be a `length²` unit.
        """
        side = (area / 6) ** (1 / 2)
        return cls(side)


class Sphere:
    """Class representing a sphere"""

    @ureg.check(None, "[length]")
    def __init__(self, radius):
        """Construct a Sphere from its radius and compute its diameter :math:`d`,
        volume :math:`V` and area :math:`A`

        :param radius: radius of the sphere. Is expected to be a `length` unit.
        """
        self.radius = radius
        """Sphere's radius"""
        self.diameter = 2 * self.radius
        """Sphere's diameter :math:`d = \\frac{r}{2}`"""
        self.volume = 4 / 3 * math.pi * self.radius**3
        """Sphere's volume :math:`V = \\frac{4}{3} \\pi r^3`"""
        self.area = 4 * math.pi * self.radius**2
        """Sphere's area :math:`A = 4 \\pi r^2`"""

    @classmethod
    def from_diameter(cls, diameter: pint.Quantity):
        """Construct a Sphere from its diameter, deducting its radius :math:`r` from
        its diameter :math:`d`

        :math:`r=\\frac{d}{2}`

        :param diameter: diameter of the sphere. Is expected to be a `length` unit.
        """
        radius = diameter / 2
        return cls(radius)

    @classmethod
    def from_volume(cls, volume: pint.Quantity):
        """Construct a Sphere from its volume, deducting its radius :math:`r` from
        its volume :math:`V`

        :math:`r=\\root{3}\\of{\\frac{3 \\cdot V}{4 \\pi}}`

        :param volume: Volume of the sphere . Is expected to be a `length³` unit.
        """
        radius = (3 * volume / (4 * math.pi)) ** (1 / 3)
        return cls(radius)

    @classmethod
    def from_area(cls, area: pint.Quantity):
        """Construct a Sphere from its area, deducting its radius :math:`r` from its
        area :math:`A`

        :math:`r=\\sqrt{\\frac{A}{4 \\pi}}`

        :param area: Are of the sphere. Is expected to be a `length²` unit.
        """
        radius = (area / (4 * math.pi)) ** (1 / 2)
        return cls(radius)
