import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # memastikan mode 3D aktif
import pandas as pd

class PointVisualizer:
    """Menampilkan plot 3D dari kumpulan koordinat."""

    def __init__(self, points, labels=None):
        """
        points: numpy array (N,3) atau pandas DataFrame dengan kolom X,Y,Z
        labels: optional list of strings
        """
        # Normalisasi points menjadi numpy array Nx3
        if isinstance(points, pd.DataFrame):
            if set(["X","Y","Z"]).issubset(points.columns):
                self.points = points[["X","Y","Z"]].values
            else:
                raise ValueError("DataFrame harus memiliki kolom X,Y,Z")
        else:
            self.points = np.asarray(points, dtype=float)

        if self.points.ndim != 2 or self.points.shape[1] != 3:
            raise ValueError("points harus array shape (N,3) atau DataFrame dengan kolom X,Y,Z")

        self.labels = labels if labels is not None else [f"P{i+1}" for i in range(self.points.shape[0])]

    def show_3d(self):
        """Menampilkan scatter plot 3D dengan label per titik."""
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Pisahkan komponen koordinat
        xs, ys, zs = self.points[:, 0], self.points[:, 1], self.points[:, 2]

        # Plot titik
        ax.scatter(xs, ys, zs, c='royalblue', s=30, depthshade=True)

        # Tambahkan label nama titik (P1, P2, P3, ...)
        for i, (x, y, z) in enumerate(zip(xs, ys, zs), start=1):
            lbl = self.labels[i-1] if i-1 < len(self.labels) else f"P{i}"
            ax.text(x, y, z, lbl, fontsize=8, color='darkred')

        # Label sumbu
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        ax.set_title("Scatter Plot 3D - Koordinat Titik")
        plt.tight_layout()
        plt.show()
