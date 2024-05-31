import pymupdf

from general import google

book, params = google.open_google()
book.worksheet('pdf').update_cell(1, 1, 'test')

