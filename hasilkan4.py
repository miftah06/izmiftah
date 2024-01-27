import keyword
import random

def generate_dynamic_features(num_features):
    dynamic_features = []

    # Mendapatkan kata kunci dari modul keyword
    keyword_list = keyword.kwlist

    # Menghasilkan kombinasi kata kunci baru
    for _ in range(num_features):
        feature = random.choice(keyword_list) + random.choice(keyword_list)
        dynamic_features.append(feature)

    return dynamic_features

def save_to_file(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(data))

if __name__ == "__main__":
    num_dynamic_features = 1000  # Ganti sesuai kebutuhan

    # Generate fitur baru secara dinamis
    dynamic_features = generate_dynamic_features(num_dynamic_features)

    # Simpan fitur baru ke dalam file fitur.txt
    save_to_file("keyword1.txt", dynamic_features)

    print("Fitur baru telah dihasilkan dan disimpan dalam keyword1.txt.")
