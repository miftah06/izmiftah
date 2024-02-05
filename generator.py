import os
import csv  # Mengganti import numpy as np
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

    # Membuat list dari nama objek
    data = {'Nama Objek Jawaban': object_names}

    # Menyimpan list ke file CSV
    csv_file_path = 'katakunci.csv'
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Nama Objek Jawaban']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for obj_name in object_names:
            writer.writerow({'Nama Objek Jawaban': obj_name})

    print(f"{num_objects} Nama objek telah disimpan ke dalam katakunci.csv")

# Contoh penggunaan
keywords_file = 'katakunci.txt'  # Ganti dengan file yang berisi kata kunci
num_objects_to_generate = 10  # Ganti dengan jumlah objek yang ingin dihasilkan
generate_object_names(keywords_file, num_objects_to_generate)
