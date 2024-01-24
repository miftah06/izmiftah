import nltk
from fpdf import FPDF
import random
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
import os

nltk.download("words")

def process_keywords_from_csv(input_file):
    with open(input_file, "r", encoding="utf-8") as file:
        keywords_csv = file.read().lower().split(',')
    return list(set(keywords_csv))

def process_keywords_from_txt(input_file):
    with open(input_file, "r", encoding="utf-8") as file:
        keywords_txt = file.read().lower().split()
    return list(set(keywords_txt))

def randomize_words(text, num_iterations):
    words_list = text.split()
    for _ in range(num_iterations):
        random.shuffle(words_list)
    return ' '.join(words_list)

def input_description():
    return input("Masukkan deskripsi untuk melengkapi kata-kata di dalam teks PDF: ")

def construct_academic_paper_pdf(title, synopsis, keywords_csv, keywords_txt, i, max_pages, description):
    pdf_filename = f"output_cerpen_{i}.pdf"

    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    title_style = ParagraphStyle(name="Title", fontName="Helvetica-Bold", fontSize=16, alignment=1, spaceAfter=10)
    synopsis_style = ParagraphStyle(name="Synopsis", fontName="Helvetica", fontSize=12, alignment=0, spaceAfter=10)
    keywords_style = ParagraphStyle(name="Keywords", fontName="Helvetica", fontSize=10, alignment=0, spaceAfter=10)
    content_style = ParagraphStyle(name="Content", fontName="Courier", fontSize=10, alignment=0, spaceAfter=10)

    flowables = []

    flowables.append(Paragraph(title, title_style))
    flowables.append(Paragraph("\n\n\n", title_style))
    flowables.append(Paragraph(f"<i>{synopsis}</i>", synopsis_style))
    flowables.append(Paragraph("\n\n", title_style))

    flowables.append(Paragraph("Keywords from CSV:", keywords_style))
    for keyword in keywords_csv:
        flowables.append(Paragraph(f"{keyword}, ", keywords_style))

    flowables.append(Paragraph("\n\n", title_style))

    flowables.append(Paragraph("Keywords from TXT:", keywords_style))
    for keyword in keywords_txt:
        flowables.append(Paragraph(f"{keyword}, ", keywords_style))

    flowables.append(Paragraph("\n\n", title_style))

    while len(flowables) <= 400 and doc.page < max_pages:
        random_content = randomize_words("Random content for variety. ", random.randint(700, 1000))
        flowables.append(Paragraph(random_content, content_style))

    flowables.append(Paragraph("\n\n", title_style))

    closing_statement = "Terima kasih atas perhatiannya. Semoga Anda menikmati Cerita Kalian."
    flowables.append(Paragraph(closing_statement, content_style))

    description_paragraph = Paragraph(f"\n\nDeskripsi:\n{description}", content_style)
    flowables.append(description_paragraph)

    doc.build(flowables)

    print(f"Cerpen content saved to '{pdf_filename}'.")

judul_cerita = input("Masukkan judul ex: Quantum Heroine No Seraph: Heroine of AI: ")
max_pages = 100

for i in range(1, 6):
    isi_bab = input(f"Masukkan Isi bagian/ bab Tulisan ke-{i} ex: Part 1. Kematian : ")
    if isi_bab.strip() == "":
        print(f"Isi Bab ke-{i} tidak diisi. Melanjutkan ke bab berikutnya.")
        continue

    keywords_csv = process_keywords_from_csv(os.path.join(os.getcwd(), "katakunci.csv"))
    keywords_txt = process_keywords_from_txt(os.path.join(os.getcwd(), "katakunci.txt"))

    description = input_description()

    construct_academic_paper_pdf(judul_cerita, isi_bab, keywords_csv, keywords_txt, i, max_pages, description)
