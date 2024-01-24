import os
import pandas as pd
import pdfkit
import random
from fpdf import FPDF
from datetime import datetime
 
def handle_nan(value, default_value=""):
    return default_value if pd.isna(value) else value

def generate_opsional_list(data, page_number, katakunci_list):
    opsional_html = ""
    for i in range(1, 10):
        opsional_key = f'Opsional {i}'
        if opsional_key in data and len(data[opsional_key]) > page_number - 1:
            opsional_value = handle_nan(data[opsional_key][page_number - 1], f"Default Opsional {i}")
            opsional_html += f"                <li class='indent justify left'>{opsional_value}</li>\n"
    random.shuffle(katakunci_list)
    opsional_html += f"<li class='indent justify left'>{', '.join(katakunci_list)}</li>\n"
    return opsional_html
 
def generate_html(data, katakunci_list):
    page_number = []
    template = """
    <!DOCTYPE html>
    <html>
    <head>

    """
    for i, bab_key in enumerate(data['Bab']):
        subjudul_key = f'Subjudul {i+1}'
        Halaman_key = f'Logo {i+1}'

        template += """
            <!-- Page {i+1} -->
 
        """

    template += """
        </div>
    </body>
    </html>
    """
    return template

def generate_pdf_from_html(html_content, output_pdf):
    with open('pdf.html', 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)
    pdfkit.from_file('pdf.html', output_pdf)
    print(f"Dokumen PDF berhasil disimpan di {output_pdf}")

def beauty_pdf(data):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    bold_style = 'B'
    newline_style = 'Ln'
    
    for key, values in data.items():
        if key.startswith("Subjudul"):

            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, str(values[0]), ln=True, align='C')

            for value in values[1:]:
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, str(value), align='L')

            pdf.ln(5)

    pdf.output("final_output.pdf")
    print("\nProses selesai. File PDF yang indah tersedia di final_output.pdf.")
 
if __name__ == "__main__":
    excel_file = 'auto.xlsx'

    if os.path.exists(excel_file):
        data = pd.read_excel(excel_file).to_dict(orient='list')
    else:
        print(f"File '{excel_file}' not found.")
        data = {}


    with open('katakunci.csv', 'r', encoding='utf-8') as katakunci_file:
        katakunci_list = katakunci_file.read().strip().split(',')
    

    with open('katakunci.txt', 'r', encoding='utf-8') as katakunci_file:
        keyword_list = katakunci_file.read().strip().split(',')
    

    html_content = generate_html(data, katakunci_list)
    output_pdf = "final_output.pdf"
    generate_pdf_from_html(html_content, output_pdf)

    beauty_pdf(data)