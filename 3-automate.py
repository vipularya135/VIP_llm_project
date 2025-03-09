# import time
# import pandas as pd
# from scholarly import scholarly

# # Function to get professor data
# def collect_data(professor_name, institution):
#     try:
#         search_query = scholarly.search_author(professor_name)
#         author = next(search_query)  # Get first search result
#         author_info = scholarly.fill(author)  # Fetch full details

#         data = {
#             "Institution": institution,
#             "Name": author_info.get('name', ''),
#             "Affiliation": author_info.get('affiliation', ''),
#             "h-index": author_info.get('hindex', 0),
#             "i10-index": author_info.get('i10index', 0),
#             "Citations": author_info.get('citedby', 0)
#         }
#         return data

#     except StopIteration:
#         print(f"No data found for: {professor_name}")
#         return None  # No valid data

#     except Exception as e:
#         print(f"Error fetching data for {professor_name}: {e}")
#         return None  # Handle unexpected errors

# # Read professor names with institutions
# def read_professor_names(file_path):
#     professors = []
#     institution = None  # Track the current institution

#     try:
#         with open(file_path, "r", encoding="utf-8") as file:
#             for line in file:
#                 line = line.strip()

#                 if line.endswith(":"):  # Institution name detected
#                     institution = line[:-1]  # Remove colon
#                 elif line.startswith("-"):  # Professor name detected
#                     professor_name = line[2:]  # Remove "- - " prefix
#                     if institution:
#                         professors.append((professor_name, institution))  # Store (professor, institution)
        
#         return professors

#     except Exception as e:
#         print(f"Error reading file {file_path}: {e}")
#         return []  # Return empty list on failure

# # Save data to a text file
# def save_to_txt(data_list, output_txt):
#     try:
#         with open(output_txt, "w", encoding="utf-8") as file:
#             for data in data_list:
#                 file.write(f"Institution: {data['Institution']}\n")
#                 file.write(f"Name: {data['Name']}\n")
#                 file.write(f"Affiliation: {data['Affiliation']}\n")
#                 file.write(f"h-index: {data['h-index']}\n")
#                 file.write(f"i10-index: {data['i10-index']}\n")
#                 file.write(f"Citations: {data['Citations']}\n")
#                 file.write("-" * 40 + "\n")  # Separator between entries
#         print(f"Saved {len(data_list)} professor records to {output_txt}")

#     except Exception as e:
#         print(f"Error saving to file {output_txt}: {e}")

# # Main function to get data for all professors
# def get_all_professor_data(input_file, output_txt):
#     professors = read_professor_names(input_file)
#     results = []

#     if not professors:
#         print("No professor names found in the file.")
#         return

#     for professor, institution in professors:
#         print(f"Fetching data for: {professor} ({institution})")
#         data = collect_data(professor, institution)

#         if data:  # Only save if data is found
#             results.append(data)

#         time.sleep(3)  # Delay to prevent rate limiting

#     # Save results to TXT file
#     if results:
#         save_to_txt(results, output_txt)
#     else:
#         print("No valid professor data found.")

# # File paths
# input_file = "test.txt"
# output_txt = "3_temp_professor_data.txt"

# # Run the script
# get_all_professor_data(input_file, output_txt)

import time
import pandas as pd
from scholarly import scholarly

def collect_data(professor_name):
    """Fetches Google Scholar data for a given professor."""
    try:
        search_query = scholarly.search_author(professor_name)
        author = next(search_query, None)  # Get first search result safely
        
        if not author:
            print(f"No data found for: {professor_name}")
            return None
        
        author_info = scholarly.fill(author)  # Fetch full details
        data = {
            "Name": author_info.get('name', ''),
            "Affiliation": author_info.get('affiliation', ''),
            "h-index": author_info.get('hindex', 0),
            "i10-index": author_info.get('i10index', 0),
            "Citations": author_info.get('citedby', 0)
        }
        return data
    except Exception as e:
        print(f"Error fetching data for {professor_name}: {e}")
        return None

def read_professor_names(file_path):
    """Reads professor names from a text file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            professors = [line.strip() for line in file if line.strip()]
        return professors
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []

def save_to_txt(data_list, output_txt):
    """Saves collected professor data to a text file."""
    try:
        with open(output_txt, "w", encoding="utf-8") as file:
            for data in data_list:
                file.write(f"Name: {data['Name']}\n")
                file.write(f"Affiliation: {data['Affiliation']}\n")
                file.write(f"h-index: {data['h-index']}\n")
                file.write(f"i10-index: {data['i10-index']}\n")
                file.write(f"Citations: {data['Citations']}\n")
                file.write("-" * 40 + "\n")  # Separator between entries
        print(f"Saved {len(data_list)} professor records to {output_txt}")
    except Exception as e:
        print(f"Error saving to file {output_txt}: {e}")

def get_all_professor_data(input_file, output_txt):
    """Processes professor names and fetches their data."""
    professors = read_professor_names(input_file)
    results = []
    
    if not professors:
        print("No professor names found in the file.")
        return
    
    for professor in professors:
        print(f"Fetching data for: {professor}")
        data = collect_data(professor)
        
        if data:  # Only save if data is found
            results.append(data)
        
        time.sleep(3)  # Delay to prevent rate limiting
    
    if results:
        save_to_txt(results, output_txt)
    else:
        print("No valid professor data found.")

# File paths
input_file = "test.txt"
output_txt = "temp_professor_data.txt"

# Run the script
get_all_professor_data(input_file, output_txt)
