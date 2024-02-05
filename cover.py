import os
import pandas as pd
from bs4 import BeautifulSoup
from fpdf import FPDF

def validate_length(judul, skripsi):
    while len(judul) != len(skripsi[0]):
        print("Panjang judul tulisan skripsi dan salah satu dari tulisan opsional harus sama.")
        judul = "Masukkan judul"

    # Menerima input untuk setiap opsional
    opsional = []
    for i in range(4):
        prompt = f"Opsional berupa keterangan misal: ex: \n 1.Diajukan untuk bla bla,\n 2. Pada program studi xxx, \n 3. untuk xxx \n 4. ujian fakultas xxx...\n dengan jumlah kata yang harus sama ya! \n  {i + 1}: "
        input_opsional = "isi dengan opsional data"
        opsional.append(input_opsional)

    # Menambahkan input judul_karya dan jenis_karyatulis
    judul_karya = "Masukkan judul karya"
    jenis_karyatulis = "Masukkan jenis karya tulis"

    return judul, opsional, judul_karya, jenis_karyatulis

def bootstrap1():
    # Meminta input dari pengguna
    judul, opsional, judul_karya, jenis_karyatulis = validate_length("", [[] for _ in range(4)])  # Menyesuaikan dengan perubahan dalam validate_length
    logo = "cover.png"

    oleh = "Masukkan nama"
    nim = "Masukkan NIM"
    fakultas = "Masukkan fakultas"
    universitas = "Masukkan universitas"
    tahun = "Masukkan tahun (contoh: 2024)"

    # Membuat DataFrame dari input
    data_dict = {
        'Logo': [logo],
        'Opsional 1': [opsional[0]],
        'Opsional 2': [opsional[1]],
        'Opsional 3': [opsional[2]],
        'Opsional 4': [opsional[3]],
        'Oleh': [oleh],
        'NIM': [nim],
        'Fakultas': [fakultas],
        'Universitas': [universitas],
        'Tahun': [tahun],
        'Judul_karya': [judul_karya],
        'Jenis_karyatulis': [jenis_karyatulis]
    }

    with pd.ExcelWriter('cover.xlsx', engine='xlsxwriter') as writer:
        pd.DataFrame(data_dict).to_excel(writer, index=False, sheet_name='Sheet1')

def generate_html(data):
    # Template HTML dengan Bootstrap dan W3Schools builder
    template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{data['Judul_karya'][0]}</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
        <style>
            body {{
                margin: 4%;
            }}
            .container {{
                margin: auto;
                width: 80%;
                text-align: center;
            }}
            .img-fluid {{
                max-width: 100%;
                height: auto;
            }}
            .bold {{
                font-weight: bold;
            }}
            .underline {{
                text-decoration: underline;
            }}
            .newline {{
                margin-bottom: 0.2em;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="bold">{data['Judul_karya'][0]}</h1>
            <div>
                <img src="{data['Logo'][0]}" alt="Logo" class="img-fluid">
            </div>
            <p class="bold newline">{data['Jenis_karyatulis'][0]}</p>
            <p class="bold">{data['Opsional 1'][0]}</p>
            <p class="bold">{data['Opsional 2'][0]}</p>
            <p class="bold">{data['Opsional 3'][0]}</p>
            <p class="bold">{data['Opsional 4'][0]}</p>
            <p class="bold underline newline">Oleh: </p>
            <p class="bold newline> {data['Oleh'][0]}</p>
            <p class="bold newline">{data['NIM'][0]}</p>
            <p class="bold newline">{data['Fakultas'][0]}</p>
            <p class="bold newline">{data['Universitas'][0]}</p>
            <p class="bold newline">{data['Tahun'][0]}</p>
        </div>
    </body>
    </html>
    """

    # Hapus ". nan." dari teks
    template = template.replace(". nan.", "")

    return template

def beauty_pdf(data):
    # Membuat file HTML dari data
    html_content = generate_html(data)

    # Menyimpan HTML ke dalam file
    with open('cover.html', 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

    # Convert HTML ke PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Membaca HTML dan menambahkannya ke PDF
    with open('cover.html', 'r', encoding='utf-8') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')
        for tag in soup.find_all(['p', 'h1', 'h2']):
            pdf.multi_cell(0, 10, tag.text)

    # Simpan PDF
    pdf.output('beauty-cover.pdf')

def main():
    print("Selamat datang!\n untuk judul kita batasi jadi 8 kalimat \n dan tidak boleh berkereta api!")
    print("\n 1. Menjalankan skrip Bootstrap untuk membuat file Excel.\n")
    bootstrap1()

    print("\n2. Menjalankan skrip Beauty-PDF untuk membuat PDF yang indah.")
    # Membaca data dari file Excel
    data = pd.read_excel('cover.xlsx').to_dict(orient='list')

    # Memanggil fungsi beauty_pdf dengan menyediakan data yang dibutuhkan
    beauty_pdf(data)

    print("\nProses selesai. File PDF yang indah tersedia di beauty-cover.pdf.")

if __name__ == "__main__":
    main()

