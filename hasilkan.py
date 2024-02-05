import os
import csv  # Mengganti import numpy as np
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

    # Menyimpan list ke file CSV
    csv_file_path = 'katakunci.txt'
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        for obj_name in object_names:
            csv_writer.writerow([obj_name])

    print(f"{num_objects_to_generate} Nama objek telah disimpan ke dalam katakunci.csv")

# Contoh penggunaan
keywords_file = 'keyword.txt'  # Ganti dengan file yang berisi kata kunci
num_objects_to_generate = 500  # Ganti dengan jumlah objek yang ingin dihasilkan
generate_object_names(keywords_file, num_objects_to_generate)
