import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd

from generator import PointGenerator
from visualizer import PointVisualizer
from filemanager import FileManager


class CoordinateGUI:
    """Kelas utama untuk antarmuka pengguna (GUI)."""

    def __init__(self, root):
        # Jendela utama
        self.root = root
        self.root.title("Koordinat Point Generator (Geofisika)")

        # Frame untuk input parameter
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        # Label & input untuk batas koordinat
        tk.Label(input_frame, text="Xmin").grid(row=0, column=0)
        tk.Label(input_frame, text="Xmax").grid(row=0, column=2)
        tk.Label(input_frame, text="Ymin").grid(row=1, column=0)
        tk.Label(input_frame, text="Ymax").grid(row=1, column=2)
        tk.Label(input_frame, text="Zmin").grid(row=2, column=0)
        tk.Label(input_frame, text="Zmax").grid(row=2, column=2)

        # Entry field
        self.xmin = tk.Entry(input_frame, width=8)
        self.xmax = tk.Entry(input_frame, width=8)
        self.ymin = tk.Entry(input_frame, width=8)
        self.ymax = tk.Entry(input_frame, width=8)
        self.zmin = tk.Entry(input_frame, width=8)
        self.zmax = tk.Entry(input_frame, width=8)

        # Posisi grid input
        self.xmin.grid(row=0, column=1, padx=5)
        self.xmax.grid(row=0, column=3, padx=5)
        self.ymin.grid(row=1, column=1, padx=5)
        self.ymax.grid(row=1, column=3, padx=5)
        self.zmin.grid(row=2, column=1, padx=5)
        self.zmax.grid(row=2, column=3, padx=5)

        # Input tambahan
        tk.Label(input_frame, text="Jumlah Titik").grid(row=3, column=0)
        tk.Label(input_frame, text="Spacing").grid(row=3, column=2)

        self.num_points = tk.Entry(input_frame, width=8)
        self.spacing = tk.Entry(input_frame, width=8)
        self.num_points.grid(row=3, column=1)
        self.spacing.grid(row=3, column=3)

        # Pilihan mode
        tk.Label(input_frame, text="Mode").grid(row=4, column=0)
        self.mode_var = tk.StringVar(value='grid')
        ttk.Combobox(
            input_frame,
            textvariable=self.mode_var,
            values=['grid', 'random'],
            width=6
        ).grid(row=4, column=1)

        # Tombol aksi
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Generate", command=self.generate_points).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Plot 3D", command=self.plot_points).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Save CSV", command=self.save_points).grid(row=0, column=2, padx=5)

        # Tabel hasil koordinat (dengan kolom Label)
        self.table = ttk.Treeview(
            self.root,
            columns=("Label", "X", "Y", "Z"),
            show='headings',
            height=10
        )
        for col in ("Label", "X", "Y", "Z"):
            self.table.heading(col, text=col)
            self.table.column(col, width=100, anchor='center')
        self.table.pack(padx=10, pady=10)

        # Variabel penyimpanan titik
        self.points = None   # numpy array (N,3)
        self.labels = None   # list (N,)

    def _normalize_result(self, result, gen):
        """
        Terima hasil dari PointGenerator (bisa ndarray atau pandas DataFrame).
        Kembalikan tuple (points_ndarray, labels_list).
        """
        # Jika pandas DataFrame
        if isinstance(result, pd.DataFrame):
            # Pastikan kolom X,Y,Z ada
            if set(["X", "Y", "Z"]).issubset(result.columns):
                pts = result[["X", "Y", "Z"]].values
            else:
                raise ValueError("DataFrame hasil generator tidak memiliki kolom X,Y,Z")
            # Ambil label jika ada
            if "Label" in result.columns:
                labels = result["Label"].astype(str).tolist()
            else:
                labels = getattr(gen, "labels", [f"P{i+1}" for i in range(len(pts))])
        else:
            # Asumsikan ndarray-like
            pts = np.asarray(result, dtype=float)
            if pts.ndim != 2 or pts.shape[1] != 3:
                raise ValueError("Hasil generator harus array shape (N,3) atau DataFrame dengan kolom X,Y,Z")
            labels = getattr(gen, "labels", [f"P{i+1}" for i in range(pts.shape[0])])
        return pts, labels

    def generate_points(self):
        """Menghasilkan titik koordinat dari input pengguna."""
        try:
            xmin = float(self.xmin.get())
            xmax = float(self.xmax.get())
            ymin = float(self.ymin.get())
            ymax = float(self.ymax.get())
            zmin = float(self.zmin.get())
            zmax = float(self.zmax.get())
            # num_points optional: default jika kosong
            num_points_text = self.num_points.get().strip()
            num_points = int(num_points_text) if num_points_text != "" else 0
            spacing_text = self.spacing.get().strip()
            spacing = float(spacing_text) if spacing_text != "" else 1.0
            mode = self.mode_var.get()

            # Buat objek generator
            gen = PointGenerator(
                xmin, xmax, ymin, ymax, zmin, zmax,
                num_points=num_points if num_points>0 else 0,
                spacing=spacing, mode=mode
            )

            raw = gen.generate()   # bisa ndarray atau DataFrame depending on generator implementation
            pts, labels = self._normalize_result(raw, gen)

            # Simpan hasil
            self.points = pts
            self.labels = labels

            # Hapus tabel lama
            for row in self.table.get_children():
                self.table.delete(row)

            # Masukkan hasil baru ke tabel
            for label, p in zip(self.labels, self.points):
                self.table.insert("", "end", values=(label, round(p[0], 2), round(p[1], 2), round(p[2], 2)))

            messagebox.showinfo("Sukses", "Koordinat berhasil digenerate!")

        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

    def plot_points(self):
        """Menampilkan scatter plot 3D di jendela terpisah."""
        if self.points is None:
            messagebox.showwarning("Peringatan", "Generate titik terlebih dahulu!")
            return
        vis = PointVisualizer(self.points, labels=self.labels)
        vis.show_3d()

    def save_points(self):
        """Menyimpan titik ke file CSV."""
        if self.points is None:
            messagebox.showwarning("Peringatan", "Tidak ada data untuk disimpan!")
            return
        fm = FileManager(self.points, self.labels)
        fm.save_to_csv("koordinat_output.csv")
        messagebox.showinfo("Sukses", "File CSV berhasil disimpan!")


# Jalankan GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = CoordinateGUI(root)
    root.mainloop()
