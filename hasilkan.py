import pandas as pd
import random
from weasyprint import HTML

def generate_object_names(keywords_file, num_objects=1000):
    # Membaca kata kunci dari file
    with open(keywords_file, 'r', encoding='utf-8') as file:
        keywords = file.read().splitlines()

    # Memastikan jumlah kata kunci cukup untuk menghasilkan objek
    if len(keywords) < 10:
        raise ValueError("Jumlah kata kunci harus minimal 10 untuk menghasilkan objek.")

    # Menghasilkan nama objek secara acak dan panjangnya diperpanjang menjadi 10x
    object_names = []
    for _ in range(num_objects):
        extended_name = []
        for _ in range(100):
            word = random.choice(keywords)
            if word not in extended_name:
                extended_name.append(word)
        object_name = ' '.join(extended_name)
        object_names.append(object_name)

    # Membuat DataFrame dengan nama objek
    data = {'Nama Objek Jawaban': object_names}
    df = pd.DataFrame(data)

    return df

def save_as_pdf(dataframe, output_pdf):
    # Membuat file HTML sementara dari DataFrame
    html_filename = 'temp.html'
    dataframe.to_html(html_filename, index=False)

    # Mengonversi file HTML ke PDF menggunakan WeasyPrint
    HTML(string=open(html_filename, 'r', encoding='utf-8').read()).write_pdf(output_pdf)

    print(f"PDF telah disimpan sebagai {output_pdf}")

# Contoh penggunaan
keywords_file = 'keyword.txt'  # Ganti dengan file yang berisi kata kunci
num_objects_to_generate = 500 # Ganti dengan jumlah objek yang ingin dihasilkan
generated_objects = generate_object_names(keywords_file)

# Menyimpan DataFrame ke file CSV
generated_objects.to_csv('katakunci.txt', index=False)

# Menghasilkan PDF dari DataFrame
output_pdf = 'output.pdf'  # Ganti dengan nama file PDF yang diinginkan
save_as_pdf(generated_objects, output_pdf)
