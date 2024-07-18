import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

def create_pyramid(subdivisions, height, base_subdivisions=None, side_visibility=1.0, base_visibility=1.0):
    base_subdivisions = base_subdivisions if base_subdivisions is not None else subdivisions
    
    # Define the vertices of the pyramid
    vertices = np.array([[-1, -1, 0],
                         [1, -1, 0],
                         [1, 1, 0],
                         [-1, 1, 0],
                         [0, 0, height]])

    # Define the faces of the pyramid
    faces = [
        [vertices[0], vertices[1], vertices[4]],
        [vertices[1], vertices[2], vertices[4]],
        [vertices[2], vertices[3], vertices[4]],
        [vertices[3], vertices[0], vertices[4]],
    ]

    def subdivide_triangle(v1, v2, v3, depth):
        if depth == 0:
            return [[v1, v2, v3]]
        
        v12 = (v1 + v2) / 2
        v23 = (v2 + v3) / 2
        v31 = (v3 + v1) / 2
        
        return (subdivide_triangle(v1, v12, v31, depth - 1) +
                subdivide_triangle(v2, v23, v12, depth - 1) +
                subdivide_triangle(v3, v31, v23, depth - 1) +
                subdivide_triangle(v12, v23, v31, depth - 1))

    # Subdivide each triangular face
    subdivided_faces = []
    for face in faces:
        subdivided_faces.extend(subdivide_triangle(face[0], face[1], face[2], subdivisions))
    
    # Create triangulated base
    base_vertices = vertices[:4]
    base_center = np.mean(base_vertices, axis=0)
    base_faces = []
    for i in range(4):
        v1, v2 = base_vertices[i], base_vertices[(i+1)%4]
        base_faces.extend(subdivide_triangle(v1, v2, base_center, base_subdivisions))

    # Create a 3D plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the pyramid sides
    ax.add_collection3d(Poly3DCollection(subdivided_faces, facecolors='cyan', linewidths=0.5, edgecolors='r', alpha=0.25 * side_visibility))

    # Plot the triangulated base
    ax.add_collection3d(Poly3DCollection(base_faces, facecolors='lightgreen', linewidths=0.5, edgecolors='g', alpha=0.25 * base_visibility))

    # Set the limits and labels
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    ax.set_zlim([0, height + 0.5])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Show the plot
    plt.show()

# Example usage
create_pyramid(subdivisions=3, height=2, base_subdivisions=2, side_visibility=0.8, base_visibility=1.0)
