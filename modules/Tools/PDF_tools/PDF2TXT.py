import PyPDF2

def pdf_to_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text


pdf_file_path = '<<file_path>>'
output_text = pdf_to_text(pdf_file_path)
print(output_text)