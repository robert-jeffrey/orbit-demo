"""vector.py

Toolkit of 2d vector functions

"""

import numpy as np

from toolkit import cartesian_from_polar2d

class Vector2D:
    """A 2-dimensional cartesian vector."""
    __slots__ = ('x', 'y')
    
    def __init__(self, x, y):
        """Initialiser."""
        self.x = x
        self.y = y
        
    def __repr__(self):
        return f"Vector2D(x={self.x}, y={self.y})"
        
    def __iter__(self):
        return iter([self.x, self.y])
        
    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __radd__(self, other):
        return self + other
    
    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector2D(scalar * self.x, scalar * self.y)
    
    def __rmul__(self, scalar):
        return self * scalar
    
    def __div__(self, scalar):
        return self * (1./scalar)
    
    def __matmul__(self, other):
        return self.x * other.x + self.y * other.y
    
    def __rmatmul__(self, other):
        return self @ other

    def __abs__(self):
        return np.sqrt(self @ self)

    def angle(self):
        return np.arctan2(self.y, self.x)
    
    def polar(self):
        return abs(self), self.angle()
    
    @classmethod
    def from_polar(cls, radius, angle):
        _x, _y = cartesian_from_polar2d(radius, angle)
        return cls(_x, _y)