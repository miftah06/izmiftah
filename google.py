import time

import telebot
from googlesearch import search

token = '6864959328:AAG7H2xldKkqr9-6ppEYVYHK09ARf2QzDd0'
bot = telebot.TeleBot(token, threaded=False)


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
        time.sleep(2)
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


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)            # Keep the bot running
        except Exception:
            time.sleep(3)
