import time
import os
import pandas as pd
import requests
from scholarly import scholarly

# ------------------------- Step 1: Fetch Professor Data -------------------------
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

def save_to_csv(data_list, output_csv):
    """Saves collected professor data to a CSV file."""
    try:
        df = pd.DataFrame(data_list)
        df.to_csv(output_csv, index=False)
        print(f"✅ Saved {len(data_list)} professor records to {output_csv}")
    except Exception as e:
        print(f"Error saving to CSV {output_csv}: {e}")

def get_all_professor_data(input_file, output_csv):
    """Processes professor names and fetches their data."""
    professors = read_professor_names(input_file)
    results = []
    
    if not professors:
        print("No professor names found in the file.")
        return
    
    for professor in professors:
        print(f"🔍 Fetching data for: {professor}")
        data = collect_data(professor)
        
        if data:  # Only save if data is found
            results.append(data)
        
        time.sleep(3)  # Delay to prevent rate limiting
    
    if results:
        save_to_csv(results, output_csv)
    else:
        print("❌ No valid professor data found.")

# ------------------------- Step 2: Clean CSV File -------------------------
def clean_csv(input_csv):
    """Removes rows where any column contains 'unknown'."""
    try:
        df = pd.read_csv(input_csv)
        df_cleaned = df[~df.apply(lambda row: row.astype(str).str.contains('unknown', case=False, na=False).any(), axis=1)]
        df_cleaned.to_csv(input_csv, index=False)
        print("✅ Cleaned CSV file saved successfully.")
    except Exception as e:
        print(f"Error cleaning CSV file {input_csv}: {e}")

# ------------------------- Step 3: Remove Commas from Text File -------------------------
def remove_commas(file_path):
    """Reads a file, removes commas, and overwrites it."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().replace(",", "")

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

        print("✅ All commas have been removed successfully!")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# ------------------------- Step 4: Enrich Data with API -------------------------
API_KEY = os.getenv("TOGETHER_API_KEY", "tgp_v1_Ga1yHScBrASp9zatw7sr-LcMzzFk5t0m_BFNDOVaRaA")  # Replace with your API key

TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"

def get_college_and_research_interests(name, affiliation):
    """Fetch college and research interests using Together API."""
    prompt = (f"For the professor {name}, affiliated with {affiliation}, "
              f"identify:\n1. The main university or company they belong to (only one).\n"
              f"2. Two primary research interests.\n"
              f"Format response strictly as:\n"
              f"University/Company, Research Interest 1, Research Interest 2\n"
              f"Example: Stanford University, Machine Learning, Computer Vision")

    data = {
        "model": "deepseek-ai/DeepSeek-V3",
        "messages": [{"role": "user", "content": prompt}]
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(TOGETHER_API_URL, headers=headers, json=data)

        if response.status_code == 200:
            response_data = response.json()
            ai_response = response_data["choices"][0]["message"]["content"].strip()

            print(f"Response for {name}: {ai_response}")  # Debugging log

            parts = ai_response.split(",")  # Ensure response is properly formatted
            if len(parts) >= 3:
                college = parts[0].strip()
                research_1 = parts[1].strip()
                research_2 = parts[2].strip()
                return college, research_1, research_2

        print(f"⚠️ Unexpected response format for {name}: {response.text}")
        return "Unknown", "Unknown", "Unknown"

    except requests.exceptions.RequestException as e:
        print(f"❌ API Error for {name}: {str(e)}")
        return "Error", "Error", "Error"

def enrich_data_with_api(csv_file):
    """Enriches professor data with additional research information."""
    try:
        df = pd.read_csv(csv_file)

        for col in ["College/Company", "Research Interest 1", "Research Interest 2"]:
            if col not in df.columns:
                df[col] = ""

        for index, row in df.iterrows():
            name = row["Name"]
            affiliation = row["Affiliation"]

            print(f"🔍 Processing: {name} ({affiliation})...")
            college, research_1, research_2 = get_college_and_research_interests(name, affiliation)

            df.at[index, "College/Company"] = college
            df.at[index, "Research Interest 1"] = research_1
            df.at[index, "Research Interest 2"] = research_2

            time.sleep(5)  # Exponential backoff to avoid rate limits

        df.to_csv(csv_file, index=False)
        print(f"✅ Updated data saved to {csv_file}")

    except Exception as e:
        print(f"Error processing API enrichment: {e}")

# ------------------------- Run the Full Pipeline -------------------------
if __name__ == "__main__":
    input_txt = r"C:\Users\krish\Desktop\sem6\llm\project\test.txt"
    output_csv = r"C:\Users\krish\Desktop\sem6\llm\project\temp_professor_data.csv"
    output_txt = r"C:\Users\krish\Desktop\sem6\llm\project\temp_professor_data.txt"

    print("🚀 Starting Data Collection Pipeline...")
    get_all_professor_data(input_txt, output_csv)
    clean_csv(output_csv)
    remove_commas(output_txt)
    enrich_data_with_api(output_csv)
    print("✅ Pipeline Execution Completed!")
