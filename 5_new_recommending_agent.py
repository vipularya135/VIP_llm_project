import pandas as pd
from sentence_transformers import SentenceTransformer, util

def load_data(file_path):
    df = pd.read_csv(file_path)
    df["Combined_Research"] = df[["Research Interest 1", "Research Interest 2"]].fillna('').agg(' '.join, axis=1)
    return df

def filter_data(df, user_query):
    user_query_lower = user_query.lower()
    
    # If query specifies an institution (e.g., "IIT"), filter by affiliation
    if "iit" in user_query_lower:
        df = df[df["Affiliation"].str.contains("IIT", case=False, na=False)]
    elif "university" in user_query_lower:
        df = df[df["Affiliation"].str.contains("University", case=False, na=False)]
    elif "mit" in user_query_lower:
        df = df[df["Affiliation"].str.contains("MIT", case=False, na=False)]
    
    return df

def recommend_professors(user_query, df, top_n=3):
    df = filter_data(df, user_query)  # Apply filtering based on user query
    
    if df.empty:
        return "No matching professors found based on your query."
    
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Pretrained Transformer Model
    research_embeddings = model.encode(df["Combined_Research"].tolist(), convert_to_tensor=True)
    user_embedding = model.encode(user_query, convert_to_tensor=True)
    
    similarities = util.pytorch_cos_sim(user_embedding, research_embeddings)[0]
    top_indices = similarities.argsort(descending=True)[:top_n]
    recommended_df = df.iloc[top_indices.tolist()]
    
    recommended_df["Citations"] = pd.to_numeric(recommended_df["Citations"], errors='coerce')
    recommended_df = recommended_df.sort_values(by="Citations", ascending=False)
    
    return recommended_df[["Name", "Affiliation", "Citations", "h-index", "Research Interest 1", "Research Interest 2"]]

# Load Data
data_path = "C:\\Users\\krish\\OneDrive\\Desktop\\sem6\\llm\\project\\4_updated_professor_data.csv"
df = load_data(data_path)

# Example Usage
user_query = "As a student moving into engineering, I want to learn from the best minds in Computer Science. Can you give me the names of the top professors in this field from NIT Colleges only?" 


recommendations = recommend_professors(user_query, df)

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
print(recommendations.to_string(index=False))
