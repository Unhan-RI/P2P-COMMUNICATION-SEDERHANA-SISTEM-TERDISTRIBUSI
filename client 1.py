import socket
import threading
import os
import time
import random

# Konfigurasi node 
NODE_HOST = "192.168.137.1"
NODE_PORT = 8001

# Daftar peer (node lain dalam jaringan)
peers = [
    (NODE_HOST, NODE_PORT),
    ('192.168.137.92', 8002),
    ('192.168.137.1', 8003),
    ('192.168.137.209', 8004),
]

# File yang disimpan oleh node ini
penyimpanan_file = {}

# Mengisi penyimpanan_file dengan file yang ada di direktori proyek
direktori_proyek = os.path.dirname(os.path.abspath(__file__))
for nama_file in os.listdir(direktori_proyek):
    if os.path.isfile(os.path.join(direktori_proyek, nama_file)):
        with open(os.path.join(direktori_proyek, nama_file), 'r') as file:
            penyimpanan_file[nama_file] = file.read()

# Membuat folder 'downloaded' jika belum ada
direktori_unduhan = os.path.join(direktori_proyek, 'downloaded')
if not os.path.exists(direktori_unduhan):
    os.makedirs(direktori_unduhan)

# Fungsi untuk menangani client
def tangani_client(conn, addr):
    print(f"Terhubung dengan {addr}")
    data = conn.recv(1024).decode()
    if data.startswith("REQUEST"):
        _, nama_file = data.split(":")
        if nama_file in penyimpanan_file:
            conn.send(f"FOUND:{nama_file}:{penyimpanan_file[nama_file]}".encode())
        else:
            conn.send(f"NOT_FOUND:{nama_file}".encode())
    conn.close()

# Fungsi server untuk mendengarkan permintaan
def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((NODE_HOST, NODE_PORT))
    server_socket.listen(5)
    print(f"Server mendengarkan di {NODE_HOST}:{NODE_PORT}")
    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=tangani_client, args=(conn, addr))
        client_thread.start()

# Fungsi client untuk mengirim permintaan dan mendownload file jika ditemukan
def client(nama_file):
    visited_peers = set()
    while len(visited_peers) < len(peers):
        peer = random.choice(peers)
        if peer in visited_peers:
            continue
        visited_peers.add(peer)
        peer_host, peer_port = peer
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            start_time = time.time()
            peer_socket.connect((peer_host, peer_port))
            peer_socket.send(f"REQUEST:{nama_file}".encode())
            response = peer_socket.recv(1024).decode()
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.startswith("FOUND"):
                _, nama_file, isi_file = response.split(":", 2)
                print(f"File ditemukan di {peer_host}:{peer_port}: {nama_file}")
                
                # Menyimpan file ke folder 'downloaded'
                with open(os.path.join(direktori_unduhan, nama_file), 'w') as file:
                    file.write(isi_file)
                
                print(f"File {nama_file} diunduh dan disimpan ke {direktori_unduhan}")
                print(f"Waktu respons: {response_time:.4f} detik")
                peer_socket.close()
                return
            else:
                print(f"File tidak ditemukan di {peer_host}:{peer_port}")
                print(f"Waktu respons: {response_time:.4f} detik")
            peer_socket.close()
        except ConnectionRefusedError:
            print(f"Tidak dapat terhubung ke {peer_host}:{peer_port}")
            continue
    print("File tidak ditemukan di semua peer.")

# Random walk untuk pencarian dan pengunduhan file
def pencarian_random_walk(nama_file):
    client(nama_file)

# Menjalankan server dan client bersamaan
if __name__ == "__main__":
    server_thread = threading.Thread(target=server)
    server_thread.start()

    while True:
        user_input = input("Masukkan nama file yang ingin dicari: ")
        pencarian_random_walk(user_input)
