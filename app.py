import streamlit as st
import google.generativeai as genai
import time
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io

st.set_page_config(page_title="Generator Modul Ajar Deep Learning", page_icon="📚", layout="wide")

st.title("📚 Generator Modul Ajar Deep Learning")
st.subheader("SMP Tri Sukses Boarding School Jambi (1 JP = 30 Menit)")
st.caption("Berbasis CP Terbaru BSKAP 046/H/KR/2025 - Kurikulum Merdeka")

# FUNGSI EXPORT DOCX
def generate_docx(title, content):
    doc = Document()
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run(f"MODUL AJAR DEEP LEARNING\n{title.upper()}")
    run_title.font.name = 'Arial'
    run_title.font.size = Pt(14)
    run_title.font.bold = True
    
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    lines = content.split('\n')
    for line in lines:
        line_strip = line.strip()
        if not line_strip:
            continue
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        
        if line_strip.startswith('# '):
            run = p.add_run(line_strip[2:])
            run.font.bold = True
        elif line_strip.startswith('## '):
            run = p.add_run(line_strip[3:])
            run.font.bold = True
        elif line_strip.startswith('* ') or line_strip.startswith('- '):
            p.style = 'List Bullet'
            run = p.add_run(line_strip[2:])
        else:
            run = p.add_run(line_strip)
            
    bio = io.BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio

# SISTEM MULTI-KEY ROTATION (Membaca list key dari Secrets)
api_keys = []
if "GEMINI_API_KEYS" in st.secrets:
    # Mengambil list key yang dipisahkan koma
    api_keys = [k.strip() for k in st.secrets["GEMINI_API_KEYS"].split(",") if k.strip()]
elif "GEMINI_API_KEY" in st.secrets:
    api_keys = [st.secrets["GEMINI_API_KEY"]]

# Sidebar
st.sidebar.header("⚙️ Pengaturan Aplikasi")
if api_keys:
    st.sidebar.success(f"✅ Akses AI Aktif ({len(api_keys)} Kunci Cadangan Tersedia)")
else:
    manual_key = st.sidebar.text_input("Masukkan Gemini API Key (Manual):", type="password")
    if manual_key:
        api_keys = [manual_key]

st.sidebar.markdown("---")
st.sidebar.info("""
**Aturan Standar Sekolah:**
- 1 JP = 30 Menit
- Strategi Deep Learning: Mindful, Meaningful, Joyful
- Pendekatan Ramah Asrama / Non-Gadget (Unplugged)
""")

# DATABASE REKOMENDASI TOPIK
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

# Form Input
st.header("📝 Form Isian Modul Ajar")
col1, col2 = st.columns(2)

with col1:
    mapel = st.selectbox("Mata Pelajaran", ["Informatika", "IPA", "Matematika", "Bahasa Indonesia", "Pendidikan Pancasila"])
    kelas = st.selectbox("Kelas (Fase D)", ["Kelas 7", "Kelas 8", "Kelas 9"])
    elemen_cp = st.selectbox("Elemen CP (Informatika)", list(REKOMENDASI_TOPIK.keys()))
    pilihan_topik = st.selectbox("💡 Pilih Rekomendasi Topik/Materi (Sesuai CP Terbaru):", REKOMENDASI_TOPIK[elemen_cp])
    
    if pilihan_topik == "Lainnya (Ketik Manual)":
        topik_final = st.text_input("Ketikkan Topik/Pokok Bahasan Custom:", placeholder="Contoh: Logika Pengurutan Sandal di Masjid")
    else:
        topik_final = pilihan_topik

with col2:
    jumlah_pertemuan = st.number_input("Jumlah Pertemuan", min_value=1, max_value=5, value=2)
    jp_per_pertemuan = st.number_input("Alokasi JP per Pertemuan (1 JP = 30 mnt)", min_value=1, max_value=4, value=2)
    pendekatan = st.radio("Pendekatan Pembelajaran", ["Unplugged (Tanpa Gadget/Cetak/Papan Tulis)", "Plugged (Praktik Lab/Komputer)"])

st.markdown("---")

if st.button("🚀 Buat Modul Ajar Sekarang", type="primary"):
    if not api_keys:
        st.error("API Key belum dikonfigurasi.")
    elif not topik_final:
        st.warning("Pilih atau ketikkan Topik terlebih dahulu.")
    else:
        total_menit = jp_per_pertemuan * 30
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

        === ATURAN DEEP LEARNING (3M) & BOARDING SCHOOL ===
        1. Mindful: Apersepsi niat belajar, kesadaran diri, pertanyaan pemantik kehidupan asrama.
        2. Meaningful: Studi kasus kontekstual boarding school.
        3. Joyful: Metode interaktif, diskusi kelompok, atau simulasi fisik unplugged.
        4. Durasi Waktu: Presisi berdasarkan {total_menit} Menit per pertemuan.

        === STRUKTUR OUTPUT ===
        1. IDENTITAS & DESAIN MODUL
        2. PERTEMUAN DEMI PERTEMUAN (Rinci Pertemuan 1 - {jumlah_pertemuan}):
           - TP Khusus, Pertanyaan Pemantik, Pendahuluan ({int(total_menit*0.15)} mnt), Inti ({int(total_menit*0.70)} mnt), Penutup ({int(total_menit*0.15)} mnt).
        3. RENCANA ASESMEN & RUBRIK KARAKTER SANTRI
        4. DRAF LKPD CETAK / PAPER-BASED
        """

        model_names = ['gemini-1.5-flash', 'gemini-1.5-flash-8b', 'gemini-1.5-pro']
        success = False
        response_text = ""
        last_err = ""

        with st.spinner("AI sedang menyusun Modul Ajar..."):
            # PERTAMA: Coba putar semua API Key yang tersedia
            for key in api_keys:
                if success:
                    break
                try:
                    genai.configure(api_key=key)
                    for m_name in model_names:
                        try:
                            model = genai.GenerativeModel(m_name)
                            res = model.generate_content(prompt)
                            response_text = res.text
                            success = True
                            break
                        except Exception as e_mod:
                            last_err = str(e_mod)
                            continue
                except Exception as e_key:
                    last_err = str(e_key)
                    continue

        if success:
            st.success("✨ Modul Ajar Berhasil Dibuat!")
            st.markdown("---")
            st.markdown(response_text)
            st.markdown("---")
            
            col_dl1, col_dl2 = st.columns(2)
            docx_file = generate_docx(f"{mapel} - {topik_final}", response_text)
            
            with col_dl1:
                st.download_button(
                    label="📄 Unduh File MS Word (.docx)",
                    data=docx_file,
                    file_name=f"Modul_Ajar_{mapel}_{kelas}_{topik_final}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    type="primary"
                )
            with col_dl2:
                st.download_button(
                    label="💾 Unduh Teks (.txt)",
                    data=response_text,
                    file_name=f"Modul_Ajar_{mapel}_{kelas}_{topik_final}.txt",
                    mime="text/plain"
                )
        else:
            st.error("Gagal menghubungkan ke AI. Silakan tunggu 10 detik lalu klik tombol lagi.")
            st.caption(f"Error detail: {last_err}")
