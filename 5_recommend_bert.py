import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util

# Load the pre-trained BERT model for sentence similarity
model = SentenceTransformer('distilbert-base-nli-mean-tokens')

# Path to your dataset
csv_path = r"C:\Users\krish\Desktop\sem6\llm\project\4_updated_professor_data.csv"

# Load the dataset
df = pd.read_csv(csv_path)

# Ensure column names are correct based on your dataset
# If column names are different, update them accordingly
df.columns = ["Name", "Description", "Citations", "h-index", "i10-index", "Affiliation", "Field1", "Field2"]

# Combine relevant columns into a single text description
df["Full_Description"] = df["Name"] + ", " + df["Description"] + ", " + df["Affiliation"].fillna("") + ", " + df["Field1"].fillna("") + ", " + df["Field2"].fillna("")

# Generate embeddings for each professor's description
descriptions = df["Full_Description"].tolist()
description_embeddings = model.encode(descriptions, convert_to_tensor=True)

# Function to get top 5 professors for a given query
def recommend_professors(user_query, top_n=5):
    # Encode user query
    query_embedding = model.encode(user_query, convert_to_tensor=True)
    
    # Compute cosine similarity between query and each professor's description
    similarities = util.pytorch_cos_sim(query_embedding, description_embeddings)
    
    # Get top N matching indices
    top_indices = np.argsort(-similarities.numpy())[0][:top_n]  # Negative for descending sort
    
    # Fetch and display top professors
    top_professors = df.iloc[top_indices]
    return top_professors[["Name", "Affiliation", "Field1", "Field2", "Citations", "h-index"]]

# Example Query
user_query = "As a student moving into engineering, I want to learn from the best minds in Computer Science from NIT colleges."
top_professors = recommend_professors(user_query)

# Display results
print(top_professors)
