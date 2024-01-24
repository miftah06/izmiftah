import os
import pandas as pd
from fpdf import FPDF
import pdfkit
from datetime import datetime

def handle_nan(value, default_value=""):
    return default_value if pd.isna(value) else value
    
def generate_html(data):
    halaman = handle_nan(data['Logo'][0], "Default Halaman")
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{halaman} - {handle_nan(data['Bab'][0], "Default Bab")}</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
        <style>
            body {{
                margin: 4%;
                font-family: 'Times New Roman', Times, serif;
            }}
            .container {{
                margin: auto;
                width: 70%;
                text-align: justify;
            }}
            .bold {{
                font-weight: bold;
                font-size: 16px;
            }}
            .indent {{
                text-indent: 20px;
            }}
            .justify {{
                text-align: justify;
            }}
            .left {{
                text-align: left;
                margin-bottom: 2em;
            }}
            .center {{
                text-align: center;
            }}
            .ul-spacing {{
                margin-left: 1em;
            }}
            .first-line-indent {{
                text-indent: 3em;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="bold center">{handle_nan(data['Bab'][0], "")}</h1>
            <p class="indent justify bold">
                {handle_nan(data['Subjudul 1'][0], "")}
            </p>
            <div class="left ul-spacing">
                <ul class="first-line-indent">
                    {halaman}
                </ul>    
            </div>
            <ol>
    """

    # Save HTML
    output_html_path = f'materi_{timestamp}.html'
    with open(output_html_path, 'w', encoding='utf-8') as html_file:
        html_file.write(template)    
    print("\nProses selesai. File HTML yang indah tersedia di materi.html.")
    return template

def generate_pdf_from_html(html_content, output_pdf):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name, file_extension = os.path.splitext(output_pdf)
    stamped_output_pdf = f"{file_name}_{timestamp}{file_extension}"

    with open('materi.html', 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

    pdfkit.from_file('materi.html', stamped_output_pdf)
    os.remove('materi.html')

    print(f"Dokumen PDF berhasil disimpan di {stamped_output_pdf}")        

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

def main():
    # Baca data dari file Excel
    input_file_path = 'auto.xlsx'
    data = pd.read_excel(input_file_path).to_dict(orient='list')

    # Panggil fungsi untuk membuat HTML
    html_content = generate_html(data)

    with open(f'output.html', 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

    # Panggil fungsi untuk membuat PDF
    beauty_pdf(data)

if __name__ == "__main__":
    main()
