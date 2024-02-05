import os
import numpy as np
from datetime import datetime
from fpdf import FPDF

def handle_nan(value, default_value=""):
    return default_value if np.isnan(value) else value

def generate_html(data, keyword):
    halaman = handle_nan(data[0]['Logo'], "")

    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Filter the DataFrame based on the provided keyword
    filtered_data = data[data['Keyword'] == keyword]

    # Check if any matching rows are found
    if filtered_data.shape[0] == 0:
        return "No matching data found for the provided keyword."

    selected_row = filtered_data.iloc[0]

    # Extract values from the selected row
    logo_value = handle_nan(selected_row['Logo'], "")
    bab_value = handle_nan(selected_row['Bab'], "Default Bab")
    subjudul_value = handle_nan(selected_row['Subjudul'], "Default Subjudul")

    # Generate HTML content
    html_content = f"""
    <!-- Your HTML structure here -->
    <h1>{bab_value}</h1>
    <p>{subjudul_value}</p>
    <p>{logo_value}</p>
    <!-- Add more HTML elements as needed -->
    """

    # Generate list items for optional data
    for i in range(1, 4):  # Assuming optional data is up to 3
        optional_subjudul_key = f'Subjudul {i}'
        optional_logo_key = f'Logo {i}'
        optional_opsional_key = f'Opsional {i}'

        optional_subjudul_value = handle_nan(selected_row[optional_subjudul_key], "")
        optional_logo_value = handle_nan(selected_row[optional_logo_key], "")
        optional_opsional_value = handle_nan(selected_row[optional_opsional_key], "")

        if optional_subjudul_value:
            html_content += f"<li class='indent justify left'>{optional_subjudul_value}</li>"

        if optional_logo_value:
            html_content += f"<li class='indent justify left'>{optional_logo_value}</li>"

        if optional_opsional_value:
            html_content += f"<li class='indent justify left'>{optional_opsional_value}</li>"

    html_content += """
            </ul>
        </div>
    </body>
    </html>
    """

    # Save HTML
    output_html_path = f'isi_{timestamp}.html'
    with open(output_html_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

    print("\nProses selesai. File HTML yang indah tersedia di isi_{timestamp}.html.")
    return html_content, output_html_path

def generate_pdf_from_html(html_content, output_pdf):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name, file_extension = os.path.splitext(output_pdf)
    stamped_output_pdf = f"{file_name}_{timestamp}{file_extension}"

    with open('pdf.html', 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

    try:
        from xvfbwrapper import Xvfb
        vdisplay = Xvfb()
        vdisplay.start()
    except ImportError:
        pass

    import pdfkit

    pdfkit.from_file('pdf.html', stamped_output_pdf)

    if 'vdisplay' in locals():
        vdisplay.stop()

    print(f"Dokumen HTML berhasil disimpan di {output_pdf}")
    return stamped_output_pdf  # Mengembalikan path PDF yang dihasilkan

def beauty_pdf(data):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Adding content to PDF, modify as needed
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, "Insert your content here")

    pdf.output("final_output.pdf")
    print("\nProses selesai. File PDF yang indah tersedia di final_output.pdf.")

def get_input_file_path():
    pass

def main():
    # Meminta input file Excel dari pengguna
    input_file_path = get_input_file_path()

    # Baca data dari file Excel
    data = np.random.randint(0, len(input_file_path))

    # Panggil fungsi untuk membuat HTML
    keyword = "YourKeywordHere"  # Ganti dengan kata kunci yang sesuai
    html_content, output_html_path = generate_html(data, keyword)

    # Panggil fungsi untuk membuat PDF
    pdf_path = generate_pdf_from_html(html_content, "final_output.pdf")
    beauty_pdf(data)

if __name__ == "__main__":
    main()
