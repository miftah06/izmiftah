import os
import numpy as np
from fpdf import FPDF
from datetime import datetime

def handle_nan(value, default_value=""):
    return default_value if np.isnan(value) else value

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
    return output_html_path

def generate_pdf_from_html(html_content, output_pdf):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name, file_extension = os.path.splitext(output_pdf)
    stamped_output_pdf = f"{file_name}_{timestamp}{file_extension}"

    with open(html_content, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Times New Roman", size=12)

    # Membaca HTML dan menambahkannya ke PDF
    with open(html_content, 'r', encoding='utf-8') as html_file:
        pdf.add_page()
        pdf.set_font("Times New Roman", size=12)
        for line in html_file:
            pdf.multi_cell(0, 10, line)

    # Simpan PDF
    pdf.output(stamped_output_pdf)

    os.remove(html_content)

    print(f"Dokumen PDF berhasil disimpan di {stamped_output_pdf}")

def main():
    # Baca data dari file Excel
    input_file_path = 'auto.npy'
    data = np.load(input_file_path, allow_pickle=True).item()

    # Panggil fungsi untuk membuat HTML
    html_content = generate_html(data)

    # Panggil fungsi untuk membuat PDF
    generate_pdf_from_html(html_content, 'final_output.pdf')

if __name__ == "__main__":
    main()
