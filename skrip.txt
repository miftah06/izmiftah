import random
import keyword

def generate_keyword_file(filename, num_keywords):
    keyword_list = keyword.kwlist
    num_keywords = min(num_keywords, len(keyword_list))

    random_keywords = random.sample(keyword_list, num_keywords)

    with open(filename, "w") as file:
        file.write("\n".join(random_keywords))

def create_prompt(input_file1, input_file2, output_file, command_option, specification_option, prompt_type, additional_input=None):
    with open(input_file1, "r") as objek_file:
        object_options = objek_file.readlines()

    with open(input_file2, "r") as fitur_file:
        features_options = fitur_file.readlines()

    with open("keyword1.txt", "r") as key1_file:
        key1_options = key1_file.readlines()

    with open("keyword2.txt", "r") as key2_file:
        key2_options = key2_file.readlines()

    with open("skrip.txt", "r") as skrip_file:
        skrip_options = skrip_file.readlines()

    with open(output_file, "w") as file:
        dan = key1_options
        jika = key2_options
        skrip = skrip_options
        for prompt in processed_data:
            object_option = random.choice(object_options).strip()
            features_option = random.choice(features_options).strip()
            key1_option = random.choice(key1_options).strip()
            key1_option = random.choice(dan).strip()
            skrip_option = random.choice(skrip).strip()

            if prompt_type == "text":
                output_line = f"\n\n\n HASIL OUTPUTNYA : \n\n\n {command_option} {specification_option} serta {object_option} \n\n dengan tambahan fungsi {object_options} \n\n adapun jika isinya berupa {skrip} {key1_option} \n\n\n\n dengan skrip: \n\n {skrip_option} {specification_option}\n\n\n"
            elif prompt_type == "image":
                output_line = f"Generate image with command: \n\n\n {command_option}, dengan latar elegant dengan penuh estetika nuansa {specification_option} bertemakan {key1_option} dengan warna {object_option} \n\n\n"
            elif prompt_type == "script":
                output_line = f"Execute script: \n\n\n {command_option} {specification_option} dan serta {prompt} jika hal tersebut berupa  \n {skrip_options} \n dengan {object_option} \n\n di dalam skrip {skrip} {key1_option} \n\n dengan module atau plugin tambahan {skrip_option}{features_option} \n\n\n {specification_option}\n\n\n\n"
            elif prompt_type == "soal":
                soal = additional_input
                output_line = f"Prompt jawab soalnya \n\n\n {command_option} {specification_option} dan jawablah jika soalnya:  \n {skrip_options} \n tanpa {object_option} \n\n maka tolong jawab {skrip} {key1_option} \n\n dengan menjelaskan {skrip_option}{features_option} \n\n\n {specification_option} secara rinci \n\n sebanyak {soal} soal \n\n"
            elif prompt_type == "cerita":
                paragraf = additional_input
                output_line = f"Prompt ceritanya: \n\n\n {command_option} {specification_option} dan buatlah momen lucu setelah terjadi kejadian berupa  \n\n {skrip_options} \n\n\n dan buatlah ceritanya dengan penuh drama dan lelucon keharmonisan \n\n dan jangan lupa buat ulang dengan tema: \n {key1_option} \n\n dengan menambahkan tambahkan {skrip_option} \n {specification_option} di dalam ceritanya \n\n sebanyak {paragraf} paragraf \n\n"
            else:
                output_line = "Invalid prompt type\n masukkan opsi\n 1.image, \n 2.text atau \n 3.script \n"

            file.write(output_line)

def read_and_write_file(input_filename, output_filename):
    with open(input_filename, "r") as input_file:
        input_data = input_file.readlines()

    # Lakukan sesuatu dengan data yang dibaca

    with open(output_filename, "w") as output_file:
        # Lakukan sesuatu dengan data dan tulis ke file keluaran
        output_file.write("Contoh hasil tulisan ke file teks.")

# Generate keyword1.txt dengan 50 kata kunci acak dari modul keyword
generate_keyword_file("fitur.txt", 500)

# Generate keyword2.txt dengan 50 kata kunci acak dari modul keyword
generate_keyword_file("objek.txt", 500)

print("Keyword telah dihasilkan dan disimpan dalam fitur.txt dan objek.txt.")

# Baca jenis prompt dari pengguna
prompt_type = input("Masukkan jenis prompt (text/image/script/soal/cerita): ")

# Baca isi input.txt dan acak urutannya
with open("input.txt", "r") as file:
    input_data = file.readlines()
    random.shuffle(input_data)

# Opsi pengguna untuk perintah dan spesifikasi
command_option = input("Masukkan opsi perintah: ")
specification_option = input("Masukkan opsi spesifikasi: ")

# Baca tambahan input untuk prompt jenis soal atau cerita
additional_input = None
if prompt_type in ["soal", "cerita"]:
    additional_input = input("Masukkan jumlah jawaban/soal (untuk soal) atau jumlah paragraf (untuk cerita): ")

# Proses input sesuai dengan opsi yang diberikan
processed_data = [line.strip() for line in input_data]

# Membuat AI prompt dengan input dari dua file kata kunci
create_prompt("keyword1.txt", "keyword2.txt", "output.txt", command_option, specification_option, prompt_type, additional_input)

print("Output telah dibuat dan disimpan dalam output.txt.")
