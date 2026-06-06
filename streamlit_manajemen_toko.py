import json
from pathlib import Path
import streamlit as st
import pandas as pd

APP_TITLE = "Store Pusepmuti"
PASSWORD = "Store01"
DATA_FILE = Path("data_produk.json")

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🛍️",
    layout="wide"
)

# =========================
# SESSION STATE
# =========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "nomor_id" not in st.session_state:
    st.session_state.nomor_id = 1

if "daftar_produk" not in st.session_state:
    st.session_state.daftar_produk = []


# =========================
# LOAD DATA
# =========================

def load_data():
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            st.session_state.daftar_produk = data

            max_id = 0

            for p in data:
                try:
                    angka = int(p["id_produk"][1:])
                    max_id = max(max_id, angka)
                except:
                    pass

            st.session_state.nomor_id = max_id + 1

        except Exception as e:
            st.error(f"Gagal load data: {e}")


# =========================
# SAVE DATA
# =========================

def save_data():
    DATA_FILE.write_text(
        json.dumps(
            st.session_state.daftar_produk,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


# =========================
# GENERATE ID
# =========================

def generate_id():
    kode = f"B{st.session_state.nomor_id:03}"
    st.session_state.nomor_id += 1
    return kode


# =========================
# LOGIN
# =========================

with st.sidebar:

    st.header("Login Admin")

    if not st.session_state.logged_in:

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Masuk"):

            if password == PASSWORD:
                st.session_state.logged_in = True
                load_data()
                st.success("Login berhasil")
                st.rerun()

            else:
                st.error("Password salah")

    else:

        st.success("Login aktif")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

if not st.session_state.logged_in:
    st.stop()


# =========================
# JUDUL
# =========================

st.title("🛍️ Store Pusepmuti")

menu = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Tambah Produk",
        "Daftar Produk",
        "Cari Produk",
        "Jual Produk",
        "Update Stok",
        "Simpan Data",
        "Close Shift"
    ]
)

# =========================
# DASHBOARD
# =========================

if menu == "Dashboard":

    st.header("Dashboard")

    df = pd.DataFrame(
        st.session_state.daftar_produk
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Jumlah Produk",
        len(df)
    )

    total_stok = (
        int(df["stok"].sum())
        if not df.empty else 0
    )

    col2.metric(
        "Total Stok",
        total_stok
    )

    total_nilai = (
        int((df["harga"] * df["stok"]).sum())
        if not df.empty else 0
    )

    col3.metric(
        "Nilai Persediaan",
        f"Rp{total_nilai:,}".replace(",", ".")
    )

    st.dataframe(
        df,
        use_container_width=True
    )


# =========================
# TAMBAH PRODUK
# =========================

elif menu == "Tambah Produk":

    st.header("Tambah Produk")

    with st.form("tambah_produk"):

        nama = st.text_input("Nama Produk")

        harga = st.number_input(
            "Harga",
            min_value=0
        )

        stok = st.number_input(
            "Stok",
            min_value=0
        )

        kategori = st.text_input(
            "Kategori"
        )

        submit = st.form_submit_button(
            "Tambah Produk"
        )

    if submit:

        produk = {
            "id_produk": generate_id(),
            "nama": nama,
            "harga": int(harga),
            "stok": int(stok),
            "kategori": kategori
        }

        st.session_state.daftar_produk.append(
            produk
        )

        st.success(
            f"Produk berhasil ditambahkan dengan ID {produk['id_produk']}"
        )


# =========================
# DAFTAR PRODUK
# =========================

elif menu == "Daftar Produk":

    st.header("Daftar Produk")

    df = pd.DataFrame(
        st.session_state.daftar_produk
    )

    st.dataframe(
        df,
        use_container_width=True
    )


# =========================
# CARI PRODUK
# =========================

elif menu == "Cari Produk":

    st.header("Cari Produk")

    keyword = st.text_input(
        "Masukkan nama produk"
    )

    if keyword:

        hasil = []

        for produk in st.session_state.daftar_produk:

            if keyword.lower() in produk["nama"].lower():
                hasil.append(produk)

        if hasil:

            st.success(
                "Produk ditemukan"
            )

            st.dataframe(
                pd.DataFrame(hasil),
                use_container_width=True
            )

        else:
            st.error(
                "Produk tidak ditemukan"
            )


# =========================
# JUAL PRODUK
# =========================

elif menu == "Jual Produk":

    st.header("Penjualan")

    if not st.session_state.daftar_produk:

        st.warning(
            "Belum ada produk"
        )

    else:

        ids = [
            p["id_produk"]
            for p in st.session_state.daftar_produk
        ]

        pid = st.selectbox(
            "Pilih Produk",
            ids
        )

        jumlah = st.number_input(
            "Jumlah Beli",
            min_value=1
        )

        metode = st.selectbox(
            "Metode Pembayaran",
            [
                "Cash",
                "Debit",
                "Kredit"
            ]
        )

        if st.button(
            "Proses Penjualan"
        ):

            produk = None

            for p in st.session_state.daftar_produk:
                if p["id_produk"] == pid:
                    produk = p
                    break

            if jumlah > produk["stok"]:

                st.error(
                    "Stok tidak mencukupi"
                )

            else:

                total = produk["harga"] * jumlah

                garansi = (
                    "1 Tahun"
                    if produk["harga"] >= 1000000
                    else "6 Bulan"
                )

                cashback = 0

                if total >= 100000:
                    cashback = 500000

                total_bayar = total - cashback

                produk["stok"] -= jumlah

                st.success(
                    "Transaksi Berhasil"
                )

                st.write(
                    f"Produk : {produk['nama']}"
                )
                st.write(
                    f"Metode : {metode}"
                )
                st.write(
                    f"Garansi : {garansi}"
                )
                st.write(
                    f"Cashback : Rp{cashback:,}".replace(",", ".")
                )
                st.write(
                    f"Total Bayar : Rp{total_bayar:,}".replace(",", ".")
                )
                st.write(
                    f"Sisa Stok : {produk['stok']}"
                )


# =========================
# UPDATE STOK
# =========================

elif menu == "Update Stok":

    st.header(
        "Update Stok"
    )

    if not st.session_state.daftar_produk:

        st.warning(
            "Belum ada produk"
        )

    else:

        ids = [
            p["id_produk"]
            for p in st.session_state.daftar_produk
        ]

        pid = st.selectbox(
            "Pilih Produk",
            ids
        )

        tambah = st.number_input(
            "Tambah Stok",
            min_value=1
        )

        if st.button(
            "Update"
        ):

            for p in st.session_state.daftar_produk:

                if p["id_produk"] == pid:

                    p["stok"] += tambah

                    st.success(
                        f"Stok sekarang: {p['stok']}"
                    )

                    break


# =========================
# SIMPAN DATA
# =========================

elif menu == "Simpan Data":

    st.header("Simpan Data")

    if st.button(
        "Simpan ke JSON"
    ):

        save_data()

        st.success(
            "Data berhasil disimpan"
        )


# =========================
# CLOSE SHIFT
# =========================

elif menu == "Close Shift":

    st.header(
        "Close Shift"
    )

    pilihan = st.radio(
        "Pilih Shift",
        [
            "Close Shift Pusep",
            "Close Shift Muti"
        ]
    )

    if st.button(
        "Tutup Shift"
    ):

        st.session_state.logged_in = False

        if pilihan == "Close Shift Pusep":

            st.success(
                "✨ Shift Pusep berhasil ditutup"
            )

        else:

            st.success(
                "✨ Shift Muti berhasil ditutup"
            )

        st.rerun()