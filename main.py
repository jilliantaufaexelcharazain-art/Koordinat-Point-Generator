# main.py

from generator import PointGenerator
from visualizer import PointVisualizer
from filemanager import FileManager

def main():
    print("=== Koordinat Point Generator (Versi Terminal) ===")

    # Ambil input dari pengguna
    xmin = float(input("Masukkan Xmin: "))
    xmax = float(input("Masukkan Xmax: "))
    ymin = float(input("Masukkan Ymin: "))
    ymax = float(input("Masukkan Ymax: "))
    zmin = float(input("Masukkan Zmin: "))
    zmax = float(input("Masukkan Zmax: "))

    mode = input("Pilih mode (grid/random): ").strip().lower()
    num_points = int(input("Jumlah titik (untuk mode random): "))
    spacing = float(input("Jarak antar titik (untuk mode grid): "))

    # Buat generator
    gen = PointGenerator(xmin, xmax, ymin, ymax, zmin, zmax,
                         num_points=num_points, spacing=spacing, mode=mode)

    # Generate titik
    points = gen.generate()

    # Simpan ke file CSV
    fm = FileManager(points)
    fm.save_to_csv("output_koordinat.csv")

    # Visualisasi
    vis = PointVisualizer(points)
    vis.show_3d()

    print("\nProses selesai ✅")
    print("File hasil disimpan sebagai: output_koordinat.csv")

if __name__ == "__main__":
    main()
