from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from abc import abstractmethod

from compas.utilities import is_color_rgb
from .artist import Artist


class MeshArtist(Artist):
    """Base class for all mesh artists.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A COMPAS mesh.

    Attributes
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        The mesh data structure.
    vertices : list[int]
        The selection of vertices that should be included in the drawing.
        Defaults to all vertices.
    edges : list[tuple[int, int]]
        The selection of edges that should be included in the drawing.
        Defaults to all edges.
    faces : list[int]
        The selection of faces that should be included in the drawing.
        Defaults to all faces.
    color : tuple[float, float, float]
        The base RGB color of the mesh.
        Defaults to :attr:`default_color`.
    vertex_xyz : dict[int, list[float]]
        View coordinates of the vertices.
        Defaults to the real coordinates.
    vertex_color : dict[int, tuple[float, float, float]]
        Vertex colors.
        Missing vertices get the default vertex color :attr:`default_vertexcolor`.
    edge_color : dict[tuple[int, int], tuple[float, float, float]]
        Edge colors.
        Missing edges get the default edge color :attr:`default_edgecolor`.
    face_color : dict[int, tuple[float, float, float]]
        Face colors.
        Missing faces get the default face color :attr:`default_facecolor`.
    vertex_text : dict[int, str]
        Vertex labels.
        Defaults to the vertex identifiers.
    edge_text : dict[tuple[int, int], str]
        Edge labels.
        Defaults to the edge identifiers.
    face_text : dict[int, tuple[float, float, float]]
        Face labels.
        Defaults to the face identifiers.
    vertex_size : dict[int, float]
        Vertex sizes.
        Defaults to 1.
        Visualization of vertices with variable size is not available for all visualization contexts.
    edge_width : dict[tuple[int, int], float]
        Edge widths.
        Defaults to 1.
        Visualization of edges with variable width is not available for all visualization contexts.

    Class Attributes
    ----------------
    default_color : tuple[float, float, float]
        The default base color of the mesh.
    default_vertexcolor : tuple[float, float, float]
        The default color of the vertices of the mesh.
    default_edgecolor : tuple[float, float, float]
        The default color of the edges of the mesh.
    default_facecolor : tuple[float, float, float]
        The default color of the faces of the mesh.
    default_vertexsize : float
        The default size of the vertices of the mesh.
    default_edgewidth : float
        The default width of the edges of the mesh.

    """

    default_color = (0.0, 0.0, 0.0)
    default_vertexcolor = (1.0, 1.0, 1.0)
    default_edgecolor = (0.0, 0.0, 0.0)
    default_facecolor = (0.9, 0.9, 0.9)
    default_vertexsize = 5
    default_edgewidth = 1.0

    def __init__(self, mesh, **kwargs):
        super(MeshArtist, self).__init__()

        self._mesh = None
        self._vertices = None
        self._edges = None
        self._faces = None
        self._color = None
        self._vertex_xyz = None
        self._vertex_color = None
        self._vertex_text = None
        self._vertex_size = None
        self._edge_color = None
        self._edge_text = None
        self._edge_width = None
        self._face_color = None
        self._face_text = None

        self._vertexcollection = None
        self._edgecollection = None
        self._facecollection = None
        self._vertexnormalcollection = None
        self._facenormalcollection = None
        self._vertexlabelcollection = None
        self._edgelabelcollection = None
        self._facelabelcollection = None

        self.mesh = mesh

    @property
    def mesh(self):
        return self._mesh

    @mesh.setter
    def mesh(self, mesh):
        self._mesh = mesh
        self._vertex_xyz = None

    @property
    def vertices(self):
        if self._vertices is None:
            self._vertices = list(self.mesh.vertices())
        return self._vertices

    @vertices.setter
    def vertices(self, vertices):
        self._vertices = vertices

    @property
    def edges(self):
        if self._edges is None:
            self._edges = list(self.mesh.edges())
        return self._edges

    @edges.setter
    def edges(self, edges):
        self._edges = edges

    @property
    def faces(self):
        if self._faces is None:
            self._faces = list(self.mesh.faces())
        return self._faces

    @faces.setter
    def faces(self, faces):
        self._faces = faces

    @property
    def color(self):
        if not self._color:
            self._color = self.default_color
        return self._color

    @color.setter
    def color(self, color):
        if is_color_rgb(color):
            self._color = color

    @property
    def vertex_xyz(self):
        if self._vertex_xyz is None:
            return {vertex: self.mesh.vertex_attributes(vertex, 'xyz') for vertex in self.mesh.vertices()}
        return self._vertex_xyz

    @vertex_xyz.setter
    def vertex_xyz(self, vertex_xyz):
        self._vertex_xyz = vertex_xyz

    @property
    def vertex_color(self):
        if self._vertex_color is None:
            self._vertex_color = {vertex: self.default_vertexcolor for vertex in self.mesh.vertices()}
        return self._vertex_color

    @vertex_color.setter
    def vertex_color(self, vertex_color):
        if isinstance(vertex_color, dict):
            self._vertex_color = vertex_color
        elif is_color_rgb(vertex_color):
            self._vertex_color = {vertex: vertex_color for vertex in self.mesh.vertices()}

    @property
    def vertex_text(self):
        if self._vertex_text is None:
            self._vertex_text = {vertex: str(vertex) for vertex in self.mesh.vertices()}
        return self._vertex_text

    @vertex_text.setter
    def vertex_text(self, text):
        if text == 'key':
            self._vertex_text = {vertex: str(vertex) for vertex in self.mesh.vertices()}
        elif text == 'index':
            self._vertex_text = {vertex: str(index) for index, vertex in enumerate(self.mesh.vertices())}
        elif isinstance(text, dict):
            self._vertex_text = text

    @property
    def vertex_size(self):
        if not self._vertex_size:
            self._vertex_size = {vertex: self.default_vertexsize for vertex in self.mesh.vertices()}
        return self._vertex_size

    @vertex_size.setter
    def vertex_size(self, vertexsize):
        if isinstance(vertexsize, dict):
            self._vertex_size = vertexsize
        elif isinstance(vertexsize, (int, float)):
            self._vertex_size = {vertex: vertexsize for vertex in self.mesh.vertices()}

    @property
    def edge_color(self):
        if self._edge_color is None:
            self._edge_color = {edge: self.default_edgecolor for edge in self.mesh.edges()}
        return self._edge_color

    @edge_color.setter
    def edge_color(self, edge_color):
        if isinstance(edge_color, dict):
            self._edge_color = edge_color
        elif is_color_rgb(edge_color):
            self._edge_color = {edge: edge_color for edge in self.mesh.edges()}

    @property
    def edge_text(self):
        if self._edge_text is None:
            self._edge_text = {edge: "{}-{}".format(*edge) for edge in self.mesh.edges()}
        return self._edge_text

    @edge_text.setter
    def edge_text(self, text):
        if text == 'key':
            self._edge_text = {edge: "{}-{}".format(*edge) for edge in self.mesh.edges()}
        elif text == 'index':
            self._edge_text = {edge: str(index) for index, edge in enumerate(self.mesh.edges())}
        elif isinstance(text, dict):
            self._edge_text = text

    @property
    def edge_width(self):
        if not self._edge_width:
            self._edge_width = {edge: self.default_edgewidth for edge in self.mesh.edges()}
        return self._edge_width

    @edge_width.setter
    def edge_width(self, edgewidth):
        if isinstance(edgewidth, dict):
            self._edge_width = edgewidth
        elif isinstance(edgewidth, (int, float)):
            self._edge_width = {edge: edgewidth for edge in self.mesh.edges()}

    @property
    def face_color(self):
        if self._face_color is None:
            self._face_color = {face: self.default_facecolor for face in self.mesh.faces()}
        return self._face_color

    @face_color.setter
    def face_color(self, face_color):
        if isinstance(face_color, dict):
            self._face_color = face_color
        elif is_color_rgb(face_color):
            self._face_color = {face: face_color for face in self.mesh.faces()}

    @property
    def face_text(self):
        if self._face_text is None:
            self._face_text = {face: str(face) for face in self.mesh.faces()}
        return self._face_text

    @face_text.setter
    def face_text(self, text):
        if text == 'key':
            self._face_text = {face: str(face) for face in self.mesh.faces()}
        elif text == 'index':
            self._face_text = {face: str(index) for index, face in enumerate(self.mesh.faces())}
        elif isinstance(text, dict):
            self._face_text = text

    @abstractmethod
    def draw_vertices(self, vertices=None, color=None, text=None):
        """Draw the vertices of the mesh.

        Parameters
        ----------
        vertices : list[int], optional
            The vertices to include in the drawing.
            Default is all vertices.
        color : Union[tuple[float, float, float], dict[int, tuple[float, float, float]]], optional
            The color of the vertices,
            as either a single color to be applied to all vertices,
            or a color dict, mapping specific vertices to specific colors.
        text : dict[int, str], optional
            The text labels for the vertices
            as a text dict, mapping specific vertices to specific text labels.

        Returns
        -------
        list
            The identifiers of the objects representing the vertices in the visualization context.

        """
        raise NotImplementedError

    @abstractmethod
    def draw_edges(self, edges=None, color=None, text=None):
        """Draw the edges of the mesh.

        Parameters
        ----------
        edges : list[tuple[int, int]], optional
            The edges to include in the drawing.
            Default is all edges.
        color : tuple[float, float, float] | dict[tuple[int, int], tuple[float, float, float]], optional
            The color of the edges,
            as either a single color to be applied to all edges,
            or a color dict, mapping specific edges to specific colors.
        text : dict[tuple[int, int], str], optional
            The text labels for the edges
            as a text dict, mapping specific edges to specific text labels.

        Returns
        -------
        list
            The identifiers of the objects representing the edges in the visualization context.

        """
        raise NotImplementedError

    @abstractmethod
    def draw_faces(self, faces=None, color=None, text=None):
        """Draw the faces of the mesh.

        Parameters
        ----------
        faces : list[int], optional
            The faces to include in the drawing.
            Default is all faces.
        color : tuple[float, float, float] | dict[int, tuple[float, float, float]], optional
            The color of the faces,
            as either a single color to be applied to all faces,
            or a color dict, mapping specific faces to specific colors.
        text : dict[int, str], optional
            The text labels for the faces
            as a text dict, mapping specific faces to specific text labels.

        Returns
        -------
        list
            The identifiers of the objects representing the faces in the visualization context.

        """
        raise NotImplementedError

    @abstractmethod
    def draw_mesh(self):
        """Draw the mesh of the mesh.

        Returns
        -------
        list
            The identifiers of the objects representing the mesh in the visualization context.

        """
        raise NotImplementedError

    @abstractmethod
    def clear_vertices(self):
        """Clear the vertices of the mesh.

        Returns
        -------
        None

        """
        raise NotImplementedError

    @abstractmethod
    def clear_edges(self):
        """Clear the edges of the mesh.

        Returns
        -------
        None

        """
        raise NotImplementedError

    @abstractmethod
    def clear_faces(self):
        """Clear the faces of the mesh.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def clear(self):
        """Clear all components of the mesh.

        Returns
        -------
        None

        """
        self.clear_vertices()
        self.clear_edges()
        self.clear_faces()
