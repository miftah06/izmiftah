import random

import pdfkit
from fpdf import FPDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# Fungsi untuk menghasilkan daftar kata kunci secara acak
def generate_random_keywords(num_keywords):
    # Daftar kata kunci acak
    keywords = []

    # Batasi jumlah kata kunci yang dihasilkan hingga num_keywords
    while len(keywords) < num_keywords:
        # Ganti dengan logika Anda untuk menghasilkan kata kunci acak
        # Di sini, kita akan menggunakan kata-kata acak sebagai contoh
        random_keyword = "Keyword_" + str(random.randint(1, 100))
        keywords.append(random_keyword)

    return keywords

# Fungsi untuk menghasilkan daftar kata kunci dalam bentuk PDF menggunakan pdfkit
def generate_keywords_pdf_pdfkit(keywords, pdf_filename):
    # Buat HTML dari daftar kata kunci
    html_content = "<html><body><ul>"
    for keyword in keywords:
        html_content += f"<li>{keyword}</li>"
    html_content += "</ul></body></html>"

    # Simpan HTML dalam file sementara
    html_file = "temp_keywords.html"
    with open(html_file, "w") as f:
        f.write(html_content)

    # Mengonversi HTML ke PDF menggunakan pdfkit
    pdfkit.from_file(html_file, pdf_filename)

    print(f"Dokumen PDF berhasil disimpan di {pdf_filename}")

# Fungsi untuk menghasilkan daftar kata kunci dalam bentuk PDF menggunakan fpdf
def generate_keywords_pdf_fpdf(keywords, pdf_filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for keyword in keywords:
        pdf.cell(200, 10, txt=keyword, ln=True)

    pdf.output(pdf_filename)
    print(f"Dokumen PDF berhasil disimpan di {pdf_filename}")

# Fungsi untuk menghasilkan dokumen PDF dari daftar kata kunci dengan reportlab
def generate_keywords_pdf_reportlab(keywords, pdf_filename):
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # Set font dan ukuran teks
    c.setFont("Helvetica", 12)

    # Tulis daftar kata kunci ke PDF
    y = 700
    for keyword in keywords:
        c.drawString(50, y, keyword)
        y -= 20

    # Simpan PDF
    c.save()

    print(f"Dokumen PDF berhasil disimpan di {pdf_filename}")

# Fungsi untuk menggabungkan semua fungsi di atas
def main():
    try:
        num_keywords = 5  # Ganti dengan jumlah kata kunci yang Anda inginkan

        # Generate daftar kata kunci secara acak
        random_keywords = generate_random_keywords(num_keywords)

        # Nama file PDF yang akan dihasilkan
        pdf_filename_pdfkit = "random_keywords_pdfkit.pdf"
        pdf_filename_fpdf = "random_keywords_fpdf.pdf"
        pdf_filename_reportlab = "random_keywords_reportlab.pdf"

        # Generate daftar kata kunci dalam bentuk PDF menggunakan pdfkit
        generate_keywords_pdf_pdfkit(random_keywords, pdf_filename_pdfkit)

        # Generate daftar kata kunci dalam bentuk PDF menggunakan fpdf
        generate_keywords_pdf_fpdf(random_keywords, pdf_filename_fpdf)

        # Generate daftar kata kunci dalam bentuk PDF menggunakan reportlab
        generate_keywords_pdf_reportlab(random_keywords, pdf_filename_reportlab)

        print("Kata kunci acak telah dihasilkan.")
        print(f"PDF (pdfkit): {pdf_filename_pdfkit}")
        print(f"PDF (fpdf): {pdf_filename_fpdf}")
        print(f"PDF (reportlab): {pdf_filename_reportlab}")
    except Exception as e:
        print(f"Error: {e}")

def get_keywords_from_csv(csv_filename):
    keywords = []
    try:
        with open(csv_filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                keywords.extend(line.strip().split(','))  # Split kata kunci berdasarkan koma
    except FileNotFoundError:
        print(f"File {csv_filename} tidak ditemukan.")
    return keywords

# Contoh penggunaan
csv_filename = 'katakunci.csv'  # Ganti dengan nama file CSV yang sesuai
keywords = get_keywords_from_csv(csv_filename)
print("Kata kunci dari katakunci.csv:", keywords)


if __name__ == "__main__":
    main()
