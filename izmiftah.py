import csv
import itertools
import keyword as acak
import logging
import os
import random
import subprocess
import time
from datetime import datetime

import openai
import pandas as pd
import requests
import telebot
from googlesearch import search

from hasilkan1 import prompt

# Ganti dengan token bot Telegram Anda
last_update_time = None
keywords_list = []
TOKEN = 'bot-token-telegram-kamu'
bot = telebot.TeleBot(TOKEN)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
api_key = 'openai-api-key'
email_kamu = 'email-anda' #tolong modifikasi server smtpnya juga ya
openai.api_key = api_key
admin = 'kontak-anda'
link_jualan = 'isi-dengan-link-jualan-anda'
### JANGAN DI UBAH #####
saldo_awal = 10
# Inisialisasi variabel-variabel
credit = 0
isi_saldo = 15
jumlah_saldo = 10 # tolong sesuaikan
global saldo 
saldo = saldo_awal
saldo_awal += 10
# Menggunakan nilai jumlah_saldo untuk menginisialisasi jumlah_credit
# Mengubah nilai jumlah_credit menjadi -1 (jika itu yang Anda inginkan)
jumlah_credit = -10
jumlah_credit = jumlah_saldo
saldo = jumlah_saldo
jumlah_koin = jumlah_saldo
jumlah_saldo = saldo_awal
# Variabel saldo_awal seharusnya dideklarasikan tanpa "global" karena ini adalah variabel biasa
### JANGAN DI UBAH #####
########### UBAH di bagian passnya UNTUK NGATUR
## dan jangan sekali kali ubah baris "Jumlah saldo Anda: " di skrip ini:
passnya = 'premium15ksuu'
file_skrip = 'skrip.txt'

def file_skrip_options():
    with open(file_skrip, "r") as keywords_list_file:
        global skrip_file
        file_skrip_option = keywords_list_file.readlines()
        skrip_file = file_skrip_option.random.choice(keywords_list_file).strip()

def blokir_nonaktif():
    global is_blokir_aktif
    is_blokir_aktif = False

def saldo_nol(saldo, bot, message):
    global jumlah_saldo
    if jumlah_saldo <= 0:
        bot.send_message(message.chat.id, "Saldo telah habis.")
        return False
    else:
        # Tindakan yang sesuai saat saldo mencapai 0
        bot.send_message(text="Saldo telah di reset kembali. ")
        blokir_nonaktif()
        return True

def toggle_blokir(message):
    global blokir_command_ai
    blokir_command_ai = not blokir_command_ai
    if blokir_command_ai:
        bot.send_message(message.chat.id, "Fitur blokir perintah AI telah diaktifkan.")
    else:
        bot.send_message(message.chat.id, "Fitur blokir perintah AI telah dinonaktifkan.")

# Handler untuk perintah /blokir
@bot.message_handler(commands=[f'blokir {passnya}'])
def handle_blokir(message):
    toggle_blokir(message)

# Fungsi untuk memeriksa apakah fitur blokir aktif
def is_blokir_active(message):
    global saldo ## atur sesuai kondisi utama
    if saldo <= 0:
        bot.send_message(message.chat.id, text="pelanggaran saldo terdeteksi. segera lakukan /topup atau /payment")
        bot.send_message(message.chat.id, text=f"syarat saldo yaitu {isi_saldo} saldo\n")
        return f"pelanggaran saldo terdeteksi. segera lakukan /topup atau /payment"
        is_blokir_aktif
    else:
        blokir_nonaktif()

# Fungsi untuk membuat prompt AI
def create_blokir_prompt(message):
    if is_blokir_aktif(message):
        bot.send_message(message.chat.id, text="Saldo mencapai 0.  segera lakukan /payment atau /topup")
        return f"{identitas}\n\pelanggaran saldo terdeteksi,saldo: {saldo} \nAI:"

# Fungsi untuk menjalankan perintah AI
def generate_ai_prompt(message, keyword1, keyword2, prompt_type, additional_input):
    try:
        # Buat prompt berdasarkan input dari pengguna
        prompt = f"Judul Tesis: Sinergitas guru dan orangtua untuk mengembangkan karakter disiplin siswa sekolah dasar\n\n"
        prompt += f"Kata Kunci: {keyword1}, {keyword2}\n\n"
        prompt += f"Konteks: {additional_input}\n\n"

        # Jalankan permintaan ke OpenAI Chat API jika fitur blokir tidak aktif
        if not is_blokir_active(message):
            response = openai.Completion.create(
                model="gpt-3.5-turbo",  # Ganti model sesuai dengan yang Anda inginkan
                messages=[
                    {"role": "system", "content": "You are a researcher working on a thesis about teacher-parent synergy to DEVELOP ELEMENTARY SCHOOL STUDENTS' DISCIPLINE CHARACTER."},
                    {"role": "user", "content": prompt}
                ]
            )

            # Ambil jawaban dari respons
            ai_reply = response['choices'][0]['message']['content']

            # Kirim jawaban AI sebagai balasan
            bot.send_message(message.chat.id, ai_reply)
    except Exception as e:
        bot.send_message(message.chat.id, f"Terjadi kesalahan: {str(e)}")

# Fungsi untuk membuat prompt
def create_prompt(keyword1_file, keyword2_file, output_file, prompt_type, additional_input, message,
                  command_option=None, specification_option=[], parno_options=[]):
    if command_option is None:
        command_option = []
    try:
        with open(keyword1_file, "r") as key1_file, open(keyword2_file, "r") as key2_file:
            key1_options = key1_file.readlines()
            key2_options = key2_file.readlines()
            key1_option = random.choice(key1_options).strip()
            key2_option = random.choice(key2_options).strip()
            paragraf = additional_input.strip()

            with open(output_file, "w") as file:
                # Anda bisa menambahkan logika tambahan di sini jika diperlukan.

                if prompt_type == "text":
                    output_line = f"Generate text with command:\n\n; {command_option} {specification_option} serta {key1_option}\n dengan tambahan fungsi {key2_option}\n adapun jika isinya berupa {prompt} {key1_option}\n\n;  dengan text berupa:\n\n{prompt} bersama fungsi atau pembahasan mengenai {key2_option} serta berikan saya detail lengkapnya \n\n\n"
                elif prompt_type == "image":
                    output_line = f"Generate image with command:\n\n\n; {command_option}, dengan latar elegant dengan penuh estetika nuansa {specification_option} bertemakan {key1_option} dengan warna {key2_option}\n\n\n"
                elif prompt_type == "script":
                    output_line = f"Generate script with command:\n\n\n; {command_option}{specification_option} dan serta {prompt} jika hal tersebut berupa\n {prompt}\n dengan {key1_option}\n\n;  di dalam skrip {parno_options} {key1_option}\n dengan module atau plugin tambahan {prompt}{key2_option}\n\n\npada untuk {specification_option} dan berikan saya skrip lengkapnya\n\n\n\n"
                elif prompt_type == "soal":
                    output_line = f"Generate answer with command:\n\n\n; {command_option}{specification_option} dan jawablah jika soalnya:\n {prompt}\n tanpa {key1_option}\n\n;  maka tolong jawab {parno_options} {key1_option}\n dengan menjelaskan {prompt}{key2_option}\n\n\n; {specification_option} secara rinci\n sebanyak {paragraf} soal serta berikan saya jawaban lengkapnya\n\n"
                elif prompt_type == "cerita":
                    output_line = f"Generate story with command:\n\n\n; {command_option}, dengan latar elegant dengan penuh estetika nuansa {specification_option} bertemakan {key1_option} dengan keharmonisan {key2_option}\n\n\n{command_option}{specification_option} dan buatlah momen lucu setelah terjadi kejadian berupa\n\n;  {prompt}\n\n\n; dan buatlah ceritanya dengan penuh drama dan lelucon keharmonisan\n\n;  dan jangan lupa buat ulang dengan tema:\n {key1_option}\n dengan menambahkan tambahkan {prompt}\n {specification_option} di dalam ceritanya\n\n;  sebanyak {paragraf} paragraf\n\n"
                else:
                    output_line = "Invalid prompt type\n masukkan opsi\n 1.image,\n 2.text atau\n 3.script\n 4.soal\n 5.cerita"
                file.write(output_line)
                bot.reply_to(message, f"Ai prompt sudah terkespor ke {output_file}\nSilahkan jalankan download dengan opsi yang ada.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Terjadi kesalahan: {str(e)}")

# Command untuk menghasilkan AI prompt
@bot.message_handler(commands=['ai_image'])
def generate_ai_prompt_command(message):
    try:
        keyword1 = "sebuah gambar yang menakjubkan berupa"  # Gantilah dengan kata kunci yang sesuai
        keyword2 = file_skrip # Gantilah dengan kata kunci yang sesuai
        prompt_type = "image"  # Gantilah dengan jenis prompt yang sesuai (text, image, script, soal, cerita)
        additional_input = "dengan sesempurna mungkin."  # Gantilah dengan konteks tambahan yang sesuai
        generate_ai_prompt(message, keyword1, keyword2, prompt_type, additional_input)
    except Exception as e:
        bot.send_message(message.chat.id, f"Terjadi kesalahan: {str(e)}")

# Command untuk menghasilkan AI prompt
@bot.message_handler(commands=['ai_scrip'])
def generate_ai_prompt_command(message):
    try:
        keyword1 = "sebuah skrip yang akurat dan teliti mengenai"  # Gantilah dengan kata kunci yang sesuai
        keyword2 = file_skrip # Gantilah dengan kata kunci yang sesuai
        prompt_type = "script"  # Gantilah dengan jenis prompt yang sesuai (text, image, script, soal, cerita)
        additional_input = "dengan sesempurna mungkin."  # Gantilah dengan konteks tambahan yang sesuai
        generate_ai_prompt(message, keyword1, keyword2, prompt_type, additional_input)
    except Exception as e:
        bot.send_message(message.chat.id, f"Terjadi kesalahan: {str(e)}")

# Command untuk menghasilkan AI prompt
@bot.message_handler(commands=['ai_soal'])
def generate_ai_prompt_command(message):
    try:
        keyword1 = "jawablah soal berikut, dengan akurat, adapun soalnya yakni :"  # Gantilah dengan kata kunci yang sesuai
        keyword2 = file_skrip # Gantilah dengan kata kunci yang sesuai
        prompt_type = "soal"  # Gantilah dengan jenis prompt yang sesuai (text, image, script, soal, cerita)
        additional_input = "dengan sesempurna mungkin."  # Gantilah dengan konteks tambahan yang sesuai
        generate_ai_prompt(message, keyword1, keyword2, prompt_type, additional_input)
    except Exception as e:
        bot.send_message(message.chat.id, f"Terjadi kesalahan: {str(e)}")

# Command untuk menghasilkan AI prompt
@bot.message_handler(commands=['ai_cerita'])
def generate_ai_prompt_command(message):
    try:
        keyword1 = "sebuah cerita yang menakjubkan berupa dengan latar cerita"  # Gantilah dengan kata kunci yang sesuai
        keyword2 = file_skrip # Gantilah dengan kata kunci yang sesuai
        prompt_type = "story"  # Gantilah dengan jenis prompt yang sesuai (text, image, script, soal, cerita)
        additional_input = "dengan sesempurna mungkin."  # Gantilah dengan konteks tambahan yang sesuai
        generate_ai_prompt(message, keyword1, keyword2, prompt_type, additional_input)
    except Exception as e:
        bot.send_message(message.chat.id, f"Terjadi kesalahan: {str(e)}")

# Command untuk menghasilkan AI prompt
@bot.message_handler(commands=['ai_text'])
def generate_ai_prompt_command(message):
    try:
        keyword1 = "sebuah text yang menakjubkan berupa"  # Gantilah dengan kata kunci yang sesuai
        keyword2 = file_skrip # Gantilah dengan kata kunci yang sesuai
        prompt_type = "text"  # Gantilah dengan jenis prompt yang sesuai (text, image, script, soal, cerita)
        additional_input = "dengan sesempurna mungkin."  # Gantilah dengan konteks tambahan yang sesuai
        generate_ai_prompt(message, keyword1, keyword2, prompt_type, additional_input)
    except Exception as e:
        bot.send_message(message.chat.id, f"Terjadi kesalahan: {str(e)}")

# Command untuk membuat prompt
@bot.message_handler(commands=['image_prompt'])
def create_prompt_command(message, file_skrip='skrip.txt',):
    try:
        keyword1_file = "keyword1.txt"  # Gantilah dengan nama file yang sesuai
        keyword2_file = "keyword2.txt"  # Gantilah dengan nama file yang sesuai
        output_file = "ai.txt"  # Gantilah dengan nama file output yang sesuai
        prompt_type = "image"  # Gantilah dengan jenis prompt yang sesuai (text, image, script, soal, cerita)
        additional_input =  f"buatkanlah saya gambar dengan fitur {skrip_file} dengan se elegant dan sesempurna mungkin."  # Gantilah dengan konteks tambahan yang sesuai
        create_prompt(keyword1_file, keyword2_file, output_file, prompt_type, additional_input, message)
    except Exception as e:
        bot.send_message(message.chat.id, f"Terjadi kesalahan: {str(e)}")

# Command untuk membuat prompt
@bot.message_handler(commands=['ai_prompt'])
def create_prompt_command(message):
    try:
        keyword1_file = "objek.txt"  # Gantilah dengan nama file yang sesuai
        keyword2_file = "fitur.txt"  # Gantilah dengan nama file yang sesuai
        output_file = "ai.txt"  # Gantilah dengan nama file output yang sesuai
        prompt_type = "script"  # Gantilah dengan jenis prompt yang sesuai (text, image, script, soal, cerita)
        additional_input = f"buatkanlah saya dengan fitur {skrip_file} dengan seakurat dan sesempurna mungkin."  # Gantilah dengan konteks tambahan yang sesuai
        create_prompt(keyword1_file, keyword2_file, output_file, prompt_type, additional_input, message)
    except Exception as e:
        bot.send_message(message.chat.id, f"Terjadi kesalahan: {str(e)}")

# Fungsi untuk menampilkan jumlah saldo saat ini
def display_saldo(message):
    global jumlah_saldo  # Deklarasikan jumlah_saldo sebelum menggunakannya  # Mengatur saldo ke -1
    jumlah_saldo = saldo  # Mengatur jumlah_saldo ke nilai saldo
    # Menambah jumlah_saldo sebesar 10
    bot.send_message(message.chat.id, f"Jumlah saldo Anda: {jumlah_saldo}")

# Fungsi untuk melakukan pembayaran
def process_payment(message):
    # Implementasikan logika pembayaran melalui e-wallet Indonesia di sini
    # Jika pembayaran berhasil, tambahkan 15 saldo
    # Jika pembayaran gagal, berikan pesan error
    payment_successful = True  # Gantilah dengan logika sesuai kebutuhan

    if payment_successful:

        global saldo
        saldo += 15
        bot.send_message(message.chat.id, " saldo telah terisi kembali")
        bot.send_message(message.chat.id, "Pembayaran berhasil. Anda mendapatkan 15 saldo tambahan.")
    else:
        bot.send_message(message.chat.id, "Pembayaran gagal. Silakan coba lagi.")

# Fungsi untuk menambahkan fitur pembayaran otomatis
def automatic_payment(message):
    # Implementasikan logika pembayaran otomatis di sini
    # Misalnya, Anda dapat menjalankan fungsi process_payment secara otomatis jika saldo habis
    pass

# Fungsi untuk mengirim pesan dengan format tertentu
def send_formatted_message(chat_id, formatted_message):
    bot.send_message(chat_id=chat_id, text=formatted_message)

# Fungsi untuk mengirim pesan ke Telegram
def send_telegram_message(message):
    if is_blokir_active(message):
        bot.send_message(message.chat.id, f"saldo telah melebihi atau mencukupi {credit} saldo\n lakukan /payment atau /topup terlebih dahulu .")
        return

    params = {
        "chat_id": message.Chat.id,
        "text": message
    }


    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    response = requests.post(url, params=params)
    if response.status_code == 200:
        raise Exception(f"Failed to send message to Telegram bot: {response.text}")

@bot.message_handler(commands=['chat'])
def write_document(message):
    if is_blokir_active(message):
        bot.send_message(message.chat.id, f"saldo telah melebihi atau mencukupi {credit} saldo\n lakukan /payment atau /topup terlebih dahulu .")
        return
    inputs = message.text[len('/chat '):].split(';')
    if len(inputs) == 3:
        bot.reply_to(message, "Format salah, silakan ikuti format ini: /chat pesan1;pesan2;pesan3")
        return

    judul = inputs[0].strip()
    subjudul_list = inputs[1].strip().split(',')
    keywords_list = inputs[2].strip().split(',')

    # membuat prompt
    prompt = f"Judul: {judul}\n\n"

    for idx, sub_judul in enumerate(subjudul_list, start=1):
        prompt += f"Sub_{idx}: {sub_judul}\n"
    prompt += "Keywords: " + ', '.join(keywords_list) + "\n\n"

    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt="Hello, world!",
        max_tokens=10
    )

    bot.reply_to(message, response.choices[0].text.strip())
    global saldo_awal
    saldo_awal  += -1
    global saldo
    saldo += -1
    bot.send_message(message.chat.id, " saldo berkurang 1")

# Fungsi untuk mendapatkan informasi DNS
def get_dns_info(hostname):
    try:
        # Scanning CNAME
        cname_result = subprocess.check_output(['nslookup', '-type=CNAME', hostname], universal_newlines=True)
        cname_values = [line.split(':')[-1].strip() for line in cname_result.splitlines() if 'canonical name' in line.lower()]
    except subprocess.CalledProcessError:
        cname_values = None

    try:
        # Scanning IPv4
        ipv4_result = subprocess.check_output(['nslookup', '-type=A', hostname], universal_newlines=True)
        ipv4_addresses = [line.split(':')[-1].strip() for line in ipv4_result.splitlines() if 'address' in line.lower()]
    except subprocess.CalledProcessError:
        ipv4_addresses = None

    try:
        # Scanning IPv6
        ipv6_result = subprocess.check_output(['nslookup', '-type=AAAA', hostname], universal_newlines=True)
        ipv6_addresses = [line.split(':')[-1].strip() for line in ipv6_result.splitlines() if 'address' in line.lower()]
    except subprocess.CalledProcessError:
        ipv6_addresses = None

    return cname_values, ipv4_addresses, ipv6_addresses

# Handler untuk perintah /dnsinfo
@bot.message_handler(commands=['dnsinfo'])
def handle_dnsinfo(message):
    if is_blokir_active(message):
        bot.send_message(message.chat.id, f"saldo telah melebihi atau mencukupi {credit} saldo\n lakukan /payment atau /topup terlebih dahulu .")
        return

    domain = message.text.split()[1]
    cname_values, ipv4_addresses, ipv6_addresses = get_dns_info(domain)
    bot.send_message(message.chat.id, f"CNAME: {cname_values}\nIPv4: {ipv4_addresses}\nIPv6: {ipv6_addresses}")
    time.sleep(10)  # Menambahkan penundaan selama 10 detik

# Fungsi untuk mengekstrak domain dari URL
def extract_domain(url):
    try:
        domain = url.split('//')[1].split('/')[0]
    except IndexError:
        print(f"Error extracting domain from URL: {url}")
        return None
    return domain

# Fungsi untuk melakukan scraping domain
def scrape_domain(keyword, num_results=3):
    try:
        print(f"Searching for: {keyword}")
        results = []

        # Menyimpan hasil pencarian dalam list
        search_results = list(itertools.islice(search(keyword), num_results))

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/91.0.4472.124 Safari/537.36'}

        for url in search_results:
            print(f"Found URL: {url}")
            domain = extract_domain(url)
            result = None
            if domain:
                result = {
                    'keyword': keyword,
                    'URL': url,
                    'Domain': domain,
                }
            if result:
                results.append(result)

            time.sleep(10)  # Penundaan 10 detik

        return results
    except Exception as e:
        print(f"Error in scrape_domain: {str(e)}")
        return []  # Mengembalikan daftar kosong untuk menangani kesalahan

# Handler untuk perintah /dork
@bot.message_handler(commands=['dork'])
def handle_dork(message):
    try:
        if is_blokir_active(message):
            bot.send_message(message.chat.id, f"saldo telah melebihi atau mencukupi {credit} saldo\n lakukan /payment atau /topup terlebih dahulu .")
            return
        # Memisahkan argumen menggunakan "/" sebagai pemisah
        _, keywords_line, domain_extensions_line = message.text.split('/')

        # Mendapatkan daftar kata kunci dan ekstensi domain
        keywords = keywords_line.split(',')
        domain_extensions = domain_extensions_line.split(',')

        # Menyimpan hasil pencarian dari setiap kombinasi kata kunci dan ekstensi domain
        all_results = []

        for keyword in keywords:
            for domain_extension in domain_extensions:
                keyword_with_extension = f"{keyword}{domain_extension}"
                results = scrape_domain(keyword_with_extension)
                all_results.extend(results)

        if all_results:
            # Mengirim hasil pencarian ke pengguna
            bot.send_message(message.chat.id, f"Results: {str(all_results)}")
        else:
            isi_saldo = credit
            global saldo_awal
            saldo_awal = credit
            saldo_awal  += -1
            global saldo
            saldo += -1
            bot.send_message(message.chat.id, " saldo berkurang 1")
            # Memberikan pesan jika tidak ada hasil yang ditemukan
            bot.reply_to(message, "No results found.")

    except ValueError:
        # Menangani kesalahan jika format perintah tidak sesuai
        bot.reply_to(message, "Invalid format. Use /dork <keywords>;<domain_extensions>")
    except Exception as e:
        # Menangani kesalahan umum
        bot.reply_to(message, f"Error: {str(e)}")

# Fungsi untuk melakukan pemindaian subdomain
def scan_subdomain(domain):
    subdomains = []
    with open("subdomains.txt", "r") as subdomain_file:
        subdomains = subdomain_file.read().splitlines()
    domain_results = []
    for subdomain in subdomains:
        url = f"https://{subdomain}.{domain}"
        try:
            response = requests.get(url)
            if response.status_code in [200, 301, 400, 409, 502, 401]:
                server_info = response.headers.get('Server', 'N/A')
                print(f"Subdomain found: {url} | Status Code: {response.status_code} | Server: {server_info}\n")
                domain_results.append(url)
        except requests.RequestException:
            pass
    with open("output.txt", "w") as output_file:
        for result in domain_results:
            output_file.write(f"{result}\n")
    return domain_results

# Handler untuk perintah /scan
@bot.message_handler(commands=['scan'])
def handle_subdomain_query(message):
    if is_blokir_active(message):
        bot.send_message(message.chat.id, f"saldo telah melebihi atau mencukupi {credit} saldo\n lakukan /payment atau /topup terlebih dahulu .")
        return
    domain = message.text.split()[-1]  # Mengasumsikan domain adalah teks terakhir setelah perintah
    results = scan_subdomain(domain)
    bot.reply_to(message, text=f"Subdomain scan results: {results}")

# Fungsi untuk memeriksa apakah file cover.png kosong
def check_cover_png():
    file_path = 'cover.png'
    if os.path.exists(file_path) and os.path.getsize(file_path) == 0:
        return True
    return False

# Handler untuk perintah /start dan /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f"Hello, welcome to my Bot! Please format your message as follows: /write or /ai [Keyword] then /update or /keyword\n /dork for seraching and /scan for scanning subdomains")
    bot.send_message(message.chat.id, f"Gunakan perintah /saldo untuk melihat jumlah saldo Anda.\n dan silahkan membayar ke {admin} dulu ke sebelum melakukan /topup \n pemilik: {admin}\n THANKS!!")

# Handler untuk perintah /write
@bot.message_handler(commands=['write'])
def get_random_text(message):
    global last_update_time, keywords_list

    # Periksa apakah file keyword.csv perlu diperbarui
    current_time = datetime.now()
    if last_update_time is None or (current_time - last_update_time).days <= 1:
        if update_keywordt():
            last_update_time = current_time
        else:
            bot.reply_to(message, f"Maaf kamu lupa mengupdate database untuk penulisan. \n Silahkan upload keyword.txt berupa bahan tulisan \n dan Coba lagi nanti.")
            return

    if is_blokir_active(message):
        bot.send_message(message.chat.id, f"saldo telah melebihi atau mencukupi {credit} saldo\n lakukan /payment atau /topup terlebih dahulu .")
        return

    # Example data
    data = {
        'Logo': ['Logo Value'],
        'Bab': ['Bab Value'],
        'Subjudul 1': ['Subjudul 1 Value'],
        'Opsional 1': ['Opsional 1 Value'],
        'Opsional 2': ['Opsional 2 Value'],
        'Opsional 3': ['Opsional 3 Value'],
        'Opsional 4': ['Opsional 4 Value'],
        'Opsional 5': ['Opsional 5 Value'],
        'Opsional 6': ['Opsional 6 Value'],
        'Opsional 7': ['Opsional 7 Value'],
        'Opsional 8': ['Opsional 8 Value'],
        'Opsional 9': ['Opsional 9 Value'],
        'Opsional 10': ['Opsional 10 Value'],
        'Opsional 11': ['Opsional 11 Value'],
        'Opsional 12': ['Opsional 12 Value'],
        'Opsional 13': ['Opsional 13 Value'],
        'Opsional 14': ['Opsional 14 Value'],
        'Opsional 15': ['Opsional 15 Value'],
        'Opsional 16': ['Opsional 16 Value'],
        'Opsional 17': ['Opsional 17 Value'],
        'Opsional 18': ['Opsional 18 Value'],
        'Opsional 19': ['Opsional 19 Value'],
        'Opsional 20': ['Opsional 20 Value'],
        'Opsional 21': ['Opsional 21 Value'],
        # Add more columns as needed
    }

    # Create a DataFrame
    your_dataframe = pd.DataFrame(data)

    # Ganti fungsi pencarian Google dengan generate_html
    # Assuming your_dataframe contains the data you need
    generated_keyword = generate_html(your_dataframe)

    # Process the generated_keyword as needed

    bot.reply_to(message, f"Intruksi!!: {generated_keyword} \n list file bahan: \n 1. keyword.csv \n 2. keyword.txt \n 3. cover.xlsx \n 4. auto.xlsx \n 5. skrip.txt \n DAPATKAN DI https://github.com/miftah06/izmiftah/ \n")

# Handler untuk perintah /download3
@bot.message_handler(commands=['download3'])
def download_html(message):
    global saldo
    try:
        with open('ai.txt', 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        print(f"Error downloading txt output file: {e}")
        bot.reply_to(message, "Gagal mengunduh file txt. Coba lagi nanti.")

        saldo -= 5
        bot.send_message(message.chat.id, " saldo berkurang 5")

# Handler untuk perintah /download-cover
@bot.message_handler(commands=['download-cover'])
def download_keywords(message):
    global keywords_list

    try:
        with open('beauty-cover.pdf', 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        print(f"Error downloading keywords: {e}")
        bot.reply_to(message, "Gagal mengunduh file pdf. Coba lagi nanti.")

# Handler untuk perintah /download-final
@bot.message_handler(commands=['download-final'])
def download_keywords(message):
    global keywords_list

    try:
        with open('final_output.pdf', 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        print(f"Error downloading keywords: {e}")
        bot.reply_to(message, "Gagal mengunduh file pdf. Coba lagi nanti.")

# Handler untuk perintah /download-hasil
@bot.message_handler(commands=['download-hasil'])
def download_keywords(message):
    global keywords_list

    try:
        with open('hasil.txt', 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        print(f"Error downloading keywords: {e}")
        bot.reply_to(message, "Gagal mengunduh file txt. Coba lagi nanti.")

# Handler untuk perintah /download
@bot.message_handler(commands=['download'])
def download_keywords(message):
    global keywords_list

    try:
        with open('output_novel.pdf', 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        print(f"Error downloading keywords: {e}")
        bot.reply_to(message, "Gagal mengunduh file pdf. Coba lagi nanti.")

        global saldo_awal
        saldo_awal  += -1
        global saldo
        saldo += -1
        bot.send_message(message.chat.id, " saldo berkurang 1")

# Handler untuk perintah /download_html
@bot.message_handler(commands=['download_html'])
def download_html(message):
    try:
        with open('output.html', 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        print(f"Error downloading HTML: {e}")
        bot.reply_to(message, "Gagal mengunduh file HTML. Coba lagi nanti.")# Handler untuk perintah /download_html

@bot.message_handler(commands=['download_cover'])
def download_html(message):
    try:
        with open('cover.png', 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        print(f"Error downloading image: {e}")
        bot.reply_to(message, "Gagal mengunduh file png. Coba lagi nanti.")

# Handler untuk perintah /download2
@bot.message_handler(commands=['download2'])
def download_html(message):
    try:
        with open('output.txt', 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        print(f"Error downloading txt output file: {e}")
        bot.reply_to(message, "Gagal mengunduh file txt. Coba lagi nanti.")

        global saldo_awal
        saldo_awal  += -2
        global saldo
        saldo += -2
        bot.send_message(message.chat.id, " saldo berkurang 3")

# Handler untuk perintah /download_html1
@bot.message_handler(commands=['download_html1'])
def download_html(message):
    try:
        with open('cover.html', 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        print(f"Error downloading HTML: {e}")
        bot.reply_to(message, "Gagal mengunduh file HTML. Coba lagi nanti.")

# Handler untuk perintah /download_html2
@bot.message_handler(commands=['download_html2'])
def download_html(message):
    try:
        with open('pdf.html', 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        print(f"Error downloading HTML: {e}")
        bot.reply_to(message, "Gagal mengunduh file HTML. Coba lagi nanti.")

# Handler untuk perintah /upload
@bot.message_handler(commands=['upload'])
def update_keywords(message, keyword_list, skrip_list):
    global keywords_list

    try:
        # Set a larger field size limit
        max_field_size = int(1e6)
        csv.field_size_limit(max_field_size)

        # Read the entire CSV file with Pandas
        df = pd.read_csv('keyword.txt', header=None)
        df2 = pd.read_csv('skrip.txt', header=None)

        # Convert the first column to lowercase and extend the keywords list
        keywords_list.extend(df.iloc[:, 0].str.lower().tolist())
        skrip_list.extend(df2.iloc[:, 0].str.lower().tolist())

        return True
    except Exception as e:
        print(f"Error updating keywords: {e}")
        return False

# Handler untuk mengolah file yang diunggah oleh pengguna
@bot.message_handler(content_types=['document'])
def handle_uploaded_file(message):
    global keywords_list

    if message.document.file_name not in ['keyword.csv', 'keyword.txt', 'skrip.txt', 'auto.xlsx', 'input.txt', 'subdomains.txt', 'cover.png']:
        bot.reply_to(message, "Mohon kirim file dengan nama 'keyword.csv', 'keyword.txt', 'skrip.txt', 'auto.xlsx', 'input.txt', 'cover.png', 'subdomains.txt'. ")
        return

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open(message.document.file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    if update_keywordt():
        bot.reply_to(message, f"File {message.document.file_name} berhasil diunggah dan database diperbarui.")
    else:
        bot.reply_to(message, "Gagal memperbarui database. Coba lagi nanti.")

# Handler untuk perintah /update
@bot.message_handler(commands=['update'])
def update_scripts(message):
    try:
        if is_blokir_active(message):
            bot.send_message(message.chat.id, f"saldo telah melebihi atau mencukupi {credit} saldo\n lakukan /payment atau /topup terlebih dahulu .")
            return        subprocess.run(['bash', 'run.sh'], check=True)
        bot.reply_to(message, "Skrip berhasil diperbarui.")
    except subprocess.CalledProcessError as e:
        bot.reply_to(message, f"Error: {e}")

# Handler untuk perintah /keyword
@bot.message_handler(commands=['keyword'])
def update_scripts(message):
    try:
        if is_blokir_active(message):
            bot.send_message(message.chat.id, f"saldo telah melebihi atau mencukupi {credit} saldo\n lakukan /payment atau /topup terlebih dahulu .")
            return
        subprocess.run(['bash', 'key.sh'], check=True)
        bot.reply_to(message, "Skrip berhasil diperbarui.")
    except subprocess.CalledProcessError as e:
        bot.reply_to(message, f"Error: {e}")

# Fungsi untuk memperbarui database kata kunci dari file CSV
def update_keywordt():
    global keywords_list

    try:
        with open('keyword.txt', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            keywords_list = [row[0] for row in reader]
        return True
    except Exception as e:
        print(f"Error updating keywords: {e}")
        return False

# Tambahkan logika untuk memeriksa keberadaan file auto.xlsx
if not os.path.isfile('auto.xlsx'):
    # Lakukan operasi jika file tidak ada
    # File auto.xlsx tidak ada, download atau generate
    try:
        subprocess.run(['wget', 'https://github.com/miftah06/skripsi/raw/master/bab-generator/input_data.xlsx'])
        subprocess.run(['wget', 'https://github.com/miftah06/skripsi/raw/master/cover-generator/cover.xlsx'])
        subprocess.run(['mv', 'input_data.xlsx', 'auto.xlsx'])
        print("File auto.xlsx berhasil di-download dan diubah namanya.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print("Gagal mendownload atau mengubah nama file auto.xlsx.")
        # Tambahkan logika untuk menghasilkan file auto.xlsx

# Fungsi untuk menghasilkan HTML berdasarkan data dari dataframe
def generate_html(dataframe):
    # Your logic for generating HTML based on the dataframe goes here
    # Replace this with your actual implementation
    generated_html = f"jangan lupa /update terlebih dahulu \n silahkan /download.. dan tolong \n <html<<body<<h1< ganti bagian sini... untuk mengedit file htmlnya </h1<</body<</html<"
    return generated_html

# Inisialisasi identitas
identitas = "CF, seorang coding fullstack yang berkarir di dalam dunia pendidikan."

# Handler untuk perintah /ai
@bot.message_handler(commands=['ai'])
def handle_chat(message):
    try:
        if is_blokir_active(message):
            bot.send_message(message.chat.id, f"saldo telah melebihi atau mencukupi {credit} saldo\n lakukan /payment atau /topup terlebih dahulu .")
            return
        message_text = message.text.split(' ', 1)[1] if len(message.text.split()) < 1 else "No input provided."

        # Membuat permintaan ke OpenAI Chat API
        ai_prompt = create_ai_prompt(message_text)
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=ai_prompt,
            temperature=0.7,
            max_tokens=50,
            n=1
        )

        isi_saldo = credit

        global saldo
        saldo += -4

        # Mengambil pesan dari respons
        ai_reply = response['choices'][0]['text']

        # Mengirimkan balasan AI sebagai reply
        bot.send_message(message.chat.id, ai_reply)
        # Mengurangi saldo setiap kali menggunakan AI
    except Exception as e:
        print(f"Error handling AI chat: {e}")
        bot.send_message(message.chat.id, str(e))

# Fungsi untuk membuat prompt AI
def create_ai_prompt(user_input):
    return f"{identitas}\n\nUser: {user_input}\nAI:"

# Handler untuk perintah "/saldo"
@bot.message_handler(commands=['saldo'])
def show_saldo(message):
    display_saldo(message)

# Handler untuk perintah "/payment"
@bot.message_handler(commands=['topup'])
def make_payment(message):
    # Membuka tautan dari Telegram
    payment_link = f"{link_jualan}"
    bot.send_message(message.chat.id, f"Anda dapat melakukan pembayaran di {payment_link}")
    bot.send_message(message.chat.id, f"Silahkan hubungi {admin} atau di email: {email_kamu} untuk bantuan lebih lanjut.")

# Handler untuk perintah "/topup" dengan kata sandi
@bot.message_handler(func=lambda message: message.text.startswith('/payment '))
def payment_with_password(message):
    command_parts = message.text.split(' ')
    if len(command_parts) == 2:
        password = command_parts[1]
        if password == passnya:
            global saldo
            saldo += 15
            bot.send_message(message.chat.id, "Top up berhasil.")
            blokir_nonaktif()
            bot.send_message(message.chat.id, " saldo anda di telah terisi kembali")# Menambah saldo setiap kali melakukan pembayaran
        else:
            bot.send_message(message.chat.id, "Kata sandi salah. Coba lagi.")
    else:
        bot.send_message(message.chat.id, "Perintah tidak valid. lakukan topup dengan: /payment [password]")

# Handler untuk pesan biasa
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    automatic_payment(message)
    display_saldo(message)
    # Implementasikan logika lainnya untuk bot Anda di sini

def generate_keyword_file(filename, num_keywords):
    keyword_list = acak.kwlist
    num_keywords = min(num_keywords, len(keyword_list))

    random_keywords = random.sample(keyword_list, num_keywords)

    with open(filename, "w") as file:
        file.write("\n".join(random_keywords))

@bot.message_handler(commands=['bikin_prompt'])
def handle_prompt(message, keyword_list):
    args = message.text.split('/')[1:]

    if len(args) == 7:
        keyword1_file, keyword2_file, output_file, command_option, specification_option, prompt_type, additional_input = args

        # Generate keyword files
        generate_keyword_file(keyword1_file, 500)
        generate_keyword_file(keyword2_file, 500)

        # Create prompt
        create_prompt(keyword1_file, keyword2_file, output_file, command_option, specification_option, prompt_type, additional_input, message)

        # Send the output file to the user
        with open(output_file, 'r') as file:
            output_text = file.read()

        bot.send_message(message.chat.id, output_text)
    else:
        bot.send_message(message.chat.id, "Format prompt tidak valid. Gunakan format /ai_prompt fitur.txt/objek.txt/ai.txt/kata_perintah/specification_option/prompt_type/jumlah")

# Fungsi untuk mengurangi saldo
def kurangi_saldo(jumlah):
    global saldo
    saldo -= jumlah
    if isi_saldo == 0:
        bot.send_message(text=f"saldo telah mencapai atau lebih dari: 0 lakukan /payment atau /topup terlebih dahulu .")
        is_blokir_aktif



# Fungsi peg_parser
def peg_parser():
    # Implementasi peg_parser di sini
    pass

# Contoh penggunaan assert
def check_saldo():
    global jumlah_saldo
    saldo = jumlah_saldo
    jumlah_saldo = -11
    assert saldo >= -1, "Saldo tidak boleh negatif."

if __name__ == '__main__':
    # Cek isi_saldo dan lakukan sesuatu jika isi_saldo == 10
    bot.polling(none_stop=True)
    try:
        jumlah_koin = jumlah_saldo
        jumlah_koin -= +10
        if saldo_awal <= 0:
            print("Saldo telah habis. bot di blokir aksesnya ")
        # Misalnya, jalankan peg_parser()
    except Exception as e:
        print(f"terjadi kecurangan saldo {str(e)}")

    check_saldo()
    print(f"Harga per {isi_saldo} saldo adalah 5 ribu per bulan")

    # Loop utama
    while True:
        try:
            # Cek apakah saldo mencapai atau kurang dari 0
            if blokir_nonaktif():
                break  # Keluar dari loop jika terblokir

            # Lakukan tindakan lain di sini
            # ...

            # Contoh: Kurangi saldo setiap kali sesuai dengan aktivitas tertentu
            kurangi_saldo(5) # Misalnya, mengurangi saldo sebesar 3

            # Cek apakah saldo mencapai 0
            if saldo := 0:
                print(f"Saldo belum premium. ")
                is_blokir_aktif
                break  # Keluar dari loop jika saldo mencapai 0

        except Exception as e:
            print(f"Terjadi kesalahan: {str(e)}")