# Peer-to-Peer (P2P) Communication with Random Walk File Search

Rizqullah Aryaputra Piliang & Ikhwan M. Faried

## Deskripsi Proyek

Proyek ini adalah implementasi dari sistem komunikasi peer-to-peer (P2P) yang mendukung pencarian dan pengunduhan file melalui metode **random walk**. Setiap node dalam jaringan berperan sebagai server dan client, memungkinkan berbagi file dan pencarian secara acak di antara peers (node lain).

### Fitur Utama:

- **Random Walk**: Sistem pencarian file menggunakan metode random walk, di mana setiap permintaan dikirim ke peer yang dipilih secara acak hingga file ditemukan atau semua peer dikunjungi.
- **Multithreading**: Sistem ini menggunakan multithreading, memungkinkan node menangani beberapa permintaan secara bersamaan sebagai server sambil tetap bisa melakukan pencarian file sebagai client.
- **Manajemen File**: Setiap node menyimpan file secara lokal, dan node lain dapat meminta file tersebut.
- **Penyimpanan Unduhan**: File yang berhasil diunduh akan disimpan di direktori terpisah (`downloaded`).

## Struktur Kode

### 1. Konfigurasi Node

```python
NODE_HOST = "192.168.137.1"
NODE_PORT = 8001
peers = [
    (NODE_HOST, NODE_PORT),
    ('192.168.137.92', 8002),
    ('192.168.137.1', 8003),
    ('192.168.137.209', 8004),
]
```

Bagian ini mendefinisikan host dan port untuk node yang sedang berjalan dan daftar peers, yaitu node lain yang tersedia untuk komunikasi dalam jaringan.

### 2. Penyimpanan File

```python
penyimpanan_file = {}
```

File yang terdapat di direktori proyek akan dimuat ke dalam variabel `penyimpanan_file`. Setiap file yang ada dapat diminta oleh node lain.

### 3. Direktori Unduhan

```python
direktori_unduhan = os.path.join(direktori_proyek, 'downloaded')
if not os.path.exists(direktori_unduhan):
    os.makedirs(direktori_unduhan)
```

Kode ini memastikan adanya folder `downloaded` yang digunakan untuk menyimpan file yang diunduh dari node lain.

### 4. Fungsi Server

```python
def tangani_client(conn, addr):
    ...
def server():
    ...
```

Node berfungsi sebagai server yang mendengarkan permintaan file dari peer lain. Jika file yang diminta tersedia, server mengirimkan file tersebut ke client.

### 5. Fungsi Client

```python
def client(nama_file):
    ...
```

Fungsi ini mengirimkan permintaan file ke peer yang dipilih secara acak menggunakan metode random walk. Jika file ditemukan, file akan diunduh dan disimpan ke direktori `downloaded`.

### 6. Random Walk

```python
def pencarian_random_walk(nama_file):
    ...
```

Metode random walk digunakan untuk mencari file secara acak dari daftar peers. Peer dipilih secara acak hingga file ditemukan atau semua peer sudah dikunjungi.

### 7. Menjalankan Server dan Client

```python
if __name__ == "__main__":
    ...
```

Bagian ini menginisialisasi server dalam thread terpisah sehingga node bisa menjalankan fungsinya sebagai server dan client secara bersamaan. Pengguna dapat memasukkan nama file yang ingin dicari, dan sistem akan melakukan pencarian file menggunakan random walk.

## Cara Kerja

1. Node yang aktif mendengarkan permintaan file dari peer lain.
2. Pengguna memasukkan nama file yang ingin dicari, dan sistem akan memilih peer secara acak untuk mencari file tersebut.
3. Jika file ditemukan, file akan diunduh dan disimpan ke direktori `downloaded`.
4. Jika file tidak ditemukan di semua peer, sistem akan menampilkan pesan bahwa file tidak tersedia.

## Cara Menjalankan

1. Pastikan Anda menjalankan program ini di jaringan yang sama untuk semua node. Misalnya adalah sudah dibuat client 1 dan client 2 yang bisa Anda jalankan dalam jaringan yang 1 segmen
2. Jalankan script di terminal:
   ```
   python client_1.py
   ```
3. Masukkan nama file yang ingin dicari ketika diminta. Kemudian file akan disimpan di direktori unduhan

## Dependensi

Proyek ini tidak memerlukan pustaka eksternal selain pustaka standar Python, seperti:

- `socket`: untuk komunikasi jaringan.
- `threading`: untuk menangani koneksi bersamaan.
- `os` dan `time`: untuk operasi file dan pencatatan waktu.
- `random`: untuk implementasi random walk.

## Pengembangan Selanjutnya

Beberapa ide pengembangan di masa depan:

- **Keamanan**: Menambahkan lapisan enkripsi untuk komunikasi antar node.
- **Optimisasi Pencarian**: Implementasi algoritma pencarian yang lebih efisien, seperti DHT (Distributed Hash Table), untuk mempercepat pencarian file.
- **Manajemen Peers**: Mengelola daftar peers secara dinamis, memungkinkan penambahan atau penghapusan peers selama runtime.
