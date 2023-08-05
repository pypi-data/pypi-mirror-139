from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.colors import Color
from .artist import Artist


class CurveArtist(Artist):
    """Base class for artists for curves.

    Parameters
    ----------
    curve: :class:`~compas.geometry.Curve`
        The curve geometry.
    color : tuple[float, float, float] | :class:`~compas.colors.Color`, optional
        The RGB color.

    Attributes
    ----------
    curve : :class:`~compas.geometry.Curve`
        The geometry of the curve.
    color : :class:`~compas.colors.Color`
        The color of the curve.

    Class Attributes
    ----------------
    default_color : :class:`~compas.colors.Color`
        The default color of the curve.

    """

    default_color = Color(0, 0, 0)

    def __init__(self, curve, color=None, **kwargs):
        super(CurveArtist, self).__init__()
        self._curve = None
        self._color = None
        self.curve = curve
        self.color = color

    @property
    def curve(self):
        return self._curve

    @curve.setter
    def curve(self, curve):
        self._curve = curve

    @property
    def color(self):
        if not self._color:
            self.color = self.default_color
        return self._color

    @color.setter
    def color(self, color):
        if not color:
            return
        if Color.is_rgb255(color):
            self._color = Color.from_rgb255(* list(color))
        elif Color.is_hex(color):
            self._color = Color.from_hex(color)
        else:
            self._color = Color(* list(color))
