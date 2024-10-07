import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

# Fungsi untuk mendapatkan koneksi ke database MySQL
def get_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='db_dal'
    )
    return connection

# Fungsi untuk mengambil data dari database
def get_data_from_db():
    conn = get_connection()
    query = "SELECT * FROM pddikti_example"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.title('Streamlit Simple App')

# Menambahkan navigasi di sidebar
page = st.sidebar.radio("Pilih halaman", ["Dataset", "Visualisasi", "Form input"])

if page == "Dataset":
    st.header("Halaman Dataset")

    # Baca data dari database
    data = get_data_from_db()

    # Tampilkan data di Streamlit
    st.write(data)

elif page == "Visualisasi":
    st.header("Halaman Visualisasi")
    
    # Baca data dari database
    data = get_data_from_db()

    # Pastikan kolom 'universitas' ada di data
    if 'universitas' in data.columns:
        # Filter berdasarkan universitas
        selected_university = st.selectbox('Pilih Universitas', data['universitas'].unique())
        filtered_data = data[data['universitas'] == selected_university]

        # Buat figure dan axis baru
        fig, ax = plt.subplots(figsize=(12, 6))

        for prog_studi in filtered_data['program_studi'].unique():
            subset = filtered_data[filtered_data['program_studi'] == prog_studi]
            subset = subset.sort_values(by='id', ascending=False)

            ax.plot(subset['semester'], subset['jumlah'], label=prog_studi)

        ax.set_title(f"Visualisasi Data untuk {selected_university}")
        ax.set_xlabel('Semester')
        ax.set_ylabel('Jumlah')
        ax.legend()
        plt.xticks(rotation=90)  # Rotasi label sumbu x menjadi vertikal

        # Tampilkan figure di Streamlit
        st.pyplot(fig)
    else:
        st.error("Kolom 'universitas' tidak ditemukan dalam data.")

elif page == "Form input":
    st.header("Halaman Form Input")

    # Input form
    with st.form(key='input_form'):
        input_semester = st.text_input('Semester')
        input_jumlah = st.number_input('Jumlah', min_value=0, format='%d')
        input_program_studi = st.text_input('Program Studi')
        input_universitas = st.text_input('Universitas')
        submit_button = st.form_submit_button(label='Submit Data')

    if submit_button:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO pddikti_example(semester, jumlah, program_studi, universitas)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (input_semester, input_jumlah, input_program_studi, input_universitas))
        conn.commit()
        conn.close()
        st.success("Data successfully submitted to the database!")
