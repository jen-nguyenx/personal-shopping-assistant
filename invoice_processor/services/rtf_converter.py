from django.conf import settings
import os
from striprtf.striprtf import rtf_to_text

def convert_rtf_to_csv(rtf_path, csv_filename):
    # Read RTF and convert to plain text
    with open(rtf_path, 'r') as file:
        rtf_content = file.read()
        text_content = rtf_to_text(rtf_content)

    # Set the path to save the CSV file in the data folder
    csv_path = os.path.join(settings.DATA_DIR, csv_filename)

    # Write the plain text to a CSV file
    with open(csv_path, 'w', newline='') as csvfile:
        for line in text_content.strip().split('\n'):
            csvfile.write(line + '\n')

    print(f"File saved in: {csv_path}")
