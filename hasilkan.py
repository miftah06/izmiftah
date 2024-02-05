import numpy as np  # Mengganti import pd dan import pandas as pd
import random

def generate_object_names(keywords_file, num_objects=1000):
    # Membaca kata kunci dari file
    with open(keywords_file, 'r', encoding='utf-8') as file:
        keywords = file.read().splitlines()

    # Memastikan jumlah kata kunci cukup untuk menghasilkan objek
    if len(keywords) < 100:
        raise ValueError("Jumlah kata kunci harus minimal 100 untuk menghasilkan objek.")

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
    df = np.array(data)  # Mengganti pd.DataFrame menjadi np.DataFrame

    return df

# Contoh penggunaan
keywords_file = 'keyword.txt'  # Ganti dengan file yang berisi kata kunci
num_objects_to_generate = 500 # Ganti dengan jumlah objek yang ingin dihasilkan
generated_objects = generate_object_names(keywords_file, num_objects_to_generate)

# Menyimpan DataFrame ke file CSV
file = open('katakunci.txt', 'a').write(__s=' ')
generate_object_names(file)

print(f"{num_objects_to_generate} Nama objek telah disimpan ke dalam katakunci.csv")
