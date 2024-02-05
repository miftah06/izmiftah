import os
import numpy as np

def load_keywords():
    """Load keywords from katakunci.csv or get input from the user if the file is not present."""
    keywords_file = 'katakunci.csv'
    if os.path.exists(keywords_file):
        try:
            keywords_df = np.genfromtxt(keywords_file, delimiter=',', dtype='str')
            return keywords_df[:, 1].tolist()  # Assuming 'Nama Objek Jawaban' is in the second column
        except KeyError:
            print(f"'Nama Objek Jawaban' column not found in {keywords_file}.")
    else:
        print(f"File {keywords_file} not found. Please create the file with a 'Nama Objek Jawaban' column.")
    return []

def validate_length(judul, skripsi):
    while len(judul) != len(skripsi[0]):
        print("Panjang judul tulisan skripsi dan salah satu dari tulisan opsional harus sama.")
        judul ="Masukkan Bagan judul pada isi ex: \n A. Latar Belakang: "

    # Load keywords from katakunci.csv or get input from the user
    keywords = load_keywords()

    # Menerima input untuk setiap opsional
    opsional = []
    for i in range(15):  # Sesuaikan dengan jumlah opsional
        if i < len(keywords):
            input_opsional = keywords[i]
        else:
            prompt = f"Opsional berupa isi keterangan misal: ex: \n Berupa isi Rumusan Masalah \n1. Apa yang dixxx...? 1 \n atau materi dst.. {i + 1}: "
            input_opsional =prompt
        opsional.append(input_opsional)

    return judul, opsional

def validate_subjudul(judul, i):
    while not judul:
        print(f"Subjudul {i} tidak boleh kosong.")
        judul = "Subjudul isi di sini "
    return judul

def split_title_into_sections(judul):
    # Memecah judul menjadi bagian-bagian
    sections = judul.split('{')

    # Menghapus karakter tidak diinginkan
    sections = [section.replace('}', '') for section in sections]

    return sections

def bootstrap():
    # Meminta input dari pengguna
    bab ="Masukkan BAB misal' BAB II PEMBAHASAN: "
    halaman ="Masukkan opsional satu baris full isi halaman (ganti renderan halaman ke kesimpulan): "

    # Membuat DataFrame kosong
    data_dict = {
        'Bab': [],
        'Logo': [],
    }

    for j in range(15):
        data_dict[f'Opsional {j + 1}'] = []
        data_dict[f'Subjudul {j + 1}'] = []

    i = 1
    while True:
        # Meminta input dari pengguna untuk subjudul dan opsional
        subjudul, opsional = validate_length("", [[] for _ in range(15)])  # Menyesuaikan dengan perubahan dalam validate_length
        subjudul = validate_subjudul(subjudul, i)

        # Memecah judul menjadi bagian-bagian
        subjudul_sections = split_title_into_sections(subjudul)

        # Menambahkan data ke dalam DataFrame
        data_dict['Bab'].append(bab)
        data_dict['Logo'].append(halaman)

        for j in range(15):
            data_dict[f'Opsional {j + 1}'].append(opsional[j])
            if j < len(subjudul_sections):
                data_dict[f'Subjudul {j + 1}'].append(subjudul_sections[j])
            else:
                data_dict[f'Subjudul {j + 1}'].append('')  # Mengisi dengan string kosong jika tidak ada subjudul

        i += 1

        # Mengecek apakah pengguna ingin melanjutkan atau tidak
        lanjut ="Apakah ingin menambahkan subjudul lagi? (y/n): ".lower()
        if lanjut != 'y':
            break

    # Membuat DataFrame dari input
    df = pd.DataFrame(data_dict)

    # Menyimpan DataFrame ke file Excel
    with pd.ExcelWriter('auto.xlsx', engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

if __name__ == "__main__":
    bootstrap()
