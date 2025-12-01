"""
pdf_to_png.py

Creates "schedule_chart.png" out of "schedule_chart.pdf" so it can be added to the README.
"""

from pdf2image import convert_from_path

pages = convert_from_path('../schedule_chart.pdf', dpi=200)
pages[0].save('../schedule_chart.png', 'PNG')  # saves first page as PNG
