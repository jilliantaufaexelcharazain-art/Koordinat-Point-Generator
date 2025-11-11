# generator.py
import numpy as np

class PointGenerator:
    """
    Class untuk menghasilkan koordinat titik 3D (X, Y, Z)
    dalam mode 'grid' atau 'random'.

    - generate() mengembalikan numpy array shape (N, 3)
    - labels tersedia di self.labels (list of "P1", "P2", ...)
    """

    def __init__(self, xmin=0, xmax=1, ymin=0, ymax=1, zmin=0, zmax=1,
                 num_points=100, mode='random', spacing=1.0):
        # Simpan parameter batas dan mode
        self.xmin = float(xmin)
        self.xmax = float(xmax)
        self.ymin = float(ymin)
        self.ymax = float(ymax)
        self.zmin = float(zmin)
        self.zmax = float(zmax)
        self.num_points = int(num_points)
        self.mode = mode.lower()
        self.spacing = float(spacing)

        # inisialisasi container hasil
        self.points = None      # numpy array (N,3)
        self.labels = None      # list of labels "P1", "P2", ...

    def generate(self):
        """Fungsi utama untuk menghasilkan koordinat berdasarkan mode.
        Mengisi self.points (numpy array) dan self.labels (list) lalu mengembalikan self.points.
        """
        if self.mode == 'grid':
            pts = self._generate_grid()
        elif self.mode == 'random':
            pts = self._generate_random()
        else:
            raise ValueError("Mode tidak dikenal. Gunakan 'grid' atau 'random'.")

        # Simpan hasil ke atribut
        self.points = np.asarray(pts, dtype=float)
        self.labels = [f"P{i+1}" for i in range(self.points.shape[0])]
        return self.points

    def _generate_grid(self):
        """
        Membuat grid 3D penuh berdasarkan rentang dan jarak antar titik (spacing).
        Mengembalikan numpy array shape (N,3).
        """
        # Pastikan spacing positif
        if self.spacing <= 0:
            raise ValueError("spacing harus > 0")

        # Buat vektor nilai X, Y, Z sesuai rentang dan jarak antar titik
        x_vals = np.arange(self.xmin, self.xmax + 1e-9, self.spacing)
        y_vals = np.arange(self.ymin, self.ymax + 1e-9, self.spacing)
        z_vals = np.arange(self.zmin, self.zmax + 1e-9, self.spacing)

        # Jika salah satu axis hanya punya satu nilai dan num_points diminta lebih kecil,
        # tetap hasilkan grid penuh lalu trim sesuai num_points jika perlu.
        X, Y, Z = np.meshgrid(x_vals, y_vals, z_vals, indexing='ij')

        # Flatten menjadi N x 3
        points = np.column_stack((X.ravel(), Y.ravel(), Z.ravel()))

        # Jika user meminta num_points lebih sedikit, ambil subset terdepan
        if (self.num_points is not None) and (self.num_points > 0) and (len(points) > self.num_points):
            points = points[:self.num_points, :]

        return points

    def _generate_random(self):
        """
        Menghasilkan titik acak seragam di dalam batas (xmin..xmax, ymin..ymax, zmin..zmax)
        Mengembalikan numpy array shape (N,3).
        """
        if self.num_points <= 0:
            raise ValueError("num_points harus > 0 untuk mode random")

        x = np.random.uniform(self.xmin, self.xmax, self.num_points)
        y = np.random.uniform(self.ymin, self.ymax, self.num_points)
        z = np.random.uniform(self.zmin, self.zmax, self.num_points)

        points = np.column_stack((x, y, z))
        return points
