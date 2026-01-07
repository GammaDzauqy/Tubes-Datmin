import streamlit as st
import os
from src.engine import load_documents, search_engine, get_summary

st.set_page_config(page_title="E-Arsip (IFB-307)", layout="wide")

st.title("📂 Sistem Pencarian Arsip Surat Perusahaan")
st.markdown("---")

# Load Data
DATA_FOLDER = "data"
df_docs = load_documents(DATA_FOLDER)

# Sidebar Informasi
st.sidebar.header("Statistik Sistem")
st.sidebar.info(f"Jumlah Dokumen Terindeks: {len(df_docs)}")
if st.sidebar.button("Refresh Data"):
    st.experimental_rerun()

if "did_rerun" not in st.session_state:
    st.session_state.did_rerun = True
    st.experimental_rerun()

# Pencarian (Fitur Utama)
query = st.text_input("🔍 Masukkan kata kunci atau perihal surat:", placeholder="Contoh: SK Pengangkatan")

if query:
    if len(df_docs) == 0:
        st.error("Folder 'data' kosong! Masukkan file .txt terlebih dahulu.")
    else:
        results = search_engine(query, df_docs)
        
        if not results.empty:
            st.success(f"Ditemukan {len(results)} dokumen yang relevan.")
            
            for _, row in results.iterrows():
                # Tampilkan hasil dengan Ranking dan Summary (Fitur Wajib 4 & 6)
                with st.expander(f"📄 {row['filename']} (Skor Relevansi: {row['score']:.4f})"):
                    st.subheader("Ringkasan Dokumen (Extractive):")
                    st.write(get_summary(row['content']))
                    st.markdown("---")
                    st.subheader("Isi Lengkap:")
                    st.text(row['content'])
        else:
            st.warning("Tidak ada dokumen yang cocok dengan kata kunci tersebut.")
else:
    st.info("Silakan ketik kata kunci untuk mulai mencari.")