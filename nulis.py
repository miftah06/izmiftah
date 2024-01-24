import os
import subprocess
import pandas as pd
from datetime import datetime
import csv
import telebot 
import requests
from multiprocessing.dummy import Pool as ThreadPool

from auto import bootstrap as generate_novel  
import autopdf
from autopdf import generate_html  


bot = telebot.TeleBot("6822789783:AAExtKVMfMYflPTmWD3RPpcyI4D2HhsqbcQ")  # Ganti dengan token bot Telegram Anda
last_update_time = None
keywords_list = []
keyword = "Tolong ganti tulisan di bagian ini setelah jadi"

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

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello, welcome to my Bot! Please format your message as follows: /write [Keyword]")

@bot.message_handler(commands=['write'])
def get_random_text(message):
    global keywords_list
    # ... Rest of your code here

@bot.message_handler(commands=['scan_subdomain'])
def handle_subdomain_query(message):
    domain = message.text.split()[-1]  # assuming the domain is the last text after the command
    results = scan_subdomain(domain)
    bot.reply_to(message, f"Subdomain scan results: {results}")

def check_cover_png():
    file_path = 'cover.png'
    if os.path.exists(file_path) and os.path.getsize(file_path) == 0:
        return True
    return False

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Halo, selamat datang di bot saya! Kirim pesan dengan format: /write [Keyword]")

@bot.message_handler(commands=['write'])
def get_random_text(message):
    global last_update_time, keywords_list

    # Periksa apakah file katakunci.csv perlu diperbarui
    current_time = datetime.now()
    if last_update_time is None or (current_time - last_update_time).days >= 1:
        if update_keywords():
            last_update_time = current_time
        else:
            bot.reply_to(message, f"Maaf admin lupa mengupdate database untuk penulisan. \n Silahkan upload keyword.txt berupa bahan tulisan \n dan Coba lagi nanti.")
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

    bot.reply_to(message, f"Intruksi!!: {generated_keyword} \n list file bahan: \n 1. katakunci.csv \n 2. keyword.txt \n 3. cover.xlsx \n 4. auto.xlsx \n DAPATKAN DI https://github.com/miftah06/skripsi/raw/master/bab-generator/ \n")

@bot.message_handler(commands=['download-cover'])
def download_keywords(message):
    global keywords_list

    try:
        with open('beauty-cover.pdf', 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        print(f"Error downloading keywords: {e}")
        bot.reply_to(message, "Gagal mengunduh file pdf. Coba lagi nanti.")

@bot.message_handler(commands=['download-final'])
def download_keywords(message):
    global keywords_list

    try:
        with open('final_output.pdf', 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        print(f"Error downloading keywords: {e}")
        bot.reply_to(message, "Gagal mengunduh file pdf. Coba lagi nanti.")

@bot.message_handler(commands=['download'])
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

@bot.message_handler(commands=['download_html1'])
def download_html(message):
    try:
        with open('materi.html', 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        print(f"Error downloading HTML: {e}")
        bot.reply_to(message, "Gagal mengunduh file HTML. Coba lagi nanti.")

@bot.message_handler(commands=['download_html2'])
def download_html(message):
    try:
        with open('cover.html', 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        print(f"Error downloading HTML: {e}")
        bot.reply_to(message, "Gagal mengunduh file HTML. Coba lagi nanti.")

@bot.message_handler(commands=['download_html3'])
def download_html(message):
    try:
        with open('pdf.html', 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        print(f"Error downloading HTML: {e}")
        bot.reply_to(message, "Gagal mengunduh file HTML. Coba lagi nanti.")

@bot.message_handler(commands=['upload'])
def update_keywords(message):
    global keywords_list

    try:
        # Set a larger field size limit
        max_field_size = int(1e6)
        csv.field_size_limit(max_field_size)

        # Read the entire CSV file with Pandas
        df = pd.read_csv('keyword.txt', header=None)

        # Convert the first column to lowercase and extend the keywords list
        keywords_list.extend(df.iloc[:, 0].str.lower().tolist())

        return True
    except Exception as e:
        print(f"Error updating keywords: {e}")
        return False

    if check_cover_png():
        bot.reply_to(message, "cover.png kosong. Silahkan upload cover.png sebagai logo atau cover karya tulis atau novel Anda.")
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

    if message.document.file_name not in ['katakunci.csv', 'keyword.txt']:
        bot.reply_to(message, "Mohon kirim file dengan nama 'katakunci.csv' atau 'keyword.txt'.")
        return

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open(message.document.file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    if update_keywords():
        bot.reply_to(message, f"File {message.document.file_name} berhasil diunggah dan database diperbarui.")
    else:
        bot.reply_to(message, "Gagal memperbarui database. Coba lagi nanti.")

@bot.message_handler(commands=['update'])
def update_scripts(message):
    try:
        subprocess.run(['bash', 'run.sh'], check=True)
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
        subprocess.run(['wget', 'https://github.com/miftah06/skripsi/raw/master/bab-generator/input_data.xlsx'])
        subprocess.run(['wget', 'https://github.com/miftah06/skripsi/raw/master/cover-generator/cover.xlsx'])
        subprocess.run(['mv', 'input_data.xlsx', 'auto.xlsx'])
        print("File auto.xlsx berhasil di-download dan diubah namanya.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print("Gagal mendownload atau mengubah nama file auto.xlsx.")
        # Tambahkan logika untuk menghasilkan file auto.xlsx

def generate_html(dataframe):
    # Your logic for generating HTML based on the dataframe goes here
    # Replace this with your actual implementation
    generated_html = f"jangan lupa /update terlebih dahulu \n silahkan /download.. dan tolong \n <html><body><h1>{keyword}</h1></body></html>"
    return generated_html

bot.polling()
