import pandas as pd

# Load the CSV file
df = pd.read_csv(r"C:\Users\krish\Desktop\sem6\llm\project\temp_professor_data.csv")

# Remove rows where any column contains 'unknown'
df_cleaned = df[~df.apply(lambda row: row.astype(str).str.contains('unknown', case=False, na=False).any(), axis=1)]

# Save the cleaned CSV file (overwrite original file)
df_cleaned.to_csv(r"C:\Users\krish\Desktop\sem6\llm\project\temp_professor_data.csv", index=False)

print("Cleaned CSV file saved successfully.")