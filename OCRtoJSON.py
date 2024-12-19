import os
import json
import logging
from PIL import Image
import pytesseract

# If Tesseract is not in the system PATH, specify its location:
# pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

# Set input and output directories
input_dir = "/media/jimmychestnut/bastion/data/raw/Documents/Official Records/Army/Army Personnel File$"
output_base = "/media/jimmychestnut/bastion/data/processed"

# Configure logging
logging.basicConfig(
    filename='ocr_processing.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Function to process all .tif files recursively
def process_tif_files(input_dir, output_base):
    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            if filename.lower().endswith(".tif"):
                # Construct full input path
                input_path = os.path.join(root, filename)
                
                # Determine relative path from the raw directory
                rel_path = os.path.relpath(input_path, start="/media/jimmychestnut/bastion/data/raw")
                # Remove the original extension and add .json
                rel_path_json = os.path.splitext(rel_path)[0] + ".json"
                
                # Construct the output path in the processed directory
                output_path = os.path.join(output_base, rel_path_json)
                
                # Ensure all parent directories exist
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Perform OCR
                try:
                    image = Image.open(input_path)
                    ocr_text = pytesseract.image_to_string(image)

                    # Create a JSON object
                    output_data = {
                        "filename": filename,
                        "ocr_text": ocr_text,
                        "metadata": {
                            "source": "Army Personnel File"
                        }
                    }

                    # Write JSON output
                    with open(output_path, "w", encoding="utf-8") as json_file:
                        json.dump(output_data, json_file, indent=4)

                    logging.info(f"Processed: {input_path} -> {output_path}")
                except Exception as e:
                    logging.error(f"Error processing {input_path}: {e}")

# Run the OCR processing
process_tif_files(input_dir, output_base)
