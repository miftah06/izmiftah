import numpy as np  # Mengganti import pd dan import pandas as pd
import random

def generate_object_names(keywords_file, num_objects=100):
    # Membaca kata kunci dari file
    with open(keywords_file, 'r', encoding='utf-8') as file:
        keywords = file.read().splitlines()

    # Memastikan jumlah kata kunci cukup untuk menghasilkan objek
    if len(keywords) < 100:
        raise ValueError("Jumlah kata kunci harus minimal 100 untuk menghasilkan objek.")

    # Menghasilkan nama objek secara acak dan panjangnya diperpendek menjadi 100
    object_names = []
    for _ in range(num_objects):
        shortened_name = ' '.join(random.sample(keywords, 100))
        object_names.append(shortened_name)

    # Membuat DataFrame dengan nama objek
    data = {'Nama Objek Jawaban': object_names}
    df = np.array(data)  # Mengganti pd.DataFrame menjadi np.DataFrame

    return df

# Contoh penggunaan
keywords_file = 'katakunci.txt'  # Ganti dengan file yang berisi kata kunci
num_objects_to_generate = 10  # Ganti dengan jumlah objek yang ingin dihasilkan
generated_objects = generate_object_names(keywords_file, num_objects_to_generate)

# Menyimpan DataFrame ke file CSV
generated_objects.tofile('katakunci.csv')

print(f"{num_objects_to_generate} Nama objek telah disimpan ke dalam katakunci.csv")
