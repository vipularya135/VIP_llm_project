import csv
import re

def convert_txt_to_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = file.read()
    
    # Splitting based on the separator lines
    entries = data.strip().split("----------------------------------------")
    
    # Define the output CSV file headers
    # headers = ["Institution", "Name", "Affiliation", "h-index", "i10-index", "Citations"]
    headers = [ "Name", "Affiliation", "h-index", "i10-index", "Citations"]

    # Open CSV file to write data
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(headers)
        
        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue
            
            # Extract data fields using regex
            # institution_match = re.search(r"Institution: (.+)", entry)
            name_match = re.search(r"Name: (.+)", entry)
            affiliation_match = re.search(r"Affiliation: (.+)", entry)
            h_index_match = re.search(r"h-index: (\d+)", entry)
            i10_index_match = re.search(r"i10-index: (\d+)", entry)
            citations_match = re.search(r"Citations: (\d+)", entry)
            
            # Extracted values
            # institution = institution_match.group(1) if institution_match else ""
            name = name_match.group(1) if name_match else ""
            affiliation = affiliation_match.group(1) if affiliation_match else ""
            h_index = h_index_match.group(1) if h_index_match else ""
            i10_index = i10_index_match.group(1) if i10_index_match else ""
            citations = citations_match.group(1) if citations_match else ""
            
            # Write row to CSV
            csv_writer.writerow([name, affiliation, h_index, i10_index, citations])

# Usage Example
convert_txt_to_csv("3_professor_data.txt", "3_professor_data.csv")
