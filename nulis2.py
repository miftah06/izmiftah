import random

# Daftar kata-kata yang dapat digunakan untuk membuat judul
judul_kata_kunci = ["Penelitian", "Studi", "Analisis", "Pengaruh", "Implementasi", "Evaluasi", "Pentingnya", "Manfaat", "Kualitas", "Sistem", "Pengembangan", "Pendekatan", "Peran", "Teknologi", "Strategi"]

# Fungsi untuk menghasilkan judul acak
def generate_random_judul():
    # Pilih beberapa kata acak dari daftar kata-kata kunci
    num_words = random.randint(2, 5)  # Misalnya, judul terdiri dari 2 hingga 5 kata
    random_words = random.sample(judul_kata_kunci, num_words)

    # Gabungkan kata-kata menjadi judul
    random_judul = " ".join(random_words)

    return random_judul

# Contoh penggunaan
random_judul = generate_random_judul()
print("Judul acak yang dihasilkan:", random_judul)
import csv

def get_keywords_from_csv(csv_filename):
    keywords = []
    try:
        with open(csv_filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                keywords.extend(row)  # Menambahkan kata kunci dari setiap baris
    except FileNotFoundError:
        print(f"File {csv_filename} tidak ditemukan.")
    return keywords

# Contoh penggunaan
csv_filename = 'katakunci.csv'  # Ganti dengan nama file CSV yang sesuai
keywords = get_keywords_from_csv(csv_filename)
print("Kata kunci dari katakunci.csv:", keywords)
