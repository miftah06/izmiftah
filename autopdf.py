import os
import pandas as pd
from datetime import datetime
import pandas as pd
import pdfkit

def handle_nan(value, default_value=""):
    return default_value if pd.isna(value) else value

def generate_html(data):

    halaman = handle_nan(data.iloc[0]['Logo'], "")

    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    try:
        df = pd.read_csv('katakunci.csv')
    except FileNotFoundError:
        raise FileNotFoundError("File 'katakunci.csv' not found. Make sure the file exists.")

    # Filter the DataFrame based on the provided keyword
    filtered_data = df[df['Keyword'] == keyword]

    # Check if any matching rows are found
    if filtered_data.empty:
        return "No matching data found for the provided keyword."

    # Randomly select one row from the filtered data
    selected_row = filtered_data.sample(n=1, random_state=42)

    # Extract values from the selected row
    logo_value = handle_nan(selected_row.iloc[0]['Logo'], "")
    bab_value = handle_nan(selected_row.iloc[0]['Bab'], "Default Bab")
    subjudul_value = handle_nan(selected_row.iloc[0]['Subjudul 1'], "Default Subjudul")

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

        if optional_subjudul_key in data.columns and not pd.isna(data.iloc[0][optional_subjudul_key]):
            optional_value = handle_nan(data.iloc[0][optional_subjudul_key], f"")
            template += f"<li class='indent justify left'>{optional_value}</li>"

        if optional_logo_key in data.columns and not pd.isna(data.iloc[0][optional_logo_key]):
            optional_value = handle_nan(data.iloc[0][optional_logo_key], f"")
            template += f"<li class='indent justify left'>{optional_value}</li>"

        if optional_opsional_key in data.columns and not pd.isna(data.iloc[0][optional_opsional_key]):
            optional_value = handle_nan(data.iloc[0][optional_opsional_key], f"")
            template += f"<li class='indent justify left'>{optional_value}</li>"

    template += """
            </ul>
        </div>
    </body>
    </html>
    """

    return html_content

    # Save HTML
    output_html_path = f'isi_{timestamp}.html'
    with open(output_html_path, 'w', encoding='utf-8') as html_file:
        html_file.write(template)

    print("\nProses selesai. File HTML yang indah tersedia di pdf.html.")
    return template, output_html_path
    
def generate_pdf_from_html(html_content, output_pdf):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name, file_extension = os.path.splitext(output_pdf)
    stamped_output_pdf = f"{file_name}_{timestamp}{file_extension}"

    with open('pdf.html', 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

    pdfkit.from_file('pdf.html', stamped_output_pdf)

    print(f"Dokumen html berhasil disimpan di isi_{timestamp}.html")
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

def main():
    # Meminta input file Excel dari pengguna
    input_file_path = get_input_file_path()
    
    # Baca data dari file Excel
    data = pd.read_excel(input_file_path)

    
    # Panggil fungsi untuk membuat HTML
    html_content = generate_html(data, keyword)

    # Panggil fungsi untuk membuat PDF
    pdf_path = generate_pdf_from_html(html_content, "final_output.pdf")
    beauty_pdf(data)

if __name__ == "__main__":
    main()
