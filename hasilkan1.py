import random

# List dengan berbagai kalimat prompt
prompts = [
    "Buatlah skrip Python untuk menghitung jumlah kata dalam sebuah teks.",
    "Bagaimana cara mengonversi data dari tipe satu ke tipe lain dalam Python?",
    "Berikan penjelasan singkat tentang konsep pemrograman berorientasi objek.",
    "Tuliskan program Python sederhana untuk menghasilkan deret Fibonacci.",
    "Jelaskan perbedaan antara list dan tuple dalam Python.",
    "Apakah keuntungan menggunakan fungsi dalam pemrograman?",
    "Bagaimana cara mengakses elemen-elemen dalam sebuah dictionary di Python?",
    "Berikan penjelasan tentang penanganan kesalahan (error handling) dalam Python.",
    "Tuliskan program Python untuk mencari bilangan prima dalam rentang tertentu.",
    "Bagaimana cara menggunakan modul eksternal (external module) dalam Python?",
    "Apa perbedaan antara metode GET dan POST dalam protokol HTTP?",
    "Jelaskan konsep inheritance dalam pemrograman berorientasi objek.",
    "Tuliskan program Python yang menghitung rata-rata dari sebuah list.",
    "Bagaimana cara membaca dan menulis file teks dalam Python?",
    "Berikan penjelasan tentang virtual environment dalam Python.",
    "Apakah perbedaan antara == dan is dalam Python?",
    "Bagaimana cara mengatasi konflik merge dalam sistem kontrol versi Git?",
    "Jelaskan perbedaan antara linear search dan binary search.",
    "Tuliskan program Python untuk mengurutkan elemen-elemen dalam sebuah list.",
    "Bagaimana cara menggunakan regular expression (regex) dalam Python?",
    "Apa itu algoritma dan kenapa penting dalam pemrograman?",
    "Berikan penjelasan tentang konsep Big-O dalam analisis kinerja algoritma.",
    "Tuliskan program Python untuk menghitung faktorial dari suatu bilangan.",
    "Bagaimana cara menggabungkan dua list dalam Python?",
    "Jelaskan perbedaan antara stack dan queue.",
    "Apakah itu recursion dan bagaimana cara mengimplementasikannya dalam Python?",
    "Berikan penjelasan tentang konsep multithreading dalam pemrograman.",
    "Tuliskan program Python untuk menghasilkan pola segitiga.",
    "Bagaimana cara menangani eksepsi (exception) dalam Python?",
    "Jelaskan perbedaan antara mutable dan immutable objects dalam Python."
]

# Acak urutan kalimat-kalimat prompt
random.shuffle(prompts)

# Simpan kalimat-kalimat yang sudah diacak ke dalam file prompt.txt
with open("input.txt", "w") as file:
    for prompt in prompts:
        file.write(prompt + "\n")
