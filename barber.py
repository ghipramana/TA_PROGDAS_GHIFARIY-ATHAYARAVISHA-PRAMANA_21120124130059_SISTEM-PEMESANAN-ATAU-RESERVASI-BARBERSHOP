import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from collections import deque
import re

class BarberShopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Barber Shop")

        # Daftar waktu per capster
        self.times_by_capster = {
            "Pilbert": ["09:00", "10:00", "11:00", "13:00", "14:00", "15:00"],
            "Gedong": ["09:00", "10:00", "11:00", "13:00", "14:00", "15:00"]
        }
        self.available_capster = ["Pilbert", "Gedong"]

        # Variabel untuk input
        self.customer_name = tk.StringVar()
        self.customer_phone = tk.StringVar()
        self.selected_time = tk.StringVar()
        self.capster_request = tk.StringVar()

        # Gambar logo barbershop
        self.image_path = "White Circular Barbershop Logo.png"
        self.image = ImageTk.PhotoImage(Image.open(self.image_path))
        self.label_image = tk.Label(root, image=self.image)
        self.label_image.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

        # Form input
        self.label_name = tk.Label(root, text="Nama:")
        self.label_name.config(font=("Courier New", 12), fg="black")
        self.label_name.grid(row=1, column=0, sticky=tk.W)
        self.entry_name = tk.Entry(root, textvariable=self.customer_name, width=30)
        self.entry_name.config(font=("Courier New", 12), fg="black", bg="white")
        self.entry_name.grid(row=1, column=1, columnspan=2)

        self.label_phone = tk.Label(root, text="No HP:")
        self.label_phone.config(font=("Courier New", 12), fg="black")
        self.label_phone.grid(row=2, column=0, sticky=tk.W)
        self.entry_phone = tk.Entry(root, textvariable=self.customer_phone, width=30)
        self.entry_phone.config(font=("Courier New", 12), fg="black", bg="white")
        self.entry_phone.grid(row=2, column=1, columnspan=2)

        self.label_capster = tk.Label(root, text="Capster yang diinginkan:")
        self.label_capster.config(font=("Courier New", 12), fg="black")
        self.label_capster.grid(row=3, column=0, sticky=tk.W)
        self.dropdown_capster = tk.OptionMenu(root, self.capster_request, *self.available_capster, command=self.update_time_dropdown)
        self.dropdown_capster.config(font=("Courier New", 12), fg="black", bg="white")
        self.dropdown_capster.grid(row=3, column=1, columnspan=2)

        self.label_time = tk.Label(root, text="Waktu:")
        self.label_time.config(font=("Courier New", 12), fg="black")
        self.label_time.grid(row=4, column=0, sticky=tk.W)
        self.dropdown_time = tk.OptionMenu(root, self.selected_time, "")
        self.dropdown_time.config(font=("Courier New", 12), fg="black", bg="white")
        self.dropdown_time.grid(row=4, column=1, columnspan=2)

        self.reserve_button = tk.Button(root, text="Reservasi", command=self.make_reservation)
        self.reserve_button.config(font=("Courier New", 14), bg="green", fg="white")
        self.reserve_button.grid(row=5, column=0, columnspan=3, pady=10)

        # Stack untuk Pilbert, Queue untuk Gedong
        self.reservation_stack = deque()  # Stack untuk Pilbert
        self.reservation_queue = deque()  # Queue untuk Gedong

    def make_reservation(self):
        customer_name = self.customer_name.get()
        customer_phone = self.customer_phone.get()
        selected_time = self.selected_time.get()
        capster_request = self.capster_request.get()

        # Validasi input
        if customer_name == "" or not re.match('^[a-zA-Z\s]+$', customer_name):
            messagebox.showerror("Error", "Nama pelanggan harus diisi dan hanya boleh berisi huruf.")
            return
        if customer_phone == "" or not customer_phone.isdigit():
            messagebox.showerror("Error", "Nomor telepon harus diisi dan berupa angka.")
            return
        if selected_time == "":
            messagebox.showerror("Error", "Mohon pilih waktu reservasi.")
            return
        if capster_request == "":
            messagebox.showerror("Error", "Mohon pilih capster yang tersedia.")
            return

        # Simpan reservasi
        reservation = {
            "Nama": customer_name,
            "No HP": customer_phone,
            "Waktu": selected_time,
            "Capster yang diinginkan": capster_request
        }

        if capster_request == "Pilbert":
            self.reservation_stack.append(reservation)
        elif capster_request == "Gedong":
            self.reservation_queue.append(reservation)

        # Hapus waktu dari capster yang dipilih
        if selected_time in self.times_by_capster[capster_request]:
            self.times_by_capster[capster_request].remove(selected_time)
        self.update_time_dropdown(capster_request)

        messagebox.showinfo("Reservasi Barbershop", f"Reservasi berhasil! Capster: {capster_request}")
        self.show_reservation_info(reservation)
        self.reset_input()

        # Tanya apakah ingin reservasi lagi
        reserve_again = messagebox.askyesno("Reservasi Lagi?", "Apakah Anda ingin melakukan reservasi lagi?")
        if not reserve_again:
            self.root.quit()

    def update_time_dropdown(self, capster_request=None):
        """Perbarui dropdown waktu berdasarkan capster"""
        if not capster_request:
            capster_request = self.capster_request.get()

        menu = self.dropdown_time["menu"]
        menu.delete(0, "end")
        for time in self.times_by_capster.get(capster_request, []):
            menu.add_command(label=time, command=lambda value=time: self.selected_time.set(value))

    def show_reservation_info(self, reservation):
        """Tampilkan informasi reservasi"""
        info_text = f"Informasi Reservasi:\n" \
                    f"Nama: {reservation['Nama']}\n" \
                    f"No HP: {reservation['No HP']}\n" \
                    f"Waktu: {reservation['Waktu']}\n" \
                    f"Capster yang diinginkan: {reservation['Capster yang diinginkan']}"
        messagebox.showinfo("Informasi Reservasi", info_text)

    def reset_input(self):
        """Reset input form"""
        self.customer_name.set("")
        self.customer_phone.set("")
        self.selected_time.set("")
        self.capster_request.set("")

root = tk.Tk()
app = BarberShopApp(root)
root.mainloop()