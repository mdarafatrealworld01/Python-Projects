#pip install PyMuPDF

# Extract invoice data from a PDF file

import fitz  # PyMuPDF
import re

def extract_invoice_data(pdf_path):
    # Open the PDF file
    document = fitz.open(pdf_path)
    invoice_data = {}

    # Regular expressions for extracting data
    invoice_number_pattern = r'Invoice Number:\s*(\S+)'
    date_pattern = r'Date:\s*(\S+)'
    total_amount_pattern = r'Total Amount:\s*\$?(\d+(\.\d{2})?)'

    # Iterate through each page in the PDF
    for page_num in range(len(document)):
        page = document[page_num]
        text = page.get_text()

        # Search for patterns in the text
        invoice_number_match = re.search(invoice_number_pattern, text)
        date_match = re.search(date_pattern, text)
        total_amount_match = re.search(total_amount_pattern, text)

        # Extract data if found
        if invoice_number_match:
            invoice_data['Invoice Number'] = invoice_number_match.group(1)
        if date_match:
            invoice_data['Date'] = date_match.group(1)
        if total_amount_match:
            invoice_data['Total Amount'] = total_amount_match.group(1)

    # Close the document
    document.close()

    return invoice_data

if __name__ == "__main__":
    pdf_path = 'C:\\Users\\Md Arafat\\Desktop\\Advance level\\example.pdf'  # Change this to your PDF file path
    invoice_data = extract_invoice_data(pdf_path)

    # Print the extracted invoice data
    print("Extracted Invoice Data:")
    for key, value in invoice_data.items():
        print(f"{key}: {value}")