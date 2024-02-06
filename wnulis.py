import random

import nltk
from weasyprint import HTML

nltk.download("words")

def process_keywords_from_csv(input_file):
    with open(input_file, "r", encoding="utf-8") as file:
        keywords_csv = file.read().lower().split(',')
    return list(set(keywords_csv))  # Remove duplicates and convert to list

def process_keywords_from_txt(input_file):
    with open(input_file, "r", encoding="utf-8") as file:
        keywords_txt = file.read().lower().split()
    return list(set(keywords_txt))  # Remove duplicates and convert to list

def randomize_words(text, num_iterations):
    words_list = text.split()
    for _ in range(num_iterations):
        random.shuffle(words_list)
    return ' '.join(words_list)

def construct_novel_pdf(title, synopsis, keywords_csv, keywords_txt):
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
    </head>
    <body>
        <h1>{title}</h1>
        <p><i>{synopsis}</i></p>
    """

    for keyword in keywords_csv:
        html_content += f"<p>{keyword},</p>"

    for keyword in keywords_txt:
        html_content += f"<p>{keyword}...</p>"

    while len(html_content) <= 40000:  # Adjust the length as needed
        random_content = randomize_words("Random content for variety. ", random.randint(700, 1000))
        html_content += f"<p>{random_content}</p>"

    closing_statement = "Terima kasih atas perhatiannya. Semoga Anda menikmati cerita ini."
    html_content += f"<p>{closing_statement}</p>"

    html_content += """
    </body>
    </html>
    """

    pdf_filename = "output_novel.pdf"
    HTML(string=html_content).write_pdf(pdf_filename)

    print(f"Novel content saved to '{pdf_filename}'.")

# Example usage:
judul_cerita = "Masukkan judul cerita"
sinopsis = "Masukkan sinopsis cerita"

# Process keywords from CSV and TXT
keywords_csv = process_keywords_from_csv("katakunci.csv")
keywords_txt = process_keywords_from_txt("katakunci.txt")

# Construct novel narrative based on keywords and save as PDF
construct_novel_pdf(judul_cerita, sinopsis, keywords_csv, keywords_txt)
