import csv
import keyword
import os
import random
import subprocess
import time
import urllib.error
import urllib.request

import openai
import telebot
from googlesearch import search
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate

# Ganti dengan API key OpenAI Anda
openai.api_key = 'your-openai-api-key'
bot = telebot.TeleBot("telegram-bot-token-kamu")  # Ganti dengan token bot Telegram Anda
last_update_time = None
keywords_list = []

def generate_keyword_file(filename, num_keywords):
    keyword_list = keyword.kwlist
    num_keywords = min(num_keywords, len(keyword_list))

    random_keywords = random.sample(keyword_list, num_keywords)

    with open(filename, "w") as file:
        file.write("\n".join(random_keywords))


@bot.message_handler(commands=['ai_prompt'])
def handle_prompt(message):
    args = message.text.split('/')[1:]

    if len(args) == 7:
        keyword1_file, keyword2_file, output_file, command_option, specification_option, prompt_type, additional_input = args

        # Generate keyword files
        generate_keyword_file(keyword1_file, 500)
        generate_keyword_file(keyword2_file, 500)

        # Create prompt
        create_prompt(keyword1_file, keyword2_file, output_file, command_option, specification_option, prompt_type,
                      additional_input, message)

        # Send the output file to the user
        with open(output_file, 'r') as file:
            output_text = file.read()

        bot.send_message(message.chat.id, output_text)
    else:
        bot.send_message(message.chat.id,
                         "Format prompt tidak valid. Gunakan format /ai_prompt fitur.txt/objek.txt/ai.txt/kata_perintah/specification_option/prompt_type/jumlah")


def create_prompt(keyword1_file, keyword2_file, output_file, command_option, specification_option, prompt_type,
                  additional_input, message):
    with open("skrip.txt", "r") as parno_file:
        parno_options = parno_file.readlines()
        prompt = random.choice(parno_options).strip()
    with open(keyword1_file, "r") as key1_file, open(keyword2_file, "r") as key2_file, open(output_file, "w") as file:
        key1_options = key1_file.readlines()
        key2_options = key2_file.readlines()
        key1_option = random.choice(key1_options).strip()
        key2_option = random.choice(key2_options).strip()
        paragraf = additional_input.strip()

        try:
            subprocess.run(['bash', 'key.sh'], check=True)
            bot.reply_to(message,
                         f"Ai prompt sudah terkespor ke {output_file}\nSilahkan jalankan /keyword lalu /download_hasil \n lalu /download2 untuk output.txt sebagai /ai /command/command/output.txt atau ai.txt untuk /download3.")
        except subprocess.CalledProcessError as e:
            bot.reply_to(message, f"Error: {e}")
        if prompt_type == "text":
            output_line = f"Generate script with command:\n\n\n {command_option} {specification_option} serta {key1_option}\n dengan tambahan fungsi {key2_option}\n adapun jika isinya berupa {prompt} {key1_option}\n\n dengan fitur:\n\n{prompt} bersama fungsi atau pembahasan mengenai {key2_option} serta berikan saya detail lengkapnya \n\n\n"
        elif prompt_type == "image":
            output_line = f"Generate image with command:\n\n\n {command_option}, dengan latar elegant dengan penuh estetika nuansa {specification_option} bertemakan {key1_option} dengan warna {key2_option}\n\n\n"
        elif prompt_type == "script":
            output_line = f"Generate script with command:\n\n\n {command_option}{specification_option} dan serta {prompt} jika hal tersebut berupa\n {prompt}\n dengan {key1_option}\n\n di dalam skrip {parno_options} {key1_option}\n dengan module atau plugin tambahan {prompt}{key2_option}\n\n\npada untuk {specification_option} dan berikan saya skrip lengkapnya\n\n\n\n"
        elif prompt_type == "soal":
            output_line = f"Generate answer with command:\n\n\n {command_option}{specification_option} dan jawablah jika soalnya:\n {prompt}\n tanpa {key1_option}\n\n maka tolong jawab {parno_options} {key1_option}\n dengan menjelaskan {prompt}{key2_option}\n\n\n {specification_option} secara rinci\n sebanyak {paragraf} paragraf serta berikan saya jawaban lengkapnya\n\n"
        elif prompt_type == "cerita":
            output_line = f"Generate story with command:\n\n\n {command_option}, dengan latar elegant dengan penuh estetika nuansa {specification_option} bertemakan {key1_option} dengan warna {key2_option}\n\n\n{command_option}{specification_option} dan buatlah momen lucu setelah terjadi kejadian berupa\n\n {prompt}\n\n\n dan buatlah ceritanya dengan penuh drama dan lelucon keharmonisan\n\n dan jangan lupa buat ulang dengan tema:\n {key1_option}\n dengan menambahkan tambahkan {prompt}\n {specification_option} di dalam ceritanya\n\n sebanyak {paragraf} paragraf\n\n"
        else:
            output_line = "Invalid prompt type\n masukkan opsi\n 1.image,\n 2.text atau\n 3.script\n"
        file.write(output_line)


def extract_domain(url):
    try:
        domain = url.split('//')[1].split('/')[0]
    except IndexError:
        print(f"Error extracting domain from URL: {url}")
        return None
    return domain


def scrape_domain(keyword):
    print(f"Searching for: {keyword}")
    results = []
    count = 0
    for url in search(keyword, num_results=3):
        print(f"Found URL: {url}")
        domain = extract_domain(url)
        result = None
        if domain:
            result = {
                'Keyword': keyword,
                'URL': url,
                'Domain': domain,
            }
        if result:
            results.append(result)
            count += 1
        if count >= 3:
            break
        time.sleep(5)
    return results


@bot.message_handler(commands=['dork'])
def handle_message(message):
    try:
        _, keywords_line, domain_extensions_line = message.text.split('/')
    except ValueError:
        bot.reply_to(message, "Invalid format. Use /dork <keywords>/<domain_extensions>")
        return
    keywords = keywords_line.split(',')
    domain_extensions = domain_extensions_line.split(',')
    all_results = []
    for keyword in keywords:
        for domain_extension in domain_extensions:
            keyword_with_extension = f"{keyword}{domain_extension}"
            results = scrape_domain(keyword_with_extension)
            all_results.extend(results)
    if all_results:
        bot.send_message(message.chat.id, str(all_results))
    else:
        bot.reply_to(message, "No results found.")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello, welcome to my Bot! Please format your message as follows: /write [Keyword]")


def check_cover_png():
    file_path = 'cover.png'
    if os.path.exists(file_path) and os.path.getsize(file_path) == 0:
        return True
    return False


def random_keywords(dataframe):
    num_keywords = len(dataframe)
    if num_keywords == 0:
        return []

    # Menghasilkan indeks kata kunci acak tanpa penggantian
    random_indices = random.sample(range(num_keywords), min(num_keywords, 10))

    # Mengambil kata kunci yang sesuai dengan indeks yang dihasilkan secara acak
    random_keywords = [dataframe.iloc[idx, 0] for idx in random_indices]

    return random_keywords


@bot.message_handler(commands=['write'])
def get_random_text(message):
    global last_update_time, keywords_list

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
    your_dataframe = data

    # Ganti fungsi pencarian Google dengan generate_html
    # Assuming your_dataframe contains the data you need
    generated_keyword = random_keywords(your_dataframe)

    # Process the generated_keyword as needed

    bot.reply_to(message,
                 f"Intruksi!!: {generated_keyword} \n list file bahan: \n 1. katakunci.csv \n 2. keyword.txt \n 3. cover.xlsx \n 4. auto.xlsx \n 5. skrip.txt \n DAPATKAN DI https://github.com/miftah06/izmiftah/ \n")


@bot.message_handler(commands=['download3'])
def download_html(message):
    try:
        with open('ai.txt', 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        print(f"Error downloading txt output file: {e}")
        bot.reply_to(message, "Gagal mengunduh file txt. Coba lagi nanti.")


@bot.message_handler(commands=['download_cover'])
def download_keywords(message):
    global keywords_list

    try:
        with open('beauty-cover.pdf', 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        print(f"Error downloading keywords: {e}")
        bot.reply_to(message, "Gagal mengunduh file pdf. Coba lagi nanti.")


@bot.message_handler(commands=['download_final'])
def download_keywords(message):
    global keywords_list

    try:
        with open('final_output.pdf', 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        print(f"Error downloading keywords: {e}")
        bot.reply_to(message, "Gagal mengunduh file pdf. Coba lagi nanti.")


@bot.message_handler(commands=['download_hasil'])
def download_keywords(message):
    global keywords_list

    try:
        with open('hasil.txt', 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        print(f"Error downloading keywords: {e}")
        bot.reply_to(message, "Gagal mengunduh file txt. Coba lagi nanti.")


@bot.message_handler(commands=['download_novel'])
def download_keywords(message):
    global keywords_list

    try:
        with open('output_novel.pdf', 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        print(f"Error downloading keywords: {e}")
        bot.reply_to(message, "Gagal mengunduh file pdf. Coba lagi nanti.")


@bot.message_handler(commands=['download_html'])
def download_html(message):
    try:
        with open('output.html', 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        print(f"Error downloading HTML: {e}")
        bot.reply_to(message, "Gagal mengunduh file HTML. Coba lagi nanti.")


@bot.message_handler(commands=['download2'])
def download_html(message):
    try:
        with open('output.txt', 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        print(f"Error downloading txt output file: {e}")
        bot.reply_to(message, "Gagal mengunduh file txt. Coba lagi nanti.")


@bot.message_handler(commands=['download_html1'])
def download_html(message):
    try:
        with open('cover.html', 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        print(f"Error downloading HTML: {e}")
        bot.reply_to(message, "Gagal mengunduh file HTML. Coba lagi nanti.")


@bot.message_handler(commands=['download_html2'])
def download_html(message):
    try:
        with open('pdf.html', 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        print(f"Error downloading HTML: {e}")
        bot.reply_to(message, "Gagal mengunduh file HTML. Coba lagi nanti.")


def read_keywords_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            keywords = file.read().splitlines()
        return keywords
    except Exception as e:
        print(f"Error reading keywords file '{filename}': {e}")
        return []


def extend_keywords_list(new_keywords):
    global keywords_list
    keywords_list.extend(new_keywords)


@bot.message_handler(commands=['upload'])
def update_keywords(message):
    global keywords_list

    keyword_filename = 'keyword.txt'  # Ganti dengan nama file keyword yang sesuai
    new_keywords = read_keywords_file(keyword_filename)

    if new_keywords:
        extend_keywords_list(new_keywords)
        bot.reply_to(message, f"Keywords berhasil diperbarui. Total {len(new_keywords)} kata kunci ditambahkan.")
    else:
        bot.reply_to(message, "Gagal memperbarui keywords. Pastikan file 'keyword.txt' tersedia dan berisi kata kunci.")

    if check_cover_png():
        bot.reply_to(message,
                     "cover.png kosong. Silahkan upload cover.png sebagai logo atau cover karya tulis atau novel Anda.")
    else:
        bot.reply_to(message, "Terima kasih! File cover.png sudah diunggah.")


def process_uploaded_file(file_path):
    # Implement your logic to process the uploaded file
    # For example, you can read the contents of the file
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # Process the content as needed
            print(f"Content of the uploaded file:\n{content}")
            return True
    except Exception as e:
        print(f"Error processing uploaded file: {e}")
        return False


@bot.message_handler(content_types=['document'])
def handle_uploaded_file(message):
    global keywords_list

    if message.document.file_name not in ['katakunci.csv', 'keyword.txt', 'skrip.txt', 'auto.xlsx', 'input.txt',
                                          'subdomains.txt']:
        bot.reply_to(message,
                     "Mohon kirim file dengan nama 'katakunci.csv', 'keyword.txt', 'skrip.txt', 'auto.xlsx', 'input.txt', 'subdomains.txt'.")
        return

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open(message.document.file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    if update_keywords():
        bot.reply_to(message, f"File {message.document.file_name} berhasil diunggah dan database diperbarui.")
    else:
        bot.reply_to(message, "Gagal memperbarui database. Coba lagi nanti.")


@bot.message_handler(commands=['keyword'])
def update_scripts(message):
    try:
        subprocess.run(['bash', 'key.sh'], check=True)
        bot.reply_to(message, "Skrip berhasil diperbarui.")
    except subprocess.CalledProcessError as e:
        bot.reply_to(message, f"Error: {e}")


def update_keywords():
    global keywords_list

    try:
        with open('katakunci.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            keywords_list = [row[0] for row in reader]
        return True
    except Exception as e:
        print(f"Error updating keywords: {e}")
        return False


# Tambahkan logika untuk memeriksa keberadaan file auto.xlsx
if not os.path.isfile('auto.xlsx'):
    # File auto.xlsx tidak ada, download atau generate
    try:
        subprocess.run(['wget', 'https://github.com/miftah06/izmiftah/raw/main/auto.xlsx'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error downloading auto.xlsx: {e}")

# Tambahkan logika untuk memeriksa keberadaan file subdomains.txt
if not os.path.isfile('subdomains.txt'):
    # File subdomains.txt tidak ada, download atau generate
    try:
        subprocess.run(['wget', 'https://github.com/miftah06/izmiftah/raw/main/subdomains.txt'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error downloading subdomains.txt: {e}")


def get_dns_info(hostname):
    try:
        # Scanning CNAME
        cname_result = subprocess.check_output(['nslookup', '-type=CNAME', hostname], universal_newlines=True)
        cname_values = [line.split(':')[-1].strip() for line in cname_result.splitlines() if
                        'canonical name' in line.lower()]
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


@bot.message_handler(commands=['dnsinfo'])
def handle_dnsinfo(message):
    try:
        # Mendapatkan domain dari pesan
        domain = message.text.split()[-1]
        cname_values, ipv4_addresses, ipv6_addresses = get_dns_info(domain)
        bot.send_message(message.chat.id, f"CNAME: {cname_values}\nIPv4: {ipv4_addresses}\nIPv6: {ipv6_addresses}")
    except IndexError:
        bot.send_message(message.chat.id, "Format perintah tidak valid. Gunakan /dnsinfo <domain>.")


def scan_subdomain(domain):
    subdomains = []
    with open("subdomains.txt", "r") as subdomain_file:
        subdomains = subdomain_file.read().splitlines()
    domain_results = []
    for subdomain in subdomains:
        url = f"https://{subdomain}.{domain}"
        try:
            response = urllib.request.urlopen(url)
            if response.getcode() in [200, 301, 400, 409, 502, 401]:
                server_info = response.getheader('Server', 'N/A')
                print(f"Subdomain found: {url} | Status Code: {response.getcode()} | Server: {server_info}\n")
                domain_results.append(url)
        except urllib.error.URLError:
            pass
    with open("output.txt", "w") as output_file:
        for result in domain_results:
            output_file.write(f"{result}\n")
    return domain_results


@bot.message_handler(commands=['scan'])
def handle_subdomain_query(message):
    try:
        # Mendapatkan domain dari pesan
        domain = message.text.split()[-1]
        results = scan_subdomain(domain)
        bot.reply_to(message, f"Hasil pemindaian subdomain: {results}")
    except IndexError:
        bot.send_message(message.chat.id, "Format perintah tidak valid. Gunakan /scan <domain>.")

    # Fungsi untuk menyimpan kata kunci dalam file CSV dan TXT


def save_keywords_to_files(keywords, csv_filename, txt_filename):
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Keyword'])
        for keyword in keywords:
            writer.writerow([keyword])

    with open(txt_filename, 'w', encoding='utf-8') as txtfile:
        for keyword in keywords:
            txtfile.write(keyword + '\n')


def generate_novel_content(keywords, pdf_filename):
    # Buat dokumen PDF dengan ReportLab
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # Buat halaman PDF
    story = []

    # Ganti dengan logika Anda untuk menghasilkan konten PDF berdasarkan kata kunci
    # Di sini, kita akan menambahkan setiap kata kunci sebagai paragraf dengan gaya khusus
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    keyword_style = normal_style.clone('KeywordStyle')
    keyword_style.textColor = colors.blue  # Mengatur warna teks kata kunci menjadi biru

    for keyword in keywords:
        keyword_paragraph = Paragraph(keyword, keyword_style)
        story.append(keyword_paragraph)

    # Menambahkan konten ke dokumen PDF
    doc.build(story)

    # Fungsi untuk menghasilkan kata kunci acak
# Fungsi untuk menghasilkan daftar kata kunci secara acak
def generate_random_keywords(num_keywords):
    # Inisialisasi set kosong untuk menyimpan kata kunci
    keywords = set()

    # Batasi jumlah kata kunci yang dihasilkan hingga num_keywords
    while len(keywords) < num_keywords:
        # Menggunakan OpenAI API untuk menghasilkan kata kunci acak
        response = openai.Completion.create(
            engine="text-davinci-002",  # Gunakan mesin GPT-3.5 Turbo
            prompt="Generate a random keyword related to your topic.",
            max_tokens=100,
        )

        # Mendapatkan teks dari respons dan membersihkannya
        word = response.choices[0].text.strip()

        # Pastikan kata kunci unik sebelum ditambahkan ke daftar
        if word not in keywords:
            keywords.add(word)

    # Mengembalikan daftar kata kunci dalam bentuk list
    return list(keywords)
def generate_random_keywords(num_keywords):
    # Daftar kata kunci acak
    keywords = []

    # Batasi jumlah kata kunci yang dihasilkan hingga num_keywords
    while len(keywords) < num_keywords:
        # Ganti dengan logika Anda untuk menghasilkan kata kunci acak
        # Di sini, kita akan menggunakan kata-kata acak sebagai contoh
        random_keyword = "Keyword_" + str(random.randint(1, 100))
        keywords.append(random_keyword)

    return keywords

# Fungsi untuk menghasilkan daftar kata kunci dalam bentuk PDF menggunakan reportlab
def generate_keywords_pdf_reportlab(keywords, pdf_filename):
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # Set font dan ukuran teks
    c.setFont("Helvetica", 12)

    # Tulis daftar kata kunci ke PDF
    y = 700
    for keyword in keywords:
        c.drawString(50, y, keyword)
        y -= 20

    # Simpan PDF
    c.save()

    print(f"Dokumen PDF berhasil disimpan di {pdf_filename}")

# Handler untuk perintah /update
@bot.message_handler(commands=['update'])
def update_keywords(message):
    try:
        num_keywords = 5  # Ganti dengan jumlah kata kunci yang Anda inginkan

        # Generate daftar kata kunci secara acak
        random_keywords = generate_random_keywords(num_keywords)

        # Nama file PDF yang akan dihasilkan
        pdf_filename_reportlab = "output_novel.pdf"

        # Generate daftar kata kunci dalam bentuk PDF menggunakan reportlab
        generate_keywords_pdf_reportlab(random_keywords, pdf_filename_reportlab)

        bot.reply_to(message, f"Kata kunci acak telah dihasilkan. PDF (reportlab): {pdf_filename_reportlab}")
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

# Handler untuk perintah /ai
@bot.message_handler(commands=['ai'])
def handle_ai(message):
    try:
        message_text = message.text.split(' ', 1)[1] if len(message.text.split()) > 1 else "No input provided."

        # Membuat permintaan ke OpenAI Chat API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Pilih model yang sesuai
            messages=[
                {"role": "system", "content": "You are a worker with your research and development."},
                {"role": "user", "content": message_text}
            ]
        )

        # Mengambil pesan dari respons
        ai_reply = response['choices'][0]['message']['content']

        # Mengirimkan balasan AI sebagai reply
        bot.reply_to(message, ai_reply)

    except Exception as e:
        bot.reply_to(message, str(e))


# Handler untuk perintah /download
@bot.message_handler(commands=['download'])
def download_file(message):
    try:
        file_name = message.text.split(' ', 1)[1] if len(message.text.split()) > 1 else "output_novel.pdf"
        with open(file_name, 'rb') as file:
            bot.send_document(message.chat.id, file)
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")


# Handler untuk perintah /ai
@bot.message_handler(commands=['ai'])
def handle_chat(message):
    try:
        message_text = message.text.split(' ', 1)[1] if len(message.text.split()) > 1 else "No input provided."

        # Membuat permintaan ke OpenAI Chat API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Pilih model yang sesuai
            messages=[
                {"role": "system", "content": "You are a worker with your research and development."},
                {"role": "user", "content": message_text}
            ]
        )

        # Mengambil pesan dari respons
        ai_reply = response['choices'][0]['message']['content']

        # Mengirimkan balasan AI sebagai reply
        bot.send_message(message.chat.id, ai_reply)

    except Exception as e:
        bot.send_message(message.chat.id, str(e))


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception:
            time.sleep(10)
