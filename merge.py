import io

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
        print(response.content)
        file_list.append(response.content)

# Creating new empty pdf
merged_pdf = pymupdf.open()

# Adding the files to empty pdf
for file in file_list:
    pdf_doc = pymupdf.open(file)
    # Append each page to the merged pdf
    for page_num in range(pdf_doc.page_count):
        merged_pdf.insert_pdf(pdf_doc, from_page=page_num, to_page=page_num)

    # closing the current pdf_doc
    pdf_doc.close()

# Reading and saving merged pdf into buffer
pdf_buffer = io.BytesIO
merged_pdf.save(pdf_buffer)
merged_pdf.close()

# Writing merged pdf to binary string
pdf_string = pdf_buffer.getvalue()

# Closing buffer
pdf_buffer.close()

book.worksheet('pdf').update_cell(1, 1, pdf_string)
