import pandas as pd

# Load the CSV file
file_path = "C:\\Users\\krish\\Desktop\\sem6\\llm\\project\\4_updated_professor_data.csv"
df = pd.read_csv(file_path)

# Remove duplicates
df_cleaned = df.drop_duplicates()

# Save the cleaned file
output_path = "C:\\Users\\krish\\Desktop\\sem6\\llm\\project\\4_updated_professor_data.csv"
df_cleaned.to_csv(output_path, index=False)

print(f"Duplicates removed! Cleaned file saved at: {output_path}")
