def create_prompt(input_file, output_file):
    # Baca keyword dari file input
    with open(input_file, 'r') as file:
        keywords = file.read().splitlines()

    # Buat prompt AI dari keyword
    prompt = " ".join(keywords)

    # Tulis prompt ke file output dengan new line untuk setiap kata
    with open(output_file, 'w') as file:
        file.write("\n".join(keywords))

def sort_elements(input_list):
    try:
        # Urutkan elemen-elemen dalam list
        sorted_list = sorted(input_list)

        # Hapus elemen-elemen yang bernilai False
        sorted_list = [elem for elem in sorted_list if elem is not False]

        return sorted_list
    except Exception as e:
        return f"Error: {str(e)}"

# Contoh penggunaan fungsi sort_elements
input_list = [4, 2, 7, False, 1, True, 5, False, 3]
sorted_result = sort_elements(input_list)
print("Sorted Result:", sorted_result)

# Contoh penggunaan fungsi create_prompt
input_file = "output.txt"
output_file = "hasil.txt"
create_prompt(input_file, output_file)
print(f"Prompt telah dibuat dan disimpan dalam file {output_file}.")
