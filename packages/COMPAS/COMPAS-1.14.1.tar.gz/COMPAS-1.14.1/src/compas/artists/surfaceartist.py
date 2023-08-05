from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.colors import Color
from .artist import Artist


class SurfaceArtist(Artist):
    """Base class for artists for surfaces.

    Parameters
    ----------
    surface: :class:`~compas.geometry.Surface`
        The surface geometry.
    color : tuple[float, float, float] | :class:`~compas.colors.Color`, optional
        The RGB color.

    Attributes
    ----------
    surface : :class:`~compas.geometry.Surface`
        The geometry of the surface.
    color : :class:`~compas.colors.Color`
        The color of the surface.

    Class Attributes
    ----------------
    default_color : :class:`~compas.colors.Color`
        The default color of the surface.

    """

    default_color = Color(0, 0, 0)

    def __init__(self, surface, color=None, **kwargs):
        super(SurfaceArtist, self).__init__()
        self._surface = None
        self._color = None
        self.surface = surface
        self.color = color

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, surface):
        self._surface = surface

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
