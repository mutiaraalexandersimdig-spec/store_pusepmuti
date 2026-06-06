import json
from pathlib import Path
import streamlit as st
import pandas as pd

APP_TITLE = "Store Pusepmuti"
PASSWORD = "Store01"
DATA_FILE = Path("data_produk.json")

st.set_page_config(page_title=APP_TITLE, page_icon="🛍️", layout="wide")

def init_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "nomor_id" not in st.session_state:
        st.session_state.nomor_id = 1
    if "daftar_produk" not in st.session_state:
        st.session_state.daftar_produk = []

def load_data():
    if DATA_FILE.exists():
        try:
            raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            st.session_state.daftar_produk = raw
        except:
            pass

def save_data():
    DATA_FILE.write_text(
        json.dumps(st.session_state.daftar_produk, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

def generate_id():
    kode = f"B{st.session_state.nomor_id:03}"
    st.session_state.nomor_id += 1
    return kode

init_state()

st.title("🛍️ Store Pusepmuti")

with st.sidebar:
    st.header("Login Admin")

    if not st.session_state.logged_in:
        pw = st.text_input("Password", type="password")

        if st.button("Masuk"):
            if pw == PASSWORD:
                st.session_state.logged_in = True
                load_data()
                st.success("Login berhasil")
            else:
                st.error("Password salah")

if not st.session_state.logged_in:
    st.stop()

menu = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Tambah Produk",
        "Daftar Produk",
        "Simpan Data"
    ]
)

if menu == "Dashboard":

    df = pd.DataFrame(st.session_state.daftar_produk)

    st.subheader("Dashboard")

    st.write(f"Jumlah Produk: {len(df)}")

    if not df.empty:
        st.dataframe(df, use_container_width=True)

elif menu == "Tambah Produk":

    st.subheader("Tambah Produk")

    nama = st.text_input("Nama Produk")
    harga = st.number_input("Harga", min_value=0)
    stok = st.number_input("Stok", min_value=0)
    kategori = st.text_input("Kategori")

    if st.button("Tambah"):

        st.session_state.daftar_produk.append({
            "id_produk": generate_id(),
            "nama": nama,
            "harga": int(harga),
            "stok": int(stok),
            "kategori": kategori
        })

        st.success("Produk berhasil ditambahkan")

elif menu == "Daftar Produk":

    st.subheader("Daftar Produk")

    df = pd.DataFrame(st.session_state.daftar_produk)

    st.dataframe(df, use_container_width=True)

elif menu == "Simpan Data":

    if st.button("Simpan ke JSON"):
        save_data()
        st.success("Data berhasil disimpan")