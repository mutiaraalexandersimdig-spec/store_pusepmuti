# =========================================
# IMPORT LIBRARY
# =========================================

from dataclasses import dataclass
import json


# =========================================
# RECORD / DATA CLASS PRODUK
# =========================================

@dataclass
class Produk:
    id_produk: str
    nama: str
    harga: int
    stok: int
    kategori: str


# =========================================
# CLASS TOKO
# =========================================

class Toko:

    # =====================================
    # CONSTRUCTOR
    # =====================================

    def __init__(self):

        # Array/List untuk menyimpan produk
        self.daftar_produk = []

        # Nomor ID otomatis
        self.nomor_id = 1


    # =====================================
    # GENERATE ID PRODUK
    # =====================================

    def generate_id(self):

        kode = f"B{self.nomor_id:03}"

        self.nomor_id += 1

        return kode


    # =====================================
    # TAMBAH PRODUK
    # =====================================

    def tambah_produk(self):

        print("\n=== TAMBAH PRODUK ===")

        nama = input("Nama Produk : ")

        harga = int(input("Harga       : "))

        stok = int(input("Stok        : "))

        kategori = input("Kategori    : ")

        id_produk = self.generate_id()

        produk_baru = Produk(
            id_produk,
            nama,
            harga,
            stok,
            kategori
        )

        self.daftar_produk.append(produk_baru)

        print("\nProduk berhasil ditambahkan 💖")
        print("ID Produk :", id_produk)


    # =====================================
    # TAMPILKAN PRODUK
    # =====================================

    def tampilkan_produk(self):

        print("\n=== DAFTAR PRODUK ===")

        if len(self.daftar_produk) == 0:

            print("Belum ada produk 😭")
            return

        print("-" * 70)

        print(
            f"{'ID':10}"
            f"{'Nama':15}"
            f"{'Harga':12}"
            f"{'Stok':10}"
            f"{'Kategori'}"
        )

        print("-" * 70)

        for produk in self.daftar_produk:

            print(
                f"{produk.id_produk:10}"
                f"{produk.nama:15}"
                f"{produk.harga:12}"
                f"{produk.stok:10}"
                f"{produk.kategori}"
            )


    # =====================================
    # CARI PRODUK
    # =====================================

    def cari_produk(self):

        print("\n=== CARI PRODUK ===")

        keyword = input("Masukkan nama produk : ").lower()

        ditemukan = False

        for produk in self.daftar_produk:

            if keyword in produk.nama.lower():

                print("\nProduk ditemukan 💖")

                print("ID       :", produk.id_produk)
                print("Nama     :", produk.nama)
                print("Harga    :", produk.harga)
                print("Stok     :", produk.stok)
                print("Kategori :", produk.kategori)

                ditemukan = True

        if ditemukan == False:

            print("Produk tidak ditemukan 😭")

    # =====================================
    # JUAL PRODUK
    # =====================================

    def jual_produk(self):

        print("\n=== PENJUALAN ===")

        id_produk = input("Masukkan ID Produk : ")

        jumlah_beli = int(input("Jumlah beli : "))

        for produk in self.daftar_produk:

            if produk.id_produk == id_produk:

                # ==========================
                # CEK STOK
                # ==========================

                if jumlah_beli > produk.stok:

                    print("Stok tidak mencukupi 😭")

                    return

                # ==========================
                # HITUNG TOTAL
                # ==========================

                total = produk.harga * jumlah_beli

                # ==========================
                # GARANSI BERDASARKAN HARGA
                # ==========================

                if produk.harga >= 1000000:

                    garansi = "1 Tahun"

                else:

                    garansi = "6 Bulan"

                # ==========================
                # CASHBACK
                # ==========================

                cashback = 0

                if total >= 100000:

                    cashback = 500000

                    total -= cashback

                # ==========================
                # METODE PEMBAYARAN
                # ==========================

                print("\nMetode Pembayaran")

                print("1. Cash")
                print("2. Debit")
                print("3. Kredit")

                pilihan_bayar = input("Pilih : ")

                if pilihan_bayar == "1":

                    metode = "Cash"

                elif pilihan_bayar == "2":

                    metode = "Debit"

                elif pilihan_bayar == "3":

                    metode = "Kredit"

                else:

                    metode = "Tidak Diketahui"

                # ==========================
                # KURANGI STOK
                # ==========================

                produk.stok -= jumlah_beli

                # ==========================
                # CETAK STRUK
                # ==========================

                print("\n")
                print("🌸 ========================== 🌸")
                print("        STORE PUSEPMUTI")
                print("🌸 ========================== 🌸")

                print(f"🧾 Produk      : {produk.nama}")
                print(f"💸 Harga       : Rp{produk.harga}")
                print(f"🛒 Jumlah      : {jumlah_beli}")
                print(f"💳 Pembayaran  : {metode}")
                print(f"🛡️ Garansi      : {garansi}")
                print(f"🎁 Cashback    : Rp{cashback}")
                print(f"💰 Total Bayar : Rp{total}")

                print("--------------------------------")

                print(f"📦 Sisa stok   : {produk.stok}")

                print("\n✨ Terima kasih sudah belanja ✨")
                print("💖 Semoga harimu menyenangkan 💖")

                print("🌸 ========================== 🌸")

                return

        print("Produk tidak ditemukan 😭")


    # =====================================
    # UPDATE STOK
    # =====================================

    def update_stok(self):

        print("\n=== UPDATE STOK ===")

        id_produk = input("Masukkan ID Produk : ")

        jumlah = int(input("Tambah stok : "))

        for produk in self.daftar_produk:

            if produk.id_produk == id_produk:

                produk.stok += jumlah

                print("\nStok berhasil diupdate 💖")
                print("Stok sekarang :", produk.stok)

                return

        print("Produk tidak ditemukan 😭")

    # =====================================
    # SIMPAN DATA JSON
    # =====================================

    def simpan_data(self):

        data = []

        for produk in self.daftar_produk:

            data.append({
                "id_produk": produk.id_produk,
                "nama": produk.nama,
                "harga": produk.harga,
                "stok": produk.stok,
                "kategori": produk.kategori
            })

        with open("data_produk.json", "w") as file:

            json.dump(data, file, indent=4)

        print("\nData berhasil disimpan 💖")


# =========================================
# LOGIN ADMIN
# =========================================

def login():

    print("=" * 55)
    print("             ✨ STORE PUSEPMUTI ✨")
    print("           Selamat Datang Admin")
    print("=" * 55)

    password_benar = "Store01"

    while True:

        password = input("Masukkan Password : ")

        if password == password_benar:

            print("\nLogin berhasil 💖")
            print("Selamat bekerja admin 🌸")

            break

        else:

            print("Password salah 😭")


# =========================================
# MENU UTAMA
# =========================================

def menu():

    login()

    toko = Toko()

    while True:

        print("\n")
        print("=" * 55)
        print("              🛍️ STORE PUSEPMUTI 🛍️")
        print("=" * 55)

        print("1. Tambah Produk")
        print("2. Tampilkan Produk")
        print("3. Cari Produk")
        print("4. Jual Produk")
        print("5. Update Stok")
        print("6. Simpan Data")
        print("0. Close Shift")

        pilihan = input("\nPilih menu : ")

        if pilihan == "1":

            toko.tambah_produk()

        elif pilihan == "2":

            toko.tampilkan_produk()

        elif pilihan == "3":

            toko.cari_produk()

        elif pilihan == "4":

            toko.jual_produk()

        elif pilihan == "5":

            toko.update_stok()

        elif pilihan == "6":

            toko.simpan_data()

        elif pilihan == "0":

            print("\n🌸 Apakah Anda yakin ingin close shift? 🌸")

            print("1. Close Shift Pusep")
            print("2. Close Shift Muti")
            print("0. Tidak Jadi")

            close_shift = input("\nPilih : ")

            if close_shift == "1":

                print("\n✨ Shift Pusep berhasil ditutup ✨")
                print("💖 Terima kasih sudah menjaga toko hari ini 💖")
                print("🌷 Jangan lupa istirahat yaa 🌷")

                break

            elif close_shift == "2":

                print("\n✨ Shift Muti berhasil ditutup ✨")
                print("💖 Kerja bagus hari ini 💖")
                print("🌸 Sampai jumpa di shift berikutnya 🌸")

                break

            elif close_shift == "0":

                print("\nClose shift dibatalkan 🌷")

            else:

                print("Pilihan tidak tersedia 😭")

        else:

            print("Menu tidak tersedia 😭")


# =========================================
# PROGRAM UTAMA
# =========================================

menu()