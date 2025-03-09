# import google.generativeai as genai
# import pandas as pd
# import time
# import os

# API_KEY = "AIzaSyBey3g5o9XGkuWK6PGuim8cghj4QvfGz1o"  # Replace with your actual API key
# genai.configure(api_key=API_KEY)

# # File paths
# input_file = r"C:\Users\krish\OneDrive\Desktop\sem6\llm\project\test1.csv"
# output_file = r"C:\Users\krish\OneDrive\Desktop\sem6\llm\project\updated_professor_data.csv"

# # Function to extract college and research interests
# def get_college_and_research_interests(name, affiliation):
#     prompt = (f"For the professor {name}, affiliated with {affiliation}, "
#               f"identify:\n1. The main university or company they belong to (only one).\n"
#               f"2. Two primary research interests.\n"
#               f"Format response strictly as:\n"
#               f"University/Company, Research Interest 1, Research Interest 2\n"
#               f"Example: Stanford University, Machine Learning, Computer Vision")

#     try:
#         model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")
#         response = model.generate_content(prompt)

#         if response and response.text:
#             print(f"Response for {name}: {response.text.strip()}")  # Debugging log

#             parts = response.text.strip().split(",")

#             # Ensure response has 3 parts (College, Research1, Research2)
#             if len(parts) >= 3:
#                 college = parts[0].strip()
#                 research_1 = parts[1].strip()
#                 research_2 = parts[2].strip()
#                 return college, research_1, research_2

#         return "Unknown", "Unknown", "Unknown"  # Default if response fails

#     except Exception as e:
#         print(f"API Error for {name}: {str(e)}")  # Debugging log
#         return "Error", "Error", "Error"

# # Read dataset
# df = pd.read_csv(input_file)

# # Add new columns
# df["College/Company"] = ""
# df["Research Interest 1"] = ""
# df["Research Interest 2"] = ""

# # Process each professor
# for index, row in df.iterrows():
#     name = row["Name"]
#     affiliation = row["Affiliation"]

#     print(f"Processing: {name} ({affiliation})...")  # Debugging log
#     college, research_1, research_2 = get_college_and_research_interests(name, affiliation)

#     df.at[index, "College/Company"] = college
#     df.at[index, "Research Interest 1"] = research_1
#     df.at[index, "Research Interest 2"] = research_2

#     # Sleep to avoid API rate limits
#     time.sleep(5)  # Increased delay to prevent issues

# # Save updated dataset
# df.to_csv(output_file, index=False)
# print(f"✅ Updated data saved to {output_file}")



import requests
import pandas as pd
import time
import os

# Load API Key Securely (Set as an environment variable)
API_KEY = "tgp_v1_Ga1yHScBrASp9zatw7sr-LcMzzFk5t0m_BFNDOVaRaA"  # Ensure this is set in your system
if not API_KEY:
    raise ValueError("❌ API key is missing. Set TOGETHER_API_KEY as an environment variable.")

# Together API endpoint
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"

# File Paths
input_file = r"C:\Users\krish\Desktop\sem6\llm\project\temp_professor_data.csv"
output_file = r"C:\Users\krish\Desktop\sem6\llm\project\temp_professor_data.csv"

# Function to extract college and research interests using DeepSeek-V3
def get_college_and_research_interests(name, affiliation):
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
        print(f"❌ API Error for {name}: {str(e)}")  # Debugging log
        return "Error", "Error", "Error"

# Read dataset
df = pd.read_csv(input_file)

# Add new columns if they don't exist
for col in ["College/Company", "Research Interest 1", "Research Interest 2"]:
    if col not in df.columns:
        df[col] = ""

# Process each professor
for index, row in df.iterrows():
    name = row["Name"]
    affiliation = row["Affiliation"]

    print(f"🔍 Processing: {name} ({affiliation})...")  # Debugging log
    college, research_1, research_2 = get_college_and_research_interests(name, affiliation)

    df.at[index, "College/Company"] = college
    df.at[index, "Research Interest 1"] = research_1
    df.at[index, "Research Interest 2"] = research_2

    # Implementing Exponential Backoff to avoid rate limits
    time.sleep(5)  # You can adjust this based on API rate limits

# Save updated dataset
df.to_csv(output_file, index=False)
print(f"✅ Updated data saved to {output_file}")
