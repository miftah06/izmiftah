import itertools
import random

def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read().splitlines()
    return content

def generate_object_combinations(fitur_file, objek_file, num_combinations):
    fitur_keywords = read_file(fitur_file)
    objek_keywords = read_file(objek_file)

    # Menggabungkan kata kunci fitur dan objek
    combined_keywords = fitur_keywords + objek_keywords

    # Menghasilkan semua kombinasi kata objek
    object_combinations = list(itertools.product(combined_keywords, repeat=2))

    # Memilih sejumlah kombinasi sesuai dengan num_combinations
    selected_combinations = random.sample(object_combinations, num_combinations)

    return selected_combinations

def save_to_file(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        for item in data:
            file.write(f"{item[0]} {item[1]}\n")

if __name__ == "__main__":
    fitur_file_path = "fitur.txt"
    objek_file_path = "objek.txt"
    output_file_path = "keyword2.txt"
    num_combinations = 1000  # Ganti sesuai kebutuhan

    # Generate ribuan kata objek dari file fitur dan objek
    object_combinations = generate_object_combinations(fitur_file_path, objek_file_path, num_combinations)

    # Simpan kombinasi kata objek ke dalam file output
    save_to_file(output_file_path, object_combinations)

    print(f"Ribuan kata objek telah dihasilkan dan disimpan dalam {output_file_path}.")
