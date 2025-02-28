# import google.generativeai as genai

# # Set up Gemini API
# API_KEY = "AIzaSyClUe23xTltQKrUhgLbH9eLkiv_6uEc8AY"  # Replace with your actual key
# genai.configure(api_key=API_KEY)

# def get_professors(college_name):
#     prompt = f"List only the names of all professors from {college_name}. Provide only names, no extra text."
    
#     try:
#         model = genai.GenerativeModel("gemini-pro")
#         response = model.generate_content(prompt)
        
#         # Extract and format the response
#         if response and response.text:
#             professor_names = response.text.strip().split("\n")
#             return [name.strip() for name in professor_names if name.strip()]
#         else:
#             return ["No data found."]
    
#     except Exception as e:
#         return [f"Error: {str(e)}"]

# # Example usage
# college_name = "IIT bombay"
# professors = get_professors(college_name)
# print(professors)


import google.generativeai as genai
import time

# Set up Gemini API
API_KEY = "AIzaSyClUe23xTltQKrUhgLbH9eLkiv_6uEc8AY"  # Replace with your actual key
genai.configure(api_key=API_KEY)

# File paths
input_file = r"C:\Users\krish\OneDrive\Desktop\sem6\llm\top100_Engineering_Colleges.txt"
output_file = r"C:\Users\krish\OneDrive\Desktop\sem6\llm\professors_list.txt"

# Function to get professors for a given college
def get_professors(college_name):
    prompt = f"List only the names of all professors from {college_name}. Provide only names, no extra text."

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        
        if response and response.text:
            professor_names = response.text.strip().split("\n")
            return [name.strip() for name in professor_names if name.strip()]
        else:
            return ["No data found."]
    
    except Exception as e:
        return [f"Error: {str(e)}"]

# Read college names from file
with open(input_file, "r", encoding="utf-8") as f:
    college_list = [line.strip() for line in f.readlines() if line.strip()]

# Process in chunks to avoid API limits
chunk_size = 10  # Adjust based on response length
total_colleges = len(college_list)

with open(output_file, "w", encoding="utf-8") as f_out:
    for i in range(0, total_colleges, chunk_size):
        chunk = college_list[i:i+chunk_size]
        
        for college in chunk:
            print(f"Fetching professors from: {college} ...")
            professors = get_professors(college)
            
            # Write results to file
            f_out.write(f"\n{college}:\n")
            f_out.write("\n".join(professors) + "\n")
        
        print(f"Processed {i+chunk_size} out of {total_colleges} colleges.\n")
        
        # To prevent hitting API rate limits, wait before next batch
        time.sleep(5)

print("Data saved to professors_list.txt ✅")
