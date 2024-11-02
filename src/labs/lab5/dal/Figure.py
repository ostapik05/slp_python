import numpy as np


class Vertex:
    def __init__(self, x, y, z, color=(0, 0, 100)):
        self.position = np.array([x, y, z], dtype=np.float32)
        self.color = color
    def position(self):
        return self.x, self.y, self.z


class Edge:
    def __init__(self, start_vertex: Vertex, end_vertex: Vertex, color=(1, 0, 0)):
        self.vertices = (start_vertex, end_vertex)
        self.color = color


class Face:
    def __init__(self, vertices: list[Vertex], color=(0, 1, 0)):
        self.vertices = vertices
        self.color = color


class FigureData:
    def __init__(self, vertices, edges, faces=None, color=(1, 1, 1), draw_mode='edges'):
        # Determine if vertices are already instances of Vertex
        self.vertices = [v if isinstance(v, Vertex) else Vertex(*v) for v in vertices]
        self.edges = [Edge(*e) for e in edges]
        self.faces = [Face(f) for f in faces] if faces is not None else []
        self.color = color
        self.angle = [0, 0, 0]
        self.draw_mode = draw_mode
        self.selected = False

class FigureData:
    def __init__(self, vertices, edges, faces=None, color=(1, 1, 1), draw_mode='edges', figure_color = True):
        self.vertices = [v if isinstance(v, Vertex) else Vertex(*v) for v in vertices]
        self.edges = [e if isinstance(e, Edge) else Edge(*e) for e in edges]
        self.faces = [f if isinstance(f, Face) else Face(f) for f in faces] if faces is not None else []
        self.color = color
        self.angle = [0, 0, 0]
        self.draw_mode = draw_mode
        self.selected = False
        self.figure_color = True

# Cube example
cube_vertices = [
    Vertex(-1, -1, -1), Vertex(1, -1, -1), Vertex(1, 1, -1), Vertex(-1, 1, -1),
    Vertex(-1, -1, 1), Vertex(1, -1, 1), Vertex(1, 1, 1), Vertex(-1, 1, 1)
]
cube_edges = [Edge(cube_vertices[0], cube_vertices[1]), Edge(cube_vertices[1], cube_vertices[2]),
              Edge(cube_vertices[2], cube_vertices[3]), Edge(cube_vertices[3], cube_vertices[0]),
              Edge(cube_vertices[4], cube_vertices[5]), Edge(cube_vertices[5], cube_vertices[6]),
              Edge(cube_vertices[6], cube_vertices[7]), Edge(cube_vertices[7], cube_vertices[4]),
              Edge(cube_vertices[0], cube_vertices[4]), Edge(cube_vertices[1], cube_vertices[5]),
              Edge(cube_vertices[2], cube_vertices[6]), Edge(cube_vertices[3], cube_vertices[7])]
cube_faces = [Face([cube_vertices[0], cube_vertices[1], cube_vertices[2], cube_vertices[3]]),
              Face([cube_vertices[4], cube_vertices[5], cube_vertices[6], cube_vertices[7]]),
              Face([cube_vertices[0], cube_vertices[1], cube_vertices[5], cube_vertices[4]]),
              Face([cube_vertices[2], cube_vertices[3], cube_vertices[7], cube_vertices[6]]),
              Face([cube_vertices[0], cube_vertices[3], cube_vertices[7], cube_vertices[4]]),
              Face([cube_vertices[1], cube_vertices[2], cube_vertices[6], cube_vertices[5]])]
cube_data = FigureData(cube_vertices, cube_edges, cube_faces, color=(0, 1, 0))

# Pyramid example
pyramid_vertices = [
    Vertex(0, 1, 0), Vertex(-1, -1, -1), Vertex(1, -1, -1),
    Vertex(1, -1, 1), Vertex(-1, -1, 1)
]
pyramid_edges = [Edge(pyramid_vertices[0], pyramid_vertices[1]), Edge(pyramid_vertices[0], pyramid_vertices[2]),
                 Edge(pyramid_vertices[0], pyramid_vertices[3]), Edge(pyramid_vertices[0], pyramid_vertices[4]),
                 Edge(pyramid_vertices[1], pyramid_vertices[2]), Edge(pyramid_vertices[2], pyramid_vertices[3]),
                 Edge(pyramid_vertices[3], pyramid_vertices[4]), Edge(pyramid_vertices[4], pyramid_vertices[1])]
pyramid_faces = [Face([pyramid_vertices[0], pyramid_vertices[1], pyramid_vertices[2]]),
                 Face([pyramid_vertices[0], pyramid_vertices[2], pyramid_vertices[3]]),
                 Face([pyramid_vertices[0], pyramid_vertices[3], pyramid_vertices[4]]),
                 Face([pyramid_vertices[0], pyramid_vertices[4], pyramid_vertices[1]]),
                 Face([pyramid_vertices[1], pyramid_vertices[2], pyramid_vertices[3], pyramid_vertices[4]])]
pyramid_data = FigureData(pyramid_vertices, pyramid_edges, pyramid_faces, color=(1, 0, 0), draw_mode='faces')

# Sphere example
sphere_vertices = [
    Vertex(-1, 0, 0), Vertex(1, 0, 0), Vertex(0, 1, 0),
    Vertex(0, -1, 0), Vertex(0, 0, 1), Vertex(0, 0, -1)
]
sphere_edges = [Edge(sphere_vertices[0], sphere_vertices[1]), Edge(sphere_vertices[2], sphere_vertices[3]),
                Edge(sphere_vertices[4], sphere_vertices[5])]
sphere_faces = [Face([sphere_vertices[0], sphere_vertices[1], sphere_vertices[2]]),
                Face([sphere_vertices[3], sphere_vertices[4], sphere_vertices[5]])]
sphere_data = FigureData(sphere_vertices, sphere_edges, sphere_faces, color=(0, 0, 1), draw_mode='edges')


# Tetrahedron example
tetrahedron_vertices = [
    Vertex(1, 1, 1), Vertex(-1, -1, 1), Vertex(-1, 1, -1), Vertex(1, -1, -1)
]
tetrahedron_edges = [Edge(tetrahedron_vertices[0], tetrahedron_vertices[1]),
                     Edge(tetrahedron_vertices[0], tetrahedron_vertices[2]),
                     Edge(tetrahedron_vertices[0], tetrahedron_vertices[3]),
                     Edge(tetrahedron_vertices[1], tetrahedron_vertices[2]),
                     Edge(tetrahedron_vertices[1], tetrahedron_vertices[3]),
                     Edge(tetrahedron_vertices[2], tetrahedron_vertices[3])]
tetrahedron_faces = [Face([tetrahedron_vertices[0], tetrahedron_vertices[1], tetrahedron_vertices[2]]),
                     Face([tetrahedron_vertices[1], tetrahedron_vertices[2], tetrahedron_vertices[3]]),
                     Face([tetrahedron_vertices[2], tetrahedron_vertices[3], tetrahedron_vertices[0]]),
                     Face([tetrahedron_vertices[3], tetrahedron_vertices[0], tetrahedron_vertices[1]])]
tetrahedron_data = FigureData(tetrahedron_vertices, tetrahedron_edges, tetrahedron_faces, color=(1, 1, 0),
                                draw_mode='faces')


# Hexahedron example
hexahedron_vertices = [
    Vertex(1, 1, 1), Vertex(-1, 1, 1), Vertex(-1, -1, 1), Vertex(1, -1, 1),
    Vertex(1, -1, -1), Vertex(1, 1, -1), Vertex(-1, 1, -1), Vertex(-1, -1, -1)
]
hexahedron_edges = [Edge(hexahedron_vertices[0], hexahedron_vertices[1]),
                    Edge(hexahedron_vertices[1], hexahedron_vertices[2]),
                    Edge(hexahedron_vertices[2], hexahedron_vertices[3]),
                    Edge(hexahedron_vertices[3], hexahedron_vertices[0]),
                    Edge(hexahedron_vertices[4], hexahedron_vertices[5]),
                    Edge(hexahedron_vertices[5], hexahedron_vertices[6]),
                    Edge(hexahedron_vertices[6], hexahedron_vertices[7]),
                    Edge(hexahedron_vertices[7], hexahedron_vertices[4]),
                    Edge(hexahedron_vertices[0], hexahedron_vertices[5]),
                    Edge(hexahedron_vertices[1], hexahedron_vertices[6]),
                    Edge(hexahedron_vertices[2], hexahedron_vertices[7]),
                    Edge(hexahedron_vertices[3], hexahedron_vertices[4])]
hexahedron_faces = [
    Face([hexahedron_vertices[0], hexahedron_vertices[1], hexahedron_vertices[2], hexahedron_vertices[3]]),
    Face([hexahedron_vertices[4], hexahedron_vertices[5], hexahedron_vertices[6], hexahedron_vertices[7]]),
    Face([hexahedron_vertices[0], hexahedron_vertices[1], hexahedron_vertices[6], hexahedron_vertices[5]]),
    Face([hexahedron_vertices[1], hexahedron_vertices[2], hexahedron_vertices[7], hexahedron_vertices[6]]),
    Face([hexahedron_vertices[2], hexahedron_vertices[3], hexahedron_vertices[4], hexahedron_vertices[7]]),
    Face([hexahedron_vertices[3], hexahedron_vertices[0], hexahedron_vertices[5], hexahedron_vertices[4]])]
hexahedron_data = FigureData(hexahedron_vertices, hexahedron_edges, hexahedron_faces, color=(0, 1, 1),
                               draw_mode='faces')


# Octahedron example
octahedron_vertices = [
    Vertex(0, 1, 0), Vertex(1, 0, 0), Vertex(0, 0, 1),
    Vertex(-1, 0, 0), Vertex(0, 0, -1), Vertex(0, -1, 0)
]
octahedron_edges = [Edge(octahedron_vertices[0], octahedron_vertices[1]),
                    Edge(octahedron_vertices[0], octahedron_vertices[2]),
                    Edge(octahedron_vertices[0], octahedron_vertices[3]),
                    Edge(octahedron_vertices[0], octahedron_vertices[4]),
                    Edge(octahedron_vertices[1], octahedron_vertices[2]),
                    Edge(octahedron_vertices[2], octahedron_vertices[3]),
                    Edge(octahedron_vertices[3], octahedron_vertices[4]),
                    Edge(octahedron_vertices[4], octahedron_vertices[1]),
                    Edge(octahedron_vertices[1], octahedron_vertices[5]),
                    Edge(octahedron_vertices[2], octahedron_vertices[5]),
                    Edge(octahedron_vertices[3], octahedron_vertices[5]),
                    Edge(octahedron_vertices[4], octahedron_vertices[5])]
octahedron_faces = [Face([octahedron_vertices[0], octahedron_vertices[1], octahedron_vertices[2]]),
                    Face([octahedron_vertices[0], octahedron_vertices[2], octahedron_vertices[3]]),
                    Face([octahedron_vertices[0], octahedron_vertices[3], octahedron_vertices[4]]),
                    Face([octahedron_vertices[0], octahedron_vertices[4], octahedron_vertices[1]]),
                    Face([octahedron_vertices[5], octahedron_vertices[1], octahedron_vertices[2]]),
                    Face([octahedron_vertices[5], octahedron_vertices[2], octahedron_vertices[3]]),
                    Face([octahedron_vertices[5], octahedron_vertices[3], octahedron_vertices[4]]),
                    Face([octahedron_vertices[5], octahedron_vertices[4], octahedron_vertices[1]])]
octahedron_data = FigureData(octahedron_vertices, octahedron_edges, octahedron_faces, color=(1, 0, 1),
                               draw_mode='edges')


# Icosahedron example
icosahedron_vertices = [
    Vertex(0, 1, 0), Vertex(0.8944, 0.4472, 0), Vertex(0.2764, 0.4472, 0.8506),
    Vertex(-0.7236, 0.4472, 0.5257), Vertex(-0.7236, 0.4472, -0.5257), Vertex(0.2764, 0.4472, -0.8506),
    Vertex(0.7236, -0.4472, 0.5257), Vertex(-0.2764, -0.4472, 0.8506), Vertex(-0.8944, -0.4472, 0),
    Vertex(-0.2764, -0.4472, -0.8506), Vertex(0.7236, -0.4472, -0.5257), Vertex(0, -1, 0)
]
icosahedron_edges = [Edge(icosahedron_vertices[0], icosahedron_vertices[1]),
                     Edge(icosahedron_vertices[0], icosahedron_vertices[2]),
                     Edge(icosahedron_vertices[0], icosahedron_vertices[3]),
                     Edge(icosahedron_vertices[0], icosahedron_vertices[4]),
                     Edge(icosahedron_vertices[0], icosahedron_vertices[5]),
                     Edge(icosahedron_vertices[1], icosahedron_vertices[2]),
                     Edge(icosahedron_vertices[1], icosahedron_vertices[5]),
                     Edge(icosahedron_vertices[1], icosahedron_vertices[6]),
                     Edge(icosahedron_vertices[2], icosahedron_vertices[3]),
                     Edge(icosahedron_vertices[2], icosahedron_vertices[6]),
                     Edge(icosahedron_vertices[2], icosahedron_vertices[7]),
                     Edge(icosahedron_vertices[3], icosahedron_vertices[4]),
                     Edge(icosahedron_vertices[3], icosahedron_vertices[7]),
                     Edge(icosahedron_vertices[3], icosahedron_vertices[8]),
                     Edge(icosahedron_vertices[4], icosahedron_vertices[5]),
                     Edge(icosahedron_vertices[4], icosahedron_vertices[8]),
                     Edge(icosahedron_vertices[4], icosahedron_vertices[9]),
                     Edge(icosahedron_vertices[5], icosahedron_vertices[10]),
                     Edge(icosahedron_vertices[6], icosahedron_vertices[7]),
                     Edge(icosahedron_vertices[6], icosahedron_vertices[10]),
                     Edge(icosahedron_vertices[7], icosahedron_vertices[8]),
                     Edge(icosahedron_vertices[7], icosahedron_vertices[11]),
                     Edge(icosahedron_vertices[8], icosahedron_vertices[9]),
                     Edge(icosahedron_vertices[8], icosahedron_vertices[11]),
                     Edge(icosahedron_vertices[9], icosahedron_vertices[10]),
                     Edge(icosahedron_vertices[9], icosahedron_vertices[11]),
                     Edge(icosahedron_vertices[10], icosahedron_vertices[11]),
                     Edge(icosahedron_vertices[5], icosahedron_vertices[11])]
icosahedron_faces = [Face([icosahedron_vertices[0], icosahedron_vertices[1], icosahedron_vertices[2]]),
                     Face([icosahedron_vertices[0], icosahedron_vertices[2], icosahedron_vertices[3]]),
                     Face([icosahedron_vertices[0], icosahedron_vertices[3], icosahedron_vertices[4]]),
                     Face([icosahedron_vertices[0], icosahedron_vertices[4], icosahedron_vertices[5]]),
                     Face([icosahedron_vertices[0], icosahedron_vertices[5], icosahedron_vertices[1]]),
                     Face([icosahedron_vertices[1], icosahedron_vertices[2], icosahedron_vertices[6]]),
                     Face([icosahedron_vertices[2], icosahedron_vertices[3], icosahedron_vertices[7]]),
                     Face([icosahedron_vertices[3], icosahedron_vertices[4], icosahedron_vertices[8]]),
                     Face([icosahedron_vertices[4], icosahedron_vertices[5], icosahedron_vertices[9]]),
                     Face([icosahedron_vertices[5], icosahedron_vertices[1], icosahedron_vertices[10]]),
                     Face([icosahedron_vertices[6], icosahedron_vertices[7], icosahedron_vertices[11]]),
                     Face([icosahedron_vertices[7], icosahedron_vertices[8], icosahedron_vertices[11]]),
                     Face([icosahedron_vertices[8], icosahedron_vertices[9], icosahedron_vertices[11]]),
                     Face([icosahedron_vertices[9], icosahedron_vertices[10], icosahedron_vertices[11]]),
                     Face([icosahedron_vertices[10], icosahedron_vertices[6], icosahedron_vertices[11]])]
icosahedron_data = FigureData(icosahedron_vertices, icosahedron_edges, icosahedron_faces, color=(0, 1, 1),
                                draw_mode='faces')


# Dictionary containing all figures
figures = {
    "Cube": cube_data,
    "Pyramid": pyramid_data,
    "Sphere": sphere_data,
    "Tetrahedron": tetrahedron_data,
    "Hexahedron": hexahedron_data,
    "Octahedron": octahedron_data,
    "Icosahedron": icosahedron_data
}

# Dictionary containing colors and their RGB values
colors = {
    "Red": [1, 0, 0],
    "Green": [0, 1, 0],
    "Blue": [0, 0, 1],
    "Yellow": [1, 1, 0],
    "Cyan": [0, 1, 1],
    "Magenta": [1, 0, 1],
    "White": [1, 1, 1],
    "Black": [0, 0, 0]
}
