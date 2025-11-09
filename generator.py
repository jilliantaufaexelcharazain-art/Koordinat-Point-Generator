# generator.py

import numpy as np

class PointGenerator:
    """
    Class untuk menghasilkan koordinat titik 3D (X, Y, Z)
    dalam mode grid atau random.
    """

    def __init__(self, xmin, xmax, ymin, ymax, zmin, zmax,
                 num_points=100, mode='random', spacing=1.0):
        # Simpan parameter batas dan mode
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax
        self.num_points = num_points
        self.mode = mode.lower()
        self.spacing = spacing

    def generate(self):
        """Fungsi utama untuk menghasilkan koordinat berdasarkan mode."""
        if self.mode == 'grid':
            return self._generate_grid()
        elif self.mode == 'random':
            return self._generate_random()
        else:
            raise ValueError("Mode tidak dikenal. Gunakan 'grid' atau 'random'.")

    def _generate_grid(self):
        """Membuat titik-titik dalam pola grid 3D (teratur)."""
        # Membuat vektor untuk sumbu X, Y, Z berdasarkan jarak antar titik (spacing)
        x = np.arange(self.xmin, self.xmax + self.spacing, self.spacing)
        y = np.arange(self.ymin, self.ymax + self.spacing, self.spacing)
        z = np.arange(self.zmin, self.zmax + self.spacing, self.spacing)

        # Membentuk kombinasi semua titik (meshgrid)
        X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

        # Mengubah hasil meshgrid menjadi daftar titik (N x 3)
        points = np.column_stack((X.ravel(), Y.ravel(), Z.ravel()))

        # Jika total titik lebih banyak dari yang diinginkan, ambil sebagian
        if len(points) > self.num_points:
            points = points[:self.num_points]

        return points

    def _generate_random(self):
        """Membuat titik-titik acak dalam batas X, Y, Z."""
        # Menghasilkan titik acak seragam di dalam batas koordinat
        x = np.random.uniform(self.xmin, self.xmax, self.num_points)
        y = np.random.uniform(self.ymin, self.ymax, self.num_points)
        z = np.random.uniform(self.zmin, self.zmax, self.num_points)

        # Menggabungkan menjadi array (N x 3)
        points = np.column_stack((x, y, z))
        return points
