import pymupdf

from general import google

book, params = google.open_google()
print(params)
book.worksheet('pdf').update_cell(1, 1, 'test')

