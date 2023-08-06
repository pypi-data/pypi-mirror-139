import math
from ammonite import ureg
from ammonite import pint


class Rectangle:
    """Class representing a rectangle"""

    @ureg.check(None, "[length]", "[length]")
    def __init__(self, width: pint.Quantity, length: pint.Quantity):
        """Construct a rectangle from its width :math:`w` and length :math:`l` and
        compute its area :math:`A` and perimeter :math:`p`

        :param width: width of the rectangle. Is expected to be a `length` unit.
        :param length: length of the rectangle. Is expected to be a `length` unit.
        """
        self.width = width
        """Rectangle width"""
        self.length = length
        """Rectangle length"""
        self.area = self.width * self.length
        """Rectangle area :math:`A = w \\cdot l`"""
        self.perimeter = (self.width + self.length) * 2
        """Rectangle perimeter :math:`p = 2 (w + l)`"""


class Square:
    """Class representing a square"""

    @ureg.check(None, "[length]")
    def __init__(self, side: pint.Quantity):
        """Construct a square from its side :math:`w` and compute its area :math:`A`
        and perimeter :math:`p`

        :param side: Side of the square. Is expected to be a `length` unit.
        """
        self.side = side
        """Square side"""
        self.area = self.side**2
        """Square area :math:`A = w \\cdot l`"""
        self.perimeter = self.side * 4
        """Square perimeter :math:`p = 2 \\cdot w \\cdot l`"""

    @classmethod
    def from_area(cls, area: pint.Quantity):
        """Construct a square, deducting its side :math:`w` from its area :math:`A`

        :math:`w = \\sqrt{A}`

        :param area: Area of the square. Is expected to be a `length²` unit.
        """
        side = area ** (1 / 2)
        return cls(side)

    @classmethod
    def from_perimeter(cls, perimeter: pint.Quantity):
        """Construct a square, deducting its side :math:`w` from its perimeter :math:`p`

        :math:`w = \\frac{p}{4}`

        :param perimeter: perimeter of the square. Is expected to be a `length` unit.
        """
        side = perimeter / 4
        return cls(side)


class Circle:
    """Class representing a circle"""

    @ureg.check(None, "[length]")
    def __init__(self, radius: pint.Quantity):
        """Construct a Circle from its radius :math:`r` and compute its diameter
        :math:`d`, area :math:`A` and perimeter :math:`p`

        :param radius: radius of the circle. Is expected to be a `length` unit.
        """
        self.radius = radius
        """Circle's radius"""
        self.diameter = 2 * self.radius
        """Circle's diameter :math:`d = 2 \\cdot r`"""
        self.area = math.pi * self.radius**2
        """Circle's area :math:`A = \\pi \\cdot r^2`"""
        self.perimeter = 2 * math.pi * self.radius
        """Circle's perimeter :math:`p = 2 \\pi \\cdot r`"""

    @classmethod
    def from_diameter(cls, diameter: pint.Quantity):
        """Construct a Circle, deducting its radius :math:`r` from its diameter
        :math:`d`.

        :math:`r=\\frac{d}{2}`

        :param diameter: diameter of the circle. Is expected to be a `length` unit.
        """
        radius = diameter / 2
        return cls(radius)

    @classmethod
    def from_area(cls, area: pint.Quantity):
        """Construct a Circle, deducting its radius :math:`r` from its area :math:`A`.

        :math:`r = \\sqrt{\\frac{A}{\\pi}}`

        :param area: area of the circle. Is expected to be a `length²` unit.
        """
        radius = (area / math.pi) ** (1 / 2)
        return cls(radius)

    @classmethod
    def from_perimeter(cls, perimeter: pint.Quantity):
        """Construct a Circle, deducting its radius :math:`r` from its perimeter
        :math:`p`:

        :math:`r = \\frac{p}{2\\pi}`

        :param perimeter: perimeter of the circle. Is expected to be a `length` unit.
        """
        diameter = perimeter / math.pi
        return cls.from_diameter(diameter=diameter)
