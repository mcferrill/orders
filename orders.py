#!/usr/bin/env python3

import fitz # PyMuPDF
import re
import sys

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

# Function to convert extracted text to desired format
def convert_to_single_line_order(extracted_text):
    # Split the text into individual medication sections
    medications = extracted_text.split('Initial Med List:')[1]
    sections = medications.split('Medication:')[1:]

    orders = []

    for section in sections:
        lines = section.splitlines()

        # Medication
        s = lines[0].strip()

        if 'Dosage:' in section:
            s += ' ' + re.search(r"Dosage:(.+)", section).group(1).strip()

        # Route placeholder
        s += ' PO'

        if 'Frequency:' in section:
            s += ' ' + re.search(r"Frequency:(.+)", section).group(1).strip()

        # Find instructions line and handle multiline
        instructions = ''
        if 'Instructions:' in section:
            instructions = section.split('Instructions:')[1]
        elif 'Sig:' in section:
            instructions = section.split('Sig:')[1]
        if instructions:
            s += ' ' + instructions.split('Provider')[0].strip().replace('\n', ' ')
        # instructions_index = lines.index('Instructions') + 1
        # instructions_lines = []
        # for i in range(instructions_index, len(lines)):
        #     if lines[i].strip() == "Provider":
        #         break
        #     instructions_lines.append(lines[i].strip())
        # instructions = " ".join(instructions_lines)

        if 'Start Date:' in section:
            s += ' ' + re.search(r"Start Date:(\S+)", section).group(1)

        # Duration
        s += ' until discontinued'

        if 'Provider:' in section:
            provider_result = re.search(r"Provider\n(.+)", section)
            if provider_result:
                s += ' Dr. ' + provider_result.group(1).strip()

        orders.append(s)

    return orders


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('''usage: python orders.py PDF_NAME
To output to file use:
python orders.py PDF_NAME > OUTPUT.txt''')
    text = extract_text_from_pdf(sys.argv[1])
    for order in convert_to_single_line_order(text):
        print(order)
        print()
