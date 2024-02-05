import nltk
import random
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph

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
    pdf_filename = "output_novel.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # Set custom styles for better aesthetics
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    synopsis_style = styles['BodyText']

    # List to hold the flowables (elements) of the PDF
    flowables = []

    # Add title with center alignment and larger font
    flowables.append(Paragraph(title, title_style))

    # Add aesthetically formatted synopsis
    flowables.append(Paragraph(f"<i>{synopsis}</i>", synopsis_style))

    # Adding unique keywords from CSV to the plot
    for keyword in keywords_csv:
        flowables.append(Paragraph(f"{keyword},", synopsis_style))

    # Adding unique keywords from TXT to the plot
    for keyword in keywords_txt:
        flowables.append(Paragraph(f"{keyword}...", synopsis_style))

    # Randomize and add content until reaching a certain length
    while len(flowables) <= 400:
        random_content = randomize_words("Random content for variety. ", random.randint(700, 1000))
        flowables.append(Paragraph(random_content, synopsis_style))

    # Add closing statement
    closing_statement = "Terima kasih atas perhatiannya. Semoga Anda menikmati cerita ini."
    flowables.append(Paragraph(closing_statement, synopsis_style))

    # Build the PDF document
    doc.build(flowables)

    print(f"Konten novel tersimpan di '{pdf_filename}.'")

# Example usage:
judul_cerita = "Masukkan judul cerita"
sinopsis = "Masukkan sinopsis cerita"

# Process keywords from CSV and TXT
keywords_csv = process_keywords_from_csv("katakunci.csv")
keywords_txt = process_keywords_from_txt("katakunci.txt")

# Construct novel narrative based on keywords and save as PDF
construct_novel_pdf(judul_cerita, sinopsis, keywords_csv, keywords_txt)
