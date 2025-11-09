# visualizer.py

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # modul tambahan untuk 3D plot

class PointVisualizer:
    """
    Class untuk menampilkan koordinat titik 3D
    dalam jendela plot terpisah.
    """

    def __init__(self, points):
        # Simpan data titik (numpy array dengan kolom X, Y, Z)
        self.points = points

    def show_3d(self):
        """Menampilkan scatter plot 3D di jendela terpisah."""
        # Buat figure baru untuk tampilan 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Ambil kolom X, Y, Z dari array
        x = self.points[:, 0]
        y = self.points[:, 1]
        z = self.points[:, 2]

        # Tampilkan scatter plot
        ax.scatter(x, y, z, c='blue', s=20, alpha=0.8)

        # Label sumbu
        ax.set_xlabel('X (meter)')
        ax.set_ylabel('Y (meter)')
        ax.set_zlabel('Z (meter)')

        # Judul
        ax.set_title('3D Coordinate Scatter Plot')

        # Tampilkan plot di window baru
        plt.show()
