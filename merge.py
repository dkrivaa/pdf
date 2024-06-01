from io import BytesIO
import os
import base64
import pymupdf
import requests

from general import google


# Opening Google and getting parameters passed (download urls)
book, params = google.open_google()
print(params)
# Making list of download urls passed
downloadUrls = list(params.values())

# Getting the files to merge
file_list = []
for url in downloadUrls:
    response = requests.get(url)
    if response.status_code == 200:
        # Create a temporary file to save the PDF content
        file_name = os.path.basename(url)[-5:] + '.pdf'
        with open(file_name, 'wb') as pdf_file:
            pdf_file.write(response.content)
            file_list.append(file_name)

# Creating new empty pdf
merged_pdf = pymupdf.open()

# Adding the files to empty pdf
for file in file_list:
    with pymupdf.open(file) as pdf:
        # Append each page to the merged pdf
        for page_num in range(pdf.page_count):
            merged_pdf.insert_pdf(pdf, from_page=page_num, to_page=page_num)

# Reading and saving merged pdf into buffer
pdf_buffer = BytesIO()
merged_pdf.save(pdf_buffer)
merged_pdf.close()

# Clean up temporary files
for file in file_list:
    os.remove(file)

# Writing merged pdf to binary string
pdf_string = pdf_buffer.getvalue()

# Closing buffer
pdf_buffer.close()

# Convert the binary string to a format that can be inserted into a cell
pdf_base64 = base64.b64encode(pdf_string).decode('utf-8')

book.worksheet('pdf').update_cell(1, 1, pdf_base64)
