import os
import json
import logging
import pdfplumber
import pytesseract
import nltk
nltk.data.path.append('/home/jimmychestnut/nltk_data')
from nltk.tokenize import sent_tokenize

# Download the punkt tokenizer data
nltk.download('punkt')

# Configure logging
logging.basicConfig(
    filename='ocr_processing.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define paths
input_base = "/media/jimmychestnut/bastion/data/raw/Documents"
output_base = "/media/jimmychestnut/bastion/data/processed"

def process_pdf(input_path):
    try:
        # Compute the relative path of the input file
        rel_path = os.path.relpath(input_path, start=input_base)

        # Construct the output path using the relative path
        output_path = os.path.join(output_base, rel_path)

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with pdfplumber.open(input_path) as pdf:
            file_name = os.path.splitext(os.path.basename(input_path))[0]
            all_chunks = []

            for page_number, page in enumerate(pdf.pages, start=1):
                # Extract text from the page
                text = page.extract_text()
                if not text:
                    # Perform OCR if no text is extracted
                    logging.info(f"No text found on page {page_number}, performing OCR")
                    image = page.to_image()
                    text = pytesseract.image_to_string(image.original)

                # Tokenize the text into sentences
                sentences = sent_tokenize(text)
                all_chunks.extend(sentences)

            # Save the extracted text as JSON
            output_file = os.path.splitext(output_path)[0] + ".json"
            with open(output_file, "w", encoding="utf-8") as json_file:
                json.dump(all_chunks, json_file, indent=4)

            logging.info(f"Processed PDF: {input_path} -> {output_file}")
    except Exception as e:
        logging.error(f"Error processing {input_path}: {e}")

# Run the PDF processing
process_pdf("/media/jimmychestnut/bastion/data/raw/Documents/Official Records/Medical/Med Record/Chestnut_James_Wayne_6303___sensitive.pdf")

