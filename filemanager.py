# filemanager.py

import pandas as pd

class FileManager:
    """
    Class untuk menyimpan data koordinat ke dalam file CSV.
    """

    def __init__(self, points, labels=None):
        """
        Parameters:
        - points: array numpy (N x 3) berisi X, Y, Z
        - labels: list opsional berisi nama titik (P1, P2, dst)
        """
        self.points = points
        self.labels = labels

    def save_to_csv(self, filename="koordinat_output.csv"):
        """Menyimpan data ke file CSV dengan header Label, X, Y, Z."""
        # Membuat DataFrame dari array numpy
        df = pd.DataFrame(self.points, columns=['X', 'Y', 'Z'])

        # Tambahkan label jika tersedia
        if self.labels is not None and len(self.labels) == len(df):
            df.insert(0, 'Label', self.labels)
        else:
            df.insert(0, 'Label', [f'P{i+1}' for i in range(len(df))])

        # Simpan ke file CSV
        df.to_csv(filename, index=False)

        # Konfirmasi sukses
        print(f"✅ File CSV berhasil disimpan: {filename}")
