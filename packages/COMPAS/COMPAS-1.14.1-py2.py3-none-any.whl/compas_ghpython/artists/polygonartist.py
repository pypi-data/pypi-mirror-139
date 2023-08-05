from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython
from compas.artists import PrimitiveArtist
from .artist import GHArtist


class PolygonArtist(GHArtist, PrimitiveArtist):
    """Artist for drawing polygons.

    Parameters
    ----------
    polygon : :class:`compas.geometry.Polygon`
        A COMPAS polygon.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`compas_ghpython.artists.GHArtist` and :class:`compas.artists.PrimitiveArtist` for more info.

    """

    def __init__(self, polygon, **kwargs):
        super(PolygonArtist, self).__init__(primitive=polygon, **kwargs)

    def draw(self, show_points=False, show_edges=False, show_face=True):
        """Draw the polygon.

        Parameters
        ----------
        show_points : bool, optional
            If True, draw the points of the polygon.
        show_edges : bool, optional
            If True, draw the edges of the polygon.
        show_face : bool, optional
            If True, draw the face of the polygon.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Point3d`, :rhino:`Rhino.Geometry.Line`, :rhino:`Rhino.Geometry.Mesh`]
            The Rhino points, lines and face.

        """
        _points = map(list, self.primitive.points)
        result = []
        if show_points:
            points = [{'pos': point, 'color': self.color, 'name': self.primitive.name} for point in _points]
            result += compas_ghpython.draw_points(points)
        if show_edges:
            lines = [{'start': list(a), 'end': list(b), 'color': self.color, 'name': self.primitive.name} for a, b in self.primitive.lines]
            result += compas_ghpython.draw_lines(lines)
        if show_face:
            polygons = [{'points': _points, 'color': self.color, 'name': self.primitive.name}]
            result += compas_ghpython.draw_faces(polygons)
        return result
