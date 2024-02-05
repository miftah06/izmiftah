import numpy as np
from bs4 import BeautifulSoup
from fpdf import FPDF

def validate_length(judul, skripsi):
    while len(judul.split()) != len(skripsi[0].split()):
        print("Panjang judul tulisan skripsi dan salah satu dari tulisan opsional harus sama.")
        judul = input("Masukkan judul: ")

    # Menerima input untuk setiap opsional
    opsional = []
    for i in range(4):
        prompt = f"Opsional {i + 1}: "
        input_opsional = input(f"Masukkan opsional {i + 1}: ")
        opsional.append(input_opsional)

    # Menambahkan input judul_karya dan jenis_karyatulis
    judul_karya = input("Masukkan judul karya: ")
    jenis_karyatulis = input("Masukkan jenis karya tulis: ")

    return judul, opsional, judul_karya, jenis_karyatulis

def bootstrap1():
    # Meminta input dari pengguna
    judul, opsional, judul_karya, jenis_karyatulis = validate_length("", [[] for _ in range(4)])

    logo = input("Masukkan nama file gambar logo: ")
    oleh = input("Masukkan nama pengarang: ")
    nim = input("Masukkan NIM: ")
    fakultas = input("Masukkan fakultas: ")
    universitas = input("Masukkan universitas: ")
    tahun = input("Masukkan tahun (contoh: 2024): ")

    # Membuat dictionary dari input
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

    # Simpan data ke dalam file Excel dengan NumPy
    output_excel_path = 'cover.xlsx'
    np.savez(output_excel_path, **data_dict)

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
    pdf.set_font("Times New Roman", size=12)

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
    data_dict = dict(np.load('cover.xlsx', allow_pickle=True))

    # Memanggil fungsi beauty_pdf dengan menyediakan data yang dibutuhkan
    beauty_pdf(data_dict)

    print("\nProses selesai. File PDF yang indah tersedia di beauty-cover.pdf.")

if __name__ == "__main__":
    main()
