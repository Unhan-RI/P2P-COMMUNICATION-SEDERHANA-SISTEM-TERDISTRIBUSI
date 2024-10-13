import socket
import threading
import os
import time
import random

# Konfigurasi node dasar
NODE_HOST = "192.168.137.1"  # Ubah IP ini sesuai kebutuhan
NODE_PORT = 8001  # Port server

# Fungsi untuk membuat daftar peer secara dinamis
def generate_peers(total_nodes, base_host, base_port):
    peers = []
    for i in range(total_nodes):
        peers.append((base_host, base_port + i))
    return peers

# Inisialisasi peer (node lain dalam jaringan) secara dinamis berdasarkan input jumlah node
peers = []

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
def server(node_host, node_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((node_host, node_port))
    server_socket.listen(5)
    print(f"Server mendengarkan di {node_host}:{node_port}")
    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=tangani_client, args=(conn, addr))
        client_thread.start()

# Fungsi client untuk mengirim permintaan dan mengukur waktu respon serta throughput
def client(nama_file, peer):
    visited_peers = set()
    total_data_received = 0
    start_time_overall = time.time()
    
    while len(visited_peers) < len(peers):
        peer_host, peer_port = peer
        if peer in visited_peers:
            continue
        visited_peers.add(peer)
        
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
                total_data_received += len(isi_file.encode())
                
                # Menyimpan file ke folder 'downloaded'
                with open(os.path.join(direktori_unduhan, nama_file), 'w') as file:
                    file.write(isi_file)
                
                print(f"File ditemukan di {peer_host}:{peer_port}: {nama_file}")
                print(f"File {nama_file} diunduh dan disimpan ke {direktori_unduhan}")
                print(f"Waktu respons: {response_time:.4f} detik")
                peer_socket.close()
                break
            else:
                print(f"File tidak ditemukan di {peer_host}:{peer_port}")
                print(f"Waktu respons: {response_time:.4f} detik")
            peer_socket.close()
        except ConnectionRefusedError:
            print(f"Tidak dapat terhubung ke {peer_host}:{peer_port}")
            continue
    
    end_time_overall = time.time()
    total_time = end_time_overall - start_time_overall
    throughput = total_data_received / total_time if total_time > 0 else 0
    
    print(f"Total waktu keseluruhan: {total_time:.4f} detik")
    print(f"Throughput: {throughput:.4f} bytes/detik")

# Random walk untuk pencarian dan pengunduhan file
def pencarian_random_walk(nama_file):
    peer = random.choice(peers)
    client(nama_file, peer)

# Fungsi untuk menjalankan server secara paralel
def run_server_parallel(total_nodes):
    for i in range(total_nodes):
        node_host, node_port = peers[i]
        threading.Thread(target=server, args=(node_host, node_port)).start()

# Fungsi untuk menjalankan pengujian dengan jumlah node yang dinamis
def run_test(nama_file, jumlah_node):
    print(f"\n\nMenjalankan pengujian dengan {jumlah_node} node...")
    # Mengenerate peers secara dinamis
    global peers
    peers = generate_peers(jumlah_node, NODE_HOST, NODE_PORT)
    
    # Menjalankan server di setiap node
    run_server_parallel(jumlah_node)
    
    # Menjalankan client untuk mencari file
    pencarian_random_walk(nama_file)

# Menjalankan server dan client bersamaan
if __name__ == "__main__":
    while True:
        user_input_file = input("Masukkan nama file yang ingin dicari: ")
        user_input_nodes = int(input("Masukkan jumlah node yang ingin diuji: "))
        run_test(user_input_file, user_input_nodes)
