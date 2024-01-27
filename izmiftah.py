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
from googlesearch import search
from bs4 import BeautifulSoup
import time
import random
import keyword

bot = telebot.TeleBot("IDBOT_TELEGRAM_KAMU")  # Ganti dengan token bot Telegram Anda
last_update_time = None
keywords_list = []
keyword = "Tolong ganti tulisan di bagian ini setelah jadi"

def generate_keyword_file(filename, num_keywords):
    keyword_list = keyword.kwlist
    num_keywords = min(num_keywords, len(keyword_list))

    random_keywords = random.sample(keyword_list, num_keywords)

    with open(filename, "w") as file:
        file.write("\n".join(random_keywords))

@bot.message_handler(commands=['ai'])
def handle_prompt(message):
    # Mendapatkan argumen dari prompt
    args = message.text.split('/')[2:]

    if len(args) == 7:
        keyword1_file = args[0]
        keyword2_file = args[1]
        output_file = args[2]
        command_option = args[3]
        specification_option = args[4]
        prompt_type = args[5]
        additional_input = args[6]

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
        bot.send_message(message.chat.id, "Format prompt tidak valid. Gunakan format /buatlah keyword1.txt/keyword2.txt/output.txt/kata_perintah/specification_option/prompt_type/jumlah/")

def create_prompt(keyword1_file, keyword2_file, output_file, command_option, specification_option, prompt_type, additional_input, message):
    with open(keyword1_file, "r") as key1_file:
        key1_options = key1_file.readlines()

    with open(keyword2_file, "r") as key2_file:
        key2_options = key2_file.readlines()

    with open(output_file, "w") as file:
        dan = key1_options
        jika = key2_options
        for prompt in processed_data:
            key1_option = random.choice(key1_options).strip()
            key2_option = random.choice(key2_options).strip()
                
            try:
                subprocess.run(['bash', 'key.sh'], check=True)
                bot.reply_to(message, f"Ai prompt sudah terkespor ke {output_file} .")
            except subprocess.CalledProcessError as e:
                bot.reply_to(message, f"Error: {e}")
                
            if prompt_type == "text":
                output_line = f"\n\n\n HASIL OUTPUTNYA : \n\n\n {command_option} {specification_option} serta {key1_option} \n\n dengan tambahan fungsi {key2_option} \n\n adapun jika isinya berupa {prompt} {key1_option} \n\n\n\n dengan skrip: \n\n {prompt} {specification_option}\n\n\n"
            elif prompt_type == "image":
                output_line = f"Generate image with command: \n\n\n {command_option}, dengan latar elegant dengan penuh estetika nuansa {specification_option} bertemakan {key1_option} dengan warna {key2_option} \n\n\n"
            elif prompt_type == "script":
                output_line = f"Execute script: \n\n\n {command_option} {specification_option} dan serta {prompt} jika hal tersebut berupa  \n {prompt} \n dengan {key1_option} \n\n di dalam skrip {prompt} {key1_option} \n\n dengan module atau plugin tambahan {prompt}{key2_option} \n\n\n {specification_option}\n\n\n\n"
            elif prompt_type == "soal":
                soal = additional_input
                output_line = f"Prompt jawab soalnya \n\n\n {command_option} {specification_option} dan jawablah jika soalnya:  \n {prompt} \n tanpa {key1_option} \n\n maka tolong jawab {prompt} {key1_option} \n\n dengan menjelaskan {prompt}{key2_option} \n\n\n {specification_option} secara rinci \n\n sebanyak {soal} soal \n\n"
            elif prompt_type == "cerita":
                paragraf = additional_input
                output_line = f"Prompt ceritanya: \n\n\n {command_option} {specification_option} dan buatlah momen lucu setelah terjadi kejadian berupa  \n\n {prompt} \n\n\n dan buatlah ceritanya dengan penuh drama dan lelucon keharmonisan \n\n dan jangan lupa buat ulang dengan tema: \n {key1_option} \n\n dengan menambahkan tambahkan {prompt} \n {specification_option} di dalam ceritanya \n\n sebanyak {paragraf} paragraf \n\n"
            else:
                output_line = "Invalid prompt type\n masukkan opsi\n 1.image, \n 2.text atau \n 3.script \n"

            file.write(output_line)

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
    
@bot.message_handler(commands=['dnsinfo'])
def handle_dnsinfo(message):
    domain = message.text.split()[1]
    cname_values, ipv4_addresses, ipv6_addresses = get_dns_info(domain)
    bot.send_message(message.chat.id, f"CNAME: {cname_values}\nIPv4: {ipv4_addresses}\nIPv6: {ipv6_addresses}")
    time.sleep(10)  # Add a delay of 10 seconds
    
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
        bot.reply_to(message, "Invalid format. Use /dork <keywords>;<domain_extensions>")
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

@bot.message_handler(commands=['scan'])
def handle_subdomain_query(message):
    domain = message.text.split()[-1]  # assuming the domain is the last text after the command
    results = scan_subdomain(domain)
    bot.reply_to(message, f"Subdomain scan results: {results}")

def check_cover_png():
    file_path = 'cover.png'
    if os.path.exists(file_path) and os.path.getsize(file_path) == 0:
        return True
    return False

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
        
@bot.message_handler(commands=['download-hasil'])
def download_keywords(message):
    global keywords_list

    try:
        with open('hasil.txt', 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        print(f"Error downloading keywords: {e}")
        bot.reply_to(message, "Gagal mengunduh file txt. Coba lagi nanti.")

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
    
if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)            # Keep the bot running
        except Exception:
            time.sleep(10)
