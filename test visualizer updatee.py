
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PointApp:
    def __init__(self, master):
        self.master = master
        master.title("Point Generator (2D)")
        master.geometry("950x650")

        # Data internal: list of tuples (nama, x, y)
        self.points = []

        # Untuk operasi edit/update
        self.edit_index = None
        self.editing_item_id = None

        # Menyimpan figure yang sedang ditampilkan (jika ada)
        self.current_fig = None
        self.canvas_plot = None

        # -----------------------
        # FRAME INPUT & BUTTONS
        # -----------------------
        frame_input = tk.Frame(master)
        frame_input.pack(padx=10, pady=10, anchor="w")

        tk.Label(frame_input, text="Nama:").grid(row=0, column=0, sticky="w")
        tk.Label(frame_input, text="X:").grid(row=0, column=2, sticky="w")
        tk.Label(frame_input, text="Y:").grid(row=0, column=4, sticky="w")

        self.entry_nama = tk.Entry(frame_input, width=12)
        self.entry_x = tk.Entry(frame_input, width=12)
        self.entry_y = tk.Entry(frame_input, width=12)

        self.entry_nama.grid(row=0, column=1, padx=(4, 12))
        self.entry_x.grid(row=0, column=3, padx=(4, 12))
        self.entry_y.grid(row=0, column=5, padx=(4, 12))

        # Tombol-tombol fungsi
        self.btn_add = tk.Button(frame_input, text="Tambah Titik", width=12, command=self.add_point)
        self.btn_edit = tk.Button(frame_input, text="Edit Titik", width=12, command=self.edit_point)
        self.btn_update = tk.Button(frame_input, text="Update Titik", width=12, command=self.update_point, state="disabled")
        self.btn_delete = tk.Button(frame_input, text="Hapus Titik", width=12, command=self.delete_point)
        self.btn_plot = tk.Button(frame_input, text="Tampilkan Grafik", width=14, command=self.plot_points)
        self.btn_save_data = tk.Button(frame_input, text="Save Data", width=10, command=self.save_points)
        self.btn_save_plot = tk.Button(frame_input, text="Save Grafik", width=12, command=self.save_plot)

        # Letakkan tombol
        self.btn_add.grid(row=0, column=6, padx=6)
        self.btn_edit.grid(row=0, column=7, padx=6)
        self.btn_update.grid(row=0, column=8, padx=6)
        self.btn_delete.grid(row=0, column=9, padx=6)
        self.btn_plot.grid(row=0, column=10, padx=6)
        self.btn_save_data.grid(row=0, column=11, padx=6)
        self.btn_save_plot.grid(row=0, column=12, padx=6)

        # -----------------------
        # FRAME TABEL (TREEVIEW)
        # -----------------------
        frame_table = tk.Frame(master)
        frame_table.pack(padx=10, pady=(0, 10), fill="both", expand=False)

        columns = ("nama", "x", "y")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=12)
        self.tree.heading("nama", text="Nama")
        self.tree.heading("x", text="X")
        self.tree.heading("y", text="Y")
        self.tree.column("nama", width=150, anchor="center")
        self.tree.column("x", width=120, anchor="center")
        self.tree.column("y", width=120, anchor="center")

        vsb = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(frame_table, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        frame_table.grid_rowconfigure(0, weight=1)
        frame_table.grid_columnconfigure(0, weight=1)

        # Kaitan double-click untuk edit cepat
        self.tree.bind("<Double-1>", self.on_tree_double_click)

        # -----------------------
        # FRAME PLOT
        # -----------------------
        self.frame_plot = tk.Frame(master)
        self.frame_plot.pack(padx=10, pady=10, fill="both", expand=True)

        # Label placeholder untuk area grafik
        self.plot_placeholder = tk.Label(self.frame_plot, text="Tekan 'Tampilkan Grafik' untuk melihat plot.", anchor="center")
        self.plot_placeholder.pack(expand=True, fill="both")

    # -----------------------
    # Fungsi Tambah Titik
    # -----------------------
    def add_point(self):
        nama = self.entry_nama.get().strip()
        x_str = self.entry_x.get().strip()
        y_str = self.entry_y.get().strip()

        if nama == "" or x_str == "" or y_str == "":
            messagebox.showerror("Error", "Semua input (Nama, X, Y) harus diisi.")
            return

        try:
            x = float(x_str)
            y = float(y_str)
        except ValueError:
            messagebox.showerror("Error", "X dan Y harus berupa angka.")
            return

        # Tambah ke data internal
        self.points.append((nama, x, y))

        # Tambah ke treeview
        self.tree.insert("", "end", values=(nama, x, y))

        # Bersihkan entry
        self.clear_entries()

    # -----------------------
    # Fungsi Edit Titik (mengisi inputs)
    # -----------------------
    def edit_point(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Pilih satu baris di tabel untuk diedit.")
            return

        values = self.tree.item(selected, "values")
        if not values:
            messagebox.showerror("Error", "Baris yang dipilih tidak valid.")
            return

        # Simpan indeks dan item id agar update bisa dilakukan
        self.edit_index = self.tree.index(selected)
        self.editing_item_id = selected

        # Isi entries
        self.entry_nama.delete(0, tk.END)
        self.entry_x.delete(0, tk.END)
        self.entry_y.delete(0, tk.END)

        self.entry_nama.insert(0, values[0])
        self.entry_x.insert(0, values[1])
        self.entry_y.insert(0, values[2])

        # Aktifkan tombol Update
        self.btn_update.config(state="normal")

    # -----------------------
    # Fungsi Update Titik
    # -----------------------
    def update_point(self):
        if self.edit_index is None or self.editing_item_id is None:
            messagebox.showerror("Error", "Tidak ada titik yang sedang diedit.")
            return

        nama = self.entry_nama.get().strip()
        x_str = self.entry_x.get().strip()
        y_str = self.entry_y.get().strip()

        if nama == "" or x_str == "" or y_str == "":
            messagebox.showerror("Error", "Semua input (Nama, X, Y) harus diisi.")
            return

        try:
            x = float(x_str)
            y = float(y_str)
        except ValueError:
            messagebox.showerror("Error", "X dan Y harus berupa angka.")
            return

        # Update data internal
        self.points[self.edit_index] = (nama, x, y)

        # Refresh treeview (lebih sederhana untuk re-render)
        self.refresh_treeview()

        # Bersihkan entry & reset edit state
        self.clear_entries()
        self.edit_index = None
        self.editing_item_id = None
        self.btn_update.config(state="disabled")

    # -----------------------
    # Fungsi Hapus Titik
    # -----------------------
    def delete_point(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Pilih titik yang ingin dihapus.")
            return

        idx = self.tree.index(selected)

        # Hapus dari internal list
        try:
            del self.points[idx]
        except IndexError:
            pass

        # Hapus dari treeview
        self.tree.delete(selected)

        # Jika sedang mengedit baris yang sama, batalkan edit
        if self.editing_item_id == selected:
            self.edit_index = None
            self.editing_item_id = None
            self.clear_entries()
            self.btn_update.config(state="disabled")

    # -----------------------
    # Fungsi menampilkan plot
    # -----------------------
    def plot_points(self):
        if len(self.points) == 0:
            messagebox.showerror("Error", "Belum ada titik untuk ditampilkan.")
            return

        # Hapus placeholder atau canvas lama
        if self.canvas_plot:
            self.canvas_plot.get_tk_widget().destroy()
            self.canvas_plot = None
        else:
            self.plot_placeholder.destroy()

        # Ambil data
        x_vals = [p[1] for p in self.points]
        y_vals = [p[2] for p in self.points]

        # Buat figure untuk ditampilkan
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.scatter(x_vals, y_vals, s=40)

        # Tambahkan label (nama) di tiap titik
        for nama, x, y in self.points:
            ax.text(x, y, f" {nama}", fontsize=9, va="bottom", ha="left")

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("Plot Titik Koordinat 2D")
        ax.grid(True)
        ax.axis('equal')  # agar skala X dan Y lebih seragam

        # Tampilkan di tkinter
        self.current_fig = fig
        self.canvas_plot = FigureCanvasTkAgg(fig, master=self.frame_plot)
        self.canvas_plot.draw()
        self.canvas_plot.get_tk_widget().pack(fill="both", expand=True)

    # -----------------------
    # Fungsi Save Data (txt/csv)
    # -----------------------
    def save_points(self):
        if len(self.points) == 0:
            messagebox.showerror("Error", "Tidak ada data untuk disimpan.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV File", "*.csv"), ("Text File", "*.txt")]
        )

        if not file_path:
            return

        try:
            if file_path.endswith(".csv"):
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("Nama,X,Y\n")
                    for p in self.points:
                        f.write(f"{p[0]},{p[1]},{p[2]}\n")
            else:
                # txt
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("Nama\tX\tY\n")
                    for p in self.points:
                        f.write(f"{p[0]}\t{p[1]}\t{p[2]}\n")
            messagebox.showinfo("Sukses", f"Data berhasil disimpan ke {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan data: {e}")

    # -----------------------
    # Fungsi Save Plot (png/jpg/pdf)
    # -----------------------
    def save_plot(self):
        if len(self.points) == 0:
            messagebox.showerror("Error", "Belum ada grafik untuk disimpan.")
            return

        # Jika ada figure aktif di GUI, simpan itu; kalau tidak, buat figure baru untuk disimpan
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("PDF File", "*.pdf")]
        )

        if not file_path:
            return

        try:
            # Buat figure baru agar tidak terpengaruh oleh canvas yang sedang di-embed
            x_vals = [p[1] for p in self.points]
            y_vals = [p[2] for p in self.points]

            fig, ax = plt.subplots(figsize=(6, 5))
            ax.scatter(x_vals, y_vals, s=40)
            for nama, x, y in self.points:
                ax.text(x, y, f" {nama}", fontsize=9, va="bottom", ha="left")
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_title("Plot Titik Koordinat 2D")
            ax.grid(True)
            ax.axis('equal')

            fig.savefig(file_path, bbox_inches="tight")
            plt.close(fig)
            messagebox.showinfo("Sukses", f"Grafik berhasil disimpan ke {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan grafik: {e}")

    # -----------------------
    # Utility: refresh treeview dari self.points
    # -----------------------
    def refresh_treeview(self):
        # Hapus semua
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Insert ulang
        for p in self.points:
            self.tree.insert("", "end", values=p)

    # -----------------------
    # Utility: clear entries
    # -----------------------
    def clear_entries(self):
        self.entry_nama.delete(0, tk.END)
        self.entry_x.delete(0, tk.END)
        self.entry_y.delete(0, tk.END)

    # -----------------------
    # Double click di tabel -> cepat edit
    # -----------------------
    def on_tree_double_click(self, event):
        # panggil edit_point saat double click pada baris
        self.edit_point()


if __name__ == "__main__":
    root = tk.Tk()
    app = PointApp(root)
    root.mainloop()
