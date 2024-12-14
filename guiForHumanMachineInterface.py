import socket
import json
import tkinter as tk
from tkinter import ttk, messagebox
import threading

# Konfigurasi server
HOST = ''
PORT = 8080

# Variabel kontrol untuk menghentikan pembaruan
stop_update_sensor1 = False
stop_update_sensor2 = False

# Fungsi untuk memperbarui tampilan data sensor
def update_display(sensor1_data, sensor2_data):
    global stop_update_sensor1, stop_update_sensor2

    ax1, ay1 = sensor1_data
    ax2, ay2 = sensor2_data

    if not stop_update_sensor1:
        # Update label dengan data terbaru untuk sensor 1
        label_sensor1_ax.config(text=f"Sumbu X: {ax1:.2f}")
        label_sensor1_ay.config(text=f"Sumbu Y: {ay1:.2f}")

        # Cek kondisi untuk sensor 1
        if 0 <= ax1 <= 0.9 and 0 <= ay1 <= 0.9:
            stop_update_sensor1 = True
            messagebox.showinfo("Facebow", "Tetapkan kesejajaran!")

    if not stop_update_sensor2:
        # Update label dengan data terbaru untuk sensor 2
        label_sensor2_ax.config(text=f"Sumbu X: {ax2:.2f}")
        label_sensor2_ay.config(text=f"Sumbu Y: {ay2:.2f}")

        # Cek kondisi untuk sensor 2
        if 0 <= ax2 <= 0.9 and 0 <= ay2 <= 0.9:
            stop_update_sensor2 = True
            messagebox.showinfo("Foxplane", "Tetapkan kesejajaran!")

# Fungsi untuk memulai server dan menerima data
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Server berjalan di {HOST}:{PORT}")

        while True:
            print("Menunggu koneksi...")
            conn, addr = server_socket.accept()
            with conn:
                print(f"Koneksi diterima dari {addr}")
                buffer = ""
                while True:
                    try:
                        # Menerima data dalam batch
                        data = conn.recv(1024).decode('utf-8')
                        if not data:
                            break
                        
                        # Tambahkan ke buffer
                        buffer += data

                        # Proses jika ada delimiter
                        while '\n' in buffer:
                            line, buffer = buffer.split('\n', 1)
                            print(f"Data diterima: {line}")

                            try:
                                # Parse JSON yang diterima
                                sensor_data = json.loads(line)
                                
                                # Mengambil data dari sensor pertama
                                sensor1 = sensor_data.get("sensor1", {})
                                ax1 = sensor1.get("ax", 0.0)
                                ay1 = sensor1.get("ay", 0.0)

                                # Mengambil data dari sensor kedua
                                sensor2 = sensor_data.get("sensor2", {})
                                ax2 = sensor2.get("ax", 0.0)
                                ay2 = sensor2.get("ay", 0.0)

                                # Update tampilan GUI dengan data terbaru
                                update_display((ax1, ay1), (ax2, ay2))
                            except json.JSONDecodeError:
                                print("Data yang diterima tidak valid JSON")
                    except Exception as e:
                        print(f"Terjadi kesalahan: {e}")
                        break

# Fungsi untuk reset monitoring
def reset_updates():
    global stop_update_sensor1, stop_update_sensor2
    stop_update_sensor1 = False
    stop_update_sensor2 = False
    label_status.config(text="Monitoring aktif kembali.")

# Fungsi untuk membuka menu Kesejajaran
def open_kesejajaran():
    home_frame.pack_forget()
    gui_frame.pack()

# Fungsi untuk kembali ke menu Home
def back_to_home():
    gui_frame.pack_forget()
    home_frame.pack()

# Membuat jendela GUI
root = tk.Tk()
root.title("Aplikasi Monitoring Sensor")
root.geometry("400x400")

# Frame Home
home_frame = ttk.Frame(root)
home_frame.pack()

home_label = tk.Label(home_frame, text="Selamat Datang di Monitoring Sensor", font=("Arial", 14))
home_label.pack(pady=20)

btn_kesejajaran = ttk.Button(home_frame, text="Kesejajaran", command=open_kesejajaran)
btn_kesejajaran.pack(pady=10)

# Frame GUI utama (Kesejajaran)
gui_frame = ttk.Frame(root)

label_title = tk.Label(gui_frame, text="Data Sensor MPU6050", font=("Arial", 16))
label_title.pack(pady=10)

# Frame untuk menampilkan data sensor 1
frame_sensor1 = ttk.Frame(gui_frame)
frame_sensor1.pack(pady=10)

canvas_sensor1 = tk.Canvas(frame_sensor1, width=380, height=80)
canvas_sensor1.pack()
canvas_sensor1.create_rectangle(10, 10, 380, 70, fill='lightblue', outline="")

label_sensor1 = tk.Label(frame_sensor1, text="Facebow", font=("Arial", 12))
label_sensor1.place(x=160, y=10)

label_sensor1_ax = tk.Label(frame_sensor1, text="Sumbu X: 0.00", font=("Arial", 10))
label_sensor1_ax.place(x=50, y=40)

label_sensor1_ay = tk.Label(frame_sensor1, text="Sumbu Y: 0.00", font=("Arial", 10))
label_sensor1_ay.place(x=250, y=40)

# Frame untuk menampilkan data sensor 2
frame_sensor2 = ttk.Frame(gui_frame)
frame_sensor2.pack(pady=10)

canvas_sensor2 = tk.Canvas(frame_sensor2, width=380, height=80)
canvas_sensor2.pack()
canvas_sensor2.create_rectangle(10, 10, 380, 70, fill='lightgreen', outline="")

label_sensor2 = tk.Label(frame_sensor2, text="Foxplane", font=("Arial", 12))
label_sensor2.place(x=160, y=10)

label_sensor2_ax = tk.Label(frame_sensor2, text="Sumbu X: 0.00", font=("Arial", 10))
label_sensor2_ax.place(x=50, y=40)

label_sensor2_ay = tk.Label(frame_sensor2, text="Sumbu Y: 0.00", font=("Arial", 10))
label_sensor2_ay.place(x=250, y=40)

# Tombol Reset dan Kembali
btn_reset = ttk.Button(gui_frame, text="Reset Monitoring", command=reset_updates)
btn_reset.pack(pady=10)

btn_back = ttk.Button(gui_frame, text="Kembali ke Home", command=back_to_home)
btn_back.pack(pady=10)

label_status = tk.Label(gui_frame, text="", font=("Arial", 10), fg="green")
label_status.pack(pady=5)

# Memulai server di thread terpisah
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# Menjalankan GUI
root.mainloop()
