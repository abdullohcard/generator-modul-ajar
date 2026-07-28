import streamlit as st
import google.generativeai as genai

# Config Halaman
st.set_page_config(page_title="Generator Modul Ajar Deep Learning", page_icon="📚", layout="wide")

# Header Aplikasi
st.title("📚 Generator Modul Ajar Deep Learning")
st.subheader("SMP Tri Sukses Boarding School Jambi (1 JP = 30 Menit)")
st.caption("Berbasis CP Terbaru BSKAP 046/H/KR/2025 - Kurikulum Merdeka")

# Sidebar untuk Pengaturan API Key
st.sidebar.header("🔑 Pengaturan Akses AI")
api_key = st.sidebar.text_input("Masukkan Google Gemini API Key Anda:", type="password")

st.sidebar.markdown("---")
st.sidebar.info("""
**Aturan Standar Sekolah:**
- 1 JP = 30 Menit
- Strategi Deep Learning: Mindful, Meaningful, Joyful
- Pendekatan Ramah Asrama / Non-Gadget (Unplugged)
""")

# DATABASE REKOMENDASI TOPIK BERDASARKAN CP INFORMATIKA FASE D (BSKAP 046/H/KR/2025)
REKOMENDASI_TOPIK = {
    "Berpikir Komputasional": [
        "Penerapan BK untuk Pemecahan Masalah Sehari-hari Santri di Asrama",
        "Pengenalan Konsep Himpunan Data Terstruktur dalam Kehidupan Sekolah",
        "Pemanfaatan Lembar Kerja Pengolah Data untuk Penyelesaian Masalah Sederhana",
        "Penyelesaian Persoalan Data Berstruktur Sederhana Volume Kecil",
        "Penulisan Sekumpulan Instruksi Algoritma Menggunakan Pseudocode Sederhana",
        "Lainnya (Ketik Manual)"
    ],
    "Literasi Digital": [
        "Cara Kerja dan Penggunaan Mesin Pencari (Search Engine) Secara Efektif",
        "Evaluasi Kualitas Informasi, Kredibilitas Sumber, dan Membedakan Fakta vs Hoaks",
        "Pengenalan Ekosistem Media Pers Digital dan Etika Berkomunikasi",
        "Pemanfaatan Aplikasi Pengolah Dokumen, Lembar Kerja, dan Presentasi",
        "Komponen, Fungsi, dan Cara Kerja Utama Komputer",
        "Konsep Konektivitas Jaringan Lokal dan Internet (Kabel & Nirkabel)",
        "Pemanfaatan Perangkat Digital untuk Produksi dan Diseminasi Konten Positif",
        "Rekam Jejak Digital, Kesadaran Penuh (Mindfulness), dan Toleransi di Dunia Digital",
        "Keamanan Digital: Kata Sandi Aman, Proteksi Data Pribadi, dan Pencegahan Malware",
        "Lainnya (Ketik Manual)"
    ],
    "Analisis Data": [
        "Pengumpulan dan Penataan Data Kegiatan Santri Secara Terstruktur",
        "Pemrosesan dan Visualisasi Data Sederhana Menggunakan Lembar Kerja",
        "Analisis Data Hasil Pengamatan Lingkungan Sekolah/Asrama",
        "Lainnya (Ketik Manual)"
    ],
    "Algoritma dan Pemrograman": [
        "Perancangan Langkah Logis (Algoritma) Aktivitas Harian",
        "Penerapan Struktur Kontrol dan Percabangan Logika Sederhana",
        "Penerapan Pseudocode dan Flowchart untuk Logika Program Unplugged",
        "Lainnya (Ketik Manual)"
    ]
}

# Form Input Data Modul
st.header("📝 Form Isian Modul Ajar")

col1, col2 = st.columns(2)

with col1:
    mapel = st.selectbox("Mata Pelajaran", ["Informatika", "IPA", "Matematika", "Bahasa Indonesia", "Pendidikan Pancasila"])
    kelas = st.selectbox("Kelas (Fase D)", ["Kelas 7", "Kelas 8", "Kelas 9"])
    
    # Dropdown Elemen CP
    elemen_cp = st.selectbox("Elemen CP (Informatika)", list(REKOMENDASI_TOPIK.keys()))
    
    # DROPDOWN REKOMENDASI TOPIK (Otomatis berubah sesuai Elemen yang dipilih)
    pilihan_topik = st.selectbox(
        "💡 Pilih Rekomendasi Topik/Materi (Sesuai CP Terbaru):",
        REKOMENDASI_TOPIK[elemen_cp]
    )
    
    # Jika memilih 'Lainnya (Ketik Manual)', munculkan input box
    if pilihan_topik == "Lainnya (Ketik Manual)":
        topik_final = st.text_input("Ketikkan Topik/Pokok Bahasan Custom:", placeholder="Contoh: Logika Pengurutan Sandal di Masjid")
    else:
        topik_final = pilihan_topik

with col2:
    jumlah_pertemuan = st.number_input("Jumlah Pertemuan", min_value=1, max_value=5, value=2)
    jp_per_pertemuan = st.number_input("Alokasi JP per Pertemuan (1 JP = 30 mnt)", min_value=1, max_value=4, value=2)
    pendekatan = st.radio("Pendekatan Pembelajaran", ["Unplugged (Tanpa Gadget/Cetak/Papan Tulis)", "Plugged (Praktik Lab/Komputer)"])

st.markdown("---")

# Tombol Eksekusi
if st.button("🚀 Buat Modul Ajar Sekarang", type="primary"):
    if not api_key:
        st.error("Silakan masukkan Gemini API Key Anda terlebih dahulu di menu sebelah kiri (Sidebar)!")
    elif not topik_final:
        st.warning("Silakan pilih atau ketikkan Topik/Pokok Bahasan Materi terlebih dahulu.")
    else:
        try:
            # Inisialisasi Gemini API
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            total_menit = jp_per_pertemuan * 30
            
            # Formulasi Prompt System
            prompt = f"""
            Anda adalah pakar kurikulum dan konsultan edukasi Kurikulum Merdeka Kemendikdasmen Indonesia.
            Buatkan Modul Ajar Pembelajaran Mendalam (Deep Learning) terstruktur dan rapi.

            === INFORMASI UTAMA ===
            - Sekolah: SMP Tri Sukses Boarding School Jambi
            - Mata Pelajaran: {mapel}
            - Jenjang / Fase: {kelas} (Fase D)
            - Elemen CP: {elemen_cp} (Berdasarkan BSKAP 046/H/KR/2025)
            - Topik / Pokok Bahasan: {topik_final}
            - Jumlah Pertemuan: {jumlah_pertemuan} Pertemuan
            - Durasi per Pertemuan: {jp_per_pertemuan} JP ({total_menit} Menit)
            - Pendekatan: {pendekatan}

            === ATURAN PEMBELAJARAN DEEP LEARNING (3M) & BOARDING SCHOOL ===
            1. Mindful (Berkesadaran): Apersepsi berorientasi niat belajar, kesadaran diri, dan pertanyaan pemantik yang relevan dengan kehidupan santri/lingkungan asrama.
            2. Meaningful (Bermakna): Studi kasus kontekstual yang dekat dengan kehidupan sehari-hari siswa di boarding school.
            3. Joyful (Menggembirakan): Metode interaktif, diskusi kelompok, atau simulasi fisik (khususnya jika pendekatan Unplugged/non-gadget).
            4. Durasi Waktu: Pembagian alokasi menit harus presisi berdasarkan {total_menit} Menit per pertemuan.

            === STRUKTUR OUTPUT ===
            1. IDENTITAS & DESAIN MODUL (Mapel, Kelas, Alokasi Waktu, Elemen CP, Dimensi Lulusan).
            2. PERTEMUAN DEMI PERTEMUAN (Sajikan rinci dari Pertemuan 1 hingga Pertemuan {jumlah_pertemuan}):
               - Tujuan Pembelajaran (TP) Khusus Pertemuan Ini
               - Pertanyaan Pemantik (Mindful)
               - Kegiatan Pendahuluan ({int(total_menit*0.15)} Menit)
               - Kegiatan Inti: Memahami & Mengaplikasikan ({int(total_menit*0.70)} Menit)
               - Kegiatan Penutup & Refleksi: Merefleksikan ({int(total_menit*0.15)} Menit)
            3. RENCANA ASESMEN (Diagnostik, Formatif, Rubrik Penilaian Karakter Santri).
            4. DRAF LEMBAR KERJA PESERTA DIDIK (LKPD) CETAK / PAPER-BASED.
            """

            with st.spinner("AI sedang menyusun Modul Ajar Deep Learning... Mohon tunggu sebentar."):
                response = model.generate_content(prompt)
                
                st.success("✨ Modul Ajar Berhasil Dibuat!")
                st.markdown("---")
                
                # Menampilkan Hasil Generator
                st.markdown(response.text)
                
                # Fitur Download / Copy Text
                st.download_button(
                    label="💾 Unduh Hasil Modul (.txt)",
                    data=response.text,
                    file_name=f"Modul_Ajar_{mapel}_{kelas}_{topik_final}.txt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(f"Terjadi kesalahan saat menghubungkan ke AI: {e}")
