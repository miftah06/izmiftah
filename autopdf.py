import pandas as pd
from datetime import datetime
import os
from weasyprint import HTML

def handle_nan(value, default_value=""):
    return default_value if pd.isna(value) else value

def generate_html(data, keyword):

    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Filter the DataFrame based on the provided keyword
    filtered_data = data[data['Keyword'] == keyword]

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

    return html_content

def generate_pdf_from_html(html_content, output_pdf):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name, file_extension = os.path.splitext(output_pdf)
    stamped_output_pdf = f"{file_name}_{timestamp}{file_extension}"

    # Save HTML to a temporary file
    with open('pdf.html', 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

    # Convert HTML to PDF using WeasyPrint
    HTML(string=open('pdf.html', 'r', encoding='utf-8').read()).write_pdf(stamped_output_pdf)

    print(f"Dokumen HTML berhasil diubah menjadi PDF dan disimpan sebagai {stamped_output_pdf}")
    return stamped_output_pdf  # Mengembalikan path PDF yang dihasilkan

def beauty_pdf(data):
    # Your FPDF code for enhancing the PDF can be added here
    pass

def main():
    # Meminta input file Excel dari pengguna
    input_file_path = input("Masukkan nama file Excel: ")

    # Baca data dari file Excel
    data = pd.read_excel(input_file_path)

    # Meminta keyword dari pengguna
    keyword = input("Masukkan kata kunci: ")

    # Panggil fungsi untuk membuat HTML
    html_content = generate_html(data, keyword)

    # Panggil fungsi untuk membuat PDF
    pdf_path = generate_pdf_from_html(html_content, "final_output.pdf")
    beauty_pdf(data)

if __name__ == "__main__":
    main()
