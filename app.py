import streamlit as st
import google.generativeai as genai
import time
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io

# Config Halaman
st.set_page_config(page_title="Generator Modul Ajar Deep Learning", page_icon="📚", layout="wide")

# Header Aplikasi
st.title("📚 Generator Modul Ajar Deep Learning")
st.subheader("SMP Tri Sukses Boarding School Jambi (1 JP = 30 Menit)")
st.caption("Berbasis CP Terbaru BSKAP 046/H/KR/2025 - Kurikulum Merdeka")

# FUNGSI UNTUK MERUBAH TEKS MENJADI FILE DOCX (WORD)
def generate_docx(title, content):
    doc = Document()
    
    # Setting Margin (Normal 1 inch)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        
    # Judul Dokumen
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run(f"MODUL AJAR DEEP LEARNING\n{title.upper()}")
    run_title.font.name = 'Arial'
    run_title.font.size = Pt(14)
    run_title.font.bold = True
    
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    # Mengolah Teks Baris demi Baris
    lines = content.split('\n')
    for line in lines:
        line_strip = line.strip()
        if not line_strip:
            continue
            
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        
        # Heading 1 / Judul Utama
        if line_strip.startswith('# '):
            run = p.add_run(line_strip[2:])
            run.font.name = 'Arial'
            run.font.size = Pt(12)
            run.font.bold = True
        # Heading 2 / Sub Judul
        elif line_strip.startswith('## '):
            run = p.add_run(line_strip[3:])
            run.font.name = 'Arial'
            run.font.size = Pt(11)
            run.font.bold = True
        # Heading 3
        elif line_strip.startswith('### '):
            run = p.add_run(line_strip[4:])
            run.font.name = 'Arial'
            run.font.size = Pt(10.5)
            run.font.bold = True
        # Poin / Bullet List
        elif line_strip.startswith('* ') or line_strip.startswith('- '):
            p.style = 'List Bullet'
            run = p.add_run(line_strip[2:])
            run.font.name = 'Arial'
            run.font.size = Pt(10.5)
        # Paragraf Biasa
        else:
            run = p.add_run(line_strip)
            run.font.name = 'Arial'
            run.font.size = Pt(10.5)

    # Simpan ke memory buffer
    bio = io.BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio

# SISTEM API KEY OTOMATIS (Membaca dari Streamlit Secrets)
api_key = ""
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]

# Sidebar
st.sidebar.header("⚙️ Pengaturan Aplikasi")
if api_key:
    st.sidebar.success("✅ Akses AI Otomatis Aktif!")
else:
    api_key = st.sidebar.text_input("Masukkan Gemini API Key (Manual):", type="password")

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
    
    # DROPDOWN REKOMENDASI TOPIK
    pilihan_topik = st.selectbox(
        "💡 Pilih Rekomendasi Topik/Materi (Sesuai CP Terbaru):",
        REKOMENDASI_TOPIK[elemen_cp]
    )
    
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
        st.error("Sistem API Key belum terkonfigurasi. Silakan isi API Key di Settings Streamlit!")
    elif not topik_final:
        st.warning("Silakan pilih atau ketikkan Topik/Pokok Bahasan Materi terlebih dahulu.")
    else:
        try:
            genai.configure(api_key=api_key)
            
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

            # DAFTAR PRIORITAS MODEL DENGAN AUTO-FALLBACK
            model_candidates = [
                'gemini-1.5-flash',
                'gemini-1.5-flash-8b',
                'gemini-1.5-pro',
                'gemini-2.0-flash',
                'gemini-pro'
            ]
            
            response = None
            success = False
            last_error = ""

            with st.spinner("AI sedang menyusun Modul Ajar Deep Learning... Mohon tunggu sebentar."):
                for model_name in model_candidates:
                    try:
                        model = genai.GenerativeModel(model_name)
                        response = model.generate_content(prompt)
                        success = True
                        break
                    except Exception as e:
                        last_error = str(e)
                        time.sleep(1)
                        continue

            if success and response:
                st.success("✨ Modul Ajar Berhasil Dibuat!")
                st.markdown("---")
                
                # Menampilkan Teks Hasil
                st.markdown(response.text)
                st.markdown("---")
                
                # OPSI UNDUH: WORD (.DOCX) & TEKS (.TXT)
                col_dl1, col_col_dl2 = st.columns(2)
                
                # Konversi Hasil AI ke File Word
                docx_file = generate_docx(f"{mapel} - {topik_final}", response.text)
                
                with col_dl1:
                    st.download_button(
                        label="📄 Unduh File MS Word (.docx)",
                        data=docx_file,
                        file_name=f"Modul_Ajar_{mapel}_{kelas}_{topik_final}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        type="primary"
                    )
                
                with col_col_dl2:
                    st.download_button(
                        label="💾 Unduh Teks (.txt)",
                        data=response.text,
                        file_name=f"Modul_Ajar_{mapel}_{kelas}_{topik_final}.txt",
                        mime="text/plain"
                    )
            else:
                st.error("Layanan AI sedang sibuk/mencapai batas kuota gratis. Tunggu sekitar 30 detik lalu coba lagi.")

        except Exception as e:
            st.error(f"Terjadi kesalahan sistem: {e}")
