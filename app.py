import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Pilihan halaman
page = st.sidebar.selectbox("Pilih Halaman", ["Beranda", "Visualisasi"])

if page == "Beranda":
    st.title("Selamat Datang di Halaman Beranda")

elif page == "Visualisasi":
    st.header("Halaman Visualisasi")

    # Baca file CSV
    data = pd.read_csv("pddikti_example.csv")

    # Filter berdasarkan universitas
    selected_university = st.selectbox('Pilih Universitas', data['universitas'].unique())
    filtered_data = data[data['universitas'] == selected_university]

    # Buat visualisasi
    fig, ax = plt.subplots(figsize=(12, 6))

    for prog_studi in filtered_data['program_studi'].unique():
        subset = filtered_data[filtered_data['program_studi'] == prog_studi]

        # Urutkan data berdasarkan 'id' dengan urutan menurun
        subset = subset.sort_values(by="id", ascending=False)

        ax.plot(subset['semester'], subset['jumlah'], label=prog_studi)

    ax.set_title(f"Visualisasi Data untuk {selected_university}")
    ax.set_xlabel('Semester')
    ax.set_xticks(subset['semester'])
    ax.set_xticklabels(subset['semester'], rotation=90)
    ax.set_ylabel('Jumlah')
    ax.legend()

    st.pyplot(fig)  # Menampilkan figure secara eksplisit
